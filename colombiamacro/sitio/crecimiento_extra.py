"""Pagina de crecimiento ampliada (v12.4): seis medidas, tres velocidades, crecimiento por
periodos, real frente a nominal (deflactor implicito), aportes por grandes grupos, economia
sin Gobierno y sin mineria, amplitud, sectores frente a su historia y nivel frente al camino
previo a la pandemia.

Solo datos observados del DANE y del Banco de la Republica; nada se proyecta.
Las figuras usan la paleta de origen de construir.py: app.js las adapta al tema.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

TX = {
    "s_medidas": ("El crecimiento en seis medidas", "Growth in six measures"),
    "s_velocidad": ("¿A qué velocidad crece la economía?", "How fast is the economy growing?"),
    "s_precios": ("¿Cuánto es crecimiento real y cuánto son precios?", "How much is real growth and how much is prices?"),
    "s_quien": ("¿Quién explica el crecimiento?", "Who explains growth?"),
    "s_amplitud": ("¿Cuántos sectores crecen y cómo van frente a su historia?", "How many sectors grow, and how do they compare with their history?"),
    "s_nivel": ("¿Dónde está la economía frente a su camino previo?", "Where is the economy versus its earlier path?"),
    "s_lit": ("Bases metodológicas y literatura", "Methodological basis and literature"),
    # lecturas
    "l_anual": ("Anual · {q}", "Annual · {q}"), "l_anual_d": ("frente al mismo trimestre de {a}", "versus the same quarter of {a}"),
    "l_trim": ("Trimestral anualizado", "Quarterly, annualised"),
    "l_trim_d": ("ritmo del último trimestre si durara un año ({v} sin anualizar)", "last quarter's pace if sustained for a year ({v} not annualised)"),
    "l_corrido": ("Año corrido · {p}", "Year to date · {p}"), "l_corrido_d": ("frente al mismo periodo de {a}", "versus the same period of {a}"),
    "l_priv": ("Sin Gobierno", "Excluding government"),
    "l_priv_d": ("crecimiento del resto de la economía (Gobierno: {v})", "growth of the rest of the economy (government: {v})"),
    "l_defl": ("Precios de toda la economía", "Economy-wide prices"),
    "l_defl_d": ("deflactor del PIB, anual · IPC: {v}", "GDP deflator, annual · CPI: {v}"),
    "l_2019": ("Tamaño frente a 2019", "Size versus 2019"),
    "l_2019_d": ("PIB desestacionalizado frente al T4 2019", "seasonally adjusted GDP versus 2019 Q4"),
    # respuestas
    "r_medidas": ("El PIB creció {a} en {q} frente a un año antes; el ritmo del trimestre, anualizado, fue {t}. "
                  "En lo corrido del año ({p}) la economía crece {c}. "
                  "Sin el sector Gobierno, educación y salud, el resto de la economía crece {pr}{pg}. "
                  "Los precios de todo lo que produce el país (deflactor) suben {df}, frente a {ipc} del IPC.",
                  "GDP grew {a} in {q} versus a year earlier; the quarter's annualised pace was {t}. "
                  "Year to date ({p}) the economy is growing {c}. "
                  "Excluding government, education and health, the rest of the economy grows {pr}{pg}. "
                  "Prices of everything the country produces (deflator) are rising {df}, versus {ipc} for the CPI."),
    "r_velocidad": ("Tres formas de medir el mismo crecimiento: frente al año anterior ({a}), los últimos 12 meses frente a los 12 previos ({d}) y el trimestre anualizado ({t}). "
                    "Cuando el ritmo trimestral supera al anual, la economía está acelerando. "
                    "Por periodos, el país creció {p1} al año en {n1}, {p2} en {n2} y {p3} en {n3}.",
                    "Three ways to measure the same growth: versus a year earlier ({a}), the last 12 months versus the previous 12 ({d}) and the annualised quarter ({t}). "
                    "When the quarterly pace exceeds the annual one, the economy is accelerating. "
                    "By period, the country grew {p1} a year in {n1}, {p2} in {n2} and {p3} in {n3}."),
    "r_precios": ("El PIB en pesos corrientes crece {n}; descontando precios, crece {r}. La diferencia, {df}, es la inflación de toda la economía (deflactor). "
                  "{dir}. Los términos de intercambio cambiaron {ti} en un año.",
                  "GDP in current pesos grows {n}; net of prices, {r}. The difference, {df}, is economy-wide inflation (deflator). "
                  "{dir}. The terms of trade changed {ti} over a year."),
    "r_dir_mas": ("El deflactor va por encima del IPC: los precios de lo que Colombia produce y exporta (petróleo, carbón, café) suben más que los de lo que consumen los hogares",
                  "The deflator runs above the CPI: prices of what Colombia produces and exports (oil, coal, coffee) rise faster than household consumer prices"),
    "r_dir_menos": ("El deflactor va por debajo del IPC: los precios de lo que Colombia produce y exporta suben menos que los de lo que consumen los hogares",
                    "The deflator runs below the CPI: prices of what Colombia produces and exports rise more slowly than household consumer prices"),
    "r_quien": ("En {q} los servicios de mercado aportan {sm} puntos, el Gobierno {go}, la industria y la construcción {ic} y el sector primario {pr}. "
                "Sin Gobierno la economía crece {sg}; sin minería, {sn}. "
                "Los aportes suman el crecimiento del valor agregado ({va}); el PIB ({pib}) incluye además los impuestos netos.",
                "In {q} market services contribute {sm} points, government {go}, manufacturing and construction {ic} and the primary sector {pr}. "
                "Excluding government the economy grows {sg}; excluding mining, {sn}. "
                "Contributions add up to value-added growth ({va}); GDP ({pib}) also includes net taxes."),
    "r_amplitud": ("{k} de los 12 sectores crecen frente a un año antes. "
                   "Frente a su propio promedio de 2015–2019, {m} sectores crecen más rápido hoy; {top} es el que más se aleja hacia arriba y {bot} hacia abajo.",
                   "{k} of the 12 sectors are growing versus a year earlier. "
                   "Versus their own 2015–2019 average, {m} sectors grow faster today; {top} is furthest above and {bot} furthest below."),
    "r_nivel": ("La economía es {v} más grande que a finales de 2019. "
                "Pero si hubiera seguido el ritmo de 2015–2019 ({g} al año), hoy sería {b} {dir}: la pandemia dejó una pérdida de nivel que no se ha recuperado.",
                "The economy is {v} larger than at end-2019. "
                "But had it kept its 2015–2019 pace ({g} a year), it would now be {b} {dir}: the pandemic left a level loss that has not been recovered."),
    "dir_mayor": ("más grande", "larger"), "dir_menor": ("más grande de lo que es", "larger than it is"),
    "r_nivel_rec": ("La economía es {v} más grande que a finales de 2019 y ya superó el camino que traía en 2015–2019 ({g} al año) en {b}.",
                    "The economy is {v} larger than at end-2019 and has already moved {b} above its 2015–2019 path ({g} a year)."),
    "pg_si": (": el sector público explica una parte grande del dato", ": the public sector explains a large part of the figure"),
    "pg_no": (", un ritmo similar al total", ", a pace similar to the total"),
    # graficos
    "g_velocidades": ("Tres velocidades del crecimiento del PIB", "Three speeds of GDP growth"),
    "h_velocidades": ("Línea azul: frente al mismo trimestre del año anterior. Línea verde: últimos 12 meses frente a los 12 anteriores (más suave). Barras: el trimestre frente al anterior, anualizado (más rápido, más ruidoso). 2020–2021 se recortan para no aplastar la escala.",
                      "Blue line: versus the same quarter a year earlier. Green line: last 12 months versus the previous 12 (smoother). Bars: the quarter versus the previous one, annualised (faster, noisier). 2020–2021 are capped so the scale stays readable."),
    "lbl_anual": ("Anual", "Annual"), "lbl_12m": ("12 meses", "12 months"), "lbl_saar": ("Trimestre anualizado", "Annualised quarter"),
    "g_periodos": ("Crecimiento promedio por periodo", "Average growth by period"),
    "h_periodos": ("Crecimiento anual compuesto del PIB real en cada periodo. El último es el año corrido frente al mismo periodo del año anterior.",
                   "Compound annual real GDP growth in each period. The last bar is year to date versus the same period a year earlier."),
    "p_auge": ("Auge petrolero", "Oil boom"), "p_ajuste": ("Ajuste", "Adjustment"), "p_covid": ("Pandemia y rebote", "Pandemic and rebound"),
    "p_post": ("Pospandemia", "Post-pandemic"), "p_corrido": ("Año corrido", "Year to date"),
    "g_realnom": ("PIB en pesos corrientes y PIB real", "GDP in current pesos and real GDP"),
    "h_realnom": ("Variación anual. Azul: PIB real (descontando precios). Naranja: PIB en pesos de cada momento. La distancia entre las dos es el aumento de precios de toda la economía.",
                  "Annual change. Blue: real GDP (net of prices). Orange: GDP in pesos of each period. The distance between them is the economy-wide price increase."),
    "lbl_nominal": ("PIB nominal", "Nominal GDP"), "lbl_real": ("PIB real", "Real GDP"),
    "g_deflactor": ("Precios de lo que se produce frente a precios de lo que se consume", "Prices of what is produced versus prices of what is consumed"),
    "h_deflactor": ("Línea morada: deflactor implícito del PIB (precios de todo lo que produce el país). Línea naranja: IPC (precios de la canasta de los hogares), promedio del trimestre. Cuando la morada va arriba, suben más los precios de lo que Colombia vende al mundo.",
                    "Purple line: implicit GDP deflator (prices of everything the country produces). Orange line: CPI (household basket prices), quarterly average. Purple above means prices of what Colombia sells abroad are rising faster."),
    "lbl_defl": ("Deflactor del PIB", "GDP deflator"), "lbl_ipc": ("IPC", "CPI"),
    "g_grupos": ("Aportes al crecimiento por grandes grupos", "Contributions to growth by broad group"),
    "h_grupos": ("Puntos porcentuales que cada grupo suma al crecimiento anual del valor agregado. La línea es el total. Servicios de mercado: comercio, transporte, comunicaciones, finanzas, inmobiliarias, servicios profesionales y entretenimiento.",
                 "Percentage points each group adds to annual value-added growth. The line is the total. Market services: trade, transport, communications, finance, real estate, professional services and entertainment."),
    "gr_prim": ("Primario (agro y minería)", "Primary (farming and mining)"), "gr_ind": ("Industria, energía y construcción", "Manufacturing, utilities and construction"),
    "gr_serv": ("Servicios de mercado", "Market services"), "gr_gob": ("Gobierno, educación y salud", "Government, education and health"),
    "lbl_total_va": ("Valor agregado", "Value added"),
    "g_singob": ("La economía con y sin Gobierno", "The economy with and without government"),
    "h_singob": ("Variación anual del valor agregado. Azul: total. Verde: sin el sector Gobierno, educación y salud. Gris punteado: sin minería. Si la verde va por debajo, el sector público está sosteniendo el crecimiento.",
                 "Annual change in value added. Blue: total. Green: excluding government, education and health. Grey dotted: excluding mining. Green below blue means the public sector is propping up growth."),
    "lbl_total": ("Total", "Total"), "lbl_singob": ("Sin Gobierno", "Excluding government"), "lbl_sinmin": ("Sin minería", "Excluding mining"),
    "g_crecen": ("Sectores que crecen, de 12", "Sectors growing, out of 12"),
    "h_crecen": ("Cada barra es un trimestre: cuántos de los 12 sectores producen más que un año antes. Verde: 7 o más (crecimiento extendido); naranja: 6 o menos.",
                 "Each bar is a quarter: how many of the 12 sectors produce more than a year earlier. Green: 7 or more (broad growth); orange: 6 or fewer."),
    "lbl_amplio": ("7 o más", "7 or more"), "lbl_estrecho": ("6 o menos", "6 or fewer"),
    "g_historia": ("Cada sector frente a su propia historia", "Each sector versus its own history"),
    "h_historia": ("Punto gris: crecimiento anual promedio de 2015–2019. Punto de color: promedio de los últimos 4 trimestres. Verde si hoy crece más que en su historia; naranja si crece menos.",
                   "Grey dot: average annual growth in 2015–2019. Coloured dot: average of the last 4 quarters. Green if it grows faster than its history; orange if slower."),
    "lbl_hist": ("Promedio 2015–2019", "2015–2019 average"), "lbl_hoy": ("Últimos 4 trimestres", "Last 4 quarters"),
    "g_nivel": ("Nivel del PIB frente al camino de 2015–2019", "GDP level versus its 2015–2019 path"),
    "h_nivel": ("PIB real desestacionalizado, T4 2019 = 100. La línea punteada prolonga la tendencia de 2015–2019: no es una proyección, es la referencia de dónde estaría la economía si no hubiera cambiado su ritmo.",
                "Seasonally adjusted real GDP, 2019 Q4 = 100. The dotted line extends the 2015–2019 trend: not a forecast, but a reference for where the economy would be had its pace not changed."),
    "lbl_pib": ("PIB real", "Real GDP"), "lbl_tend": ("Camino de 2015–2019", "2015–2019 path"),
}

GRUPOS = {
    "gr_prim": ["Agro y pesca", "Minería"],
    "gr_ind": ["Industria", "Electricidad, gas y agua", "Construcción"],
    "gr_serv": ["Comercio, transporte y turismo", "Información y comunicaciones", "Finanzas y seguros", "Inmobiliarias",
                "Servicios profesionales", "Arte, hogares y otros"],
    "gr_gob": ["Gobierno, educación y salud"],
}
SECTOR_EN = {"Agro y pesca": "Farming and fishing", "Minería": "Mining", "Industria": "Manufacturing",
             "Electricidad, gas y agua": "Utilities", "Construcción": "Construction",
             "Comercio, transporte y turismo": "Trade, transport and tourism", "Información y comunicaciones": "Information and communications",
             "Finanzas y seguros": "Finance and insurance", "Inmobiliarias": "Real estate", "Servicios profesionales": "Professional services",
             "Gobierno, educación y salud": "Government, education and health", "Arte, hogares y otros": "Arts, households and other"}

LITERATURA = [
    ("Burns, A. F. y Mitchell, W. C. (1946). <i>Measuring Business Cycles</i>. NBER.",
     "Índices de difusión: cuántos sectores se mueven en la misma dirección.", "Diffusion indices: how many sectors move together."),
    ("Hodrick, R. J. y Prescott, E. C. (1997). Postwar U.S. Business Cycles. <i>Journal of Money, Credit and Banking</i>, 29(1), 1–16.",
     "Tendencia y ritmo normal de crecimiento.", "Trend and normal growth pace."),
    ("Hamilton, J. D. (2018). Why You Should Never Use the Hodrick-Prescott Filter. <i>Review of Economics and Statistics</i>, 100(5), 831–843.",
     "Crítica y alternativa al filtro HP (se usa en la página del ciclo).", "Critique of and alternative to the HP filter (used on the cycle page)."),
    ("Kohli, U. (2004). Real GDP, Real Domestic Income, and Terms-of-Trade Changes. <i>Journal of International Economics</i>, 62(1), 83–106.",
     "Por qué el deflactor del PIB y el IPC divergen cuando cambian los términos de intercambio.", "Why the GDP deflator and the CPI diverge when the terms of trade change."),
    ("Cerra, V. y Saxena, S. C. (2008). Growth Dynamics: The Myth of Economic Recovery. <i>American Economic Review</i>, 98(1), 439–457.",
     "Las crisis dejan pérdidas permanentes de nivel del producto.", "Crises leave permanent output-level losses."),
    ("Blanchard, O., Cerutti, E. y Summers, L. (2015). Inflation and Activity: Two Explorations and their Monetary Policy Implications. IMF WP/15/230.",
     "Histéresis: recesiones que reducen el camino del producto.", "Hysteresis: recessions that lower the output path."),
    ("DANE. Cuentas nacionales trimestrales: metodología (enfoque de la producción, índices encadenados).",
     "Por qué los aportes por sector no suman exactamente el PIB (impuestos y encadenamiento).", "Why sector contributions do not add exactly to GDP (taxes and chain-linking)."),
]


def tx(k, L):
    return TX[k][0 if L == "es" else 1]


def _qx(idx):
    return pd.DatetimeIndex(idx) + pd.offsets.QuarterEnd(0)


def medidas(d):
    """Indicadores derivados (solo datos observados)."""
    p = d.pib.set_index("fecha").sort_index()
    r = p["pib_real_miles_millones_ref2015"].astype(float)
    sa = p["pib_real_ajustado_miles_millones_ref2015"].astype(float)
    n = p["pib_nominal_billones_cop"].astype(float)
    yoy = (r / r.shift(4) - 1) * 100
    r4 = r.rolling(4).sum()
    d12 = (r4 / r4.shift(4) - 1) * 100
    saar = ((sa / sa.shift(1)) ** 4 - 1) * 100
    qoq = (sa / sa.shift(1) - 1) * 100
    nom = (n / n.shift(4) - 1) * 100
    defl = n / r
    defl_y = (defl / defl.shift(4) - 1) * 100
    ipc = d.inflacion.set_index("fecha")["inflacion_anual"].resample("QS").mean()
    fin = r.index[-1]
    q_ano = r[r.index.year == fin.year]
    q_prev = r[(r.index.year == fin.year - 1) & (r.index.month <= fin.month)]
    corrido = (q_ano.sum() / q_prev.sum() - 1) * 100
    # aportes y crecimiento sin Gobierno / sin mineria
    s = d.sectores.copy()
    tot_c = s.groupby("fecha")["contribucion"].sum()
    tot_w = s.groupby("fecha")["peso"].sum()

    def sin(sector):
        x = s[s["sector"] == sector].set_index("fecha")
        return 100 * (tot_c - x["contribucion"]) / (tot_w - x["peso"])

    grupos = pd.DataFrame({k: s[s["sector"].isin(v)].groupby("fecha")["contribucion"].sum() for k, v in GRUPOS.items()})
    crecen = s.groupby("fecha")["yoy"].apply(lambda x: int((x > 0).sum()))
    # tendencia 2015-2019 (log-lineal) del PIB desestacionalizado
    base = sa.loc["2015-01-01":"2019-10-01"]
    tt = np.arange(len(base))
    b1, b0 = np.polyfit(tt, np.log(base.values), 1)
    idx = sa.loc["2015-01-01":]
    tend = pd.Series(np.exp(b0 + b1 * np.arange(len(idx))), index=idx.index)
    return {"r": r, "sa": sa, "yoy": yoy, "d12": d12, "saar": saar, "qoq": qoq, "nom": nom, "defl_y": defl_y, "ipc": ipc,
            "corrido": corrido, "fin": fin, "q_ini": q_ano.index[0], "tot_c": tot_c, "singob": sin("Gobierno, educación y salud"),
            "sinmin": sin("Minería"), "grupos": grupos, "crecen": crecen, "tend": tend, "g_tend": (np.exp(4 * b1) - 1) * 100,
            "vs2019": (sa.iloc[-1] / sa.loc["2019-10-01"] - 1) * 100, "brecha_tend": (sa.iloc[-1] / tend.iloc[-1] - 1) * 100}


def cagr(r, a0, a1):
    """Crecimiento anual compuesto entre el ano a0-1 y a1 (anos completos)."""
    y = r.groupby(r.index.year).sum()
    return ((y[a1] / y[a0 - 1]) ** (1 / (a1 - a0 + 1)) - 1) * 100


def construir_crecimiento(d, s, L):
    """Devuelve (html_antes_de_la_seccion_actual, html_despues)."""
    from colombiamacro.sitio import construir as cs
    num, fecha, esc = cs.num, cs.fecha, cs.esc
    cs.LANG_ACTUAL[0] = L
    M = medidas(d)
    fin = M["fin"]
    q = fecha(fin, "q", L)
    pct = lambda v, dec=1, sg=True: num(float(v), dec, L, sg, "%")
    sector = lambda n: n if L == "es" else SECTOR_EN.get(n, n)
    periodo = (f'{"T1" if L == "es" else "Q1"}–{q.split()[0]} {fin.year}') if fin.month > 1 else q
    ipc_q = M["ipc"].get(fin, np.nan)
    sec_u = d.sectores[d.sectores["fecha"] == d.sectores["fecha"].max()]
    gob = sec_u[sec_u["sector"] == "Gobierno, educación y salud"].iloc[0]

    def seccion(sid, titulo, resp, cuerpo):
        return (f'<section id="{sid}" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{titulo}</h2></div>'
                f'{cs.respuesta_html(resp, L)}{cuerpo}</section>')

    def lec(k, v, dsc, tono, href):
        return (f'<a class="lec {tono}" href="{href}"><span class="lec-k">{k}</span><b class="lec-v">{v}</b>'
                f'<span class="lec-d">{dsc}</span></a>')

    tono = lambda v, ref=0: "ok" if v >= ref else "warn"
    lecturas = "".join([
        lec(tx("l_anual", L).format(q=q), pct(M["yoy"].iloc[-1]), tx("l_anual_d", L).format(a=fin.year - 1), tono(M["yoy"].iloc[-1], 2), "#crec-velocidad"),
        lec(tx("l_trim", L), pct(M["saar"].iloc[-1]), tx("l_trim_d", L).format(v=pct(M["qoq"].iloc[-1])), tono(M["saar"].iloc[-1], 2), "#crec-velocidad"),
        lec(tx("l_corrido", L).format(p=periodo), pct(M["corrido"]), tx("l_corrido_d", L).format(a=fin.year - 1), tono(M["corrido"], 2), "#crec-velocidad"),
        lec(tx("l_priv", L), pct(M["singob"].iloc[-1]), tx("l_priv_d", L).format(v=pct(gob["yoy"])), tono(M["singob"].iloc[-1], 2), "#crec-quien"),
        lec(tx("l_defl", L), pct(M["defl_y"].iloc[-1], 1, False), tx("l_defl_d", L).format(v=pct(ipc_q, 1, False)), "", "#crec-precios"),
        lec(tx("l_2019", L), pct(M["vs2019"]), tx("l_2019_d", L), "", "#crec-nivel"),
    ])
    r0 = tx("r_medidas", L).format(a=pct(M["yoy"].iloc[-1]), q=q, t=pct(M["saar"].iloc[-1]), p=periodo, c=pct(M["corrido"]),
                                   pr=pct(M["singob"].iloc[-1]), pg=tx("pg_si" if M["tot_c"].iloc[-1] - M["singob"].iloc[-1] > 0.5 else "pg_no", L), df=pct(M["defl_y"].iloc[-1], 1, False), ipc=pct(ipc_q, 1, False))
    antes = seccion("crec-medidas", tx("s_medidas", L), r0, f'<div class="lecturas seis">{lecturas}</div>')

    # ------------------------------------------------ velocidades + periodos
    desde = pd.Timestamp("2012-01-01")
    f1 = cs.base(L, height=340)
    sv = M["saar"].loc[desde:].dropna()
    f1.add_trace(go.Bar(x=_qx(sv.index), y=sv.clip(-12, 16).round(2), name=tx("lbl_saar", L),
                        marker=dict(color="rgba(42,120,214,0.62)", line=dict(width=0)), hovertemplate="%{y:.1f}%"))
    yv = M["yoy"].loc[desde:].dropna()
    cs.linea(f1, _qx(yv.index), yv.clip(-12, 16), tx("lbl_anual", L), cs.C1, width=2.4, lang=L)
    dv = M["d12"].loc[desde:].dropna()
    cs.linea(f1, _qx(dv.index), dv.clip(-12, 16), tx("lbl_12m", L), cs.C3, width=2.0, lang=L)
    f1.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    f1.update_layout(bargap=0.2)
    g1 = cs.bloque_grafico(tx("g_velocidades", L), cs.fig_html(f1, {}, "g-velocidades"), tx("h_velocidades", L))

    r = M["r"]
    per = [("p_auge", 2010, 2014), ("p_ajuste", 2015, 2019), ("p_covid", 2020, 2021), ("p_post", 2022, 2025)]
    per = [(k, a0, a1) for k, a0, a1 in per if r.index.year.min() <= a0 - 1 and (r.index.year == a1).sum() == 4]
    vals = [(f'{tx(k, L)}<br>{a0}–{a1}', cagr(r, a0, a1)) for k, a0, a1 in per] + [(f'{tx("p_corrido", L)}<br>{periodo}', M["corrido"])]
    f2 = cs.base(L, height=340, fecha_x=False)
    f2.add_trace(go.Bar(x=[v[0] for v in vals], y=[round(v[1], 2) for v in vals], showlegend=False,
                        marker=dict(color=[cs.C1] * (len(vals) - 1) + ["rgba(42,120,214,0.62)"], line=dict(width=0)),
                        text=[pct(v[1], 1, False) for v in vals], textposition="outside", cliponaxis=False,
                        hovertemplate="%{y:.1f}%<extra></extra>"))
    f2.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    f2.update_yaxes(range=[min(0, min(v[1] for v in vals)) - 0.5, max(v[1] for v in vals) * 1.25])
    f2.update_layout(bargap=0.4, hovermode="closest")
    g2 = cs.bloque_grafico(tx("g_periodos", L), cs.fig_html(f2, {"notime": True}, "g-periodos"), tx("h_periodos", L))
    pv = [(tx(k, L).lower(), f"{a0}–{a1}", cagr(r, a0, a1)) for k, a0, a1 in per]
    pv = [pv[0], pv[1], pv[-1]] if len(pv) >= 3 else (pv + pv[:1] * 3)[:3]
    r1 = tx("r_velocidad", L).format(a=pct(M["yoy"].iloc[-1]), d=pct(M["d12"].iloc[-1]), t=pct(M["saar"].iloc[-1]),
                                     p1=pct(pv[0][2], 1, False), n1=pv[0][1], p2=pct(pv[1][2], 1, False), n2=pv[1][1],
                                     p3=pct(pv[2][2], 1, False), n3=pv[2][1])
    s_vel = seccion("crec-velocidad", tx("s_velocidad", L), r1, f'<div class="grid">{g1}{g2}</div>')

    # ------------------------------------------------ real vs nominal, deflactor vs IPC
    f3 = cs.base(L, height=330)
    nv = M["nom"].loc[desde:].dropna()
    cs.linea(f3, _qx(nv.index), nv.clip(-15, 30), tx("lbl_nominal", L), cs.C2, width=2.2, lang=L)
    cs.linea(f3, _qx(yv.index), yv.clip(-15, 30), tx("lbl_real", L), cs.C1, width=2.2, lang=L)
    f3.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    g3 = cs.bloque_grafico(tx("g_realnom", L), cs.fig_html(f3, {}, "g-real-nominal"), tx("h_realnom", L))
    f4 = cs.base(L, height=330)
    dfv = M["defl_y"].loc[desde:].dropna()
    cs.linea(f4, _qx(dfv.index), dfv, tx("lbl_defl", L), cs.C7, width=2.4, lang=L)
    iv = M["ipc"].loc[desde:fin].dropna()
    cs.linea(f4, _qx(iv.index), iv, tx("lbl_ipc", L), cs.C2, width=2.0, lang=L)
    f4.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    g4 = cs.bloque_grafico(tx("g_deflactor", L), cs.fig_html(f4, {}, "g-deflactor"), tx("h_deflactor", L))
    ti = d.extra.get("terminos_intercambio")
    ti_txt = "—"
    if ti is not None and not ti.empty:
        tq = ti.set_index("fecha").iloc[:, 0].resample("QS").mean()
        if fin in tq.index and fin - pd.DateOffset(years=1) in tq.index:
            ti_txt = pct((tq[fin] / tq[fin - pd.DateOffset(years=1)] - 1) * 100)
    r2 = tx("r_precios", L).format(n=pct(M["nom"].iloc[-1]), r=pct(M["yoy"].iloc[-1]), df=pct(M["defl_y"].iloc[-1], 1, False),
                                   dir=tx("r_dir_mas" if M["defl_y"].iloc[-1] > ipc_q else "r_dir_menos", L), ti=ti_txt)
    s_pre = seccion("crec-precios", tx("s_precios", L), r2, f'<div class="grid">{g3}{g4}</div>')

    # ------------------------------------------------ quien: grupos + sin gobierno
    gr = M["grupos"].loc[pd.Timestamp(fin) - pd.DateOffset(years=4):]
    colores = {"gr_serv": cs.C1, "gr_gob": cs.C7, "gr_ind": cs.C4, "gr_prim": cs.C2}
    f5 = cs.base(L, height=360, suffix=" pp")
    xg = _qx(gr.index)
    for k in ("gr_serv", "gr_gob", "gr_ind", "gr_prim"):
        f5.add_trace(go.Bar(x=xg, y=gr[k].round(2), name=tx(k, L), marker=dict(color=colores[k], line=dict(width=0)),
                            hovertemplate="%{y:.2f} pp"))
    tc = M["tot_c"].loc[gr.index]
    f5.add_trace(go.Scatter(x=xg, y=tc.round(2), name=tx("lbl_total_va", L), mode="lines+markers",
                            line=dict(color=cs.INK, width=2), marker=dict(size=6, color=cs.INK), hovertemplate="%{y:.1f}%"))
    f5.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    f5.update_layout(barmode="relative", bargap=0.25)
    f5.update_xaxes(dtick="M6", tickformat="%m/%Y", tickangle=0)
    g5 = cs.bloque_grafico(tx("g_grupos", L), cs.fig_html(f5, {"notime": True}, "g-aportes-grupos"), tx("h_grupos", L))
    f6 = cs.base(L, height=360)
    for serie, lbl, col, w, dash in ((M["tot_c"], "lbl_total", cs.C1, 2.4, None), (M["singob"], "lbl_singob", cs.C3, 2.2, None),
                                     (M["sinmin"], "lbl_sinmin", cs.GRAY, 1.6, "dot")):
        sv_ = serie.loc[desde:].dropna()
        cs.linea(f6, _qx(sv_.index), sv_.clip(-12, 16), tx(lbl, L), col, width=w, dash=dash, lang=L)
    f6.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    g6 = cs.bloque_grafico(tx("g_singob", L), cs.fig_html(f6, {}, "g-sin-gobierno"), tx("h_singob", L))
    ug = M["grupos"].iloc[-1]
    r3 = tx("r_quien", L).format(q=fecha(M["grupos"].index[-1], "q", L), sm=num(ug["gr_serv"], 1, L), go=num(ug["gr_gob"], 1, L),
                                 ic=num(ug["gr_ind"], 1, L, True), pr=num(ug["gr_prim"], 1, L, True), sg=pct(M["singob"].iloc[-1]),
                                 sn=pct(M["sinmin"].iloc[-1]), va=pct(M["tot_c"].iloc[-1]), pib=pct(M["yoy"].iloc[-1]))
    s_quien = seccion("crec-quien", tx("s_quien", L), r3, f'<div class="grid">{g5}{g6}</div>')

    # ------------------------------------------------ amplitud + historia
    cr = M["crecen"].loc["2010":]
    f7 = cs.base(L, height=330, suffix="")
    for cond, lbl, col in ((cr >= 7, "lbl_amplio", cs.C3), (cr < 7, "lbl_estrecho", cs.C2)):
        f7.add_trace(go.Bar(x=_qx(cr.index), y=cr.where(cond), name=tx(lbl, L), marker=dict(color=col, line=dict(width=0)),
                            hovertemplate="%{y} / 12"))
    f7.add_hline(y=6.5, line=dict(color=cs.INK2, width=1, dash="dot"))
    f7.update_yaxes(range=[0, 12.5], dtick=3)
    f7.update_layout(barmode="overlay", bargap=0.15)
    g7 = cs.bloque_grafico(tx("g_crecen", L), cs.fig_html(f7, {"noy": True}, "g-sectores-crecen"), tx("h_crecen", L))
    sc = d.sectores.copy()
    hist = sc[(sc["fecha"] >= "2015-01-01") & (sc["fecha"] <= "2019-10-01")].groupby("sector")["yoy"].mean()
    ult4 = sc[sc["fecha"] > sc["fecha"].max() - pd.DateOffset(years=1)].groupby("sector")["yoy"].mean()
    tb = pd.DataFrame({"h": hist, "u": ult4}).dropna().sort_values("u")
    nombres = [sector(n) for n in tb.index]
    f8 = cs.base(L, height=420, fecha_x=False)
    for (nm, row) in zip(nombres, tb.itertuples()):
        f8.add_trace(go.Scatter(x=[row.h, row.u], y=[nm, nm], mode="lines", line=dict(color=cs.RULE, width=3),
                                showlegend=False, hoverinfo="skip"))
    f8.add_trace(go.Scatter(x=tb["h"].round(2), y=nombres, mode="markers", name=tx("lbl_hist", L),
                            marker=dict(size=11, color=cs.GRAY, line=dict(color="#fff", width=1.5)), hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
    f8.add_trace(go.Scatter(x=tb["u"].round(2), y=nombres, mode="markers", name=tx("lbl_hoy", L),
                            marker=dict(size=13, color=[cs.C3 if u >= h else cs.C2 for h, u in zip(tb["h"], tb["u"])],
                                        line=dict(color="#fff", width=1.5)), hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
    f8.add_vline(x=0, line=dict(color=cs.INK2, width=1))
    f8.update_xaxes(ticksuffix="%", showgrid=True, gridcolor=cs.GRID)
    f8.update_yaxes(ticksuffix="", tickfont=dict(size=12, color=cs.INK2))
    f8.update_layout(hovermode="closest")
    g8 = cs.bloque_grafico(tx("g_historia", L), cs.fig_html(f8, {"notime": True}, "g-sector-historia"), tx("h_historia", L))
    dif = (tb["u"] - tb["h"]).sort_values()
    r4 = tx("r_amplitud", L).format(k=int(M["crecen"].iloc[-1]), m=int((dif > 0).sum()), top=sector(dif.index[-1]), bot=sector(dif.index[0]))
    s_amp = seccion("crec-amplitud", tx("s_amplitud", L), r4, f'<div class="grid">{g7}{g8}</div>')

    # ------------------------------------------------ nivel frente al camino previo
    sa = M["sa"].loc["2015-01-01":]
    base19 = M["sa"].loc["2019-10-01"]
    f9 = cs.base(L, height=340, suffix="")
    cs.linea(f9, _qx(sa.index), 100 * sa / base19, tx("lbl_pib", L), cs.C1, width=2.6, suf="", lang=L)
    cs.linea(f9, _qx(M["tend"].index), 100 * M["tend"] / base19, tx("lbl_tend", L), cs.INK2, width=1.6, dash="dot", suf="", lang=L)
    f9.add_hline(y=100, line=dict(color=cs.RULE, width=1))
    g9 = cs.bloque_grafico(tx("g_nivel", L), cs.fig_html(f9, {}, "g-nivel"), tx("h_nivel", L), ancho=True)
    bt = M["brecha_tend"]
    if bt < 0:
        r5 = tx("r_nivel", L).format(v=pct(M["vs2019"], 1, False), g=pct(M["g_tend"], 1, False), b=pct(-bt / (1 + bt / 100), 1, False),
                                     dir=tx("dir_mayor", L))
    else:
        r5 = tx("r_nivel_rec", L).format(v=pct(M["vs2019"], 1, False), g=pct(M["g_tend"], 1, False), b=pct(bt, 1, False))
    s_niv = seccion("crec-nivel", tx("s_nivel", L), r5, f'<div class="grid">{g9}</div>')

    # ------------------------------------------------ literatura
    items = "".join(f'<li><span class="ref">{ref}</span><span class="ref-u">{es if L == "es" else en}</span></li>' for ref, es, en in LITERATURA)
    s_lit = (f'<section id="crec-literatura" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{tx("s_lit", L)}</h2></div>'
             f'<ol class="refs">{items}</ol></section>')

    return antes, s_vel + s_pre + s_quien + s_amp + s_niv + s_lit, r0
