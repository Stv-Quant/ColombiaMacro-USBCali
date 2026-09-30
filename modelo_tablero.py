"""Modelo de datos del tablero: carga tablas, calcula indicadores y redacta la lectura.

Separado de la capa Dash para poder probar cada cifra que aparece en pantalla.
Todas las frases del veredicto se derivan de reglas explicitas (umbrales abajo);
no hay texto escrito a mano que pueda quedar desactualizado.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

import analitica_macro as am

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("MACRO_DATA_DIR", BASE_DIR))

# Tasa real neutral de referencia: estimacion del equipo tecnico de BanRep de 2,7% (2025)
# con senal de subida hacia 3,0% (2026). Parametro externo, documentado en METODOLOGIA.md.
NEUTRAL_REAL = (2.7, 3.0)
UMBRAL_BRECHA = 0.5      # |brecha| < 0,5% del PIB potencial = "cerca del potencial"
UMBRAL_POSTURA = 0.5     # pp sobre/bajo el rango neutral para calificar la postura
ANCLA_EXPECTATIVAS = 4.0 # techo del rango meta: 5y5y por encima = expectativas desancladas


def _read(name: str, **kw) -> pd.DataFrame | None:
    for folder in (DATA_DIR, BASE_DIR):
        path = folder / name
        if path.exists():
            return pd.read_csv(path, **kw)
    return None


def _serie(long: pd.DataFrame | None, name: str) -> pd.DataFrame:
    if long is None:
        return pd.DataFrame(columns=["fecha", name])
    sub = long.loc[long["serie"] == name, ["fecha", "valor"]].rename(columns={"valor": name})
    return sub.sort_values("fecha").reset_index(drop=True)


TES_COLS = ["tes_pesos_1y", "tes_pesos_5y", "tes_pesos_10y", "tes_uvr_1y", "tes_uvr_5y", "tes_uvr_10y"]


def limpiar_saltos_tes(tes: pd.DataFrame) -> pd.DataFrame:
    """Oculta en los calculos derivados los saltos aislados de un dia (> 2 pp y revertidos).

    Mismo criterio que validar_datos.isolated_tes_spikes; el CSV original no se modifica.
    """
    from validar_datos import isolated_tes_spikes
    out = tes.copy()
    for col in TES_COLS:
        if col in out:
            out.loc[isolated_tes_spikes(out[col]), col] = np.nan
    return out


@dataclass
class Datos:
    pib: pd.DataFrame
    ipc: pd.DataFrame
    tes: pd.DataFrame
    colcap: pd.DataFrame
    estado: pd.DataFrame
    ciclo: pd.DataFrame
    inflacion: pd.DataFrame
    tasas: pd.DataFrame
    mercado: pd.DataFrame
    ise: pd.DataFrame | None
    laboral: pd.DataFrame | None
    extra: dict = field(default_factory=dict)
    legado: pd.DataFrame | None = None


def cargar() -> Datos:
    pib = _read("pib_colombia.csv", parse_dates=["fecha"]).dropna(subset=["pib_real_yoy"])
    ipc = _read("inflacion_clean.csv", parse_dates=["fecha"])
    tes = _read("tasas_interes_clean.csv", parse_dates=["fecha"])
    colcap = _read("colcap_oficial.csv", parse_dates=["fecha"])
    estado = _read("estado_fuentes.csv")
    long = _read("series_banrep.csv", parse_dates=["fecha"])
    extra = {k: _serie(long, k) for k in (
        "tpm", "trm", "ibr_overnight", "inflacion_basica_sar", "inflacion_sin_alimentos",
        "inflacion_nucleo15", "inflacion_regulados", "inflacion_alimentos", "meta_inflacion",
        "itcr_ipc", "terminos_intercambio", "reservas_netas_musd", "cuenta_corriente_pct_pib",
        "ied_musd", "deuda_bruta_gnc_pct_pib", "salario_minimo_var")}
    tpm = extra["tpm"] if not extra["tpm"].empty else None
    trm = extra["trm"] if not extra["trm"].empty else None

    tes = limpiar_saltos_tes(tes)
    inflacion = am.regimen_inflacion(ipc)
    for k in ("inflacion_basica_sar", "inflacion_sin_alimentos", "inflacion_alimentos",
              "inflacion_regulados"):
        if not extra[k].empty:
            inflacion = inflacion.merge(extra[k], on="fecha", how="left")
    ise = _read("ise_mensual.csv", parse_dates=["fecha"])
    laboral = _read("mercado_laboral.csv", parse_dates=["fecha"])
    legado = _read("indices_colombia.csv", parse_dates=["fecha"])
    return Datos(pib=pib, ipc=ipc, tes=tes, colcap=colcap, estado=estado,
                 ciclo=am.tabla_ciclo(pib), inflacion=inflacion,
                 tasas=am.depurar_derivadas(am.tabla_tasas(tes, tpm, ipc))[0],
                 mercado=am.tabla_mercado(colcap, trm, ipc),
                 ise=ise, laboral=laboral, extra=extra, legado=legado)


# ---------------------------------------------------------------- instantanea
def _last(df: pd.DataFrame | None, col: str):
    if df is None or col not in df or df[col].dropna().empty:
        return None
    row = df.dropna(subset=[col]).iloc[-1]
    return {"valor": float(row[col]), "fecha": pd.Timestamp(row["fecha"])}


def _hace(df: pd.DataFrame, col: str, fecha: pd.Timestamp, dias: int):
    sub = df.dropna(subset=[col])
    sub = sub[sub["fecha"] <= fecha - pd.Timedelta(days=dias)]
    return None if sub.empty else float(sub.iloc[-1][col])


def instantanea(d: Datos) -> dict:
    s: dict = {}
    c = d.ciclo.dropna(subset=["brecha_hp_tiempo_real"]).iloc[-1]
    s["ciclo"] = {k: (float(c[k]) if isinstance(c[k], (int, float, np.floating)) else c[k])
                  for k in ("trimestre", "pib_real_yoy", "pib_real_qoq_saar", "brecha_hp_tiempo_real",
                            "brecha_min", "brecha_max", "delta_brecha", "fase", "fase_hamilton",
                            "crecimiento_potencial_hp", "metodos_brecha_positiva",
                            "metodos_disponibles")}
    s["ciclo"]["fecha"] = pd.Timestamp(c["fecha"])

    inf = d.inflacion.iloc[-1]
    s["inflacion"] = {"total": float(inf["inflacion_anual"]), "fecha": pd.Timestamp(inf["fecha"]),
                      "mensual": float(inf["inflacion_mensual"]),
                      "cambio_3m": float(inf["cambio_3m_pp"]),
                      "hace_12m": _hace(d.inflacion, "inflacion_anual", inf["fecha"], 360)}
    b = _last(d.inflacion, "inflacion_basica_sar")
    s["inflacion"]["basica"] = b["valor"] if b else None

    t = d.tasas.dropna(subset=["tes_pesos_10y"]).iloc[-1]
    s["tasas"] = {k: (float(t[k]) if k in t and pd.notna(t[k]) else None) for k in (
        "tes_pesos_1y", "tes_pesos_5y", "tes_pesos_10y", "bei_1y", "bei_5y", "bei_10y", "bei_5y5y",
        "pendiente_10y_1y", "tpm", "tpm_real_exante", "tpm_real_expost", "pendiente_10y_tpm")}
    s["tasas"]["fecha"] = pd.Timestamp(t["fecha"])
    s["tasas"]["tes10_hace_3m"] = _hace(d.tasas, "tes_pesos_10y", t["fecha"], 91)
    tpm = d.extra["tpm"]
    if not tpm.empty:
        cambios = tpm[tpm["tpm"].diff().fillna(0) != 0]
        ultimo = cambios.iloc[-1] if not cambios.empty else None
        s["tasas"]["tpm_ultimo_cambio"] = None if ultimo is None else {
            "fecha": pd.Timestamp(ultimo["fecha"]),
            "delta": float(ultimo["tpm"] - tpm[tpm["fecha"] < ultimo["fecha"]]["tpm"].iloc[-1])}
        s["tasas"]["tpm_hace_12m"] = _hace(tpm, "tpm", tpm["fecha"].max(), 365)

    m = d.mercado.iloc[-1]
    s["mercado"] = {"colcap": float(m["colcap_puntos"]), "fecha": pd.Timestamp(m["fecha"]),
                    "drawdown": float(m["drawdown_pct"]),
                    "colcap_12m": am.retorno_ventana(d.mercado["colcap_puntos"], d.mercado["fecha"], 365)}
    if "colcap_usd" in d.mercado:
        s["mercado"]["colcap_usd_12m"] = am.retorno_ventana(d.mercado["colcap_usd"], d.mercado["fecha"], 365)
    trm = d.extra["trm"]
    if not trm.empty:
        s["mercado"]["trm"] = float(trm["trm"].iloc[-1])
        s["mercado"]["trm_fecha"] = pd.Timestamp(trm["fecha"].iloc[-1])
        s["mercado"]["trm_12m"] = am.retorno_ventana(trm["trm"], trm["fecha"], 365)

    for key, col in (("itcr", "itcr_ipc"), ("cc", "cuenta_corriente_pct_pib"),
                     ("deuda", "deuda_bruta_gnc_pct_pib")):
        s[key] = _last(d.extra[col], col)
    s["ise"] = None
    if d.ise is not None:
        r = d.ise.dropna(subset=["ise_sa"]).iloc[-1]
        s["ise"] = {"fecha": pd.Timestamp(r["fecha"]), "yoy": float(r["ise_yoy"]),
                    "saar_3m": float(r["ise_sa_3m3m_saar"])}
    s["laboral"] = None
    if d.laboral is not None:
        r = d.laboral.dropna(subset=["td_sa"]).iloc[-1]
        s["laboral"] = {"fecha": pd.Timestamp(r["fecha"]), "td": float(r["td_sa"]),
                        "td_hace_12m": _hace(d.laboral, "td_sa", r["fecha"], 360)}
    return s


# ---------------------------------------------------------------- clasificaciones
def lectura_brecha(g: float) -> str:
    if g >= UMBRAL_BRECHA:
        return "encima"
    if g <= -UMBRAL_BRECHA:
        return "debajo"
    return "cerca"


def postura_monetaria(real_exante: float | None) -> str | None:
    if real_exante is None or pd.isna(real_exante):
        return None
    lo, hi = NEUTRAL_REAL
    if real_exante > hi + UMBRAL_POSTURA:
        return "restrictiva"
    if real_exante < lo - UMBRAL_POSTURA:
        return "expansiva"
    return "neutral"


def anclaje(bei_5y5y: float | None) -> str | None:
    if bei_5y5y is None or pd.isna(bei_5y5y):
        return None
    return "desancladas" if bei_5y5y > ANCLA_EXPECTATIVAS else "ancladas"


# ---------------------------------------------------------------- texto
def _n(x, dec=1, lang="es", signo=False):
    if x is None or pd.isna(x):
        return "—"
    txt = f"{x:+,.{dec}f}" if signo else f"{x:,.{dec}f}"
    if lang == "es":
        txt = txt.replace(",", "§").replace(".", ",").replace("§", ".")
    return txt


FASE_TXT = {k: {"es": v[0], "en": v[1]} for k, v in am.FASES.items()}


def veredicto(s: dict, lang: str = "es") -> dict:
    """Titular y cuatro parrafos cortos. Cada frase cita el dato que la sustenta."""
    c, i, t, m = s["ciclo"], s["inflacion"], s["tasas"], s["mercado"]
    brecha = lectura_brecha(c["brecha_hp_tiempo_real"])
    post = postura_monetaria(t.get("tpm_real_exante"))
    ancla = anclaje(t.get("bei_5y5y"))
    fase = FASE_TXT[c["fase"]][lang]
    acelera = i["cambio_3m"] > 0.1
    cede = i["cambio_3m"] < -0.1
    fuera = i["total"] > 4 or i["total"] < 2

    if lang == "es":
        pos = {"encima": "por encima de", "debajo": "por debajo de", "cerca": "cerca de"}[brecha]
        dir_inf = "acelerando" if acelera else ("cediendo" if cede else "estable")
        titular = (f"{fase}: la economía opera {pos} su potencial y la inflación "
                   f"({_n(i['total'], 2, lang)}%) está {dir_inf}"
                   + (" fuera del rango meta." if fuera else " dentro del rango meta."))
        act = (f"PIB real {c['trimestre']}: {_n(c['pib_real_yoy'], 1, lang)}% anual. Brecha del producto "
               f"{_n(c['brecha_hp_tiempo_real'], 1, lang, True)}% del potencial (rango entre métodos "
               f"{_n(c['brecha_min'], 1, lang, True)} a {_n(c['brecha_max'], 1, lang, True)}); crecimiento "
               f"potencial estimado {_n(c['crecimiento_potencial_hp'], 1, lang)}%.")
        if s.get("ise"):
            act += (f" El ISE a {s['ise']['fecha']:%m/%Y} crece {_n(s['ise']['yoy'], 1, lang)}% anual y "
                    f"{_n(s['ise']['saar_3m'], 1, lang)}% anualizado en el último trimestre móvil.")
        pre = (f"IPC {i['fecha']:%m/%Y}: {_n(i['total'], 2, lang)}% anual, "
               f"{_n(i['cambio_3m'], 2, lang, True)} pp en tres meses; meta 3% ±1 pp.")
        if i.get("basica") is not None:
            pre += f" Inflación básica (sin alimentos ni regulados): {_n(i['basica'], 2, lang)}%."
        pol = ""
        if t.get("tpm") is not None:
            pol = (f"Tasa de política {_n(t['tpm'], 2, lang)}%; tasa real ex ante "
                   f"{_n(t['tpm_real_exante'], 1, lang)}% frente a una neutral estimada de "
                   f"{_n(NEUTRAL_REAL[0], 1, lang)}–{_n(NEUTRAL_REAL[1], 1, lang)}%: postura {post}.")
        exp = (f"Los TES descuentan inflación de {_n(t['bei_1y'], 1, lang)}% a un año y "
               f"{_n(t['bei_5y5y'], 1, lang)}% en el tramo 5 a 10 años: expectativas {ancla} "
               f"respecto al techo de 4%.")
        mer = (f"TES 10 años {_n(t['tes_pesos_10y'], 2, lang)}%; COLCAP "
               f"{_n(m['colcap_12m'], 1, lang, True)}% en 12 meses")
        if m.get("colcap_usd_12m") is not None:
            mer += f" ({_n(m['colcap_usd_12m'], 1, lang, True)}% en dólares)"
        if m.get("trm") is not None:
            mer += f"; TRM {_n(m['trm'], 0, lang)} COP/USD ({_n(m['trm_12m'], 1, lang, True)}% en 12 meses)"
        mer += "."
    else:
        pos = {"encima": "above", "debajo": "below", "cerca": "close to"}[brecha]
        dir_inf = "accelerating" if acelera else ("easing" if cede else "stable")
        titular = (f"{fase}: the economy is operating {pos} potential and inflation "
                   f"({_n(i['total'], 2, lang)}%) is {dir_inf}"
                   + (" outside the target range." if fuera else " inside the target range."))
        act = (f"Real GDP {c['trimestre'].replace('T', 'Q')}: {_n(c['pib_real_yoy'], 1, lang)}% y/y. Output gap "
               f"{_n(c['brecha_hp_tiempo_real'], 1, lang, True)}% of potential (range across methods "
               f"{_n(c['brecha_min'], 1, lang, True)} to {_n(c['brecha_max'], 1, lang, True)}); estimated "
               f"potential growth {_n(c['crecimiento_potencial_hp'], 1, lang)}%.")
        if s.get("ise"):
            act += (f" The monthly activity index (ISE, {s['ise']['fecha']:%m/%Y}) grows "
                    f"{_n(s['ise']['yoy'], 1, lang)}% y/y and {_n(s['ise']['saar_3m'], 1, lang)}% 3m/3m annualised.")
        pre = (f"CPI {i['fecha']:%m/%Y}: {_n(i['total'], 2, lang)}% y/y, "
               f"{_n(i['cambio_3m'], 2, lang, True)} pp over three months; target 3% ±1 pp.")
        if i.get("basica") is not None:
            pre += f" Core inflation (ex food and regulated): {_n(i['basica'], 2, lang)}%."
        post_en = {"restrictiva": "restrictive", "neutral": "neutral", "expansiva": "expansionary", None: "n/a"}[post]
        pol = ""
        if t.get("tpm") is not None:
            pol = (f"Policy rate {_n(t['tpm'], 2, lang)}%; ex-ante real rate "
                   f"{_n(t['tpm_real_exante'], 1, lang)}% vs an estimated neutral of "
                   f"{_n(NEUTRAL_REAL[0], 1, lang)}–{_n(NEUTRAL_REAL[1], 1, lang)}%: {post_en} stance.")
        ancla_en = {"desancladas": "de-anchored", "ancladas": "anchored", None: "n/a"}[ancla]
        exp = (f"TES breakevens price {_n(t['bei_1y'], 1, lang)}% inflation one year ahead and "
               f"{_n(t['bei_5y5y'], 1, lang)}% in the 5y5y forward: expectations {ancla_en} "
               f"relative to the 4% ceiling.")
        mer = (f"10-year TES {_n(t['tes_pesos_10y'], 2, lang)}%; COLCAP "
               f"{_n(m['colcap_12m'], 1, lang, True)}% over 12 months")
        if m.get("colcap_usd_12m") is not None:
            mer += f" ({_n(m['colcap_usd_12m'], 1, lang, True)}% in USD)"
        if m.get("trm") is not None:
            mer += f"; USD/COP {_n(m['trm'], 0, lang)} ({_n(m['trm_12m'], 1, lang, True)}% over 12 months)"
        mer += "."
    return {"titular": titular, "actividad": act, "precios": pre, "politica": pol,
            "expectativas": exp, "mercados": mer, "fase": c["fase"], "brecha": brecha,
            "postura": post, "anclaje": ancla}


def tabla_senales(d: Datos, s: dict, lang: str = "es") -> pd.DataFrame:
    """Indicador, ultimo dato, cambio, percentil historico desde 2010."""
    rows = []

    def add(key_es, key_en, df, col, unidad, dias, fecha_col="fecha", dec=2, relativo=False):
        if df is None or col not in df or df[col].dropna().empty:
            return
        sub = df.dropna(subset=[col])
        last = sub.iloc[-1]
        prev = _hace(sub, col, last[fecha_col], dias)
        rows.append({
            "indicador": key_es if lang == "es" else key_en,
            "valor": float(last[col]), "unidad": unidad, "dec": dec,
            "fecha": pd.Timestamp(last[fecha_col]),
            "cambio": None if prev is None else (100 * (float(last[col]) / prev - 1) if relativo
                                                 else float(last[col] - prev)),
            "relativo": relativo,
            "ventana": dias,
            "percentil": am.percentil(sub[col], float(last[col]), fechas=sub[fecha_col]),
        })

    add("PIB real, crecimiento anual", "Real GDP growth, y/y", d.ciclo, "pib_real_yoy", "%", 365, dec=1)
    add("Brecha del producto (HP tiempo real)", "Output gap (real-time HP)", d.ciclo,
        "brecha_hp_tiempo_real", "% pot.", 365, dec=1)
    if d.ise is not None:
        add("ISE, crecimiento anual", "Activity index (ISE), y/y", d.ise, "ise_yoy", "%", 365, dec=1)
    if d.laboral is not None:
        add("Desempleo (desestacionalizado)", "Unemployment rate (SA)", d.laboral, "td_sa", "%", 365, dec=1)
    add("Inflación anual", "Headline inflation", d.inflacion, "inflacion_anual", "%", 365)
    add("Inflación básica sin alim. ni regulados", "Core inflation ex food & regulated",
        d.inflacion, "inflacion_basica_sar", "%", 365)
    add("Inflación implícita 1 año (TES)", "1y breakeven inflation (TES)", d.tasas, "bei_1y", "%", 91)
    add("Inflación implícita 5y5y (TES)", "5y5y breakeven inflation (TES)", d.tasas, "bei_5y5y", "%", 91)
    add("Tasa de política BanRep", "BanRep policy rate", d.tasas, "tpm", "%", 365)
    add("Tasa real ex ante", "Ex-ante real policy rate", d.tasas, "tpm_real_exante", "%", 365)
    add("TES pesos 10 años", "10y TES yield", d.tasas, "tes_pesos_10y", "%", 91)
    add("Pendiente TES 10A–1A", "TES slope 10y–1y", d.tasas, "pendiente_10y_1y", "pp", 91)
    if not d.extra["trm"].empty:
        add("TRM (COP por USD)", "USD/COP (TRM)", d.extra["trm"], "trm", "COP", 365, dec=0, relativo=True)
    if not d.extra["itcr_ipc"].empty:
        add("Tasa de cambio real (ITCR)", "Real exchange rate (ITCR)", d.extra["itcr_ipc"],
            "itcr_ipc", "índice" if lang == "es" else "index", 365, dec=1, relativo=True)
    add("COLCAP (puntos)", "COLCAP (points)", d.mercado, "colcap_puntos", "pts", 365, dec=0, relativo=True)
    if not d.extra["cuenta_corriente_pct_pib"].empty:
        add("Cuenta corriente", "Current account", d.extra["cuenta_corriente_pct_pib"],
            "cuenta_corriente_pct_pib", "% PIB" if lang == "es" else "% GDP", 365, dec=1)
    if not d.extra["deuda_bruta_gnc_pct_pib"].empty:
        add("Deuda bruta GNC", "Central gov. gross debt", d.extra["deuda_bruta_gnc_pct_pib"],
            "deuda_bruta_gnc_pct_pib", "% PIB" if lang == "es" else "% GDP", 365, dec=1)
    return pd.DataFrame(rows)
