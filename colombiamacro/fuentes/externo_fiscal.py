"""Cuentas externas y fiscales (Banco de la Republica, graficador SUAMECA).

Balanza de pagos trimestral (cuenta corriente por componentes y cuenta financiera por tipo de flujo), inversion
extranjera directa por sector, remesas, deuda externa publica y privada, posicion de inversion internacional,
reservas (PLI) y balance fiscal del Gobierno nacional central (mensual, caja) y del sector publico no financiero
(trimestral, caja).

Escribe externo_fiscal.csv: fecha (inicio del periodo), serie, valor, frecuencia, unidad, id_banrep
Uso: python -m colombiamacro.fuentes.externo_fiscal [--local archivo.json]
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

OUT = data("externo_fiscal.csv")
T, M, A = "trimestral", "mensual", "anual"
USD, COP = "millones USD", "miles de millones COP"
# serie: (id, frecuencia, unidad)
SERIES = {
    # cuenta corriente (balanza de pagos, millones de dolares, flujo del trimestre)
    "cc": (15136, T, USD), "bienes_servicios": (15135, T, USD), "bienes": (15706, T, USD), "servicios": (15719, T, USD),
    "ingreso_primario": (15140, T, USD), "ingreso_secundario": (15141, T, USD),
    "exportaciones_bienes": (15707, T, USD), "importaciones_bienes": (15708, T, USD),
    # cuenta financiera (signo BPM6: negativo = entrada neta de capital)
    "cf": (16142, T, USD), "cf_directa": (16143, T, USD), "cf_cartera": (16196, T, USD), "cf_otra": (16303, T, USD),
    "cf_reservas": (16527, T, USD), "cf_derivados": (16271, T, USD), "errores": (16544, T, USD),
    # inversion directa
    "ied": (15133, T, USD), "idce": (15134, T, USD),
    "ied_petroleo": (15377, T, USD), "ied_mineria": (15369, T, USD), "ied_industria": (15370, T, USD),
    "ied_financiero": (15375, T, USD), "ied_comercio": (15373, T, USD), "ied_transporte": (15374, T, USD),
    "ied_electricidad": (15371, T, USD), "ied_construccion": (15372, T, USD), "ied_servicios": (15376, T, USD),
    "ied_agro": (15368, T, USD),
    # remesas, deuda externa, posicion de inversion internacional, reservas
    "remesas": (15363, M, USD),
    "deuda_externa": (15330, M, USD), "deuda_externa_publica": (15331, M, USD), "deuda_externa_privada": (15332, M, USD),
    "deuda_externa_pib": (15329, M, "% PIB"),
    "pii_neta": (16600, T, USD), "pii_activos": (16601, T, USD), "pii_pasivos": (16602, T, USD),
    "reservas_pli": (16850, M, USD),
    # Gobierno nacional central (caja, mensual) y sector publico no financiero (caja, trimestral)
    "gnc_ingresos": (16722, M, COP), "gnc_gastos": (16723, M, COP), "gnc_intereses": (16724, M, COP), "gnc_balance": (16725, M, COP),
    "gnc_fin_interno": (16726, M, COP), "gnc_fin_externo": (16727, M, COP),
    "spnf_ingresos": (16728, T, COP), "spnf_gastos": (16729, T, COP), "spnf_intereses": (16730, T, COP), "spnf_balance": (16731, T, COP),
    "spnf_fin_interno": (16732, T, COP), "spnf_fin_externo": (16733, T, COP), "spnf_empresas_publicas": (16734, T, COP),
    "deuda_gnc_pib": (15328, A, "% PIB"),
    # precios del comercio exterior en dolares (indices encadenados de los terminos de intercambio)
    "precio_exportaciones": (15361, M, "índice"), "precio_importaciones": (15362, M, "índice"),
}


def _periodo(fechas: pd.Series, freq: str) -> pd.Series:
    return fechas.dt.to_period({"trimestral": "Q", "mensual": "M", "anual": "Y"}[freq]).dt.to_timestamp()


def actualizar(local: Path | None = None) -> bool:
    filas, errores = [], []
    crudo = json.loads(Path(local).read_text(encoding="utf-8")) if local else None
    ctx = None if local else banrep_ca_bundle()
    bundle = ctx.__enter__() if ctx else None
    try:
        for nombre, (sid, freq, unidad) in SERIES.items():
            try:
                if crudo is not None:
                    df = parse_payload(crudo[str(sid)], sid, None, "valor", drop_future=False)
                else:
                    df = fetch_series(sid, "valor", None, verify=bundle, drop_future=False)
                    time.sleep(0.4)
                df["fecha"] = _periodo(df["fecha"], freq)
                df = df.drop_duplicates("fecha", keep="last")
                if len(df) < 8:
                    raise ValueError(f"solo {len(df)} datos")
                df["serie"], df["frecuencia"], df["unidad"], df["id_banrep"] = nombre, freq, unidad, sid
                filas.append(df)
            except Exception as exc:
                errores.append(f"{nombre}: {exc}")
    finally:
        if ctx:
            ctx.__exit__(None, None, None)
    tabla = pd.concat(filas, ignore_index=True) if filas else pd.DataFrame()
    if OUT.exists():
        old = pd.read_csv(OUT, parse_dates=["fecha"])
        faltan = set(old["serie"]) - set(tabla.get("serie", []))
        if faltan:
            tabla = pd.concat([tabla, old[old["serie"].isin(faltan)]], ignore_index=True)
    if not tabla.empty:
        tabla = tabla[["fecha", "serie", "valor", "frecuencia", "unidad", "id_banrep"]].sort_values(["serie", "fecha"])
        tabla["fecha"] = pd.to_datetime(tabla["fecha"]).dt.strftime("%Y-%m-%d")
        ch = write_if_changed(tabla, OUT, float_format="%.4f")
        print(f"externo_fiscal.csv: {tabla['serie'].nunique()} de {len(SERIES)} series ({'actualizado' if ch else 'sin cambios'})")
    for e in errores:
        print(f"  ERROR {e}")
    return not errores


def cargar() -> dict[str, pd.Series] | None:
    if not OUT.exists():
        return None
    t = pd.read_csv(OUT, parse_dates=["fecha"])
    return {k: g.set_index("fecha")["valor"].sort_index() for k, g in t.groupby("serie")}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--local", type=Path)
    a = ap.parse_args()
    sys.exit(0 if actualizar(a.local) else 1)
