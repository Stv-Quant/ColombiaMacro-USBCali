"""Acciones de la bolsa colombiana: canasta del COLCAP y precios semanales.

Salidas
-------
colcap_canasta.csv   canasta vigente: ticker, nombre, emisor, sector, peso (%), precio, fecha_canasta
                     Fuente: composicion diaria del fondo iShares MSCI COLCAP (BlackRock), que
                     replica el indice; los pesos son los del fondo, no los oficiales de la BVC.
acciones_semanal.csv precios de cierre semanales (no ajustados por dividendos, igual que el
                     COLCAP) de cada accion de la canasta: fecha (viernes), ticker, simbolo, cierre.
                     Fuente: Yahoo Finance, simbolos <TICKER>.CL.

Reglas
------
* Si una descarga falla se conserva la version anterior (de la canasta o de cada accion).
* Una accion con cambio de ticker se empalma con su serie anterior (ALIAS) usando el precio
  de la primera semana comun, sin saltos artificiales.
* Se rechazan precios no positivos y series con menos de 26 semanas.

Uso: python -m colombiamacro.fuentes.acciones
"""

from __future__ import annotations

import csv
import io
import re
import sys
import time

import pandas as pd
import requests

from colombiamacro.config import data

OUT_CANASTA = data("colcap_canasta.csv")
OUT_PRECIOS = data("acciones_semanal.csv")

CANASTA_URL = ("https://www.blackrock.com/co/productos/251708/ishares-fondo-burstil-ishares-colcap-fund/"
               "1497267045723.ajax?fileType=csv&fileName=ICOLCAP_holdings&dataType=fund")
YAHOO_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{simbolo}"
INICIO = 1262304000  # 2010-01-01
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
           "Accept": "*/*", "Accept-Language": "es-CO,es;q=0.9"}

# ticker actual -> tickers anteriores en Yahoo (se empalman hacia atras)
ALIAS = {"PFDAVIGRP": ["PFDAVVNDA"]}
MIN_SEMANAS = 26
MESES = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7, "ago": 8,
         "sept": 9, "sep": 9, "oct": 10, "nov": 11, "dic": 12}


# ------------------------------------------------------------------ canasta
def _num_co(txt: str) -> float:
    return float(str(txt).replace(".", "").replace(",", "."))


def emisor(nombre: str) -> str:
    """Nombre de la empresa sin la clase de accion: agrupa ordinarias y preferenciales."""
    n = re.sub(r"[.,]", " ", str(nombre).upper())
    n = re.sub(r"\b(PREF|PRF|PREFERENCIAL|SA|ESP|S|A)\b", " ", n)
    return re.sub(r"\s+", " ", n).strip()


def parse_canasta(texto: str) -> pd.DataFrame:
    """Lee el CSV de composicion de iShares (formato colombiano: 1.234,56)."""
    lineas = texto.lstrip("﻿").splitlines()
    m = re.search(r"(\d{1,2}) ([A-Za-z]+)\.? (\d{4})", lineas[0]) if lineas else None
    mes = MESES.get(m.group(2).lower(), MESES.get(m.group(2).lower()[:3])) if m else None
    if not mes:
        raise ValueError("No se encontro la fecha de la canasta")
    fecha = pd.Timestamp(int(m.group(3)), mes, int(m.group(1)))
    inicio = next(i for i, l in enumerate(lineas) if l.startswith("Ticker,"))
    filas = list(csv.DictReader(io.StringIO("\n".join(lineas[inicio:]))))
    out = []
    for f in filas:
        if (f.get("Asset Class") or "").strip() != "Equity":
            continue
        if "Colombia" not in (f.get("Exchange") or "") or (f.get("Ticker") or "-") in ("-", ""):
            continue
        peso = _num_co(f["Weight (%)"])
        if peso <= 0:
            continue
        out.append({"ticker": f["Ticker"].strip(), "nombre": f["Name"].strip(), "emisor": emisor(f["Name"]),
                    "sector": f["Sector"].strip(), "peso": peso, "precio": _num_co(f["Price"]),
                    "fecha_canasta": fecha.date().isoformat()})
    df = pd.DataFrame(out).sort_values("peso", ascending=False).reset_index(drop=True)
    if len(df) < 10 or not 80 <= df["peso"].sum() <= 101:
        raise ValueError(f"Canasta incompleta: {len(df)} acciones, {df['peso'].sum() if len(df) else 0:.1f}% del fondo")
    return df


def descargar_canasta() -> pd.DataFrame:
    r = requests.get(CANASTA_URL, headers=HEADERS, timeout=40)
    r.raise_for_status()
    return parse_canasta(r.text)


# ------------------------------------------------------------------ precios
def viernes(fechas: pd.Series) -> pd.Series:
    """Fecha de cada semana = su viernes; la semana en curso se fecha hoy (no en el futuro)."""
    hoy = pd.Timestamp.today().normalize()
    v = pd.to_datetime(fechas).dt.to_period("W-FRI").dt.end_time.dt.normalize()
    return v.where(v <= hoy, hoy)


def parse_yahoo(j: dict) -> pd.DataFrame:
    res = (j.get("chart") or {}).get("result")
    if not res:
        raise ValueError(f"Yahoo sin datos: {(j.get('chart') or {}).get('error')}")
    res = res[0]
    ts = res.get("timestamp") or []
    close = res["indicators"]["quote"][0].get("close") or []
    df = pd.DataFrame({"fecha": pd.to_datetime(ts, unit="s").normalize(), "cierre": close}).dropna()
    # Barras semanales de Yahoo: fecha = lunes; se reportan al viernes de esa semana.
    df["fecha"] = viernes(df["fecha"])
    df = df[df["cierre"] > 0].drop_duplicates("fecha", keep="last").sort_values("fecha")
    return df.reset_index(drop=True)


def descargar_yahoo(ticker: str, intentos: int = 3) -> pd.DataFrame:
    ultimo = None
    for k in range(intentos):
        try:
            r = requests.get(YAHOO_URL.format(simbolo=f"{ticker}.CL"), headers=HEADERS, timeout=30,
                             params={"period1": INICIO, "period2": int(time.time()) + 86400, "interval": "1wk"})
            r.raise_for_status()
            return parse_yahoo(r.json())
        except Exception as exc:  # limite de tasa o red intermitente
            ultimo = exc
            time.sleep(2 * (k + 1))
    raise ultimo


def empalmar(actual: pd.DataFrame, anterior: pd.DataFrame) -> pd.DataFrame:
    """Extiende hacia atras la serie actual con la anterior, escalada en la primera semana comun."""
    if anterior.empty:
        return actual
    if actual.empty:
        return anterior
    f0 = actual["fecha"].min()
    comun = anterior[anterior["fecha"] <= f0]
    if comun.empty:
        return actual
    ref = comun.iloc[-1]
    escala = float(actual.iloc[0]["cierre"]) / float(ref["cierre"])
    previo = anterior[anterior["fecha"] < f0].copy()
    previo["cierre"] = previo["cierre"] * escala
    return pd.concat([previo, actual], ignore_index=True)


def validar_precios(ticker: str, df: pd.DataFrame) -> pd.DataFrame:
    if len(df) < MIN_SEMANAS:
        raise ValueError(f"{ticker}: solo {len(df)} semanas")
    if (df["cierre"] <= 0).any() or df["fecha"].duplicated().any():
        raise ValueError(f"{ticker}: precios invalidos")
    return df


def serie_accion(ticker: str, fetch=descargar_yahoo) -> tuple[pd.DataFrame, str]:
    df = fetch(ticker)
    simbolos = [f"{ticker}.CL"]
    for viejo in ALIAS.get(ticker, []):
        try:
            df = empalmar(df, fetch(viejo))
            simbolos.append(f"{viejo}.CL")
        except Exception as exc:
            print(f"  aviso: sin historia anterior de {ticker} ({viejo}): {exc}")
    return validar_precios(ticker, df), "+".join(simbolos)


def combinar(previo: pd.DataFrame, nuevos: dict[str, tuple[pd.DataFrame, str]]) -> pd.DataFrame:
    """Reemplaza las acciones descargadas y conserva las demas del archivo anterior."""
    partes = [previo[~previo["ticker"].isin(nuevos)]] if not previo.empty else []
    for t, (df, simbolo) in nuevos.items():
        partes.append(df.assign(ticker=t, simbolo=simbolo)[["fecha", "ticker", "simbolo", "cierre"]])
    out = pd.concat(partes, ignore_index=True)
    out["fecha"] = pd.to_datetime(out["fecha"])
    out["cierre"] = out["cierre"].round(4)
    return out.sort_values(["ticker", "fecha"]).reset_index(drop=True)


def escribir(df: pd.DataFrame, ruta, fechas=("fecha",)) -> bool:
    d = df.copy()
    for c in fechas:
        if c in d:
            d[c] = pd.to_datetime(d[c]).dt.strftime("%Y-%m-%d")
    texto = d.to_csv(index=False, lineterminator="\n")
    if ruta.exists() and ruta.read_text(encoding="utf-8") == texto:
        return False
    ruta.write_text(texto, encoding="utf-8")
    return True


def leer_previo(ruta, **kw) -> pd.DataFrame:
    return pd.read_csv(ruta, **kw) if ruta.exists() else pd.DataFrame()


def main() -> int:
    errores = []
    try:
        canasta = descargar_canasta()
        cambio = escribir(canasta, OUT_CANASTA, fechas=())
        print(f"  canasta COLCAP: {len(canasta)} acciones al {canasta['fecha_canasta'].iloc[0]}"
              f"{'' if cambio else ' (sin cambios)'}")
    except Exception as exc:
        errores.append(f"canasta: {exc}")
        canasta = leer_previo(OUT_CANASTA)
        print(f"  ERROR canasta: {exc} — se conserva la anterior ({len(canasta)} acciones)")
    if canasta.empty:
        print("  ERROR: no hay canasta para descargar precios")
        return 1

    previo = leer_previo(OUT_PRECIOS, parse_dates=["fecha"])
    nuevos = {}
    for t in canasta["ticker"]:
        try:
            nuevos[t] = serie_accion(t)
            df = nuevos[t][0]
            print(f"  {t:<11} {len(df):>4} semanas hasta {df['fecha'].max().date()}")
        except Exception as exc:
            errores.append(f"{t}: {exc}")
            print(f"  ERROR {t}: {exc} — se conserva la serie anterior")
        time.sleep(0.4)
    if nuevos:
        escribir(combinar(previo, nuevos), OUT_PRECIOS)
    print(f"  acciones actualizadas: {len(nuevos)} de {len(canasta)}")
    for e in errores:
        print(f"  FALLO {e}")
    # Falla total = error; fallas parciales solo avisan (la canasta sigue util).
    return 1 if not nuevos else 0


if __name__ == "__main__":
    sys.exit(main())
