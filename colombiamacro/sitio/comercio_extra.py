"""Pagina de comercio exterior (v12.3): exportaciones e importaciones de bienes, solo con
cifras oficiales del DANE (con registros de la DIAN). Todo describe datos observados.

Lee las tablas que escribe colombiamacro.fuentes.comercio; si faltan, la pagina no se publica.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from colombiamacro.config import DATA_DIR

TX = {
    "s_cifras": ("El comercio exterior en doce cifras", "Foreign trade in twelve figures"),
    "s_flujos": ("¿Cuánto vende y cuánto compra Colombia?", "How much does Colombia sell and buy?"),
    "s_vende": ("¿Qué vende Colombia?", "What does Colombia sell?"),
    "s_compra": ("¿Qué compra y para qué?", "What does it buy, and for what?"),
    "s_socios": ("¿Con quién comercia?", "Who does it trade with?"),
    # lecturas
    "l_expo": ("Exportaciones, 12 meses", "Exports, 12 months"),
    "l_impo": ("Importaciones, 12 meses", "Imports, 12 months"),
    "l_bal": ("Balanza comercial, 12 meses", "Trade balance, 12 months"),
    "l_min": ("Petróleo y carbón", "Oil and coal"),
    "l_bk": ("Bienes de capital", "Capital goods"),
    "vs_ano": ("{v} frente a los 12 meses anteriores", "{v} versus the previous 12 months"),
    "deficit": ("déficit: se compra más de lo que se vende", "deficit: the country buys more than it sells"),
    "superavit": ("superávit: se vende más de lo que se compra", "surplus: the country sells more than it buys"),
    "l_min_d": ("de lo exportado en 12 meses · hace un año {v}", "of 12-month exports · a year ago {v}"),
    "l_bk_d": ("importaciones {p} {a} frente a {a0}: maquinaria y equipo para invertir",
               "imports {p} {a} versus {a0}: machinery and equipment to invest"),
    "mm": ("US$ {v} mil millones", "US${v} bn"),
    # respuestas
    "r_cifras": ("En los últimos 12 meses (hasta {m}) Colombia exportó {e} e importó {i}: un déficit comercial de {b}. "
                 "Las exportaciones cambiaron {ve} y las importaciones {vi} frente al año anterior. "
                 "Petróleo y carbón son {sm} de lo que vende el país, frente a {sm0} hace un año. "
                 "Las compras de bienes de capital, que anticipan inversión, crecen {bk} en {p} de {a}.",
                 "Over the last 12 months (to {m}) Colombia exported {e} and imported {i}: a trade deficit of {b}. "
                 "Exports changed {ve} and imports {vi} versus the year before. "
                 "Oil and coal are {sm} of what the country sells, versus {sm0} a year earlier. "
                 "Purchases of capital goods, which anticipate investment, are up {bk} in {p} {a}."),
    "r_flujos": ("El último año con superávit comercial fue {u}; el déficit se amplió desde 2014, cuando cayó el precio del petróleo. "
                 "En 12 meses el país vendió {e} y compró {i}. En {a} (enero a {mes}) el déficit acumulado es {b}.",
                 "The last year with a trade surplus was {u}; the deficit widened from 2014, when oil prices fell. "
                 "Over 12 months the country sold {e} and bought {i}. In {a} (January to {mes}) the cumulative deficit is {b}."),
    "r_vende": ("Los productos no tradicionales (industria, agro, flores, químicos) son {nt} de las ventas en 12 meses. "
                "El petróleo aporta {pe} y el carbón {ca}; el café, {cf}. "
                "El peso de petróleo y carbón pasó de {max} en {fmax} a {sm} hoy: el país depende menos de la minería que hace una década.",
                "Non-traditional products (manufacturing, farming, flowers, chemicals) are {nt} of 12-month sales. "
                "Oil contributes {pe} and coal {ca}; coffee, {cf}. "
                "The weight of oil and coal went from {max} in {fmax} to {sm} today: the country depends less on mining than a decade ago."),
    "r_compra": ("En {p} de {a} las importaciones crecen {t} frente a {a0}. "
                 "Lo que más sube son los bienes de consumo duradero ({cd}) y el equipo de transporte ({et}). "
                 "Las materias primas para la industria, la mayor partida, crecen {mi}.",
                 "In {p} {a} imports are up {t} versus {a0}. "
                 "The fastest risers are durable consumer goods ({cd}) and transport equipment ({et}). "
                 "Raw materials for industry, the largest item, are up {mi}."),
    "r_socios": ("{d1} compra {s1} de las exportaciones colombianas en 12 meses; le siguen {d2} ({s2}) y {d3} ({s3}). "
                 "Por el lado de las compras, {o1} vende {p1} de lo que importa Colombia y {o2} {p2}.",
                 "{d1} buys {s1} of Colombia's exports over 12 months, followed by {d2} ({s2}) and {d3} ({s3}). "
                 "On the purchasing side, {o1} supplies {p1} of Colombia's imports and {o2} {p2}."),
    # graficos
    "g_flujos": ("Exportaciones e importaciones, suma de 12 meses", "Exports and imports, 12-month sum"),
    "h_flujos": ("Cada punto suma los 12 meses anteriores, en miles de millones de dólares. Cuando la línea naranja (importaciones) va por encima de la azul (exportaciones), el país tiene déficit comercial.",
                 "Each point adds up the previous 12 months, in billions of dollars. When the orange line (imports) is above the blue one (exports), the country runs a trade deficit."),
    "lbl_expo": ("Exportaciones", "Exports"), "lbl_impo": ("Importaciones", "Imports"),
    "g_balanza": ("Balanza comercial por año", "Trade balance by year"),
    "h_balanza": ("Exportaciones menos importaciones de cada año, en miles de millones de dólares. Verde: superávit; naranja: déficit. El último año va de enero al último mes publicado.",
                  "Exports minus imports each year, in billions of dollars. Green: surplus; orange: deficit. The last year runs from January to the latest month published."),
    "g_productos": ("¿Qué vende? Exportaciones de los últimos 12 meses", "What does it sell? Exports over the last 12 months"),
    "h_productos": ("Largo de la barra: miles de millones de dólares vendidos en 12 meses. El número es la parte del total. Pase el cursor para ver la variación anual.",
                    "Bar length: billions of dollars sold over 12 months. The number is the share of the total. Hover to see the annual change."),
    "g_minero": ("Peso del petróleo y el carbón en las exportaciones", "Weight of oil and coal in exports"),
    "h_minero": ("Porcentaje de las exportaciones de 12 meses que corresponde a petróleo y derivados más carbón. Si baja, el país depende menos de la minería.",
                 "Share of 12-month exports that is oil and derivatives plus coal. When it falls, the country depends less on mining."),
    "g_uso": ("¿Para qué importa? Variación {p} {a} frente a {a0}", "What are imports for? Change {p} {a} vs {a0}"),
    "h_uso": ("Clasificación por uso o destino económico (CUODE). Verde: crece; naranja: cae. El número entre paréntesis es la parte de cada grupo en las importaciones del periodo.",
              "Classification by economic use (CUODE). Green: growing; orange: falling. The number in brackets is each group's share of imports in the period."),
    "g_estructura": ("Composición de las importaciones por uso", "Imports by use, composition"),
    "h_estructura": ("Cada barra es un año (100%). Azul: bienes de consumo; verde: materias primas e insumos; naranja: bienes de capital y construcción. El último año es parcial.",
                     "Each bar is one year (100%). Blue: consumer goods; green: raw materials and inputs; orange: capital goods and construction. The latest year is partial."),
    "lbl_consumo": ("Consumo", "Consumer goods"), "lbl_mp": ("Materias primas", "Raw materials"), "lbl_bk": ("Capital y construcción", "Capital and construction"),
    "g_destinos": ("¿A quién le vende? Parte de las exportaciones, 12 meses", "Who buys? Share of exports, 12 months"),
    "h_destinos": ("Porcentaje de las exportaciones de los últimos 12 meses que va a cada destino. «Resto» agrupa los demás países.",
                   "Share of the last 12 months' exports going to each destination. 'Rest' groups the other countries."),
    "g_origenes": ("¿A quién le compra? Parte de las importaciones, 12 meses", "Who sells to Colombia? Share of imports, 12 months"),
    "h_origenes": ("Porcentaje de las importaciones de los últimos 12 meses que viene de cada país (los 10 principales).",
                   "Share of the last 12 months' imports coming from each country (top 10)."),
    "parcial": ("ene–{m}", "Jan–{m}"),
}

PRODUCTOS = [("no_tradicionales", ("No tradicionales", "Non-traditional")), ("petroleo", ("Petróleo y derivados", "Oil and derivatives")),
             ("carbon", ("Carbón", "Coal")), ("cafe", ("Café", "Coffee")), ("ferroniquel", ("Ferroníquel", "Ferronickel"))]
DESTINOS = {"estados_unidos": ("Estados Unidos", "United States"), "union_europea": ("Unión Europea", "European Union"),
            "panama": ("Panamá", "Panama"), "china": ("China", "China"), "india": ("India", "India"), "brasil": ("Brasil", "Brazil"),
            "mexico": ("México", "Mexico"), "ecuador": ("Ecuador", "Ecuador"), "peru": ("Perú", "Peru"), "canada": ("Canadá", "Canada"),
            "venezuela": ("Venezuela", "Venezuela"), "japon": ("Japón", "Japan"), "argentina": ("Argentina", "Argentina"),
            "bolivia": ("Bolivia", "Bolivia"), "paraguay": ("Paraguay", "Paraguay"), "uruguay": ("Uruguay", "Uruguay"), "resto": ("Resto", "Rest")}
PAISES_EN = {"Alemania": "Germany", "Bélgica": "Belgium", "Brasil": "Brazil", "Canadá": "Canada", "Corea": "South Korea",
             "España": "Spain", "Estados Unidos": "United States", "Francia": "France", "Italia": "Italy", "Japón": "Japan",
             "Malasia": "Malaysia", "México": "Mexico", "Países Bajos": "Netherlands", "Perú": "Peru", "Reino Unido": "United Kingdom",
             "Rusia": "Russia", "Suecia": "Sweden", "Suiza": "Switzerland", "Tailandia": "Thailand", "Taiwán": "Taiwan",
             "Trinidad y Tobago": "Trinidad and Tobago"}
# subgrupos CUODE (Cuadro A13) en el orden del grafico; nombres cortos
CUODE_SUB = [("Bienes de consumo no duradero", ("Consumo no duradero", "Non-durable consumer")),
             ("Bienes de consumo duradero", ("Consumo duradero", "Durable consumer")),
             ("Combustibles, lubricantes y conexos", ("Combustibles", "Fuels")),
             ("Materias primas y productos intermedios para la agricultura", ("Insumos para el agro", "Farm inputs")),
             ("Materias primas y productos intermedios para la industria", ("Insumos para la industria", "Industrial inputs")),
             ("Materiales de construcción", ("Materiales de construcción", "Construction materials")),
             ("Bienes de capital para la agricultura", ("Capital para el agro", "Farm capital goods")),
             ("Bienes de capital para la industria", ("Capital para la industria", "Industrial capital goods")),
             ("Equipo de transporte", ("Equipo de transporte", "Transport equipment"))]

ARCHIVOS = ["exportaciones_mensuales.csv", "exportaciones_destinos.csv", "importaciones_mensuales.csv",
            "importaciones_cuode_reciente.csv", "importaciones_cuode_anual.csv", "importaciones_origen.csv"]


def tx(k, L):
    return TX[k][0 if L == "es" else 1]


def cargar():
    """Tablas de comercio, o None si falta alguna (la pagina no se publica)."""
    if not all((DATA_DIR / f).exists() for f in ARCHIVOS):
        return None
    lee = lambda f, **kw: pd.read_csv(DATA_DIR / f, **kw)
    return {"expo": lee("exportaciones_mensuales.csv", parse_dates=["fecha"]),
            "destinos": lee("exportaciones_destinos.csv", parse_dates=["fecha"]),
            "impo": lee("importaciones_mensuales.csv", parse_dates=["fecha"]),
            "cuode": lee("importaciones_cuode_reciente.csv"),
            "cuode_anual": lee("importaciones_cuode_anual.csv"),
            "origen": lee("importaciones_origen.csv", parse_dates=["fecha"])}


def _norm(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFKD", str(s).lower()) if not unicodedata.combining(c)).strip()


def resumen(c):
    """Cifras clave (en millones de USD y %) que usan la pagina y la portada."""
    e = c["expo"].set_index("fecha").sort_index()
    i = c["impo"].set_index("fecha").sort_index()
    fin = min(e.index.max(), i.index.max())
    e, i = e.loc[:fin], i.loc[:fin]
    e12, i12 = e["total"].rolling(12).sum() / 1000, i["total"].rolling(12).sum() / 1000   # millones de USD
    min12 = (e["petroleo"] + e["carbon"]).rolling(12).sum() / 1000
    hace = fin - pd.DateOffset(years=1)
    cu = c["cuode"]
    bk = cu[cu["grupo"].map(_norm).str.startswith("bienes de capital")].iloc[0]
    return {"fin": fin, "expo12": e12.loc[fin], "impo12": i12.loc[fin], "bal12": e12.loc[fin] - i12.loc[fin],
            "expo_var": 100 * (e12.loc[fin] / e12.loc[hace] - 1), "impo_var": 100 * (i12.loc[fin] / i12.loc[hace] - 1),
            "min_sh": 100 * min12.loc[fin] / e12.loc[fin], "min_sh0": 100 * min12.loc[hace] / e12.loc[hace],
            "bk_var": float(bk["corrido_var"]), "periodo": str(cu["periodo_corrido"].iloc[0]),
            "anio": str(cu["anio_actual"].iloc[0]), "anio0": str(cu["anio_anterior"].iloc[0]),
            "e": e, "i": i, "e12": e12, "i12": i12, "min12": min12}


def construir_comercio(c, L):
    """HTML de la pagina de comercio exterior. Devuelve (html, primera_respuesta)."""
    from colombiamacro.sitio import construir as cs
    num, fecha, esc = cs.num, cs.fecha, cs.esc
    cs.LANG_ACTUAL[0] = L        # el modulo puede cargarse dos veces (python -m): fija el idioma de las fichas
    R = resumen(c)
    fin = R["fin"]
    mes = fecha(fin, "m", L)
    bn = lambda v, signo=False: tx("mm", L).format(v=num(v / 1000, 1, L, signo))
    bc = lambda v, signo=False: (f"US$ {num(v / 1000, 1, L, signo)} mil M" if L == "es" else f"US${num(v / 1000, 1, L, signo)} bn")
    pct = lambda v, dec=1, signo=False: num(v, dec, L, signo, "%")
    periodo = R["periodo"].lower().replace(" - ", "–") if L == "es" else tx("parcial", L).format(m=cs.MESES["en"][fin.month - 1])
    secs = []

    def sec(sid, titulo, resp, cuerpo):
        secs.append(f'<section id="{sid}" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{titulo}</h2></div>'
                    f'{cs.respuesta_html(resp, L)}{cuerpo}</section>')

    # ------------------------------------------------ 0. cinco cifras
    def lec(k, v, dsc, tono, href):
        return (f'<a class="lec {tono}" href="{href}"><span class="lec-k">{k}</span><b class="lec-v">{v}</b>'
                f'<span class="lec-d">{dsc}</span></a>')

    lecturas = "".join([
        lec(f'{tx("l_expo", L)} · {mes}', bc(R["expo12"]), tx("vs_ano", L).format(v=pct(R["expo_var"], 1, True)),
            "ok" if R["expo_var"] >= 0 else "warn", "#comercio-flujos"),
        lec(f'{tx("l_impo", L)} · {mes}', bc(R["impo12"]), tx("vs_ano", L).format(v=pct(R["impo_var"], 1, True)), "", "#comercio-flujos"),
        lec(tx("l_bal", L), bc(R["bal12"], True), tx("deficit" if R["bal12"] < 0 else "superavit", L),
            "warn" if R["bal12"] < 0 else "ok", "#comercio-flujos"),
        lec(tx("l_min", L), pct(R["min_sh"], 0), tx("l_min_d", L).format(v=pct(R["min_sh0"], 0)), "", "#comercio-vende"),
        lec(f'{tx("l_bk", L)} · {periodo} {R["anio"]}', pct(R["bk_var"], 1, True),
            tx("l_bk_d", L).format(p=periodo, a=R["anio"], a0=R["anio0"]), "ok" if R["bk_var"] >= 0 else "warn", "#comercio-compra"),
    ])
    r0 = tx("r_cifras", L).format(m=mes, e=bn(R["expo12"]), i=bn(R["impo12"]), b=bn(abs(R["bal12"])),
                                  ve=pct(R["expo_var"], 1, True), vi=pct(R["impo_var"], 1, True),
                                  sm=pct(R["min_sh"], 0), sm0=pct(R["min_sh0"], 0), bk=pct(R["bk_var"], 1),
                                  p=periodo, a=R["anio"])
    from colombiamacro.sitio.comercio_mas import construir_mas
    extra_tiles, extra_secs = construir_mas(c, R, L)
    sec("comercio-cifras", tx("s_cifras", L), r0, f'<div class="lecturas ocho">{lecturas}{extra_tiles}</div>')

    # ------------------------------------------------ 1. flujos y balanza
    e12, i12 = R["e12"].dropna(), R["i12"].dropna()
    f1 = cs.base(L, height=330, suffix="")
    xe = e12.index + pd.offsets.MonthEnd(0)
    cs.linea(f1, xe, e12 / 1000, tx("lbl_expo", L), cs.C1, width=2.4, suf=" mil M US$" if L == "es" else " bn US$", lang=L)
    cs.linea(f1, i12.index + pd.offsets.MonthEnd(0), i12 / 1000, tx("lbl_impo", L), cs.C2, width=2.4,
             suf=" mil M US$" if L == "es" else " bn US$", lang=L)
    f1.update_yaxes(rangemode="tozero")
    g1 = cs.bloque_grafico(tx("g_flujos", L), cs.fig_html(f1, {}, "g-comercio-flujos"), tx("h_flujos", L))

    e, i = R["e"], R["i"]
    anual = pd.DataFrame({"e": e["total"].groupby(e.index.year).sum(), "i": i["total"].groupby(i.index.year).sum(),
                          "n": i["total"].groupby(i.index.year).count()}).dropna()
    anual = anual[anual["n"] > 0]
    bal = (anual["e"] - anual["i"]) / 1e6
    etiquetas = [str(a) + (f" ({tx('parcial', L).format(m=cs.MESES[L][fin.month - 1])})" if a == fin.year and fin.month < 12 else "") for a in bal.index]
    f2 = cs.base(L, height=330, suffix="", fecha_x=False)
    f2.add_trace(go.Bar(x=etiquetas, y=bal.round(2), showlegend=False,
                        marker=dict(color=[cs.C3 if v >= 0 else cs.C2 for v in bal], line=dict(width=0)),
                        hovertemplate="%{x}: %{y:.1f}" + (" mil M US$" if L == "es" else " bn US$") + "<extra></extra>"))
    f2.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    f2.update_layout(bargap=0.25, hovermode="closest")
    f2.update_xaxes(tickangle=-45)
    g2 = cs.bloque_grafico(tx("g_balanza", L), cs.fig_html(f2, {"notime": True}, "g-balanza"), tx("h_balanza", L))
    ytd = bal.iloc[-1] * 1000
    u_sup = [a for a, v in bal.items() if v > 0]
    r1 = tx("r_flujos", L).format(u=u_sup[-1] if u_sup else "—", e=bn(R["expo12"]), i=bn(R["impo12"]), a=fin.year, mes=cs.MESES[L][fin.month - 1] if L == "en" else
                                  ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"][fin.month - 1],
                                  b=bn(abs(ytd)))
    sec("comercio-flujos", tx("s_flujos", L), r1, f'<div class="grid">{g1}{g2}</div>')

    # ------------------------------------------------ 2. que vende
    u12 = e.rolling(12).sum().loc[fin] / 1e6
    a12 = e.rolling(12).sum().loc[fin - pd.DateOffset(years=1)] / 1e6
    filas = [(n[0 if L == "es" else 1], u12[k], 100 * u12[k] / u12["total"], 100 * (u12[k] / a12[k] - 1)) for k, n in PRODUCTOS]
    filas.sort(key=lambda r: r[1])
    colores = {"Petróleo y derivados": cs.C1, "Oil and derivatives": cs.C1, "Carbón": "#8a6d3b", "Coal": "#8a6d3b"}
    f3 = cs.base(L, height=280, suffix="", fecha_x=False)
    f3.add_trace(go.Bar(y=[r[0] for r in filas], x=[round(r[1], 2) for r in filas], orientation="h", showlegend=False,
                        marker=dict(color=[colores.get(r[0], cs.C3) for r in filas], line=dict(width=0)),
                        text=[pct(r[2], 0) for r in filas], textposition="outside", cliponaxis=False,
                        customdata=[[num(r[1], 1, L), pct(r[3], 1, True)] for r in filas],
                        hovertemplate="%{y}: %{customdata[0]}" + (" mil M US$" if L == "es" else " bn US$") +
                                      "<br>" + ("Variación anual" if L == "es" else "Annual change") + ": %{customdata[1]}<extra></extra>"))
    f3.update_xaxes(showgrid=True, gridcolor=cs.GRID, range=[0, max(r[1] for r in filas) * 1.18])
    f3.update_yaxes(ticksuffix="", tickfont=dict(size=12.5, color=cs.INK2))
    f3.update_layout(hovermode="closest", bargap=0.35)
    g3 = cs.bloque_grafico(tx("g_productos", L), cs.fig_html(f3, {"notime": True}, "g-expo-productos"), tx("h_productos", L))

    sh = (100 * R["min12"] / R["e12"]).dropna()
    sh = sh[sh.index >= "1995-01-01"]
    f4 = cs.base(L, height=280)
    cs.linea(f4, sh.index + pd.offsets.MonthEnd(0), sh, tx("l_min", L), cs.C1, width=2.4, fmt=".0f", lang=L)
    f4.update_layout(showlegend=False)
    f4.update_yaxes(range=[0, 80])
    g4 = cs.bloque_grafico(tx("g_minero", L), cs.fig_html(f4, {}, "g-expo-minero"), tx("h_minero", L))
    smax = sh.loc["2005":]
    d_ = {r[0]: r[2] for r in filas}
    nm = lambda k: dict(PRODUCTOS)[k][0 if L == "es" else 1]
    r2 = tx("r_vende", L).format(nt=pct(d_[nm("no_tradicionales")], 0), pe=pct(d_[nm("petroleo")], 0), ca=pct(d_[nm("carbon")], 0),
                                 cf=pct(d_[nm("cafe")], 0), max=pct(smax.max(), 0), fmax=fecha(smax.idxmax(), "m", L), sm=pct(sh.iloc[-1], 0))
    sec("comercio-vende", tx("s_vende", L), r2, f'<div class="grid">{g3}{g4}</div>')

    # ------------------------------------------------ 3. que compra (CUODE)
    cu = c["cuode"].copy()
    cu["k"] = cu["grupo"].map(_norm)
    tot = cu.iloc[0]
    sub = []
    for g_, n_ in CUODE_SUB:
        r_ = cu[cu["k"].str.startswith(_norm(g_))]
        if not r_.empty:
            r_ = r_.iloc[0]
            sub.append((n_[0 if L == "es" else 1], float(r_["corrido_var"]), 100 * r_["corrido_actual"] / tot["corrido_actual"]))
    sub.sort(key=lambda r: r[1])
    f5 = cs.base(L, height=360, fecha_x=False)
    f5.add_trace(go.Bar(y=[f"{r[0]} ({num(r[2], 0, L)}%)" for r in sub], x=[round(r[1], 2) for r in sub], orientation="h", showlegend=False,
                        marker=dict(color=[cs.C3 if r[1] >= 0 else cs.C2 for r in sub], line=dict(width=0)),
                        text=[pct(r[1], 1, True) for r in sub], textposition="outside", cliponaxis=False,
                        hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
    lim = max(abs(r[1]) for r in sub) * 1.5
    f5.add_vline(x=0, line=dict(color=cs.INK2, width=1))
    f5.update_xaxes(range=[min(-12, min(r[1] for r in sub) * 4), lim], ticksuffix="%", showgrid=True, gridcolor=cs.GRID)
    f5.update_yaxes(ticksuffix="", tickfont=dict(size=12, color=cs.INK2))
    f5.update_layout(hovermode="closest", bargap=0.3)
    g5 = cs.bloque_grafico(tx("g_uso", L).format(p=periodo, a=R["anio"], a0=R["anio0"]),
                           cs.fig_html(f5, {"notime": True}, "g-impo-uso"), tx("h_uso", L))

    ca = c["cuode_anual"].copy()
    ca["k"] = ca["grupo"].map(_norm)
    piv = ca.pivot_table(index="anio", columns="k", values="valor", aggfunc="sum")
    grandes = [("bienes de consumo", "lbl_consumo", cs.C1), ("materias primas y productos intermedios", "lbl_mp", cs.C3),
               ("bienes de capital y materiales de construccion", "lbl_bk", cs.C2)]
    piv = piv[[g_ for g_, _, _ in grandes]].loc[2005:]
    shp = 100 * piv.div(piv.sum(axis=1), axis=0)
    ult_a = int(shp.index.max())
    xa = [str(a) + (f"*" if a == ult_a and fin.month < 12 else "") for a in shp.index]
    f6 = cs.base(L, height=330, fecha_x=False)
    for g_, lbl, col in grandes:
        f6.add_trace(go.Bar(x=xa, y=shp[g_].round(1), name=tx(lbl, L), marker=dict(color=col, line=dict(width=0)),
                            hovertemplate=tx(lbl, L) + ": %{y:.0f}%<extra>%{x}</extra>"))
    f6.update_layout(barmode="stack", bargap=0.2, hovermode="closest")
    f6.update_yaxes(range=[0, 100])
    f6.update_xaxes(tickangle=-45)
    g6 = cs.bloque_grafico(tx("g_estructura", L), cs.fig_html(f6, {"notime": True}, "g-impo-estructura"), tx("h_estructura", L))
    vs = {n_: v for n_, v, _ in sub}
    nn = lambda es: dict(CUODE_SUB)[es][0 if L == "es" else 1]
    r3 = tx("r_compra", L).format(p=periodo, a=R["anio"], a0=R["anio0"], t=pct(float(tot["corrido_var"]), 1, True),
                                  cd=pct(vs.get(nn("Bienes de consumo duradero"), np.nan), 1, True),
                                  et=pct(vs.get(nn("Equipo de transporte"), np.nan), 1, True),
                                  mi=pct(vs.get(nn("Materias primas y productos intermedios para la industria"), np.nan), 1, True))
    sec("comercio-compra", tx("s_compra", L), r3, f'<div class="grid">{g5}{g6}</div>')

    # ------------------------------------------------ 4. socios
    de = c["destinos"].set_index("fecha").sort_index().loc[:fin]
    d12 = de.rolling(12).sum().iloc[-1]
    part = (100 * d12.drop("total") / d12["total"]).sort_values(ascending=False)
    top = [k for k in part.index if k != "resto"][:9]
    filas_d = [(DESTINOS[k][0 if L == "es" else 1], part[k]) for k in top] + [(DESTINOS["resto"][0 if L == "es" else 1], part["resto"] + part.drop(top + ["resto"]).sum())]
    filas_d = filas_d[::-1]
    f7 = cs.base(L, height=360, fecha_x=False)
    f7.add_trace(go.Bar(y=[r[0] for r in filas_d], x=[round(r[1], 2) for r in filas_d], orientation="h", showlegend=False,
                        marker=dict(color=[cs.GRAY if i_ == 0 else cs.C1 for i_ in range(len(filas_d))], line=dict(width=0)),
                        text=[pct(r[1], 1) for r in filas_d], textposition="outside", cliponaxis=False,
                        hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
    f7.update_xaxes(range=[0, max(r[1] for r in filas_d) * 1.2], ticksuffix="%", showgrid=True, gridcolor=cs.GRID)
    f7.update_yaxes(ticksuffix="", tickfont=dict(size=12, color=cs.INK2))
    f7.update_layout(hovermode="closest", bargap=0.3)
    g7 = cs.bloque_grafico(tx("g_destinos", L), cs.fig_html(f7, {"notime": True}, "g-destinos"), tx("h_destinos", L))

    og = c["origen"]
    og = og[(og["fecha"] > fin - pd.DateOffset(years=1)) & (og["fecha"] <= fin)]
    tot_i = i.loc[i.index > fin - pd.DateOffset(years=1), "publicadas"].sum()
    po = (100 * og.groupby("pais")["valor"].sum() / tot_i).sort_values(ascending=False).head(10)
    nom_o = lambda p: p if L == "es" else PAISES_EN.get(p, p)
    filas_o = [(nom_o(p), v) for p, v in po.items()][::-1]
    f8 = cs.base(L, height=360, fecha_x=False)
    f8.add_trace(go.Bar(y=[r[0] for r in filas_o], x=[round(r[1], 2) for r in filas_o], orientation="h", showlegend=False,
                        marker=dict(color=cs.C2, line=dict(width=0)), text=[pct(r[1], 1) for r in filas_o],
                        textposition="outside", cliponaxis=False, hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
    f8.update_xaxes(range=[0, max(r[1] for r in filas_o) * 1.2], ticksuffix="%", showgrid=True, gridcolor=cs.GRID)
    f8.update_yaxes(ticksuffix="", tickfont=dict(size=12, color=cs.INK2))
    f8.update_layout(hovermode="closest", bargap=0.3)
    g8 = cs.bloque_grafico(tx("g_origenes", L), cs.fig_html(f8, {"notime": True}, "g-origenes"), tx("h_origenes", L))
    dd = filas_d[::-1]
    oo = filas_o[::-1]
    r4 = tx("r_socios", L).format(d1=dd[0][0], s1=pct(dd[0][1], 0), d2=dd[1][0], s2=pct(dd[1][1], 0), d3=dd[2][0], s3=pct(dd[2][1], 0),
                                  o1=oo[0][0], p1=pct(oo[0][1], 0), o2=oo[1][0], p2=pct(oo[1][1], 0))
    sec("comercio-socios", tx("s_socios", L), r4, f'<div class="grid">{g7}{g8}</div>')

    secs.append(extra_secs)
    return "".join(secs), r0, R
