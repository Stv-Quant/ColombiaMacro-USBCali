"""Valida las tablas publicadas y genera el estado de cada fuente."""

import sys

import pandas as pd

from colombiamacro.config import DATA_DIR as BASE

TODAY = pd.Timestamp.today().normalize()
SOURCES = {
    "PIB real (DANE)": ("pib_colombia.csv", "trimestral", 130),
    "Inflación – IPC (DANE)": ("inflacion_clean.csv", "mensual", 45),
    "Tasas de los TES (BanRep)": ("tasas_interes_clean.csv", "diaria_mercado", 10),
    "Bolsa – COLCAP (BanRep)": ("colcap_oficial.csv", "diaria_mercado", 7),
}

# Fuentes complementarias: su ausencia no bloquea el tablero (se muestran como
# pendientes), pero si existen deben pasar los controles.
EXTRA_SOURCES = {
    # El DANE publica el ISE y la GEIH entre 30 y 50 dias despues del mes: un mes
    # fechado el dia 1 tiene normalmente entre 60 y 95 dias al publicarse.
    "Actividad mensual – ISE (DANE)": ("ise_mensual.csv", "mensual", 110),
    "Desempleo – GEIH (DANE)": ("mercado_laboral.csv", "mensual", 100),
}
# serie en series_banrep.csv: (nombre visible, frecuencia, dias de tolerancia)
BANREP_SERIES = {
    "tpm": ("Tasa de política (BanRep)", "diaria", 10),
    "trm": ("Dólar – TRM (BanRep)", "diaria", 10),
    "inflacion_basica_sar": ("Inflación básica (BanRep)", "mensual", 75),
    "itcr_ipc": ("Tasa de cambio real (BanRep)", "mensual", 100),
    "cuenta_corriente_pct_pib": ("Cuenta corriente (BanRep)", "trimestral", 200),
    "deuda_bruta_gnc_pct_pib": ("Deuda del Gobierno (MinHacienda)", "anual", 800),
}


def validate_extras():
    errors, warnings, states = [], [], []
    for name, (filename, frequency, stale_days) in EXTRA_SOURCES.items():
        path = BASE / filename
        if not path.exists():
            warnings.append(f"{filename}: pendiente de primera descarga")
            states.append({"fuente": name, "archivo": filename, "frecuencia": frequency,
                           "ultima_observacion": "", "ultima_publicacion_o_corte": "",
                           "estado": "pendiente"})
            continue
        df = pd.read_csv(path, parse_dates=["fecha"])
        if df["fecha"].duplicated().any() or not df["fecha"].is_monotonic_increasing:
            errors.append(f"{filename}: fechas duplicadas o desordenadas")
        if not df["fecha"].equals(pd.Series(pd.date_range(df["fecha"].min(), df["fecha"].max(),
                                                           freq="MS"), name="fecha")):
            errors.append(f"{filename}: faltan meses")
        if (df["fecha"] > TODAY).any():
            errors.append(f"{filename}: observaciones futuras")
        latest = df["fecha"].max()
        age = (TODAY - latest).days
        states.append({"fuente": name, "archivo": filename, "frecuencia": frequency,
                       "ultima_observacion": latest.strftime("%Y-%m-%d"),
                       "ultima_publicacion_o_corte": latest.strftime("%Y-%m-%d"),
                       "estado": "rezagado" if age > stale_days else "vigente"})
    if (BASE / "ise_mensual.csv").exists():
        ise = pd.read_csv(BASE / "ise_mensual.csv", parse_dates=["fecha"])
        expected = ise["ise_original"].pct_change(12, fill_method=None) * 100
        if (expected - ise["ise_yoy"]).abs().dropna().gt(1e-4).any():
            errors.append("ISE: ise_yoy no coincide con el indice original")
    if (BASE / "mercado_laboral.csv").exists():
        lab = pd.read_csv(BASE / "mercado_laboral.csv")
        implied = 100 * (1 - lab["to_sa"] / lab["tgp_sa"])  # TD = 1 - TO/TGP
        if (implied - lab["td_sa"]).abs().gt(0.05).any():
            errors.append("GEIH: TD no es consistente con TO y TGP")
    path = BASE / "series_banrep.csv"
    if not path.exists():
        warnings.append("series_banrep.csv: pendiente de primera descarga")
        for key, (label, freq, _) in BANREP_SERIES.items():
            states.append({"fuente": label, "archivo": "series_banrep.csv", "frecuencia": freq,
                           "ultima_observacion": "", "ultima_publicacion_o_corte": "",
                           "estado": "pendiente"})
        return errors, warnings, states
    long = pd.read_csv(path, parse_dates=["fecha"])
    if long.duplicated(["serie", "fecha"]).any():
        errors.append("series_banrep.csv: pares serie/fecha duplicados")
    if (long["fecha"] > TODAY).any():
        errors.append("series_banrep.csv: observaciones futuras")
    for key, (label, freq, stale_days) in BANREP_SERIES.items():
        sub = long[long["serie"] == key]
        if sub.empty:
            warnings.append(f"series_banrep.csv: falta {key}")
            continue
        latest = sub["fecha"].max()
        age = (TODAY - latest).days
        states.append({"fuente": label, "archivo": "series_banrep.csv", "frecuencia": freq,
                       "ultima_observacion": latest.strftime("%Y-%m-%d"),
                       "ultima_publicacion_o_corte": latest.strftime("%Y-%m-%d"),
                       "estado": "rezagado" if age > stale_days else "vigente"})
    return errors, warnings, states


def isolated_tes_spikes(series):
    previous = series.shift(1)
    following = series.shift(-1)
    return ((series - previous).abs() > 2
            ) & ((series - following).abs() > 2
                 ) & ((previous - following).abs() < 1)


def validate():
    errors, warnings, states, alerts = [], [], [], []
    tables = {}
    for name, (filename, frequency, stale_days) in SOURCES.items():
        path = BASE / filename
        if not path.exists():
            errors.append(f"{filename}: archivo ausente")
            continue
        df = pd.read_csv(path, parse_dates=["fecha"])
        tables[filename] = df
        if df.empty or df["fecha"].isna().any():
            errors.append(f"{filename}: tabla vacia o fechas invalidas")
            continue
        if df["fecha"].duplicated().any() or not df["fecha"].is_monotonic_increasing:
            errors.append(f"{filename}: fechas duplicadas o desordenadas")
        if (df["fecha"] > TODAY).any():
            errors.append(f"{filename}: observaciones futuras")
        latest = df["fecha"].max()
        published = latest
        if filename in ("pib_colombia.csv", "inflacion_clean.csv"):
            dates = pd.to_datetime(df["fecha_publicacion_vintage"], format="%Y-%m-%d",
                                   errors="coerce").dropna()
            if dates.empty:
                errors.append(f"{filename}: falta fecha de publicacion")
            else:
                published = dates.max()
        age = (TODAY - published).days
        states.append({"fuente": name, "archivo": filename, "frecuencia": frequency,
                       "ultima_observacion": latest.strftime("%Y-%m-%d"),
                       "ultima_publicacion_o_corte": published.strftime("%Y-%m-%d"),
                       "estado": "rezagado" if age > stale_days else "vigente"})
        if age > stale_days:
            warnings.append(f"{filename}: ultima observacion {latest.date()} ({age} dias)")

    if len(tables) != len(SOURCES):
        return errors, warnings, states, alerts

    pib = tables["pib_colombia.csv"].set_index("fecha")
    if not pib.index.equals(pd.date_range(pib.index.min(), pib.index.max(), freq="QS")):
        errors.append("PIB: faltan trimestres o fechas fuera de trimestre")
    for level, rate, lag in (
        ("pib_real_miles_millones_ref2015", "pib_real_yoy", 4),
        ("pib_real_ajustado_miles_millones_ref2015", "pib_real_qoq_sa", 1),
        ("pib_nominal_billones_cop", "pib_nominal_yoy", 4),
    ):
        expected = pib[level].pct_change(lag, fill_method=None) * 100
        if (expected - pib[rate]).abs().dropna().gt(0.0001).any():
            errors.append(f"PIB: {rate} no coincide con {level}")
    if not pib["fecha_publicacion_vintage"].nunique() == 1:
        errors.append("PIB: vintages mezclados")

    ipc = tables["inflacion_clean.csv"].set_index("fecha")
    if not ipc.index.equals(pd.date_range(ipc.index.min(), ipc.index.max(), freq="MS")):
        errors.append("IPC: faltan meses")
    if ipc[["inflacion_mensual", "inflacion_anual"]].isna().any().any():
        errors.append("IPC: variaciones faltantes")
    if not ipc["inflacion_mensual"].between(-5, 10).all() or not ipc["inflacion_anual"].between(-10, 50).all():
        errors.append("IPC: valores fuera de rango de control")
    if ipc.iloc[-1]["fuente_anual"] != "DANE_variacion_reportada":
        errors.append("IPC: la ultima variacion anual no esta contrastada con DANE")

    tes = tables["tasas_interes_clean.csv"]
    required_tes = ["tes_pesos_1y", "tes_pesos_5y", "tes_pesos_10y"]
    if tes[required_tes].isna().any().any() or not tes[required_tes].apply(
        lambda col: col.between(-5, 40).all()
    ).all():
        errors.append("TES: tasas pesos faltantes o fuera de rango")
    for col in required_tes:
        for _, point in tes.loc[isolated_tes_spikes(tes[col]), ["fecha", col]].iterrows():
            alerts.append({"archivo": "tasas_interes_clean.csv",
                           "fecha": point["fecha"].strftime("%Y-%m-%d"),
                           "variable": col, "valor": float(point[col]),
                           "tipo": "salto_aislado_revertido_mayor_2pp",
                           "accion": "conservado_en_csv_omitido_en_grafico"})
    if alerts:
        warnings.append(f"TES: {len(alerts)} observaciones aisladas sospechosas")

    colcap = tables["colcap_oficial.csv"]
    if (colcap["colcap_puntos"] <= 0).any() or colcap["colcap_puntos"].pct_change(
        fill_method=None
    ).abs().gt(0.25).any():
        errors.append("COLCAP: valor o salto diario invalido")
    base_row = colcap.loc[colcap["fecha"] == pd.Timestamp("2009-02-09"), "colcap_puntos"]
    if len(base_row) != 1 or (
        colcap["colcap_base100"] - colcap["colcap_puntos"] / base_row.iloc[0] * 100
    ).abs().gt(0.0001).any():
        errors.append("COLCAP: base 100 incorrecta")

    return errors, warnings, states, alerts


def main():
    errors, warnings, states, alerts = validate()
    e2, w2, s2 = validate_extras()
    errors, warnings, states = errors + e2, warnings + w2, states + s2
    for item in warnings:
        print("AVISO:", item)
    for item in errors:
        print("ERROR:", item)
    if errors:
        return 1
    pd.DataFrame(states).to_csv(BASE / "estado_fuentes.csv", index=False, lineterminator="\n")
    pd.DataFrame(alerts, columns=["archivo", "fecha", "variable", "valor", "tipo", "accion"]
                 ).to_csv(BASE / "alertas_datos.csv", index=False)
    print(pd.DataFrame(states).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
