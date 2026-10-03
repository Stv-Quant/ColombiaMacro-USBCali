"""Pagina del peso colombiano (v12.13): ocho medidas, el peso frente al dolar global y a sus pares, el peso
frente a otras monedas, tasa de cambio real (multilateral, de competitividad y bilateral), petroleo y
terminos de intercambio, flujos de la balanza cambiaria y reservas, volatilidad, ventana explicativa y
literatura.

Solo datos observados: TRM (Superintendencia Financiera, via BanRep), tasas de cambio, ITCR, balanza
cambiaria y subastas de reservas (Banco de la Republica), indice amplio del dolar y peso mexicano (Reserva
Federal, H.10) y Brent (EIA), estos tres via FRED.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

TX = {
    "s_medidas": ("El peso en ocho medidas", "The peso in eight measures"),
    "s_global": ("¿Es el peso o es el dólar?", "Is it the peso or the dollar?"),
    "s_monedas": ("El peso frente a otras monedas", "The peso against other currencies"),
    "s_real": ("Tasa de cambio real: ¿el peso está caro o barato?", "Real exchange rate: is the peso expensive or cheap?"),
    "s_petroleo": ("Petróleo y términos de intercambio", "Oil and terms of trade"),
    "s_flujos": ("¿Entran o salen dólares?", "Are dollars coming in or going out?"),
    "s_vol": ("¿Qué tan volátil es el peso?", "How volatile is the peso?"),
    "s_lit": ("Bases metodológicas y literatura", "Methodological basis and literature"),
    # lecturas
    "l_trm": ("Dólar (TRM) · {f}", "Dollar (TRM) · {f}"), "l_trm_d": ("en 12 meses {v} · hace un año ${a}", "over 12 months {v} · a year ago ${a}"),
    "l_eur": ("Euro en pesos", "Euro in pesos"), "l_eur_d": ("en 12 meses {v}", "over 12 months {v}"),
    "l_pares": ("Peso frente a sus vecinos", "Peso against its peers"), "l_pares_d": ("COP {c} · real, peso mexicano y sol {p} en promedio (12 meses)", "COP {c} · real, Mexican peso and sol {p} on average (12 months)"),
    "l_dxy": ("Dólar global (Reserva Federal)", "Global dollar (Federal Reserve)"), "l_dxy_d": ("frente a 26 monedas · 12 meses", "against 26 currencies · 12 months"),
    "l_itcr": ("Tasa de cambio real (ITCR)", "Real exchange rate (ITCR)"), "l_itcr_d": ("2010 = 100 · promedio desde 2000: {v}", "2010 = 100 · average since 2000: {v}"),
    "l_brent": ("Petróleo Brent", "Brent oil"), "l_brent_d": ("dólares por barril · 12 meses {v}", "dollars per barrel · 12 months {v}"),
    "l_vol": ("Volatilidad del peso", "Peso volatility"), "l_vol_d": ("anualizada, 60 días · promedio {v}", "annualised, 60 days · average {v}"),
    "l_res": ("Reservas internacionales netas", "Net international reserves"), "l_res_d": ("{f} · opciones PUT subastadas en {a}: US${p} millones", "{f} · PUT options auctioned in {a}: US${p} million"),
    "l_res_d0": ("{f}", "{f}"),
    # respuestas
    "r_medidas": ("Un dólar cuesta ${t} pesos: el peso se {dir} {v} en 12 meses. En el mismo lapso el dólar global cambió {g} y las monedas vecinas (real, peso mexicano y sol) {p} en promedio: "
                  "{lectura} La tasa de cambio real está en {r} (2010 = 100), {rr} su promedio desde 2000.",
                  "One dollar costs ${t} pesos: the peso {dir_en} {v} over 12 months. Over the same period the global dollar changed {g} and peer currencies (real, Mexican peso and sol) {p} on average: "
                  "{lectura} The real exchange rate stands at {r} (2010 = 100), {rr} its average since 2000."),
    "dir_fort": ("fortaleció", "strengthened"), "dir_deb": ("debilitó", "weakened"),
    "lec_propio": ("el movimiento del peso es sobre todo propio de Colombia.", "the peso's move is mostly specific to Colombia."),
    "lec_global": ("el peso se movió en línea con el dólar y sus vecinos.", "the peso moved in line with the dollar and its peers."),
    "bajo": ("por debajo de", "below"), "sobre": ("por encima de", "above"),
    "r_global": ("En 12 meses el peso colombiano {c} frente al dólar, el real brasileño {b}, el peso mexicano {m} y el sol peruano {s}; el dólar se movió {g} frente a 26 monedas. "
                 "La diferencia entre el peso y el promedio de sus vecinos es {x} pp. Desde 2008, la correlación entre los cambios anuales de la TRM y del dólar global es {k}.",
                 "Over 12 months the Colombian peso moved {c} against the dollar, the Brazilian real {b}, the Mexican peso {m} and the Peruvian sol {s}; the dollar moved {g} against 26 currencies. "
                 "The gap between the peso and its peers' average is {x} pp. Since 2008, the correlation between annual changes in the TRM and the global dollar is {k}."),
    "r_monedas": ("En 12 meses el peso {dir} frente a {n} de las {t} monedas: {lista}. Signo negativo = se necesitan menos pesos para comprar esa moneda.",
                  "Over 12 months the peso {dir} against {n} of the {t} currencies: {lista}. A negative sign = fewer pesos are needed to buy that currency."),
    "dir_gana": ("se fortaleció", "strengthened"), "dir_pierde": ("se debilitó", "weakened"),
    "r_real": ("El ITCR (ponderado por el comercio total, deflactado con el IPC) está en {r}, {d} frente a su promedio desde 2000. "
               "El índice de competitividad en Estados Unidos (ITCR-C) está en {c}. Frente a su promedio, el ITCR bilateral va de {v1} con {p1} a {v2} con {p2} (negativo = peso más caro).",
               "The ITCR (weighted by total trade, deflated with CPI) stands at {r}, {d} against its average since 2000. "
               "The competitiveness index in the US market (ITCR-C) is {c}. Relative to its average, the bilateral ITCR ranges from {v1} with {p1} to {v2} with {p2} (negative = more expensive peso)."),
    "r_petroleo": ("El Brent cuesta US${b} por barril ({bc} en 12 meses) y los términos de intercambio cambiaron {ti} en un año. "
                   "En los últimos 12 meses la correlación semanal entre la TRM y el Brent fue {k1} y en los últimos 10 años {k10}: cuando el petróleo sube, el peso tiende a fortalecerse, pero el vínculo es parcial.",
                   "Brent costs US${b} per barrel ({bc} over 12 months) and the terms of trade changed {ti} in a year. "
                   "Over the last 12 months the weekly correlation between the TRM and Brent was {k1} and over the last 10 years {k10}: when oil rises the peso tends to strengthen, but the link is partial."),
    "r_flujos": ("En los últimos 12 meses la balanza cambiaria registró {cc} por cuenta corriente y {cap} por movimientos de capital; las reservas brutas cambiaron {res}. "
                 "Las reservas internacionales netas suman US${rn} millones.",
                 "Over the last 12 months the foreign-exchange balance recorded {cc} on current account and {cap} in capital movements; gross reserves changed {res}. "
                 "Net international reserves total US${rn} million."),
    "r_vol": ("La volatilidad anualizada del peso en los últimos 60 días es {v} ({cmp} su promedio de {vh}). Hoy el real brasileño tiene {b} y el peso mexicano {m}.",
              "The peso's annualised volatility over the last 60 days is {v} ({cmp} its average of {vh}). Today the Brazilian real has {b} and the Mexican peso {m}."),
    "mayor": ("por encima de", "above"), "menor": ("por debajo de", "below"),
    # graficos
    "g_pares": ("Cambio frente al dólar en 12 meses", "Change against the dollar over 12 months"),
    "h_pares": ("Variación de las unidades de cada moneda por dólar: positivo = la moneda se debilita. «Dólar global» es el índice amplio de la Reserva Federal (positivo = el dólar se fortalece).",
                "Change in units of each currency per dollar: positive = the currency weakens. 'Global dollar' is the Federal Reserve broad index (positive = the dollar strengthens)."),
    "g_co": ("TRM y dólar global: cambio anual", "TRM and global dollar: annual change"),
    "h_co": ("Variación en 12 meses. Si las dos líneas se mueven juntas, el peso sigue al dólar en el mundo; si se separan, pesan más los factores de Colombia.",
             "12-month change. When both lines move together the peso follows the dollar worldwide; when they diverge, Colombian factors weigh more."),
    "lbl_trm": ("TRM", "TRM"), "lbl_dxy": ("Dólar global", "Global dollar"),
    "g_idx": ("Pesos por cada moneda (índice)", "Pesos per unit of each currency (index)"),
    "h_idx": ("Cuántos pesos cuesta cada moneda, con base 100 al inicio del horizonte elegido. Si la línea sube, el peso se debilita frente a esa moneda.",
              "How many pesos each currency costs, indexed to 100 at the start of the chosen horizon. If the line rises, the peso weakens against that currency."),
    "g_cruces": ("El peso frente a cada moneda: cambio en 12 meses", "The peso against each currency: 12-month change"),
    "h_cruces": ("Variación de los pesos necesarios para comprar una unidad de cada moneda. Negativo (verde) = el peso se fortalece.",
                 "Change in pesos needed to buy one unit of each currency. Negative (green) = the peso strengthens."),
    "g_itcr": ("Tasa de cambio real multilateral", "Multilateral real exchange rate"),
    "h_itcr": ("ITCR deflactado con IPC y ponderado por comercio total, e ITCR-C (competitividad frente a otros exportadores en Estados Unidos). Sube = el peso se abarata en términos reales.",
               "ITCR deflated with CPI and weighted by total trade, and ITCR-C (competitiveness against other exporters in the US market). Up = the peso becomes cheaper in real terms."),
    "lbl_itcr": ("ITCR (IPC, comercio total)", "ITCR (CPI, total trade)"), "lbl_itcrc": ("ITCR-C (Estados Unidos)", "ITCR-C (US market)"),
    "g_bil": ("Tasa de cambio real bilateral frente a su promedio", "Bilateral real exchange rate versus its average"),
    "h_bil": ("Distancia del ITCR bilateral (deflactado con IPP) frente a su promedio desde 2000. Negativo = el peso está más caro que su promedio frente a ese país.",
              "Distance of the bilateral ITCR (deflated with PPI) from its average since 2000. Negative = the peso is more expensive than its average against that country."),
    "g_brent": ("Petróleo Brent y TRM (índice)", "Brent oil and TRM (index)"),
    "h_brent": ("Base 100 al inicio del horizonte elegido. El peso suele fortalecerse (TRM baja) cuando el petróleo sube: el crudo es la principal exportación de Colombia.",
                "Indexed to 100 at the start of the chosen horizon. The peso tends to strengthen (TRM falls) when oil rises: crude is Colombia's main export."),
    "lbl_brent": ("Brent", "Brent"),
    "g_corr": ("Correlación TRM–Brent y TRM–dólar global (52 semanas)", "TRM–Brent and TRM–global dollar correlation (52 weeks)"),
    "h_corr": ("Correlación móvil de 52 semanas entre los cambios semanales de la TRM y del Brent o del dólar global. Negativa con el Brent: cuando el petróleo sube, la TRM baja.",
               "52-week rolling correlation between weekly changes in the TRM and Brent or the global dollar. Negative with Brent: when oil rises, the TRM falls."),
    "lbl_c_brent": ("TRM y Brent", "TRM and Brent"), "lbl_c_dxy": ("TRM y dólar global", "TRM and global dollar"),
    "g_bc": ("Balanza cambiaria: suma de 12 meses", "Foreign-exchange balance: 12-month sum"),
    "h_bc": ("Dólares que entraron (+) o salieron (−) por el mercado cambiario, en miles de millones de dólares. La cuenta corriente incluye exportaciones, importaciones, servicios y remesas canalizadas.",
             "Dollars that came in (+) or went out (−) through the FX market, in billions of dollars. The current account includes exports, imports, services and remittances channelled through the market."),
    "lbl_cc": ("Cuenta corriente", "Current account"), "lbl_cap": ("Movimientos de capital", "Capital movements"), "lbl_res": ("Variación de reservas", "Change in reserves"),
    "g_res": ("Reservas internacionales netas y compras de reservas", "Net international reserves and reserve purchases"),
    "h_res": ("Línea: reservas internacionales netas (miles de millones de dólares). Barras: monto de opciones PUT subastadas cada año para acumular reservas.",
              "Line: net international reserves (billions of dollars). Bars: amount of PUT options auctioned each year to accumulate reserves."),
    "lbl_rn": ("Reservas netas", "Net reserves"), "lbl_put": ("Opciones PUT subastadas", "PUT options auctioned"),
    "g_vol": ("Volatilidad del peso y de sus vecinos", "Volatility of the peso and its peers"),
    "h_vol": ("Desviación estándar de los cambios diarios de 60 días hábiles, anualizada (× √252), en porcentaje.",
              "Standard deviation of daily changes over 60 business days, annualised (× √252), in percent."),
    "mon": {"usd": ("Dólar", "US dollar"), "eur": ("Euro", "Euro"), "gbp": ("Libra", "Pound"), "jpy": ("Yen", "Yen"), "cny": ("Yuan", "Yuan"),
            "brl": ("Real brasileño", "Brazilian real"), "mxn": ("Peso mexicano", "Mexican peso"), "pen": ("Sol peruano", "Peruvian sol"),
            "cop": ("Peso colombiano", "Colombian peso"), "dxy": ("Dólar global", "Global dollar")},
    "pais": {"eeuu": ("Estados Unidos", "United States"), "china": ("China", "China"), "brasil": ("Brasil", "Brazil"), "mexico": ("México", "Mexico")},
}
LITERATURA = [
    ("Dornbusch, R. (1976). Expectations and Exchange Rate Dynamics. <i>Journal of Political Economy</i>, 84(6), 1161–1176.",
     "Por qué la tasa de cambio reacciona más que otros precios ante choques monetarios.", "Why the exchange rate overreacts to monetary shocks."),
    ("Meese, R. A. y Rogoff, K. (1983). Empirical Exchange Rate Models of the Seventies: Do They Fit Out of Sample? <i>Journal of International Economics</i>, 14(1–2), 3–24.",
     "La tasa de cambio es difícil de anticipar: por eso este tablero solo muestra datos observados.", "Exchange rates are hard to anticipate: this is why the dashboard shows only observed data."),
    ("Rogoff, K. (1996). The Purchasing Power Parity Puzzle. <i>Journal of Economic Literature</i>, 34(2), 647–668.",
     "La tasa de cambio real y la paridad del poder adquisitivo.", "The real exchange rate and purchasing power parity."),
    ("Chen, Y.-C. y Rogoff, K. (2003). Commodity Currencies. <i>Journal of International Economics</i>, 60(1), 133–160.",
     "Monedas de países exportadores de materias primas y su vínculo con esos precios.", "Currencies of commodity exporters and their link to commodity prices."),
    ("Rey, H. (2013). Dilemma not Trilemma: The Global Financial Cycle and Monetary Policy Independence. <i>Jackson Hole Economic Symposium</i>, Federal Reserve Bank of Kansas City.",
     "El dólar y el ciclo financiero global mueven a las monedas emergentes.", "The dollar and the global financial cycle move emerging-market currencies."),
    ("Banco de la República. Metodología de cálculo del Índice de Tasa de Cambio Real (ITCR) de Colombia.",
     "Definición del ITCR, deflactores, ponderaciones y socios comerciales.", "Definition of the ITCR, deflators, weights and trading partners."),
    ("Superintendencia Financiera de Colombia. Tasa de cambio representativa del mercado: antecedentes normativos y metodología.",
     "Cómo se calcula y certifica la TRM.", "How the TRM is calculated and certified."),
]


def tx(k, L):
    return TX[k][0 if L == "es" else 1]


def cambio(s: pd.Series, meses: int = 12) -> float:
    """Variacion porcentual del ultimo dato frente al ultimo disponible hace `meses`."""
    s = s.dropna()
    ref = s.loc[:s.index[-1] - pd.DateOffset(months=meses)]
    return float((s.iloc[-1] / ref.iloc[-1] - 1) * 100) if len(ref) else np.nan


def volatilidad(s: pd.Series, ventana: int = 60) -> pd.Series:
    """Volatilidad anualizada (%) de los cambios logaritmicos diarios."""
    return np.log(s.dropna()).diff().rolling(ventana, min_periods=int(ventana * 0.8)).std() * np.sqrt(252) * 100


def correlacion_movil(a: pd.Series, b: pd.Series, semanas: int = 52) -> pd.Series:
    w = pd.DataFrame({"a": a, "b": b}).resample("W-FRI").last().pct_change(fill_method=None).dropna()
    return w["a"].rolling(semanas, min_periods=int(semanas * 0.8)).corr(w["b"])


def construir_cambio(d, L):
    """Devuelve (antes, despues)."""
    from colombiamacro.fuentes import cambiario as cb
    from colombiamacro.sitio import construir as cs
    num, fecha = cs.num, cs.fecha
    cs.LANG_ACTUAL[0] = L
    k = 0 if L == "es" else 1
    C = cb.cargar()
    if C is None or d.extra["trm"].empty:
        return "", ""
    pct = lambda v, dec=1, sg=True: num(float(v), dec, L, sg, "%")
    mon = lambda c: TX["mon"][c][k]
    trm = d.extra["trm"].set_index("fecha")["trm"].sort_index()
    hoy = trm.index[-1]
    cop12 = cambio(trm)
    pares = {"brl": C["brl_usd"], "mxn": C["mxn_usd"], "pen": C["pen_usd"]}
    p12 = {c: cambio(s) for c, s in pares.items()}
    prom_p = float(np.mean(list(p12.values())))
    dxy12 = cambio(C["dolar_global"])
    propio = abs(cop12 - prom_p) > max(3.0, abs(prom_p))
    it = d.extra["itcr_ipc"].set_index("fecha")["itcr_ipc"].sort_index()
    it_prom = float(it.loc["2000":].mean())
    vol = volatilidad(trm).dropna()
    res = d.extra["reservas_netas_musd"].set_index("fecha")["reservas_netas_musd"].sort_index()
    put = C["put_acumulacion"]
    put_a = put.groupby(put.index.year).sum() / 1e6
    ff = fecha(hoy, "d", L)

    def seccion(sid, titulo, resp, cuerpo):
        return (f'<section id="{sid}" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{titulo}</h2></div>'
                f'{cs.respuesta_html(resp, L)}{cuerpo}</section>')

    def lec(kk, v, dsc, tono, href):
        return (f'<a class="lec {tono}" href="{href}"><span class="lec-k">{kk}</span><b class="lec-v">{v}</b>'
                f'<span class="lec-d">{dsc}</span></a>')

    trm_hace = trm.loc[:hoy - pd.DateOffset(years=1)].iloc[-1]
    ult_put = int(put.index[-1].year) if len(put) else None
    res_d = (tx("l_res_d", L).format(f=fecha(res.index[-1], "m", L), a=ult_put, p=num(float(put_a.loc[ult_put]), 0, L))
             if ult_put and ult_put >= hoy.year - 1 else tx("l_res_d0", L).format(f=fecha(res.index[-1], "m", L)))
    tiles = [
        lec(tx("l_trm", L).format(f=ff), "$" + num(float(trm.iloc[-1]), 0, L), tx("l_trm_d", L).format(v=pct(cop12), a=num(float(trm_hace), 0, L)), "", "#mercados"),
        lec(tx("l_eur", L), "$" + num(float(C["cop_eur"].iloc[-1]), 0, L), tx("l_eur_d", L).format(v=pct(cambio(C["cop_eur"]))), "", "#tc-monedas"),
        lec(tx("l_pares", L), num(cop12 - prom_p, 1, L, True, " pp"), tx("l_pares_d", L).format(c=pct(cop12), p=pct(prom_p)), "warn" if propio else "", "#tc-global"),
        lec(tx("l_dxy", L), pct(dxy12), tx("l_dxy_d", L), "", "#tc-global"),
        lec(tx("l_itcr", L), num(float(it.iloc[-1]), 1, L), tx("l_itcr_d", L).format(v=num(it_prom, 1, L)), "", "#tc-real"),
        lec(tx("l_brent", L), "US$" + num(float(C["brent"].iloc[-1]), 1, L), tx("l_brent_d", L).format(v=pct(cambio(C["brent"]))), "", "#tc-petroleo"),
        lec(tx("l_vol", L), pct(vol.iloc[-1], 1, False), tx("l_vol_d", L).format(v=pct(vol.mean(), 1, False)), "warn" if vol.iloc[-1] > vol.quantile(0.8) else "", "#tc-vol"),
        lec(tx("l_res", L), "US$" + num(float(res.iloc[-1]) / 1000, 1, L) + (" mil M" if L == "es" else " bn"), res_d, "", "#tc-flujos"),
    ]
    r0 = tx("r_medidas", L).format(t=num(float(trm.iloc[-1]), 0, L), dir=tx("dir_fort" if cop12 < 0 else "dir_deb", L),
                                   dir_en=TX["dir_fort"][1] if cop12 < 0 else TX["dir_deb"][1], v=pct(abs(cop12), 1, False),
                                   g=pct(dxy12), p=pct(prom_p), lectura=tx("lec_propio" if propio else "lec_global", L),
                                   r=num(float(it.iloc[-1]), 1, L), rr=tx("bajo" if it.iloc[-1] < it_prom else "sobre", L))
    antes = seccion("tc-medidas", tx("s_medidas", L), r0, f'<div class="lecturas ocho">{"".join(tiles)}</div>')

    # ------------------------------------------------ peso vs dolar global y pares
    orden = [("cop", cop12), ("brl", p12["brl"]), ("mxn", p12["mxn"]), ("pen", p12["pen"]), ("dxy", dxy12)]
    f1 = cs.base(L, height=330, fecha_x=False)
    f1.add_trace(go.Bar(x=[mon(c) for c, _ in orden], y=[round(v, 2) for _, v in orden], showlegend=False,
                        marker=dict(color=[cs.C2 if c == "cop" else (cs.C7 if c == "dxy" else cs.C1) for c, _ in orden], line=dict(width=0)),
                        text=[pct(v) for _, v in orden], textposition="outside", cliponaxis=False, hovertemplate="%{x}: %{y:+.1f}%<extra></extra>"))
    f1.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    lo, hi = min(v for _, v in orden), max(v for _, v in orden)
    f1.update_yaxes(range=[min(0, lo) * 1.25 - 1, max(0, hi) * 1.25 + 1])
    f1.update_layout(bargap=0.4, hovermode="closest")
    q_btn = (f'<button type="button" class="ex-q" data-dialog="exp-peso" aria-haspopup="dialog" '
             f'title="{"¿Cómo se calcula la TRM y qué es la tasa de cambio real?" if L == "es" else "How is the TRM computed and what is the real exchange rate?"}">?</button>')
    g1 = cs.bloque_grafico(tx("g_pares", L), cs.fig_html(f1, {"notime": True, "noy": True}, "g-tc-pares"), tx("h_pares", L))
    co = pd.DataFrame({"trm": trm, "dxy": C["dolar_global"]}).resample("W-FRI").last()
    co12 = (co / co.shift(52) - 1).mul(100).dropna()
    f2 = cs.base(L, height=330)
    cs.linea(f2, co12.index, co12["trm"], tx("lbl_trm", L), cs.C2, width=2.2, lang=L)
    cs.linea(f2, co12.index, co12["dxy"], tx("lbl_dxy", L), cs.C7, width=2.0, lang=L)
    f2.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    g2 = cs.bloque_grafico(tx("g_co", L), cs.fig_html(f2, {}, "g-tc-dolar-global"), tx("h_co", L))
    k_dxy = float(co12["trm"].corr(co12["dxy"]))
    r1 = tx("r_global", L).format(c=pct(cop12), b=pct(p12["brl"]), m=pct(p12["mxn"]), s=pct(p12["pen"]), g=pct(dxy12),
                                  x=num(cop12 - prom_p, 1, L, True), k=num(k_dxy, 2, L))
    s_glob = seccion("tc-global", tx("s_global", L), r1, f'<div class="grid">{g1}{g2}</div>')

    # ------------------------------------------------ otras monedas
    cruces = {"usd": trm, "eur": C["cop_eur"], "gbp": C["cop_gbp"], "jpy": C["cop_jpy"], "cny": C["cop_cny"],
              "brl": (trm / C["brl_usd"].reindex(trm.index, method="ffill")).dropna(),
              "mxn": (trm / C["mxn_usd"].reindex(trm.index, method="ffill")).dropna(),
              "pen": (trm / C["pen_usd"].reindex(trm.index, method="ffill")).dropna()}
    wi = pd.DataFrame({c: s for c, s in cruces.items() if c in ("usd", "eur", "cny", "brl", "mxn")}).loc["2009":].resample("W-FRI").last().dropna()
    f3 = cs.base(L, height=340, suffix="")
    for (c, col), w_ in zip([("usd", cs.C2), ("eur", cs.C1), ("cny", cs.C4), ("brl", cs.C3), ("mxn", cs.C7)], (2.6, 2, 1.8, 1.8, 1.8)):
        cs.linea(f3, wi.index, wi[c], mon(c), col, width=w_, fmt=".1f", suf="", lang=L)
    g3 = cs.bloque_grafico(tx("g_idx", L), cs.fig_html(f3, {"rebase": True}, "g-tc-monedas"), tx("h_idx", L))
    cc = sorted(((c, cambio(s)) for c, s in cruces.items()), key=lambda x: x[1])
    f4 = cs.base(L, height=360, fecha_x=False)
    f4.add_trace(go.Bar(y=[mon(c) for c, _ in cc], x=[round(v, 2) for _, v in cc], orientation="h", showlegend=False,
                        marker=dict(color=[cs.C3 if v < 0 else cs.C2 for _, v in cc], line=dict(width=0)),
                        text=[pct(v) for _, v in cc], textposition="outside", cliponaxis=False, hovertemplate="%{y}: %{x:+.1f}%<extra></extra>"))
    f4.add_vline(x=0, line=dict(color=cs.INK2, width=1))
    f4.update_xaxes(range=[min(0, cc[0][1]) * 1.3 - 1, max(0, cc[-1][1]) * 1.3 + 1], showgrid=True, gridcolor=cs.GRID)
    f4.update_yaxes(ticksuffix="", tickfont=dict(size=12, color=cs.INK2))
    f4.update_layout(bargap=0.3, hovermode="closest")
    g4 = cs.bloque_grafico(tx("g_cruces", L), cs.fig_html(f4, {"notime": True, "noy": True}, "g-tc-cruces"), tx("h_cruces", L))
    gana = [x for x in cc if x[1] < 0]
    sel = gana if len(gana) >= len(cc) / 2 else [x for x in cc if x[1] >= 0]
    lista = ", ".join(f"{mon(c).lower() if L == 'es' else mon(c)} ({pct(v)})" for c, v in sel)
    r2 = tx("r_monedas", L).format(dir=tx("dir_gana" if sel is gana else "dir_pierde", L), n=len(sel), t=len(cc), lista=lista)
    s_mon = seccion("tc-monedas", tx("s_monedas", L), r2, f'<div class="grid">{g3}{g4}</div>')

    # ------------------------------------------------ tasa de cambio real
    itc = C["itcr_c"]
    wr = pd.DataFrame({"itcr": it, "itcr_c": itc}).loc["2000":].dropna(how="all")
    xm = wr.index + pd.offsets.MonthEnd(0)
    f5 = cs.base(L, height=340, suffix="")
    cs.linea(f5, xm, wr["itcr"], tx("lbl_itcr", L), cs.C1, width=2.4, fmt=".1f", suf="", lang=L)
    cs.linea(f5, xm, wr["itcr_c"], tx("lbl_itcrc", L), cs.C4, width=1.8, fmt=".1f", suf="", lang=L)
    f5.add_hline(y=100, line=dict(color=cs.INK2, width=1))
    f5.add_hline(y=it_prom, line=dict(color=cs.C1, width=1, dash="dot"))
    g5 = cs.bloque_grafico(tx("g_itcr", L), cs.fig_html(f5, {}, "g-tc-itcr"), tx("h_itcr", L))
    g5 = g5.replace("</figcaption>", f" {q_btn}</figcaption>", 1)
    bil = {p: (float(C[f"itcr_{p}"].iloc[-1]) / float(C[f"itcr_{p}"].loc["2000":].mean()) - 1) * 100 for p in ("eeuu", "china", "brasil", "mexico")}
    bo = sorted(bil.items(), key=lambda x: x[1])
    f6 = cs.base(L, height=300, fecha_x=False)
    f6.add_trace(go.Bar(y=[TX["pais"][p][k] for p, _ in bo], x=[round(v, 1) for _, v in bo], orientation="h", showlegend=False,
                        marker=dict(color=[cs.C2 if v < 0 else cs.C1 for _, v in bo], line=dict(width=0)),
                        text=[pct(v) for _, v in bo], textposition="outside", cliponaxis=False, hovertemplate="%{y}: %{x:+.1f}%<extra></extra>"))
    f6.add_vline(x=0, line=dict(color=cs.INK2, width=1))
    f6.update_xaxes(range=[min(0, bo[0][1]) * 1.35 - 2, max(0, bo[-1][1]) * 1.35 + 2], showgrid=True, gridcolor=cs.GRID)
    f6.update_yaxes(ticksuffix="", tickfont=dict(size=12, color=cs.INK2))
    f6.update_layout(bargap=0.35, hovermode="closest")
    g6 = cs.bloque_grafico(tx("g_bil", L), cs.fig_html(f6, {"notime": True, "noy": True}, "g-tc-bilateral"), tx("h_bil", L))
    p1, p2 = bo[0], bo[-1]
    r3 = tx("r_real", L).format(r=num(float(it.iloc[-1]), 1, L), d=pct((float(it.iloc[-1]) / it_prom - 1) * 100), c=num(float(itc.iloc[-1]), 1, L),
                                p1=TX["pais"][p1[0]][k], v1=pct(p1[1]), p2=TX["pais"][p2[0]][k], v2=pct(p2[1]))
    s_real = seccion("tc-real", tx("s_real", L), r3, f'<div class="grid">{g5}{g6}</div>') + ventana_peso(trm, it, L, num, fecha)

    # ------------------------------------------------ petroleo y terminos de intercambio
    wb = pd.DataFrame({"brent": C["brent"], "trm": trm}).loc["2008":].resample("W-FRI").last().dropna()
    f7 = cs.base(L, height=340, suffix="")
    cs.linea(f7, wb.index, wb["brent"], tx("lbl_brent", L), cs.C4, width=2.0, fmt=".1f", suf="", lang=L)
    cs.linea(f7, wb.index, wb["trm"], tx("lbl_trm", L), cs.C2, width=2.2, fmt=".1f", suf="", lang=L)
    g7 = cs.bloque_grafico(tx("g_brent", L), cs.fig_html(f7, {"rebase": True}, "g-tc-brent"), tx("h_brent", L))
    cb_ = correlacion_movil(trm, C["brent"]).dropna()
    cd_ = correlacion_movil(trm, C["dolar_global"]).dropna()
    f8 = cs.base(L, height=340, suffix="")
    cs.linea(f8, cb_.index, cb_, tx("lbl_c_brent", L), cs.C4, width=2.0, fmt=".2f", suf="", lang=L)
    cs.linea(f8, cd_.index, cd_, tx("lbl_c_dxy", L), cs.C7, width=2.0, fmt=".2f", suf="", lang=L)
    f8.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    f8.update_yaxes(range=[-1, 1])
    g8 = cs.bloque_grafico(tx("g_corr", L), cs.fig_html(f8, {"noy": True}, "g-tc-correlacion"), tx("h_corr", L))
    wk = pd.DataFrame({"t": trm, "b": C["brent"]}).resample("W-FRI").last().pct_change(fill_method=None).dropna()
    k1 = float(wk.loc[wk.index[-1] - pd.DateOffset(years=1):].corr().iloc[0, 1])
    k10 = float(wk.loc[wk.index[-1] - pd.DateOffset(years=10):].corr().iloc[0, 1])
    ti = d.extra["terminos_intercambio"].set_index("fecha")["terminos_intercambio"].sort_index()
    r4 = tx("r_petroleo", L).format(b=num(float(C["brent"].iloc[-1]), 1, L), bc=pct(cambio(C["brent"])), ti=pct(cambio(ti)),
                                    k1=num(k1, 2, L), k10=num(k10, 2, L))
    s_pet = seccion("tc-petroleo", tx("s_petroleo", L), r4, f'<div class="grid">{g7}{g8}</div>')

    # ------------------------------------------------ flujos y reservas
    bc = pd.DataFrame({c: C[c] for c in ("bc_cuenta_corriente", "bc_capital", "bc_reservas")}).sort_index()
    b12 = bc.rolling(12).sum().dropna() / 1000
    xb = b12.index + pd.offsets.MonthEnd(0)
    f9 = cs.base(L, height=340, suffix="")
    for col, lbl, color, w_ in (("bc_cuenta_corriente", "lbl_cc", cs.C1, 2.2), ("bc_capital", "lbl_cap", cs.C2, 2.2), ("bc_reservas", "lbl_res", cs.C3, 1.8)):
        cs.linea(f9, xb, b12[col], tx(lbl, L), color, width=w_, fmt=".1f", suf=" mil M" if L == "es" else " bn", lang=L)
    f9.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    g9 = cs.bloque_grafico(tx("g_bc", L), cs.fig_html(f9, {}, "g-tc-balanza"), tx("h_bc", L))
    f10 = cs.base(L, height=340, suffix="")
    rr = (res.loc["2000":] / 1000)
    f10.add_trace(go.Bar(x=[pd.Timestamp(int(a), 12, 31) for a in put_a.index if a >= 2000], y=[round(v / 1000, 2) for a, v in put_a.items() if a >= 2000],
                         name=tx("lbl_put", L), marker=dict(color=cs.C4, line=dict(width=0)), width=1000 * 3600 * 24 * 200,
                         hovertemplate="%{x|%Y}: US$%{y:.2f} " + ("mil M" if L == "es" else "bn") + "<extra></extra>"))
    cs.linea(f10, rr.index + pd.offsets.MonthEnd(0), rr, tx("lbl_rn", L), cs.C1, width=2.4, fmt=".1f", suf=" mil M" if L == "es" else " bn", lang=L)
    g10 = cs.bloque_grafico(tx("g_res", L), cs.fig_html(f10, {}, "g-tc-reservas"), tx("h_res", L))
    u12 = bc.tail(12).sum()
    usd = lambda v: ("+" if v >= 0 else "−") + "US$" + num(abs(float(v)), 0, L) + (" millones" if L == "es" else " million")
    r5 = tx("r_flujos", L).format(cc=usd(u12["bc_cuenta_corriente"]), cap=usd(u12["bc_capital"]), res=usd(u12["bc_reservas"]),
                                  rn=num(float(res.iloc[-1]), 0, L))
    s_flu = seccion("tc-flujos", tx("s_flujos", L), r5, f'<div class="grid">{g9}{g10}</div>')

    # ------------------------------------------------ volatilidad
    vb = volatilidad(C["brl_usd"]).dropna()
    vm = volatilidad(C["mxn_usd"]).dropna()
    wv = pd.DataFrame({"cop": vol, "brl": vb, "mxn": vm}).loc["2008":].resample("W-FRI").last()
    f11 = cs.base(L, height=330)
    cs.linea(f11, wv.index, wv["cop"], mon("cop"), cs.C2, width=2.4, lang=L)
    cs.linea(f11, wv.index, wv["brl"], mon("brl"), cs.C3, width=1.6, lang=L)
    cs.linea(f11, wv.index, wv["mxn"], mon("mxn"), cs.C7, width=1.6, lang=L)
    g11 = cs.bloque_grafico(tx("g_vol", L), cs.fig_html(f11, {}, "g-tc-volatilidad"), tx("h_vol", L), ancho=True)
    r6 = tx("r_vol", L).format(v=pct(vol.iloc[-1], 1, False), cmp=tx("mayor" if vol.iloc[-1] > vol.mean() else "menor", L),
                               vh=pct(vol.mean(), 1, False), b=pct(vb.iloc[-1], 1, False), m=pct(vm.iloc[-1], 1, False))
    s_vol = seccion("tc-vol", tx("s_vol", L), r6, f'<div class="grid">{g11}</div>')

    items = "".join(f'<li><span class="ref">{ref}</span><span class="ref-u">{es if L == "es" else en}</span></li>' for ref, es, en in LITERATURA)
    s_lit = (f'<section id="tc-literatura" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{tx("s_lit", L)}</h2></div>'
             f'<ol class="refs">{items}</ol></section>')
    return antes, s_glob + s_mon + s_real + s_pet + s_flu + s_vol + s_lit


# ====================================================================== ventana explicativa: TRM y tasa de cambio real
def ventana_peso(trm, it, L, num, fecha) -> str:
    es = L == "es"
    T = (lambda a, b: a if es else b)
    return f"""<dialog class="explica" id="exp-peso" aria-labelledby="exp-peso-t">
<div class="ex-cab"><p class="ex-k">{T("Para entender", "To understand")} · Superfinanciera · Banco de la República</p><h2 id="exp-peso-t">{T("¿Cómo se calcula la TRM y qué es la tasa de cambio real?", "How is the TRM computed and what is the real exchange rate?")}</h2>
<button type="button" class="ex-x" data-cerrar aria-label="{T("Cerrar", "Close")}">✕</button></div>
<div class="ex-cuerpo">
<p class="ex-lede">{T(f"La <b>TRM</b> (Tasa de Cambio Representativa del Mercado) es el precio de referencia del dólar en pesos. Hoy: <b>${num(float(trm.iloc[-1]), 2, L)}</b> ({fecha(trm.index[-1], 'd', L)}). Colombia tiene un régimen de tasa de cambio flexible: ninguna autoridad fija el precio del dólar; lo determinan la oferta y la demanda.",
 f"The <b>TRM</b> (Representative Market Exchange Rate) is the reference price of the dollar in pesos. Today: <b>${num(float(trm.iloc[-1]), 2, L)}</b> ({fecha(trm.index[-1], 'd', L)}). Colombia has a flexible exchange-rate regime: no authority sets the price of the dollar; supply and demand do.")}</p>

<h3>{T("1. Quién la calcula y con qué operaciones", "1. Who computes it and from which trades")}</h3>
<p>{T("La Superintendencia Financiera de Colombia la calcula y certifica cada día. Es el promedio ponderado por monto de las compras y ventas de dólares contra pesos, pactadas para cumplirse el mismo día, entre los intermediarios del mercado cambiario y otras entidades vigiladas, el Ministerio de Hacienda y las cámaras de riesgo central de contraparte.",
 "The Financial Superintendence of Colombia computes and certifies it every day. It is the amount-weighted average of dollar purchases and sales against pesos, agreed for same-day settlement, between foreign-exchange market intermediaries and other supervised entities, the Ministry of Finance and central counterparty clearing houses.")}</p>
<ul class="ex-lista">
<li>{T("Se excluyen los derivados, las operaciones con entidades del exterior, las de efectivo y las menores de US$5.000.", "Derivatives, trades with foreign entities, cash trades and trades under US$5,000 are excluded.")}</li>
<li>{T("La TRM calculada con las operaciones de un día rige el día hábil siguiente.", "The TRM computed from one day's trades applies on the next business day.")}</li>
<li>{T("Es una tasa de referencia: no es obligatoria en los contratos; las partes pactan libremente su precio.", "It is a reference rate: it is not mandatory in contracts; parties freely agree on their price.")}</li>
</ul>

<h3>{T("2. La tasa de cambio real (ITCR)", "2. The real exchange rate (ITCR)")}</h3>
<p>{T("La TRM dice cuántos pesos cuesta un dólar; la tasa de cambio real dice si los bienes colombianos son caros o baratos frente a los de otros países. El Banco de la República la calcula como la tasa de cambio nominal del peso frente a las monedas de sus principales socios comerciales, ajustada por la inflación relativa.",
 "The TRM says how many pesos a dollar costs; the real exchange rate says whether Colombian goods are expensive or cheap relative to other countries. The Banco de la República computes it as the peso's nominal exchange rate against its main trading partners' currencies, adjusted for relative inflation.")}</p>
<ul class="ex-lista">
<li>{T("Cubre los 22 principales socios comerciales (al menos 80% del comercio), con ponderaciones móviles de 12 meses de exportaciones e importaciones.", "It covers the 22 main trading partners (at least 80% of trade), with 12-month rolling weights of exports and imports.")}</li>
<li>{T("Se publica con dos deflactores (IPC e IPP) y dos ponderaciones: comercio total o no tradicional (sin café, petróleo, carbón, ferroníquel, esmeraldas ni oro).", "It is published with two deflators (CPI and PPI) and two weightings: total trade or non-traditional trade (excluding coffee, oil, coal, ferronickel, emeralds and gold).")}</li>
<li>{T(f"Base 2010 = 100. El Banco advierte que 2010 es solo una fecha de comparación, no un nivel de equilibrio. El índice sube cuando el peso se abarata en términos reales: hoy está en {num(float(it.iloc[-1]), 1, L)}.",
       f"Base 2010 = 100. The Bank warns that 2010 is only a comparison date, not an equilibrium level. The index rises when the peso becomes cheaper in real terms: today it stands at {num(float(it.iloc[-1]), 1, L)}.")}</li>
<li>{T("El ITCR-C mide la competitividad frente a otros países que venden en el mercado de Estados Unidos.", "The ITCR-C measures competitiveness against other countries selling in the US market.")}</li>
</ul>

<h3>{T("3. Cómo leer las cifras de esta página", "3. How to read the figures on this page")}</h3>
<p>{T("Cuando la TRM baja, el peso se fortalece (se necesitan menos pesos por dólar). Para saber si el movimiento es de Colombia o del mundo, la página compara el peso con el índice amplio del dólar de la Reserva Federal (frente a 26 monedas) y con las monedas vecinas: real brasileño, peso mexicano y sol peruano.",
 "When the TRM falls, the peso strengthens (fewer pesos per dollar). To tell whether a move is Colombian or global, the page compares the peso with the Federal Reserve's broad dollar index (against 26 currencies) and with peer currencies: Brazilian real, Mexican peso and Peruvian sol.")}</p>

<h3>{T("Fuentes oficiales", "Official sources")}</h3>
<ul class="ex-fuentes">
<li><a href="https://www.superfinanciera.gov.co/publicaciones/10100375/informes-y-cifrascifrasestablecimientos-de-creditoinformacion-periodicadiariatasa-de-cambio-representativa-del-mercado-trmantecedentes-normativos-trm-10100375/" target="_blank" rel="noopener">Superintendencia Financiera — {T("TRM: antecedentes normativos", "TRM: regulatory background")}</a></li>
<li><a href="https://www.banrep.gov.co/es/quien-calcula-tasa-representativa-del-mercado-trm-colombia-y-no-fijada-alguna-autoridad" target="_blank" rel="noopener">Banco de la República — {T("¿Quién calcula la TRM?", "Who computes the TRM?")}</a></li>
<li><a href="https://www.banrep.gov.co/economia/pli/Metodologia_ITCR_u.PDF" target="_blank" rel="noopener">Banco de la República — {T("Metodología del ITCR", "ITCR methodology")}</a></li>
<li>{T("Banco de la República, Resolución Externa 1 de 2018 de la Junta Directiva y Circular DOAM-146.", "Banco de la República, Board External Resolution 1 of 2018 and Circular DOAM-146.")}</li>
<li><a href="https://www.federalreserve.gov/releases/h10/" target="_blank" rel="noopener">{T("Reserva Federal — H.10, índice amplio del dólar", "Federal Reserve — H.10, broad dollar index")}</a></li>
</ul>
</div></dialog>"""
