"""
ColombiaMacro — Monitor del ciclo economico colombiano (v9).

Estructura narrativa (una pregunta por seccion):
  0. Veredicto: fase del ciclo y lectura automatica con las cifras que la sustentan.
  1. Actividad: ¿crece la economia por encima de su potencial?
  2. Precios: ¿esta la inflacion convergiendo a la meta?
  3. Politica y curva: ¿cual es la postura de BanRep y que descuenta el mercado?
  4. Mercados y sector externo: ¿como se reflejan en activos, peso y balanza?
  5. Tablero de senales, laboratorio (canastas historicas) y fuentes.

Cada grafico usa un solo eje y una sola unidad. Los calculos viven en
analitica_macro.py y modelo_tablero.py; este archivo solo presenta.
El tablero anterior se conserva en dashboard_legacy.py.

    python dashboard_colombia.py  ->  http://127.0.0.1:8050
"""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from flask import abort, send_from_directory

import analitica_macro as am
import modelo_tablero as mt

BASE_DIR = Path(__file__).resolve().parent

# ══════════════════════════════════════════════════════════ datos
D = mt.cargar()
S = mt.instantanea(D)

# ══════════════════════════════════════════════════════════ sistema visual
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#7a7974"
SURFACE, PANEL, RULE, GRID = "#fcfcfb", "#ffffff", "#e4e2dc", "#eeede8"
C1, C2, C3, C4, C7 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#4a3aa7"
GRAY_LINE = "#a3a19b"
BAND = "rgba(27,175,122,0.10)"
FASE_COLOR = {k: v[2] for k, v in am.FASES.items()}
FONT = "Inter, 'Segoe UI', system-ui, sans-serif"
SERIF = "'Source Serif 4', Georgia, serif"
MSCI = pd.Timestamp("2021-05-28")

MESES = {"es": ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"],
         "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]}

T = {  # (es, en)
    "kicker": ("Monitor del ciclo económico · Colombia", "Business-cycle monitor · Colombia"),
    "datos_al": ("Datos al", "Data as of"),
    "periodo": ("Horizonte", "Horizon"),
    "q1": ("¿Crece la economía por encima de su potencial?", "Is the economy growing above potential?"),
    "q2": ("¿Está la inflación convergiendo a la meta?", "Is inflation converging to target?"),
    "q3": ("¿Cuál es la postura de BanRep y qué descuenta el mercado?",
           "How tight is BanRep, and what is the market pricing?"),
    "q4": ("¿Cómo lo reflejan la bolsa, el peso y las cuentas externas?",
           "How do equities, the peso and external accounts reflect it?"),
    "q5": ("Tablero de señales", "Signal board"),
    "s1": ("Actividad", "Activity"), "s2": ("Precios", "Prices"),
    "s3": ("Política monetaria y curva", "Monetary policy & curve"),
    "s4": ("Mercados y sector externo", "Markets & external sector"),
    "s5": ("Señales", "Signals"),
    "k_act": ("Actividad", "Activity"), "k_inf": ("Inflación", "Inflation"),
    "k_pol": ("Política monetaria", "Monetary policy"), "k_mer": ("Mercados", "Markets"),
    "pib_yoy": ("PIB real, anual", "Real GDP, y/y"),
    "brecha": ("Brecha del producto", "Output gap"),
    "ipc": ("IPC anual", "Headline CPI"), "basica": ("Básica s/alim. ni regul.", "Core ex food & regulated"),
    "tpm": ("Tasa de política", "Policy rate"), "real": ("Real ex ante", "Ex-ante real"),
    "tes10": ("TES 10 años", "10y TES"), "colcap12": ("COLCAP 12 meses", "COLCAP 12m"),
    "trm": ("TRM", "USD/COP"),
    "g_brecha": ("Brecha del producto (% del PIB potencial)", "Output gap (% of potential GDP)"),
    "g_reloj": ("Reloj del ciclo: nivel y dirección de la brecha", "Cycle clock: level and direction of the gap"),
    "g_act": ("Crecimiento real anual: PIB trimestral, ISE mensual y potencial",
              "Real growth y/y: quarterly GDP, monthly ISE and potential"),
    "g_lab": ("Tasa de desempleo desestacionalizada", "Unemployment rate, seasonally adjusted"),
    "g_inf": ("Inflación total y básica frente al rango meta", "Headline and core inflation vs target range"),
    "g_comp": ("Inflación de alimentos y regulados", "Food and regulated-price inflation"),
    "g_exp": ("Expectativas de mercado: inflación implícita en TES", "Market expectations: TES breakeven inflation"),
    "g_pol": ("Tasa de política frente a inflación", "Policy rate vs inflation"),
    "g_real": ("Tasa de política real ex ante frente a la neutral estimada",
               "Ex-ante real policy rate vs estimated neutral"),
    "g_curva": ("Curva cero cupón TES pesos", "TES peso zero-coupon curve"),
    "g_pend": ("Pendiente de la curva", "Curve slope"),
    "g_colcap": ("COLCAP en pesos y en dólares (base 100 al inicio del horizonte)",
                 "COLCAP in pesos and in dollars (rebased to 100 at start of horizon)"),
    "g_trm": ("Tasa de cambio nominal: pesos por dólar (TRM)", "Nominal exchange rate: pesos per dollar (TRM)"),
    "g_itcr": ("Tasa de cambio real multilateral (ITCR-IPC, 2010 = 100)", "Multilateral real exchange rate (ITCR-CPI, 2010 = 100)"),
    "g_cc": ("Cuenta corriente (% del PIB, trimestral)", "Current account (% of GDP, quarterly)"),
    "g_deuda": ("Deuda bruta del Gobierno Nacional Central (% del PIB)",
                "Central government gross debt (% of GDP)"),
    "pendiente_fuente": ("Pendiente de la primera descarga automática de esta fuente.",
                         "Awaiting the first automated download of this source."),
    "metodo": ("Método y lectura", "Method and reading"),
    "col_ind": ("Indicador", "Indicator"), "col_ult": ("Último", "Latest"),
    "col_fecha": ("Referencia", "Reference"), "col_cambio": ("Cambio", "Change"),
    "col_pct": ("Percentil desde 2010", "Percentile since 2010"),
    "lab": ("Laboratorio: canastas bursátiles históricas (experimental)",
            "Lab: historical equity baskets (experimental)"),
    "fuentes": ("Fuentes, vigencia y descargas", "Sources, freshness and downloads"),
    "aviso": ("Tablero académico con datos oficiales. No constituye recomendación de inversión. "
              "Las estimaciones de brecha y postura son modelos con incertidumbre explícita.",
              "Academic dashboard built on official data. Not investment advice. "
              "Output-gap and stance estimates are models with explicit uncertainty."),
}


def tr(key: str, lang: str) -> str:
    es, en = T[key]
    return es if lang == "es" else en


def num(x, dec=1, lang="es", signo=False, suf=""):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    txt = f"{x:+,.{dec}f}" if signo else f"{x:,.{dec}f}"
    if lang == "es":
        txt = txt.replace(",", "§").replace(".", ",").replace("§", ".")
    return txt + suf


def fecha_txt(ts, freq: str, lang: str) -> str:
    ts = pd.Timestamp(ts)
    if freq == "q":
        q = (ts.month - 1) // 3 + 1
        return f"{'T' if lang == 'es' else 'Q'}{q} {ts.year}"
    if freq == "m":
        return f"{MESES[lang][ts.month - 1]} {ts.year}"
    if freq == "y":
        return str(ts.year)
    return f"{ts.day} {MESES[lang][ts.month - 1]} {ts.year}"


# ══════════════════════════════════════════════════════════ figuras
CONFIG = {"displaylogo": False, "responsive": True, "displayModeBar": "hover",
          "modeBarButtons": [["zoom2d", "pan2d", "resetScale2d", "toImage"]],
          "toImageButtonOptions": {"format": "png", "scale": 3}}


def base_fig(height=300, suffix="%", xdate=True):
    fig = go.Figure()
    fig.update_layout(
        height=height, margin=dict(l=8, r=12, t=8, b=8), paper_bgcolor=PANEL, plot_bgcolor=PANEL,
        font=dict(family=FONT, size=12, color=INK2), hovermode="x unified" if xdate else "closest",
        hoverlabel=dict(bgcolor=PANEL, bordercolor=RULE, font=dict(family=FONT, size=12, color=INK)),
        legend=dict(orientation="h", x=0, y=1.02, yanchor="bottom", xanchor="left",
                    font=dict(size=11, color=INK2), bgcolor="rgba(0,0,0,0)"),
        showlegend=True, dragmode="zoom",
    )
    fig.update_yaxes(ticksuffix=suffix, gridcolor=GRID, gridwidth=1, zeroline=False,
                     showline=False, tickfont=dict(size=11, color=MUTED), automargin=True)
    fig.update_xaxes(showgrid=False, showline=True, linecolor=RULE, ticks="outside",
                     tickcolor=RULE, tickfont=dict(size=11, color=MUTED), automargin=True)
    return fig


def rango(periodo: str, fin: pd.Timestamp):
    years = {"3A": 3, "5A": 5, "10A": 10}.get(periodo)
    if years is None:
        return None
    return [fin - pd.DateOffset(years=years), fin + pd.Timedelta(days=20)]


def recortar(df, periodo, fin, col="fecha"):
    r = rango(periodo, fin)
    return df if r is None else df[df[col] >= r[0] - pd.DateOffset(months=3)]


def line(fig, x, y, name, color, width=2, dash=None, fmt="%{y:.2f}%", mode="lines", **kw):
    fig.add_trace(go.Scatter(x=x, y=y, name=name, mode=mode,
                             line=dict(color=color, width=width, dash=dash),
                             hovertemplate=f"{fmt}<extra>{name}</extra>", **kw))


def banda_meta(fig, lang, x0=None, x1=None):
    fig.add_hrect(y0=2, y1=4, fillcolor=BAND, line_width=0, layer="below")
    fig.add_hline(y=3, line=dict(color=C3, width=1), layer="below")
    fig.add_annotation(xref="paper", x=0.995, y=4, yref="y", text="Meta 3% ±1" if lang == "es" else "Target 3% ±1",
                       showarrow=False, xanchor="right", yanchor="bottom", font=dict(size=10, color=C3))


def rango_robusto(fig, valores: pd.Series, fechas: pd.Series, lang: str, margen=1.0):
    """Si el horizonte incluye 2020-2021, fija el eje con los datos sin COVID y lo anota.

    Los puntos del choque quedan fuera de escala (visibles en el tooltip), para que la
    lectura reciente no quede aplastada por valores de -18% / +18%.
    """
    covid = (fechas >= pd.Timestamp("2020-01-01")) & (fechas <= pd.Timestamp("2022-06-30"))
    if not covid.any():
        return
    resto = valores[~covid].dropna()
    if resto.empty or valores[covid].abs().max() <= resto.abs().max() * 1.5:
        return
    lo, hi = float(resto.min()) - margen, float(resto.max()) + margen
    fig.update_yaxes(range=[lo, hi])
    fig.add_annotation(xref="paper", yref="paper", x=0.995, y=0.02, xanchor="right", yanchor="bottom",
                       showarrow=False, font=dict(size=10, color=MUTED),
                       text="2020–22 fuera de escala (ver tooltip)" if lang == "es" else "2020–22 off scale (see tooltip)")


def q_end(s: pd.Series) -> pd.Series:
    return s + pd.offsets.QuarterEnd(0)


def fig_brecha(lang, periodo):
    c = D.ciclo.dropna(subset=["brecha_hp_tiempo_real"])
    fin = q_end(c["fecha"]).max()
    c = recortar(c, periodo, fin)
    x = q_end(c["fecha"])
    fig = base_fig(300)
    fig.add_trace(go.Scatter(x=x, y=c["brecha_max"], line=dict(width=0), hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Scatter(x=x, y=c["brecha_min"], fill="tonexty", fillcolor="rgba(42,120,214,0.14)",
                             line=dict(width=0), name="Rango entre métodos" if lang == "es" else "Range across methods",
                             hovertemplate="%{y:.1f}%<extra>min</extra>"))
    line(fig, x, c["brecha_hp_tiempo_real"], "HP en tiempo real" if lang == "es" else "Real-time HP", C1,
         fmt="%{y:+.2f}%", mode="lines+markers", marker=dict(size=5))
    line(fig, x, c["brecha_hamilton"], "Hamilton (2018)", GRAY_LINE, width=1.2, fmt="%{y:+.2f}%")
    fig.add_hline(y=0, line=dict(color=INK2, width=1))
    rango_robusto(fig, pd.concat([c["brecha_min"], c["brecha_max"]]), pd.concat([x, x]), lang, 0.6)
    cov0, cov1 = pd.Timestamp(am.COVID_DESDE), q_end(pd.Series([pd.Timestamp(am.COVID_HASTA)])).iloc[0]
    if x.min() <= cov1:
        fig.add_vrect(x0=cov0, x1=cov1, fillcolor="rgba(0,0,0,0.04)", line_width=0, layer="below")
        fig.add_annotation(x=cov0, y=1, yref="paper", xanchor="left", yanchor="top", showarrow=False,
                           text="COVID: fuera de la tendencia" if lang == "es" else "COVID: excluded from trend",
                           font=dict(size=10, color=MUTED))
    fig.update_xaxes(range=rango(periodo, fin))
    return fig


def fig_reloj(lang):
    c = D.ciclo.dropna(subset=["brecha_hp_tiempo_real", "delta_brecha"]).tail(12).copy()
    fig = base_fig(300, suffix="", xdate=False)
    lim_x = max(2.0, float(c["brecha_hp_tiempo_real"].abs().max()) * 1.25)
    lim_y = max(1.5, float(c["delta_brecha"].abs().max()) * 1.25)
    quad = {"expansion": (1, 1), "desaceleracion": (1, -1), "contraccion": (-1, -1), "recuperacion": (-1, 1)}
    for k, (sx, sy) in quad.items():
        fig.add_annotation(x=sx * lim_x * 0.97, y=sy * lim_y * 0.95, showarrow=False,
                           xanchor="right" if sx > 0 else "left", yanchor="top" if sy > 0 else "bottom",
                           text=am.FASES[k][0 if lang == "es" else 1], font=dict(size=11, color=FASE_COLOR[k]))
    fig.add_hline(y=0, line=dict(color=RULE, width=1))
    fig.add_vline(x=0, line=dict(color=RULE, width=1))
    etiqueta = [fecha_txt(f, "q", lang) for f in c["fecha"]]
    fig.add_trace(go.Scatter(x=c["brecha_hp_tiempo_real"], y=c["delta_brecha"], mode="lines",
                             line=dict(color=GRAY_LINE, width=1), hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Scatter(
        x=c["brecha_hp_tiempo_real"], y=c["delta_brecha"], mode="markers", showlegend=False,
        marker=dict(size=[7] * (len(c) - 1) + [14], color=[FASE_COLOR[f] for f in c["fase"]],
                    line=dict(color=PANEL, width=2), opacity=[0.55] * (len(c) - 1) + [1]),
        text=etiqueta, customdata=[am.FASES[f][0 if lang == "es" else 1] for f in c["fase"]],
        hovertemplate=("%{text}<br>" + ("Brecha" if lang == "es" else "Gap") + " %{x:+.2f}%<br>"
                       + ("Cambio 2T" if lang == "es" else "2Q change") + " %{y:+.2f} pp<br>%{customdata}<extra></extra>")))
    last = c.iloc[-1]
    fig.add_annotation(x=last["brecha_hp_tiempo_real"], y=last["delta_brecha"], text=etiqueta[-1],
                       showarrow=True, arrowhead=0, ax=28, ay=-22, font=dict(size=11, color=INK))
    fig.update_xaxes(range=[-lim_x, lim_x], showline=False, ticksuffix="%", zeroline=False,
                     title=dict(text="Brecha (nivel)" if lang == "es" else "Gap (level)", font=dict(size=11)))
    fig.update_yaxes(range=[-lim_y, lim_y], ticksuffix=" pp",
                     title=dict(text="Cambio en 2 trimestres" if lang == "es" else "Change over 2 quarters",
                                font=dict(size=11)))
    return fig


def fig_actividad(lang, periodo):
    c = D.ciclo
    fin = max(q_end(c["fecha"]).max(), D.ise["fecha"].max() if D.ise is not None else pd.Timestamp(0))
    fig = base_fig(300)
    cc = recortar(c, periodo, fin)
    line(fig, q_end(cc["fecha"]), cc["pib_real_yoy"], "PIB real (trimestral)" if lang == "es" else "Real GDP (quarterly)",
         C1, mode="lines+markers", marker=dict(size=5), fmt="%{y:.1f}%")
    if D.ise is not None:
        ii = recortar(D.ise, periodo, fin)
        line(fig, ii["fecha"] + pd.offsets.MonthEnd(0), ii["ise_yoy"],
             "ISE (mensual, serie original)" if lang == "es" else "ISE (monthly, original)", C2, width=1.3, fmt="%{y:.1f}%")
    line(fig, q_end(cc["fecha"]), cc["crecimiento_potencial_hp"],
         "Crecimiento potencial (HP dos colas)" if lang == "es" else "Potential growth (two-sided HP)", GRAY_LINE, width=1.5, dash="dot",
         fmt="%{y:.1f}%")
    fig.add_hline(y=0, line=dict(color=INK2, width=1))
    vals, fechas = [cc["pib_real_yoy"]], [q_end(cc["fecha"])]
    if D.ise is not None:
        vals.append(ii["ise_yoy"]); fechas.append(ii["fecha"])
    rango_robusto(fig, pd.concat(vals), pd.concat(fechas), lang)
    fig.update_xaxes(range=rango(periodo, fin))
    return fig


def fig_laboral(lang, periodo):
    if D.laboral is None:
        return None
    lb = D.laboral
    fin = lb["fecha"].max()
    lb = recortar(lb, periodo, fin)
    fig = base_fig(260)
    line(fig, lb["fecha"], lb["td_sa"], "TD mensual" if lang == "es" else "Monthly rate", C1, width=1.2, fmt="%{y:.1f}%")
    line(fig, lb["fecha"], lb["td_sa_3m"], "Promedio 3 meses" if lang == "es" else "3-month average", C2, fmt="%{y:.1f}%")
    fig.update_xaxes(range=rango(periodo, fin))
    return fig


def fig_inflacion(lang, periodo):
    inf = D.inflacion
    fin = inf["fecha"].max()
    inf = recortar(inf, periodo, fin)
    fig = base_fig(320)
    banda_meta(fig, lang)
    line(fig, inf["fecha"], inf["inflacion_anual"], "IPC total" if lang == "es" else "Headline CPI", C1, width=2.2)
    if "inflacion_basica_sar" in inf:
        line(fig, inf["fecha"], inf["inflacion_basica_sar"], tr("basica", lang), C2)
    fig.update_xaxes(range=rango(periodo, fin))
    return fig


def fig_componentes(lang, periodo):
    inf = D.inflacion
    cols = [c for c in ("inflacion_alimentos", "inflacion_regulados") if c in inf]
    if not cols:
        return None
    fin = inf["fecha"].max()
    inf = recortar(inf, periodo, fin)
    fig = base_fig(260)
    banda_meta(fig, lang)
    names = {"inflacion_alimentos": ("Alimentos", "Food", C4), "inflacion_regulados": ("Regulados", "Regulated", C7)}
    for col in cols:
        es, en, color = names[col]
        line(fig, inf["fecha"], inf[col], es if lang == "es" else en, color)
    fig.update_xaxes(range=rango(periodo, fin))
    return fig


def semanal(df, cols):
    return (df.set_index("fecha")[cols].resample("W-FRI").last().dropna(how="all").reset_index())


def fig_expectativas(lang, periodo):
    t = D.tasas
    fin = t["fecha"].max()
    w = recortar(semanal(t, ["bei_1y", "bei_5y5y"]), periodo, fin)
    inf = recortar(D.inflacion, periodo, fin)
    fig = base_fig(320)
    banda_meta(fig, lang)
    line(fig, inf["fecha"] + pd.offsets.MonthEnd(0), inf["inflacion_anual"],
         "IPC observado" if lang == "es" else "Realised CPI", GRAY_LINE, width=1.4)
    line(fig, w["fecha"], w["bei_1y"], "Implícita 1 año" if lang == "es" else "1y breakeven", C1)
    line(fig, w["fecha"], w["bei_5y5y"], "Implícita 5 años dentro de 5 (5y5y)" if lang == "es" else "5y5y forward breakeven", C7)
    fig.update_xaxes(range=rango(periodo, fin))
    return fig


def fig_politica(lang, periodo):
    if D.extra["tpm"].empty:
        return None
    t = D.tasas
    fin = t["fecha"].max()
    w = recortar(semanal(t, ["tpm", "bei_1y"]), periodo, fin)
    inf = recortar(D.inflacion, periodo, fin)
    fig = base_fig(320)
    banda_meta(fig, lang)
    fig.add_trace(go.Scatter(x=w["fecha"], y=w["tpm"], name=tr("tpm", lang), line=dict(color=C1, width=2.4, shape="hv"),
                             hovertemplate="%{y:.2f}%<extra>" + tr("tpm", lang) + "</extra>"))
    line(fig, inf["fecha"] + pd.offsets.MonthEnd(0), inf["inflacion_anual"], tr("ipc", lang), C2)
    line(fig, w["fecha"], w["bei_1y"], "Inflación implícita 1 año" if lang == "es" else "1y breakeven", GRAY_LINE, width=1.4)
    fig.update_xaxes(range=rango(periodo, fin))
    return fig


def fig_real(lang, periodo):
    if D.extra["tpm"].empty:
        return None
    t = D.tasas
    fin = t["fecha"].max()
    w = recortar(semanal(t, ["tpm_real_exante", "tpm_real_expost"]), periodo, fin)
    fig = base_fig(320)
    lo, hi = mt.NEUTRAL_REAL
    fig.add_hrect(y0=lo, y1=hi, fillcolor="rgba(82,81,78,0.10)", line_width=0, layer="below")
    fig.add_annotation(xref="paper", x=0.005, y=hi, text=("Neutral estimada BanRep 2025–26" if lang == "es"
                                                          else "BanRep neutral estimate 2025–26"),
                       showarrow=False, xanchor="left", yanchor="bottom", font=dict(size=10, color=INK2))
    line(fig, w["fecha"], w["tpm_real_exante"], "Ex ante (deflactada con implícita 1A)" if lang == "es"
         else "Ex ante (deflated by 1y breakeven)", C1)
    line(fig, w["fecha"], w["tpm_real_expost"], "Ex post (deflactada con IPC)" if lang == "es"
         else "Ex post (deflated by CPI)", GRAY_LINE, width=1.4)
    fig.add_hline(y=0, line=dict(color=INK2, width=1))
    fig.update_xaxes(range=rango(periodo, fin))
    return fig


def fig_curva(lang):
    t = D.tasas.dropna(subset=["tes_pesos_10y"])
    hoy = t["fecha"].max()
    fig = base_fig(300, xdate=False)
    specs = [(0, C1, 2.6, "hoy" if lang == "es" else "today"),
             (91, C2, 1.6, "hace 3 meses" if lang == "es" else "3 months ago"),
             (365, GRAY_LINE, 1.6, "hace 12 meses" if lang == "es" else "12 months ago")]
    for dias, color, width, label in specs:
        row = t[t["fecha"] <= hoy - pd.Timedelta(days=dias)].iloc[-1]
        y = [row["tes_pesos_1y"], row["tes_pesos_5y"], row["tes_pesos_10y"]]
        name = f"{fecha_txt(row['fecha'], 'd', lang)} ({label})"
        fig.add_trace(go.Scatter(x=[1, 5, 10], y=y, name=name, mode="lines+markers",
                                 line=dict(color=color, width=width), marker=dict(size=8, line=dict(color=PANEL, width=2)),
                                 hovertemplate="%{x}A: %{y:.2f}%<extra>" + name + "</extra>"))
    fig.update_xaxes(tickvals=[1, 5, 10], ticktext=["1A", "5A", "10A"] if lang == "es" else ["1y", "5y", "10y"],
                     range=[0.4, 10.6], title=dict(text="Plazo" if lang == "es" else "Tenor", font=dict(size=11)))
    return fig


def fig_pendiente(lang, periodo):
    t = D.tasas
    fin = t["fecha"].max()
    cols = ["pendiente_10y_1y"] + (["pendiente_10y_tpm"] if "pendiente_10y_tpm" in t else [])
    w = recortar(semanal(t, cols), periodo, fin)
    fig = base_fig(300, suffix=" pp")
    line(fig, w["fecha"], w["pendiente_10y_1y"], "TES 10A − TES 1A" if lang == "es" else "10y − 1y TES", C1, fmt="%{y:+.2f} pp")
    if "pendiente_10y_tpm" in w:
        line(fig, w["fecha"], w["pendiente_10y_tpm"], "TES 10A − tasa de política" if lang == "es"
             else "10y TES − policy rate", C2, fmt="%{y:+.2f} pp")
    fig.add_hline(y=0, line=dict(color=INK2, width=1))
    fig.update_xaxes(range=rango(periodo, fin))
    return fig


def fig_colcap(lang, periodo):
    m = D.mercado
    fin = m["fecha"].max()
    r = rango(periodo, fin)
    mm = m if r is None else m[m["fecha"] >= r[0]]
    if periodo in ("10A", "MAX"):  # horizonte largo: cierre semanal, suficiente para la lectura
        mm = semanal(mm, [c for c in ("colcap_puntos", "colcap_usd") if c in mm])
    fig = base_fig(320, suffix="")
    base = mm["colcap_puntos"].iloc[0]
    line(fig, mm["fecha"], 100 * mm["colcap_puntos"] / base, "COLCAP en pesos" if lang == "es" else "COLCAP in COP",
         C1, fmt="%{y:.1f}")
    if "colcap_usd" in mm and mm["colcap_usd"].notna().any():
        u = mm.dropna(subset=["colcap_usd"])
        line(fig, u["fecha"], 100 * u["colcap_usd"] / u["colcap_usd"].iloc[0],
             "COLCAP en dólares" if lang == "es" else "COLCAP in USD", C2, fmt="%{y:.1f}")
    fig.add_hline(y=100, line=dict(color=INK2, width=1))
    if mm["fecha"].min() <= MSCI <= mm["fecha"].max():
        fig.add_vline(x=MSCI, line=dict(color=MUTED, width=1, dash="dot"))
        fig.add_annotation(x=MSCI, y=1, yref="paper", showarrow=False, xanchor="left", yanchor="top",
                           text=" BVC → MSCI", font=dict(size=10, color=MUTED))
    fig.update_xaxes(range=r)
    return fig


def fig_trm(lang, periodo):
    trm, itcr = D.extra["trm"], D.extra["itcr_ipc"]
    if trm.empty:
        return None
    fin = trm["fecha"].max()
    trm = recortar(trm, periodo, fin)
    if periodo in ("10A", "MAX"):
        trm = semanal(trm, ["trm"])
    fig = base_fig(320, suffix="")
    line(fig, trm["fecha"], trm["trm"], "TRM (COP por USD)" if lang == "es" else "USD/COP (TRM)", C1, fmt="%{y:,.0f}")
    fig.update_xaxes(range=rango(periodo, fin))
    return fig


def fig_itcr(lang, periodo):
    itcr = D.extra["itcr_ipc"]
    if itcr.empty:
        return None
    fin = itcr["fecha"].max()
    it = recortar(itcr, periodo, fin)
    fig = base_fig(260, suffix="")
    line(fig, it["fecha"], it["itcr_ipc"], "ITCR-IPC (2010=100)", C1, fmt="%{y:.1f}")
    fig.add_hline(y=100, line=dict(color=INK2, width=1))
    fig.add_annotation(xref="paper", x=0.005, y=1, yref="paper", showarrow=False, xanchor="left", yanchor="top",
                       text="↑ depreciación real · ↓ apreciación real" if lang == "es" else "↑ real depreciation · ↓ real appreciation",
                       font=dict(size=10, color=MUTED))
    fig.update_xaxes(range=rango(periodo, fin))
    return fig


def fig_barras(serie, lang, periodo, freq, color=C1, suffix="%"):
    df = D.extra[serie]
    if df.empty:
        return None
    fin = df["fecha"].max()
    df = recortar(df, periodo, fin)
    fig = base_fig(260, suffix=suffix)
    x = q_end(df["fecha"]) if freq == "q" else df["fecha"] + pd.offsets.YearEnd(0)
    fig.add_trace(go.Bar(x=x, y=df[serie], marker=dict(color=color, line=dict(width=0)), showlegend=False,
                         customdata=[fecha_txt(f, freq, lang) for f in df["fecha"]],
                         hovertemplate="%{customdata}: %{y:.1f}" + suffix + "<extra></extra>"))
    fig.update_layout(bargap=0.25)
    fig.add_hline(y=0, line=dict(color=INK2, width=1))
    return fig


def fig_laboratorio(lang):
    if D.legado is None:
        return None
    col = semanal(D.colcap, ["colcap_base100"])
    fig = base_fig(320, suffix="")
    line(fig, col["fecha"], col["colcap_base100"], "COLCAP oficial (BanRep)" if lang == "es" else "Official COLCAP (BanRep)",
         C1, fmt="%{y:.1f}")
    lg = semanal(D.legado, ["sintetico_base100", "grandes_base100"])
    line(fig, lg["fecha"], lg["sintetico_base100"], "Índice equiponderado (reconstrucción)" if lang == "es"
         else "Equal-weight basket (reconstruction)", C3, width=1.4, dash="dot", fmt="%{y:.1f}")
    line(fig, lg["fecha"], lg["grandes_base100"], "“7 Magníficas” (reconstrucción)" if lang == "es"
         else "“Magnificent 7” (reconstruction)", C4, width=1.4, dash="dot", fmt="%{y:.1f}")
    fig.add_hline(y=100, line=dict(color=INK2, width=1))
    return fig


# ══════════════════════════════════════════════════════════ componentes
def chart(title, fig, note=None, lang="es", wide=False):
    body = (dcc.Graph(figure=fig, config=CONFIG, className="graph",
                      style={"height": f"{fig.layout.height}px"}) if fig is not None
            else html.Div(tr("pendiente_fuente", lang), className="pending"))
    return html.Figure([html.Figcaption(title, className="chart-title"), body,
                        html.P(note, className="chart-note") if note else None],
                       className="chart wide" if wide else "chart")


def kpi(label, value, sub, extra=None, tone=None):
    return html.Div([
        html.Div(label, className="kpi-label"),
        html.Div(value, className="kpi-value"),
        html.Div(sub, className="kpi-sub"),
        html.Div(extra, className=f"kpi-extra {tone or ''}") if extra else None,
    ], className="kpi")


def section(n, key_s, key_q, lectura, children, metodo, lang):
    return html.Section([
        html.Header([html.Span(f"{n:02d}", className="sec-num"),
                     html.Div([html.Div(tr(key_s, lang), className="sec-kicker"),
                               html.H2(tr(key_q, lang), className="sec-title")])], className="sec-head"),
        html.Div([html.P(p) for p in lectura if p], className="lectura"),
        html.Div(children, className="grid"),
        html.Details([html.Summary(tr("metodo", lang)), dcc.Markdown(metodo, className="md")], className="metodo"),
    ], id=f"s{n}", className="section")


METODO = {
    "act": {
        "es": """
**Brecha del producto.** Se calcula sobre `100·ln(PIB real desestacionalizado)` (DANE, Cuadro 4, ref. 2015).
Tres estimaciones:
- *HP en tiempo real* (principal): filtro Hodrick-Prescott (λ = 1.600) aplicado en ventana creciente; en cada trimestre solo se usa información disponible hasta ese trimestre, lo que evita el sesgo de fin de muestra del HP de dos colas (Orphanides y van Norden, 2002).
- *HP de dos colas* (revisión ex post) y *Hamilton (2018)* (h = 8, p = 4) como contraste.
- Los trimestres 2020-T2 a 2021-T2 (confinamiento y paro nacional) se interpolan **solo para estimar la tendencia**; la brecha se mide contra el dato observado.

**Reloj del ciclo** (metodología OCDE): cuadrante según el signo de la brecha y de su cambio en dos trimestres.
El sombreado azul muestra el rango entre métodos: cuando es amplio, la fase debe leerse con cautela.

**ISE**: índice mensual de actividad del DANE; la variación anual usa la serie original (comparable con el PIB).
""",
        "en": """
**Output gap.** Computed on `100·ln(seasonally adjusted real GDP)` (DANE, table 4, 2015 reference).
Three estimates:
- *Real-time HP* (headline): Hodrick-Prescott (λ = 1,600) on an expanding window; each quarter uses only data available up to that quarter, avoiding the end-point bias of the two-sided filter (Orphanides & van Norden, 2002).
- *Two-sided HP* (ex-post revision) and *Hamilton (2018)* (h = 8, p = 4) as cross-checks.
- 2020-Q2 to 2021-Q2 (lockdown and national strike) are interpolated **only to estimate the trend**; the gap is measured against observed data.

**Cycle clock** (OECD method): quadrant given by the sign of the gap and of its two-quarter change.
The blue band shows the range across methods: when wide, read the phase with caution.

**ISE**: DANE's monthly activity index; the y/y change uses the original series (comparable with GDP).
"""},
    "pre": {
        "es": """
**Inflación total**: variación anual del IPC (DANE); el último mes usa la cifra publicada por el DANE.
**Básica**: sin alimentos ni regulados (BanRep, serie 15390), la medida que BanRep usa para leer presiones persistentes.
**Rango meta**: 3% ± 1 pp (BanRep, desde 2010).
**Expectativas de mercado**: inflación implícita (breakeven) `(1+y_pesos)/(1+y_UVR) − 1` con la curva cero cupón TES.
El *5y5y* es la inflación implícita promedio entre los años 5 y 10: `((1+y10)^10/(1+y5)^5)^(1/5)` en pesos y en UVR.
Incluye primas por riesgo inflacionario y liquidez; no es una expectativa pura.
""",
        "en": """
**Headline inflation**: annual CPI change (DANE); the latest month uses DANE's published figure.
**Core**: ex food and regulated prices (BanRep series 15390), BanRep's gauge of persistent pressure.
**Target range**: 3% ± 1 pp (BanRep, since 2010).
**Market expectations**: breakeven inflation `(1+y_COP)/(1+y_UVR) − 1` on TES zero-coupon curves.
The *5y5y* is average breakeven between years 5 and 10: `((1+y10)^10/(1+y5)^5)^(1/5)` in pesos and UVR.
It embeds inflation-risk and liquidity premia; it is not a pure expectation.
"""},
    "pol": {
        "es": f"""
**Tasa real ex ante** = `(1+TPM)/(1+inflación implícita 1A) − 1` (Fisher exacto). **Ex post** deflacta con el IPC ya publicado a cada fecha (sin usar datos futuros).
**Neutral de referencia**: {mt.NEUTRAL_REAL[0]}–{mt.NEUTRAL_REAL[1]}% real, estimación del equipo técnico de BanRep (2025, con ajuste al alza para 2026).
Postura = *restrictiva* si la tasa real ex ante supera el rango en más de {mt.UMBRAL_POSTURA} pp; *expansiva* si queda {mt.UMBRAL_POSTURA} pp por debajo.
**Curva**: TES cero cupón pesos (BanRep, modelo Nelson-Siegel). Pendiente positiva = el mercado exige más prima a plazos largos.
""",
        "en": f"""
**Ex-ante real rate** = `(1+policy rate)/(1+1y breakeven) − 1` (exact Fisher). **Ex post** deflates by the CPI already published at each date (no look-ahead).
**Neutral reference**: {mt.NEUTRAL_REAL[0]}–{mt.NEUTRAL_REAL[1]}% real, BanRep staff estimate (2025, revised upward for 2026).
Stance = *restrictive* if the ex-ante real rate exceeds the range by more than {mt.UMBRAL_POSTURA} pp; *expansionary* if {mt.UMBRAL_POSTURA} pp below.
**Curve**: TES peso zero-coupon (BanRep, Nelson-Siegel). A positive slope means investors demand more term premium.
"""},
    "mer": {
        "es": """
**COLCAP**: índice oficial publicado por BanRep (BVC; desde el 28-may-2021 metodología MSCI COLCAP con continuidad de niveles). Es un índice de precios: no incluye dividendos.
**COLCAP en dólares** = puntos / TRM del mismo día. **ITCR-IPC**: tasa de cambio real multilateral (2010 = 100); valores altos = peso real más débil.
**Cuenta corriente** y **deuda del GNC**: BanRep y Ministerio de Hacienda, vía el graficador de series de BanRep.
""",
        "en": """
**COLCAP**: official index published by BanRep (BVC; since 28-May-2021 MSCI COLCAP methodology with level continuity). A price index: excludes dividends.
**COLCAP in USD** = points / same-day TRM. **ITCR-CPI**: multilateral real exchange rate (2010 = 100); higher = weaker real peso.
**Current account** and **central-government debt**: BanRep and Ministry of Finance, via BanRep's series service.
"""},
}


def tabla_senales(lang):
    df = mt.tabla_senales(D, S, lang)
    head = html.Tr([html.Th(tr(k, lang)) for k in ("col_ind", "col_ult", "col_fecha", "col_cambio", "col_pct")])
    rows = []
    for _, r in df.iterrows():
        freq = "d"
        if r["indicador"].startswith(("PIB", "Brecha", "Real GDP", "Output")):
            freq = "q"
        elif any(w in r["indicador"] for w in ("Inflación anual", "básica", "Headline", "Core", "ISE", "Desempleo",
                                                "Unemployment", "ITCR")):
            freq = "m"
        elif r["indicador"].startswith(("Cuenta", "Current")):
            freq = "q"
        elif r["indicador"].startswith(("Deuda", "Central")):
            freq = "y"
        ventana = {91: "3m", 365: "12m"}[r["ventana"]]
        pct = r["percentil"]
        extremo = pct is not None and not np.isnan(pct) and (pct >= 90 or pct <= 10)
        rows.append(html.Tr([
            html.Td(r["indicador"]),
            html.Td(f"{num(r['valor'], r['dec'], lang)} {r['unidad']}", className="num"),
            html.Td(fecha_txt(r["fecha"], freq, lang), className="muted"),
            html.Td("—" if r["cambio"] is None or pd.isna(r["cambio"]) else
                    (f"{num(r['cambio'], 1, lang, True)}% ({ventana})" if r["relativo"] else
                     f"{num(r['cambio'], r['dec'], lang, True)} {'pp' if r['unidad'].startswith('%') else ''} ({ventana})"),
                    className="num"),
            html.Td(html.Div([html.Div(className="pct-track", children=html.Div(
                className="pct-fill" + (" extreme" if extremo else ""), style={"width": f"{0 if np.isnan(pct) else pct:.0f}%"})),
                html.Span(num(pct, 0, lang), className="pct-num")], className="pct"))]))
    return html.Table([html.Thead(head), html.Tbody(rows)], className="signals")


def tabla_estado(lang):
    est = D.estado
    if est is None:
        return None
    head = html.Tr([html.Th(x) for x in (("Fuente", "Frecuencia", "Último dato", "Estado") if lang == "es"
                                          else ("Source", "Frequency", "Latest", "Status"))])
    rows = [html.Tr([html.Td(r["fuente"]), html.Td(r["frecuencia"]), html.Td(r["ultima_observacion"] or "—"),
                     html.Td(html.Span(r["estado"], className=f"status {r['estado']}"))])
            for _, r in est.iterrows()]
    return html.Table([html.Thead(head), html.Tbody(rows)], className="signals compact")


DESCARGAS = ["pib_colombia.csv", "inflacion_clean.csv", "tasas_interes_clean.csv", "colcap_oficial.csv",
             "series_banrep.csv", "ise_mensual.csv", "mercado_laboral.csv", "estado_fuentes.csv"]


def fecha_corte():
    fechas = [S["tasas"]["fecha"], S["mercado"]["fecha"]]
    if S["mercado"].get("trm_fecha") is not None:
        fechas.append(S["mercado"]["trm_fecha"])
    return max(fechas)


def pagina(lang: str, periodo: str):
    v = mt.veredicto(S, lang)
    c, i, t, m = S["ciclo"], S["inflacion"], S["tasas"], S["mercado"]
    fase_label = am.FASES[c["fase"]][0 if lang == "es" else 1]
    postura = {"restrictiva": ("restrictiva", "restrictive"), "neutral": ("neutral", "neutral"),
               "expansiva": ("expansiva", "expansionary"), None: ("—", "—")}[v["postura"]][0 if lang == "es" else 1]

    hero = html.Section([
        html.Div([
            html.Div(tr("kicker", lang), className="kicker"),
            html.Div([html.Span(fase_label, className="phase-chip",
                                style={"background": FASE_COLOR[c["fase"]]}),
                      html.Span(f"{tr('datos_al', lang)} {fecha_txt(fecha_corte(), 'd', lang)}", className="asof")],
                     className="hero-meta"),
            html.H1(v["titular"], className="headline"),
            html.P(v["expectativas"], className="dek"),
        ], className="hero-text"),
        html.Div([
            kpi(tr("k_act", lang), num(c["pib_real_yoy"], 1, lang, suf="%"),
                f"{tr('pib_yoy', lang)} · {fecha_txt(c['fecha'], 'q', lang)}",
                f"{tr('brecha', lang)} {num(c['brecha_hp_tiempo_real'], 1, lang, True, '%')}"),
            kpi(tr("k_inf", lang), num(i["total"], 2, lang, suf="%"),
                f"{tr('ipc', lang)} · {fecha_txt(i['fecha'], 'm', lang)}",
                f"{tr('basica', lang)} {num(i.get('basica'), 2, lang, suf='%')}"),
            kpi(tr("k_pol", lang), num(t.get("tpm"), 2, lang, suf="%"),
                f"{tr('tpm', lang)} · {fecha_txt(t['fecha'], 'd', lang)}",
                f"{tr('real', lang)} {num(t.get('tpm_real_exante'), 1, lang, suf='%')} · {postura}"),
            kpi(tr("k_mer", lang), num(t["tes_pesos_10y"], 2, lang, suf="%"),
                f"{tr('tes10', lang)} · {fecha_txt(t['fecha'], 'd', lang)}",
                f"{tr('colcap12', lang)} {num(m['colcap_12m'], 1, lang, True, '%')}"
                + (f" · {tr('trm', lang)} {num(m['trm'], 0, lang)}" if m.get("trm") else "")),
        ], className="kpis"),
    ], className="hero")

    nav = html.Nav([html.A([html.Span(f"{n:02d}"), tr(k, lang)], href=f"#s{n}")
                    for n, k in ((1, "s1"), (2, "s2"), (3, "s3"), (4, "s4"), (5, "s5"))], className="toc")

    notas = {
        "brecha": ("Línea: estimación principal. Banda: mínimo y máximo entre HP tiempo real, HP dos colas y Hamilton."
                   if lang == "es" else "Line: headline estimate. Band: min–max across real-time HP, two-sided HP and Hamilton."),
        "reloj": ("Últimos 12 trimestres; el punto grande es el más reciente." if lang == "es"
                  else "Last 12 quarters; the large dot is the latest."),
    }
    s1 = section(1, "s1", "q1", [v["actividad"]], [
        chart(tr("g_brecha", lang), fig_brecha(lang, periodo), notas["brecha"], lang),
        chart(tr("g_reloj", lang), fig_reloj(lang), notas["reloj"], lang),
        chart(tr("g_act", lang), fig_actividad(lang, periodo), None, lang),
        chart(tr("g_lab", lang), fig_laboral(lang, periodo), None, lang),
    ], METODO["act"][lang], lang)
    s2 = section(2, "s2", "q2", [v["precios"], v["expectativas"]], [
        chart(tr("g_inf", lang), fig_inflacion(lang, periodo), None, lang),
        chart(tr("g_exp", lang), fig_expectativas(lang, periodo), None, lang),
        chart(tr("g_comp", lang), fig_componentes(lang, periodo), None, lang, wide=True),
    ], METODO["pre"][lang], lang)
    s3 = section(3, "s3", "q3", [v["politica"]], [
        chart(tr("g_pol", lang), fig_politica(lang, periodo), None, lang),
        chart(tr("g_real", lang), fig_real(lang, periodo), None, lang),
        chart(tr("g_curva", lang), fig_curva(lang), None, lang),
        chart(tr("g_pend", lang), fig_pendiente(lang, periodo), None, lang),
    ], METODO["pol"][lang], lang)
    s4 = section(4, "s4", "q4", [v["mercados"]], [
        chart(tr("g_colcap", lang), fig_colcap(lang, periodo), None, lang),
        chart(tr("g_trm", lang), fig_trm(lang, periodo), None, lang),
        chart(tr("g_itcr", lang), fig_itcr(lang, periodo), None, lang),
        chart(tr("g_cc", lang), fig_barras("cuenta_corriente_pct_pib", lang, periodo, "q"), None, lang),
        chart(tr("g_deuda", lang), fig_barras("deuda_bruta_gnc_pct_pib", lang, "MAX", "y", color=C7), None, lang, wide=True),
    ], METODO["mer"][lang], lang)
    s5 = html.Section([
        html.Header([html.Span("05", className="sec-num"),
                     html.Div([html.Div(tr("s5", lang), className="sec-kicker"),
                               html.H2(tr("q5", lang), className="sec-title")])], className="sec-head"),
        html.P(("Cada fila muestra el último dato, su cambio y en qué percentil de su propia historia (desde 2010) se ubica. "
                "Barras resaltadas: percentil ≤ 10 o ≥ 90." if lang == "es" else
                "Each row shows the latest value, its change and its percentile within its own history (since 2010). "
                "Highlighted bars: percentile ≤ 10 or ≥ 90."), className="lectura-p"),
        tabla_senales(lang),
        html.Details([html.Summary(tr("lab", lang)),
                      html.P(("Reconstrucciones propias heredadas del proyecto: retornos mensuales de canastas locales distribuidos "
                              "a días, sin ajuste por dividendos ni eventos corporativos y con composición posterior a 2021 aproximada. "
                              "No son índices oficiales ni alimentan ninguna cifra del tablero; se muestran para revisión metodológica."
                              if lang == "es" else
                              "Legacy in-house reconstructions: monthly basket returns spread to days, not adjusted for dividends or "
                              "corporate actions, with approximate post-2021 composition. Not official indices and not used anywhere "
                              "else in the dashboard; shown for methodological review."), className="chart-note"),
                      chart("COLCAP vs canastas (base 100 = 9-feb-2009)", fig_laboratorio(lang), None, lang, wide=True)],
                     className="metodo lab"),
        html.Details([html.Summary(tr("fuentes", lang)), tabla_estado(lang),
                      html.P([("Descargar datos: " if lang == "es" else "Download data: ")] +
                             [html.A(f, href=f"/datos/{f}", className="dl") for f in DESCARGAS
                              if (mt.DATA_DIR / f).exists() or (BASE_DIR / f).exists()], className="downloads"),
                      html.P(["Metodología completa: " if lang == "es" else "Full methodology: ",
                              html.A("METODOLOGIA.md", href="/datos/METODOLOGIA.md")], className="downloads")],
                     className="metodo", open=False),
    ], id="s5", className="section")
    return [hero, nav, s1, s2, s3, s4, s5,
            html.Footer([html.P(tr("aviso", lang)),
                         html.P("DANE · Banco de la República · BVC/MSCI · Ministerio de Hacienda")], className="foot")]


# ══════════════════════════════════════════════════════════ app
app = Dash(__name__, title="ColombiaMacro · Monitor del ciclo", assets_folder=str(BASE_DIR / "assets_v2"),
           external_stylesheets=["https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700"
                                 "&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&display=swap"],
           meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"},
                      {"name": "description", "content": "Monitor del ciclo económico colombiano con datos oficiales."}])
server = app.server


@server.route("/datos/<path:nombre>")
def descargar(nombre):
    permitidos = set(DESCARGAS) | {"METODOLOGIA.md", "DATA_DICTIONARY.md"}
    if nombre not in permitidos:
        abort(404)
    for folder in (mt.DATA_DIR, BASE_DIR):
        if (folder / nombre).exists():
            return send_from_directory(folder, nombre, as_attachment=nombre.endswith(".csv"))
    abort(404)


app.layout = html.Div([
    html.Div([
        html.Div([html.Img(src=app.get_asset_url("logo universisas.png"), className="logo"),
                  html.Div([html.Div("ColombiaMacro", className="brand"),
                            html.Div("USB Cali · FinancialTools", className="brand-sub")])], className="brand-wrap"),
        html.Div([
            html.Div([html.Span(id="lbl-periodo", className="ctl-label"),
                      dcc.RadioItems(id="periodo", value="10A", inline=True, className="seg",
                                     options=[{"label": x, "value": x} for x in ("3A", "5A", "10A", "MAX")])],
                     className="ctl"),
            dcc.RadioItems(id="lang", value="es", inline=True, className="seg",
                           options=[{"label": "ES", "value": "es"}, {"label": "EN", "value": "en"}]),
        ], className="controls"),
    ], className="topbar"),
    dcc.Loading(html.Main(id="main", className="main"), type="dot", color=C1),
], className="app")


@app.callback(Output("main", "children"), Output("lbl-periodo", "children"),
              Input("lang", "value"), Input("periodo", "value"))
def render(lang, periodo):
    return pagina(lang, periodo), tr("periodo", lang)


if __name__ == "__main__":
    app.run(debug=False, port=int(os.environ.get("PORT", 8050)))
