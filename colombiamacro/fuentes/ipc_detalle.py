"""IPC en detalle (DANE, base 2018): divisiones, niveles de ingreso, 23 ciudades, 188 subclases y
clasificaciones por tipo de bien (servicios, durables, semidurables, no durables, energeticos).

Escribe:
  ipc_divisiones.csv      fecha, division, ponderacion, var_mensual, var_corrido, var_anual, contrib_mensual, contrib_corrido, contrib_anual
  ipc_ingresos.csv        fecha, grupo, var_mensual, var_corrido, var_anual
  ipc_ciudades.csv        fecha, ciudad, division, var_anual          (23 ciudades + otras areas, 12 divisiones + total)
  ipc_subclases.csv       fecha, codigo, subclase, var_mensual, var_anual, contrib_anual
  ipc_clasificaciones.csv fecha, serie, indice                       (mensual desde 2009, dic 2018 = 100)
  ipc_ponderaciones.csv   subclase, pobres, vulnerables, media, altos, total   (ponderaciones oficiales de la canasta 2018, %)

El anexo principal (anex-IPC-<mes><ano>.xlsx) esta junto a los anexos enlazados en la pagina del IPC.
Uso: python -m colombiamacro.fuentes.ipc_detalle [--local carpeta]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd
import requests

from colombiamacro.config import data
from colombiamacro.fuentes.banrep import write_if_changed
from colombiamacro.fuentes.demanda import HEADERS, descargar, enlace
from colombiamacro.fuentes.regional import _filas, _n

DANE_IPC = "https://www.dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/indice-de-precios-al-consumidor-ipc"
MESES = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
         "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12}
DIVISIONES = {"alimentos y bebidas no alcoholicas": "alimentos", "bebidas alcoholicas y tabaco": "alcohol_tabaco",
              "prendas de vestir y calzado": "vestuario", "alojamiento, agua, electricidad, gas y otros combustibles": "vivienda",
              "muebles, articulos para el hogar y para la conservacion ordinaria del hogar": "muebles", "salud": "salud",
              "transporte": "transporte", "informacion y comunicacion": "comunicaciones", "recreacion y cultura": "recreacion",
              "educacion": "educacion", "restaurantes y hoteles": "restaurantes", "bienes y servicios diversos": "diversos", "total": "total"}
CLASIF = {"11": "energeticos", "12": "sin_alimentos_energeticos", "13": "servicios", "14": "durables", "15": "semidurables", "16": "no_durables"}


def _fecha_hoja(filas) -> pd.Timestamp:
    for r in filas[:12]:
        m = re.match(r"^\s*([a-záéíóú]+) de (\d{4})", _n(r[0]) if r and r[0] else "")
        if m and m.group(1) in MESES:
            return pd.Timestamp(int(m.group(2)), MESES[m.group(1)], 1)
    raise ValueError("IPC: no encuentro el mes del anexo")


def _div(nombre) -> str | None:
    return DIVISIONES.get(_n(nombre))


def leer_divisiones(cont: bytes) -> pd.DataFrame:
    f = _filas(cont, "2")
    fecha = _fecha_hoja(f)
    cols = ["ponderacion", "var_mensual", "var_corrido", "var_anual", "contrib_mensual", "contrib_corrido", "contrib_anual"]
    out = []
    for r in f:
        d = _div(r[0]) if r and r[0] else None
        if d and isinstance(r[1], (int, float)):
            out.append({"fecha": fecha, "division": d, **{c: float(r[i + 1]) for i, c in enumerate(cols)}})
    df = pd.DataFrame(out)
    if len(df) != 13 or abs(df[df["division"] != "total"]["ponderacion"].sum() - 100) > 0.5:
        raise ValueError("IPC divisiones incompletas")
    return df


def leer_ingresos(cont: bytes) -> pd.DataFrame:
    f = _filas(cont, "3")
    fecha = _fecha_hoja(f)
    h = next(i for i, r in enumerate(f) if r and any(_n(x) == "pobres" for x in r if x))
    grupos = {c: _n(v) for c, v in enumerate(f[h]) if v}
    fila = next(r for r in f[h + 2:] if r and _n(r[0]).startswith("ipc total"))
    out = []
    for c, g in grupos.items():
        clave = {"pobres": "pobres", "vulnerables": "vulnerables", "clase media": "media", "ingresos altos": "altos", "total": "total"}.get(g)
        if clave:
            out.append({"fecha": fecha, "grupo": clave, "var_mensual": fila[c], "var_corrido": fila[c + 1], "var_anual": fila[c + 2]})
    if len(out) != 5:
        raise ValueError("IPC por ingresos incompleto")
    return pd.DataFrame(out)


def leer_ciudades(cont: bytes) -> pd.DataFrame:
    f = _filas(cont, "6")
    fecha = _fecha_hoja(f)
    h = next(i for i, r in enumerate(f) if r and _n(r[0]) == "ciudades")
    cab = {c: _div(v) for c, v in enumerate(f[h]) if c > 0 and v and _div(v)}
    out = []
    for r in f[h + 1:]:
        if not r or not r[0] or _n(r[0]).startswith("fuente"):
            break
        ciudad = "Total" if _n(r[0]) == "total ipc" else str(r[0]).strip()
        for c, d in cab.items():
            if isinstance(r[c], (int, float)):
                out.append({"fecha": fecha, "ciudad": ciudad, "division": d, "var_anual": float(r[c])})
    df = pd.DataFrame(out)
    if df["ciudad"].nunique() < 23:
        raise ValueError("IPC por ciudades incompleto")
    return df


def leer_subclases(cont: bytes) -> pd.DataFrame:
    f = _filas(cont, "8")
    fecha = _fecha_hoja(f)
    out = []
    for r in f:
        if r and re.fullmatch(r"\d{8}", str(r[0] or "").strip()) and isinstance(r[5], (int, float)):
            out.append({"fecha": fecha, "codigo": str(r[0]).strip(), "subclase": re.sub(r"\s+", " ", str(r[1])).strip(),
                        "var_mensual": r[3], "var_anual": r[5], "contrib_anual": r[8]})
    df = pd.DataFrame(out)
    if len(df) < 150:
        raise ValueError(f"IPC subclases: {len(df)}")
    return df


def leer_clasificaciones(cont: bytes) -> pd.DataFrame:
    out = []
    for hoja, serie in CLASIF.items():
        f = _filas(cont, hoja)
        for r in f:
            if r and isinstance(r[0], (int, float)) and 2000 < r[0] < 2100 and _n(r[1]) in MESES and isinstance(r[2], (int, float)):
                out.append({"fecha": pd.Timestamp(int(r[0]), MESES[_n(r[1])], 1), "serie": serie, "indice": float(r[2])})
    df = pd.DataFrame(out).drop_duplicates(["fecha", "serie"])
    if df["serie"].nunique() != len(CLASIF) or df.groupby("serie").size().min() < 150:
        raise ValueError("IPC clasificaciones incompletas")
    return df.sort_values(["serie", "fecha"])


DANE_POND = ("https://www.dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/indice-de-precios-al-consumidor-ipc/"
             "ipc-actualizacion-metodologica-2019/ipc-ponderadores")


def leer_ponderaciones(html: str) -> pd.DataFrame:
    """Tabla de ponderaciones por subclase (la de 150 a 260 filas) de la pagina de actualizacion metodologica."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    num_ = lambda x: float(x.replace(".", "").replace(",", ".")) if re.fullmatch(r"-?[\d.]+,\d+|-?\d+", x.strip()) else None
    for t in soup.find_all("table"):
        filas = [[c.get_text(" ", strip=True) for c in tr.find_all(["td", "th"])] for tr in t.find_all("tr")]
        if 150 <= len(filas) <= 260 and all(len(f) >= 6 for f in filas[1:]):
            out = []
            for f in filas[1:]:
                v = [num_(x) for x in f[1:6]]
                if None not in v:
                    out.append({"subclase": re.sub(r"\s+", " ", f[0]).strip(), "pobres": v[0], "vulnerables": v[1], "media": v[2], "altos": v[3], "total": v[4]})
            df = pd.DataFrame(out)
            if len(df) >= 180 and abs(df["total"].sum() - 100) < 1.5:
                return df
    raise ValueError("Ponderaciones del IPC: no encuentro la tabla de subclases")


def url_anexo(html: str) -> str:
    """El anexo principal no siempre esta enlazado: se deriva del anexo de indices del mismo mes."""
    try:
        return enlace(html, DANE_IPC, r"/anex-IPC-[a-z]{3}20\d{2}\.xlsx$")
    except ValueError:
        return enlace(html, DANE_IPC, r"/anex-IPC-Indices-[a-z]{3}20\d{2}\.xlsx$").replace("anex-IPC-Indices-", "anex-IPC-")


def actualizar(local: Path | None = None) -> bool:
    pond_html = None
    if local:
        hits = sorted(p for p in Path(local).iterdir() if re.fullmatch(r"anex-IPC-[a-z]{3}20\d{2}\.xlsx", p.name, re.I))
        cont = hits[-1].read_bytes()
        ph = Path(local) / "ipc-ponderadores.html"
        pond_html = ph.read_text(encoding="utf-8", errors="ignore") if ph.exists() else None
    else:
        s = requests.Session()
        r = s.get(DANE_IPC, timeout=40, headers=HEADERS)
        r.raise_for_status()
        cont = descargar(url_anexo(r.text), s)
        try:
            rp = s.get(DANE_POND, timeout=40, headers=HEADERS)
            rp.raise_for_status()
            pond_html = rp.text
        except Exception as exc:
            print(f"  ERROR descarga ponderaciones: {exc}")
    ok = True
    if pond_html:
        try:
            pdf_ = leer_ponderaciones(pond_html)
            ch = write_if_changed(pdf_, data("ipc_ponderaciones.csv"), float_format="%.2f")
            print(f"ipc_ponderaciones.csv: {len(pdf_)} subclases ({'actualizado' if ch else 'sin cambios'})")
        except Exception as exc:
            ok = False
            print(f"  ERROR ipc_ponderaciones.csv: {exc}")
    for nombre, fn, ff in (("ipc_divisiones.csv", leer_divisiones, "%.4f"), ("ipc_ingresos.csv", leer_ingresos, "%.4f"),
                           ("ipc_ciudades.csv", leer_ciudades, "%.4f"), ("ipc_subclases.csv", leer_subclases, "%.4f"),
                           ("ipc_clasificaciones.csv", leer_clasificaciones, "%.4f")):
        try:
            df = fn(cont)
            df["fecha"] = pd.to_datetime(df["fecha"]).dt.strftime("%Y-%m-%d")
            ch = write_if_changed(df.reset_index(drop=True), data(nombre), float_format=ff)
            print(f"{nombre}: {len(df)} filas hasta {df['fecha'].max()} ({'actualizado' if ch else 'sin cambios'})")
        except Exception as exc:
            ok = False
            print(f"  ERROR {nombre}: {exc}")
    return ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--local", type=Path)
    a = ap.parse_args()
    sys.exit(0 if actualizar(a.local) else 1)
