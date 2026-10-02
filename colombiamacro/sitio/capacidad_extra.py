"""Pagina de capacidad ampliada (v12.7): seis medidas de holgura, brecha por sector, holgura laboral
(subutilizacion de la fuerza de trabajo, OIT), mapa de las regiones (crecimiento, tamano frente a 2019,
PIB por persona y desempleo de la capital), estructura productiva y diversificacion de cada
departamento, y desempleo por ciudad.

Solo datos observados (DANE); nada se proyecta. Colores de origen: app.js los adapta al tema.
"""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from colombiamacro import analitica as am
from colombiamacro.config import DATA_DIR

TX = {
    "s_medidas": ("La capacidad en seis medidas", "Capacity in six measures"),
    "s_sectores": ("¿Qué sectores trabajan por encima o por debajo de su capacidad?", "Which sectors run above or below capacity?"),
    "s_laboral": ("¿Cuánta holgura hay en el mercado laboral?", "How much slack is there in the labour market?"),
    "s_regiones": ("¿Dónde está la capacidad? Las regiones", "Where is the capacity? The regions"),
    "s_estructura": ("¿De qué vive cada región?", "What does each region live on?"),
    "s_ciudades": ("Desempleo en las 32 capitales", "Unemployment in the 32 capital cities"),
    "s_lit": ("Bases metodológicas y literatura", "Methodological basis and literature"),
    # lecturas
    "l_cons": ("Brecha del producto", "Output gap"), "l_cons_d": ("mediana de 5 métodos · rango {lo} a {hi}", "median of 5 methods · range {lo} to {hi}"),
    "l_sec": ("Sectores sobre su tendencia", "Sectors above trend"), "l_sec_d": ("de 12 · más apretado: {s}", "of 12 · tightest: {s}"),
    "l_u": ("Desempleo frente a su tendencia", "Unemployment vs trend"), "l_u_d": ("{t} · desempleo {v} ({q})", "{t} · unemployment {v} ({q})"),
    "u_bajo": ("por debajo: mercado laboral apretado", "below: tight labour market"), "u_alto": ("por encima: hay holgura", "above: there is slack"),
    "l_sub": ("Subutilización laboral", "Labour underutilisation"), "l_sub_d": ("de la fuerza de trabajo ampliada (12 meses) · hace un año {v}", "of the extended labour force (12 months) · a year ago {v}"),
    "l_reg": ("Regiones más grandes que en 2019", "Regions larger than in 2019"), "l_reg_d": ("de 33 departamentos ({a})", "of 33 departments ({a})"),
    "l_div": ("Región más concentrada", "Most concentrated region"), "l_div_d": ("{s}: {v} de su economía", "{s}: {v} of its economy"),
    # respuestas
    "r_medidas": ("La economía produce {g} por encima de su capacidad según la mediana de cinco métodos, pero la holgura no es pareja. "
                  "Solo {k} de 12 sectores trabajan sobre su tendencia y el desempleo está {u} pp {dir_u} de la suya. "
                  "{n} de 33 departamentos ya producen más que en 2019; {lag} siguen por debajo.",
                  "The economy is producing {g} above capacity by the median of five methods, but slack is uneven. "
                  "Only {k} of 12 sectors run above trend and unemployment is {u} pp {dir_u} its own. "
                  "{n} of 33 departments already produce more than in 2019; {lag} remain below."),
    "debajo": ("por debajo", "below"), "encima": ("por encima", "above"),
    "r_sectores": ("{s1} es el sector más por encima de su tendencia ({v1}) y {s2} el más por debajo ({v2}). "
                   "Cuando pocos sectores están apretados, el crecimiento puede seguir sin presionar los precios de toda la economía; "
                   "la presión se concentra donde la brecha es positiva.",
                   "{s1} is the sector furthest above trend ({v1}) and {s2} the furthest below ({v2}). "
                   "When few sectors are stretched, growth can continue without pushing up economy-wide prices; "
                   "pressure concentrates where the gap is positive."),
    "r_laboral": ("El desempleo (desestacionalizado) es {td} y su tendencia {tr}. "
                  "La medida compuesta de subutilización de la OIT, que suma desempleados, subempleados por horas y quienes quieren trabajar pero no buscan, "
                  "llega a {m} de la fuerza de trabajo ampliada (promedio de 12 meses), frente a {m0} un año antes.",
                  "Unemployment (seasonally adjusted) is {td} and its trend {tr}. "
                  "The ILO composite measure of labour underutilisation, which adds the unemployed, the time-related underemployed and those who want to work but are not searching, "
                  "stands at {m} of the extended labour force (12-month average), versus {m0} a year earlier."),
    "r_regiones": ("En {a} la economía creció más en {d1} ({v1}) y cayó más en {d2} ({v2}). "
                   "Frente a 2019, {n} de 33 departamentos son más grandes; los más rezagados son {lag}{min_txt}. "
                   "Bogotá produce {bog} del PIB y su PIB por persona es {pcb} veces el de Colombia.",
                   "In {a} the economy grew most in {d1} ({v1}) and fell most in {d2} ({v2}). "
                   "Versus 2019, {n} of 33 departments are larger; the furthest behind are {lag}{min_txt}. "
                   "Bogotá produces {bog} of GDP and its GDP per person is {pcb} times Colombia's."),
    "min_si": (", economías donde la minería pesa {v} o más", ", economies where mining weighs {v} or more"),
    "r_estructura": ("La economía de {d1} depende en {v1} de {s1}; la de {d2}, en {v2} de {s2}. "
                     "Con el índice de Herfindahl, el departamento más diversificado es {div} (equivale a {nd} sectores del mismo tamaño) "
                     "y el más concentrado {con} ({nc}): una región concentrada tiene menos margen cuando su sector principal se frena.",
                     "{d1}'s economy depends {v1} on {s1}; {d2}'s, {v2} on {s2}. "
                     "By the Herfindahl index, the most diversified department is {div} (equivalent to {nd} equal-sized sectors) "
                     "and the most concentrated {con} ({nc}): a concentrated region has less room when its main sector slows."),
    "r_ciudades": ("En el año que termina en {m}, el desempleo va de {lo} en {c1} a {hi} en {c2}. "
                   "Bajó en {n} de 32 capitales frente al año anterior. Las tres con más desempleo son {top3}.",
                   "In the year to {m}, unemployment ranges from {lo} in {c1} to {hi} in {c2}. "
                   "It fell in {n} of 32 capitals versus a year earlier. The three with the highest unemployment are {top3}."),
    # graficos
    "g_heat": ("Brecha de cada sector frente a su tendencia", "Each sector's gap versus its trend"),
    "h_heat": ("Cada celda es un sector en un trimestre: azul, produce por encima de su tendencia (sin holgura); naranja, por debajo (con holgura). Los sectores van ordenados por la brecha más reciente.",
               "Each cell is a sector in a quarter: blue, producing above its trend (no slack); orange, below it (slack). Sectors are ordered by the latest gap."),
    "g_barras": ("Brecha de cada sector hoy ({q})", "Each sector's gap today ({q})"),
    "h_barras": ("Distancia porcentual entre lo que produce el sector y su tendencia. Azul: sobre su capacidad; naranja: con holgura.",
                 "Percentage distance between what the sector produces and its trend. Blue: above capacity; orange: slack."),
    "g_sub": ("Desempleo, subempleo y subutilización total (promedio de 12 meses)", "Unemployment, underemployment and total underutilisation (12-month average)"),
    "h_sub": ("Tres medidas de la OIT, de la más estrecha a la más amplia: tasa de desempleo; desempleo más subempleo por horas; y la medida compuesta, que agrega la fuerza de trabajo potencial (personas disponibles que no buscan).",
              "Three ILO measures, from narrowest to broadest: unemployment rate; unemployment plus time-related underemployment; and the composite measure, which adds the potential labour force (available people who are not searching)."),
    "lbl_td": ("Desempleo", "Unemployment"), "lbl_tcsd": ("Desempleo + subempleo", "Unemployment + underemployment"),
    "lbl_mcsft": ("Subutilización total", "Total underutilisation"),
    "g_ugap": ("Desempleo frente a su tendencia", "Unemployment versus its trend"),
    "h_ugap": ("Línea: tasa de desempleo desestacionalizada, promedio del trimestre. Punteada: su tendencia (Hodrick-Prescott, sin 2020–2021). Por debajo de la tendencia, el mercado laboral está apretado.",
               "Line: seasonally adjusted unemployment rate, quarterly average. Dotted: its trend (Hodrick-Prescott, excluding 2020–2021). Below trend, the labour market is tight."),
    "lbl_tend": ("Tendencia", "Trend"),
    "g_mapa": ("Mapa de las regiones", "Map of the regions"),
    "h_mapa": ("Mapa esquemático: cada casilla es un departamento, ubicado aproximadamente donde está. Elija la medida con los botones. Pase el cursor o toque una casilla para ver el detalle.",
               "Schematic map: each tile is a department, placed roughly where it is. Pick the measure with the buttons. Hover or tap a tile for details."),
    "m_crec": ("Crecimiento {a}", "Growth {a}"), "m_2019": ("Frente a 2019", "Versus 2019"), "m_pc": ("PIB por persona", "GDP per person"),
    "m_td": ("Desempleo de la capital", "Capital-city unemployment"),
    "leg_crec": ("Crecimiento real del PIB del departamento frente al año anterior.", "Real GDP growth of the department versus the previous year."),
    "leg_2019": ("Tamaño de la economía del departamento frente a 2019 (real).", "Size of the department's economy versus 2019 (real)."),
    "leg_pc": ("PIB por persona del departamento; Colombia = 100.", "Department GDP per person; Colombia = 100."),
    "leg_td": ("Tasa de desempleo de la ciudad capital, año móvil (más oscuro = más desempleo).", "Unemployment rate of the capital city, rolling year (darker = higher)."),
    "g_rank": ("Tamaño de cada economía regional frente a 2019", "Size of each regional economy versus 2019"),
    "h_rank": ("Variación del PIB real de cada departamento entre 2019 y {a}. La línea punteada es Colombia.",
               "Change in each department's real GDP between 2019 and {a}. The dotted line is Colombia."),
    "g_estr": ("Estructura productiva por departamento ({a})", "Production structure by department ({a})"),
    "h_estr": ("Participación de cada sector en el valor agregado del departamento, a precios corrientes. Más oscuro = más peso. Departamentos ordenados por tamaño.",
               "Each sector's share of the department's value added, at current prices. Darker = larger share. Departments ordered by size."),
    "g_div": ("Diversificación: número equivalente de sectores", "Diversification: equivalent number of sectors"),
    "h_div": ("Inverso del índice de Herfindahl-Hirschman de las participaciones sectoriales (1/Σs²). Con 12 sectores iguales el valor sería 12; cuanto más bajo, más depende la región de pocos sectores.",
              "Inverse Herfindahl-Hirschman index of sector shares (1/Σs²). With 12 equal sectors it would be 12; the lower it is, the more the region depends on a few sectors."),
    "g_ciud": ("Tasa de desempleo por ciudad capital, año móvil", "Unemployment rate by capital city, rolling year"),
    "h_ciud": ("Punto gris: el año móvil terminado un año antes. Punto de color: el más reciente. Verde si bajó; naranja si subió.",
               "Grey dot: the rolling year ending a year earlier. Coloured dot: the latest. Green if it fell; orange if it rose."),
    "lbl_hace": ("Hace un año", "A year ago"), "lbl_hoy": ("Hoy", "Now"),
}
RAMA_N = {"agro": ("Agro", "Farming"), "mineria": ("Minería", "Mining"), "industria": ("Industria", "Manufacturing"),
          "electricidad": ("Energía y agua", "Utilities"), "construccion": ("Construcción", "Construction"),
          "comercio": ("Comercio y transporte", "Trade and transport"), "informacion": ("Comunicaciones", "Communications"),
          "finanzas": ("Finanzas", "Finance"), "inmobiliarias": ("Inmobiliarias", "Real estate"),
          "profesionales": ("Serv. profesionales", "Prof. services"), "gobierno": ("Gobierno, educ. y salud", "Gov., educ. and health"),
          "arte": ("Arte y otros", "Arts and other")}
# mapa esquematico: (columna, fila) aproximadas; abreviatura
TILES = {
    "88": (0, 0, "SAP"), "44": (5, 1, "GUA"), "08": (3, 1, "ATL"), "47": (4, 1, "MAG"),
    "23": (2, 2, "COR"), "70": (3, 2, "SUC"), "13": (4, 2, "BOL"), "20": (5, 2, "CES"),
    "27": (1, 3, "CHO"), "05": (2, 3, "ANT"), "68": (3, 3, "SAN"), "54": (4, 3, "NSA"), "81": (5, 3, "ARA"),
    "66": (1, 4, "RIS"), "17": (2, 4, "CAL"), "25": (3, 4, "CUN"), "15": (4, 4, "BOY"), "85": (5, 4, "CAS"), "99": (6, 4, "VID"),
    "76": (1, 5, "VAL"), "63": (2, 5, "QUI"), "73": (3, 5, "TOL"), "11": (4, 5, "BOG"), "50": (5, 5, "MET"), "94": (6, 5, "GUN"),
    "19": (1, 6, "CAU"), "41": (2, 6, "HUI"), "18": (3, 6, "CAQ"), "95": (4, 6, "GUV"), "97": (5, 6, "VAU"),
    "52": (1, 7, "NAR"), "86": (2, 7, "PUT"), "91": (3, 7, "AMA"),
}
CAPITAL = {"11": "Bogotá D.C.", "05": "Medellín A.M.", "76": "Cali A.M.", "08": "Barranquilla A.M.", "68": "Bucaramanga A.M.",
           "17": "Manizales A.M.", "52": "Pasto", "66": "Pereira A.M.", "54": "Cúcuta A.M.", "73": "Ibagué", "23": "Montería",
           "13": "Cartagena", "50": "Villavicencio", "15": "Tunja", "18": "Florencia", "19": "Popayán", "20": "Valledupar",
           "27": "Quibdó", "41": "Neiva", "44": "Riohacha", "47": "Santa Marta", "63": "Armenia", "70": "Sincelejo", "81": "Arauca",
           "85": "Yopal", "86": "Mocoa", "91": "Leticia", "94": "Inírida", "95": "San José del Guaviare", "97": "Mitú",
           "99": "Puerto Carreño", "88": "San Andrés"}
NOMBRE_CORTO = {"San Andrés, Providencia y Santa Catalina (Archipiélago)": "San Andrés", "Bogotá D.C.": "Bogotá"}
LITERATURA = [
    ("Okun, A. M. (1962). Potential GNP: Its Measurement and Significance. <i>Proceedings of the Business and Economic Statistics Section</i>, ASA.",
     "Producto potencial y relación entre holgura del producto y del empleo.", "Potential output and the link between output and labour slack."),
    ("OIT (2013). Resolución sobre las estadísticas del trabajo, la ocupación y la subutilización de la fuerza de trabajo. 19.ª CIET.",
     "Definición de subocupación, fuerza de trabajo potencial y medida compuesta de subutilización.", "Definitions of underemployment, potential labour force and the composite underutilisation measure."),
    ("Hodrick, R. J. y Prescott, E. C. (1997). Postwar U.S. Business Cycles. <i>Journal of Money, Credit and Banking</i>, 29(1), 1–16.",
     "Tendencia de cada sector y del desempleo.", "Trend of each sector and of unemployment."),
    ("Hirschman, A. O. (1964). The Paternity of an Index. <i>American Economic Review</i>, 54(5), 761; Herfindahl, O. C. (1950). <i>Concentration in the Steel Industry</i>. Columbia University.",
     "Índice de concentración y número equivalente de sectores.", "Concentration index and equivalent number of sectors."),
    ("DANE. Cuentas nacionales departamentales, base 2015: metodología (CD-01).",
     "PIB y valor agregado por departamento y actividad.", "GDP and value added by department and activity."),
]


def tx(k, L):
    return TX[k][0 if L == "es" else 1]


def cargar():
    arch = ["pib_departamentos.csv", "pib_departamentos_ramas.csv", "laboral_ciudades.csv", "laboral_subutilizacion.csv"]
    if not all((DATA_DIR / f).exists() for f in arch):
        return None
    dep = pd.read_csv(DATA_DIR / arch[0], dtype={"codigo": str})
    ram = pd.read_csv(DATA_DIR / arch[1], dtype={"codigo": str})
    for x in (dep, ram):
        x["codigo"] = x["codigo"].str.zfill(2)
    return {"dep": dep, "ramas": ram,
            "ciudades": pd.read_csv(DATA_DIR / arch[2], parse_dates=["fecha"]),
            "sub": pd.read_csv(DATA_DIR / arch[3], parse_dates=["fecha"])}


def medidas(R, d):
    dep = R["dep"]
    a = int(dep["anio"].max())
    p = dep.pivot(index="anio", columns="codigo", values="pib_real")
    nom = dep.drop_duplicates("codigo").set_index("codigo")["departamento"].map(lambda n: NOMBRE_CORTO.get(n, n))
    crec = (p.loc[a] / p.loc[a - 1] - 1) * 100
    v19 = (p.loc[a] / p.loc[2019] - 1) * 100
    pc = dep[dep["anio"] == a].set_index("codigo")["pib_pc"]
    pc_idx = 100 * pc / pc["00"]
    peso = 100 * dep[dep["anio"] == a].set_index("codigo")["pib_corriente"] / dep[(dep["anio"] == a) & (dep["codigo"] == "00")]["pib_corriente"].iloc[0]
    ram = R["ramas"]
    ra = ram[(ram["anio"] == a) & (ram["rama"] != "impuestos") & (ram["codigo"] != "00")].pivot(index="codigo", columns="rama", values="va_corriente")
    sh = 100 * ra.div(ra.sum(axis=1), axis=0)
    hhi = ((sh / 100) ** 2).sum(axis=1)
    c = R["ciudades"]
    fin = c["fecha"].max()
    td = c[c["fecha"] == fin].set_index("ciudad")["td"]
    td0 = c[c["fecha"] == fin - pd.DateOffset(years=1)].set_index("ciudad")["td"]
    sub = R["sub"].set_index("fecha").sort_index()
    sub12 = sub.rolling(12, min_periods=12).mean()
    return {"a": a, "nom": nom, "crec": crec, "v19": v19, "pc_idx": pc_idx, "peso": peso, "sh": sh, "neq": 1 / hhi,
            "td": td, "td0": td0, "fin_c": fin, "sub12": sub12}


def _bucket(v, cortes):
    """Indice de color divergente -3..3 segun cortes ascendentes (6 valores)."""
    if v is None or pd.isna(v):
        return "na"
    k = int(np.searchsorted(cortes, v))
    return str(k - 3)


def construir_capacidad(d, s, L):
    """Devuelve (antes, despues). Si faltan los datos regionales devuelve solo lo nacional."""
    from colombiamacro.sitio import construir as cs
    num, fecha, esc = cs.num, cs.fecha, cs.esc
    cs.LANG_ACTUAL[0] = L
    pct = lambda v, dec=1, sg=True: num(float(v), dec, L, sg, "%")
    R = cargar()
    M = medidas(R, d) if R is not None else None

    def seccion(sid, titulo, resp, cuerpo):
        return (f'<section id="{sid}" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{titulo}</h2></div>'
                f'{cs.respuesta_html(resp, L)}{cuerpo}</section>')

    def lec(k, v, dsc, tono, href):
        return (f'<a class="lec {tono}" href="{href}"><span class="lec-k">{k}</span><b class="lec-v">{v}</b>'
                f'<span class="lec-d">{dsc}</span></a>')

    sec_es = d.sectores
    from colombiamacro.sitio.crecimiento_extra import SECTOR_EN
    sec_nombre = (lambda n: n) if L == "es" else (lambda n: SECTOR_EN.get(n, n))
    cons = am.brechas_consenso(d.pib, d.ciclo).dropna(subset=["mediana"]).iloc[-1]
    bs = am.brecha_sectores(sec_es).dropna(how="all")
    bu = bs.iloc[-1].dropna().sort_values()
    k = int((bu > 0).sum())
    ok = am.okun(am.brechas_consenso(d.pib, d.ciclo).set_index("fecha")["brecha_hp_dos_colas"], d.laboral.set_index("fecha")["td_sa"])
    ug = ok["serie"]["brecha_u"]
    tdq = d.laboral.set_index("fecha")["td_sa"].astype(float).resample("QS").mean()
    tend_u = (tdq - ug.reindex(tdq.index)).dropna()
    # tendencia del desempleo en todos los trimestres (HP sin 2020-2021, interpolada) para el grafico
    tdc = am.serie_sin_covid(tdq).dropna()
    tr_u = pd.Series(am.hp_trend(tdc.to_numpy()), index=tdc.index).reindex(tdq.index).interpolate()
    ul = float(ug.iloc[-1])

    tiles = [
        lec(tx("l_cons", L), pct(cons["mediana"]), tx("l_cons_d", L).format(lo=pct(cons["minimo"]), hi=pct(cons["maximo"])),
            "warn" if cons["mediana"] > 0.5 else "ok", "#capacidad"),
        lec(tx("l_sec", L), f"{k}", tx("l_sec_d", L).format(s=sec_nombre(bu.index[-1])), "ok" if k > 6 else "warn", "#cap-sectores"),
        lec(tx("l_u", L), num(ul, 1, L, True, " pp"), tx("l_u_d", L).format(t=tx("u_bajo" if ul < 0 else "u_alto", L),
                                                                            v=pct(tdq.dropna().iloc[-1], 1, False), q=fecha(tdq.dropna().index[-1], "q", L)),
            "warn" if ul < 0 else "ok", "#cap-laboral"),
    ]
    if M is not None:
        sub = M["sub12"]["mcsft"].dropna()
        hace = sub.loc[:sub.index[-1] - pd.DateOffset(years=1)]
        n19 = int((M["v19"].drop("00") > 0).sum())
        conc = M["sh"].max(axis=1).sort_values()
        dcon = conc.index[-1]
        tiles += [
            lec(tx("l_sub", L), pct(sub.iloc[-1], 1, False), tx("l_sub_d", L).format(v=pct(hace.iloc[-1], 1, False) if not hace.empty else "—"),
                "ok" if hace.empty or sub.iloc[-1] <= hace.iloc[-1] else "warn", "#cap-laboral"),
            lec(tx("l_reg", L), f"{n19}", tx("l_reg_d", L).format(a=M["a"]), "ok" if n19 >= 25 else "warn", "#cap-regiones"),
            lec(tx("l_div", L), M["nom"][dcon], tx("l_div_d", L).format(s=RAMA_N[M["sh"].loc[dcon].idxmax()][0 if L == "es" else 1].lower(),
                                                                       v=pct(conc.iloc[-1], 0, False)), "", "#cap-estructura"),
        ]
    lag = ", ".join(M["nom"][c] for c in M["v19"].drop("00").sort_values().index[:3]) if M is not None else "—"
    r0 = tx("r_medidas", L).format(g=pct(cons["mediana"]), k=k, u=num(abs(ul), 1, L), dir_u=tx("debajo" if ul < 0 else "encima", L),
                                   n=n19 if M is not None else "—", lag=lag)
    antes = seccion("cap-medidas", tx("s_medidas", L), r0, f'<div class="lecturas seis">{"".join(tiles)}</div>')

    # ------------------------------------------------ sectores
    hb = bs.loc["2016":].T.reindex(bu.index[::-1])
    xq = list(pd.DatetimeIndex(hb.columns) + pd.offsets.QuarterEnd(0))
    f1 = cs.base(L, height=440)
    f1.add_trace(go.Heatmap(x=xq, y=[sec_nombre(n) for n in hb.index], z=[[None if pd.isna(v) else round(float(v), 2) for v in fila] for fila in hb.values],
                            zmid=0, zmin=-8, zmax=8, colorscale=[[0, "#b04a17"], [0.35, "#f3c9b3"], [0.5, "#f7f6f2"], [0.65, "#bfd7f3"], [1, "#1f4f8f"]],
                            colorbar=dict(ticksuffix="%", thickness=10, len=0.9, outlinewidth=0, tickfont=dict(size=11, color=cs.MUTED)),
                            xgap=1, ygap=1, customdata=[[fecha(f, "q", L) for f in hb.columns]] * len(hb.index),
                            hovertemplate="<b>%{y}</b> · %{customdata}<br>%{z:.1f}%<extra></extra>"))
    f1.update_layout(hovermode="closest", showlegend=False)
    f1.update_yaxes(ticksuffix="", tickfont=dict(size=11.5, color=cs.INK2), gridcolor="rgba(0,0,0,0)")
    f1.update_xaxes(showline=False)
    g1 = cs.bloque_grafico(tx("g_heat", L), cs.fig_html(f1, {"noy": True, "notime": True}, "g-cap-sectores"), tx("h_heat", L))
    f2 = cs.base(L, height=440, fecha_x=False)
    f2.add_trace(go.Bar(y=[sec_nombre(n) for n in bu.index], x=bu.round(2), orientation="h", showlegend=False,
                        marker=dict(color=[cs.C1 if v >= 0 else cs.C2 for v in bu], line=dict(width=0)),
                        text=[pct(v) for v in bu], textposition="outside", cliponaxis=False, hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
    f2.add_vline(x=0, line=dict(color=cs.INK2, width=1))
    m_ = max(abs(bu.min()), abs(bu.max())) * 1.4
    f2.update_xaxes(range=[-m_, m_], ticksuffix="%", showgrid=True, gridcolor=cs.GRID)
    f2.update_yaxes(ticksuffix="", tickfont=dict(size=12, color=cs.INK2))
    f2.update_layout(hovermode="closest", bargap=0.3)
    g2 = cs.bloque_grafico(tx("g_barras", L).format(q=fecha(bs.index[-1], "q", L)), cs.fig_html(f2, {"notime": True}, "g-cap-sectores-hoy"), tx("h_barras", L))
    r1 = tx("r_sectores", L).format(s1=sec_nombre(bu.index[-1]), v1=pct(bu.iloc[-1]), s2=sec_nombre(bu.index[0]), v2=pct(bu.iloc[0]))
    s_sec = seccion("cap-sectores", tx("s_sectores", L), r1, f'<div class="grid">{g1}{g2}</div>')

    # ------------------------------------------------ laboral
    f4 = cs.base(L, height=330)
    xu = tdq.loc["2010":].dropna()
    cs.linea(f4, xu.index + pd.offsets.QuarterEnd(0), xu, tx("lbl_td", L), cs.C1, width=2.4, lang=L)
    tu = tr_u.loc["2010":].dropna()
    cs.linea(f4, tu.index + pd.offsets.QuarterEnd(0), tu, tx("lbl_tend", L), cs.INK2, width=1.6, dash="dot", lang=L)
    f4.update_yaxes(range=[0, 25])
    g4 = cs.bloque_grafico(tx("g_ugap", L), cs.fig_html(f4, {"noy": True}, "g-cap-desempleo"), tx("h_ugap", L))
    g3, r2 = "", tx("r_laboral", L).format(td=pct(tdq.dropna().iloc[-1], 1, False), tr=pct(tr_u.dropna().iloc[-1], 1, False), m="—", m0="—")
    if M is not None:
        s12 = M["sub12"].dropna(subset=["mcsft"])
        f3 = cs.base(L, height=330)
        for col, lbl, color, w in (("td", "lbl_td", cs.C1, 2.0), ("tcsd", "lbl_tcsd", cs.C3, 2.0), ("mcsft", "lbl_mcsft", cs.C2, 2.6)):
            cs.linea(f3, s12.index + pd.offsets.MonthEnd(0), s12[col], tx(lbl, L), color, width=w, lang=L)
        f3.update_yaxes(rangemode="tozero")
        g3 = cs.bloque_grafico(tx("g_sub", L), cs.fig_html(f3, {"noy": True}, "g-cap-subutilizacion"), tx("h_sub", L))
        m0 = s12["mcsft"].loc[:s12.index[-1] - pd.DateOffset(years=1)]
        r2 = tx("r_laboral", L).format(td=pct(tdq.dropna().iloc[-1], 1, False), tr=pct(tr_u.dropna().iloc[-1], 1, False),
                                       m=pct(s12["mcsft"].iloc[-1], 1, False), m0=pct(m0.iloc[-1], 1, False) if not m0.empty else "—")
    s_lab = seccion("cap-laboral", tx("s_laboral", L), r2, f'<div class="grid">{g3}{g4}</div>')

    if M is None:
        return antes, s_sec + s_lab, ""

    # ------------------------------------------------ regiones: mapa esquematico + ranking
    a = M["a"]
    td_dep = {c: M["td"].get(cap) for c, cap in CAPITAL.items()}
    metricas = {
        "crec": (M["crec"], [-2, -1, -0.25, 0.25, 1.5, 3], lambda v: pct(v)),
        "v19": (M["v19"], [-5, -1, 1, 8, 14, 20], lambda v: pct(v)),
        "pc": (M["pc_idx"], [40, 60, 85, 115, 140, 170], lambda v: num(v, 0, L)),
        "td": (pd.Series(td_dep, dtype=float), [7, 8.5, 10, 12, 15, 20], lambda v: pct(v, 1, False)),
    }
    celdas = []
    for cod, (cx, cy, ab) in TILES.items():
        attrs = []
        for m, (ser, cortes, fmt) in metricas.items():
            v = ser.get(cod)
            b = _bucket(v, cortes)
            if m == "td" and b != "na":
                b = str(-int(b))                    # mas desempleo = naranja
            attrs.append(f'data-{m}="{b}|{esc(fmt(v)) if v is not None and not pd.isna(v) else "—"}"')
        nombre = M["nom"].get(cod, cod)
        prin = M["sh"].loc[cod].idxmax() if cod in M["sh"].index else None
        tip = (f'{esc(nombre)} · {tx("m_crec", L).format(a=a)}: {pct(M["crec"][cod])} · {tx("m_2019", L)}: {pct(M["v19"][cod])} · '
               f'{tx("m_pc", L)}: {num(M["pc_idx"][cod], 0, L)} · {RAMA_N[prin][0 if L == "es" else 1] if prin else ""} {pct(M["sh"].loc[cod].max(), 0, False) if prin else ""}'
               + (f' · {tx("m_td", L)}: {pct(td_dep[cod], 1, False)}' if td_dep.get(cod) is not None else ""))
        celdas.append(f'<div class="tm-c" style="grid-column:{cx + 1};grid-row:{cy + 1}" tabindex="0" title="{tip}" {" ".join(attrs)}>'
                      f'<b>{ab}</b><span class="tm-v"></span></div>')
    botones = "".join(f'<button type="button" data-m="{m}"{" class=\"on\"" if m == "v19" else ""}>{esc(tx("m_" + ("2019" if m == "v19" else m), L).format(a=a))}</button>'
                      for m in ("crec", "v19", "pc", "td"))
    leyendas = "".join(f'<span class="tm-leg" data-m="{m}">{tx("leg_" + ("2019" if m == "v19" else m), L)}</span>' for m in ("crec", "v19", "pc", "td"))
    escala = "".join(f'<i class="tm-b{b}"></i>' for b in ("-3", "-2", "-1", "0", "1", "2", "3"))
    mapa = (f'<figure class="chart"><figcaption>{tx("g_mapa", L)}</figcaption>'
            f'<div class="tmapa" data-m="v19"><div class="tm-btn" role="group">{botones}</div>'
            f'<div class="tm-grid">{"".join(celdas)}</div><div class="tm-pie">{leyendas}<span class="tm-esc">{escala}</span></div></div>'
            f'<p class="how"><span>?</span>{tx("h_mapa", L)}</p>{cs.pie_ficha("g-cap-mapa", L)}</figure>')
    rk = M["v19"].drop("00").sort_values()
    f5 = cs.base(L, height=640, fecha_x=False)
    f5.add_trace(go.Bar(y=[M["nom"][c] for c in rk.index], x=rk.round(2), orientation="h", showlegend=False,
                        marker=dict(color=[cs.C1 if v >= 0 else cs.C2 for v in rk], line=dict(width=0)),
                        text=[pct(v) for v in rk], textposition="outside", cliponaxis=False, textfont=dict(size=10.5, color=cs.INK2),
                        hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
    f5.add_vline(x=float(M["v19"]["00"]), line=dict(color=cs.INK, width=1.2, dash="dot"))
    f5.add_vline(x=0, line=dict(color=cs.INK2, width=1))
    f5.update_xaxes(ticksuffix="%", showgrid=True, gridcolor=cs.GRID, range=[min(-10, rk.min() * 1.3), rk.max() * 1.25])
    f5.update_yaxes(ticksuffix="", tickfont=dict(size=11, color=cs.INK2))
    f5.update_layout(hovermode="closest", bargap=0.25)
    g5 = cs.bloque_grafico(tx("g_rank", L), cs.fig_html(f5, {"notime": True}, "g-cap-regiones"), tx("h_rank", L).format(a=a))
    cr = M["crec"].drop("00").sort_values()
    rez = list(rk.index[:3])
    mmin = min(M["sh"].loc[c_, "mineria"] for c_ in rez) if all(c_ in M["sh"].index for c_ in rez) else 0
    min_txt = tx("min_si", L).format(v=pct(mmin, 0, False)) if mmin >= 15 else ""
    r3 = tx("r_regiones", L).format(a=a, d1=M["nom"][cr.index[-1]], v1=pct(cr.iloc[-1]), d2=M["nom"][cr.index[0]], v2=pct(cr.iloc[0]),
                                    n=int((rk > 0).sum()), lag=lag, min_txt=min_txt, bog=pct(M["peso"]["11"], 0, False), pcb=num(M["pc_idx"]["11"] / 100, 1, L))
    s_reg = seccion("cap-regiones", tx("s_regiones", L), r3, f'<div class="grid">{mapa}{g5}</div>')

    # ------------------------------------------------ estructura + diversificacion
    orden = M["peso"].drop("00").sort_values(ascending=False).index
    sh = M["sh"].reindex(orden)
    cols = ["agro", "mineria", "industria", "electricidad", "construccion", "comercio", "informacion", "finanzas", "inmobiliarias",
            "profesionales", "gobierno", "arte"]
    sh = sh[cols]
    f6 = cs.base(L, height=760, fecha_x=False)
    f6.add_trace(go.Heatmap(x=[RAMA_N[c][0 if L == "es" else 1] for c in cols], y=[M["nom"][c] for c in sh.index],
                            z=sh.round(1).values.tolist(), zmin=0, zmax=40,
                            colorscale=[[0, "#f7f6f2"], [0.25, "#bfd7f3"], [0.6, "#5b9be3"], [1, "#1f4f8f"]],
                            colorbar=dict(ticksuffix="%", thickness=10, len=0.6, outlinewidth=0, tickfont=dict(size=11, color=cs.MUTED)),
                            xgap=1, ygap=1, hovertemplate="<b>%{y}</b> · %{x}: %{z:.1f}%<extra></extra>"))
    f6.update_layout(hovermode="closest", showlegend=False)
    f6.update_yaxes(autorange="reversed", ticksuffix="", tickfont=dict(size=11, color=cs.INK2), gridcolor="rgba(0,0,0,0)")
    f6.update_xaxes(side="top", tickangle=-40, showline=False, tickfont=dict(size=11, color=cs.INK2))
    g6 = cs.bloque_grafico(tx("g_estr", L).format(a=a), cs.fig_html(f6, {"notime": True}, "g-cap-estructura"), tx("h_estr", L))
    nq = M["neq"].sort_values()
    f7 = cs.base(L, height=760, fecha_x=False)
    f7.add_trace(go.Bar(y=[M["nom"][c] for c in nq.index], x=nq.round(2), orientation="h", showlegend=False,
                        marker=dict(color=cs.C3, line=dict(width=0)), text=[num(v, 1, L) for v in nq], textposition="outside",
                        cliponaxis=False, textfont=dict(size=10.5, color=cs.INK2), hovertemplate="%{y}: %{x:.1f}<extra></extra>"))
    f7.update_xaxes(range=[0, 12], showgrid=True, gridcolor=cs.GRID, ticksuffix="")
    f7.update_yaxes(ticksuffix="", tickfont=dict(size=11, color=cs.INK2))
    f7.update_layout(hovermode="closest", bargap=0.25)
    g7 = cs.bloque_grafico(tx("g_div", L), cs.fig_html(f7, {"notime": True}, "g-cap-diversificacion"), tx("h_div", L))
    mx = M["sh"].max(axis=1).sort_values(ascending=False)
    d1, d2 = mx.index[0], mx.index[1]
    rn = lambda c: RAMA_N[M["sh"].loc[c].idxmax()][0 if L == "es" else 1].lower()
    r4 = tx("r_estructura", L).format(d1=M["nom"][d1], v1=pct(mx.iloc[0], 0, False), s1=rn(d1), d2=M["nom"][d2], v2=pct(mx.iloc[1], 0, False), s2=rn(d2),
                                      div=M["nom"][nq.index[-1]], nd=num(nq.iloc[-1], 1, L), con=M["nom"][nq.index[0]], nc=num(nq.iloc[0], 1, L))
    s_est = seccion("cap-estructura", tx("s_estructura", L), r4, f'<div class="grid">{g6}{g7}</div>')

    # ------------------------------------------------ ciudades
    tdc_ = pd.DataFrame({"hoy": M["td"], "hace": M["td0"]}).dropna().sort_values("hoy")
    f8 = cs.base(L, height=680, fecha_x=False)
    for ciudad, r_ in tdc_.iterrows():
        f8.add_trace(go.Scatter(x=[r_["hace"], r_["hoy"]], y=[ciudad, ciudad], mode="lines", line=dict(color=cs.RULE, width=3),
                                showlegend=False, hoverinfo="skip"))
    f8.add_trace(go.Scatter(x=tdc_["hace"].round(2), y=tdc_.index, mode="markers", name=tx("lbl_hace", L),
                            marker=dict(size=10, color=cs.GRAY, line=dict(color="#fff", width=1.5)), hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
    f8.add_trace(go.Scatter(x=tdc_["hoy"].round(2), y=tdc_.index, mode="markers", name=tx("lbl_hoy", L),
                            marker=dict(size=12, color=[cs.C3 if h <= a_ else cs.C2 for h, a_ in zip(tdc_["hoy"], tdc_["hace"])],
                                        line=dict(color="#fff", width=1.5)), hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
    f8.update_xaxes(ticksuffix="%", showgrid=True, gridcolor=cs.GRID, rangemode="tozero")
    f8.update_yaxes(ticksuffix="", tickfont=dict(size=11, color=cs.INK2))
    f8.update_layout(hovermode="closest")
    g8 = cs.bloque_grafico(tx("g_ciud", L), cs.fig_html(f8, {"notime": True}, "g-cap-ciudades"), tx("h_ciud", L), ancho=True)
    r5 = tx("r_ciudades", L).format(m=fecha(M["fin_c"], "m", L), lo=pct(tdc_["hoy"].iloc[0], 1, False), c1=tdc_.index[0],
                                    hi=pct(tdc_["hoy"].iloc[-1], 1, False), c2=tdc_.index[-1], n=int((tdc_["hoy"] < tdc_["hace"]).sum()),
                                    top3=", ".join(f"{c_} ({pct(v_, 1, False)})" for c_, v_ in tdc_["hoy"].iloc[::-1].iloc[:3].items()))
    s_ciu = seccion("cap-ciudades", tx("s_ciudades", L), r5, f'<div class="grid">{g8}</div>')

    items = "".join(f'<li><span class="ref">{ref}</span><span class="ref-u">{es if L == "es" else en}</span></li>' for ref, es, en in LITERATURA)
    s_lit = (f'<section id="cap-literatura" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{tx("s_lit", L)}</h2></div>'
             f'<ol class="refs">{items}</ol></section>')
    return antes, s_sec + s_lab + s_reg + s_est + s_lit, s_ciu.replace('id="cap-ciudades"', 'id="emp-ciudades"')
