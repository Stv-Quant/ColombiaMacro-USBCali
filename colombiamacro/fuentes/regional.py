"""Datos regionales y de holgura laboral (DANE).

Escribe:
  pib_departamentos.csv        anio, codigo, departamento, pib_corriente, pib_real, pib_pc (pesos corrientes por habitante)
  pib_departamentos_ramas.csv  anio, codigo, departamento, rama, va_corriente  (12 agrupaciones + impuestos)
  laboral_ciudades.csv         fecha (ultimo mes del ano movil), ciudad, td, ts, tgp, to   (32 ciudades capitales)
  laboral_subutilizacion.csv   fecha, td, ts, tcsd, tcdftp, mcsft  (total nacional, mensual, sin desestacionalizar)

Fuentes: anexos de Cuentas departamentales (anex-PIBDep-TotalDep, anex-PIBDep-Activecono) y de la GEIH (anex-GEIH-<mes><ano>).
Uso: python -m colombiamacro.fuentes.regional [--local carpeta]
"""

from __future__ import annotations

import argparse
import io
import re
import sys
import time
import unicodedata
from pathlib import Path

import pandas as pd
import requests
from openpyxl import load_workbook

from colombiamacro.config import data
from colombiamacro.fuentes.banrep import write_if_changed
from colombiamacro.fuentes.demanda import HEADERS, descargar, enlace

DANE_DEP = "https://www.dane.gov.co/index.php/estadisticas-por-tema/cuentas-nacionales/cuentas-nacionales-departamentales"
DANE_GEIH = "https://www.dane.gov.co/index.php/estadisticas-por-tema/mercado-laboral/empleo-y-desempleo"
PATRONES = {
    "total": (DANE_DEP, r"anex-PIBDep-TotalDep-20\d{2}p?r?\.xlsx$"),
    "ramas": (DANE_DEP, r"anex-PIBDep-Activecono-20\d{2}p?r?\.xlsx$"),
    "geih": (DANE_GEIH, r"/anex-GEIH-[a-z]{3}20\d{2}\.xlsx$"),
}
RAMAS = [("agricultura", "agro"), ("explotacion de minas", "mineria"), ("industrias manufactureras", "industria"),
         ("suministro de electricidad", "electricidad"), ("construccion", "construccion"), ("comercio al por mayor", "comercio"),
         ("informacion y comunicaciones", "informacion"), ("actividades financieras", "finanzas"),
         ("actividades inmobiliarias", "inmobiliarias"), ("actividades profesionales", "profesionales"),
         ("administracion publica", "gobierno"), ("actividades artisticas", "arte"), ("impuestos", "impuestos")]
MESES = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}
CONCEPTOS = {"tasa de desocupacion (td)": "td", "tasa de subocupacion (ts)": "ts", "tasa global de participacion (tgp)": "tgp",
             "tasa de ocupacion (to)": "to", "tcsd": "tcsd", "tcdftp": "tcdftp", "mcsft": "mcsft"}


def _n(s) -> str:
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", s).strip()


def _filas(cont: bytes, hoja: str) -> list:
    wb = load_workbook(io.BytesIO(cont), read_only=True, data_only=True)
    try:
        return [list(r) for r in wb[hoja].values]
    finally:
        wb.close()


def _anio(v):
    m = re.match(r"^(19|20)\d{2}", str(v or "").strip())
    return int(str(v).strip()[:4]) if m else None


def tabla_departamentos(filas: list, desde: int = 0, hasta: int | None = None) -> pd.DataFrame:
    """Bloque 'Codigo | DEPARTAMENTOS | anos...' a partir de la fila `desde`. Devuelve filas largas (anio, codigo, departamento, valor)."""
    h = next(i for i in range(desde, len(filas)) if filas[i] and _n(filas[i][1] if len(filas[i]) > 1 else "") == "departamentos")
    cab = filas[h]
    cols = {}
    for c in range(2, len(cab)):
        if _n(cab[c]) == "departamentos":                     # segundo bloque a la derecha (otra medida): se ignora
            break
        a = _anio(cab[c])
        if a:
            cols[c] = a
    out = []
    for r in filas[h + 1:hasta or len(filas)]:
        if not r or (r[0] is None and r[1] is None):
            if out:
                break
            continue
        nombre = str(r[1] or "").strip()
        if _n(r[0]).startswith("fuente") or not nombre:
            break
        codigo = "00" if _n(nombre) == "colombia" else str(r[0]).strip().zfill(2)
        for c, a in cols.items():
            if c < len(r) and isinstance(r[c], (int, float)):
                out.append({"anio": a, "codigo": codigo, "departamento": "Colombia" if codigo == "00" else nombre, "valor": float(r[c])})
    return pd.DataFrame(out)


def leer_departamentos(total: bytes) -> pd.DataFrame:
    partes = []
    for hoja, col in (("Cuadro 1", "pib_corriente"), ("Cuadro 2", "pib_real"), ("Cuadro 3", "pib_pc")):
        t = tabla_departamentos(_filas(total, hoja)).rename(columns={"valor": col})
        partes.append(t.set_index(["anio", "codigo", "departamento"]))
    df = pd.concat(partes, axis=1).reset_index().sort_values(["codigo", "anio"])
    if df["codigo"].nunique() < 34:
        raise ValueError(f"PIB departamental: {df['codigo'].nunique()} departamentos")
    nac = df[df["codigo"] == "00"].set_index("anio")["pib_corriente"]
    suma = df[df["codigo"] != "00"].groupby("anio")["pib_corriente"].sum()
    if ((suma - nac).abs() / nac).max() > 0.01:
        raise ValueError("PIB departamental: los departamentos no suman el total nacional")
    return df.reset_index(drop=True)


def leer_ramas(ramas: bytes) -> pd.DataFrame:
    filas = _filas(ramas, "Cuadro 1")
    out = []
    titulos = [(i, _n(str(r[0]).split("\n")[0])) for i, r in enumerate(filas) if r and isinstance(r[0], str) and "\n" in r[0]]
    for k, (i, tit) in enumerate(titulos):
        clave = next((c for pref, c in RAMAS if tit.startswith(pref)), None)
        if not clave:
            continue
        fin = titulos[k + 1][0] if k + 1 < len(titulos) else len(filas)
        t = tabla_departamentos(filas, i, fin)
        t["rama"] = clave
        out.append(t)
    df = pd.concat(out).rename(columns={"valor": "va_corriente"})
    if df["rama"].nunique() != 13:
        raise ValueError(f"PIB departamental por ramas: {df['rama'].nunique()} ramas")
    return df[["anio", "codigo", "departamento", "rama", "va_corriente"]].sort_values(["codigo", "rama", "anio"]).reset_index(drop=True)


def _periodo_fin(txt: str):
    """'Sep 25 - Ago 26' o 'Ene - Dic 21' -> ultimo mes del ano movil."""
    m = re.search(r"([A-Za-z]{3})\s*(\d{2})\s*$", str(txt or "").strip())
    if not m or m.group(1).lower()[:3] not in MESES:
        return None
    return pd.Timestamp(2000 + int(m.group(2)), MESES[m.group(1).lower()[:3]], 1)


def leer_ciudades(geih: bytes) -> pd.DataFrame:
    filas = _filas(geih, "Año_móvil_32_ciudades")
    out = []
    for i in range(len(filas) - 2):
        if filas[i + 1] and _n(filas[i + 1][0]) == "ano movil" and filas[i][0]:
            ciudad = str(filas[i][0]).strip()
            per = filas[i + 3]
            fechas = {c: _periodo_fin(per[c]) for c in range(1, len(per))}
            for r in filas[i + 4:i + 12]:
                k = CONCEPTOS.get(_n(r[0]))
                if not k:
                    continue
                for c, f in fechas.items():
                    if f is not None and c < len(r) and isinstance(r[c], (int, float)):
                        out.append({"fecha": f, "ciudad": ciudad, "k": k, "v": float(r[c])})
    df = pd.DataFrame(out).pivot_table(index=["fecha", "ciudad"], columns="k", values="v").reset_index()
    df.columns.name = None
    if df["ciudad"].nunique() < 30:
        raise ValueError(f"GEIH ciudades: {df['ciudad'].nunique()} ciudades")
    return df[["fecha", "ciudad"] + [c for c in ("td", "ts", "tgp", "to") if c in df]].sort_values(["ciudad", "fecha"])


def leer_subutilizacion(geih: bytes) -> pd.DataFrame:
    filas = _filas(geih, "Total nacional")
    h = next(i for i, r in enumerate(filas) if r and _n(r[0]) == "concepto")
    anos, meses = filas[h], filas[h + 1]
    fechas, ano = {}, None
    for c in range(1, len(meses)):
        if c < len(anos) and _anio(anos[c]):
            ano = _anio(anos[c])
        m = MESES.get(_n(meses[c])[:3])
        if ano and m:
            fechas[c] = pd.Timestamp(ano, m, 1)
    datos = {}
    for r in filas[h + 2:h + 12]:
        k = CONCEPTOS.get(_n(r[0]))
        if k and k in ("td", "ts", "tcsd", "tcdftp", "mcsft"):
            datos[k] = {f: (float(r[c]) if isinstance(r[c], (int, float)) and r[c] != 0 else None) for c, f in fechas.items() if c < len(r)}
    df = pd.DataFrame(datos)
    df.index.name = "fecha"
    if len(df) < 200 or "mcsft" not in df:
        raise ValueError("GEIH: subutilizacion incompleta")
    return df.reset_index()


def escribir(dep, ramas, ciudades, sub) -> None:
    for df, nombre, ff in ((dep, "pib_departamentos.csv", "%.3f"), (ramas, "pib_departamentos_ramas.csv", "%.3f"),
                           (ciudades, "laboral_ciudades.csv", "%.4f"), (sub, "laboral_subutilizacion.csv", "%.4f")):
        x = df.copy()
        if "fecha" in x:
            x["fecha"] = pd.to_datetime(x["fecha"]).dt.strftime("%Y-%m-%d")
        ch = write_if_changed(x, data(nombre), float_format=ff)
        print(f"{nombre}: {len(x)} filas ({'actualizado' if ch else 'sin cambios'})")


def actualizar(local: Path | None = None) -> bool:
    cont = {}
    if local:
        for k, (_, pat) in PATRONES.items():
            hits = [p for p in Path(local).iterdir() if re.search(pat.lstrip("/"), p.name, re.I)]
            if hits:
                cont[k] = sorted(hits)[-1].read_bytes()
    else:
        s = requests.Session()
        paginas = {}
        for k, (pagina, pat) in PATRONES.items():
            try:
                if pagina not in paginas:
                    r = s.get(pagina, timeout=40, headers=HEADERS)
                    r.raise_for_status()
                    paginas[pagina] = r.text
                cont[k] = descargar(enlace(paginas[pagina], pagina, pat), s)
                time.sleep(4)
            except Exception as exc:
                print(f"  ERROR descarga {k}: {exc}")
    ok = True
    try:
        dep, ramas = leer_departamentos(cont["total"]), leer_ramas(cont["ramas"])
        ciudades, sub = leer_ciudades(cont["geih"]), leer_subutilizacion(cont["geih"])
        escribir(dep, ramas, ciudades, sub)
    except Exception as exc:
        ok = False
        print(f"  ERROR datos regionales: {exc}")
    return ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--local", type=Path)
    a = ap.parse_args()
    sys.exit(0 if actualizar(a.local) else 1)
