"""Pagina de la curva TES ampliada (v12.11): ocho medidas, nivel-pendiente-curvatura, episodios de curva
invertida, como se movio la curva, tasa nominal = real + compensacion por inflacion, prima sobre la tasa
del Banco y volatilidad, ventana explicativa de la curva cero cupon y literatura.

Solo datos observados: curva cero cupon de los TES que calcula el Banco de la Republica (Nelson-Siegel
sobre operaciones del SEN y del MEC) y tasa de politica monetaria.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

TX = {
    "s_medidas": ("La curva TES en ocho medidas", "The TES curve in eight measures"),
    "s_factores": ("Nivel, pendiente y curvatura", "Level, slope and curvature"),
    "s_mov": ("¿Cómo se ha movido la curva?", "How has the curve moved?"),
    "s_real": ("Tasa nominal, tasa real y compensación por inflación", "Nominal rate, real rate and inflation compensation"),
    "s_riesgo": ("Prima sobre la tasa del Banco y volatilidad", "Premium over the policy rate and volatility"),
    "s_lit": ("Bases metodológicas y literatura", "Methodological basis and literature"),
    # lecturas
    "l_10": ("TES 10 años · {f}", "10-year TES · {f}"), "l_10_d": ("hace un año {v}", "a year ago {v}"),
    "l_1": ("TES 1 año", "1-year TES"), "l_1_d": ("tasa del Banco {v}", "policy rate {v}"),
    "l_pend": ("Pendiente 10 − 1 años", "Slope 10 − 1 years"), "l_pend_d": ("más plana que el {p} de los días desde 2003", "flatter than {p} of days since 2003"),
    "l_pend_d2": ("más empinada que el {p} de los días desde 2003", "steeper than {p} of days since 2003"),
    "l_real": ("Tasa real 10 años (UVR)", "10-year real rate (UVR)"), "l_real_d": ("hace un año {v}", "a year ago {v}"),
    "l_bei": ("Compensación por inflación 10 años", "10-year inflation compensation"), "l_bei_d": ("meta del Banco 3% · incluye primas", "Bank target 3% · includes premia"),
    "l_prima": ("TES 10 años − tasa del Banco", "10-year TES − policy rate"), "l_prima_d": ("promedio desde 2003 {v}", "average since 2003 {v}"),
    "l_vol": ("Volatilidad del TES 10 años", "10-year TES volatility"), "l_vol_d": ("anualizada, 60 días · promedio {v}", "annualised, 60 days · average {v}"),
    "l_mov": ("Movimiento en 12 meses", "12-month move"), "l_mov_d": ("nivel {n} · pendiente {p}", "level {n} · slope {p}"),
    # tipos de movimiento
    "bear_steep": ("Alza con empinamiento", "Bear steepening"), "bear_flat": ("Alza con aplanamiento", "Bear flattening"),
    "bull_steep": ("Baja con empinamiento", "Bull steepening"), "bull_flat": ("Baja con aplanamiento", "Bull flattening"),
    "quieto": ("Sin cambio de fondo", "No material change"),
    "mov_txt": {"bear_steep": ("las tasas subieron, más en los plazos largos", "rates rose, more at the long end"),
                "bear_flat": ("las tasas subieron, más en los plazos cortos", "rates rose, more at the short end"),
                "bull_steep": ("las tasas bajaron, más en los plazos cortos", "rates fell, more at the short end"),
                "bull_flat": ("las tasas bajaron, más en los plazos largos", "rates fell, more at the long end"),
                "quieto": ("el nivel y la pendiente casi no cambiaron", "level and slope barely changed")},
    # respuestas
    "r_medidas": ("El TES a 10 años rinde {l} y el de 1 año {c}; la pendiente es {p}, más plana que en el {q} de los días desde 2003. "
                  "La tasa real a 10 años (UVR) es {r} y la compensación por inflación implícita {b}. En 12 meses: {mov}.",
                  "The 10-year TES yields {l} and the 1-year {c}; the slope is {p}, flatter than on {q} of days since 2003. "
                  "The 10-year real rate (UVR) is {r} and implied inflation compensation {b}. Over 12 months: {mov}."),
    "r_factores": ("El nivel de la curva (promedio de 1, 5 y 10 años) es {n}, frente a un promedio histórico de {nh}. La pendiente es {p} y la curvatura {c}. "
                   "Desde 2003 la curva estuvo invertida (10 años por debajo de 1 año) en {k} episodios; el más reciente {ep}.",
                   "The curve level (average of 1, 5 and 10 years) is {n}, against a historical average of {nh}. The slope is {p} and the curvature {c}. "
                   "Since 2003 the curve was inverted (10 years below 1 year) in {k} episodes; the most recent {ep}."),
    "ep_txt": ("fue entre {a} y {b} (mínimo {m})", "ran from {a} to {b} (low {m})"),
    "r_mov": ("En 12 meses el TES a 1 año cambió {d1}, el de 5 años {d5} y el de 10 años {d10}: {mov}. "
              "Del cambio a 10 años, {dr} vino de la tasa real y {db} de la compensación por inflación.",
              "Over 12 months the 1-year TES changed {d1}, the 5-year {d5} and the 10-year {d10}: {mov}. "
              "Of the 10-year change, {dr} came from the real rate and {db} from inflation compensation."),
    "r_real": ("Un TES en pesos paga tasa real más compensación por inflación. Hoy, a 10 años: {n} nominal = {r} real (UVR) y {b} de compensación. "
               "La compensación supera la meta del Banco (3%) en {x} pp: incluye la inflación que el mercado descuenta y primas por riesgo y liquidez.",
               "A peso TES pays a real rate plus inflation compensation. Today, at 10 years: {n} nominal = {r} real (UVR) and {b} compensation. "
               "Compensation exceeds the Bank's target (3%) by {x} pp: it includes the inflation the market prices in plus risk and liquidity premia."),
    "r_riesgo": ("El TES a 10 años está {s} sobre la tasa del Banco ({h} en promedio desde 2003). "
                 "Su volatilidad anualizada de los últimos 60 días es {v}, {cmp} su promedio histórico ({vh}).",
                 "The 10-year TES is {s} over the policy rate ({h} on average since 2003). "
                 "Its annualised volatility over the last 60 days is {v}, {cmp} its historical average ({vh})."),
    "sobre": ("por encima de", "above"), "bajo": ("por debajo de", "below"),
    # graficos
    "g_fac": ("Nivel, pendiente y curvatura de la curva en pesos", "Level, slope and curvature of the peso curve"),
    "h_fac": ("Nivel = promedio de 1, 5 y 10 años. Pendiente = 10 años − 1 año. Curvatura = 2 × 5 años − 1 año − 10 años (positiva: la parte media está alta).",
              "Level = average of 1, 5 and 10 years. Slope = 10 years − 1 year. Curvature = 2 × 5 years − 1 year − 10 years (positive: the belly is high)."),
    "g_inv": ("Pendiente y episodios de curva invertida", "Slope and inverted-curve episodes"),
    "h_inv": ("Pendiente 10 − 1 años. Las franjas marcan los periodos en que el TES a 10 años rindió menos que el de 1 año.",
              "Slope 10 − 1 years. Shaded areas mark periods when the 10-year TES yielded less than the 1-year."),
    "lbl_nivel": ("Nivel", "Level"), "lbl_pend": ("Pendiente", "Slope"), "lbl_curv": ("Curvatura", "Curvature"),
    "g_cambios": ("Cambio de cada plazo (puntos básicos)", "Change at each maturity (basis points)"),
    "h_cambios": ("Cambio de la tasa cero cupón en 1, 3 y 12 meses. 100 pb = 1 punto porcentual.",
                  "Change in the zero-coupon rate over 1, 3 and 12 months. 100 bp = 1 percentage point."),
    "lbl_1m": ("1 mes", "1 month"), "lbl_3m": ("3 meses", "3 months"), "lbl_12m": ("12 meses", "12 months"),
    "g_desc": ("¿Tasa real o inflación? Cambio en 12 meses", "Real rate or inflation? 12-month change"),
    "h_desc": ("Cambio en 12 meses de cada plazo separado en tasa real (TES UVR) y diferencia nominal − real.",
               "12-month change at each maturity split into real rate (UVR TES) and the nominal − real gap."),
    "lbl_real": ("Tasa real (UVR)", "Real rate (UVR)"), "lbl_comp": ("Nominal − real", "Nominal − real"),
    "g_fisher": ("Nominal = real + compensación por inflación (hoy)", "Nominal = real + inflation compensation (today)"),
    "h_fisher": ("Barras apiladas: tasa real del TES UVR y diferencia hasta la tasa del TES en pesos. Pase el cursor para ver la compensación exacta (Fisher).",
                 "Stacked bars: real rate of the UVR TES and the gap to the peso TES rate. Hover for the exact compensation (Fisher)."),
    "g_real_hist": ("Tasa real y compensación por inflación a 10 años", "10-year real rate and inflation compensation"),
    "h_real_hist": ("Tasa del TES UVR a 10 años y compensación por inflación implícita (Fisher). La franja verde es el rango meta del Banco.",
                    "Rate of the 10-year UVR TES and implied inflation compensation (Fisher). The green band is the Bank's target range."),
    "lbl_bei": ("Compensación por inflación", "Inflation compensation"),
    "g_prima": ("TES frente a la tasa del Banco", "TES versus the policy rate"),
    "h_prima": ("Diferencia entre el TES a 1 y a 10 años y la tasa de política monetaria, en puntos porcentuales.",
                "Gap between the 1- and 10-year TES and the monetary policy rate, in percentage points."),
    "lbl_p1": ("1 año − tasa del Banco", "1 year − policy rate"), "lbl_p10": ("10 años − tasa del Banco", "10 years − policy rate"),
    "g_vol": ("Volatilidad del TES a 10 años", "10-year TES volatility"),
    "h_vol": ("Desviación estándar de los cambios diarios de los últimos 60 días hábiles, anualizada (× √252), en puntos básicos.",
              "Standard deviation of daily changes over the last 60 business days, annualised (× √252), in basis points."),
    "lbl_vol": ("Volatilidad anualizada", "Annualised volatility"),
    "plazo": ("{n} {u}", "{n} {u}"),
    "tab_ep": ("Episodios de curva invertida", "Inverted-curve episodes"),
    "th": (("Desde", "Hasta", "Días hábiles", "Pendiente mínima", "Tasa del Banco al inicio"),
           ("From", "To", "Business days", "Lowest slope", "Policy rate at start")),
}
LITERATURA = [
    ("Fisher, I. (1930). <i>The Theory of Interest</i>. Macmillan.",
     "Tasa nominal = tasa real + compensación por inflación.", "Nominal rate = real rate + inflation compensation."),
    ("Nelson, C. R. y Siegel, A. F. (1987). Parsimonious Modeling of Yield Curves. <i>Journal of Business</i>, 60(4), 473–489.",
     "Modelo con el que el Banco de la República estima la curva cero cupón de los TES.", "Model the Banco de la República uses to estimate the TES zero-coupon curve."),
    ("Litterman, R. y Scheinkman, J. (1991). Common Factors Affecting Bond Returns. <i>Journal of Fixed Income</i>, 1(1), 54–61.",
     "Nivel, pendiente y curvatura explican casi todo el movimiento de la curva.", "Level, slope and curvature explain almost all curve movements."),
    ("Estrella, A. y Hardouvelis, G. A. (1991). The Term Structure as a Predictor of Real Economic Activity. <i>Journal of Finance</i>, 46(2), 555–576.",
     "El contenido informativo de la pendiente de la curva.", "The information content of the curve's slope."),
    ("Gürkaynak, R. S., Sack, B. y Wright, J. H. (2010). The TIPS Yield Curve and Inflation Compensation. <i>American Economic Journal: Macroeconomics</i>, 2(1), 70–92.",
     "Por qué la compensación por inflación incluye primas además de la inflación esperada.", "Why inflation compensation includes premia besides expected inflation."),
    ("Arango, L. E., Melo, L. F. y Vásquez, D. M. (2002). Estimación de la estructura a plazo de las tasas de interés en Colombia. <i>Borradores de Economía</i> 196, Banco de la República.",
     "Estimación de la curva cero cupón colombiana.", "Estimation of the Colombian zero-coupon curve."),
    ("Espinosa, J. A., Melo, L. F. y Moreno, J. F. (2014). Estimación de la prima por vencimiento de los TES en pesos del gobierno colombiano. <i>Borradores de Economía</i> 854, Banco de la República.",
     "La prima por plazo de los TES crece y se vuelve más volátil con el vencimiento.", "The TES term premium rises and becomes more volatile with maturity."),
]


def tx(k, L):
    return TX[k][0 if L == "es" else 1]


def tipo_movimiento(d_nivel: float, d_pend: float, umbral: float = 0.10) -> str:
    """Clasificacion clasica del movimiento de la curva (en pp)."""
    if abs(d_nivel) < umbral and abs(d_pend) < umbral:
        return "quieto"
    alza = d_nivel >= 0
    emp = d_pend >= 0
    return ("bear" if alza else "bull") + ("_steep" if emp else "_flat")


def episodios_invertida(pend: pd.Series, tpm: pd.Series | None = None, min_dias: int = 5) -> pd.DataFrame:
    """Tramos consecutivos con pendiente 10-1 negativa de al menos `min_dias` dias habiles."""
    pend = pend.dropna()
    inv = pend < 0
    grupo = (inv != inv.shift()).cumsum()
    filas = []
    for _, g in pend[inv].groupby(grupo[inv]):
        if len(g) >= min_dias:
            t0 = float(tpm.asof(g.index[0])) if tpm is not None and not tpm.dropna().empty else np.nan
            filas.append({"desde": g.index[0], "hasta": g.index[-1], "dias": len(g), "minimo": float(g.min()), "tpm": t0})
    return pd.DataFrame(filas, columns=["desde", "hasta", "dias", "minimo", "tpm"])


def factores(c: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({"nivel": c[["tes_pesos_1y", "tes_pesos_5y", "tes_pesos_10y"]].mean(axis=1),
                         "pendiente": c["tes_pesos_10y"] - c["tes_pesos_1y"],
                         "curvatura": 2 * c["tes_pesos_5y"] - c["tes_pesos_1y"] - c["tes_pesos_10y"]}, index=c.index)


def volatilidad(serie: pd.Series, ventana: int = 60) -> pd.Series:
    """Volatilidad anualizada (pb) de los cambios diarios."""
    return serie.diff().mul(100).rolling(ventana, min_periods=int(ventana * 0.8)).std() * np.sqrt(252)


def construir_curva(d, L):
    """Devuelve (antes, despues)."""
    from colombiamacro.sitio import construir as cs
    num, fecha, esc = cs.num, cs.fecha, cs.esc
    cs.LANG_ACTUAL[0] = L
    k = 0 if L == "es" else 1
    pct = lambda v, dec=2, sg=False: num(float(v), dec, L, sg, "%")
    pp = lambda v, dec=2, sg=True: num(float(v), dec, L, sg, " pp")
    pb = lambda v: num(float(v) * 100, 0, L, True, " pb" if L == "es" else " bp")

    c = (d.tasas.dropna(subset=["tes_pesos_1y", "tes_pesos_5y", "tes_pesos_10y"]).sort_values("fecha")
         .drop_duplicates("fecha", keep="last").set_index("fecha"))
    if len(c) < 500:
        return "", ""
    tpm = d.tasas.set_index("fecha")["tpm"].dropna().sort_index() if "tpm" in d.tasas else pd.Series(dtype=float)
    hoy = c.index[-1]
    u = c.iloc[-1]
    hace = lambda off: c.loc[:hoy - off].iloc[-1]
    a12, a3, a1 = hace(pd.DateOffset(years=1)), hace(pd.DateOffset(months=3)), hace(pd.DateOffset(months=1))
    F = factores(c)
    fu, f12 = F.iloc[-1], F.loc[:hoy - pd.DateOffset(years=1)].iloc[-1]
    q_pend = float((F["pendiente"] > fu["pendiente"]).mean() * 100)   # % de dias con pendiente mayor
    mov = tipo_movimiento(fu["nivel"] - f12["nivel"], fu["pendiente"] - f12["pendiente"])
    tpm_hoy = float(tpm.asof(hoy)) if not tpm.empty else np.nan
    prima = (c["tes_pesos_10y"] - tpm.reindex(c.index, method="ffill")).dropna()
    prima1 = (c["tes_pesos_1y"] - tpm.reindex(c.index, method="ffill")).dropna()
    vol = volatilidad(c["tes_pesos_10y"]).dropna()
    bei10 = c["bei_10y"] if "bei_10y" in c else 100 * ((1 + c["tes_pesos_10y"] / 100) / (1 + c["tes_uvr_10y"] / 100) - 1)
    ff = fecha(hoy, "d", L)

    def seccion(sid, titulo, resp, cuerpo):
        return (f'<section id="{sid}" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{titulo}</h2></div>'
                f'{cs.respuesta_html(resp, L)}{cuerpo}</section>')

    def lec(kk, v, dsc, tono, href):
        return (f'<a class="lec {tono}" href="{href}"><span class="lec-k">{kk}</span><b class="lec-v">{v}</b>'
                f'<span class="lec-d">{dsc}</span></a>')

    pend_d = (tx("l_pend_d", L).format(p=pct(q_pend, 0)) if q_pend >= 50
              else tx("l_pend_d2", L).format(p=pct(100 - q_pend, 0)))
    tiles = [
        lec(tx("l_10", L).format(f=ff), pct(u["tes_pesos_10y"]), tx("l_10_d", L).format(v=pct(a12["tes_pesos_10y"])), "", "#curva"),
        lec(tx("l_1", L), pct(u["tes_pesos_1y"]), tx("l_1_d", L).format(v=pct(tpm_hoy)), "", "#curva"),
        lec(tx("l_pend", L), pp(fu["pendiente"]), pend_d, "warn" if fu["pendiente"] < 0.5 else "", "#cv-factores"),
        lec(tx("l_real", L), pct(u["tes_uvr_10y"]), tx("l_real_d", L).format(v=pct(a12["tes_uvr_10y"])), "", "#cv-real"),
        lec(tx("l_bei", L), pct(bei10.iloc[-1]), tx("l_bei_d", L), "warn" if bei10.iloc[-1] > 4 else "ok", "#cv-real"),
        lec(tx("l_prima", L), pp(prima.iloc[-1]), tx("l_prima_d", L).format(v=pp(prima.mean())), "", "#cv-riesgo"),
        lec(tx("l_vol", L), num(float(vol.iloc[-1]), 0, L, False, " pb" if L == "es" else " bp"),
            tx("l_vol_d", L).format(v=num(float(vol.mean()), 0, L, False, " pb" if L == "es" else " bp")),
            "warn" if vol.iloc[-1] > vol.quantile(0.8) else "", "#cv-riesgo"),
        lec(tx("l_mov", L), tx(mov, L), tx("l_mov_d", L).format(n=pb(fu["nivel"] - f12["nivel"]), p=pb(fu["pendiente"] - f12["pendiente"])), "", "#cv-movimientos"),
    ]
    r0 = tx("r_medidas", L).format(l=pct(u["tes_pesos_10y"]), c=pct(u["tes_pesos_1y"]), p=pp(fu["pendiente"]), q=pct(q_pend, 0),
                                   r=pct(u["tes_uvr_10y"]), b=pct(bei10.iloc[-1]), mov=TX["mov_txt"][mov][k])
    antes = seccion("cv-medidas", tx("s_medidas", L), r0, f'<div class="lecturas ocho">{"".join(tiles)}</div>')

    # ------------------------------------------------ factores
    w = F.resample("W-FRI").last().dropna()
    f1 = cs.base(L, height=340, suffix="")
    cs.linea(f1, w.index, w["nivel"], tx("lbl_nivel", L), cs.C1, width=2.4, suf="%", lang=L)
    cs.linea(f1, w.index, w["pendiente"], tx("lbl_pend", L), cs.C2, width=2.0, suf=" pp", lang=L)
    cs.linea(f1, w.index, w["curvatura"], tx("lbl_curv", L), cs.C3, width=1.6, suf=" pp", lang=L)
    f1.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    q_btn = (f'<button type="button" class="ex-q" data-dialog="exp-curva" aria-haspopup="dialog" '
             f'title="{"¿Qué es la curva cero cupón de los TES?" if L == "es" else "What is the TES zero-coupon curve?"}">?</button>')
    g1 = cs.bloque_grafico(tx("g_fac", L), cs.fig_html(f1, {}, "g-cv-factores"), tx("h_fac", L))
    g1 = g1.replace("</figcaption>", f" {q_btn}</figcaption>", 1)
    ep = episodios_invertida(F["pendiente"], tpm)
    f2 = cs.base(L, height=340, suffix=" pp")
    for e in ep.itertuples():
        f2.add_vrect(x0=e.desde, x1=e.hasta + pd.Timedelta(days=1), fillcolor="rgba(235,104,52,0.16)", line_width=0, layer="below")
    cs.linea(f2, w.index, w["pendiente"], tx("lbl_pend", L), cs.C2, width=2.0, suf=" pp", lang=L)
    f2.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    g2 = cs.bloque_grafico(tx("g_inv", L), cs.fig_html(f2, {}, "g-cv-invertida"), tx("h_inv", L))
    th = TX["th"][k]
    filas = "".join(f"<tr><td>{fecha(e.desde, 'd', L)}</td><td>{fecha(e.hasta, 'd', L)}</td><td class='n'>{e.dias}</td>"
                    f"<td class='n'>{pp(e.minimo)}</td><td class='n'>{pct(e.tpm)}</td></tr>" for e in ep.iloc[::-1].itertuples())
    tabla = (f'<div class="table-wrap"><table class="tbl"><caption>{tx("tab_ep", L)}</caption><thead><tr>'
             f'{"".join(f"<th>{h}</th>" for h in th)}</tr></thead><tbody>{filas}</tbody></table></div>') if len(ep) else ""
    ult = ep.iloc[-1] if len(ep) else None
    r1 = tx("r_factores", L).format(n=pct(fu["nivel"]), nh=pct(F["nivel"].mean()), p=pp(fu["pendiente"]), c=pp(fu["curvatura"]), k=len(ep),
                                    ep=tx("ep_txt", L).format(a=fecha(ult["desde"], "d", L), b=fecha(ult["hasta"], "d", L), m=pp(ult["minimo"])) if ult is not None else "—")
    s_fac = seccion("cv-factores", tx("s_factores", L), r1, f'<div class="grid">{g1}{g2}</div>{tabla}') + ventana_curva(u, bei10.iloc[-1], L, num)

    # ------------------------------------------------ movimientos
    plazos = [("1y", 1), ("5y", 5), ("10y", 10)]
    etq = [f"{n} {'año' if n == 1 else 'años'}" if L == "es" else f"{n} {'year' if n == 1 else 'years'}" for _, n in plazos]
    f3 = cs.base(L, height=330, fecha_x=False, suffix=" pb" if L == "es" else " bp")
    for ref, lbl, color in ((a1, "lbl_1m", cs.C3), (a3, "lbl_3m", cs.C1), (a12, "lbl_12m", cs.C2)):
        dv = [round((u[f"tes_pesos_{p}"] - ref[f"tes_pesos_{p}"]) * 100) for p, _ in plazos]
        f3.add_trace(go.Bar(x=etq, y=dv, name=tx(lbl, L), marker=dict(color=color, line=dict(width=0)),
                            text=[num(v_, 0, L, True) for v_ in dv], textposition="outside", cliponaxis=False,
                            hovertemplate="%{x} · " + tx(lbl, L) + ": %{y:+.0f}<extra></extra>"))
    f3.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    f3.update_layout(barmode="group", bargap=0.3, hovermode="closest")
    g3 = cs.bloque_grafico(tx("g_cambios", L), cs.fig_html(f3, {"notime": True, "noy": True}, "g-cv-cambios"), tx("h_cambios", L))
    dreal = [round((u[f"tes_uvr_{p}"] - a12[f"tes_uvr_{p}"]) * 100) for p, _ in plazos]
    dnom = [round((u[f"tes_pesos_{p}"] - a12[f"tes_pesos_{p}"]) * 100) for p, _ in plazos]
    dcomp = [n_ - r_ for n_, r_ in zip(dnom, dreal)]
    f4 = cs.base(L, height=330, fecha_x=False, suffix=" pb" if L == "es" else " bp")
    f4.add_trace(go.Bar(x=etq, y=dreal, name=tx("lbl_real", L), marker=dict(color=cs.C1, line=dict(width=0)),
                        hovertemplate="%{x} · " + tx("lbl_real", L) + ": %{y:+.0f}<extra></extra>"))
    f4.add_trace(go.Bar(x=etq, y=dcomp, name=tx("lbl_comp", L), marker=dict(color=cs.C4, line=dict(width=0)),
                        hovertemplate="%{x} · " + tx("lbl_comp", L) + ": %{y:+.0f}<extra></extra>"))
    tope = [max(0, r_) + max(0, c_) for r_, c_ in zip(dreal, dcomp)]
    f4.add_trace(go.Scatter(x=etq, y=tope, mode="text", showlegend=False, text=["Total " + num(v_, 0, L, True) for v_ in dnom],
                            textposition="top center", cliponaxis=False, hoverinfo="skip"))
    f4.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    f4.update_layout(barmode="relative", bargap=0.45, hovermode="closest", legend=dict(traceorder="normal"))
    g4 = cs.bloque_grafico(tx("g_desc", L), cs.fig_html(f4, {"notime": True, "noy": True}, "g-cv-descomposicion"), tx("h_desc", L))
    r2 = tx("r_mov", L).format(d1=pb(u["tes_pesos_1y"] - a12["tes_pesos_1y"]), d5=pb(u["tes_pesos_5y"] - a12["tes_pesos_5y"]),
                               d10=pb(u["tes_pesos_10y"] - a12["tes_pesos_10y"]), mov=TX["mov_txt"][mov][k],
                               dr=num(dreal[2], 0, L, True, " pb" if L == "es" else " bp"), db=num(dcomp[2], 0, L, True, " pb" if L == "es" else " bp"))
    s_mov = seccion("cv-movimientos", tx("s_mov", L), r2, f'<div class="grid">{g3}{g4}</div>')

    # ------------------------------------------------ real y compensacion
    reales = [float(u[f"tes_uvr_{p}"]) for p, _ in plazos]
    nomin = [float(u[f"tes_pesos_{p}"]) for p, _ in plazos]
    exacta = [100 * ((1 + n_ / 100) / (1 + r_ / 100) - 1) for n_, r_ in zip(nomin, reales)]
    f5 = cs.base(L, height=330, fecha_x=False)
    f5.add_trace(go.Bar(x=etq, y=[round(r_, 2) for r_ in reales], name=tx("lbl_real", L), marker=dict(color=cs.C1, line=dict(width=0)),
                        text=[pct(r_) for r_ in reales], textposition="inside", hovertemplate="%{x} · " + tx("lbl_real", L) + ": %{y:.2f}%<extra></extra>"))
    f5.add_trace(go.Bar(x=etq, y=[round(n_ - r_, 2) for n_, r_ in zip(nomin, reales)], name=tx("lbl_comp", L),
                        marker=dict(color=cs.C4, line=dict(width=0)), customdata=[pct(e_) for e_ in exacta],
                        text=[pp(n_ - r_, 2, False) for n_, r_ in zip(nomin, reales)], textposition="inside",
                        hovertemplate="%{x} · " + tx("lbl_comp", L) + ": %{y:.2f} pp<br>" + tx("lbl_bei", L) + " (Fisher): %{customdata}<extra></extra>"))
    f5.add_trace(go.Scatter(x=etq, y=nomin, mode="text", text=[pct(n_) for n_ in nomin], textposition="top center", showlegend=False,
                            cliponaxis=False, hoverinfo="skip"))
    f5.update_yaxes(range=[0, max(nomin) * 1.18])
    f5.update_layout(barmode="stack", bargap=0.45, hovermode="closest", legend=dict(traceorder="normal"))
    g5 = cs.bloque_grafico(tx("g_fisher", L), cs.fig_html(f5, {"notime": True, "noy": True}, "g-cv-fisher"), tx("h_fisher", L))
    wr = pd.DataFrame({"real": c["tes_uvr_10y"], "bei": bei10}).resample("W-FRI").last().dropna()
    f6 = cs.base(L, height=330)
    cs.meta_banda(f6, L)
    cs.linea(f6, wr.index, wr["real"], tx("lbl_real", L), cs.C1, width=2.2, lang=L)
    cs.linea(f6, wr.index, wr["bei"], tx("lbl_bei", L), cs.C4, width=2.2, lang=L)
    g6 = cs.bloque_grafico(tx("g_real_hist", L), cs.fig_html(f6, {}, "g-cv-real"), tx("h_real_hist", L))
    r3 = tx("r_real", L).format(n=pct(u["tes_pesos_10y"]), r=pct(u["tes_uvr_10y"]), b=pct(bei10.iloc[-1]), x=num(float(bei10.iloc[-1]) - 3, 1, L))
    s_real = seccion("cv-real", tx("s_real", L), r3, f'<div class="grid">{g5}{g6}</div>')

    # ------------------------------------------------ prima y volatilidad
    wp = pd.DataFrame({"p1": prima1, "p10": prima}).resample("W-FRI").last().dropna()
    f7 = cs.base(L, height=330, suffix=" pp")
    cs.linea(f7, wp.index, wp["p10"], tx("lbl_p10", L), cs.C1, width=2.2, suf=" pp", lang=L)
    cs.linea(f7, wp.index, wp["p1"], tx("lbl_p1", L), cs.C2, width=1.8, suf=" pp", lang=L)
    f7.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    g7 = cs.bloque_grafico(tx("g_prima", L), cs.fig_html(f7, {}, "g-cv-prima"), tx("h_prima", L))
    wv = vol.resample("W-FRI").last().dropna()
    f8 = cs.base(L, height=330, suffix=" pb" if L == "es" else " bp")
    cs.linea(f8, wv.index, wv, tx("lbl_vol", L), cs.C7, width=2.0, fmt=".0f", suf=" pb" if L == "es" else " bp", lang=L)
    f8.add_hline(y=float(vol.mean()), line=dict(color=cs.INK2, width=1, dash="dot"))
    g8 = cs.bloque_grafico(tx("g_vol", L), cs.fig_html(f8, {}, "g-cv-volatilidad"), tx("h_vol", L))
    r4 = tx("r_riesgo", L).format(s=pp(prima.iloc[-1], 2, False), h=pp(prima.mean(), 2, False),
                                  v=num(float(vol.iloc[-1]), 0, L, False, " pb" if L == "es" else " bp"),
                                  cmp=tx("sobre" if vol.iloc[-1] > vol.mean() else "bajo", L),
                                  vh=num(float(vol.mean()), 0, L, False, " pb" if L == "es" else " bp"))
    s_ries = seccion("cv-riesgo", tx("s_riesgo", L), r4, f'<div class="grid">{g7}{g8}</div>')

    items = "".join(f'<li><span class="ref">{ref}</span><span class="ref-u">{es if L == "es" else en}</span></li>' for ref, es, en in LITERATURA)
    s_lit = (f'<section id="cv-literatura" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{tx("s_lit", L)}</h2></div>'
             f'<ol class="refs">{items}</ol></section>')
    return antes, s_fac + s_mov + s_real + s_ries + s_lit


# ====================================================================== ventana explicativa: la curva cero cupon
def ventana_curva(u, bei10, L, num) -> str:
    es = L == "es"
    T = (lambda a, b: a if es else b)
    pct = lambda v: num(float(v), 2, L, False, "%")
    formas = [("normal", T("Normal (creciente)", "Normal (upward)"), "M10 70 C 60 45, 120 30, 230 22",
               T("Los plazos largos pagan más: el mercado pide más por prestar más tiempo.", "Longer maturities pay more: lenders ask more for lending longer.")),
              ("plana", T("Plana", "Flat"), "M10 46 C 80 44, 150 44, 230 43",
               T("Casi la misma tasa en todos los plazos.", "Almost the same rate at every maturity.")),
              ("invertida", T("Invertida", "Inverted"), "M10 22 C 60 40, 120 56, 230 66",
               T("Los plazos cortos pagan más que los largos. La tabla de episodios de esta página muestra cuándo ocurrió en Colombia.", "Short maturities pay more than long ones. The episode table on this page shows when it happened in Colombia."))]
    svgs = "".join(f'<li><svg viewBox="0 0 240 84" aria-hidden="true"><path d="M10 78 H232 M10 6 V78" class="ax"/>'
                   f'<path d="{p}" class="cv"/></svg><b>{t}</b><span>{d}</span></li>' for _, t, p, d in formas)
    return f"""<dialog class="explica" id="exp-curva" aria-labelledby="exp-curva-t">
<div class="ex-cab"><p class="ex-k">{T("Para entender", "To understand")} · Banco de la República</p><h2 id="exp-curva-t">{T("¿Qué es la curva cero cupón de los TES?", "What is the TES zero-coupon curve?")}</h2>
<button type="button" class="ex-x" data-cerrar aria-label="{T("Cerrar", "Close")}">✕</button></div>
<div class="ex-cuerpo">
<p class="ex-lede">{T("Los <b>TES</b> (Títulos de Tesorería) son los bonos con los que el Gobierno nacional se financia en el mercado local. La <b>curva</b> muestra la tasa de interés que el mercado exige al Gobierno para cada plazo: 1, 2, 5, 10 años… Es la referencia sobre la que se valoran los demás activos en pesos.",
 "<b>TES</b> (Treasury Securities) are the bonds the national Government uses to borrow in the local market. The <b>curve</b> shows the interest rate the market demands from the Government at each maturity: 1, 2, 5, 10 years… It is the benchmark against which other peso assets are valued.")}</p>

<h3>{T("1. ¿Por qué «cero cupón»?", "1. Why 'zero coupon'?")}</h3>
<p>{T("La mayoría de los TES pagan intereses cada año (cupones), así que su rendimiento mezcla varios plazos. Una tasa cero cupón es la de un pago único al vencimiento: limpia el efecto de los cupones y permite comparar plazos de forma pura.",
 "Most TES pay interest every year (coupons), so their yield blends several maturities. A zero-coupon rate is that of a single payment at maturity: it strips out the coupon effect and allows a clean comparison of maturities.")}</p>

<h3>{T("2. Cómo la calcula el Banco de la República", "2. How the Banco de la República computes it")}</h3>
<p>{T("El Banco estima cada día la curva con el modelo de Nelson y Siegel (1987), usando las operaciones negociadas y registradas en el SEN (Sistema Electrónico de Negociación del Banco) y en el MEC (Mercado Electrónico de Colombia, de la Bolsa de Valores de Colombia). Publica las tasas a 1, 5 y 10 años, que son las que usa este tablero.",
 "The Bank estimates the curve daily with the Nelson and Siegel (1987) model, using trades negotiated and registered on SEN (the Bank's Electronic Trading System) and MEC (Mercado Electrónico de Colombia, the Colombian Securities Exchange electronic market). It publishes the 1-, 5- and 10-year rates, which are the ones this dashboard uses.")}</p>

<h3>{T("3. Pesos y UVR", "3. Pesos and UVR")}</h3>
<p>{T(f"Hay dos curvas. Los TES en <b>pesos</b> pagan una tasa nominal. Los TES en <b>UVR</b> (Unidad de Valor Real, que se ajusta con la inflación) pagan una tasa <b>real</b>, por encima de la inflación. Hoy, a 10 años: {pct(u['tes_pesos_10y'])} en pesos y {pct(u['tes_uvr_10y'])} en UVR.",
 f"There are two curves. Peso TES pay a nominal rate. <b>UVR</b> TES (Real Value Unit, adjusted for inflation) pay a <b>real</b> rate, above inflation. Today, at 10 years: {pct(u['tes_pesos_10y'])} in pesos and {pct(u['tes_uvr_10y'])} in UVR.")}</p>
<p>{T(f"De la comparación sale la <b>compensación por inflación</b> (ecuación de Fisher): (1 + nominal) / (1 + real) − 1 = {pct(bei10)} a 10 años. No es un pronóstico de inflación: incluye además primas por riesgo inflacionario y por liquidez.",
 f"Comparing them gives <b>inflation compensation</b> (Fisher equation): (1 + nominal) / (1 + real) − 1 = {pct(bei10)} at 10 years. It is not an inflation forecast: it also includes inflation-risk and liquidity premia.")}</p>

<h3>{T("4. Las formas de la curva", "4. Curve shapes")}</h3>
<ul class="ex-formas">{svgs}</ul>

<h3>{T("5. Nivel, pendiente y curvatura", "5. Level, slope and curvature")}</h3>
<p>{T("Casi todo el movimiento de una curva se resume en tres factores (Litterman y Scheinkman, 1991): el <b>nivel</b> (todas las tasas suben o bajan juntas), la <b>pendiente</b> (distancia entre largo y corto plazo) y la <b>curvatura</b> (si la parte media se arquea). En este tablero: nivel = promedio de 1, 5 y 10 años; pendiente = 10 − 1 años; curvatura = 2 × 5 años − 1 − 10 años.",
 "Almost all of a curve's movement is summarised by three factors (Litterman and Scheinkman, 1991): the <b>level</b> (all rates moving together), the <b>slope</b> (distance between long and short end) and the <b>curvature</b> (whether the middle bends). In this dashboard: level = average of 1, 5 and 10 years; slope = 10 − 1 years; curvature = 2 × 5 years − 1 − 10 years.")}</p>

<h3>{T("Fuentes oficiales", "Official sources")}</h3>
<ul class="ex-fuentes">
<li><a href="https://suameca.banrep.gov.co/estadisticas-economicas/informacionSerie/640001/deuda_publica_tasas_cero_cupon_tes" target="_blank" rel="noopener">Banco de la República — {T("Tasas cero cupón TES (descripción de la serie)", "TES zero-coupon rates (series description)")}</a></li>
<li>Arango, L. E., Melo, L. F. y Vásquez, D. M. (2002). <i>Estimación de la estructura a plazo de las tasas de interés en Colombia</i>. Borradores de Economía 196, Banco de la República.</li>
<li>Nelson, C. R. y Siegel, A. F. (1987). Parsimonious Modeling of Yield Curves. <i>Journal of Business</i>, 60(4).</li>
<li>Fisher, I. (1930). <i>The Theory of Interest</i>.</li>
</ul>
</div></dialog>"""
