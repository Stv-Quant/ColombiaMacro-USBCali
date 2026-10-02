"""Pagina de empleo ampliada (v12.8): ocho medidas, empleo por rama y por posicion ocupacional,
brechas entre hombres y mujeres, jovenes (desempleo y NiNi), campo y ciudad, poblacion fuera de la
fuerza de trabajo y desempleo en las 32 capitales (trasladado desde Capacidad).

Solo datos observados (DANE, GEIH). Las series mensuales del DANE no estan desestacionalizadas:
se comparan promedios de 12 meses o el mismo periodo del ano anterior.
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from colombiamacro.config import DATA_DIR

TX = {
    "s_medidas": ("El empleo en ocho medidas", "Jobs in eight measures"),
    "s_ramas": ("¿Dónde se crean (y se pierden) los empleos?", "Where are jobs being created (and lost)?"),
    "s_posicion": ("¿Qué tipo de empleo se crea?", "What kind of jobs are being created?"),
    "s_genero": ("¿Cómo les va a las mujeres frente a los hombres?", "How do women fare compared with men?"),
    "s_jovenes": ("¿Cómo les va a los jóvenes?", "How are young people doing?"),
    "s_area": ("Campo y ciudad, y quienes no participan", "Countryside and cities, and those who do not participate"),
    "s_lit": ("Bases metodológicas y literatura", "Methodological basis and literature"),
    # lecturas
    "l_ocu": ("Personas ocupadas", "Employed people"), "l_ocu_d": ("millones (12 meses) · {v} mil frente a un año antes", "million (12 months) · {v} thousand versus a year earlier"),
    "l_to": ("Tasa de ocupación", "Employment rate"), "l_to_d": ("de la población en edad de trabajar · {v} en un año", "of the working-age population · {v} over a year"),
    "l_td": ("Desempleo", "Unemployment"), "l_td_d": ("desestacionalizado, {m} · hace un año {v}", "seasonally adjusted, {m} · a year ago {v}"),
    "l_inf": ("Informalidad", "Informality"), "l_inf_d": ("de los ocupados ({p}) · hace un año {v}", "of the employed ({p}) · a year ago {v}"),
    "l_asal": ("Asalariados", "Wage employees"), "l_asal_d": ("de los ocupados (12 meses) · en 2019 {v}", "of the employed (12 months) · in 2019 {v}"),
    "l_gen": ("Brecha de desempleo mujeres − hombres", "Unemployment gap, women − men"), "l_gen_d": ("mujeres {m} · hombres {h} (12 meses)", "women {m} · men {h} (12 months)"),
    "l_jov": ("Desempleo juvenil (15–28)", "Youth unemployment (15–28)"), "l_jov_d": ("{p} · hace un año {v}", "{p} · a year ago {v}"),
    "l_nini": ("Jóvenes que ni estudian ni trabajan", "Young people neither studying nor working"), "l_nini_d": ("de los jóvenes de 15 a 28 · en 2019 {v}", "of 15–28 year-olds · in 2019 {v}"),
    # respuestas
    "r_medidas": ("Colombia tiene {o} millones de personas ocupadas, {d} mil más que un año antes, y el desempleo desestacionalizado es {td}. "
                  "El empleo asalariado gana terreno: {a} de los ocupados, frente a {a19} en 2019. "
                  "Las brechas persisten: el desempleo de las mujeres supera al de los hombres en {g} pp y {n} de los jóvenes ni estudian ni trabajan.",
                  "Colombia has {o} million employed people, {d} thousand more than a year earlier, and seasonally adjusted unemployment is {td}. "
                  "Wage employment is gaining ground: {a} of the employed, versus {a19} in 2019. "
                  "Gaps persist: women's unemployment exceeds men's by {g} pp and {n} of young people neither study nor work."),
    "r_ramas": ("En el último año (promedio de 3 meses frente al mismo periodo de hace un año) {r1} sumó {v1} mil empleos y {r2} {v2} mil; "
                "{r3} perdió {v3} mil. Frente a 2019, el mayor crecimiento del empleo está en {s1} ({p1}) y la mayor caída en {s2} ({p2}).",
                "Over the last year (3-month average versus the same period a year earlier) {r1} added {v1} thousand jobs and {r2} {v2} thousand; "
                "{r3} lost {v3} thousand. Versus 2019, employment has grown most in {s1} ({p1}) and fallen most in {s2} ({p2})."),
    "r_posicion": ("Los asalariados del sector privado son {p} de los ocupados y los trabajadores por cuenta propia {c}. "
                   "En el último año los asalariados privados cambiaron {dp} mil y los cuenta propia {dc} mil: {txt}.",
                   "Private-sector wage employees are {p} of the employed and own-account workers {c}. "
                   "Over the last year private wage employees changed by {dp} thousand and own-account workers by {dc} thousand: {txt}."),
    "pos_mejor": ("el empleo se está formalizando por la vía de los contratos", "employment is formalising through wage contracts"),
    "pos_peor": ("el empleo crece sobre todo por cuenta propia, más expuesto a la informalidad", "employment grows mainly through self-employment, more exposed to informality"),
    "r_genero": ("En los últimos 12 meses el desempleo de las mujeres fue {m} y el de los hombres {h}: una brecha de {g} pp (en 2019 era {g19} pp). "
                 "La participación laboral de las mujeres es {pm}, frente a {ph} de los hombres: {fh} millones de mujeres están fuera de la fuerza de trabajo, la mayoría dedicadas a oficios del hogar.",
                 "Over the last 12 months women's unemployment was {m} and men's {h}: a {g} pp gap (it was {g19} pp in 2019). "
                 "Women's labour participation is {pm}, versus {ph} for men: {fh} million women are outside the labour force, most of them doing household work."),
    "r_jovenes": ("El desempleo de los jóvenes de 15 a 28 años es {t} ({p}), {x} veces el de toda la población; para las mujeres jóvenes llega a {m}. "
                  "{n} de los jóvenes no estudian ni están ocupados (en 2019, {n19}); {sm} de ellos son mujeres.",
                  "Unemployment among 15–28 year-olds is {t} ({p}), {x} times the overall rate; for young women it reaches {m}. "
                  "{n} of young people are neither studying nor employed (in 2019, {n19}); {sm} of them are women."),
    "r_area": ("En las cabeceras el desempleo es {c} y en el campo {r} ({p}): una diferencia de {x} pp. "
               "{f} millones de personas en edad de trabajar no participan: {h} millones se dedican al hogar y {e} millones estudian.",
               "In urban areas unemployment is {c} and in rural areas {r} ({p}): a gap of {x} pp. "
               "{f} million working-age people do not participate: {h} million do household work and {e} million study."),
    # graficos
    "g_ramas": ("Empleos creados o perdidos en un año, por rama (miles)", "Jobs created or lost over a year, by sector (thousands)"),
    "h_ramas": ("Ocupados (promedio de los últimos 3 meses) menos los del mismo periodo del año anterior. Azul: crea empleo; naranja: lo pierde.",
                "Employed (average of the last 3 months) minus the same period a year earlier. Blue: creating jobs; orange: losing them."),
    "g_ramas19": ("Empleo por rama frente a 2019", "Employment by sector versus 2019"),
    "h_ramas19": ("Ocupados de los últimos 12 meses frente al promedio de 2019, por rama de actividad.", "Employed over the last 12 months versus the 2019 average, by sector."),
    "g_pos": ("¿Cómo trabajan los colombianos? Composición del empleo", "How do Colombians work? Composition of employment"),
    "h_pos": ("Participación de cada posición ocupacional en el total de ocupados, promedio de 12 meses. La franja azul (asalariados privados) es el empleo con contrato y, en su mayoría, formal.",
              "Share of each occupational status in total employment, 12-month average. The blue band (private wage employees) is employment with a contract and mostly formal."),
    "g_posd": ("Cambio en un año por posición ocupacional (miles)", "Change over a year by occupational status (thousands)"),
    "h_posd": ("Ocupados de los últimos 3 meses frente al mismo periodo del año anterior.", "Employed over the last 3 months versus the same period a year earlier."),
    "g_gtd": ("Desempleo de mujeres y hombres", "Unemployment, women and men"),
    "h_gtd": ("Tasa de desempleo, promedio de 12 meses (sin desestacionalizar).", "Unemployment rate, 12-month average (not seasonally adjusted)."),
    "g_gtgp": ("Participación laboral de mujeres y hombres", "Labour participation, women and men"),
    "h_gtgp": ("Tasa global de participación: porcentaje de las personas en edad de trabajar que trabajan o buscan trabajo. Promedio de 12 meses.",
               "Participation rate: share of working-age people who work or look for work. 12-month average."),
    "lbl_m": ("Mujeres", "Women"), "lbl_h": ("Hombres", "Men"), "lbl_total": ("Total nacional", "National total"),
    "g_jtd": ("Desempleo juvenil (15 a 28 años)", "Youth unemployment (15 to 28)"),
    "h_jtd": ("Trimestre móvil. Línea gris: desempleo de toda la población, como referencia.", "Rolling quarter. Grey line: unemployment for the whole population, for reference."),
    "lbl_jov": ("Jóvenes", "Young people"), "lbl_jm": ("Mujeres jóvenes", "Young women"), "lbl_jh": ("Hombres jóvenes", "Young men"),
    "g_nini": ("Jóvenes que ni estudian ni están ocupados", "Young people neither studying nor employed"),
    "h_nini": ("Porcentaje del total de jóvenes de 15 a 28 años, dividido entre mujeres y hombres (la suma es el total). Trimestre móvil.",
               "Share of all 15–28 year-olds, split between women and men (they add up to the total). Rolling quarter."),
    "g_area": ("Desempleo en las cabeceras y en el campo", "Unemployment in urban and rural areas"),
    "h_area": ("Cabeceras: cascos urbanos de los municipios. Campo: centros poblados y rural disperso. Trimestre móvil.",
               "Urban: municipal town centres. Rural: villages and dispersed rural areas. Rolling quarter."),
    "lbl_cab": ("Cabeceras", "Urban"), "lbl_rur": ("Campo", "Rural"),
    "g_fuera": ("¿Por qué no participan? Población fuera de la fuerza de trabajo", "Why don't they participate? Population outside the labour force"),
    "h_fuera": ("Millones de personas en edad de trabajar que ni trabajan ni buscan trabajo, según su actividad principal. Promedio de 12 meses.",
                "Millions of working-age people who neither work nor look for work, by main activity. 12-month average."),
    "lbl_hog": ("Oficios del hogar", "Household work"), "lbl_est": ("Estudiando", "Studying"), "lbl_otr": ("Otros (pensionados, rentistas, incapacitados)", "Other (retired, rentiers, disabled)"),
}
RAMA = {"agro": ("Agro y pesca", "Farming and fishing"), "electricidad_mineria": ("Minería y servicios públicos", "Mining and utilities"),
        "industria": ("Industria", "Manufacturing"), "construccion": ("Construcción", "Construction"), "comercio": ("Comercio", "Trade"),
        "alojamiento": ("Alojamiento y comida", "Accommodation and food"), "transporte": ("Transporte", "Transport"),
        "informacion": ("Comunicaciones", "Communications"), "finanzas": ("Finanzas", "Finance"), "inmobiliarias": ("Inmobiliarias", "Real estate"),
        "profesionales": ("Serv. profesionales y administrativos", "Professional and admin services"),
        "gobierno": ("Gobierno, educación y salud", "Government, education and health"), "arte": ("Arte, hogares y otros", "Arts, households and other")}
POS = {"asalariado_privado": ("Asalariado privado", "Private wage employee"), "cuenta_propia": ("Cuenta propia", "Own-account worker"),
       "asalariado_publico": ("Asalariado del Gobierno", "Government employee"), "domestico": ("Empleo doméstico", "Domestic worker"),
       "empleador": ("Empleador", "Employer"), "jornalero": ("Jornalero o peón", "Day labourer"), "sin_remuneracion": ("Familiar sin pago", "Unpaid family worker")}
LITERATURA = [
    ("OIT (2013). Resolución sobre las estadísticas del trabajo, la ocupación y la subutilización de la fuerza de trabajo. 19.ª CIET.",
     "Definiciones de ocupación, desocupación, fuerza de trabajo y subutilización.", "Definitions of employment, unemployment, labour force and underutilisation."),
    ("OIT (1993). Resolución sobre la Clasificación Internacional de la Situación en el Empleo (CISE-93). 15.ª CIET.",
     "Posiciones ocupacionales: asalariados, cuenta propia, empleadores, familiares.", "Status in employment: employees, own-account, employers, family workers."),
    ("Maloney, W. F. (2004). Informality Revisited. <i>World Development</i>, 32(7), 1159–1178.",
     "La informalidad y el trabajo por cuenta propia como elección y como segmentación.", "Informality and self-employment as choice versus segmentation."),
    ("Goldin, C. (2014). A Grand Gender Convergence: Its Last Chapter. <i>American Economic Review</i>, 104(4), 1091–1119.",
     "Brechas de participación y resultados laborales entre mujeres y hombres.", "Gaps in participation and labour outcomes between women and men."),
    ("Bell, D. N. F. y Blanchflower, D. G. (2011). Young People and the Great Recession. <i>Oxford Review of Economic Policy</i>, 27(2), 241–267.",
     "Desempleo juvenil y cicatrices de largo plazo.", "Youth unemployment and long-term scarring."),
    ("DANE. Gran Encuesta Integrada de Hogares: metodología y marco conceptual (2021).", "Fuente de todos los datos de esta página.", "Source of all data on this page."),
]


def tx(k, L):
    return TX[k][0 if L == "es" else 1]


def cargar():
    arch = {k: f"empleo_{k}.csv" for k in ("ramas", "posicion", "sexo", "fuera_ft", "area", "jovenes")}
    if not all((DATA_DIR / f).exists() for f in arch.values()):
        return None
    return {k: pd.read_csv(DATA_DIR / f, parse_dates=["fecha"]) for k, f in arch.items()}


def medidas(E):
    r = E["ramas"].pivot(index="fecha", columns="rama", values="ocupados").sort_index()
    p = E["posicion"].pivot(index="fecha", columns="posicion", values="ocupados").sort_index().drop(columns="otro", errors="ignore")
    s = E["sexo"].pivot(index="fecha", columns="sexo", values=["td", "tgp", "to"]).sort_index()
    f = E["fuera_ft"].set_index("fecha").sort_index()
    a = E["area"].pivot(index="fecha", columns="area", values="td").sort_index()
    j = E["jovenes"].set_index("fecha").sort_index()
    p12 = p.rolling(12).mean()
    sh = 100 * p12.div(p12.sum(axis=1), axis=0)
    asal = sh["asalariado_privado"] + sh["asalariado_publico"]
    r3, p3 = r.rolling(3).mean(), p.rolling(3).mean()
    return {"r": r, "dr": (r3.iloc[-1] - r3.iloc[-13]), "r19": 100 * (r.rolling(12).mean().iloc[-1] / r.loc["2019"].mean() - 1),
            "sh": sh.dropna(), "asal": asal.dropna(), "dp": (p3.iloc[-1] - p3.iloc[-13]),
            "s12": s.rolling(12).mean().dropna(), "f12": f.rolling(12).mean().dropna(), "a": a, "j": j,
            "ocup12": r.sum(axis=1).rolling(12).mean()}


def construir_empleo(d, L, s_ciudades=""):
    """Devuelve (antes, despues)."""
    from colombiamacro.sitio import construir as cs
    num, fecha = cs.num, cs.fecha
    cs.LANG_ACTUAL[0] = L
    pct = lambda v, dec=1, sg=False: num(float(v), dec, L, sg, "%")
    k = 0 if L == "es" else 1
    E = cargar()
    if E is None:
        return "", s_ciudades
    M = medidas(E)

    def seccion(sid, titulo, resp, cuerpo):
        return (f'<section id="{sid}" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{titulo}</h2></div>'
                f'{cs.respuesta_html(resp, L)}{cuerpo}</section>')

    def lec(kk, v, dsc, tono, href):
        return (f'<a class="lec {tono}" href="{href}"><span class="lec-k">{kk}</span><b class="lec-v">{v}</b>'
                f'<span class="lec-d">{dsc}</span></a>')

    lab = d.laboral.set_index("fecha").sort_index()
    ul = lab.iloc[-1]
    hace = lab.loc[:lab.index[-1] - pd.DateOffset(years=1)].iloc[-1]
    oc = M["ocup12"].dropna()
    d_oc = oc.iloc[-1] - oc.iloc[-13]
    inf = d.informalidad
    s12, j = M["s12"], M["j"].dropna(subset=["td"])
    gap = s12[("td", "mujeres")] - s12[("td", "hombres")]
    j19 = M["j"].loc["2019"].mean()
    asal19 = M["asal"].loc["2019-12-01"] if pd.Timestamp("2019-12-01") in M["asal"].index else float("nan")
    jy = j.loc[:j.index[-1] - pd.DateOffset(years=1)].iloc[-1]
    tiles = [
        lec(tx("l_ocu", L), num(oc.iloc[-1] / 1000, 1, L), tx("l_ocu_d", L).format(v=num(d_oc, 0, L, True)), "ok" if d_oc >= 0 else "warn", "#emp-ramas"),
        lec(tx("l_to", L), pct(ul["to_sa"]), tx("l_to_d", L).format(v=num(ul["to_sa"] - hace["to_sa"], 1, L, True, " pp")),
            "ok" if ul["to_sa"] >= hace["to_sa"] else "warn", "#informalidad"),
        lec(tx("l_td", L), pct(ul["td_sa"]), tx("l_td_d", L).format(m=fecha(lab.index[-1], "m", L), v=pct(hace["td_sa"])),
            "ok" if ul["td_sa"] <= hace["td_sa"] else "warn", "#informalidad"),
    ]
    if inf is not None and not inf.empty:
        ui = inf.iloc[-1]
        ai = inf[inf["fecha"] <= ui["fecha"] - pd.DateOffset(years=1)]
        tiles.append(lec(tx("l_inf", L), pct(ui["nacional"]), tx("l_inf_d", L).format(p=fecha(ui["fecha"], "m", L), v=pct(ai.iloc[-1]["nacional"]) if not ai.empty else "—"),
                         "ok" if ai.empty or ui["nacional"] <= ai.iloc[-1]["nacional"] else "warn", "#informalidad"))
    tiles += [
        lec(tx("l_asal", L), pct(M["asal"].iloc[-1]), tx("l_asal_d", L).format(v=pct(asal19)), "ok" if M["asal"].iloc[-1] >= asal19 else "warn", "#emp-posicion"),
        lec(tx("l_gen", L), num(gap.iloc[-1], 1, L, False, " pp"), tx("l_gen_d", L).format(m=pct(s12[("td", "mujeres")].iloc[-1]), h=pct(s12[("td", "hombres")].iloc[-1])),
            "warn", "#emp-genero"),
        lec(tx("l_jov", L), pct(j["td"].iloc[-1]), tx("l_jov_d", L).format(p=fecha(j.index[-1], "m", L), v=pct(jy["td"])),
            "ok" if j["td"].iloc[-1] <= jy["td"] else "warn", "#emp-jovenes"),
        lec(tx("l_nini", L), pct(j["nini"].iloc[-1]), tx("l_nini_d", L).format(v=pct(j19["nini"])), "ok" if j["nini"].iloc[-1] <= j19["nini"] else "warn", "#emp-jovenes"),
    ]
    clase = "ocho" if len(tiles) == 8 else "seis"
    r0 = tx("r_medidas", L).format(o=num(oc.iloc[-1] / 1000, 1, L), d=num(d_oc, 0, L, True), td=pct(ul["td_sa"]), a=pct(M["asal"].iloc[-1]),
                                   a19=pct(asal19), g=num(gap.iloc[-1], 1, L), n=pct(j["nini"].iloc[-1]))
    antes = seccion("emp-medidas", tx("s_medidas", L), r0, f'<div class="lecturas {clase}">{"".join(tiles)}</div>')

    # ------------------------------------------------ ramas
    dr = M["dr"].sort_values()
    f1 = cs.base(L, height=420, fecha_x=False, suffix="")
    f1.add_trace(go.Bar(y=[RAMA[x][k] for x in dr.index], x=dr.round(1), orientation="h", showlegend=False,
                        marker=dict(color=[cs.C1 if v >= 0 else cs.C2 for v in dr], line=dict(width=0)),
                        text=[num(v, 0, L, True) for v in dr], textposition="outside", cliponaxis=False, hovertemplate="%{y}: %{x:,.0f}<extra></extra>"))
    f1.add_vline(x=0, line=dict(color=cs.INK2, width=1))
    m_ = max(abs(dr.min()), abs(dr.max())) * 1.35
    f1.update_xaxes(range=[-m_, m_], showgrid=True, gridcolor=cs.GRID)
    f1.update_yaxes(ticksuffix="", tickfont=dict(size=12, color=cs.INK2))
    f1.update_layout(hovermode="closest", bargap=0.3)
    g1 = cs.bloque_grafico(tx("g_ramas", L), cs.fig_html(f1, {"notime": True}, "g-emp-ramas"), tx("h_ramas", L))
    r19 = M["r19"].sort_values()
    f2 = cs.base(L, height=420, fecha_x=False)
    f2.add_trace(go.Bar(y=[RAMA[x][k] for x in r19.index], x=r19.round(2), orientation="h", showlegend=False,
                        marker=dict(color=[cs.C3 if v >= 0 else cs.C2 for v in r19], line=dict(width=0)),
                        text=[num(v, 1, L, True, "%") for v in r19], textposition="outside", cliponaxis=False, hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
    f2.add_vline(x=0, line=dict(color=cs.INK2, width=1))
    f2.update_xaxes(range=[min(-10, r19.min() * 1.4), r19.max() * 1.25], ticksuffix="%", showgrid=True, gridcolor=cs.GRID)
    f2.update_yaxes(ticksuffix="", tickfont=dict(size=12, color=cs.INK2))
    f2.update_layout(hovermode="closest", bargap=0.3)
    g2 = cs.bloque_grafico(tx("g_ramas19", L), cs.fig_html(f2, {"notime": True}, "g-emp-ramas-2019"), tx("h_ramas19", L))
    rn = lambda x: RAMA[x][k].lower() if L == "es" else RAMA[x][k]
    r1 = tx("r_ramas", L).format(r1=rn(dr.index[-1]), v1=num(dr.iloc[-1], 0, L), r2=rn(dr.index[-2]), v2=num(dr.iloc[-2], 0, L),
                                 r3=rn(dr.index[0]), v3=num(abs(dr.iloc[0]), 0, L), s1=rn(r19.index[-1]), p1=num(r19.iloc[-1], 1, L, True, "%"),
                                 s2=rn(r19.index[0]), p2=num(r19.iloc[0], 1, L, True, "%"))
    s_ram = seccion("emp-ramas", tx("s_ramas", L), r1, f'<div class="grid">{g1}{g2}</div>')

    # ------------------------------------------------ posicion ocupacional
    orden = [("asalariado_privado", cs.C1), ("cuenta_propia", cs.C2), ("asalariado_publico", cs.C3), ("domestico", cs.C7),
             ("empleador", cs.C4), ("jornalero", "#0f8fa3"), ("sin_remuneracion", "#8a6d3b")]
    sh = M["sh"].loc["2011":]
    f3 = cs.base(L, height=360)
    for col, color in orden:
        f3.add_trace(go.Scatter(x=sh.index + pd.offsets.MonthEnd(0), y=sh[col].round(2), name=POS[col][k], mode="lines", stackgroup="uno",
                                line=dict(width=0.6, color=color), fillcolor=color, hovertemplate="%{y:.1f}%"))
    f3.update_yaxes(range=[0, 100])
    g3 = cs.bloque_grafico(tx("g_pos", L), cs.fig_html(f3, {"noy": True}, "g-emp-posicion"), tx("h_pos", L))
    dp = M["dp"].reindex([c for c, _ in orden]).dropna().sort_values()
    f4 = cs.base(L, height=360, fecha_x=False, suffix="")
    f4.add_trace(go.Bar(y=[POS[x][k] for x in dp.index], x=dp.round(1), orientation="h", showlegend=False,
                        marker=dict(color=[cs.C1 if v >= 0 else cs.C2 for v in dp], line=dict(width=0)),
                        text=[num(v, 0, L, True) for v in dp], textposition="outside", cliponaxis=False, hovertemplate="%{y}: %{x:,.0f}<extra></extra>"))
    f4.add_vline(x=0, line=dict(color=cs.INK2, width=1))
    m_ = max(abs(dp.min()), abs(dp.max())) * 1.4
    f4.update_xaxes(range=[-m_, m_], showgrid=True, gridcolor=cs.GRID)
    f4.update_yaxes(ticksuffix="", tickfont=dict(size=12, color=cs.INK2))
    f4.update_layout(hovermode="closest", bargap=0.3)
    g4 = cs.bloque_grafico(tx("g_posd", L), cs.fig_html(f4, {"notime": True}, "g-emp-posicion-cambio"), tx("h_posd", L))
    us = M["sh"].iloc[-1]
    r2 = tx("r_posicion", L).format(p=pct(us["asalariado_privado"]), c=pct(us["cuenta_propia"]), dp=num(M["dp"]["asalariado_privado"], 0, L, True),
                                    dc=num(M["dp"]["cuenta_propia"], 0, L, True),
                                    txt=tx("pos_mejor" if M["dp"]["asalariado_privado"] > M["dp"]["cuenta_propia"] else "pos_peor", L))
    s_pos = seccion("emp-posicion", tx("s_posicion", L), r2, f'<div class="grid">{g3}{g4}</div>')

    # ------------------------------------------------ genero
    sx = s12.loc["2011":]
    f5 = cs.base(L, height=330)
    cs.linea(f5, sx.index + pd.offsets.MonthEnd(0), sx[("td", "mujeres")], tx("lbl_m", L), cs.C2, width=2.4, lang=L)
    cs.linea(f5, sx.index + pd.offsets.MonthEnd(0), sx[("td", "hombres")], tx("lbl_h", L), cs.C1, width=2.4, lang=L)
    f5.update_yaxes(rangemode="tozero")
    g5 = cs.bloque_grafico(tx("g_gtd", L), cs.fig_html(f5, {"noy": True}, "g-emp-genero-td"), tx("h_gtd", L))
    f6 = cs.base(L, height=330)
    cs.linea(f6, sx.index + pd.offsets.MonthEnd(0), sx[("tgp", "mujeres")], tx("lbl_m", L), cs.C2, width=2.4, lang=L)
    cs.linea(f6, sx.index + pd.offsets.MonthEnd(0), sx[("tgp", "hombres")], tx("lbl_h", L), cs.C1, width=2.4, lang=L)
    f6.update_yaxes(range=[40, 90])
    g6 = cs.bloque_grafico(tx("g_gtgp", L), cs.fig_html(f6, {"noy": True}, "g-emp-genero-tgp"), tx("h_gtgp", L))
    g19 = (s12[("td", "mujeres")] - s12[("td", "hombres")]).get(pd.Timestamp("2019-12-01"), float("nan"))
    f12 = M["f12"].iloc[-1]
    r3 = tx("r_genero", L).format(m=pct(s12[("td", "mujeres")].iloc[-1]), h=pct(s12[("td", "hombres")].iloc[-1]), g=num(gap.iloc[-1], 1, L),
                                  g19=num(g19, 1, L), pm=pct(s12[("tgp", "mujeres")].iloc[-1]), ph=pct(s12[("tgp", "hombres")].iloc[-1]),
                                  fh=_fuera_mujeres(E, num, L))
    s_gen = seccion("emp-genero", tx("s_genero", L), r3, f'<div class="grid">{g5}{g6}</div>')

    # ------------------------------------------------ jovenes
    jj = j.loc["2011":]
    xj = jj.index + pd.offsets.MonthEnd(0)
    f7 = cs.base(L, height=330)
    cs.linea(f7, xj, jj["td_m"], tx("lbl_jm", L), cs.C2, width=2.0, lang=L)
    cs.linea(f7, xj, jj["td"], tx("lbl_jov", L), cs.C1, width=2.6, lang=L)
    cs.linea(f7, xj, jj["td_h"], tx("lbl_jh", L), cs.C3, width=2.0, lang=L)
    tdn = lab["td_sa"].loc["2011":]
    cs.linea(f7, tdn.index + pd.offsets.MonthEnd(0), tdn, tx("lbl_total", L), cs.GRAY, width=1.5, dash="dot", lang=L)
    f7.update_yaxes(rangemode="tozero")
    g7 = cs.bloque_grafico(tx("g_jtd", L), cs.fig_html(f7, {"noy": True}, "g-emp-jovenes"), tx("h_jtd", L))
    f8 = cs.base(L, height=330)
    for col, lbl, color in (("nini_m", "lbl_m", cs.C2), ("nini_h", "lbl_h", cs.C1)):
        f8.add_trace(go.Scatter(x=xj, y=jj[col].round(2), name=tx(lbl, L), mode="lines", stackgroup="uno",
                                line=dict(width=0.6, color=color), fillcolor=color, hovertemplate="%{y:.1f}%"))
    f8.update_yaxes(rangemode="tozero")
    g8 = cs.bloque_grafico(tx("g_nini", L), cs.fig_html(f8, {"noy": True}, "g-emp-nini"), tx("h_nini", L))
    r4 = tx("r_jovenes", L).format(t=pct(j["td"].iloc[-1]), p=fecha(j.index[-1], "m", L), x=num(j["td"].iloc[-1] / ul["td_sa"], 1, L),
                                   m=pct(j["td_m"].iloc[-1]), n=pct(j["nini"].iloc[-1]), n19=pct(j19["nini"]),
                                   sm=pct(100 * j["nini_m"].iloc[-1] / j["nini"].iloc[-1], 0))
    s_jov = seccion("emp-jovenes", tx("s_jovenes", L), r4, f'<div class="grid">{g7}{g8}</div>')

    # ------------------------------------------------ area y fuera de la fuerza de trabajo
    a = M["a"].loc["2011":].dropna(subset=["cabeceras", "rural"])
    f9 = cs.base(L, height=330)
    cs.linea(f9, a.index + pd.offsets.MonthEnd(0), a["cabeceras"], tx("lbl_cab", L), cs.C1, width=2.4, lang=L)
    cs.linea(f9, a.index + pd.offsets.MonthEnd(0), a["rural"], tx("lbl_rur", L), cs.C3, width=2.4, lang=L)
    f9.update_yaxes(rangemode="tozero")
    g9 = cs.bloque_grafico(tx("g_area", L), cs.fig_html(f9, {"noy": True}, "g-emp-area"), tx("h_area", L))
    ff = M["f12"].loc["2011":] / 1000
    f10 = cs.base(L, height=330, suffix="")
    for col, lbl, color in (("hogar", "lbl_hog", cs.C2), ("estudiando", "lbl_est", cs.C1), ("otros", "lbl_otr", cs.C7)):
        f10.add_trace(go.Scatter(x=ff.index + pd.offsets.MonthEnd(0), y=ff[col].round(2), name=tx(lbl, L), mode="lines", stackgroup="uno",
                                 line=dict(width=0.6, color=color), fillcolor=color, hovertemplate="%{y:.1f} M"))
    g10 = cs.bloque_grafico(tx("g_fuera", L), cs.fig_html(f10, {"noy": True}, "g-emp-fuera"), tx("h_fuera", L))
    r5 = tx("r_area", L).format(c=pct(a["cabeceras"].iloc[-1]), r=pct(a["rural"].iloc[-1]), x=num(abs(a["cabeceras"].iloc[-1] - a["rural"].iloc[-1]), 1, L), p=fecha(a.index[-1], "m", L),
                                f=num(f12.sum() / 1000, 1, L), h=num(f12["hogar"] / 1000, 1, L), e=num(f12["estudiando"] / 1000, 1, L))
    s_area = seccion("emp-area", tx("s_area", L), r5, f'<div class="grid">{g9}{g10}</div>')

    items = "".join(f'<li><span class="ref">{ref}</span><span class="ref-u">{es if L == "es" else en}</span></li>' for ref, es, en in LITERATURA)
    s_lit = (f'<section id="emp-literatura" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{tx("s_lit", L)}</h2></div>'
             f'<ol class="refs">{items}</ol></section>')
    return antes, s_ram + s_pos + s_gen + s_jov + s_area + s_ciudades + s_lit


def _fuera_mujeres(E, num, L):
    """Mujeres fuera de la fuerza de trabajo (millones), promedio de 12 meses."""
    sx = E["sexo"]
    if "fuera_ft" not in sx:
        return "—"
    m = sx[sx["sexo"] == "mujeres"].set_index("fecha").sort_index()["fuera_ft"].rolling(12).mean().dropna()
    return num(m.iloc[-1] / 1000, 1, L) if not m.empty else "—"
