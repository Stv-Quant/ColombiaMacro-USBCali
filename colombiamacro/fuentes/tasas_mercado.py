"""Tasas de mercado, credito y liquidez del Banco de la Republica (graficador SUAMECA).

Complementa a series_banrep.csv con todo lo necesario para estudiar la transmision de la
tasa de politica: IBR por plazos, tasa interbancaria, DTF y CDT, tasas de colocacion por
modalidad, saldo de cartera por modalidad y saldos de las operaciones de liquidez (repos).

Escribe tasas_mercado.csv en formato largo: fecha, serie, valor, frecuencia, unidad, id_banrep
Uso: python -m colombiamacro.fuentes.tasas_mercado [--local suameca.json]
     (--local: archivo JSON {id: respuesta del graficador} descargado desde el navegador)
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import pandas as pd

from colombiamacro.config import data
from colombiamacro.fuentes.banrep import banrep_ca_bundle, fetch_series, parse_payload, write_if_changed

OUT = data("tasas_mercado.csv")
COLS = ["fecha", "serie", "valor", "frecuencia", "unidad", "id_banrep"]

# serie: (id BanRep, texto esperado en el nombre, frecuencia, unidad, rango valido)
SERIES = {
    # mercado monetario
    "ibr_1m":            (15325, "IBR) a 1 mes, efectiva",          "diaria",  "% e.a.", (0, 40)),
    "ibr_3m":            (15326, "IBR) a 3 meses, efectiva",        "diaria",  "% e.a.", (0, 40)),
    "ibr_6m":            (16561, "IBR) a 6 meses, efectiva",        "diaria",  "% e.a.", (0, 40)),
    "ibr_12m":           (16563, "IBR) a 12 meses, efectiva",       "diaria",  "% e.a.", (0, 40)),
    "tib":               (89,    "interbancaria",                   "diaria",  "% e.a.", (0, 80)),
    # captacion
    "dtf_90":            (65,    "DTF) a 90 días, semanal",         "semanal", "% e.a.", (0, 60)),
    "cdt_90":            (238,   "CDT) a 90 días, diaria",          "diaria",  "% e.a.", (0, 60)),
    "cdt_180":           (239,   "CDT) a 180 días, diaria",         "diaria",  "% e.a.", (0, 60)),
    "cdt_360":           (240,   "CDT) a 360 días, diaria",         "diaria",  "% e.a.", (0, 60)),
    # colocacion (semanal, promedio ponderado por monto desembolsado)
    "col_total":         (15110, "colocación Total, semanal",       "semanal", "% e.a.", (0, 80)),
    "col_sin_tesoreria": (17280, "colocación sin Tesorería, semanal", "semanal", "% e.a.", (0, 80)),
    "col_consumo":       (15111, "consumo, Tasa de interés, semanal", "semanal", "% e.a.", (0, 80)),
    "col_ordinario":     (15113, "(Ordinario), Tasa de interés, semanal", "semanal", "% e.a.", (0, 80)),
    "col_preferencial":  (15114, "(Preferencial o Corporativo), Tasa de interés, semanal", "semanal", "% e.a.", (0, 80)),
    "col_tesoreria":     (15115, "(Tesorería), Tasa de interés, semanal", "semanal", "% e.a.", (0, 80)),
    "col_vivienda":      (15105, "vivienda diferente de VIS (colocación en COP), Tasa de interés, semanal", "semanal", "% e.a.", (0, 80)),
    "col_vivienda_vis":  (15107, "vivienda VIS (colocación en COP), Tasa de interés, semanal", "semanal", "% e.a.", (0, 80)),
    # saldo de cartera en moneda legal (miles de millones de pesos)
    "cartera_total":     (373,   "Cartera Bruta sin ajuste por titularización en moneda legal, mensual", "mensual", "miles de millones COP", (1, 1e7)),
    "cartera_comercial": (363,   "Cartera comercial en moneda legal, mensual", "mensual", "miles de millones COP", (1, 1e7)),
    "cartera_consumo":   (365,   "consumo en moneda legal, mensual", "mensual", "miles de millones COP", (1, 1e7)),
    "cartera_vivienda":  (371,   "hipotecaria ajustada en moneda legal, mensual", "mensual", "miles de millones COP", (1, 1e7)),
    "cartera_micro":     (367,   "microcrédito en moneda legal, mensual", "mensual", "miles de millones COP", (0, 1e7)),
    # liquidez del Banco de la Republica (saldos diarios, miles de millones de pesos)
    "repo_1d":           (17500, "expansión plazo 1 día", "diaria", "miles de millones COP", (0, 1e6)),
    "repo_plazo":        (17501, "expansión a plazos diferentes de 1 día", "diaria", "miles de millones COP", (0, 1e6)),
    "contraccion":       (17503, "ventanilla de contracción", "diaria", "miles de millones COP", (0, 1e6)),
}
MIN_OBS = {"diaria": 500, "semanal": 200, "mensual": 60}


def validar(name: str, df: pd.DataFrame) -> pd.DataFrame:
    serie_id, _, freq, unit, (lo, hi) = SERIES[name]
    d = df.rename(columns={name: "valor"}).copy()
    if freq == "mensual":
        d["fecha"] = d["fecha"].dt.to_period("M").dt.to_timestamp()
    d = d[d["fecha"] <= pd.Timestamp.today().normalize()].drop_duplicates("fecha", keep="last")
    if len(d) < MIN_OBS[freq]:
        raise ValueError(f"solo {len(d)} observaciones")
    fuera = d.loc[~d["valor"].between(lo, hi)]
    if not fuera.empty:
        raise ValueError(f"{len(fuera)} valores fuera de [{lo}, {hi}]")
    d["serie"], d["frecuencia"], d["unidad"], d["id_banrep"] = name, freq, unit, serie_id
    return d[COLS]


def actualizar(local: Path | None = None) -> bool:
    frames, errores = {}, []
    if local:
        crudo = json.loads(Path(local).read_text(encoding="utf-8"))
        for name, (sid, esperado, *_r) in SERIES.items():
            try:
                frames[name] = parse_payload(crudo[str(sid)], sid, esperado, name, drop_future=False)
            except Exception as exc:
                errores.append(f"{name}: {exc}")
    else:
        with banrep_ca_bundle() as bundle:
            for name, (sid, esperado, *_r) in SERIES.items():
                for k in range(3):
                    try:
                        frames[name] = fetch_series(sid, name, esperado, verify=bundle, drop_future=False)
                        break
                    except Exception as exc:
                        if k == 2:
                            errores.append(f"{name}: descarga fallida: {exc}")
                        time.sleep(2 * (k + 1))
                time.sleep(0.5)
    filas = []
    for name, df in frames.items():
        try:
            filas.append(validar(name, df))
        except ValueError as exc:
            errores.append(f"{name}: {exc}")
    tabla = pd.concat(filas, ignore_index=True) if filas else pd.DataFrame(columns=COLS)
    if OUT.exists():  # conservar la ultima version valida de las series que fallaron hoy
        old = pd.read_csv(OUT, parse_dates=["fecha"])
        faltan = set(old["serie"]) - set(tabla["serie"])
        if faltan:
            tabla = pd.concat([tabla, old[old["serie"].isin(faltan)]], ignore_index=True)
    if not tabla.empty:
        tabla = tabla.sort_values(["serie", "fecha"]).reset_index(drop=True)
        tabla["fecha"] = pd.to_datetime(tabla["fecha"]).dt.strftime("%Y-%m-%d")
        ch = write_if_changed(tabla, OUT, float_format="%.6g")
        print(f"tasas_mercado.csv: {tabla['serie'].nunique()} de {len(SERIES)} series "
              f"({'actualizado' if ch else 'sin cambios'})")
    for e in errores:
        print(f"  ERROR {e}")
    return not errores


def cargar() -> dict[str, pd.Series] | None:
    """{serie: pd.Series indexada por fecha}."""
    if not OUT.exists():
        return None
    t = pd.read_csv(OUT, parse_dates=["fecha"])
    return {k: g.set_index("fecha")["valor"].sort_index() for k, g in t.groupby("serie")}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--local", type=Path)
    a = ap.parse_args()
    sys.exit(0 if actualizar(a.local) else 1)
