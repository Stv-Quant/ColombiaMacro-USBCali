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
import re
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
DESCARGAS = ["pib_colombia.csv", "pib_sectores.csv", "informalidad.csv", "informalidad_ramas.csv", "informalidad_ciudades.csv", "inflacion_clean.csv", "tasas_interes_clean.csv", "colcap_oficial.csv",
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
CHG_UP, CHG_DN = "rgba(42,120,214,0.62)", "rgba(235,104,52,0.68)"


def base(lang, height=330, suffix="%", fecha_x=True, delta=False):
    """Figura base. delta=True agrega abajo un panel con el cambio de la serie principal
    (mismo eje de fechas: el recuadro flotante muestra ambos paneles a la vez)."""
    fig = go.Figure()
    if delta:
        height += 110
        fig.update_layout(yaxis=dict(domain=[0.35, 1]), yaxis2=dict(domain=[0, 0.24], anchor="x"),
                          xaxis=dict(anchor="y2"), hoversubplots="axis")
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


def panel_cambio(fig, x, y, modo, periodo, lang, titulo):
    """Barras del cambio (vs. hace 1 ano, trimestre o mes) en el panel inferior."""
    ch = serie_cambio(x, y, modo, periodo)
    vals = [None if pd.isna(v) else round(float(v), 3) for v in ch]
    suf = " pp" if modo == "pp" else "%"
    et = etiqueta_periodo(periodo, lang)
    fig.add_trace(go.Bar(x=list(ch.index), y=vals, yaxis="y2", showlegend=False, name=f"Δ {titulo}",
                         marker=dict(color=[CHG_UP if (v or 0) >= 0 else CHG_DN for v in vals], line=dict(width=0)),
                         customdata=[num(v, 1, lang, True, suf) if v is not None else "" for v in vals],
                         hovertemplate=f"%{{customdata}} {et}"))
    fig.add_shape(type="line", xref="x domain", x0=0, x1=1, yref="y2", y0=0, y1=0,
                  line=dict(color=INK2, width=0.8))
    fig.update_layout(yaxis2=dict(ticksuffix=suf, nticks=4, gridcolor=GRID, zeroline=False, fixedrange=True,
                                  tickfont=dict(size=11, color=MUTED), automargin=True), bargap=0.12)
    fig.add_annotation(xref="paper", x=0, yref="y2 domain", y=1.03, yanchor="bottom", xanchor="left", showarrow=False,
                       text=f"<b>{t('panel_cambio', lang)}</b> · {titulo} ({et})", font=dict(size=11.5, color=MUTED))


def franja(lang, items):
    """Franja sobre el grafico: ultimo dato de cada serie y su cambio.
    items: (nombre, x, y, modo, periodo, freq, dec, suf)"""
    partes = []
    for nombre, x, y, modo, periodo, freq, dec, suf in items:
        s = pd.Series(list(pd.to_numeric(pd.Series(list(y)), errors="coerce")), index=pd.to_datetime(pd.Series(list(x))))
        s = s.dropna()
        if s.empty:
            continue
        if suf.startswith("$"):
            valor = "$" + num(s.iloc[-1], dec, lang) + suf[1:]
        else:
            valor = num(s.iloc[-1], dec, lang) + suf
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
        fig = base(L, delta=True)
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
        panel_cambio(fig, xq, yq, "pp", "t", L, t("pib_trim", L))
        fig.update_xaxes(range=rango_inicial(xq.max()))
        return fig, {"franja": franja(L, items)}

    def desempleo(self):
        L, lb = self.lang, self.d.laboral
        if lb is None:
            return None, {}
        fig = base(L, delta=True)
        self._l(fig, lb["fecha"], lb["td_sa"], t("td_mensual", L), GRAY, width=1.2, cambio=("pp", "a"))
        self._l(fig, lb["fecha"], lb["td_sa_3m"], t("td_3m", L), C1, width=2.4, cambio=("pp", "a"))
        panel_cambio(fig, lb["fecha"], lb["td_sa_3m"], "pp", "a", L, t("td_3m", L))
        fig.update_xaxes(range=rango_inicial(lb["fecha"].max()))
        return fig, {"franja": franja(L, [(t("td_3m", L), lb["fecha"], lb["td_sa_3m"], "pp", "a", "m", 1, "%"),
                                          (t("td_mensual", L), lb["fecha"], lb["td_sa"], "pp", "a", "m", 1, "%")])}

    # --- 2. precios
    def inflacion(self):
        L, inf = self.lang, self.d.inflacion
        fig = base(L, delta=True)
        meta_banda(fig, L)
        x = inf["fecha"] + pd.offsets.MonthEnd(0)
        panel_cambio(fig, x, inf["inflacion_anual"], "pp", "a", L, t("inf_total", L))
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
        fig = base(L, delta=True)
        meta_banda(fig, L)
        panel_cambio(fig, w["fecha"], w["bei_1y"], "pp", "a", L, t("espera_1a", L))
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
        fig = base(L, delta=True)
        panel_cambio(fig, w["fecha"], w["tpm"], "pp", "a", L, t("tpm_linea", L))
        self._l(fig, w["fecha"], w["tpm"], t("tpm_linea", L), C1, width=2.6, fmt=".2f", shape="hv", cambio=("pp", "a"))
        xi = d.inflacion["fecha"] + pd.offsets.MonthEnd(0)
        self._l(fig, xi, d.inflacion["inflacion_anual"], t("inf_total", L), C2, fmt=".2f", cambio=("pp", "a"))
        fig.add_hline(y=3, line=dict(color=C3, width=1, dash="dot"))
        an = (self.s.get("tasas") or {}).get("tpm_anunciada")
        if an:
            fig.add_trace(go.Scatter(x=[an["vigente"]], y=[an["tasa"]], mode="markers+text", name=t("an_marca", L),
                                     marker=dict(symbol="star", size=14, color=C1, line=dict(color="#fff", width=1)),
                                     text=[num(an["tasa"], 2, L, suf="%")], textposition="top left",
                                     hovertemplate=t("an_hover", L).format(a=fecha(an["anuncio"], "d", L)) + ": %{y:.2f}%<extra></extra>"))
        fig.update_xaxes(range=rango_inicial(max(w["fecha"].max(), an["vigente"]) if an else w["fecha"].max()))
        tp = d.extra["tpm"]
        return fig, {"franja": franja(L, [(t("tpm_linea", L), tp["fecha"], tp["tpm"], "pp", "a", "d", 2, "%"),
                                          (t("inf_total", L), xi, d.inflacion["inflacion_anual"], "pp", "a", "m", 2, "%")])}

    # --- 4. mercados
    def dolar(self):
        L, trm = self.lang, self.d.extra["trm"]
        if trm.empty:
            return None, {}
        w = semanal(trm, ["trm"])
        fig = base(L, suffix="", delta=True)
        panel_cambio(fig, w["fecha"], w["trm"], "pct", "a", L, t("trm_linea", L))
        fig.update_yaxes(tickprefix="$", tickformat=",.0f")
        self._l(fig, w["fecha"], w["trm"], t("trm_linea", L), C1, fmt=",.0f", suf="", cambio=("pct", "a"))
        fig.update_xaxes(range=rango_inicial(w["fecha"].max()))
        return fig, {"franja": franja(L, [(t("trm_linea", L), trm["fecha"], trm["trm"], "pct", ("a", "m"), "d", 0, "$")])}

    def bolsa(self):
        L, m = self.lang, self.d.mercado
        w = semanal(m, ["colcap_puntos"])
        fig = base(L, suffix="", delta=True)
        panel_cambio(fig, w["fecha"], w["colcap_puntos"], "pct", "a", L, t("colcap_linea", L))
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

    # --- produccion y capacidad (frontera de produccion)
    def capacidad(self):
        """PIB real desestacionalizado frente a su capacidad (PIB potencial): la 'frontera' de lo que la
        economia puede producir sin presionar precios. Area verde = por encima; naranja = por debajo."""
        L, d = self.lang, self.d
        p = d.pib.set_index("fecha")["pib_real_ajustado_miles_millones_ref2015"].astype(float) / 1000
        c = d.ciclo.set_index("fecha")["brecha_hp_tiempo_real"]
        df = pd.DataFrame({"y": p, "gap": c}).dropna()
        df["pot"] = df["y"] * np.exp(-df["gap"] / 100)
        x = list(qend(pd.Series(df.index)))
        y, pot = [round(v, 2) for v in df["y"]], [round(v, 2) for v in df["pot"]]
        arriba = [max(a, b) for a, b in zip(y, pot)]
        abajo = [min(a, b) for a, b in zip(y, pot)]
        fig = base(L, suffix="", delta=True)
        for borde, relleno, color in ((arriba, "rgba(26,127,75,0.22)", None), (abajo, "rgba(235,104,52,0.25)", None)):
            fig.add_trace(go.Scatter(x=x, y=pot, mode="lines", line=dict(width=0), hoverinfo="skip", showlegend=False))
            fig.add_trace(go.Scatter(x=x, y=borde, mode="lines", line=dict(width=0), fill="tonexty", fillcolor=relleno,
                                     hoverinfo="skip", showlegend=False))
        fig.add_trace(go.Scatter(x=x, y=pot, mode="lines", name=t("cap_pot", L), line=dict(color=INK2, width=2, dash="dash"),
                                 hovertemplate="$%{y:,.0f} bill.<extra>" + t("cap_pot", L) + "</extra>"))
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name=t("cap_real", L), line=dict(color=C1, width=2.6),
                                 customdata=[num(g, 1, L, True, "%") for g in df["gap"]],
                                 hovertemplate="$%{y:,.0f} bill. · " + t("cap_dif", L) + " %{customdata}<extra>" + t("cap_real", L) + "</extra>"))
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers", marker=dict(size=11, color="rgba(26,127,75,0.45)", symbol="square"),
                                 name=t("cap_sobre", L)))
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers", marker=dict(size=11, color="rgba(235,104,52,0.5)", symbol="square"),
                                 name=t("cap_holgura", L)))
        gaps = [round(float(v), 2) for v in df["gap"]]
        fig.add_trace(go.Bar(x=x, y=gaps, yaxis="y2", showlegend=False, name=t("cap_dif", L),
                             marker=dict(color=["rgba(26,127,75,0.7)" if v >= 0 else "rgba(235,104,52,0.75)" for v in gaps], line=dict(width=0)),
                             customdata=[num(v, 1, L, True, "%") for v in gaps], hovertemplate="%{customdata}"))
        fig.add_shape(type="line", xref="x domain", x0=0, x1=1, yref="y2", y0=0, y1=0, line=dict(color=INK2, width=0.8))
        fig.update_layout(yaxis2=dict(ticksuffix="%", nticks=4, gridcolor=GRID, zeroline=False, fixedrange=True,
                                      tickfont=dict(size=11, color=MUTED), automargin=True), bargap=0.15)
        fig.add_annotation(xref="paper", x=0, yref="y2 domain", y=1.03, yanchor="bottom", xanchor="left", showarrow=False,
                           text=f"<b>{t('cap_panel', L)}</b>", font=dict(size=11.5, color=MUTED))
        fig.update_layout(yaxis=dict(tickprefix="$", tickformat=",.0f", ticksuffix="",
                                     title=dict(text=t("cap_eje", L), font=dict(size=11.5))))
        fig.update_xaxes(range=rango_inicial(max(x)))
        u = df.iloc[-1]
        return fig, {"franja": franja(L, [(t("cap_dif", L), x, df["gap"], "pp", "a", "q", 1, "%")])}, u

    def crecimiento_anual(self):
        """Crecimiento real por ano: PIB real (datos originales) de cada ano frente al anterior, mas los ultimos 12 meses."""
        L, d = self.lang, self.d
        p = d.pib.set_index("fecha").sort_index()
        real4 = p["pib_real_miles_millones_ref2015"].astype(float).rolling(4).sum()
        r12 = (real4 / real4.shift(4) - 1) * 100            # crecimiento real de los ultimos 12 meses, trimestral
        r12 = r12.dropna()
        anual = r12[r12.index.month == 10]                    # T4: ano calendario completo
        ult = r12.index[-1]
        fig = base(L, suffix="%", height=380)
        xa = [pd.Timestamp(f.year, 7, 1) for f in anual.index]      # barra centrada en el ano
        prev = anual.shift(1)
        fig.add_trace(go.Bar(
            x=xa, y=[round(float(v), 2) for v in anual], name=t("pa_anual", L),
            marker=dict(color=[C1 if v >= 0 else C2 for v in anual], line=dict(width=0)),
            text=[num(v, 1, L) + "%" for v in anual], textposition="outside", cliponaxis=False,
            textfont=dict(size=10.5, color=INK2),
            customdata=[[str(f.year), txt_cambio(v - pv, "pp", L) + " " + t("pa_vs", L) if pd.notna(pv) else ""]
                        for f, v, pv in zip(anual.index, anual, prev)],
            hovertemplate="<b>%{customdata[0]}</b>: %{y:.1f}%  <span style='color:" + MUTED + "'>%{customdata[1]}</span><extra></extra>"))
        if ult.month != 10:  # ano en curso: ultimos 12 meses
            v12 = float(r12.iloc[-1])
            q12 = fecha(ult, "q", L)
            fig.add_trace(go.Bar(
                x=[qend(pd.Series([ult])).iloc[0]], y=[round(v12, 2)], name=t("pa_12m", L).format(q=q12),
                marker=dict(color="rgba(42,120,214,0.35)", line=dict(color=C1, width=1.5)),
                text=[num(v12, 1, L) + "%"], textposition="outside", cliponaxis=False, textfont=dict(size=10.5, color=INK2),
                hovertemplate=t("pa_12m", L).format(q=q12) + ": %{y:.1f}%<extra></extra>"))
        prom = float(anual[(anual.index.year >= 2010) & (anual.index.year <= 2019)].mean())
        pot = d.ciclo.set_index("fecha")["crecimiento_potencial_hp"].dropna()
        if not pot.empty:
            pa = pot.groupby(pot.index.year).mean()
            pa = pa[pa.index.isin([f.year for f in anual.index])]
            self._l(fig, [pd.Timestamp(y, 7, 1) for y in pa.index], pa.values, t("ritmo_normal", L), C3, width=1.8, dash="dot")
        # margen invisible para que la primera y la ultima barra no queden cortadas con cualquier horizonte
        x_ini, x_fin = xa[0] - pd.DateOffset(months=7), qend(pd.Series([ult])).iloc[0] + pd.DateOffset(months=7)
        fig.add_trace(go.Scatter(x=[x_ini, x_fin], y=[None, None], mode="markers", marker=dict(opacity=0),
                                 showlegend=False, hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=[x_ini, x_fin], y=[prom, prom], mode="lines", name=t("pa_prom", L).format(v=num(prom, 1, L)),
                                 line=dict(color=INK2, width=1.2, dash="dash"), hoverinfo="skip"))
        fig.add_hline(y=0, line=dict(color=INK2, width=1))
        fig.update_layout(bargap=0.3, uniformtext=dict(minsize=10, mode="show"),
                          yaxis=dict(title=dict(text=t("pa_eje", L), font=dict(size=11.5))))
        fig.update_xaxes(range=rango_inicial(x_fin))
        xr = list(qend(pd.Series(r12.index)))
        items = [(t("pa_franja", L), xr, list(r12.values), "pp", "a", "q", 1, "%")]
        u = {"r12": float(r12.iloc[-1]), "q": ult, "ultimo_ano": int(anual.index[-1].year), "v_ano": float(anual.iloc[-1]),
             "prom": prom}
        return fig, {"franja": franja(L, items)}, u

    # --- sectores (PIB por actividad)
    def sectores_barras(self):
        L, sc = self.lang, self.d.sectores
        if sc is None or sc.empty:
            return None, {}
        f = sc["fecha"].max()
        u = sc[sc["fecha"] == f].set_index("codigo")
        a = sc[sc["fecha"] == f - pd.DateOffset(years=1)].set_index("codigo")["yoy"]
        u = u.assign(hace=a).sort_values("yoy")
        fig = base(L, height=440, fecha_x=False)
        fig.add_trace(go.Bar(y=list(u["sector"]), x=[round(v, 2) for v in u["yoy"]], orientation="h", showlegend=False,
                             marker=dict(color=[C1 if v >= 0 else C2 for v in u["yoy"]], line=dict(width=0)),
                             customdata=[[num(p_, 1, L, suf="%"), num(c_, 2, L, True, " pp"), num(h, 1, L, suf="%")]
                                         for p_, c_, h in zip(u["peso"], u["contribucion"], u["hace"])],
                             text=[num(v, 1, L, True, "%") for v in u["yoy"]], textposition="outside", cliponaxis=False,
                             hovertemplate="<b>%{y}</b><br>" + t("sec_crec", L) + ": %{x:.1f}%<br>" + t("sec_hace", L)
                             + ": %{customdata[2]}<br>" + t("sec_peso", L) + ": %{customdata[0]}<br>" + t("sec_aporte", L)
                             + ": %{customdata[1]}<extra></extra>"))
        fig.add_trace(go.Scatter(y=list(u["sector"]), x=[round(v, 2) for v in u["hace"]], mode="markers",
                                 name=t("sec_raya", L).format(q=fecha(f - pd.DateOffset(years=1), "q", L)),
                                 marker=dict(symbol="line-ns", size=16, line=dict(width=2.5, color=INK)), hoverinfo="skip"))
        fig.add_vline(x=0, line=dict(color=INK2, width=1))
        lo = min(0, float(u[["yoy", "hace"]].min().min())) - 2
        hi = float(u[["yoy", "hace"]].max().max()) + 3
        fig.update_layout(hovermode="closest", bargap=0.28, margin=dict(l=6, r=30, t=6, b=6))
        fig.update_xaxes(ticksuffix="%", showgrid=True, gridcolor=GRID, range=[lo, hi], zeroline=False)
        fig.update_yaxes(ticksuffix="", tickfont=dict(size=12, color=INK2))
        return fig, {"notime": True}

    def sectores_mapa(self):
        """Mapa de calor: crecimiento anual de cada sector, trimestre a trimestre."""
        L, sc = self.lang, self.d.sectores
        if sc is None or sc.empty:
            return None, {}
        piv = sc.pivot_table(index="sector", columns="fecha", values="yoy")
        orden = sc[sc["fecha"] == sc["fecha"].max()].sort_values("peso")["sector"]
        piv = piv.reindex(orden)
        x = list(qend(pd.Series(piv.columns)))
        z = piv.values
        fig = base(L, height=440)
        fig.add_trace(go.Heatmap(
            x=x, y=list(piv.index), z=[[None if pd.isna(v) else round(float(v), 2) for v in fila] for fila in z],
            zmid=0, zmin=-12, zmax=12, colorscale=[[0, "#b04a17"], [0.35, "#f3c9b3"], [0.5, "#f7f6f2"], [0.65, "#bfd7f3"], [1, "#1f4f8f"]],
            colorbar=dict(ticksuffix="%", thickness=10, len=0.9, outlinewidth=0, tickfont=dict(size=11, color=MUTED)),
            xgap=1, ygap=1, customdata=[[fecha(f, "q", L) for f in piv.columns]] * len(piv.index),
            hovertemplate="<b>%{y}</b> · %{customdata}<br>%{z:.1f}%<extra></extra>"))
        fig.update_layout(hovermode="closest", showlegend=False, margin=dict(l=6, r=6, t=6, b=6))
        fig.update_yaxes(ticksuffix="", tickfont=dict(size=11.5, color=INK2), gridcolor="rgba(0,0,0,0)")
        fig.update_xaxes(range=rango_inicial(max(x), 5), showline=False)
        return fig, {"noy": True}

    # --- informalidad
    def informalidad(self):
        L, inf = self.lang, self.d.informalidad
        if inf is None or inf.empty:
            return None, {}
        fig = base(L, delta=True)
        x = inf["fecha"] + pd.offsets.MonthEnd(0)
        self._l(fig, x, inf["nacional"], t("inf_nal", L), C1, width=2.6, cambio=("pp", "a"))
        if "ciudades_13" in inf:
            self._l(fig, x, inf["ciudades_13"], t("inf_13", L), C3, width=1.8, cambio=("pp", "a"))
        panel_cambio(fig, x, inf["nacional"], "pp", "a", L, t("inf_nal", L))
        fig.update_xaxes(range=rango_inicial(x.max(), 10))
        return fig, {"franja": franja(L, [(t("inf_nal", L), x, inf["nacional"], "pp", "a", "m", 1, "%"),
                                          (t("inf_13", L), x, inf["ciudades_13"], "pp", "a", "m", 1, "%")])}

    def informalidad_ramas(self):
        L, ir = self.lang, self.d.informalidad_ramas
        if ir is None or ir.empty:
            return None, {}
        f = ir["fecha"].max()
        u = ir[ir["fecha"] == f].set_index("rama")
        a = ir[ir["fecha"] == f - pd.DateOffset(years=1)].set_index("rama")["tasa"]
        u = u.assign(hace=a).sort_values("tasa")
        fig = base(L, height=440, fecha_x=False)
        fig.add_trace(go.Bar(y=list(u.index), x=[round(v, 2) for v in u["tasa"]], orientation="h", showlegend=False,
                             marker=dict(color=C2, line=dict(width=0)),
                             text=[num(v, 0, L, suf="%") for v in u["tasa"]], textposition="outside", cliponaxis=False,
                             customdata=[[num(i_ / 1000, 2, L), num(o_ / 1000, 2, L), num(h, 1, L, suf="%"),
                                          num(v - h, 1, L, True, " pp") if pd.notna(h) else "—"]
                                         for i_, o_, h, v in zip(u["informales"], u["ocupados"], u["hace"], u["tasa"])],
                             hovertemplate="<b>%{y}</b><br>" + t("inf_tasa", L) + ": %{x:.1f}% (%{customdata[3]} "
                             + t("vs_ano", L) + ")<br>" + t("inf_personas", L)
                             + ": %{customdata[0]} / %{customdata[1]} M<extra></extra>"))
        fig.add_trace(go.Scatter(y=list(u.index), x=[round(v, 2) for v in u["hace"]], mode="markers",
                                 name=t("sec_raya", L).format(q=fecha(f - pd.DateOffset(years=1), "m", L)),
                                 marker=dict(symbol="line-ns", size=16, line=dict(width=2.5, color=INK)), hoverinfo="skip"))
        fig.update_layout(hovermode="closest", bargap=0.28, margin=dict(l=6, r=30, t=6, b=6))
        fig.update_xaxes(ticksuffix="%", showgrid=True, gridcolor=GRID, range=[0, 100])
        fig.update_yaxes(ticksuffix="", tickfont=dict(size=12, color=INK2))
        return fig, {"notime": True}

    def informalidad_ciudades(self):
        """Ranking de informalidad por ciudad (23 ciudades y A.M.; las 13 principales resaltadas)."""
        L, ic = self.lang, self.d.informalidad_ciudades
        if ic is None or ic.empty:
            return None, {}
        f = ic["fecha"].max()
        u = ic[ic["fecha"] == f].set_index("ciudad")
        a = ic[ic["fecha"] == f - pd.DateOffset(years=1)].set_index("ciudad")["tasa"]
        u = u.assign(hace=a).sort_values("tasa")
        fig = base(L, height=560, fecha_x=False)
        fig.add_trace(go.Bar(y=list(u.index), x=[round(v, 2) for v in u["tasa"]], orientation="h", showlegend=False,
                             marker=dict(color=[C1 if g_ == "13" else "#c9c7c0" for g_ in u["grupo"]], line=dict(width=0)),
                             text=[num(v, 0, L, suf="%") for v in u["tasa"]], textposition="outside", cliponaxis=False,
                             customdata=[[num(h, 1, L, suf="%"), num(v - h, 1, L, True, " pp") if pd.notna(h) else "—",
                                          t("inf_13c", L) if g_ == "13" else t("inf_23c", L)]
                                         for h, v, g_ in zip(u["hace"], u["tasa"], u["grupo"])],
                             hovertemplate="<b>%{y}</b> · %{customdata[2]}<br>" + t("inf_tasa", L) + ": %{x:.1f}%<br>"
                             + t("hace_ano", L) + ": %{customdata[0]} (%{customdata[1]})<extra></extra>"))
        fig.add_trace(go.Scatter(y=list(u.index), x=[round(v, 2) for v in u["hace"]], mode="markers",
                                 name=t("sec_raya", L).format(q=fecha(f - pd.DateOffset(years=1), "m", L)),
                                 marker=dict(symbol="line-ns", size=12, line=dict(width=2.2, color=INK)), hoverinfo="skip"))
        fig.add_trace(go.Bar(y=[None], x=[None], orientation="h", name=t("inf_13c", L), marker=dict(color=C1)))
        fig.add_trace(go.Bar(y=[None], x=[None], orientation="h", name=t("inf_23c", L), marker=dict(color="#c9c7c0")))
        fig.update_layout(hovermode="closest", bargap=0.22, margin=dict(l=6, r=30, t=6, b=6))
        fig.update_xaxes(ticksuffix="%", showgrid=True, gridcolor=GRID, range=[0, 80])
        fig.update_yaxes(ticksuffix="", tickfont=dict(size=11.5, color=INK2))
        return fig, {"notime": True}

    # --- 5b. bolsa por dentro
    def bolsa_indices(self, b):
        """COLCAP oficial vs equiponderado vs 7 Magnificas, base 100 (el navegador re-basa al horizonte)."""
        L = self.lang
        ix = b["indices"]
        fig = base(L, suffix="", delta=True)
        series = [("colcap", t("idx_colcap", L), C1, 2.6), ("equiponderado", t("idx_equi", L), C3, 2.0),
                  ("magnificas", t("idx_mag", L), C2, 2.0)]
        for col, nombre, color, ancho in series:
            self._l(fig, ix["fecha"], ix[col], nombre, color, width=ancho, fmt=".1f", suf="", cambio=("pct", "a"))
        for col, nombre, color, _ in series:
            ch = serie_cambio(ix["fecha"], ix[col], "pct", "a")
            fig.add_trace(go.Scatter(x=list(ch.index), y=[None if pd.isna(v) else round(float(v), 2) for v in ch],
                                     yaxis="y2", mode="lines", line=dict(color=color, width=1.4), showlegend=False,
                                     name=f"Δ {nombre}", customdata=[num(v, 1, L, True, "%") if pd.notna(v) else "" for v in ch],
                                     hovertemplate="%{customdata} " + t("vs_ano", L)))
        fig.add_shape(type="line", xref="x domain", x0=0, x1=1, yref="y2", y0=0, y1=0, line=dict(color=INK2, width=0.8))
        fig.update_layout(yaxis2=dict(ticksuffix="%", nticks=4, gridcolor=GRID, zeroline=False, fixedrange=True,
                                      tickfont=dict(size=11, color=MUTED), automargin=True))
        fig.add_annotation(xref="paper", x=0, yref="y2 domain", y=1.03, yanchor="bottom", xanchor="left", showarrow=False,
                           text=f"<b>{t('panel_cambio', L)}</b> · {t('rent_12m', L)}", font=dict(size=11.5, color=MUTED))
        fig.update_xaxes(range=rango_inicial(ix["fecha"].max()))
        return fig, {"rebase": True, "franja": franja_indices(L, ix, series)}

    def pesos(self, b):
        """Peso de cada accion en el COLCAP; las 7 Magnificas resaltadas."""
        L = self.lang
        c = b["canasta"].head(15).iloc[::-1]
        top = set(mt.magnificas(b["canasta"])["emisor"])
        fig = base(L, height=420, suffix="%", fecha_x=False)
        fig.add_trace(go.Bar(y=[f"{r.ticker}" for r in c.itertuples()], x=list(c["peso"]), orientation="h",
                             marker=dict(color=[C2 if e in top else "#c9c7c0" for e in c["emisor"]], line=dict(width=0)),
                             customdata=[[mt.nombre_corto(r.emisor), r.sector] for r in c.itertuples()], showlegend=False,
                             text=[num(v, 1, L, suf="%") for v in c["peso"]], textposition="outside", cliponaxis=False,
                             hovertemplate="<b>%{y}</b> · %{customdata[0]}<br>%{customdata[1]}<br>%{x:.2f}%<extra></extra>"))
        fig.update_layout(hovermode="closest", bargap=0.25, margin=dict(l=6, r=40, t=6, b=6))
        fig.update_xaxes(ticksuffix="%", showgrid=True, gridcolor=GRID, range=[0, float(c["peso"].max()) * 1.18])
        fig.update_yaxes(ticksuffix="", tickfont=dict(size=11.5, color=INK2))
        return fig, {"notime": True}

    # --- detalle tecnico
    def brecha(self):
        L, c = self.lang, self.d.ciclo.dropna(subset=["brecha_hp_tiempo_real"])
        x = qend(c["fecha"])
        fig = base(L, delta=True)
        fig.add_trace(go.Scatter(x=list(x), y=[round(float(v), 3) for v in c["brecha_max"]], line=dict(width=0),
                                 hoverinfo="skip", showlegend=False))
        fig.add_trace(go.Scatter(x=list(x), y=[round(float(v), 3) for v in c["brecha_min"]], fill="tonexty",
                                 fillcolor="rgba(42,120,214,0.15)", line=dict(width=0), name=t("rango_metodos", L),
                                 hoverinfo="skip"))
        self._l(fig, x, c["brecha_hp_tiempo_real"], t("brecha_principal", L), C1, width=2.4, fmt="+.1f", cambio=("pp", "t"))
        fig.add_hline(y=0, line=dict(color=INK2, width=1))
        panel_cambio(fig, x, c["brecha_hp_tiempo_real"], "pp", "t", L, t("brecha_principal", L))
        fig.update_xaxes(range=rango_inicial(x.max()))
        return fig, {"franja": franja(L, [(t("brecha_principal", L), x, c["brecha_hp_tiempo_real"], "pp", "t", "q", 1, "%")])}

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
        fig = base(L, delta=True)
        panel_cambio(fig, w["fecha"], w["tpm_real_exante"], "pp", "a", L, t("tasa_real", L))
        fig.add_hrect(y0=lo, y1=hi, fillcolor="rgba(82,81,78,0.13)", line_width=0, layer="below")
        fig.add_annotation(xref="paper", x=0.01, y=hi, yanchor="bottom", xanchor="left", showarrow=False,
                           text=t("neutral_label", L), font=dict(size=11, color=INK2))
        self._l(fig, w["fecha"], w["tpm_real_exante"], t("tasa_real", L), C1, fmt=".1f", cambio=("pp", "a"))
        fig.add_hline(y=0, line=dict(color=INK2, width=1))
        fig.update_xaxes(range=rango_inicial(w["fecha"].max()))
        return fig, {"franja": franja(L, [(t("tasa_real", L), w["fecha"], w["tpm_real_exante"], "pp", "a", "d", 1, "%")])}

    def trayectoria_inflacion(self):
        """Inflacion que el mercado descuenta para los proximos 10 anos (tramos implicitos en los TES),
        junto a la inflacion observada: permite 'ver el futuro' que hoy pagan los bonos."""
        L, d = self.lang, self.d
        tt = d.tasas.dropna(subset=["bei_1y", "bei_5y", "bei_10y"])
        if tt.empty:
            return None, {}, None
        hoy = tt.iloc[-1]
        prev = tt[tt["fecha"] <= hoy["fecha"] - pd.DateOffset(years=1)]
        fig = base(L, height=400)
        meta_banda(fig, L)
        inf = d.inflacion[d.inflacion["fecha"] >= hoy["fecha"] - pd.DateOffset(years=4)]
        self._l(fig, inf["fecha"] + pd.offsets.MonthEnd(0), inf["inflacion_anual"], t("inf_observada", L), GRAY,
                width=2, fmt=".2f")

        def tramos(r):
            b1, b5, b10 = (float(r[k]) / 100 for k in ("bei_1y", "bei_5y", "bei_10y"))
            f15 = ((1 + b5) ** 5 / (1 + b1)) ** 0.25 - 1
            f510 = ((1 + b10) ** 10 / (1 + b5) ** 5) ** 0.2 - 1
            return [(0, 1, 100 * b1), (1, 5, 100 * f15), (5, 10, 100 * f510)]

        def dibujar(r, nombre, color, dash, ancho, etiquetas):
            f0 = pd.Timestamp(r["fecha"])
            xs, ys, txt = [], [], []
            for a, b, v in tramos(r):
                xa, xb = f0 + pd.DateOffset(years=a), f0 + pd.DateOffset(years=b)
                xs += [xa, xb, None]
                ys += [round(v, 2), round(v, 2), None]
                rango = f"{xa.year}–{xb.year}"
                txt += [rango, rango, ""]
                if etiquetas:
                    fig.add_annotation(x=xa + (xb - xa) / 2, y=v, text=f"<b>{num(v, 1, L)}%</b>", showarrow=False,
                                       yshift=13, font=dict(size=12.5, color=color))
            fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", name=nombre, line=dict(color=color, width=ancho, dash=dash),
                                     customdata=txt, connectgaps=False,
                                     hovertemplate="%{customdata}: %{y:.1f}%<extra>" + nombre + "</extra>"))
        if not prev.empty:
            dibujar(prev.iloc[-1], t("tray_antes", L).format(f=fecha(prev.iloc[-1]["fecha"], "m", L)), GRAY, "dot", 2, False)
        dibujar(hoy, t("tray_hoy", L).format(f=fecha(hoy["fecha"], "d", L)), C7, None, 4, True)
        fig.add_vline(x=pd.Timestamp(hoy["fecha"]), line=dict(color=INK2, width=1, dash="dot"))
        fig.add_annotation(x=pd.Timestamp(hoy["fecha"]), yref="paper", y=1, text=t("tray_hoy_corto", L), showarrow=False,
                           xanchor="left", yanchor="top", xshift=4, font=dict(size=11.5, color=INK2))
        fig.update_layout(hovermode="closest")
        fig.update_xaxes(range=[(hoy["fecha"] - pd.DateOffset(years=4)).strftime("%Y-%m-%d"),
                                (hoy["fecha"] + pd.DateOffset(years=10, months=3)).strftime("%Y-%m-%d")])
        return fig, {"notime": True}, tramos(hoy)

    def anclaje(self):
        L, w = self.lang, semanal(self.d.tasas, ["bei_5y5y"])
        fig = base(L, delta=True)
        panel_cambio(fig, w["fecha"], w["bei_5y5y"], "pp", "a", L, t("espera_largo", L))
        meta_banda(fig, L)
        self._l(fig, w["fecha"], w["bei_5y5y"], t("espera_largo", L), C7, cambio=("pp", "a"))
        fig.update_xaxes(range=rango_inicial(w["fecha"].max()))
        return fig, {"franja": franja(L, [(t("espera_largo", L), w["fecha"], w["bei_5y5y"], "pp", "a", "d", 1, "%")])}

    def itcr(self):
        L, it = self.lang, self.d.extra["itcr_ipc"]
        if it.empty:
            return None, {}
        fig = base(L, suffix="", delta=True)
        x = it["fecha"] + pd.offsets.MonthEnd(0)
        panel_cambio(fig, x, it["itcr_ipc"], "pct", "a", L, t("itcr_linea", L))
        self._l(fig, x, it["itcr_ipc"], t("itcr_linea", L), C1, fmt=".1f", suf="", cambio=("pct", "a"))
        fig.add_hline(y=100, line=dict(color=INK2, width=1))
        fig.update_xaxes(range=rango_inicial(it["fecha"].max()))
        return fig, {"franja": franja(L, [(t("itcr_linea", L), x, it["itcr_ipc"], "pct", "a", "m", 1, "")])}


def franja_indices(lang, ix, series):
    """Rentabilidad de cada indice en el ultimo mes y en 12 meses."""
    partes = []
    for col, nombre, color, _ in series:
        s_ = pd.Series(list(ix[col]), index=pd.to_datetime(ix["fecha"])).dropna()
        cambios = []
        for per in ("a", "m"):
            ch = serie_cambio(s_.index, s_.values, "pct", per).iloc[-1]
            if pd.notna(ch):
                clase = "up" if ch > 0.005 else ("down" if ch < -0.005 else "flat")
                cambios.append(f'<span class="chg {clase}">{txt_cambio(ch, "pct", lang)}</span> <small>{etiqueta_periodo(per, lang)}</small>')
        partes.append(f'<div class="stat"><span class="stat-n"><i class="dot" style="background:{color}"></i>{esc(nombre)}</span>'
                      f'<span class="stat-c">{" &nbsp;·&nbsp; ".join(cambios)}</span></div>')
    return f'<div class="stats">{"".join(partes)}</div>'


def tabla_magnificas(b, L):
    head = "".join(f"<th>{t(k, L)}</th>" for k in ("col_empresa", "col_peso", "col_precio", "col_1m", "col_ano", "col_12m"))
    rows = []
    for r in b["magnificas"].itertuples():
        def c(v):
            if v is None or pd.isna(v):
                return "—"
            clase = "up" if v > 0.005 else ("down" if v < -0.005 else "flat")
            return f'<span class="chg {clase}">{txt_cambio(v, "pct", L)}</span>'
        rows.append(f"<tr><td><b>{esc(r.emisor)}</b><br><small>{esc(r.clases)} · {esc(r.sector)}</small></td>"
                    f"<td class='n'>{num(r.peso, 1, L, suf='%')}</td><td class='n'>${num(r.precio, 0, L)}</td>"
                    f"<td class='n'>{c(r.var_1m)}</td><td class='n'>{c(r.var_ano)}</td><td class='n'>{c(r.var_12m)}</td></tr>")
    return f"<div class='table-wrap'><table class='tbl'><thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>"


# ------------------------------------------------------------------ selectores (sectores por trimestre, ciudad)
def selector_sectores(d, L):
    sc = d.sectores
    if sc is None or sc.empty:
        return ""
    trimestres = []
    for f in sorted(sc["fecha"].unique()):
        f = pd.Timestamp(f)
        u = sc[sc["fecha"] == f]
        a = sc[sc["fecha"] == f - pd.DateOffset(years=1)].set_index("codigo")["yoy"]
        trimestres.append({"f": qend(pd.Series([f])).iloc[0].strftime("%Y-%m-%d"), "q": fecha(f, "q", L), "qa": fecha(f - pd.DateOffset(years=1), "q", L),
                           "s": [[r.sector, round(r.yoy, 2), None if pd.isna(a.get(r.codigo)) else round(float(a.get(r.codigo)), 2),
                                  round(r.peso, 2), round(r.contribucion, 3)] for r in u.itertuples()]})
    datos = json.dumps(trimestres, ensure_ascii=False, separators=(",", ":"))
    opciones = "".join(f'<option value="{k}"{" selected" if k == len(trimestres) - 1 else ""}>{esc(q["q"])}</option>'
                       for k, q in enumerate(trimestres))
    txt = json.dumps({k: t(k, L) for k in ("sec_crec", "sec_hace", "sec_peso", "sec_aporte", "sec_raya")}, ensure_ascii=False)
    return (f'<div class="picker"><label>{t("sec_ver", L)} <select id="sec-q">{opciones}</select></label>'
            f'<button class="linkbtn" id="sec-ultimo">{t("tes_volver", L)}</button></div>'
            f'<script type="application/json" id="sec-datos">{datos}</script>'
            f'<script type="application/json" id="sec-textos">{txt}</script>')


# ------------------------------------------------------------------ publicaciones oficiales
def bloque_noticias(d, s, L, n=10):
    """Nota discreta al final: ultimos datos oficiales, una linea cada uno, con enlace a la fuente."""
    from colombiamacro import noticias as nt
    items = nt.publicaciones(d, s, L)[:n]
    if not items:
        return ""
    filas = []
    for it in items:
        cuando = t("nt_dato", L) if it["aprox"] else fecha(it["fecha"], "d", L)
        filas.append(
            f'<li><span class="n-meta"><span class="n-src">{esc(it["fuente"])}</span><span class="n-date">{cuando}</span></span>'
            f'<span class="n-body"><a href="{esc(it["enlace"])}" target="_blank" rel="noopener">{esc(it["titular"])}</a>'
            f'<span class="n-det">{esc(it["detalle"])}</span></span></li>')
    salas = " · ".join(f'<a href="{u}" target="_blank" rel="noopener">{esc(nombre)}</a>' for nombre, u in nt.SALAS)
    return (f'<aside id="noticias" class="notes"><div class="notes-head"><h3>{t("q_noticias", L)}</h3>'
            f'<span>{t("resp_noticias", L)}</span></div><ul>{"".join(filas)}</ul>'
            f'<p class="notes-foot">{t("nt_salas", L)}: {salas}</p></aside>')


# ------------------------------------------------------------------ reloj del ciclo interactivo
def datos_ciclo(d: mt.Datos, lang: str) -> dict:
    """Trimestres con brecha (nivel) y su cambio en 2 trimestres (direccion) para el reloj."""
    c = d.ciclo.dropna(subset=["brecha_hp_tiempo_real", "delta_brecha", "fase"])
    trimestres = [{"q": fecha(f, "q", lang), "f": qend(pd.Series([f])).iloc[0].strftime("%Y-%m-%d"),
                   "x": round(float(x), 3), "y": round(float(y), 3), "fase": fz}
                  for f, x, y, fz in zip(c["fecha"], c["brecha_hp_tiempo_real"], c["delta_brecha"], c["fase"])]
    fases = {k: {"nombre": v[0 if lang == "es" else 1], "color": v[2], "desc": t("fd_" + k, lang)}
             for k, v in am.FASES.items()}
    return {"trimestres": trimestres, "fases": fases}


def explorador_ciclo(d: mt.Datos, lang: str) -> str:
    L = lang
    datos = json.dumps(datos_ciclo(d, L), ensure_ascii=False, separators=(",", ":"))
    textos = json.dumps({k: t(k, L) for k in (
        "ck_fase", "ck_brecha", "ck_dir", "ck_racha", "ck_encima", "ck_debajo", "ck_mejora", "ck_empeora",
        "ck_trim", "ck_trim1", "ck_hist_x", "ck_hist_y", "ck_eje_x", "ck_eje_y", "ck_hover", "vs_2t")}, ensure_ascii=False)
    tr = datos_ciclo(d, L)["trimestres"]
    ult = tr[-1]
    racha = 1
    while racha < len(tr) and tr[-1 - racha]["fase"] == ult["fase"]:
        racha += 1
    resp = t("resp_ciclo", L).format(
        q=ult["q"], fase=am.FASES[ult["fase"]][0 if L == "es" else 1].lower(),
        nivel=t("ck_encima" if ult["x"] >= 0 else "ck_debajo", L).format(v=num(abs(ult["x"]), 1, L)),
        dir=t("ck_mejora" if ult["y"] >= 0 else "ck_empeora", L).format(v=num(abs(ult["y"]), 1, L)),
        n=racha, racha=t("ck_racha1", L) if racha == 1 else t("ck_rachan", L).format(n=racha)) + " " + t("fd_" + ult["fase"], L)
    leyenda = "".join(f'<span class="ph"><i style="background:{v[2]}"></i>{esc(v[0 if L == "es" else 1])}</span>'
                      for v in am.FASES.values())
    return f"""<section id="ciclo" class="cycle">
  <div class="sec-head"><span class="sec-num">◷</span><h2>{t("q_ciclo", L)}</h2></div>
  <p class="answer" id="ciclo-resp">{resp}</p>
  <div class="curve-app cycle-app" id="ciclo-app" data-lang="{L}">
    <div class="curve-ctrl">
      <label class="curve-date">{t("ck_ver", L)} <b id="ciclo-q">—</b></label>
      <input type="range" id="ciclo-slider" min="0" max="1" value="1" step="1" aria-label="{t('ck_ver', L)}">
      <div class="seg" role="group" aria-label="{t('ck_estela', L)}">
        <button data-n="4">{t("ck_1a", L)}</button><button data-n="8" class="on">{t("ck_2a", L)}</button><button data-n="12">{t("ck_3a", L)}</button>
      </div>
      <button class="linkbtn" id="ciclo-hoy">{t("tes_volver", L)}</button>
    </div>
    <div class="stats" id="ciclo-stats"></div>
    <div class="curve-grid">
      <figure class="chart"><figcaption>{t("g_reloj_main", L)}</figcaption><div class="plot" id="g-ciclo-reloj" style="height:420px"></div>
        <p class="how"><span>?</span>{t("h_reloj_main", L)}</p>{pie_ficha("g-ciclo-reloj", L)}</figure>
      <figure class="chart"><figcaption>{t("g_ciclo_hist", L)}</figcaption><div class="phases">{leyenda}</div>
        <div class="plot" id="g-ciclo-hist" style="height:380px"></div>
        <p class="how"><span>?</span>{t("h_ciclo_hist", L)}</p>{pie_ficha("g-ciclo-hist", L)}</figure>
    </div>
  </div>
  <script type="application/json" id="ciclo-datos">{datos}</script>
  <script type="application/json" id="ciclo-textos">{textos}</script>
</section>"""


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
      <p class="how"><span>?</span>{t('tes_h_curva', L)}</p>{pie_ficha("g-curva-tes", L)}</figure>
    <figure class="chart"><figcaption>{t('tes_g_hist', L)}</figcaption><div class="plot" id="g-curva-hist"></div>
      <p class="how"><span>?</span>{t('tes_h_hist', L)}</p>{pie_ficha("g-curva-hist", L)}</figure>
  </div>
</div>"""


def fig_html(fig, meta, gid):
    """Contenedor + JSON del grafico; el JS del sitio lo dibuja."""
    if fig is None:
        return None
    data = pio.to_json(fig, validate=False, pretty=False, engine="json")
    attrs = ' data-notime="1"' if meta.get("notime") else ""
    attrs += ' data-rebase="1"' if meta.get("rebase") else ""
    attrs += ' data-noy="1"' if meta.get("noy") else ""
    alto = int(fig.layout.height or 330)
    return (meta.get("antes", "") + meta.get("franja", "") + f'<div class="plot" id="{gid}"{attrs} style="height:{alto}px"></div>'
            f'<script type="application/json" data-for="{gid}">{data}</script>')


# ------------------------------------------------------------------ piezas HTML
def tarjeta(titulo, valor, detalle, estado, tono, pregunta_id):
    return (f'<a class="card" href="#{pregunta_id}"><div class="card-top"><span class="card-title">{esc(titulo)}</span>'
            f'<span class="pill {tono}">{esc(estado)}</span></div>'
            f'<div class="card-value">{esc(valor)}</div><div class="card-detail">{detalle}</div></a>')


def pie_ficha(gid, L):
    """Pie del grafico: fuente + '?' con la metodologia (tooltip accesible)."""
    from colombiamacro.sitio.fichas import ficha
    f = ficha(gid, L)
    if not f:
        return ""
    fuente, metodo = f
    return (f'<div class="ficha"><span class="src"><b>{t("fuente_pie", L)}:</b> {esc(fuente)}</span>'
            f'<span class="info" tabindex="0" role="button" aria-label="{t("metodo_pie", L)}">?'
            f'<span class="tip" role="tooltip"><b>{t("metodo_pie", L)}.</b> {esc(metodo)}</span></span></div>')


def bloque_grafico(titulo, fig_html_str, como_leer, nota=None, ancho=False):
    cuerpo = fig_html_str or '<div class="pending">—</div>'
    extra = f'<p class="note">{nota}</p>' if nota else ""
    m = re.search(r'class="plot" id="([^"]+)"', cuerpo)
    pie = pie_ficha(m.group(1), LANG_ACTUAL[0]) if m else ""
    return (f'<figure class="chart{" wide" if ancho else ""}"><figcaption>{esc(titulo)}</figcaption>{cuerpo}'
            f'<p class="how"><span>?</span>{como_leer}</p>{extra}{pie}</figure>')


LANG_ACTUAL = ["es"]
VERSION_ACTIVOS = ["0", "0"]  # huella de estilo.css + app.js (+ datos) y de plotly: evita versiones viejas en cache


def bloque_grafico_html(titulo, cuerpo, como_leer, gid_ficha):
    """Bloque para graficos dibujados en el navegador (selectores)."""
    if not cuerpo:
        return ""
    return (f'<figure class="chart"><figcaption>{esc(titulo)}</figcaption>{cuerpo}'
            f'<p class="how"><span>?</span>{como_leer}</p>{pie_ficha(gid_ficha, LANG_ACTUAL[0])}</figure>')


def inf_13_lista(d):
    ic = d.informalidad_ciudades
    if ic is None or ic.empty:
        return []
    return sorted(ic[ic["grupo"] == "13"]["ciudad"].unique())


def seccion(sid, num_, titulo, respuesta, graficos, detalle_html, lang, abierto=False):
    """abierto=True: el bloque extra se muestra siempre (no es detalle tecnico)."""
    if detalle_html and abierto:
        det = f'<div class="extra">{detalle_html}</div>'
    elif detalle_html:
        det = f'<details class="tech"><summary>{t("detalle_tecnico", lang)}</summary><div class="tech-body">{detalle_html}</div></details>'
    else:
        det = ""
    return (f'<section id="{sid}" class="section"><div class="sec-head"><span class="sec-num">{num_}</span>'
            f'<h2>{esc(titulo)}</h2></div><p class="answer">{respuesta}</p>'
            f'<div class="grid">{"".join(graficos)}</div>{det}</section>')


# ------------------------------------------------------------------ pagina
def pagina(d, s, lang, generado):
    L = lang
    ahora = pd.Timestamp.now(tz="America/Bogota")
    construido = f"{fecha(ahora, 'd', L)}, {ahora:%H:%M}"
    LANG_ACTUAL[0] = L
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
        an = tt.get("tpm_anunciada")
        if an:
            verbo = t("an_sube" if an["tasa"] > an["anterior"] else "an_baja", L)
            cards.append(tarjeta(t("c_tasa", L), num(an["tasa"], 2, L, suf="%"),
                                 t("an_detalle", L).format(a=fecha(an["anuncio"], "d", L), v=fecha(an["vigente"], "d", L),
                                                           p=num(an["anterior"], 2, L)),
                                 verbo, "warn", "banco"))
        else:
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
    fcap, mcap, ucap = g.capacidad()
    fpa, mpa, upa = g.crecimiento_anual()
    s1_det = (f'<p>{t("x_crec", L).format(g=num(ucap["gap"], 1, L, True), pot=num(ucap["pot"], 0, L), y=num(ucap["y"], 0, L))}</p>'
              f'<p>{t("x_crec2", L)}</p>')
    ise_txt = ""
    if s.get("ise"):
        ise_txt = t("resp_ise", L).format(v=num(s["ise"]["yoy"], 1, L), f=fecha(s["ise"]["fecha"], "m", L))
    tam_txt = t("pa_resp", L).format(v=num(upa["r12"], 1, L), q=fecha(upa["q"], "q", L),
                                     a=upa["ultimo_ano"], va=num(upa["v_ano"], 1, L), p=num(upa["prom"], 1, L))
    s1 = seccion("crecimiento", "1", t("q_crec", L),
                 t("resp_crec", L).format(v=num(c["pib_real_yoy"], 1, L), q=fecha(c["fecha"], "q", L),
                                          p=num(c["crecimiento_potencial_hp"], 1, L)) + " " + ise_txt + " " + tam_txt,
                 [bloque_grafico(t("g_crec", L), fig_html(fc, mc, "g-crec"), t("h_crec", L)),
                  bloque_grafico(t("g_pa", L), fig_html(fpa, mpa, "g-pib-anual"), t("h_pa", L))],
                 f'<p>{t("x_crec_pa", L)}</p>', L)

    # --- capacidad (despues de los sectores: primero cuanto y quien crece, luego si sobra o falta capacidad)
    s_cap = seccion("capacidad", "0", t("q_cap", L),
                    t("resp_cap", L).format(q=fecha(c["fecha"], "q", L), g=num(ucap["gap"], 1, L, True),
                                            e=t("cap_encima" if ucap["gap"] >= 0 else "cap_debajo", L)),
                    [bloque_grafico(t("g_cap", L), fig_html(fcap, mcap, "g-capacidad"), t("h_cap", L), ancho=True)],
                    s1_det, L)

    # --- sectores
    s_sec = ""
    sc = d.sectores
    if sc is not None and not sc.empty:
        f = sc["fecha"].max()
        u = sc[sc["fecha"] == f].sort_values("contribucion", ascending=False)
        rap = u.sort_values("yoy", ascending=False)
        neg = u[u["yoy"] < 0]["sector"].tolist()
        resp_sec = t("resp_sectores", L).format(
            q=fecha(f, "q", L), s1=rap.iloc[0]["sector"], v1=num(rap.iloc[0]["yoy"], 1, L),
            s2=rap.iloc[1]["sector"], v2=num(rap.iloc[1]["yoy"], 1, L),
            a=u.iloc[0]["sector"], ap=num(u.iloc[0]["contribucion"], 1, L), tot=num(u["contribucion"].sum(), 1, L))
        resp_sec += " " + (t("resp_sec_neg", L).format(lista=", ".join(neg)) if neg else t("resp_sec_todos", L))
        fsb, msb = g.sectores_barras()
        msb = dict(msb, antes=selector_sectores(d, L))
        fsm, msm = g.sectores_mapa()
        s_sec = seccion("sectores", "0", t("q_sectores", L), resp_sec,
                        [bloque_grafico(t("g_sec_barras", L).format(q=fecha(f, "q", L)), fig_html(fsb, msb, "g-sec-barras"), t("h_sec_barras", L)),
                         bloque_grafico(t("g_sec_mapa", L), fig_html(fsm, msm, "g-sec-mapa"), t("h_sec_mapa", L))],
                        f'<p>{t("x_sectores", L)}</p>', L)

    # --- informalidad
    s_inf = ""
    inf = d.informalidad
    if inf is not None and not inf.empty:
        ult = inf.iloc[-1]
        ant = inf[inf["fecha"] <= ult["fecha"] - pd.DateOffset(years=1)]
        ir = d.informalidad_ramas
        millones = ""
        if ir is not None and not ir.empty:
            uu = ir[ir["fecha"] == ir["fecha"].max()]
            millones = num(uu["informales"].sum() / 1000, 1, L)
        ventana = t("mov_" + str(ult["fecha"].month), L)
        resp_inf = t("resp_desempleo", L).format(v=num(s["laboral"]["td"], 1, L), f=fecha(s["laboral"]["fecha"], "m", L),
                                                 a=num(s["laboral"]["td_hace_12m"], 1, L)) + " " if s.get("laboral") and s["laboral"].get("td_hace_12m") is not None else ""
        resp_inf += t("resp_informal", L).format(
            v=num(ult["nacional"], 1, L), p=ventana + " " + str(ult["fecha"].year), m=millones,
            a=num(ant.iloc[-1]["nacional"], 1, L) if not ant.empty else "—",
            c=num(ult["ciudades_13"], 1, L), i=num(inf.iloc[0]["nacional"], 1, L))
        fin_, min_ = g.informalidad()
        fir, mir = g.informalidad_ramas()
        fic, mic = g.informalidad_ciudades()
        trece_txt = ", ".join(inf_13_lista(d))
        s_inf = seccion("informalidad", "0", t("q_informal", L), resp_inf,
                        [bloque_grafico(t("g_desempleo", L), fig_html(fd, md, "g-desempleo"), t("h_desempleo", L)),
                         bloque_grafico(t("g_informal", L), fig_html(fin_, min_, "g-informal"), t("h_informal", L)),
                         bloque_grafico(t("g_inf_ramas", L).format(p=ventana + " " + str(ult["fecha"].year)),
                                        fig_html(fir, mir, "g-inf-ramas"), t("h_inf_ramas", L)),
                         bloque_grafico(t("g_inf_ciudades", L).format(p=ventana + " " + str(ult["fecha"].year)),
                                        fig_html(fic, mic, "g-inf-ciudades"), t("h_inf_ciudades", L), ancho=True)],
                        f'<p>{t("x_informal", L).format(lista=trece_txt)}</p>', L)

    fi, mi = g.inflacion()
    fe, me = g.expectativas()
    s2_det = "".join(filter(None, [
        f'<p>{t("x_precios", L)}</p>',
        bloque_grafico(t("g_anclaje", L), fig_html(*g.anclaje(), "g-anclaje"), t("h_anclaje", L))]))
    basica = ""
    if i.get("basica") is not None:
        basica = t("resp_basica", L).format(v=num(i["basica"], 1, L))
    ftr, mtr, tramos_hoy = g.trayectoria_inflacion()
    graf_tray = ""
    if ftr is not None:
        graf_tray = bloque_grafico(t("g_tray", L), fig_html(ftr, mtr, "g-tray"), t("h_tray", L).format(
            a=num(tramos_hoy[0][2], 1, L), b=num(tramos_hoy[1][2], 1, L), c=num(tramos_hoy[2][2], 1, L)), ancho=True)
    s2 = seccion("precios", "2", t("q_precios", L),
                 t("resp_precios", L).format(v=num(i["total"], 2, L), m=fecha(i["fecha"], "m", L),
                                             a=num(i["hace_12m"], 1, L)) + " " + basica + " " +
                 t("resp_espera", L).format(v=num(tt["bei_1y"], 1, L)),
                 [bloque_grafico(t("g_inf", L), fig_html(fi, mi, "g-inf"), t("h_inf", L)),
                  bloque_grafico(t("g_espera", L), fig_html(fe, me, "g-espera"), t("h_espera", L)), graf_tray],
                 s2_det, L)

    fp, mp = g.politica()
    s3_det = "".join(filter(None, [
        f'<p>{t("x_real", L).format(v=num(tt.get("tpm") or 0, 2, L), e=num(tt["bei_1y"], 1, L), r=num(tt.get("tpm_real_exante") or 0, 1, L))}</p>',
        f'<p>{t("x_real2", L)}</p>',
        bloque_grafico(t("g_real", L), fig_html(*g.tasa_real(), "g-real"), t("h_real", L))]))
    resp3 = t("resp_banco_na", L)
    if tt.get("tpm") is not None:
        resp3 = t("resp_banco", L).format(v=num(tt["tpm"], 2, L), r=num(tt.get("tpm_real_exante"), 1, L),
                                          e=t(f"ep2_{post}", L))
        an = tt.get("tpm_anunciada")
        if an:
            resp3 = t("an_resp", L).format(a=fecha(an["anuncio"], "d", L), n=num(an["tasa"], 2, L),
                                           p=num(an["anterior"], 2, L), v=fecha(an["vigente"], "d", L)) + " " + resp3
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
               f'<p>{t("x_curva", L)}</p></div></details></section>')

    fdol, mdol = g.dolar()
    fb, mb = g.bolsa()
    s4_det = "".join(filter(None, [
        f'<p>{t("x_mercados", L)}</p>',
        bloque_grafico(t("g_itcr", L), fig_html(*g.itcr(), "g-itcr"), t("h_itcr", L))]))
    resp4 = t("resp_bolsa", L).format(v=num(m["colcap_12m"], 1, L, True))
    if m.get("trm") is not None:
        resp4 = t("resp_dolar", L).format(v=num(m["trm"], 0, L), c=num(m["trm_12m"], 1, L, True)) + " " + resp4
    s4 = seccion("mercados", "5", t("q_mercados", L), resp4,
                 [bloque_grafico(t("g_dolar", L), fig_html(fdol, mdol, "g-dolar"), t("h_dolar", L)),
                  bloque_grafico(t("g_bolsa", L), fig_html(fb, mb, "g-bolsa"), t("h_bolsa", L))],
                 s4_det, L)

    # --- 6. bolsa por dentro
    s_emp = ""
    b = mt.bolsa_por_dentro(d)
    if b is not None:
        ix = b["indices"].set_index("fecha")
        r12 = {c: serie_cambio(ix.index, ix[c], "pct", "a").iloc[-1] for c in ("colcap", "equiponderado", "magnificas")}
        nombres = ", ".join(b["magnificas"]["emisor"])
        conc = "resp_conc_si" if r12["colcap"] - r12["equiponderado"] > 2 else (
            "resp_conc_no" if r12["equiponderado"] - r12["colcap"] > 2 else "resp_conc_igual")
        resp_emp = t("resp_empresas", L).format(
            n=nombres, p=num(b["peso_magnificas"], 0, L), c=num(r12["colcap"], 1, L, True),
            e=num(r12["equiponderado"], 1, L, True), m=num(r12["magnificas"], 1, L, True)) + " " + t(conc, L)
        fbi, mbi = g.bolsa_indices(b)
        fpe, mpe = g.pesos(b)
        s_emp = seccion("empresas", "6", t("q_empresas", L), resp_emp,
                        [bloque_grafico(t("g_indices", L), fig_html(fbi, mbi, "g-indices"), t("h_indices", L)),
                         bloque_grafico(t("g_pesos", L).format(f=fecha(b["fecha_canasta"], "d", L)),
                                        fig_html(fpe, mpe, "g-pesos"), t("h_pesos", L))],
                        f'<h3 class="sub">{t("t_magnificas", L)}</h3>{tabla_magnificas(b, L)}'
                        f'<p class="method">{t("m_empresas", L)}</p>', L, abierto=True)

    resp5 = []
    if s.get("cc"):
        resp5.append(t("resp_cc", L).format(v=num(abs(s["cc"]["valor"]), 1, L), f=fecha(s["cc"]["fecha"], "q", L)))
    if s.get("deuda"):
        resp5.append(t("resp_deuda", L).format(v=num(s["deuda"]["valor"], 1, L), f=fecha(s["deuda"]["fecha"], "y", L)))
    s5 = seccion("externo", "7", t("q_externo", L), " ".join(resp5) or t("pendiente", L),
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
<link rel="stylesheet" href="{raiz}assets/estilo.css?v={VERSION_ACTIVOS[0]}">
<script src="{raiz}assets/plotly.min.js?v={VERSION_ACTIVOS[1]}" defer></script>
<script src="{raiz}assets/app.js?v={VERSION_ACTIVOS[0]}" defer></script>
</head><body>
<header class="top"><div class="wrap top-in">
  <a class="brand" href="#inicio"><img src="{raiz}assets/logo_usb.png" alt="USB Cali"><span><b>ColombiaMacro</b><small>{t("sub_marca", L)}</small></span></a>
  <nav class="menu" id="menu"><a href="#ciclo">{t("nav_ciclo", L)}</a><a href="#crecimiento">{t("nav_crec", L)}</a><a href="#sectores">{t("nav_sectores", L)}</a><a href="#capacidad">{t("nav_cap", L)}</a><a href="#informalidad">{t("nav_informal", L)}</a><a href="#precios">{t("nav_precios", L)}</a><a href="#banco">{t("nav_banco", L)}</a><a href="#curva">{t("nav_curva", L)}</a><a href="#mercados">{t("nav_mercados", L)}</a><a href="#empresas">{t("nav_empresas", L)}</a><a href="#indicadores">{t("nav_todos", L)}</a><a href="#noticias">{t("nav_noticias", L)}</a></nav>
  <button class="menu-toggle" id="menu-toggle" aria-controls="menu" aria-expanded="true" title="{t("menu_ocultar", L)}" data-ocultar="{t("menu_btn_ocultar", L)}" data-mostrar="{t("menu_btn_mostrar", L)}"><span class="mt-ico" aria-hidden="true">☰</span><span class="mt-txt">{t("menu_btn_ocultar", L)}</span></button>
  <a class="lang" href="{otro}">{t("otro_idioma", L)}</a>
</div></header>
<main id="inicio" class="wrap">
<section class="hero">
  <p class="kicker">{t("kicker", L)} · {t("datos_al", L)} {fecha(generado, "d", L)} · {t("construido", L)} {construido}</p>
  <h1>{t("h1", L)}</h1>
  <p class="summary">{esc(mt.resumen_simple(s, L))}</p>
  <div class="cards">{"".join(cards)}</div>
  <p class="disclaimer">{t("aviso_estados", L)}</p>
</section>
{explorador_ciclo(d, L)}
<div class="horizon" role="group" aria-label="{t('horizonte', L)}"><span>{t("horizonte", L)}:</span>
  <button data-years="3">{t("h3", L)}</button><button data-years="5">{t("h5", L)}</button><button data-years="10" class="on">{t("h10", L)}</button><button data-years="0">{t("htodo", L)}</button></div>
{s1}{s_sec}{s_cap}{s_inf}{s2}{s3}{s_curva}{s4}{s_emp}{s5}
<section id="indicadores" class="section"><div class="sec-head"><span class="sec-num">8</span><h2>{t("q_todos", L)}</h2></div>
<p class="answer">{t("resp_todos", L)}</p>{tabla}</section>
{bloque_noticias(d, s, L)}
<section id="fuentes" class="section"><div class="sec-head"><span class="sec-num">9</span><h2>{t("q_fuentes", L)}</h2></div>
<p class="answer">{t("resp_fuentes", L)}</p>{fuentes}
<p class="downloads"><b>{t("descargar", L)}:</b> {descargas}</p>
<p class="downloads"><b>{t("documentos", L)}:</b> <a href="{REPO_URL}/blob/main/docs/METODOLOGIA.md">{t("metodologia", L)}</a> · <a href="{REPO_URL}/raw/main/docs/Manual_ColombiaMacro.pdf">{t("manual", L)}</a> · <a href="{REPO_URL}">GitHub</a></p>
<details class="tech"><summary>{t("glosario", L)}</summary><dl class="gloss">{gloss}</dl></details>
</section>
</main>
<footer class="wrap foot"><p>{t("aviso", L)}</p><p>DANE · Banco de la República · BVC/MSCI · Ministerio de Hacienda · {t("generado", L)} {fecha(generado, "d", L)}</p></footer>
</body></html>"""


def numerar_secciones(html_: str) -> str:
    """Numera las secciones en el orden en que aparecen (1, 2, 3...)."""
    contador = iter(range(1, 100))
    return re.sub(r'<span class="sec-num">\d+</span>', lambda m: f'<span class="sec-num">{next(contador)}</span>', html_)


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
    import hashlib
    h = hashlib.sha256()
    for f in ("estilo.css", "app.js", "curva_tes.json"):
        h.update((salida / "assets" / f).read_bytes())
    VERSION_ACTIVOS[0] = h.hexdigest()[:10]
    VERSION_ACTIVOS[1] = hashlib.sha256((salida / "assets" / "plotly.min.js").read_bytes()).hexdigest()[:10]
    (salida / "index.html").write_text(numerar_secciones(pagina(d, s, "es", generado)), encoding="utf-8")
    (salida / "en" / "index.html").write_text(numerar_secciones(pagina(d, s, "en", generado)), encoding="utf-8")
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
