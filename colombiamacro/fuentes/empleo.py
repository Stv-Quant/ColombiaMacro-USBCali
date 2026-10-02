"""Mercado laboral en detalle (DANE, GEIH): ocupados por rama y posicion, indicadores por sexo,
poblacion fuera de la fuerza de trabajo, zonas urbana y rural, y mercado laboral de la juventud.

Escribe (series sin desestacionalizar, como las publica el DANE):
  empleo_ramas.csv     fecha, rama, ocupados (miles)                     mensual, total nacional
  empleo_posicion.csv  fecha, posicion, ocupados (miles)                 mensual, total nacional
  empleo_sexo.csv      fecha, sexo, tgp, to, td, ts, ocupados, fuera_ft (miles)                     mensual, total nacional
  empleo_fuera_ft.csv  fecha, estudiando, hogar, otros (miles)           mensual, total nacional
  empleo_area.csv      fecha, area, tgp, to, td, ts                      trimestral (cabeceras / rural)
  empleo_jovenes.csv   fecha, td, td_h, td_m, tgp, nini, nini_h, nini_m  trimestre movil, 15 a 28 anos

Uso: python -m colombiamacro.fuentes.empleo [--local carpeta]
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

from colombiamacro.config import data
from colombiamacro.fuentes.banrep import write_if_changed
from colombiamacro.fuentes.demanda import HEADERS, descargar, enlace
from colombiamacro.fuentes.regional import MESES, _anio, _filas, _n

DANE_GEIH = "https://www.dane.gov.co/index.php/estadisticas-por-tema/mercado-laboral/empleo-y-desempleo"
DANE_JOV = "https://www.dane.gov.co/index.php/estadisticas-por-tema/mercado-laboral/mercado-laboral-de-la-juventud"
PATRONES = {"geih": (DANE_GEIH, r"/anex-GEIH-[a-z]{3}20\d{2}\.xlsx$"),
            "jov": (DANE_JOV, r"/anex-GEIHMLJ-[a-z]{3}-[a-z]{3}20\d{2}\.xlsx$")}
RAMAS = [("no informa", None), ("agricultura", "agro"), ("suministro de electricidad", "electricidad_mineria"),
         ("industrias manufactureras", "industria"), ("construccion", "construccion"), ("comercio", "comercio"),
         ("alojamiento", "alojamiento"), ("transporte", "transporte"), ("informacion", "informacion"),
         ("actividades financieras", "finanzas"), ("actividades inmobiliarias", "inmobiliarias"),
         ("actividades profesionales", "profesionales"), ("administracion publica", "gobierno"), ("actividades artisticas", "arte")]
POSICIONES = [("obrero, empleado particular", "asalariado_privado"), ("obrero, empleado del gobierno", "asalariado_publico"),
              ("empleado domestico", "domestico"), ("trabajador por cuenta propia", "cuenta_propia"), ("patron o empleador", "empleador"),
              ("trabajador familiar sin remuneracion", "sin_remuneracion"), ("jornalero o peon", "jornalero"), ("otro", "otro")]
TASAS = {"tasa global de participacion (tgp)": "tgp", "tasa de ocupacion (to)": "to", "tasa de desocupacion (td)": "td",
         "tasa de subocupacion (ts)": "ts", "poblacion ocupada": "ocupados", "poblacion fuera de la fuerza de trabajo": "fuera_ft"}


def _fechas_mensuales(anos, meses):
    out, ano = {}, None
    for c in range(1, len(meses)):
        if c < len(anos) and _anio(anos[c]):
            ano = _anio(anos[c])
        txt = _n(meses[c])
        m = MESES.get(txt[:3])
        f = _fin_periodo(meses[c])
        if f is not None:
            out[c] = f
        elif ano and m and len(txt) <= 4:
            out[c] = pd.Timestamp(ano, m, 1)
        elif ano and m:                                    # 'Ene - Mar' sin ano: el ano viene de la fila superior
            m2 = MESES.get(txt[-3:])
            if m2:
                out[c] = pd.Timestamp(ano + (1 if m2 < m else 0), m2, 1)
    return out


def _fin_periodo(txt):
    """'May - Jul 26' / 'Ene - Mar 07' / 'Oct - Dic 25' -> ultimo mes; 'Ene-Mar' sin ano -> None."""
    m = re.search(r"([A-Za-z]{3})\s*(\d{2})\s*$", str(txt or "").strip())
    if not m or m.group(1).lower()[:3] not in MESES:
        return None
    return pd.Timestamp(2000 + int(m.group(2)), MESES[m.group(1).lower()[:3]], 1)


def bloques(filas: list) -> list[tuple[str, dict, list]]:
    """Cada bloque 'Concepto' de una hoja: (titulo, {col: fecha}, filas de datos hasta la siguiente cabecera o 'Fuente')."""
    heads = [i for i, r in enumerate(filas) if r and _n(r[0]) == "concepto"]
    out = []
    for k, h in enumerate(heads):
        titulo = next((str(filas[j][0]).strip() for j in range(h - 1, max(h - 6, -1), -1)
                       if filas[j] and filas[j][0] and not _n(filas[j][0]).startswith("serie")), "")
        anos = filas[h]
        per = filas[h + 1]
        fechas = _fechas_mensuales(anos, per)
        if not fechas:                                     # trimestres moviles: el ano va en la etiqueta
            fechas = {c: f for c in range(1, len(per)) for f in [_fin_periodo(per[c])] if f is not None}
        fin = heads[k + 1] if k + 1 < len(heads) else len(filas)
        datos = []
        cuerpo = filas[h + 2:fin]
        for i, r in enumerate(cuerpo):
            vacia = not r or all(v in (None, "") for v in r[:3])
            if r and _n(r[0]).startswith("fuente"):
                break
            if vacia:
                sig = next((x for x in cuerpo[i + 1:] if x and any(v not in (None, "") for v in x[:3])), None)
                if sig is None or not any(isinstance(v, (int, float)) for v in sig[1:4]):
                    break                              # lo que sigue es otro bloque (titulo), no mas datos
                continue
            datos.append(r)
        out.append((titulo, fechas, datos))
    return out


def _serie(r, fechas):
    return {f: float(r[c]) for c, f in fechas.items() if c < len(r) and isinstance(r[c], (int, float)) and r[c] != 0}


def _largo(filas_bloque, fechas, mapa, col_clave, col_valor="ocupados"):
    out = []
    for r in filas_bloque:
        lab = _n(r[0])
        clave = next((c for pref, c in mapa if lab.startswith(pref)), "__")
        if clave in (None, "__"):
            continue
        for f, v in _serie(r, fechas).items():
            out.append({"fecha": f, col_clave: clave, col_valor: v})
    return pd.DataFrame(out)


def leer_ramas(geih: bytes) -> pd.DataFrame:
    titulo, fechas, datos = bloques(_filas(geih, "Ocupados TN_T13_rama"))[0]
    df = _largo(datos, fechas, RAMAS, "rama")
    if df["rama"].nunique() != 13:
        raise ValueError(f"GEIH ramas: {df['rama'].nunique()}")
    return df.sort_values(["rama", "fecha"])


def leer_posicion(geih: bytes) -> pd.DataFrame:
    titulo, fechas, datos = bloques(_filas(geih, "Ocupados TN_posición"))[0]
    df = _largo(datos, fechas, POSICIONES, "posicion")
    if df["posicion"].nunique() < 7:
        raise ValueError("GEIH posicion ocupacional incompleta")
    return df.sort_values(["posicion", "fecha"])


def _tasas(bloque, etiqueta, col):
    titulo, fechas, datos = bloque
    reg = {}
    for r in datos:
        k = TASAS.get(_n(r[0]))
        if k:
            for f, v in _serie(r, fechas).items():
                reg.setdefault(f, {})[k] = v
    df = pd.DataFrame.from_dict(reg, orient="index")
    df.index.name = "fecha"
    df = df.reset_index()
    df.insert(1, col, etiqueta)
    return df


def leer_sexo(geih: bytes) -> pd.DataFrame:
    bl = bloques(_filas(geih, "Total_nacional_IML_Sexo"))
    out = []
    for b in bl:
        t = _n(b[0])
        sexo = "hombres" if "hombres" in t else ("mujeres" if "mujeres" in t else None)
        if sexo:
            out.append(_tasas(b, sexo, "sexo"))
    df = pd.concat(out)
    if set(df["sexo"]) != {"hombres", "mujeres"}:
        raise ValueError("GEIH sexo incompleto")
    return df.sort_values(["sexo", "fecha"])


def leer_area(geih: bytes) -> pd.DataFrame:
    bl = bloques(_filas(geih, "Total nacional Trim"))
    out = []
    for b in bl:
        t = _n(b[0])
        area = "cabeceras" if t.startswith("total cabeceras") else ("rural" if "rural" in t else ("nacional" if t.startswith("total nacional") else None))
        if area:
            out.append(_tasas(b, area, "area"))
    df = pd.concat(out)
    if not {"cabeceras", "rural"} <= set(df["area"]):
        raise ValueError("GEIH zonas incompletas")
    return df.sort_values(["area", "fecha"])


def leer_fuera(geih: bytes) -> pd.DataFrame:
    titulo, fechas, datos = bloques(_filas(geih, "Pob_fuera_fuerza_trabajo_TN"))[0]
    mapa = [("estudiando", "estudiando"), ("oficios del hogar", "hogar"), ("otros", "otros")]
    df = _largo(datos, fechas, mapa, "k", "v").pivot(index="fecha", columns="k", values="v").reset_index()
    df.columns.name = None
    return df


def leer_jovenes(jov: bytes) -> pd.DataFrame:
    bl = bloques(_filas(jov, " Tnal trimestre móvil"))
    res = {}
    for b in bl:
        t = _n(b[0])
        suf = {"total nacional": "", "total nacional - hombres": "_h", "total nacional - mujeres": "_m"}.get(t)
        if suf is None:
            continue
        x = _tasas(b, "", "_").set_index("fecha")
        res["td" + suf] = x["td"]
        if suf == "":
            res["tgp"] = x["tgp"]
    nb = bloques(_filas(jov, "Jóvenes_NOE Tnal"))
    for titulo, fechas, datos in nb:
        for r in datos:
            lab = _n(r[0])
            if lab.startswith("proporcion de jovenes"):
                k = "nini_h" if "hombres" in lab else ("nini_m" if "mujeres" in lab else "nini")
                res[k] = pd.Series(_serie(r, fechas))
    df = pd.DataFrame(res)
    df.index.name = "fecha"
    if "nini" not in df or df["td"].dropna().empty:
        raise ValueError("GEIH juventud incompleta")
    return df.reset_index().sort_values("fecha")


def escribir(tablas: dict) -> None:
    for nombre, df in tablas.items():
        x = df.copy()
        x["fecha"] = pd.to_datetime(x["fecha"]).dt.strftime("%Y-%m-%d")
        ch = write_if_changed(x.reset_index(drop=True), data(nombre), float_format="%.4f")
        print(f"{nombre}: {len(x)} filas hasta {x['fecha'].max()} ({'actualizado' if ch else 'sin cambios'})")


def actualizar(local: Path | None = None) -> bool:
    cont = {}
    if local:
        for k, (_, pat) in PATRONES.items():
            hits = [p for p in Path(local).iterdir() if re.search(pat.lstrip("/"), p.name, re.I)]
            if hits:
                cont[k] = sorted(hits)[-1].read_bytes()
    else:
        s = requests.Session()
        for k, (pagina, pat) in PATRONES.items():
            try:
                r = s.get(pagina, timeout=40, headers=HEADERS)
                r.raise_for_status()
                cont[k] = descargar(enlace(r.text, pagina, pat), s)
                time.sleep(4)
            except Exception as exc:
                print(f"  ERROR descarga {k}: {exc}")
    ok = True
    for nombre, fn, clave in (("empleo_ramas.csv", leer_ramas, "geih"), ("empleo_posicion.csv", leer_posicion, "geih"),
                              ("empleo_sexo.csv", leer_sexo, "geih"), ("empleo_fuera_ft.csv", leer_fuera, "geih"),
                              ("empleo_area.csv", leer_area, "geih"), ("empleo_jovenes.csv", leer_jovenes, "jov")):
        try:
            escribir({nombre: fn(cont[clave])})
        except Exception as exc:
            ok = False
            print(f"  ERROR {nombre}: {exc}")
    return ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--local", type=Path)
    a = ap.parse_args()
    sys.exit(0 if actualizar(a.local) else 1)
