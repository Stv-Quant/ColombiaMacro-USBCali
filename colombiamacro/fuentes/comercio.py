"""Comercio exterior de bienes: exportaciones (DIAN-DANE, EXPO) e importaciones (DIAN-DANE, IMPO).

Salidas (data/)
---------------
exportaciones_mensuales.csv    fecha, cafe, carbon, petroleo, ferroniquel, tradicionales,
                               no_tradicionales, total                (miles de USD FOB)
exportaciones_destinos.csv     fecha + una columna por destino principal (miles de USD FOB)
importaciones_mensuales.csv    fecha, publicadas, zonas_francas, total (miles de USD CIF;
                               total = sistema comercial especial ampliado)
importaciones_cuode_reciente.csv  uso o destino economico (CUODE): ano corrido y ultimo mes
                               frente al mismo periodo del ano anterior (miles de USD CIF)
importaciones_cuode_anual.csv  anio, grupo, valor (millones de USD CIF; el ultimo ano es parcial)
importaciones_origen.csv       fecha, pais, valor (miles de USD CIF), principales paises

Fuente unica: anexos oficiales del DANE (operaciones EXPO e IMPO), descubiertos en las
paginas de cada operacion. Si el DANE responde 429 (demasiadas solicitudes) se espera y se
reintenta. Cada tabla se valida antes de escribirse; si algo no cuadra, se conserva la anterior.

Uso: python -m colombiamacro.fuentes.comercio
"""

from __future__ import annotations

import io
import re
import sys
import time
import unicodedata

import numpy as np
import pandas as pd
import requests

from colombiamacro.config import data
from colombiamacro.fuentes.banrep import write_if_changed

PAGINA_EXPO = "https://www.dane.gov.co/index.php/estadisticas-por-tema/comercio-internacional/exportaciones"
PAGINA_IMPO = "https://www.dane.gov.co/index.php/estadisticas-por-tema/comercio-internacional/importaciones"
MES = r"[a-z]{3}20\d{2}"
ANEXOS = {
    "expo_tradicionales": (PAGINA_EXPO, rf"/anex-EXPORTACIONES-SerieCafeCarbonPetroleoNotradicionales-{MES}\.xlsx$"),
    "expo_destinos": (PAGINA_EXPO, rf"/anex-EXPORTACIONES-SeriePrincipalesDestinos-{MES}\.xlsx$"),
    "impo_anexo": (PAGINA_IMPO, rf"/anex-IMP-{MES}\.xls$"),
    "impo_cuode_anual": (PAGINA_IMPO, rf"/anex-IMP-ImpoClasiCUODE-{MES}\.xlsx$"),
    "impo_origen": (PAGINA_IMPO, rf"/anex-IMP-MensPrincPaisesOrigen-{MES}\.xlsx$"),
}
HEADERS = {"User-Agent": "Mozilla/5.0 (ColombiaMacro; proyecto academico USB Cali)"}
MESES = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
         "septiembre": 9, "setiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12}


# ------------------------------------------------------------------ utilidades
def slug(texto) -> str:
    t = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode().lower().strip()
    return re.sub(r"[^a-z0-9]+", "_", t).strip("_")


def num(v):
    if v is None or (isinstance(v, float) and np.isnan(v)) or isinstance(v, str):
        return None
    return float(v)


def fecha_celda(v):
    """Fecha de una celda de Excel: datetime, o numero de serie (1899-12-30). Primer dia del mes."""
    if isinstance(v, (pd.Timestamp,)) or hasattr(v, "year") and hasattr(v, "month"):
        return pd.Timestamp(v.year, v.month, 1)
    if isinstance(v, (int, float)) and not (isinstance(v, float) and np.isnan(v)) and 20000 < v < 80000:
        t = pd.Timestamp("1899-12-30") + pd.Timedelta(days=float(v))
        return pd.Timestamp(t.year, t.month, 1)
    return None


def texto(v) -> str:
    return "" if v is None or (isinstance(v, float) and np.isnan(v)) else str(v).strip()


def descargar(url: str, intentos: int = 5) -> bytes:
    espera = 15
    for i in range(intentos):
        r = requests.get(url, headers=HEADERS, timeout=90)
        if r.status_code in (429, 502, 503, 504) and i < intentos - 1:
            time.sleep(espera)
            espera *= 2
            continue
        r.raise_for_status()
        if len(r.content) < 5000:
            raise ValueError(f"DANE: archivo demasiado pequeno ({len(r.content)} bytes): {url}")
        return r.content
    raise RuntimeError(f"DANE: sin respuesta util para {url}")


def enlace(pagina: str, patron: str) -> str:
    from urllib.parse import urljoin
    from bs4 import BeautifulSoup
    html = descargar_html(pagina)
    links = [a["href"] for a in BeautifulSoup(html, "html.parser").select("a[href]") if re.search(patron, a["href"], re.I)]
    links = list(dict.fromkeys(links))
    if len(links) != 1:
        raise ValueError(f"DANE: se esperaba un anexo vigente para {patron}, hay {len(links)}")
    return urljoin(pagina, links[0])


_HTML = {}


def descargar_html(pagina: str) -> str:
    if pagina not in _HTML:
        espera = 15
        for i in range(5):
            r = requests.get(pagina, headers=HEADERS, timeout=60)
            if r.status_code == 429 and i < 4:
                time.sleep(espera)
                espera *= 2
                continue
            r.raise_for_status()
            _HTML[pagina] = r.text
            break
    return _HTML[pagina]


def filas(contenido: bytes, hoja: str, xls: bool = False) -> list[list]:
    """Filas crudas de una hoja (sin encabezados), con None en celdas vacias."""
    libro = pd.ExcelFile(io.BytesIO(contenido), engine="xlrd" if xls else "openpyxl")
    nombre = next((n for n in libro.sheet_names if n.strip().lower() == hoja.strip().lower()), None)
    if nombre is None:
        raise ValueError(f"DANE: no existe la hoja {hoja!r} (hay {libro.sheet_names})")
    df = libro.parse(nombre, header=None)
    return [[None if (isinstance(v, float) and np.isnan(v)) else v for v in fila] for fila in df.itertuples(index=False)]


# ------------------------------------------------------------------ lectores (probados con los anexos reales)
def leer_expo_tradicionales(rows: list[list]) -> pd.DataFrame:
    """Hoja 'Tra y Notra': encabezados en dos filas; una fila por mes y filas de totales anuales."""
    hdr = next(i for i, r in enumerate(rows) if texto(r[0]).upper() == "MES")
    nombres = [texto(v) for v in rows[hdr + 1]]
    unidades = [texto(v) for v in rows[hdr + 2]]
    col = {}
    for j, n in enumerate(nombres):
        n_ = slug(n)
        if not n_ or "dolares" not in slug(unidades[j] if j < len(unidades) else ""):
            continue
        if n_.startswith("cafe"):
            col["cafe"] = j
        elif n_.startswith("carbon"):
            col["carbon"] = j
        elif n_.startswith("petroleo"):
            col["petroleo"] = j
        elif n_.startswith("ferroniquel"):
            col["ferroniquel"] = j
        elif "tradicionales" in n_:
            col["tradicionales"] = j
    usd = [j for j, u in enumerate(unidades) if "dolares" in slug(u)]
    col["no_tradicionales"], col["total"] = usd[-2], usd[-1]
    out = []
    for r in rows[hdr + 3:]:
        f = fecha_celda(r[0])
        if f is None:
            continue
        out.append({"fecha": f, **{k: num(r[j]) for k, j in col.items()}})
    df = pd.DataFrame(out).sort_values("fecha").reset_index(drop=True)
    orden = ["fecha", "cafe", "carbon", "petroleo", "ferroniquel", "tradicionales", "no_tradicionales", "total"]
    return df[orden]


def leer_expo_destinos(rows: list[list]) -> pd.DataFrame:
    """Hoja 'Destinos': grupos en una fila y paises en la siguiente; valores en miles de USD FOB."""
    hdr = next(i for i, r in enumerate(rows) if texto(r[0]).lower() == "mes")
    g, p = rows[hdr], rows[hdr + 1]
    col = {}
    for j in range(1, max(len(g), len(p))):
        nombre = texto(p[j]) if j < len(p) and texto(p[j]) else (texto(g[j]) if j < len(g) else "")
        if not nombre:
            continue
        s_ = slug(nombre)
        s_ = {"resto_de_paises": "resto", "total_exportaciones": "total"}.get(s_, s_)
        if s_ not in col:
            col[s_] = j
    out = []
    for r in rows[hdr + 2:]:
        f = fecha_celda(r[0])
        if f is not None:
            out.append({"fecha": f, **{k: num(r[j]) if j < len(r) else None for k, j in col.items()}})
    return pd.DataFrame(out).sort_values("fecha").reset_index(drop=True)


def leer_impo_mensual(rows: list[list]) -> pd.DataFrame:
    """Cuadro A30: importaciones mensuales (publicadas, zonas francas, sistema comercial ampliado)."""
    out = []
    for r in rows:
        f = fecha_celda(r[0])
        if f is not None and num(r[1]) is not None:
            out.append({"fecha": f, "publicadas": num(r[1]), "zonas_francas": num(r[2]), "total": num(r[3])})
    return pd.DataFrame(out).sort_values("fecha").reset_index(drop=True)


def leer_impo_cuode_reciente(rows: list[list]) -> tuple[pd.DataFrame, dict]:
    """Cuadro A13 (CUODE, miles de USD CIF): ano corrido y ultimo mes, con variacion y contribucion."""
    hdr = next(i for i, r in enumerate(rows) if texto(r[0]).upper() == "CUODE")
    periodos = [(j, texto(v)) for j, v in enumerate(rows[hdr - 1]) if texto(v)]
    (j_ytd, et_ytd), (j_mes, et_mes) = periodos[0], periodos[1]
    anos = [texto(v).rstrip("p") for v in rows[hdr][j_ytd:j_ytd + 2]]
    meta = {"periodo_corrido": et_ytd, "periodo_mes": et_mes, "anio_anterior": anos[0], "anio_actual": anos[1]}
    out, previo = [], None
    for r in rows[hdr + 2:]:
        r = list(r) + [None] * (j_mes + 5 - len(r))
        vals = [num(r[j]) for j in (j_ytd, j_ytd + 1, j_ytd + 2, j_ytd + 3, j_mes, j_mes + 1, j_mes + 2, j_mes + 3)]
        if texto(r[1]):
            nivel, nombre = 0, texto(r[1])
        elif texto(r[2]):
            nivel, nombre = 1, texto(r[2])
        elif texto(r[3]):
            nivel, nombre = 2, texto(r[3])
        else:
            continue
        if vals[0] is None:
            previo = (nivel, nombre, texto(r[0]))            # titulo partido en dos filas
            continue
        codigo = texto(r[0])
        if previo and nivel == previo[0] and not codigo:
            nombre, codigo = f"{previo[1]} {nombre[0].lower() + nombre[1:]}", previo[2]
        previo = None
        if nivel > 1:
            continue
        out.append({"codigo": codigo, "grupo": re.sub(r"\s+", " ", nombre), "nivel": nivel,
                    "corrido_anterior": vals[0], "corrido_actual": vals[1], "corrido_var": vals[2], "corrido_contrib": vals[3],
                    "mes_anterior": vals[4], "mes_actual": vals[5], "mes_var": vals[6], "mes_contrib": vals[7]})
    return pd.DataFrame(out), meta


def leer_impo_cuode_anual(rows: list[list]) -> pd.DataFrame:
    """Hoja CUODE: un ano por columna (con su participacion al lado); millones de USD CIF."""
    hdr = next(i for i, r in enumerate(rows) if texto(r[0]).lower() == "sector")
    anos = []
    for j, v in enumerate(rows[hdr]):
        m = re.match(r"^(\d{4})", texto(v).split(".")[0]) if v is not None else None
        if m:
            anos.append((j, int(m.group(1))))
    out = []
    for r in rows[hdr + 1:]:
        nombre = texto(r[0])
        if not nombre or num(r[1]) is None:
            continue
        for j, a in anos:
            if j < len(r) and num(r[j]) is not None:
                out.append({"anio": a, "grupo": re.sub(r"\s+", " ", nombre), "valor": num(r[j])})
    return pd.DataFrame(out)


def leer_impo_origen(rows: list[list], desde: int = 2010) -> pd.DataFrame:
    """Hoja 'Pais mes': bloques por pais, una fila por mes y una columna por ano."""
    hdr = next(i for i, r in enumerate(rows) if sum(isinstance(v, (int, float)) and 1990 < (v or 0) < 2100 for v in r) >= 5)
    anos = [(j, int(v)) for j, v in enumerate(rows[hdr]) if isinstance(v, (int, float)) and 1990 < v < 2100]
    out, pais = [], None
    for r in rows[hdr + 1:]:
        if texto(r[0]):
            pais = texto(r[0])
        mes = MESES.get(slug(texto(r[1]))) if len(r) > 1 else None
        if not pais or not mes or pais.lower().startswith(("fuente", "total")):
            continue
        for j, a in anos:
            if a >= desde and j < len(r) and num(r[j]) is not None:
                out.append({"fecha": pd.Timestamp(a, mes, 1), "pais": pais, "valor": num(r[j])})
    df = pd.DataFrame(out)
    # el ano en curso trae celdas vacias o en cero para los meses que aun no ocurren
    tot = df.groupby("fecha")["valor"].sum()
    ultimo = tot[tot > 0].index.max()
    df = df[df["fecha"] <= ultimo]
    return df.sort_values(["pais", "fecha"]).reset_index(drop=True)


# ------------------------------------------------------------------ validacion y escritura
def validar_mensual(df: pd.DataFrame, nombre: str, min_meses: int, col_total: str = "total") -> None:
    if len(df) < min_meses:
        raise ValueError(f"{nombre}: solo {len(df)} meses")
    if df["fecha"].duplicated().any():
        raise ValueError(f"{nombre}: meses duplicados")
    t = df[col_total].dropna()
    if (t <= 0).any() or t.iloc[-1] > 50_000_000:
        raise ValueError(f"{nombre}: totales fuera de rango")


def actualizar(locales: dict | None = None) -> bool:
    """Descarga los anexos del DANE y escribe las tablas. `locales` (clave -> ruta) permite
    procesar archivos ya descargados del mismo sitio oficial, sin red."""
    ok = True
    contenido = {}
    for clave, (pagina, patron) in ANEXOS.items():
        if locales is not None:
            if clave in locales:
                from pathlib import Path
                contenido[clave] = (pagina, Path(locales[clave]).read_bytes())
            continue
        try:
            url = enlace(pagina, patron)
            contenido[clave] = (url, descargar(url))
            time.sleep(4)                                        # el DANE limita la tasa de descargas
        except Exception as exc:
            ok = False
            print(f"  ERROR descarga {clave}: {exc}")

    def paso(nombre, fn):
        nonlocal ok
        try:
            fn()
        except Exception as exc:
            ok = False
            print(f"  ERROR {nombre}: {exc}")

    def expo():
        url, c = contenido["expo_tradicionales"]
        df = leer_expo_tradicionales(filas(c, "Tra y Notra"))
        validar_mensual(df, "Exportaciones", 300)
        dif = (df[["tradicionales", "no_tradicionales"]].sum(axis=1) - df["total"]).abs() / df["total"]
        if (dif > 0.01).any():
            raise ValueError("Exportaciones: tradicionales + no tradicionales no suman el total")
        ch = write_if_changed(df, data("exportaciones_mensuales.csv"), float_format="%.3f")
        print(f"Exportaciones: {len(df)} meses hasta {df['fecha'].max():%Y-%m} ({'actualizado' if ch else 'sin cambios'})")

    def destinos():
        url, c = contenido["expo_destinos"]
        df = leer_expo_destinos(filas(c, "Destinos"))
        validar_mensual(df, "Destinos", 150)
        ch = write_if_changed(df, data("exportaciones_destinos.csv"), float_format="%.3f")
        print(f"Destinos de exportacion: {len(df)} meses, {df.shape[1] - 1} columnas ({'actualizado' if ch else 'sin cambios'})")

    def impo():
        url, c = contenido["impo_anexo"]
        df = leer_impo_mensual(filas(c, "Cuadro A30", xls=True))
        validar_mensual(df, "Importaciones", 150)
        ch = write_if_changed(df, data("importaciones_mensuales.csv"), float_format="%.3f")
        print(f"Importaciones: {len(df)} meses hasta {df['fecha'].max():%Y-%m} ({'actualizado' if ch else 'sin cambios'})")
        cu, meta = leer_impo_cuode_reciente(filas(c, "Cuadro A13", xls=True))
        if cu.empty or abs(cu.iloc[0]["corrido_actual"] - cu[cu["nivel"] == 0].iloc[1:]["corrido_actual"].sum()) > 0.02 * cu.iloc[0]["corrido_actual"]:
            raise ValueError("CUODE reciente: los grupos no suman el total")
        for k, v in meta.items():
            cu[k] = v
        cu["fuente"] = url
        ch = write_if_changed(cu, data("importaciones_cuode_reciente.csv"), float_format="%.4f")
        print(f"Importaciones por uso (CUODE, {meta['periodo_corrido']} {meta['anio_actual']}): {len(cu)} grupos ({'actualizado' if ch else 'sin cambios'})")

    def cuode_anual():
        url, c = contenido["impo_cuode_anual"]
        df = leer_impo_cuode_anual(filas(c, "CUODE"))
        if df["anio"].nunique() < 15:
            raise ValueError("CUODE anual: historia incompleta")
        ch = write_if_changed(df, data("importaciones_cuode_anual.csv"), float_format="%.3f")
        print(f"CUODE anual: {df['anio'].min()}–{df['anio'].max()} ({'actualizado' if ch else 'sin cambios'})")

    def origen():
        url, c = contenido["impo_origen"]
        df = leer_impo_origen(filas(c, "País mes"))
        if df["pais"].nunique() < 5:
            raise ValueError("Origen de importaciones: muy pocos paises")
        ch = write_if_changed(df, data("importaciones_origen.csv"), float_format="%.3f")
        print(f"Origen de importaciones: {df['pais'].nunique()} paises ({'actualizado' if ch else 'sin cambios'})")

    for nombre, fn, clave in (("exportaciones", expo, "expo_tradicionales"), ("destinos", destinos, "expo_destinos"),
                              ("importaciones", impo, "impo_anexo"), ("cuode anual", cuode_anual, "impo_cuode_anual"),
                              ("origen", origen, "impo_origen")):
        if clave in contenido:
            paso(nombre, fn)
    return ok


if __name__ == "__main__":
    sys.exit(0 if actualizar() else 1)
