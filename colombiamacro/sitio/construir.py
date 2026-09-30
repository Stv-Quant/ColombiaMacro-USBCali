"""Construye el sitio estatico de ColombiaMacro (HTML + Plotly), en espanol e ingles.

    python -m colombiamacro.sitio.construir          # escribe site/
    python -m colombiamacro.sitio.construir --salida otra/carpeta

El sitio no necesita servidor: se publica en GitHub Pages (o cualquier hosting
estatico) y se abre en local con scripts/lanzar_local.py. Todas las cifras salen de
colombiamacro.modelo; aqui solo se presentan.
"""

from __future__ import annotations

import argparse
import html
import json
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from plotly.offline import get_plotlyjs

from colombiamacro import analitica as am
from colombiamacro import modelo as mt
from colombiamacro.config import DATA_DIR, DOCS_DIR, ROOT, SITE_DIR
from colombiamacro.sitio.textos import T, GLOSARIO

HERE = Path(__file__).resolve().parent
REPO_URL = "https://github.com/Stv-Quant/ColombiaMacro-USBCali"

# Paleta validada (skill dataviz, orden categorico fijo)
C1, C2, C3, C4, C7 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#4a3aa7"
GRAY, INK, INK2, MUTED, GRID, RULE = "#a3a19b", "#0b0b0b", "#52514e", "#7a7974", "#eeede8", "#dcdad4"
BAND = "rgba(27,175,122,0.12)"
FONT = "Inter, 'Segoe UI', system-ui, -apple-system, sans-serif"
MESES = {"es": ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"],
         "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]}
DESCARGAS = ["pib_colombia.csv", "inflacion_clean.csv", "tasas_interes_clean.csv", "colcap_oficial.csv",
             "series_banrep.csv", "ise_mensual.csv", "mercado_laboral.csv", "estado_fuentes.csv"]


# ------------------------------------------------------------------ formato
def num(x, dec=1, lang="es", signo=False, suf=""):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    txt = f"{x:+,.{dec}f}" if signo else f"{x:,.{dec}f}"
    if lang == "es":
        txt = txt.replace(",", "§").replace(".", ",").replace("§", ".")
    return txt + suf


def fecha(ts, freq, lang):
    ts = pd.Timestamp(ts)
    if freq == "q":
        return f"{'T' if lang == 'es' else 'Q'}{(ts.month - 1) // 3 + 1} {ts.year}"
    if freq == "m":
        return f"{MESES[lang][ts.month - 1]} {ts.year}"
    if freq == "y":
        return str(ts.year)
    return f"{ts.day} {MESES[lang][ts.month - 1]} {ts.year}"


def t(key, lang):
    v = T[key]
    return v[0] if lang == "es" else v[1]


def esc(s):
    return html.escape(str(s), quote=True)


# ------------------------------------------------------------------ graficos
def base(lang, height=330, suffix="%", fecha_x=True):
    fig = go.Figure()
    fig.update_layout(
        height=height, margin=dict(l=6, r=10, t=6, b=6), paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
        font=dict(family=FONT, size=12.5, color=INK2), separators=",." if lang == "es" else ".,",
        hovermode="x unified" if fecha_x else "closest",
        hoverlabel=dict(bgcolor="#ffffff", bordercolor=RULE, font=dict(family=FONT, size=12.5, color=INK)),
        legend=dict(orientation="h", x=0, y=1.0, yanchor="bottom", xanchor="left", bgcolor="rgba(0,0,0,0)",
                    font=dict(size=12, color=INK2)),
        showlegend=True,
    )
    fig.update_yaxes(ticksuffix=suffix, gridcolor=GRID, zeroline=False, tickfont=dict(size=11.5, color=MUTED),
                     automargin=True, fixedrange=True)
    fig.update_xaxes(showgrid=False, showline=True, linecolor=RULE, ticks="outside", tickcolor=RULE,
                     tickfont=dict(size=11.5, color=MUTED), automargin=True, fixedrange=True)
    if fecha_x:
        # Formato numerico de meses: evita nombres en ingles sin cargar traducciones de Plotly.
        fig.update_xaxes(type="date", hoverformat="%m/%Y", tickformatstops=[
            dict(dtickrange=[None, "M12"], value="%m/%Y"), dict(dtickrange=["M12", None], value="%Y")])
    return fig


# Cambio que acompana cada dato en el recuadro flotante y en la franja de resumen.
#   "pp"  diferencia en puntos porcentuales (tasas, inflacion, desempleo)
#   "pct" variacion porcentual (dolar, bolsa, indices)
PERIODOS = {"a": (pd.DateOffset(years=1), 20), "t": (pd.DateOffset(months=3), 20), "m": (pd.DateOffset(months=1), 12)}


def serie_cambio(x, y, modo, periodo="a"):
    """Cambio de cada punto frente al mismo punto un periodo antes (NaN si no hay dato cercano)."""
    s = pd.Series(pd.to_numeric(pd.Series(list(y)), errors="coerce").values, index=pd.to_datetime(pd.Series(list(x))))
    s = s[~s.index.duplicated(keep="last")].sort_index()
    base_ = s.dropna()
    if base_.empty:
        return pd.Series(np.nan, index=s.index)
    off, tol = PERIODOS[periodo]
    previo = base_.reindex(s.index - off, method="nearest", tolerance=pd.Timedelta(days=tol))
    previo.index = s.index
    return (s / previo - 1) * 100 if modo == "pct" else s - previo


def txt_cambio(v, modo, lang, dec=1):
    if v is None or pd.isna(v):
        return ""
    flecha = "▲" if v > 0.005 else ("▼" if v < -0.005 else "=")
    return f"{flecha} {num(v, dec, lang, True, '%' if modo == 'pct' else ' pp')}"


def etiqueta_periodo(periodo, lang):
    return t({"a": "vs_ano", "t": "vs_trim", "m": "vs_mes"}[periodo], lang)


def linea(fig, x, y, name, color, width=2.2, dash=None, fmt=".1f", suf="%", shape=None, cambio=None, lang="es"):
    """Serie de tiempo. cambio=("pp"|"pct", "a"|"t"|"m") agrega el cambio al recuadro flotante."""
    x = list(pd.to_datetime(pd.Series(list(x))))
    yy = [None if pd.isna(v) else round(float(v), 4) for v in y]
    kw = dict(hovertemplate=f"%{{y:{fmt}}}{suf}")
    if cambio:
        modo, periodo = cambio
        ch = serie_cambio(x, yy, modo, periodo).reindex(pd.DatetimeIndex(x))
        et = etiqueta_periodo(periodo, lang)
        kw["customdata"] = [(f"{txt_cambio(v, modo, lang)} {et}" if pd.notna(v) else "") for v in ch]
        kw["hovertemplate"] = f"%{{y:{fmt}}}{suf}  <span style='color:{MUTED}'>%{{customdata}}</span>"
    fig.add_trace(go.Scatter(x=x, y=yy, name=name, mode="lines",
                             line=dict(color=color, width=width, dash=dash, shape=shape), **kw))


def franja(lang, items):
    """Franja sobre el grafico: ultimo dato de cada serie y su cambio.
    items: (nombre, x, y, modo, periodo, freq, dec, suf)"""
    partes = []
    for nombre, x, y, modo, periodo, freq, dec, suf in items:
        s = pd.Series(list(pd.to_numeric(pd.Series(list(y)), errors="coerce")), index=pd.to_datetime(pd.Series(list(x))))
        s = s.dropna()
        if s.empty:
            continue
        valor = (("$" if suf == "$" else "") + num(s.iloc[-1], dec, lang) + ("" if suf == "$" else suf))
        cambios = []
        for per in (periodo if isinstance(periodo, (list, tuple)) else [periodo]):
            ch = serie_cambio(s.index, s.values, modo, per).iloc[-1]
            if pd.notna(ch):
                clase = "up" if ch > 0.005 else ("down" if ch < -0.005 else "flat")
                cambios.append(f'<span class="chg {clase}">{txt_cambio(ch, modo, lang)}</span> <small>{etiqueta_periodo(per, lang)}</small>')
        cambio = " &nbsp;·&nbsp; ".join(cambios)
        partes.append(f'<div class="stat"><span class="stat-n">{esc(nombre)}</span>'
                      f'<span class="stat-v">{valor}</span><span class="stat-f">{fecha(s.index[-1], freq, lang)}</span>'
                      f'<span class="stat-c">{cambio}</span></div>')
    return f'<div class="stats">{"".join(partes)}</div>' if partes else ""


def meta_banda(fig, lang):
    fig.add_hrect(y0=2, y1=4, fillcolor=BAND, line_width=0, layer="below")
    fig.add_hline(y=3, line=dict(color=C3, width=1.2), layer="below")
    fig.add_annotation(xref="paper", x=0.01, y=2, yref="y", yanchor="top", xanchor="left", showarrow=False,
                       text=t("meta_label", lang), font=dict(size=11, color="#127a55"))


def qend(s):
    return pd.to_datetime(s) + pd.offsets.QuarterEnd(0)


def semanal(df, cols):
    return df.set_index("fecha")[cols].resample("W-FRI").last().dropna(how="all").reset_index()


def rango_inicial(fin, anos=10):
    fin = pd.Timestamp(fin)
    return [(fin - pd.DateOffset(years=anos)).strftime("%Y-%m-%d"), (fin + pd.Timedelta(days=25)).strftime("%Y-%m-%d")]


class Graficos:
    """Cada metodo devuelve (figura, meta). meta["franja"] = HTML con el ultimo dato y su cambio."""

    def __init__(self, d: mt.Datos, s: dict, lang: str):
        self.d, self.s, self.lang = d, s, lang

    def _l(self, fig, x, y, name, color, **kw):
        linea(fig, x, y, name, color, lang=self.lang, **kw)

    # --- 1. crecimiento
    def crecimiento(self):
        L, d = self.lang, self.d
        c = d.ciclo
        fig = base(L)
        xq = qend(c["fecha"])
        yq = [round(float(v), 2) for v in c["pib_real_yoy"]]
        ch = serie_cambio(xq, yq, "pp", "t")
        fig.add_trace(go.Bar(x=list(xq), y=yq, name=t("pib_trim", L), marker=dict(color=C1, line=dict(width=0)),
                             customdata=[f"{txt_cambio(v, 'pp', L)} {t('vs_trim', L)}" if pd.notna(v) else "" for v in ch],
                             hovertemplate=f"%{{y:.1f}}%  <span style='color:{MUTED}'>%{{customdata}}</span>"))
        items = [(t("pib_trim", L), xq, yq, "pp", "t", "q", 1, "%")]
        if d.ise is not None:
            i = d.ise.dropna(subset=["ise_sa_yoy"])
            xi = i["fecha"] + pd.offsets.MonthEnd(0)
            self._l(fig, xi, i["ise_sa_yoy"], t("ise_mens", L), C2, width=1.6, cambio=("pp", "m"))
            items.append((t("ise_mens", L), xi, i["ise_sa_yoy"], "pp", "m", "m", 1, "%"))
        self._l(fig, xq, c["crecimiento_potencial_hp"], t("ritmo_normal", L), INK2, width=1.6, dash="dot")
        fig.add_hline(y=0, line=dict(color=INK2, width=1))
        fig.update_layout(bargap=0.35)
        fig.update_yaxes(range=[-8, 14])
        fig.add_annotation(xref="paper", yref="paper", x=0.99, y=0.02, xanchor="right", yanchor="bottom",
                           showarrow=False, text=t("covid_escala", L), font=dict(size=11, color=MUTED))
        fig.update_xaxes(range=rango_inicial(xq.max()))
        return fig, {"yfijo": True, "franja": franja(L, items)}

    def desempleo(self):
        L, lb = self.lang, self.d.laboral
        if lb is None:
            return None, {}
        fig = base(L)
        self._l(fig, lb["fecha"], lb["td_sa"], t("td_mensual", L), GRAY, width=1.2, cambio=("pp", "a"))
        self._l(fig, lb["fecha"], lb["td_sa_3m"], t("td_3m", L), C1, width=2.4, cambio=("pp", "a"))
        fig.update_xaxes(range=rango_inicial(lb["fecha"].max()))
        return fig, {"franja": franja(L, [(t("td_3m", L), lb["fecha"], lb["td_sa_3m"], "pp", "a", "m", 1, "%"),
                                          (t("td_mensual", L), lb["fecha"], lb["td_sa"], "pp", "a", "m", 1, "%")])}

    # --- 2. precios
    def inflacion(self):
        L, inf = self.lang, self.d.inflacion
        fig = base(L)
        meta_banda(fig, L)
        x = inf["fecha"] + pd.offsets.MonthEnd(0)
        self._l(fig, x, inf["inflacion_anual"], t("inf_total", L), C1, width=2.6, fmt=".2f", cambio=("pp", "a"))
        items = [(t("inf_total", L), x, inf["inflacion_anual"], "pp", "a", "m", 2, "%")]
        if "inflacion_basica_sar" in inf and inf["inflacion_basica_sar"].notna().any():
            self._l(fig, x, inf["inflacion_basica_sar"], t("inf_fondo", L), C2, fmt=".2f", cambio=("pp", "a"))
            items.append((t("inf_fondo", L), x, inf["inflacion_basica_sar"], "pp", "a", "m", 2, "%"))
        if "inflacion_mensual" in inf:
            items.append((t("inf_mes", L), x, inf["inflacion_mensual"], "pp", "a", "m", 2, "%"))
        fig.update_xaxes(range=rango_inicial(inf["fecha"].max()))
        return fig, {"franja": franja(L, items)}

    def expectativas(self):
        L, d = self.lang, self.d
        w = semanal(d.tasas, ["bei_1y", "bei_5y5y"])
        fig = base(L)
        meta_banda(fig, L)
        self._l(fig, d.inflacion["fecha"] + pd.offsets.MonthEnd(0), d.inflacion["inflacion_anual"], t("inf_observada", L),
                GRAY, width=1.5, fmt=".2f")
        self._l(fig, w["fecha"], w["bei_1y"], t("espera_1a", L), C7, width=2.2, cambio=("pp", "a"))
        fig.update_xaxes(range=rango_inicial(w["fecha"].max()))
        dd = d.tasas.dropna(subset=["bei_1y"])
        return fig, {"franja": franja(L, [(t("espera_1a", L), dd["fecha"], dd["bei_1y"], "pp", "a", "d", 1, "%")])}

    # --- 3. banco central
    def politica(self):
        L, d = self.lang, self.d
        if d.extra["tpm"].empty:
            return None, {}
        w = semanal(d.tasas, ["tpm"])
        fig = base(L)
        self._l(fig, w["fecha"], w["tpm"], t("tpm_linea", L), C1, width=2.6, fmt=".2f", shape="hv", cambio=("pp", "a"))
        xi = d.inflacion["fecha"] + pd.offsets.MonthEnd(0)
        self._l(fig, xi, d.inflacion["inflacion_anual"], t("inf_total", L), C2, fmt=".2f", cambio=("pp", "a"))
        fig.add_hline(y=3, line=dict(color=C3, width=1, dash="dot"))
        fig.update_xaxes(range=rango_inicial(w["fecha"].max()))
        tp = d.extra["tpm"]
        return fig, {"franja": franja(L, [(t("tpm_linea", L), tp["fecha"], tp["tpm"], "pp", "a", "d", 2, "%"),
                                          (t("inf_total", L), xi, d.inflacion["inflacion_anual"], "pp", "a", "m", 2, "%")])}

    # --- 4. mercados
    def dolar(self):
        L, trm = self.lang, self.d.extra["trm"]
        if trm.empty:
            return None, {}
        w = semanal(trm, ["trm"])
        fig = base(L, suffix="")
        fig.update_yaxes(tickprefix="$", tickformat=",.0f")
        self._l(fig, w["fecha"], w["trm"], t("trm_linea", L), C1, fmt=",.0f", suf="", cambio=("pct", "a"))
        fig.update_xaxes(range=rango_inicial(w["fecha"].max()))
        return fig, {"franja": franja(L, [(t("trm_linea", L), trm["fecha"], trm["trm"], "pct", ("a", "m"), "d", 0, "$")])}

    def bolsa(self):
        L, m = self.lang, self.d.mercado
        w = semanal(m, ["colcap_puntos"])
        fig = base(L, suffix="")
        fig.update_yaxes(tickformat=",.0f")
        self._l(fig, w["fecha"], w["colcap_puntos"], t("colcap_linea", L), C1, fmt=",.0f", suf=" pts", cambio=("pct", "a"))
        fig.update_xaxes(range=rango_inicial(w["fecha"].max()))
        mm = m.dropna(subset=["colcap_puntos"])
        return fig, {"franja": franja(L, [(t("colcap_linea", L), mm["fecha"], mm["colcap_puntos"], "pct", ("a", "m"), "d", 0, " pts")])}

    def barras(self, serie, freq, color=C1, horizonte=True):
        L, df = self.lang, self.d.extra[serie]
        if df.empty:
            return None, {}
        fig = base(L, height=280)
        x = qend(df["fecha"]) if freq == "q" else df["fecha"] + pd.offsets.YearEnd(0)
        y = [round(float(v), 2) for v in df[serie]]
        ch = serie_cambio(x, y, "pp", "a")
        et = t("vs_ano", L)
        fig.add_trace(go.Bar(x=list(x), y=y, marker=dict(color=color), showlegend=False,
                             customdata=[[fecha(f, freq, L), f"{txt_cambio(v, 'pp', L)} {et}" if pd.notna(v) else ""]
                                         for f, v in zip(df["fecha"], ch)],
                             hovertemplate=f"%{{customdata[0]}}: %{{y:.1f}}%  <span style='color:{MUTED}'>%{{customdata[1]}}</span><extra></extra>"))
        fig.update_layout(hovermode="closest", bargap=0.3)
        fig.add_hline(y=0, line=dict(color=INK2, width=1))
        if horizonte:
            fig.update_xaxes(range=rango_inicial(x.max()))
        return fig, {"franja": franja(L, [(t("g_" + ("cc" if freq == "q" else "deuda") + "_corto", L), x, y, "pp", "a", freq, 1, "%")])}

    # --- detalle tecnico
    def brecha(self):
        L, c = self.lang, self.d.ciclo.dropna(subset=["brecha_hp_tiempo_real"])
        x = qend(c["fecha"])
        fig = base(L)
        fig.add_trace(go.Scatter(x=list(x), y=[round(float(v), 3) for v in c["brecha_max"]], line=dict(width=0),
                                 hoverinfo="skip", showlegend=False))
        fig.add_trace(go.Scatter(x=list(x), y=[round(float(v), 3) for v in c["brecha_min"]], fill="tonexty",
                                 fillcolor="rgba(42,120,214,0.15)", line=dict(width=0), name=t("rango_metodos", L),
                                 hoverinfo="skip"))
        self._l(fig, x, c["brecha_hp_tiempo_real"], t("brecha_principal", L), C1, width=2.4, fmt="+.1f", cambio=("pp", "t"))
        fig.add_hline(y=0, line=dict(color=INK2, width=1))
        fig.update_yaxes(range=[-4, 5])
        fig.add_annotation(xref="paper", yref="paper", x=0.99, y=0.02, xanchor="right", yanchor="bottom",
                           showarrow=False, text=t("covid_escala", L), font=dict(size=11, color=MUTED))
        fig.update_xaxes(range=rango_inicial(x.max()))
        return fig, {"yfijo": True, "franja": franja(L, [(t("brecha_principal", L), x, c["brecha_hp_tiempo_real"], "pp", "t", "q", 1, "%")])}

    def reloj(self):
        L = self.lang
        c = self.d.ciclo.dropna(subset=["brecha_hp_tiempo_real", "delta_brecha"]).tail(12)
        fig = base(L, suffix="", fecha_x=False)
        lx = max(2.0, float(c["brecha_hp_tiempo_real"].abs().max()) * 1.25)
        ly = max(1.5, float(c["delta_brecha"].abs().max()) * 1.25)
        for k, (sx, sy) in {"expansion": (1, 1), "desaceleracion": (1, -1), "contraccion": (-1, -1),
                            "recuperacion": (-1, 1)}.items():
            fig.add_annotation(x=sx * lx * 0.96, y=sy * ly * 0.94, showarrow=False,
                               xanchor="right" if sx > 0 else "left", yanchor="top" if sy > 0 else "bottom",
                               text=f"<b>{am.FASES[k][0 if L == 'es' else 1]}</b>", font=dict(size=12, color=am.FASES[k][2]))
        fig.add_hline(y=0, line=dict(color=RULE, width=1))
        fig.add_vline(x=0, line=dict(color=RULE, width=1))
        et = [fecha(f, "q", L) for f in c["fecha"]]
        fig.add_trace(go.Scatter(x=c["brecha_hp_tiempo_real"], y=c["delta_brecha"], mode="lines",
                                 line=dict(color=GRAY, width=1), hoverinfo="skip", showlegend=False))
        fig.add_trace(go.Scatter(x=c["brecha_hp_tiempo_real"], y=c["delta_brecha"], mode="markers", showlegend=False,
                                 marker=dict(size=[8] * (len(c) - 1) + [16], color=[am.FASES[f][2] for f in c["fase"]],
                                             line=dict(color="#fff", width=2)),
                                 text=et, hovertemplate="%{text}<br>" + t("brecha_eje", L) + ": %{x:+.1f}%<br>"
                                 + t("direccion_eje", L) + ": %{y:+.1f} pp<extra></extra>"))
        fig.add_annotation(x=c["brecha_hp_tiempo_real"].iloc[-1], y=c["delta_brecha"].iloc[-1], text=et[-1],
                           ax=30, ay=-24, arrowhead=0, font=dict(size=12, color=INK))
        fig.update_xaxes(range=[-lx, lx], showline=False, ticksuffix="%", title=dict(text=t("brecha_eje", L), font=dict(size=12)))
        fig.update_yaxes(range=[-ly, ly], ticksuffix=" pp", title=dict(text=t("direccion_eje", L), font=dict(size=12)))
        return fig, {"notime": True}

    def tasa_real(self):
        L, d = self.lang, self.d
        if "tpm_real_exante" not in d.tasas:
            return None, {}
        w = semanal(d.tasas, ["tpm_real_exante"])
        lo, hi = mt.NEUTRAL_REAL
        fig = base(L)
        fig.add_hrect(y0=lo, y1=hi, fillcolor="rgba(82,81,78,0.13)", line_width=0, layer="below")
        fig.add_annotation(xref="paper", x=0.01, y=hi, yanchor="bottom", xanchor="left", showarrow=False,
                           text=t("neutral_label", L), font=dict(size=11, color=INK2))
        self._l(fig, w["fecha"], w["tpm_real_exante"], t("tasa_real", L), C1, fmt=".1f", cambio=("pp", "a"))
        fig.add_hline(y=0, line=dict(color=INK2, width=1))
        fig.update_xaxes(range=rango_inicial(w["fecha"].max()))
        return fig, {"franja": franja(L, [(t("tasa_real", L), w["fecha"], w["tpm_real_exante"], "pp", "a", "d", 1, "%")])}

    def anclaje(self):
        L, w = self.lang, semanal(self.d.tasas, ["bei_5y5y"])
        fig = base(L)
        meta_banda(fig, L)
        self._l(fig, w["fecha"], w["bei_5y5y"], t("espera_largo", L), C7, cambio=("pp", "a"))
        fig.update_xaxes(range=rango_inicial(w["fecha"].max()))
        return fig, {"franja": franja(L, [(t("espera_largo", L), w["fecha"], w["bei_5y5y"], "pp", "a", "d", 1, "%")])}

    def itcr(self):
        L, it = self.lang, self.d.extra["itcr_ipc"]
        if it.empty:
            return None, {}
        fig = base(L, suffix="")
        x = it["fecha"] + pd.offsets.MonthEnd(0)
        self._l(fig, x, it["itcr_ipc"], t("itcr_linea", L), C1, fmt=".1f", suf="", cambio=("pct", "a"))
        fig.add_hline(y=100, line=dict(color=INK2, width=1))
        fig.update_xaxes(range=rango_inicial(it["fecha"].max()))
        return fig, {"franja": franja(L, [(t("itcr_linea", L), x, it["itcr_ipc"], "pct", "a", "m", 1, "")])}


# ------------------------------------------------------------------ curva TES interactiva
TES_COLS = ["tes_pesos_1y", "tes_pesos_5y", "tes_pesos_10y", "tes_uvr_1y", "tes_uvr_5y", "tes_uvr_10y"]


def datos_curva(d: mt.Datos) -> dict:
    """Curva cero cupon diaria (BanRep) en formato compacto para el explorador del navegador."""
    tt = d.tasas[["fecha", *TES_COLS]].dropna(subset=["tes_pesos_1y", "tes_pesos_5y", "tes_pesos_10y"])
    tt = tt.sort_values("fecha").drop_duplicates("fecha", keep="last")
    out = {"f": tt["fecha"].dt.strftime("%Y-%m-%d").tolist()}
    for c in TES_COLS:
        out[c] = [None if pd.isna(v) else round(float(v), 3) for v in tt[c]]
    return out


def explorador_curva(lang):
    """HTML del explorador: el JS (app.js) lo alimenta con assets/curva_tes.json."""
    L = lang
    return f"""<div class="curve-app" id="curva-app" data-lang="{L}">
  <div class="curve-ctrl">
    <div class="seg" role="group" aria-label="{t('tes_tipo', L)}">
      <button data-tipo="pesos" class="on">{t('tes_pesos', L)}</button><button data-tipo="uvr">{t('tes_uvr', L)}</button>
    </div>
    <label class="curve-date">{t('tes_fecha', L)} <b id="curva-fecha">—</b></label>
    <input type="range" id="curva-slider" min="0" max="1" value="1" step="1" aria-label="{t('tes_fecha', L)}">
    <button class="linkbtn" id="curva-hoy">{t('tes_volver', L)}</button>
  </div>
  <div class="curve-years"><span>{t('tes_comparar', L)}</span><div id="curva-anos"></div></div>
  <div class="stats" id="curva-stats"></div>
  <div class="curve-grid">
    <figure class="chart"><figcaption>{t('tes_g_curva', L)}</figcaption><div class="plot" id="g-curva-tes"></div>
      <p class="how"><span>?</span>{t('tes_h_curva', L)}</p></figure>
    <figure class="chart"><figcaption>{t('tes_g_hist', L)}</figcaption><div class="plot" id="g-curva-hist"></div>
      <p class="how"><span>?</span>{t('tes_h_hist', L)}</p></figure>
  </div>
</div>"""


def fig_html(fig, meta, gid):
    """Contenedor + JSON del grafico; el JS del sitio lo dibuja."""
    if fig is None:
        return None
    data = pio.to_json(fig, validate=False, pretty=False, engine="json")
    attrs = ' data-notime="1"' if meta.get("notime") else ""
    attrs += ' data-yfijo="1"' if meta.get("yfijo") else ""
    return (meta.get("franja", "") + f'<div class="plot" id="{gid}"{attrs}></div>'
            f'<script type="application/json" data-for="{gid}">{data}</script>')


# ------------------------------------------------------------------ piezas HTML
def tarjeta(titulo, valor, detalle, estado, tono, pregunta_id):
    return (f'<a class="card" href="#{pregunta_id}"><div class="card-top"><span class="card-title">{esc(titulo)}</span>'
            f'<span class="pill {tono}">{esc(estado)}</span></div>'
            f'<div class="card-value">{esc(valor)}</div><div class="card-detail">{detalle}</div></a>')


def bloque_grafico(titulo, fig_html_str, como_leer, nota=None):
    cuerpo = fig_html_str or '<div class="pending">—</div>'
    extra = f'<p class="note">{nota}</p>' if nota else ""
    return (f'<figure class="chart"><figcaption>{esc(titulo)}</figcaption>{cuerpo}'
            f'<p class="how"><span>?</span>{como_leer}</p>{extra}</figure>')


def seccion(sid, num_, titulo, respuesta, graficos, detalle_html, lang):
    det = (f'<details class="tech"><summary>{t("detalle_tecnico", lang)}</summary><div class="tech-body">{detalle_html}</div></details>'
           if detalle_html else "")
    return (f'<section id="{sid}" class="section"><div class="sec-head"><span class="sec-num">{num_}</span>'
            f'<h2>{esc(titulo)}</h2></div><p class="answer">{respuesta}</p>'
            f'<div class="grid">{"".join(graficos)}</div>{det}</section>')


# ------------------------------------------------------------------ pagina
def pagina(d, s, lang, generado):
    L = lang
    g = Graficos(d, s, L)
    c, i, tt, m = s["ciclo"], s["inflacion"], s["tasas"], s["mercado"]
    ec = mt.estado_crecimiento(c["pib_real_yoy"], c["crecimiento_potencial_hp"])
    ei = mt.estado_inflacion(i["total"])
    post = mt.postura_monetaria(tt.get("tpm_real_exante"))

    tono_c = {"fuerte": "ok", "normal": "ok", "lento": "warn", "contraccion": "bad"}[ec]
    tono_i = {"en_meta": "ok", "baja": "warn", "sobre_meta": "warn", "alta": "bad"}[ei]
    cards = [
        tarjeta(t("c_crec", L), num(c["pib_real_yoy"], 1, L, suf="%"),
                f'{t("crec_detalle", L)} · {fecha(c["fecha"], "q", L)}<br>{t("ritmo_normal_corto", L)}: {num(c["crecimiento_potencial_hp"], 1, L, suf="%")}',
                t(f"ec_{ec}", L), tono_c, "crecimiento"),
        tarjeta(t("c_inf", L), num(i["total"], 2, L, suf="%"),
                f'{t("inf_detalle", L)} · {fecha(i["fecha"], "m", L)}<br>{t("hace_ano", L)}: {num(i["hace_12m"], 1, L, suf="%")} · {t("meta_corta", L)}',
                t(f"ei_{ei}", L), tono_i, "precios"),
    ]
    if tt.get("tpm") is not None:
        tono_p = {"restrictiva": "warn", "neutral": "ok", "expansiva": "warn"}.get(post, "neutral")
        cambio = tt.get("tpm_hace_12m")
        cards.append(tarjeta(t("c_tasa", L), num(tt["tpm"], 2, L, suf="%"),
                             f'{t("tasa_detalle", L)}<br>{t("hace_ano", L)}: {num(cambio, 2, L, suf="%")}',
                             t(f"ep_{post}", L), tono_p, "banco"))
    if s.get("laboral"):
        lb = s["laboral"]
        el = mt.estado_desempleo(lb["td"], lb["td_hace_12m"])
        cards.append(tarjeta(t("c_empleo", L), num(lb["td"], 1, L, suf="%"),
                             f'{t("empleo_detalle", L)} · {fecha(lb["fecha"], "m", L)}<br>{t("hace_ano", L)}: {num(lb["td_hace_12m"], 1, L, suf="%")}',
                             t(f"el_{el}", L), {"mejora": "ok", "estable": "ok", "empeora": "warn"}[el], "crecimiento"))
    if m.get("trm") is not None:
        cards.append(tarjeta(t("c_dolar", L), "$" + num(m["trm"], 0, L),
                             f'{t("dolar_detalle", L)} · {fecha(m["trm_fecha"], "d", L)}<br>{t("en_un_ano", L)}: {num(m["trm_12m"], 1, L, True, "%")}',
                             t("peso_fuerte" if m["trm_12m"] < -5 else ("peso_debil" if m["trm_12m"] > 5 else "peso_estable"), L),
                             "neutral", "mercados"))
    cards.append(tarjeta(t("c_bolsa", L), num(m["colcap"], 0, L) + " pts",
                         f'{t("bolsa_detalle", L)} · {fecha(m["fecha"], "d", L)}<br>{t("en_un_ano", L)}: {num(m["colcap_12m"], 1, L, True, "%")}',
                         t("sube" if m["colcap_12m"] > 5 else ("baja" if m["colcap_12m"] < -5 else "estable"), L),
                         "neutral", "mercados"))

    tecnico = mt.veredicto(s, L)
    fase = am.FASES[c["fase"]][0 if L == "es" else 1]

    # --- secciones
    fc, mc = g.crecimiento()
    fd, md = g.desempleo()
    s1_det = "".join(filter(None, [
        f'<p>{tecnico["actividad"]}</p>',
        bloque_grafico(t("g_brecha", L), fig_html(*g.brecha(), "g-brecha"), t("h_brecha", L)),
        bloque_grafico(t("g_reloj", L), fig_html(*g.reloj(), "g-reloj"), t("h_reloj", L).format(fase=fase)),
        f'<p class="method">{t("m_brecha", L)}</p>']))
    ise_txt = ""
    if s.get("ise"):
        ise_txt = t("resp_ise", L).format(v=num(s["ise"]["yoy"], 1, L), f=fecha(s["ise"]["fecha"], "m", L))
    s1 = seccion("crecimiento", "1", t("q_crec", L),
                 t("resp_crec", L).format(v=num(c["pib_real_yoy"], 1, L), q=fecha(c["fecha"], "q", L),
                                          p=num(c["crecimiento_potencial_hp"], 1, L)) + " " + ise_txt,
                 [bloque_grafico(t("g_crec", L), fig_html(fc, mc, "g-crec"), t("h_crec", L)),
                  bloque_grafico(t("g_desempleo", L), fig_html(fd, md, "g-desempleo"), t("h_desempleo", L))],
                 s1_det, L)

    fi, mi = g.inflacion()
    fe, me = g.expectativas()
    s2_det = "".join(filter(None, [
        f'<p>{tecnico["expectativas"]}</p>',
        bloque_grafico(t("g_anclaje", L), fig_html(*g.anclaje(), "g-anclaje"), t("h_anclaje", L)),
        f'<p class="method">{t("m_expect", L)}</p>']))
    basica = ""
    if i.get("basica") is not None:
        basica = t("resp_basica", L).format(v=num(i["basica"], 1, L))
    s2 = seccion("precios", "2", t("q_precios", L),
                 t("resp_precios", L).format(v=num(i["total"], 2, L), m=fecha(i["fecha"], "m", L),
                                             a=num(i["hace_12m"], 1, L)) + " " + basica + " " +
                 t("resp_espera", L).format(v=num(tt["bei_1y"], 1, L)),
                 [bloque_grafico(t("g_inf", L), fig_html(fi, mi, "g-inf"), t("h_inf", L)),
                  bloque_grafico(t("g_espera", L), fig_html(fe, me, "g-espera"), t("h_espera", L))],
                 s2_det, L)

    fp, mp = g.politica()
    s3_det = "".join(filter(None, [
        f'<p>{tecnico["politica"]}</p>',
        bloque_grafico(t("g_real", L), fig_html(*g.tasa_real(), "g-real"), t("h_real", L)),
        f'<p class="method">{t("m_politica", L)}</p>']))
    resp3 = t("resp_banco_na", L)
    if tt.get("tpm") is not None:
        resp3 = t("resp_banco", L).format(v=num(tt["tpm"], 2, L), r=num(tt.get("tpm_real_exante"), 1, L),
                                          e=t(f"ep2_{post}", L))
    s3 = seccion("banco", "3", t("q_banco", L), resp3,
                 [bloque_grafico(t("g_politica", L), fig_html(fp, mp, "g-politica"), t("h_politica", L))],
                 s3_det, L)

    # --- 4. curva TES (explorador interactivo)
    tc = d.tasas.dropna(subset=["tes_pesos_1y", "tes_pesos_10y"])
    ult = tc.iloc[-1]
    ant = tc[tc["fecha"] <= ult["fecha"] - pd.DateOffset(years=1)].iloc[-1]
    pend = ult["tes_pesos_10y"] - ult["tes_pesos_1y"]
    forma = "tes_normal" if pend > 0.3 else ("tes_invertida" if pend < 0 else "tes_plana")
    resp_curva = t("resp_curva", L).format(
        f=fecha(ult["fecha"], "d", L), c=num(ult["tes_pesos_1y"], 2, L), l=num(ult["tes_pesos_10y"], 2, L),
        p=num(pend, 2, L, True), forma=t(forma, L), d=num(ult["tes_pesos_10y"] - ant["tes_pesos_10y"], 2, L, True))
    s_curva = (f'<section id="curva" class="section"><div class="sec-head"><span class="sec-num">4</span>'
               f'<h2>{t("q_curva", L)}</h2></div><p class="answer">{resp_curva}</p>{explorador_curva(L)}'
               f'<details class="tech"><summary>{t("detalle_tecnico", L)}</summary><div class="tech-body">'
               f'<p class="method">{t("m_curva", L)}</p></div></details></section>')

    fdol, mdol = g.dolar()
    fb, mb = g.bolsa()
    s4_det = "".join(filter(None, [
        bloque_grafico(t("g_itcr", L), fig_html(*g.itcr(), "g-itcr"), t("h_itcr", L)),
        f'<p class="method">{t("m_mercados", L)}</p>']))
    resp4 = t("resp_bolsa", L).format(v=num(m["colcap_12m"], 1, L, True))
    if m.get("trm") is not None:
        resp4 = t("resp_dolar", L).format(v=num(m["trm"], 0, L), c=num(m["trm_12m"], 1, L, True)) + " " + resp4
    s4 = seccion("mercados", "5", t("q_mercados", L), resp4,
                 [bloque_grafico(t("g_dolar", L), fig_html(fdol, mdol, "g-dolar"), t("h_dolar", L)),
                  bloque_grafico(t("g_bolsa", L), fig_html(fb, mb, "g-bolsa"), t("h_bolsa", L))],
                 s4_det, L)

    resp5 = []
    if s.get("cc"):
        resp5.append(t("resp_cc", L).format(v=num(abs(s["cc"]["valor"]), 1, L), f=fecha(s["cc"]["fecha"], "q", L)))
    if s.get("deuda"):
        resp5.append(t("resp_deuda", L).format(v=num(s["deuda"]["valor"], 1, L), f=fecha(s["deuda"]["fecha"], "y", L)))
    s5 = seccion("externo", "6", t("q_externo", L), " ".join(resp5) or t("pendiente", L),
                 [bloque_grafico(t("g_cc", L), fig_html(*g.barras("cuenta_corriente_pct_pib", "q"), "g-cc"), t("h_cc", L)),
                  bloque_grafico(t("g_deuda", L), fig_html(*g.barras("deuda_bruta_gnc_pct_pib", "y", C7, False), "g-deuda"),
                                 t("h_deuda", L))], "", L)

    tabla = tabla_indicadores(d, s, L)
    fuentes = tabla_fuentes(d, L)
    gloss = "".join(f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in GLOSARIO[L])
    descargas = " ".join(f'<a href="datos/{f}" download>{f}</a>' for f in DESCARGAS if (DATA_DIR / f).exists())
    otro = "en/" if L == "es" else "../"
    raiz = "" if L == "es" else "../"
    return f"""<!doctype html>
<html lang="{L}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t("titulo_pagina", L)}</title>
<meta name="description" content="{esc(t('meta_desc', L))}">
<link rel="icon" href="{raiz}assets/favicon.svg">
<link rel="stylesheet" href="{raiz}assets/estilo.css">
<script src="{raiz}assets/plotly.min.js" defer></script>
<script src="{raiz}assets/app.js" defer></script>
</head><body>
<header class="top"><div class="wrap top-in">
  <a class="brand" href="#inicio"><img src="{raiz}assets/logo_usb.png" alt="USB Cali"><span><b>ColombiaMacro</b><small>{t("sub_marca", L)}</small></span></a>
  <nav class="menu"><a href="#crecimiento">{t("nav_crec", L)}</a><a href="#precios">{t("nav_precios", L)}</a><a href="#banco">{t("nav_banco", L)}</a><a href="#curva">{t("nav_curva", L)}</a><a href="#mercados">{t("nav_mercados", L)}</a><a href="#indicadores">{t("nav_todos", L)}</a></nav>
  <a class="lang" href="{otro}">{t("otro_idioma", L)}</a>
</div></header>
<main id="inicio" class="wrap">
<section class="hero">
  <p class="kicker">{t("kicker", L)} · {t("datos_al", L)} {fecha(generado, "d", L)}</p>
  <h1>{t("h1", L)}</h1>
  <p class="summary">{esc(mt.resumen_simple(s, L))}</p>
  <div class="cards">{"".join(cards)}</div>
  <p class="disclaimer">{t("aviso_estados", L)}</p>
</section>
<div class="horizon" role="group" aria-label="{t('horizonte', L)}"><span>{t("horizonte", L)}:</span>
  <button data-years="3">{t("h3", L)}</button><button data-years="5">{t("h5", L)}</button><button data-years="10" class="on">{t("h10", L)}</button><button data-years="0">{t("htodo", L)}</button></div>
{s1}{s2}{s3}{s_curva}{s4}{s5}
<section id="indicadores" class="section"><div class="sec-head"><span class="sec-num">7</span><h2>{t("q_todos", L)}</h2></div>
<p class="answer">{t("resp_todos", L)}</p>{tabla}</section>
<section id="fuentes" class="section"><div class="sec-head"><span class="sec-num">8</span><h2>{t("q_fuentes", L)}</h2></div>
<p class="answer">{t("resp_fuentes", L)}</p>{fuentes}
<p class="downloads"><b>{t("descargar", L)}:</b> {descargas}</p>
<p class="downloads"><b>{t("documentos", L)}:</b> <a href="{REPO_URL}/blob/main/docs/METODOLOGIA.md">{t("metodologia", L)}</a> · <a href="{REPO_URL}/raw/main/docs/Manual_ColombiaMacro.pdf">{t("manual", L)}</a> · <a href="{REPO_URL}">GitHub</a></p>
<details class="tech"><summary>{t("glosario", L)}</summary><dl class="gloss">{gloss}</dl></details>
</section>
</main>
<footer class="wrap foot"><p>{t("aviso", L)}</p><p>DANE · Banco de la República · BVC/MSCI · Ministerio de Hacienda · {t("generado", L)} {fecha(generado, "d", L)}</p></footer>
</body></html>"""


def tabla_indicadores(d, s, L):
    df = mt.tabla_senales(d, s, L)
    head = "".join(f"<th>{t(k, L)}</th>" for k in ("col_ind", "col_ult", "col_fecha", "col_cambio", "col_hist"))
    rows = []
    for _, r in df.iterrows():
        nombre, freq = r["indicador"], r["freq"]
        if r["cambio"] is None or pd.isna(r["cambio"]):
            cambio = "—"
        elif r["relativo"]:
            cambio = num(r["cambio"], 1, L, True, "%")
        else:
            cambio = num(r["cambio"], r["dec"], L, True, " pp" if str(r["unidad"]).startswith("%") else "")
        ventana = t("en_3m", L) if r["ventana"] == 91 else t("en_12m", L)
        nivel = mt.nivel_historico(r["percentil"])
        nivel_txt = t("niv_" + nivel, L) if nivel else "—"
        pct = 0 if pd.isna(r["percentil"]) else r["percentil"]
        rows.append(f"<tr><td>{esc(nombre)}</td><td class='n'>{num(r['valor'], r['dec'], L)} {esc(r['unidad'])}</td>"
                    f"<td class='m'>{fecha(r['fecha'], freq, L)}</td><td class='n'>{cambio} <small>{ventana}</small></td>"
                    f"<td><div class='lvl {nivel or ''}'><i style='left:{pct:.0f}%'></i></div><span class='lvl-t'>{nivel_txt}</span></td></tr>")
    return f"<div class='table-wrap'><table class='tbl'><thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>"


def tabla_fuentes(d, L):
    est = d.estado
    if est is None:
        return ""
    rows = []
    for _, r in est.iterrows():
        f = r["ultima_observacion"]
        if isinstance(f, str) and f:
            freq = {"trimestral": "q", "mensual": "m", "anual": "y"}.get(r["frecuencia"], "d")
            ftxt = fecha(f, freq, L)
        else:
            ftxt = "—"
        rows.append(f"<tr><td>{esc(r['fuente'])}</td><td class='m'>{t('fr_' + str(r['frecuencia']), L)}</td>"
                    f"<td>{ftxt}</td><td><span class='st {r['estado']}'>{t('st_' + r['estado'], L)}</span></td></tr>")
    head = "".join(f"<th>{t(k, L)}</th>" for k in ("col_fuente", "col_frec", "col_ultimo", "col_estado"))
    return f"<div class='table-wrap'><table class='tbl'><thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>"


def construir(salida: Path = SITE_DIR) -> Path:
    d = mt.cargar()
    s = mt.instantanea(d)
    generado = max(filter(None, [s["tasas"]["fecha"], s["mercado"]["fecha"], s["mercado"].get("trm_fecha")]))
    if salida.exists():
        shutil.rmtree(salida)
    (salida / "assets").mkdir(parents=True)
    (salida / "en").mkdir()
    (salida / "datos").mkdir()
    for f in ("estilo.css", "app.js", "favicon.svg"):
        shutil.copy(HERE / f, salida / "assets" / f)
    shutil.copy(DOCS_DIR / "presentacion" / "logo_usb.png", salida / "assets" / "logo_usb.png")
    (salida / "assets" / "plotly.min.js").write_text(get_plotlyjs(), encoding="utf-8")
    for f in DESCARGAS:
        if (DATA_DIR / f).exists():
            shutil.copy(DATA_DIR / f, salida / "datos" / f)
    (salida / "assets" / "curva_tes.json").write_text(json.dumps(datos_curva(d), separators=(",", ":")), encoding="utf-8")
    (salida / "index.html").write_text(pagina(d, s, "es", generado), encoding="utf-8")
    (salida / "en" / "index.html").write_text(pagina(d, s, "en", generado), encoding="utf-8")
    (salida / ".nojekyll").write_text("")
    resumen = {"generado": str(generado.date()), "fase": s["ciclo"]["fase"],
               "resumen_es": mt.resumen_simple(s, "es"), "resumen_en": mt.resumen_simple(s, "en")}
    (salida / "resumen.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
    return salida


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Construye el sitio estatico")
    ap.add_argument("--salida", type=Path, default=SITE_DIR)
    out = construir(ap.parse_args().salida)
    print(f"Sitio listo en {out}")
