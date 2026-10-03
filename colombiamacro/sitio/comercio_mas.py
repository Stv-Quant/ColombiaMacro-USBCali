"""Comercio exterior ampliado (v12.17): siete medidas adicionales y cinco secciones nuevas para la pagina de
comercio: precio frente a cantidad, evolucion de la canasta exportadora, balanza con cada socio, ascenso de
China, apertura y concentracion, ventana explicativa y literatura.

Datos: DANE con registros de la DIAN (exportaciones FOB, importaciones CIF, destinos y origenes), Banco de la
Republica (indices de precios de exportacion e importacion en dolares y terminos de intercambio) y PIB nominal
del DANE para la apertura.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

TX = {
    "l_cob": ("Cobertura", "Coverage"), "l_cob_d": ("exportaciones / importaciones · hace un año {v}", "exports / imports · a year ago {v}"),
    "l_nt": ("No tradicionales", "Non-traditional"), "l_nt_d": ("US${v} mil M en 12 meses · {c} en un año", "US${v} bn over 12 months · {c} over a year"),
    "l_cafe": ("Café", "Coffee"), "l_cafe_d": ("US${v} mil M en 12 meses · {c} en un año", "US${v} bn over 12 months · {c} over a year"),
    "l_px": ("Precios de exportación", "Export prices"), "l_px_d": ("en dólares, 12 meses · volumen implícito {v}", "in dollars, 12 months · implied volume {v}"),
    "l_ti": ("Términos de intercambio", "Terms of trade"), "l_ti_d": ("precios de lo que vende / de lo que compra · 12 meses", "prices of what it sells / of what it buys · 12 months"),
    "l_ap": ("Apertura comercial", "Trade openness"), "l_ap_d": ("(exportaciones + importaciones de bienes) / PIB · hace 10 años {v}", "(goods exports + imports) / GDP · 10 years ago {v}"),
    "l_ch": ("Balanza con China", "Balance with China"), "l_ch_d": ("12 meses · China vende {p} de lo que importa Colombia", "12 months · China supplies {p} of Colombia's imports"),
    "s_precios": ("¿Se vende más o se vende más caro?", "Selling more, or selling at higher prices?"),
    "s_evol": ("Cómo ha cambiado lo que vende Colombia", "How Colombia's exports have changed"),
    "s_bil": ("La balanza con cada socio", "The balance with each partner"),
    "s_ap": ("Apertura y concentración", "Openness and concentration"),
    "s_lit": ("Bases metodológicas y literatura", "Methodological basis and literature"),
    "r_precios": ("En 12 meses el valor de las exportaciones cambió {ve}: los precios en dólares {pe} y el volumen implícito {qe}. "
                  "Las importaciones cambiaron {vi}, con precios {pi} y volumen {qi}. Los términos de intercambio cambiaron {ti}.",
                  "Over 12 months the value of exports changed {ve}: dollar prices {pe} and implied volume {qe}. "
                  "Imports changed {vi}, with prices {pi} and volume {qi}. The terms of trade changed {ti}."),
    "r_evol": ("En 12 meses las exportaciones suman US${t} mil millones. Los productos no tradicionales pasaron de {nt0} del total en {a0} a {nt1} hoy; "
               "petróleo y carbón, de {mi0} a {mi1}.",
               "Over 12 months exports total US${t} bn. Non-traditional products went from {nt0} of the total in {a0} to {nt1} today; "
               "oil and coal, from {mi0} to {mi1}."),
    "r_bil": ("Con {s1} Colombia tiene un {t1} de US${v1} mil millones en 12 meses y con {s2} un {t2} de US${v2} mil millones. "
              "La parte de China en las importaciones pasó de {c0} en {a0} a {c1}; la de Estados Unidos, de {u0} a {u1}.",
              "With {s1} Colombia runs a {t1} of US${v1} bn over 12 months and with {s2} a {t2} of US${v2} bn. "
              "China's share of imports went from {c0} in {a0} to {c1}; that of the United States, from {u0} to {u1}."),
    "deficit": ("déficit", "deficit"), "superavit": ("superávit", "surplus"),
    "r_ap": ("El comercio de bienes equivale a {ap} del PIB. Las exportaciones van a un número de destinos equivalente a {ne} socios de igual tamaño "
             "(hace 10 años, {ne0}); y a un número de productos equivalente a {np} grupos (de los cinco que publica el DANE).",
             "Goods trade is equivalent to {ap} of GDP. Exports go to a number of destinations equivalent to {ne} equal-sized partners "
             "(10 years ago, {ne0}); and to a number of products equivalent to {np} groups (of the five DANE publishes)."),
    "g_pq_x": ("Exportaciones: valor, precio y volumen (12 meses)", "Exports: value, price and volume (12 months)"),
    "g_pq_m": ("Importaciones: valor, precio y volumen (12 meses)", "Imports: value, price and volume (12 months)"),
    "h_pq": ("Variación anual. Valor = suma de 12 meses del DANE; precio = índice de precios en dólares del Banco de la República (promedio de 12 meses); volumen implícito = (1 + valor) / (1 + precio) − 1.",
             "Annual change. Value = DANE 12-month sum; price = Banco de la República dollar price index (12-month average); implied volume = (1 + value) / (1 + price) − 1."),
    "lbl_val": ("Valor", "Value"), "lbl_pre": ("Precio", "Price"), "lbl_vol": ("Volumen implícito", "Implied volume"),
    "g_evol": ("Exportaciones por grupo de productos (12 meses)", "Exports by product group (12 months)"),
    "h_evol": ("Miles de millones de dólares FOB, suma de 12 meses, áreas apiladas: la altura total es lo exportado.",
               "Billions of FOB dollars, 12-month sum, stacked areas: the total height is what was exported."),
    "g_bil": ("Exportaciones menos importaciones con cada socio (12 meses)", "Exports minus imports with each partner (12 months)"),
    "h_bil": ("Miles de millones de dólares. Exportaciones FOB menos importaciones CIF (las CIF incluyen fletes y seguros). Verde: superávit; naranja: déficit.",
              "Billions of dollars. FOB exports minus CIF imports (CIF includes freight and insurance). Green: surplus; orange: deficit."),
    "g_ch": ("¿De dónde vienen las importaciones? China, Estados Unidos y el resto", "Where do imports come from? China, the United States and the rest"),
    "h_ch": ("Participación en las importaciones de 12 meses.", "Share of 12-month imports."),
    "g_ap": ("Apertura comercial de bienes (% del PIB)", "Goods trade openness (% of GDP)"),
    "h_ap": ("Exportaciones e importaciones de bienes de cuatro trimestres sobre el PIB en dólares de los mismos trimestres.",
             "Goods exports and imports over four quarters divided by dollar GDP for the same quarters."),
    "lbl_apx": ("Exportaciones", "Exports"), "lbl_apm": ("Importaciones", "Imports"),
    "g_hhi": ("Diversificación de destinos y productos", "Diversification of destinations and products"),
    "h_hhi": ("Número equivalente = 1 / índice de Herfindahl de las participaciones en 12 meses. Más alto = exportaciones más repartidas.",
              "Equivalent number = 1 / Herfindahl index of 12-month shares. Higher = more evenly spread exports."),
    "lbl_nd": ("Destinos (17 grupos)", "Destinations (17 groups)"), "lbl_npr": ("Productos (5 grupos)", "Products (5 groups)"),
}
PRODUCTOS = [("petroleo", ("Petróleo y derivados", "Oil and derivatives")), ("carbon", ("Carbón", "Coal")), ("cafe", ("Café", "Coffee")),
             ("ferroniquel", ("Ferroníquel", "Ferronickel")), ("no_tradicionales", ("No tradicionales", "Non-traditional"))]
SOCIOS = {"Estados Unidos": ("estados_unidos", ("Estados Unidos", "United States")), "China": ("china", ("China", "China")),
          "México": ("mexico", ("México", "Mexico")), "Brasil": ("brasil", ("Brasil", "Brazil")), "Perú": ("peru", ("Perú", "Peru")),
          "Ecuador": ("ecuador", ("Ecuador", "Ecuador")), "Canadá": ("canada", ("Canadá", "Canada")), "Japón": ("japon", ("Japón", "Japan")),
          "India": ("india", ("India", "India")), "Venezuela": ("venezuela", ("Venezuela", "Venezuela")), "Argentina": ("argentina", ("Argentina", "Argentina"))}
LITERATURA = [
    ("Prebisch, R. (1950). <i>The Economic Development of Latin America and its Principal Problems</i>. Naciones Unidas, CEPAL.",
     "Términos de intercambio y dependencia de las materias primas.", "Terms of trade and commodity dependence."),
    ("Melitz, M. J. (2003). The Impact of Trade on Intra-Industry Reallocations and Aggregate Industry Productivity. <i>Econometrica</i>, 71(6), 1695–1725.",
     "Por qué solo las empresas más productivas exportan.", "Why only the most productive firms export."),
    ("Hausmann, R., Hwang, J. y Rodrik, D. (2007). What You Export Matters. <i>Journal of Economic Growth</i>, 12(1), 1–25.",
     "La composición de las exportaciones y el crecimiento.", "Export composition and growth."),
    ("Hidalgo, C. A., Klinger, B., Barabási, A.-L. y Hausmann, R. (2007). The Product Space Conditions the Development of Nations. <i>Science</i>, 317(5837), 482–487.",
     "Diversificación productiva y espacio de productos.", "Productive diversification and the product space."),
    ("DANE. Estadísticas de comercio internacional: exportaciones (FOB) e importaciones (CIF) con base en registros administrativos de la DIAN.",
     "Fuente y definiciones de las cifras de esta página.", "Source and definitions of the figures on this page."),
]


def tx(k, L):
    return TX[k][0 if L == "es" else 1]


def anual(s: pd.Series) -> pd.Series:
    return (s / s.shift(12) - 1) * 100


def num_equivalente(part: pd.DataFrame) -> pd.Series:
    """1 / Herfindahl de participaciones (filas = fechas, columnas = categorias)."""
    sh = part.div(part.sum(axis=1), axis=0)
    return 1 / (sh ** 2).sum(axis=1)


def construir_mas(c, R, L):
    """Devuelve (lecturas_extra_html, secciones_html)."""
    from colombiamacro.fuentes import externo_fiscal as xf
    from colombiamacro.sitio import construir as cs
    num, fecha = cs.num, cs.fecha
    k = 0 if L == "es" else 1
    pct = lambda v, dec=1, sg=False: num(float(v), dec, L, sg, "%")
    bn = lambda v: num(float(v), 1, L)
    fin = R["fin"]
    e, i = R["e"], R["i"]
    e12, i12 = e["total"].rolling(12).sum() / 1e6, i["total"].rolling(12).sum() / 1e6          # miles de millones de USD
    hace = fin - pd.DateOffset(years=1)
    X = xf.cargar() or {}

    def lec(kk, v, dsc, tono, href):
        return (f'<a class="lec {tono}" href="{href}"><span class="lec-k">{kk}</span><b class="lec-v">{v}</b>'
                f'<span class="lec-d">{dsc}</span></a>')

    def sec(sid, titulo, resp, cuerpo):
        return (f'<section id="{sid}" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{titulo}</h2></div>'
                f'{cs.respuesta_html(resp, L)}{cuerpo}</section>')

    # ------------------------------------------------ precio y volumen
    px, pm = X.get("precio_exportaciones"), X.get("precio_importaciones")
    vx, vm = anual(e["total"].rolling(12).sum()), anual(i["total"].rolling(12).sum())
    pq = pd.DataFrame({"vx": vx, "px": anual(px.rolling(12).mean()) if px is not None else np.nan,
                       "vm": vm, "pm": anual(pm.rolling(12).mean()) if pm is not None else np.nan}).loc["2005":]
    pq["qx"] = ((1 + pq["vx"] / 100) / (1 + pq["px"] / 100) - 1) * 100
    pq["qm"] = ((1 + pq["vm"] / 100) / (1 + pq["pm"] / 100) - 1) * 100
    u = pq.dropna().iloc[-1]
    ti = d_ti = None
    if px is not None and pm is not None:
        ti = (px / pm).dropna()
        d_ti = float((ti.iloc[-1] / ti.iloc[-13] - 1) * 100)

    def fig_pq(cols, gid, titulo):
        f = cs.base(L, height=360)
        z = pq[list(cols)].dropna()
        xz = z.index + pd.offsets.MonthEnd(0)
        for col, lbl, color, w_, dash in zip(cols, ("lbl_val", "lbl_pre", "lbl_vol"), (cs.C1, cs.C4, cs.C3), (2.6, 1.8, 1.8), (None, "dot", None)):
            cs.linea(f, xz, z[col], tx(lbl, L), color, width=w_, dash=dash, lang=L)
        f.add_hline(y=0, line=dict(color=cs.INK2, width=1))
        cs.ejes(f, y="Variación anual" if L == "es" else "Annual change")
        return cs.bloque_grafico(tx(titulo, L), cs.fig_html(f, {}, gid), tx("h_pq", L))

    g1 = fig_pq(("vx", "px", "qx"), "g-com-pq-expo", "g_pq_x").replace("</figcaption>", " " + (
        f'<button type="button" class="ex-q" data-dialog="exp-comercio" aria-haspopup="dialog" title="{"¿Cómo se miden las exportaciones e importaciones?" if L == "es" else "How are exports and imports measured?"}">?</button>') + "</figcaption>", 1)
    g2 = fig_pq(("vm", "pm", "qm"), "g-com-pq-impo", "g_pq_m")
    r1 = tx("r_precios", L).format(ve=pct(u["vx"], 1, True), pe=pct(u["px"], 1, True), qe=pct(u["qx"], 1, True), vi=pct(u["vm"], 1, True),
                                   pi=pct(u["pm"], 1, True), qi=pct(u["qm"], 1, True), ti=pct(d_ti, 1, True) if d_ti is not None else "—")
    s_pq = sec("comercio-precios", tx("s_precios", L), r1, f'<div class="grid">{g1}{g2}</div>') + ventana_comercio(L)

    # ------------------------------------------------ evolucion de la canasta
    p12 = pd.DataFrame({k_: e[k_].rolling(12).sum() / 1e6 for k_, _ in PRODUCTOS}).loc["1995":].dropna()
    xp = p12.index + pd.offsets.MonthEnd(0)
    f3 = cs.base(L, height=380, suffix="")
    for (k_, nm), col in zip(PRODUCTOS, (cs.C4, cs.C7, cs.C2, cs.C1, cs.C3)):
        f3.add_trace(go.Scatter(x=list(xp), y=p12[k_].round(2).tolist(), mode="lines", stackgroup="x", name=nm[k],
                                line=dict(color=col, width=0.5), fillcolor=col, hovertemplate=nm[k] + ": US$%{y:.1f}" + (" mil M" if L == "es" else " bn") + "<extra></extra>"))
    cs.ejes(f3, y="Miles de millones de dólares (12 meses)" if L == "es" else "US$ billions (12 months)")
    g3 = cs.bloque_grafico(tx("g_evol", L), cs.fig_html(f3, {"noy": True}, "g-com-canasta"), tx("h_evol", L), ancho=True)
    sh_nt = p12["no_tradicionales"] / p12.sum(axis=1) * 100
    sh_mi = (p12["petroleo"] + p12["carbon"]) / p12.sum(axis=1) * 100
    a0 = sh_mi.loc["2005":].idxmax()
    r2 = tx("r_evol", L).format(t=bn(p12.sum(axis=1).iloc[-1]), nt0=pct(sh_nt.loc[a0], 0), a0=fecha(a0, "m", L), nt1=pct(sh_nt.iloc[-1], 0),
                                mi0=pct(sh_mi.loc[a0], 0), mi1=pct(sh_mi.iloc[-1], 0))
    s_ev = sec("comercio-canasta", tx("s_evol", L), r2, f'<div class="grid">{g3}</div>')

    # ------------------------------------------------ balanza bilateral y China
    de = c["destinos"].set_index("fecha").sort_index().loc[:fin]
    og = c["origen"]
    og12 = og[(og["fecha"] > hace) & (og["fecha"] <= fin)].groupby("pais")["valor"].sum()
    d12 = de.loc[de.index > hace].sum()
    bal = {}
    for pais, (col, nm) in SOCIOS.items():
        if col in d12 and pais in og12:
            bal[nm[k]] = (d12[col] - og12[pais]) / 1e6
    bal = pd.Series(bal).sort_values()
    f4 = cs.base(L, height=380, fecha_x=False)
    f4.add_trace(go.Bar(y=list(bal.index), x=bal.round(2).tolist(), orientation="h", showlegend=False,
                        marker=dict(color=[cs.C3 if v >= 0 else cs.C2 for v in bal], line=dict(width=0)),
                        text=[num(float(v), 1, L, True) for v in bal], textposition="outside", cliponaxis=False,
                        hovertemplate="%{y}: US$%{x:+.1f}" + (" mil M" if L == "es" else " bn") + "<extra></extra>"))
    f4.add_vline(x=0, line=dict(color=cs.INK2, width=1))
    f4.update_xaxes(range=[float(bal.min()) * 1.35 - 0.5, max(0, float(bal.max())) * 1.35 + 0.5], showgrid=True, gridcolor=cs.GRID)
    f4.update_yaxes(ticksuffix="", tickfont=dict(size=12, color=cs.INK2))
    f4.update_layout(hovermode="closest", bargap=0.3)
    cs.ejes(f4, x="Miles de millones de dólares (12 meses)" if L == "es" else "US$ billions (12 months)")
    g4 = cs.bloque_grafico(tx("g_bil", L), cs.fig_html(f4, {"notime": True, "noy": True}, "g-com-bilateral"), tx("h_bil", L))
    opv = og.pivot_table(index="fecha", columns="pais", values="valor", aggfunc="sum").sort_index().loc[:fin]
    tot_pub = i["publicadas"].reindex(opv.index)
    o12 = opv.rolling(12).sum()
    t12 = tot_pub.rolling(12).sum()
    shc = (o12["China"] / t12 * 100).dropna()
    shu = (o12["Estados Unidos"] / t12 * 100).dropna()
    f5 = cs.base(L, height=380)
    cs.linea(f5, shc.index + pd.offsets.MonthEnd(0), shc, "China", cs.C2, width=2.6, lang=L)
    cs.linea(f5, shu.index + pd.offsets.MonthEnd(0), shu, SOCIOS["Estados Unidos"][1][k], cs.C1, width=2.6, lang=L)
    cs.ejes(f5, y="% de las importaciones" if L == "es" else "% of imports")
    g5 = cs.bloque_grafico(tx("g_ch", L), cs.fig_html(f5, {}, "g-com-china"), tx("h_ch", L))
    a0c = shc.index[0]
    peor, mejor = bal.index[0], bal.index[-1]
    r3 = tx("r_bil", L).format(s1=peor, t1=tx("deficit" if bal[peor] < 0 else "superavit", L), v1=bn(abs(bal[peor])),
                               s2=mejor, t2=tx("deficit" if bal[mejor] < 0 else "superavit", L), v2=bn(abs(bal[mejor])),
                               c0=pct(shc.iloc[0], 0), a0=a0c.year, c1=pct(shc.iloc[-1], 0), u0=pct(shu.iloc[0], 0), u1=pct(shu.iloc[-1], 0))
    s_bi = sec("comercio-bilateral", tx("s_bil", L), r3, f'<div class="grid">{g4}{g5}</div>')

    # ------------------------------------------------ apertura y concentracion
    pib = pd.read_csv(cs.DATA_DIR / "pib_colombia.csv", parse_dates=["fecha"]).set_index("fecha")["pib_nominal_billones_cop"].dropna().sort_index()
    trm = R.get("trm")
    if trm is None:
        from colombiamacro import modelo as mt
        trm = mt.cargar().extra["trm"].set_index("fecha")["trm"].sort_index()
    trm_q = trm.groupby(trm.index.to_period("Q")).mean()
    trm_q.index = trm_q.index.to_timestamp()
    pib_usd4 = (pib * 1e6 / trm_q.reindex(pib.index)).rolling(4).sum().dropna() / 1000          # miles de millones USD
    eq = e["total"].groupby(e.index.to_period("Q")).agg(["sum", "size"])
    iq = i["total"].groupby(i.index.to_period("Q")).agg(["sum", "size"])
    eq = eq[eq["size"] == 3]["sum"]
    iq = iq[iq["size"] == 3]["sum"]
    eq.index, iq.index = eq.index.to_timestamp(), iq.index.to_timestamp()
    ap = pd.DataFrame({"x": eq.rolling(4).sum() / 1e6, "m": iq.rolling(4).sum() / 1e6}).dropna()
    ap = ap.div(pib_usd4.reindex(ap.index), axis=0).dropna() * 100
    ap = ap.loc["2005":]
    xa = ap.index + pd.offsets.QuarterEnd(0)
    f6 = cs.base(L, height=360)
    for col, lbl, color in (("x", "lbl_apx", cs.C1), ("m", "lbl_apm", cs.C2)):
        f6.add_trace(go.Scatter(x=list(xa), y=ap[col].round(1).tolist(), mode="lines", stackgroup="a", name=tx(lbl, L),
                                line=dict(color=color, width=0.5), fillcolor=color, hovertemplate=tx(lbl, L) + ": %{y:.1f}%<extra></extra>"))
    cs.ejes(f6, y="% del PIB" if L == "es" else "% of GDP")
    g6 = cs.bloque_grafico(tx("g_ap", L), cs.fig_html(f6, {"noy": True}, "g-com-apertura"), tx("h_ap", L))
    dest12 = de.drop(columns="total").rolling(12).sum().dropna().loc["2005":]
    ne = num_equivalente(dest12)
    npr = num_equivalente(p12.loc["2005":])
    f7 = cs.base(L, height=360, suffix="")
    cs.linea(f7, ne.index + pd.offsets.MonthEnd(0), ne, tx("lbl_nd", L), cs.C1, width=2.4, fmt=".1f", suf="", lang=L)
    cs.linea(f7, npr.index + pd.offsets.MonthEnd(0), npr, tx("lbl_npr", L), cs.C3, width=2.0, fmt=".1f", suf="", lang=L)
    cs.ejes(f7, y="Número equivalente de socios o productos" if L == "es" else "Equivalent number of partners or products")
    g7 = cs.bloque_grafico(tx("g_hhi", L), cs.fig_html(f7, {}, "g-com-diversificacion"), tx("h_hhi", L))
    apt = ap.sum(axis=1)
    ne0 = ne.loc[:ne.index[-1] - pd.DateOffset(years=10)].iloc[-1]
    r4 = tx("r_ap", L).format(ap=pct(apt.iloc[-1]), ne=num(float(ne.iloc[-1]), 1, L), ne0=num(float(ne0), 1, L), np=num(float(npr.iloc[-1]), 1, L))
    s_ap = sec("comercio-apertura", tx("s_ap", L), r4, f'<div class="grid">{g6}{g7}</div>')

    items = "".join(f'<li><span class="ref">{ref}</span><span class="ref-u">{es if L == "es" else en}</span></li>' for ref, es, en in LITERATURA)
    s_lit = (
        f'<section id="comercio-literatura" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{tx("s_lit", L)}</h2></div>'
        f'<ol class="refs">{items}</ol></section>')

    # ------------------------------------------------ medidas adicionales
    cob = e12 / i12 * 100
    nt12 = e["no_tradicionales"].rolling(12).sum() / 1e6
    cf12 = e["cafe"].rolling(12).sum() / 1e6
    apt0 = apt.loc[:apt.index[-1] - pd.DateOffset(years=10)]
    china_bal = bal.get(SOCIOS["China"][1][k], np.nan)
    extra = [
        lec(tx("l_cob", L), pct(cob.loc[fin], 0), tx("l_cob_d", L).format(v=pct(cob.loc[hace], 0)), "", "#comercio-flujos"),
        lec(tx("l_nt", L), pct(nt12.loc[fin] / e12.loc[fin] * 100, 0), tx("l_nt_d", L).format(v=bn(nt12.loc[fin]), c=pct((nt12.loc[fin] / nt12.loc[hace] - 1) * 100, 1, True)),
            "", "#comercio-canasta"),
        lec(tx("l_cafe", L), pct(cf12.loc[fin] / e12.loc[fin] * 100, 0), tx("l_cafe_d", L).format(v=bn(cf12.loc[fin]), c=pct((cf12.loc[fin] / cf12.loc[hace] - 1) * 100, 1, True)),
            "", "#comercio-canasta"),
        lec(tx("l_px", L), pct(u["px"], 1, True), tx("l_px_d", L).format(v=pct(u["qx"], 1, True)), "", "#comercio-precios"),
        lec(tx("l_ti", L), pct(d_ti, 1, True) if d_ti is not None else "—", tx("l_ti_d", L), "", "#comercio-precios"),
        lec(tx("l_ap", L), pct(apt.iloc[-1]), tx("l_ap_d", L).format(v=pct(apt0.iloc[-1]) if len(apt0) else "—"), "", "#comercio-apertura"),
        lec(tx("l_ch", L), (("US$ " if L == "es" else "US$") + num(float(china_bal), 1, L, True) + (" mil M" if L == "es" else " bn")) if pd.notna(china_bal) else "—",
            tx("l_ch_d", L).format(p=pct(shc.iloc[-1], 0)), "warn" if pd.notna(china_bal) and china_bal < 0 else "", "#comercio-bilateral"),
    ]
    return "".join(extra), s_pq + s_ev + s_bi + s_ap + s_lit


def ventana_comercio(L) -> str:
    es = L == "es"
    T = (lambda a, b: a if es else b)
    return f"""<dialog class="explica" id="exp-comercio" aria-labelledby="exp-comercio-t">
<div class="ex-cab"><p class="ex-k">{T("Para entender", "To understand")} · DANE · DIAN · Banco de la República</p><h2 id="exp-comercio-t">{T("¿Cómo se miden las exportaciones e importaciones?", "How are exports and imports measured?")}</h2>
<button type="button" class="ex-x" data-cerrar aria-label="{T("Cerrar", "Close")}">✕</button></div>
<div class="ex-cuerpo">
<p class="ex-lede">{T("El DANE publica cada mes las exportaciones y las importaciones de bienes de Colombia a partir de los registros administrativos de las declaraciones de aduana que recibe la DIAN.",
 "DANE publishes Colombia's goods exports and imports every month from the administrative records of customs declarations received by DIAN.")}</p>
<ul class="ex-lista">
<li><b>{T("Exportaciones FOB", "FOB exports")}</b>: {T("valor de la mercancía puesta en el puerto de salida, sin fletes ni seguros internacionales.", "value of goods at the port of departure, excluding international freight and insurance.")}</li>
<li><b>{T("Importaciones CIF", "CIF imports")}</b>: {T("valor de la mercancía más fletes y seguros hasta llegar a Colombia. Por eso la balanza con cada socio (FOB − CIF) exagera un poco el déficit frente a la de la balanza de pagos.", "value of goods plus freight and insurance to Colombia. This is why the balance with each partner (FOB − CIF) slightly overstates the deficit compared with the balance of payments.")}</li>
<li><b>{T("Tradicionales y no tradicionales", "Traditional and non-traditional")}</b>: {T("las tradicionales son café, carbón, petróleo y derivados y ferroníquel; las demás son no tradicionales.", "traditional exports are coffee, coal, oil and derivatives and ferronickel; the rest are non-traditional.")}</li>
<li><b>CUODE</b>: {T("clasificación de las importaciones según su uso económico: consumo, materias primas y bienes de capital.", "classification of imports by economic use: consumption, raw materials and capital goods.")}</li>
</ul>
<h3>{T("Precio frente a cantidad", "Price versus quantity")}</h3>
<p>{T("El valor exportado puede subir porque se vende más (volumen) o porque se vende más caro (precio). El Banco de la República calcula índices de precios de exportación e importación en dólares, con los que construye los términos de intercambio (precio de lo que se vende sobre precio de lo que se compra). Esta página divide el cambio del valor en precio y volumen implícito: (1 + valor) / (1 + precio) − 1.",
 "Export value can rise because more is sold (volume) or because it sells at a higher price (price). Banco de la República computes export and import price indices in dollars, which it uses to build the terms of trade (price of what is sold over price of what is bought). This page splits the change in value into price and implied volume: (1 + value) / (1 + price) − 1.")}</p>
<h3>{T("Dos medidas útiles", "Two useful measures")}</h3>
<ul class="ex-lista">
<li><b>{T("Apertura", "Openness")}</b>: {T("exportaciones más importaciones de bienes sobre el PIB (en dólares, con la TRM promedio).", "goods exports plus imports over GDP (in dollars, at the average TRM).")}</li>
<li><b>{T("Número equivalente", "Equivalent number")}</b>: {T("1 dividido por el índice de Herfindahl (suma de las participaciones al cuadrado). Si las exportaciones se repartieran por igual entre 4 destinos, daría 4.", "1 divided by the Herfindahl index (sum of squared shares). If exports were split equally across 4 destinations, it would be 4.")}</li>
</ul>
<h3>{T("Fuentes oficiales", "Official sources")}</h3>
<ul class="ex-fuentes">
<li><a href="https://www.dane.gov.co/index.php/estadisticas-por-tema/comercio-internacional/exportaciones" target="_blank" rel="noopener">DANE — {T("Exportaciones", "Exports")}</a></li>
<li><a href="https://www.dane.gov.co/index.php/estadisticas-por-tema/comercio-internacional/importaciones" target="_blank" rel="noopener">DANE — {T("Importaciones", "Imports")}</a></li>
<li><a href="https://suameca.banrep.gov.co/graficador-series/" target="_blank" rel="noopener">{T("Banco de la República — índices de precios del comercio exterior y términos de intercambio", "Banco de la República — foreign trade price indices and terms of trade")}</a></li>
</ul>
</div></dialog>"""
