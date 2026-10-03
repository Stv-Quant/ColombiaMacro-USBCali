"""Tasa de cambio y sus determinantes: otras monedas, tasa de cambio real bilateral, balanza cambiaria,
compras de reservas, indice global del dolar y petroleo.

Fuentes oficiales:
  Banco de la Republica (graficador SUAMECA): tasas de cambio de otras monedas, ITCR bilaterales y de
  competitividad, balanza cambiaria mensual y subastas de opciones PUT para acumular reservas.
  Reserva Federal de EE. UU. vía FRED (Banco de la Reserva Federal de St. Louis): indice amplio del dolar
  (Junta de la Reserva Federal, H.10), peso mexicano por dolar (H.10) y precio del Brent (EIA).

Escribe cambiario.csv en formato largo: fecha, serie, valor, frecuencia, unidad, fuente, id
Uso: python -m colombiamacro.fuentes.cambiario [--local carpeta]
     (--local: carpeta con banrep_cambiario.json {id: respuesta SUAMECA} y fred_cambiario.json {id: csv})
"""

from __future__ import annotations

import argparse
import io
import json
import sys
import time
from pathlib import Path

import pandas as pd
import requests

from colombiamacro.config import data
from colombiamacro.fuentes.banrep import banrep_ca_bundle, fetch_series, parse_payload, write_if_changed

OUT = data("cambiario.csv")
COLS = ["fecha", "serie", "valor", "frecuencia", "unidad", "fuente", "id"]
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}

# serie: (id BanRep, texto esperado, frecuencia, unidad, rango valido)
BANREP = {
    "brl_usd":        (15638, "BRL/USD", "diaria", "reales por dólar", (0.5, 20)),
    "pen_usd":        (15641, "PEN/USD", "diaria", "soles por dólar", (0.5, 20)),
    "cop_eur":        (30, "COP/EUR", "diaria", "pesos por euro", (500, 20000)),
    "cop_gbp":        (31, "COP/GBP", "diaria", "pesos por libra", (500, 20000)),
    "cop_jpy":        (33, "COP/JPY", "diaria", "pesos por yen", (1, 200)),
    "cop_cny":        (28, "COP/CNY", "diaria", "pesos por yuan", (50, 3000)),
    "itcr_eeuu":      (219, "Bilateral con Estados Unidos", "mensual", "índice 2010=100", (20, 300)),
    "itcr_china":     (310, "Bilateral con China", "mensual", "índice 2010=100", (20, 300)),
    "itcr_brasil":    (213, "Bilateral con Brasil", "mensual", "índice 2010=100", (20, 400)),
    "itcr_mexico":    (226, "Bilateral con México", "mensual", "índice 2010=100", (20, 300)),
    "itcr_c":         (236, "ITCR-C", "mensual", "índice 2010=100", (20, 300)),
    "bc_cuenta_corriente": (16700, "Cuenta Corriente - Mensual", "mensual", "millones USD", (-1e5, 1e5)),
    "bc_comercial":   (16702, "Balanza Comercial - Mensual", "mensual", "millones USD", (-1e5, 1e5)),
    "bc_servicios":   (16704, "Servicios y Transferencias - Mensual", "mensual", "millones USD", (-1e5, 1e5)),
    "bc_capital":     (16706, "Movimientos netos de capital - Mensual", "mensual", "millones USD", (-1e5, 1e5)),
    "bc_capital_real_gob": (16708, "sector real y gobierno - Mensual", "mensual", "millones USD", (-1e5, 1e5)),
    "bc_reservas":    (16712, "Variación reservas brutas - Mensual", "mensual", "millones USD", (-1e5, 1e5)),
    "put_acumulacion": (16670, "PUT para acumulación de reservas - Monto aprobado", "evento", "dólares", (0, 1e11)),
}
# serie: (id FRED, frecuencia, unidad, rango valido, fuente)
FREDS = {
    "dolar_global": ("DTWEXBGS", "diaria", "índice ene 2006=100", (50, 200), "Reserva Federal (H.10) vía FRED"),
    "mxn_usd":      ("DEXMXUS", "diaria", "pesos mexicanos por dólar", (1, 60), "Reserva Federal (H.10) vía FRED"),
    "brent":        ("DCOILBRENTEU", "diaria", "USD por barril", (5, 300), "EIA vía FRED"),
}
MIN_OBS = {"diaria": 1000, "mensual": 120, "evento": 10}


def _fred_csv(texto: str, col: str) -> pd.DataFrame:
    df = pd.read_csv(io.StringIO(texto))
    df.columns = ["fecha", "valor"]
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    return df.dropna()


def _validar(df: pd.DataFrame, nombre: str, freq: str, unidad: str, rango, fuente: str, ident) -> pd.DataFrame:
    d = df.copy()
    if freq == "mensual":
        d["fecha"] = d["fecha"].dt.to_period("M").dt.to_timestamp()
    d = d[d["fecha"] <= pd.Timestamp.today().normalize()].drop_duplicates("fecha", keep="last")
    if len(d) < MIN_OBS[freq]:
        raise ValueError(f"solo {len(d)} observaciones")
    fuera = d.loc[~d["valor"].between(*rango)]
    if not fuera.empty:
        raise ValueError(f"{len(fuera)} valores fuera de {rango}")
    d["serie"], d["frecuencia"], d["unidad"], d["fuente"], d["id"] = nombre, freq, unidad, fuente, str(ident)
    return d[COLS]


def actualizar(local: Path | None = None) -> bool:
    filas, errores = [], []
    if local:
        crudo_b = json.loads((Path(local) / "banrep_cambiario.json").read_text(encoding="utf-8"))
        crudo_f = json.loads((Path(local) / "fred_cambiario.json").read_text(encoding="utf-8"))
        bajar_b = lambda sid, esp, col: parse_payload(crudo_b[str(sid)], sid, esp, col, drop_future=False)
        bajar_f = lambda fid: crudo_f[fid]
        bundle_ctx = None
    else:
        bundle_ctx = banrep_ca_bundle()
        bundle = bundle_ctx.__enter__()
        bajar_b = lambda sid, esp, col: fetch_series(sid, col, esp, verify=bundle, drop_future=False)
        def bajar_f(fid):
            r = requests.get(FRED, params={"id": fid}, headers=UA, timeout=60)
            r.raise_for_status()
            return r.text
    try:
        for nombre, (sid, esp, freq, unidad, rango) in BANREP.items():
            try:
                df = bajar_b(sid, esp, "valor")
                filas.append(_validar(df, nombre, freq, unidad, rango, "Banco de la República", sid))
            except Exception as exc:
                errores.append(f"{nombre}: {exc}")
            if not local:
                time.sleep(0.5)
        for nombre, (fid, freq, unidad, rango, fuente) in FREDS.items():
            try:
                filas.append(_validar(_fred_csv(bajar_f(fid), "valor"), nombre, freq, unidad, rango, fuente, fid))
            except Exception as exc:
                errores.append(f"{nombre}: {exc}")
    finally:
        if bundle_ctx is not None:
            bundle_ctx.__exit__(None, None, None)
    tabla = pd.concat(filas, ignore_index=True) if filas else pd.DataFrame(columns=COLS)
    if OUT.exists():  # conservar la ultima version valida de las series que fallaron hoy
        old = pd.read_csv(OUT, parse_dates=["fecha"], dtype={"id": str})
        faltan = set(old["serie"]) - set(tabla["serie"])
        if faltan:
            tabla = pd.concat([tabla, old[old["serie"].isin(faltan)]], ignore_index=True)
    if not tabla.empty:
        tabla = tabla.sort_values(["serie", "fecha"]).reset_index(drop=True)
        tabla["fecha"] = pd.to_datetime(tabla["fecha"]).dt.strftime("%Y-%m-%d")
        ch = write_if_changed(tabla, OUT, float_format="%.6g")
        print(f"cambiario.csv: {tabla['serie'].nunique()} de {len(BANREP) + len(FREDS)} series "
              f"({'actualizado' if ch else 'sin cambios'})")
    for e in errores:
        print(f"  ERROR {e}")
    return not errores


def cargar() -> dict[str, pd.Series] | None:
    if not OUT.exists():
        return None
    t = pd.read_csv(OUT, parse_dates=["fecha"], dtype={"id": str})
    return {k: g.set_index("fecha")["valor"].sort_index() for k, g in t.groupby("serie")}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--local", type=Path)
    a = ap.parse_args()
    sys.exit(0 if actualizar(a.local) else 1)
