"""Pagina del sector empresarial (v12.15): doce medidas, las 10.000 empresas mas grandes (tamano, rentabilidad y
endeudamiento), sectores, regiones, concentracion, la bolsa por dentro (acciones y sectores del COLCAP), como se
financian las empresas, nacimiento y cierre de empresas, ventana explicativa y literatura.

Solo datos observados: Supersociedades (10.000 empresas mas grandes, datos.gov.co), Confecamaras/RUES (conteos del
registro mercantil), Banco de la Republica (cartera, tasas, posicion financiera, deuda externa privada, IED) y
precios de las acciones del COLCAP.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

TX = {
    "s_medidas": ("Las empresas de Colombia en doce medidas", "Colombia's companies in twelve measures"),
    "s_grandes": ("Las 10.000 empresas más grandes", "The 10,000 largest companies"),
    "s_sectores": ("¿En qué sectores están y cuáles ganan más?", "Which sectors are they in and which earn most?"),
    "s_regiones": ("¿Dónde están las empresas?", "Where are the companies?"),
    "s_conc": ("¿Qué tan concentrada está la actividad?", "How concentrated is activity?"),
    "s_acciones": ("La bolsa por dentro: acciones y sectores", "Inside the stock market: shares and sectors"),
    "s_fin": ("¿Cómo se financian las empresas?", "How do companies finance themselves?"),
    "s_registro": ("¿Nacen o cierran empresas?", "Are companies being born or closing?"),
    "s_lit": ("Bases metodológicas y literatura", "Methodological basis and literature"),
    # lecturas
    "l_ing": ("Ingresos de las 10.000 más grandes · {a}", "Revenue of the 10,000 largest · {a}"), "l_ing_d": ("billones de pesos · {c} frente a {b} (real {r})", "COP trillion · {c} vs {b} (real {r})"),
    "l_gan": ("Utilidades", "Profits"), "l_gan_d": ("billones de pesos · {c} frente a {b}", "COP trillion · {c} vs {b}"),
    "l_mar": ("Margen neto", "Net margin"), "l_mar_d": ("utilidad por cada $100 vendidos · {b}: {v}", "profit per $100 of sales · {b}: {v}"),
    "l_roe": ("Rentabilidad del patrimonio", "Return on equity"), "l_roe_d": ("utilidad / patrimonio · {b}: {v}", "profit / equity · {b}: {v}"),
    "l_end": ("Endeudamiento", "Leverage"), "l_end_d": ("pasivos / activos · {b}: {v}", "liabilities / assets · {b}: {v}"),
    "l_conc": ("Peso de las 100 más grandes", "Share of the 100 largest"), "l_conc_d": ("de los ingresos de las 10.000 · 10 mayores: {v}", "of the 10,000's revenue · top 10: {v}"),
    "l_sec": ("Sector con más ingresos", "Sector with most revenue"), "l_sec_d": ("{v} de los ingresos · mayor margen: {s} ({m})", "{v} of revenue · highest margin: {s} ({m})"),
    "l_reg": ("Bogotá y Cundinamarca", "Bogotá and Cundinamarca"), "l_reg_d": ("de los ingresos · {n} de las 10.000 empresas", "of revenue · {n} of the 10,000 companies"),
    "l_colcap": ("Bolsa (COLCAP)", "Stock market (COLCAP)"), "l_colcap_d": ("en 12 meses · {s} de {t} acciones subieron", "over 12 months · {s} of {t} shares rose"),
    "l_cred": ("Crédito a empresas", "Credit to companies"), "l_cred_d": ("cartera comercial, crecimiento real anual · tasa preferencial {t}", "commercial loans, annual real growth · preferential rate {t}"),
    "l_soc": ("Sociedades creadas (12 meses)", "Companies created (12 months)"), "l_soc_d": ("{c} frente a un año antes · hasta {f}", "{c} vs a year earlier · to {f}"),
    "l_ied": ("Inversión extranjera directa", "Foreign direct investment"), "l_ied_d": ("US$ millones, 4 trimestres a {f} · {c} en un año", "US$ million, 4 quarters to {f} · {c} over a year"),
    # respuestas
    "r_medidas": ("Las 10.000 empresas más grandes vendieron ${i} billones en {a} ({c} nominal frente a {b}) y ganaron ${g} billones: {m} por cada $100 de ventas. "
                  "Las 100 mayores concentran {t} de esos ingresos y {s} es el sector que más vende. "
                  "El crédito a empresas crece {k} real al año y en los últimos 12 meses se crearon {n} sociedades.",
                  "The 10,000 largest companies sold COP {i} trillion in {a} ({c} nominal vs {b}) and earned COP {g} trillion: {m} per $100 of sales. "
                  "The top 100 account for {t} of that revenue and {s} is the sector that sells most. "
                  "Credit to companies grows {k} in real terms a year and {n} companies were created over the last 12 months."),
    "r_grandes": ("Entre {a0} y {a1} los ingresos pasaron de ${i0} a ${i1} billones y las utilidades de ${g0} a ${g1} billones. "
                  "El margen neto fue {m1} en {a1} (máximo de la serie: {mx} en {amx}) y el endeudamiento {e1}. "
                  "La lista cambia cada año (entran y salen empresas), por eso las comparaciones muestran a las 10.000 más grandes de cada año.",
                  "Between {a0} and {a1} revenue went from COP {i0} to {i1} trillion and profits from COP {g0} to {g1} trillion. "
                  "The net margin was {m1} in {a1} (series high: {mx} in {amx}) and leverage {e1}. "
                  "The list changes every year (companies enter and leave), so comparisons show each year's 10,000 largest."),
    "r_sectores": ("{s1} genera {p1} de los ingresos, {s2} {p2} y {s3} {p3}. El mayor margen está en {sm} ({vm}) y el menor en {sn} ({vn}). "
                   "{sc} es el sector cuyos ingresos más crecieron frente a {b} ({vc}); {sd}, el que más cayó ({vd}).",
                   "{s1} generates {p1} of revenue, {s2} {p2} and {s3} {p3}. The highest margin is in {sm} ({vm}) and the lowest in {sn} ({vn}). "
                   "{sc} is the sector whose revenue grew most vs {b} ({vc}); {sd}, the one that fell most ({vd})."),
    "r_regiones": ("Bogotá y Cundinamarca concentran {pb} de los ingresos y {nb} de las 10.000 empresas; Antioquia, {pa} de los ingresos. "
                   "Las demás regiones suman {po}. Las cifras se asignan al domicilio de la empresa, no a donde produce.",
                   "Bogotá and Cundinamarca hold {pb} of revenue and {nb} of the 10,000 companies; Antioquia, {pa} of revenue. "
                   "The other regions add up to {po}. Figures are assigned to the company's registered address, not where it produces."),
    "r_conc": ("Las 10 empresas más grandes generan {t10} de los ingresos de las 10.000, las 100 mayores {t100} y las 1.000 mayores {t1000}. "
               "La mayor es {e1} (${v1} billones, {p1} del total).",
               "The 10 largest companies generate {t10} of the 10,000's revenue, the top 100 {t100} and the top 1,000 {t1000}. "
               "The largest is {e1} (COP {v1} trillion, {p1} of the total)."),
    "r_acciones": ("En los últimos 12 meses {s} de las {t} empresas del COLCAP subieron en bolsa. La que más subió fue {mx} ({vmx}) y la que más cayó {mn} ({vmn}). "
                   "El sector financiero pesa {pf} del índice.",
                   "Over the last 12 months {s} of the {t} COLCAP companies rose on the stock market. The top gainer was {mx} ({vmx}) and the biggest loser {mn} ({vmn}). "
                   "The financial sector weighs {pf} of the index."),
    "r_fin": ("La cartera comercial (crédito a empresas en pesos) crece {k} real al año, frente a {kt} del crédito total. "
              "El crédito corporativo (preferencial) cuesta {tp} y el ordinario {to}. Las sociedades no financieras deben, en términos netos, {sn} del PIB al resto de sectores, "
              "y la deuda externa del sector privado suma US${de} millones ({fde}).",
              "Commercial loans (peso credit to companies) grow {k} in real terms a year, vs {kt} for total credit. "
              "Corporate (preferential) credit costs {tp} and ordinary {to}. Non-financial corporations owe, in net terms, {sn} of GDP to other sectors, "
              "and private-sector external debt totals US${de} million ({fde})."),
    "r_registro": ("En los últimos 12 meses se matricularon {sm} sociedades y {nm} personas naturales con negocio en las cámaras de comercio, y se cancelaron {sc} y {nc}. "
                   "Frente al año anterior, la creación de sociedades cambió {cs}. Las cancelaciones incluyen depuraciones del registro, por eso tienen saltos.",
                   "Over the last 12 months {sm} companies and {nm} self-employed persons registered with the chambers of commerce, and {sc} and {nc} were cancelled. "
                   "Compared with the previous year, company creation changed {cs}. Cancellations include registry clean-ups, hence the jumps."),
    # graficos
    "g_tam": ("Ingresos y utilidades de las 10.000 más grandes", "Revenue and profits of the 10,000 largest"),
    "h_tam": ("Billones de pesos corrientes. Barras: ingresos operacionales (eje izquierdo). Línea: utilidades (eje derecho).",
              "Current COP trillion. Bars: operating revenue (left axis). Line: profits (right axis)."),
    "g_rat": ("Rentabilidad y endeudamiento", "Profitability and leverage"),
    "h_rat": ("Margen neto = utilidad / ingresos; rentabilidad del patrimonio = utilidad / patrimonio; endeudamiento = pasivos / activos. Todo para el agregado de las 10.000 de cada año.",
              "Net margin = profit / revenue; return on equity = profit / equity; leverage = liabilities / assets. All for the aggregate of each year's 10,000."),
    "lbl_ing": ("Ingresos", "Revenue"), "lbl_gan": ("Utilidades", "Profits"), "lbl_mar": ("Margen neto", "Net margin"),
    "lbl_roe": ("Rentabilidad del patrimonio", "Return on equity"), "lbl_end": ("Endeudamiento", "Leverage"),
    "g_sec": ("Ingresos por sector ({a})", "Revenue by sector ({a})"),
    "h_sec": ("Participación de cada macrosector en los ingresos de las 10.000 empresas. Pase el cursor para ver el valor y el cambio frente al año anterior.",
              "Share of each macro-sector in the 10,000 companies' revenue. Hover for the value and the change vs the previous year."),
    "g_secr": ("Rentabilidad por sector ({a})", "Profitability by sector ({a})"),
    "h_secr": ("Margen neto y rentabilidad del patrimonio de cada macrosector.", "Net margin and return on equity of each macro-sector."),
    "tab_sec": ("Indicadores por sector", "Indicators by sector"),
    "th_sec": (("Sector", "Empresas", "Ingresos (billones)", "% de ingresos", "Cambio anual", "Margen", "Rentabilidad patrimonio", "Endeudamiento"),
               ("Sector", "Companies", "Revenue (trillion)", "% of revenue", "Annual change", "Margin", "Return on equity", "Leverage")),
    "g_reg": ("Ingresos y número de empresas por región ({a})", "Revenue and number of companies by region ({a})"),
    "h_reg": ("Participación de cada región (según el domicilio de la empresa) en los ingresos y en el número de empresas.",
              "Share of each region (by company address) in revenue and in the number of companies."),
    "lbl_pi": ("% de los ingresos", "% of revenue"), "lbl_pn": ("% de las empresas", "% of companies"),
    "g_conc": ("Curva de concentración de los ingresos", "Revenue concentration curve"),
    "h_conc": ("Porcentaje de los ingresos de las 10.000 que generan las N empresas más grandes (eje horizontal en escala logarítmica).",
               "Percentage of the 10,000's revenue generated by the N largest companies (horizontal axis on a log scale)."),
    "tab_top": ("Las 15 empresas con más ingresos ({a})", "The 15 companies with most revenue ({a})"),
    "th_top": (("#", "Empresa", "Sector", "Ingresos (billones)", "Utilidad (billones)", "Margen"),
               ("#", "Company", "Sector", "Revenue (trillion)", "Profit (trillion)", "Margin")),
    "g_acc": ("Cambio de cada acción del COLCAP en 12 meses", "12-month change of each COLCAP share"),
    "h_acc": ("Variación del precio de cierre en 52 semanas (sin dividendos), una barra por empresa (su acción de mayor peso en el índice). Verde: subió; naranja: bajó.",
              "52-week change in closing price (excluding dividends), one bar per company (its share with the largest index weight). Green: rose; orange: fell."),
    "g_secc": ("Peso de cada sector en el COLCAP", "Weight of each sector in the COLCAP"),
    "h_secc": ("Suma de los pesos de las acciones de cada sector en la canasta vigente del índice.", "Sum of the weights of each sector's shares in the index's current basket."),
    "g_cart": ("Crédito a empresas y su costo", "Credit to companies and its cost"),
    "h_cart": ("Líneas sólidas: crecimiento real anual de la cartera comercial y de la cartera total (eje izquierdo). Punteadas: tasa del crédito preferencial y ordinario (eje derecho).",
               "Solid lines: annual real growth of commercial and total loans (left axis). Dotted: preferential and ordinary lending rates (right axis)."),
    "lbl_kc": ("Cartera comercial (real)", "Commercial loans (real)"), "lbl_kt": ("Cartera total (real)", "Total loans (real)"),
    "lbl_tp": ("Tasa preferencial", "Preferential rate"), "lbl_to": ("Tasa ordinaria", "Ordinary rate"),
    "g_pos": ("Posición financiera neta por sector (% del PIB)", "Net financial position by sector (% of GDP)"),
    "h_pos": ("Activos financieros menos pasivos de cada sector institucional (cuentas financieras del Banco de la República). Negativo = el sector se financia con los demás.",
              "Financial assets minus liabilities of each institutional sector (Banco de la República financial accounts). Negative = the sector is financed by the others."),
    "lbl_snf": ("Sociedades no financieras", "Non-financial corporations"), "lbl_sf": ("Sociedades financieras", "Financial corporations"),
    "lbl_gob": ("Gobierno general", "General government"), "lbl_hog": ("Hogares", "Households"),
    "g_reg_m": ("Empresas que nacen y que cierran (suma de 12 meses)", "Companies born and closing (12-month sum)"),
    "h_reg_m": ("Matrículas y cancelaciones en el registro mercantil de las cámaras de comercio (RUES). Sociedades = personas jurídicas principales y entidades sin ánimo de lucro.",
                "Registrations and cancellations in the chambers of commerce's business register (RUES). Companies = principal legal entities and non-profits."),
    "lbl_sm": ("Sociedades: matrículas", "Companies: registrations"), "lbl_sc": ("Sociedades: cancelaciones", "Companies: cancellations"),
    "lbl_nm": ("Personas naturales: matrículas", "Self-employed: registrations"), "lbl_nc": ("Personas naturales: cancelaciones", "Self-employed: cancellations"),
    "sec": {"COMERCIO": ("Comercio", "Commerce"), "SERVICIOS": ("Servicios", "Services"), "MANUFACTURA": ("Manufactura", "Manufacturing"),
            "CONSTRUCCIÓN": ("Construcción", "Construction"), "AGROPECUARIO": ("Agropecuario", "Agriculture"), "MINERO": ("Minero e hidrocarburos", "Mining and oil")},
}
LITERATURA = [
    ("Modigliani, F. y Miller, M. H. (1958). The Cost of Capital, Corporation Finance and the Theory of Investment. <i>American Economic Review</i>, 48(3), 261–297.",
     "Cómo se relacionan endeudamiento, patrimonio y valor de la empresa.", "How leverage, equity and firm value relate."),
    ("Rajan, R. G. y Zingales, L. (1998). Financial Dependence and Growth. <i>American Economic Review</i>, 88(3), 559–586.",
     "Los sectores que dependen del crédito crecen más donde el sistema financiero es más profundo.", "Credit-dependent sectors grow faster where the financial system is deeper."),
    ("Bernanke, B. S., Gertler, M. y Gilchrist, S. (1999). The Financial Accelerator in a Quantitative Business Cycle Framework. <i>Handbook of Macroeconomics</i>, 1C, 1341–1393.",
     "La salud financiera de las empresas amplifica el ciclo económico.", "Firms' financial health amplifies the business cycle."),
    ("Gabaix, X. (2011). The Granular Origins of Aggregate Fluctuations. <i>Econometrica</i>, 79(3), 733–772.",
     "Cuando unas pocas empresas son muy grandes, sus choques mueven a toda la economía.", "When a few firms are very large, their shocks move the whole economy."),
    ("Hsieh, C.-T. y Klenow, P. J. (2009). Misallocation and Manufacturing TFP in China and India. <i>Quarterly Journal of Economics</i>, 124(4), 1403–1448.",
     "La asignación de recursos entre empresas y la productividad agregada.", "Resource allocation across firms and aggregate productivity."),
    ("Superintendencia de Sociedades. Informe de las 10.000 empresas más grandes del país (2026, cifras a diciembre de 2025).",
     "Fuente de las cifras de tamaño, rentabilidad y endeudamiento.", "Source of the size, profitability and leverage figures."),
    ("Banco de la República. Reporte de Estabilidad Financiera (semestral).", "Seguimiento oficial de la situación financiera de las empresas y su deuda.", "Official monitoring of firms' financial condition and debt."),
]


def nombre_emp(n: str, largo: int = 46) -> str:
    """Razon social legible: sin la coletilla de siglas y recortada en una palabra completa."""
    import re
    n = re.split(r"\s+(?:PUDIENDO|ANTES|SIGLA)\b", str(n), flags=re.I)[0].strip().title()
    n = re.sub(r"\b(De|Del|Y|La|Las|Los|El)\b", lambda m_: m_.group(1).lower(), n)
    return n if len(n) <= largo else n[:largo].rsplit(" ", 1)[0] + "…"


def tx(k, L):
    return TX[k][0 if L == "es" else 1]


def razones(df: pd.DataFrame) -> pd.DataFrame:
    """Margen neto, rentabilidad del patrimonio y endeudamiento (%) a partir de sumas agregadas."""
    return pd.DataFrame({"margen": df["ganancia"] / df["ingresos"] * 100, "roe": df["ganancia"] / df["patrimonio"] * 100,
                         "endeudamiento": df["pasivos"] / df["activos"] * 100}, index=df.index)


def meses_completos(reg: pd.DataFrame) -> pd.DataFrame:
    """Quita el ultimo mes si aun esta incompleto (menos de la mitad de la mediana de los 12 anteriores)."""
    tot = reg.groupby("mes")["matriculas"].sum().sort_index()
    while len(tot) > 13 and tot.iloc[-1] < 0.5 * tot.iloc[-13:-1].median():
        tot = tot.iloc[:-1]
    return reg[reg["mes"] <= tot.index[-1]]


def construir_empresas(d, L):
    """Devuelve (antes, medio, despues): medidas; empresas grandes; bolsa, financiacion y registro."""
    from colombiamacro import modelo as mt
    from colombiamacro.fuentes import empresas as fe
    from colombiamacro.fuentes import tasas_mercado as tmk
    from colombiamacro.sitio import construir as cs
    from colombiamacro.sitio.tasas_extra import real_anual
    num, fecha, esc = cs.num, cs.fecha, cs.esc
    cs.LANG_ACTUAL[0] = L
    k = 0 if L == "es" else 1
    E = fe.cargar()
    if E is None:
        return "", "", ""
    pct = lambda v, dec=1, sg=False: num(float(v), dec, L, sg, "%")
    bil = lambda v, dec=1: num(float(v), dec, L)
    secn = lambda s: TX["sec"].get(s, (s.title(), s.title()))[k]
    regn = lambda r: {"BOGOTÁ - CUNDINAMARCA": "Bogotá-Cundinamarca", "COSTA PACÍFICA": "Costa Pacífica" if L == "es" else "Pacific coast",
                      "COSTA ATLÁNTICA": "Costa Atlántica" if L == "es" else "Atlantic coast", "REGIÓN CARIBE": "Región Caribe" if L == "es" else "Caribbean region",
                      "OTROS": "Otras" if L == "es" else "Other", "LLANOS": "Llanos"}.get(r, r.title())
    agg = E["agg"]
    tot = agg[agg["dimension"] == "total"].set_index("ano").sort_index()
    rz = razones(tot)
    a1, a0 = int(tot.index[-1]), int(tot.index[-2])
    u, b = tot.loc[a1], tot.loc[a0]
    infl = d.inflacion.set_index("fecha")["inflacion_anual"].sort_index()
    ipc_med = d.inflacion.set_index("fecha")["inflacion_anual"]
    # inflacion promedio del ano (para el crecimiento real de ingresos): variacion del IPC promedio anual
    pi = float(ipc_med[str(a1)].mean()) if str(a1) in ipc_med.index.year.astype(str) else float(ipc_med.iloc[-1])
    c_ing = (u["ingresos"] / b["ingresos"] - 1) * 100
    r_ing = ((1 + c_ing / 100) / (1 + pi / 100) - 1) * 100
    sec = agg[(agg["dimension"] == "macrosector")].pivot(index="categoria", columns="ano", values=["ingresos", "ganancia", "activos", "pasivos", "patrimonio", "empresas"])
    s1 = pd.DataFrame({c: sec[c][a1] for c in ("ingresos", "ganancia", "activos", "pasivos", "patrimonio", "empresas")})
    s1 = s1.join(razones(s1))
    s1["part"] = s1["ingresos"] / s1["ingresos"].sum() * 100
    s1["cambio"] = (sec["ingresos"][a1] / sec["ingresos"][a0] - 1) * 100
    s1 = s1.sort_values("ingresos", ascending=False)
    reg = agg[(agg["dimension"] == "region") & (agg["ano"] == a1)].set_index("categoria")
    reg = reg.assign(pi=reg["ingresos"] / reg["ingresos"].sum() * 100, pn=reg["empresas"] / reg["empresas"].sum() * 100).sort_values("ingresos")
    conc = agg[agg["dimension"] == "concentracion"].pivot(index="empresas", columns="ano", values="ingresos")
    T = tmk.cargar()
    infl_m = infl.copy()
    infl_m.index = infl_m.index.to_period("M").to_timestamp()
    kc = real_anual(T["cartera_comercial"], infl_m).dropna()
    kt = real_anual(T["cartera_total"], infl_m).dropna()
    tp = T["col_preferencial"].dropna()
    to = T["col_ordinario"].dropna()
    B = E["banrep"]
    regm = meses_completos(E["registro"]) if E["registro"] is not None else None

    def seccion(sid, titulo, resp, cuerpo):
        return (f'<section id="{sid}" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{titulo}</h2></div>'
                f'{cs.respuesta_html(resp, L)}{cuerpo}</section>')

    def lec(kk, v, dsc, tono, href):
        return (f'<a class="lec {tono}" href="{href}"><span class="lec-k">{kk}</span><b class="lec-v">{v}</b>'
                f'<span class="lec-d">{dsc}</span></a>')

    # ------------------------------------------------ acciones del COLCAP (12 meses por emisor)
    can = d.canasta.copy()
    precios = d.acciones.pivot_table(index="fecha", columns="ticker", values="cierre").sort_index()
    principal = can.sort_values("peso", ascending=False).drop_duplicates("emisor")
    ret = []
    for r_ in principal.itertuples():
        if r_.ticker not in precios:
            continue
        p = precios[r_.ticker].dropna()
        prev = p[p.index <= p.index[-1] - pd.Timedelta(days=364)]
        if prev.empty:
            continue
        ret.append((r_.emisor, r_.sector, float(p.iloc[-1] / prev.iloc[-1] - 1) * 100))
    ret = sorted(ret, key=lambda x: x[2])
    sube = sum(1 for x in ret if x[2] > 0)
    colcap = d.colcap.dropna(subset=["colcap_puntos"]).set_index("fecha")["colcap_puntos"]
    col12 = float(colcap.iloc[-1] / colcap.loc[:colcap.index[-1] - pd.DateOffset(years=1)].iloc[-1] - 1) * 100
    corto = lambda n: (n.title().replace(" Sa", "").replace(" Esp", " ESP"))[:30]

    # ------------------------------------------------ medidas
    top100 = float(conc.loc[100, a1])
    smax = s1["margen"].idxmax()
    bog = reg.loc["BOGOTÁ - CUNDINAMARCA"] if "BOGOTÁ - CUNDINAMARCA" in reg.index else None
    ult_reg = None
    if regm is not None:
        rs = regm[regm["categoria"].str.startswith("SOCIEDAD")].set_index("mes")["matriculas"].sort_index()
        f_r = rs.index[-1]
        s12 = rs.loc[f_r - pd.DateOffset(months=11):].sum()
        s12b = rs.loc[f_r - pd.DateOffset(months=23):f_r - pd.DateOffset(months=12)].sum()
        ult_reg = (f_r, s12, (s12 / s12b - 1) * 100)
    ied = d.extra["ied_musd"].set_index("fecha")["ied_musd"].sort_index()
    ied4 = ied.rolling(4).sum().dropna()
    tiles = [
        lec(tx("l_ing", L).format(a=a1), "$" + bil(u["ingresos"], 0), tx("l_ing_d", L).format(c=pct(c_ing, 1, True), b=a0, r=pct(r_ing, 1, True)), "", "#em-grandes"),
        lec(tx("l_gan", L), "$" + bil(u["ganancia"], 1), tx("l_gan_d", L).format(c=pct((u["ganancia"] / b["ganancia"] - 1) * 100, 1, True), b=a0), "", "#em-grandes"),
        lec(tx("l_mar", L), pct(rz.loc[a1, "margen"]), tx("l_mar_d", L).format(b=a0, v=pct(rz.loc[a0, "margen"])), "", "#em-grandes"),
        lec(tx("l_roe", L), pct(rz.loc[a1, "roe"]), tx("l_roe_d", L).format(b=a0, v=pct(rz.loc[a0, "roe"])), "", "#em-grandes"),
        lec(tx("l_end", L), pct(rz.loc[a1, "endeudamiento"]), tx("l_end_d", L).format(b=a0, v=pct(rz.loc[a0, "endeudamiento"])), "", "#em-grandes"),
        lec(tx("l_conc", L), pct(top100), tx("l_conc_d", L).format(v=pct(conc.loc[10, a1])), "", "#em-concentracion"),
        lec(tx("l_sec", L), secn(s1.index[0]), tx("l_sec_d", L).format(v=pct(s1["part"].iloc[0]), s=secn(smax), m=pct(s1.loc[smax, "margen"])), "", "#em-sectores"),
        lec(tx("l_reg", L), pct(bog["pi"]) if bog is not None else "—", tx("l_reg_d", L).format(n=pct(bog["pn"], 0) if bog is not None else "—"), "", "#em-regiones"),
        lec(tx("l_colcap", L), pct(col12, 1, True), tx("l_colcap_d", L).format(s=sube, t=len(ret)), "", "#empresas"),
        lec(tx("l_cred", L), pct(kc.iloc[-1], 1, True), tx("l_cred_d", L).format(t=pct(tp.iloc[-1], 2)), "warn" if kc.iloc[-1] < 0 else "", "#em-financiacion"),
        lec(tx("l_soc", L), num(float(ult_reg[1]), 0, L) if ult_reg else "—",
            tx("l_soc_d", L).format(c=pct(ult_reg[2], 1, True), f=fecha(ult_reg[0], "m", L)) if ult_reg else "", "", "#em-registro"),
        lec(tx("l_ied", L), "US$" + num(float(ied4.iloc[-1]), 0, L),
            tx("l_ied_d", L).format(f=fecha(ied4.index[-1], "q", L), c=pct((ied4.iloc[-1] / ied4.iloc[-5] - 1) * 100, 1, True)), "", "#em-financiacion"),
    ]
    r0 = tx("r_medidas", L).format(i=bil(u["ingresos"], 0), a=a1, c=pct(c_ing, 1, True), b=a0, g=bil(u["ganancia"], 1), m="$" + num(float(rz.loc[a1, "margen"]), 1, L),
                                   t=pct(top100), s=secn(s1.index[0]), k=pct(kc.iloc[-1], 1, True),
                                   n=num(float(ult_reg[1]), 0, L) if ult_reg else "—")
    antes = seccion("em-medidas", tx("s_medidas", L), r0, f'<div class="lecturas ocho">{"".join(tiles)}</div>')

    # ------------------------------------------------ las 10.000
    anos = [str(a) for a in tot.index]
    f1 = cs.base(L, height=360, fecha_x=False, suffix="")
    f1.add_trace(go.Bar(x=anos, y=tot["ingresos"].round(1).tolist(), name=tx("lbl_ing", L), marker=dict(color=cs.C1, line=dict(width=0)),
                        text=["$" + bil(v, 0) for v in tot["ingresos"]], textposition="inside", hovertemplate="%{x}: $%{y:,.1f}<extra></extra>"))
    f1.add_trace(go.Scatter(x=anos, y=tot["ganancia"].round(1).tolist(), name=tx("lbl_gan", L), yaxis="y2", mode="lines+markers+text",
                            line=dict(color=cs.C2, width=2.6), marker=dict(size=8, color=cs.C2), text=["$" + bil(v, 1) for v in tot["ganancia"]],
                            textposition="top center", cliponaxis=False, hovertemplate="%{x}: $%{y:,.1f}<extra></extra>"))
    f1.update_layout(yaxis2=dict(overlaying="y", side="right", showgrid=False, zeroline=False, fixedrange=True, rangemode="tozero",
                                 range=[0, float(tot["ganancia"].max()) * 1.35], tickfont=dict(size=11.5, color=cs.MUTED)),
                     bargap=0.35, hovermode="closest")
    cs.ejes(f1, y="Ingresos (billones de pesos)" if L == "es" else "Revenue (COP trillion)", y2="Utilidades (billones)" if L == "es" else "Profits (COP trillion)")
    q_btn = (f'<button type="button" class="ex-q" data-dialog="exp-empresas" aria-haspopup="dialog" '
             f'title="{"¿De dónde salen estas cifras?" if L == "es" else "Where do these figures come from?"}">?</button>')
    g1 = cs.bloque_grafico(tx("g_tam", L), cs.fig_html(f1, {"notime": True, "noy": True}, "g-em-tamano"), tx("h_tam", L))
    g1 = g1.replace("</figcaption>", f" {q_btn}</figcaption>", 1)
    f2 = cs.base(L, height=360, fecha_x=False)
    for col, lbl, color in (("margen", "lbl_mar", cs.C1), ("roe", "lbl_roe", cs.C3), ("endeudamiento", "lbl_end", cs.C7)):
        f2.add_trace(go.Scatter(x=anos, y=rz[col].round(1).tolist(), name=tx(lbl, L), mode="lines+markers+text", line=dict(color=color, width=2.4),
                                marker=dict(size=7, color=color), text=[pct(v) for v in rz[col]], textposition="top center", cliponaxis=False,
                                hovertemplate=tx(lbl, L) + " %{x}: %{y:.1f}%<extra></extra>"))
    f2.update_yaxes(range=[0, float(rz.max().max()) * 1.15])
    f2.update_layout(hovermode="closest")
    cs.ejes(f2, y="Porcentaje" if L == "es" else "Percent")
    g2 = cs.bloque_grafico(tx("g_rat", L), cs.fig_html(f2, {"notime": True, "noy": True}, "g-em-razones"), tx("h_rat", L))
    amx = int(rz["margen"].idxmax())
    r1 = tx("r_grandes", L).format(a0=anos[0], a1=a1, i0=bil(tot["ingresos"].iloc[0], 0), i1=bil(u["ingresos"], 0), g0=bil(tot["ganancia"].iloc[0], 1),
                                   g1=bil(u["ganancia"], 1), m1=pct(rz.loc[a1, "margen"]), mx=pct(rz.loc[amx, "margen"]), amx=amx, e1=pct(rz.loc[a1, "endeudamiento"]))
    s_gr = seccion("em-grandes", tx("s_grandes", L), r1, f'<div class="grid">{g1}{g2}</div>') + ventana_empresas(u, a1, L, num)

    # ------------------------------------------------ sectores
    ss = s1.sort_values("part")
    f3 = cs.base(L, height=330, fecha_x=False)
    f3.add_trace(go.Bar(y=[secn(s) for s in ss.index], x=ss["part"].round(1).tolist(), orientation="h", showlegend=False,
                        marker=dict(color=cs.C1, line=dict(width=0)), text=[pct(v) for v in ss["part"]], textposition="outside", cliponaxis=False,
                        customdata=[[bil(i_, 0), pct(c_, 1, True)] for i_, c_ in zip(ss["ingresos"], ss["cambio"])],
                        hovertemplate="%{y}: %{x:.1f}%<br>$%{customdata[0]} " + ("billones" if L == "es" else "trillion") + " · %{customdata[1]}<extra></extra>"))
    f3.update_xaxes(ticksuffix="%", range=[0, float(ss["part"].max()) * 1.25], showgrid=True, gridcolor=cs.GRID)
    f3.update_yaxes(ticksuffix="", tickfont=dict(size=12, color=cs.INK2))
    f3.update_layout(hovermode="closest", bargap=0.3)
    cs.ejes(f3, x="% de los ingresos de las 10.000" if L == "es" else "% of the 10,000's revenue")
    g3 = cs.bloque_grafico(tx("g_sec", L).format(a=a1), cs.fig_html(f3, {"notime": True, "noy": True}, "g-em-sectores"), tx("h_sec", L))
    sr = s1.sort_values("margen")
    f4 = cs.base(L, height=330, fecha_x=False)
    for col, lbl, color in (("margen", "lbl_mar", cs.C1), ("roe", "lbl_roe", cs.C3)):
        f4.add_trace(go.Bar(y=[secn(s) for s in sr.index], x=sr[col].round(1).tolist(), orientation="h", name=tx(lbl, L),
                            marker=dict(color=color, line=dict(width=0)), text=[pct(v) for v in sr[col]], textposition="outside", cliponaxis=False,
                            hovertemplate="%{y} · " + tx(lbl, L) + ": %{x:.1f}%<extra></extra>"))
    f4.add_vline(x=0, line=dict(color=cs.INK2, width=1))
    f4.update_xaxes(ticksuffix="%", showgrid=True, gridcolor=cs.GRID, range=[min(0, float(sr[["margen", "roe"]].min().min()) * 1.3), float(sr[["margen", "roe"]].max().max()) * 1.25])
    f4.update_yaxes(ticksuffix="", tickfont=dict(size=12, color=cs.INK2))
    f4.update_layout(barmode="group", hovermode="closest", bargap=0.25)
    cs.ejes(f4, x="Porcentaje" if L == "es" else "Percent")
    g4 = cs.bloque_grafico(tx("g_secr", L).format(a=a1), cs.fig_html(f4, {"notime": True, "noy": True}, "g-em-sectores-rentabilidad"), tx("h_secr", L))
    th = TX["th_sec"][k]
    filas = "".join(f"<tr><td>{secn(s)}</td><td class='n'>{num(float(r_['empresas']), 0, L)}</td><td class='n'>{bil(r_['ingresos'], 1)}</td>"
                    f"<td class='n'>{pct(r_['part'])}</td><td class='n'>{pct(r_['cambio'], 1, True)}</td><td class='n'>{pct(r_['margen'])}</td>"
                    f"<td class='n'>{pct(r_['roe'])}</td><td class='n'>{pct(r_['endeudamiento'])}</td></tr>" for s, r_ in s1.iterrows())
    tabla = (f'<div class="table-wrap"><table class="tbl"><caption>{tx("tab_sec", L)} ({a1})</caption><thead><tr>'
             f'{"".join(f"<th>{h}</th>" for h in th)}</tr></thead><tbody>{filas}</tbody></table></div>')
    sc_ = s1["cambio"]
    r2 = tx("r_sectores", L).format(s1=secn(s1.index[0]), p1=pct(s1["part"].iloc[0]), s2=secn(s1.index[1]).lower() if L == "es" else secn(s1.index[1]),
                                    p2=pct(s1["part"].iloc[1]), s3=secn(s1.index[2]).lower() if L == "es" else secn(s1.index[2]), p3=pct(s1["part"].iloc[2]),
                                    sm=secn(smax).lower() if L == "es" else secn(smax), vm=pct(s1.loc[smax, "margen"]),
                                    sn=secn(s1["margen"].idxmin()).lower() if L == "es" else secn(s1["margen"].idxmin()), vn=pct(s1["margen"].min()),
                                    sc=secn(sc_.idxmax()), vc=pct(sc_.max(), 1, True), b=a0,
                                    sd=secn(sc_.idxmin()).lower() if L == "es" else secn(sc_.idxmin()), vd=pct(sc_.min(), 1, True))
    s_se = seccion("em-sectores", tx("s_sectores", L), r2, f'<div class="grid">{g3}{g4}</div>{tabla}')

    # ------------------------------------------------ regiones
    f5 = cs.base(L, height=380, fecha_x=False)
    for col, lbl, color in (("pi", "lbl_pi", cs.C1), ("pn", "lbl_pn", cs.C4)):
        f5.add_trace(go.Bar(y=[regn(r) for r in reg.index], x=reg[col].round(1).tolist(), orientation="h", name=tx(lbl, L),
                            marker=dict(color=color, line=dict(width=0)), text=[pct(v) for v in reg[col]], textposition="outside", cliponaxis=False,
                            hovertemplate="%{y} · " + tx(lbl, L) + ": %{x:.1f}%<extra></extra>"))
    f5.update_xaxes(ticksuffix="%", range=[0, float(reg[["pi", "pn"]].max().max()) * 1.2], showgrid=True, gridcolor=cs.GRID)
    f5.update_yaxes(ticksuffix="", tickfont=dict(size=12, color=cs.INK2))
    f5.update_layout(barmode="group", hovermode="closest", bargap=0.25)
    cs.ejes(f5, x="Porcentaje del total" if L == "es" else "Percent of total")
    g5 = cs.bloque_grafico(tx("g_reg", L).format(a=a1), cs.fig_html(f5, {"notime": True, "noy": True}, "g-em-regiones"), tx("h_reg", L), ancho=True)
    ant = reg.loc["ANTIOQUIA", "pi"] if "ANTIOQUIA" in reg.index else np.nan
    r3 = tx("r_regiones", L).format(pb=pct(bog["pi"]), nb=pct(bog["pn"], 0), pa=pct(ant), po=pct(100 - bog["pi"] - ant))
    s_re = seccion("em-regiones", tx("s_regiones", L), r3, f'<div class="grid">{g5}</div>')

    # ------------------------------------------------ concentracion
    f6 = cs.base(L, height=360, fecha_x=False)
    for a_, col, w_ in ((int(tot.index[0]), cs.C4, 1.8), (a1, cs.C1, 2.8)):
        f6.add_trace(go.Scatter(x=list(conc.index), y=conc[a_].round(1).tolist(), mode="lines+markers", name=str(a_), line=dict(color=col, width=w_),
                                marker=dict(size=7, color=col), hovertemplate="Top %{x}: %{y:.1f}%<extra>" + str(a_) + "</extra>"))
    f6.update_xaxes(type="log", tickvals=list(conc.index), ticktext=[num(float(v), 0, L) for v in conc.index], showgrid=True, gridcolor=cs.GRID)
    f6.update_yaxes(range=[0, 102])
    f6.update_layout(hovermode="closest")
    cs.ejes(f6, y="% de los ingresos" if L == "es" else "% of revenue", x="Número de empresas más grandes (N)" if L == "es" else "Number of largest companies (N)")
    g6 = cs.bloque_grafico(tx("g_conc", L), cs.fig_html(f6, {"notime": True, "noy": True}, "g-em-concentracion"), tx("h_conc", L))
    tp_ = E["top"][E["top"]["ano"] == a1].sort_values("puesto").head(15)
    tht = TX["th_top"][k]
    filas_t = "".join(f"<tr><td class='n'>{int(r_.puesto)}</td><td>{esc(nombre_emp(r_.empresa))}</td><td>{secn(r_.macrosector)}</td>"
                      f"<td class='n'>{bil(r_.ingresos, 2)}</td><td class='n'>{num(float(r_.ganancia), 2, L)}</td>"
                      f"<td class='n'>{pct(r_.ganancia / r_.ingresos * 100) if r_.ingresos else '—'}</td></tr>" for r_ in tp_.itertuples())
    tabla_t = (f'<div class="table-wrap"><table class="tbl"><caption>{tx("tab_top", L).format(a=a1)}</caption><thead><tr>'
               f'{"".join(f"<th>{h}</th>" for h in tht)}</tr></thead><tbody>{filas_t}</tbody></table></div>')
    e1 = tp_.iloc[0]
    r4 = tx("r_conc", L).format(t10=pct(conc.loc[10, a1]), t100=pct(top100), t1000=pct(conc.loc[1000, a1]), e1=nombre_emp(e1["empresa"]),
                                v1=bil(e1["ingresos"], 1), p1=pct(e1["ingresos"] / u["ingresos"] * 100))
    s_co = seccion("em-concentracion", tx("s_conc", L), r4, f'<div class="grid">{g6}</div>{tabla_t}')

    # ------------------------------------------------ acciones
    f7 = cs.base(L, height=max(360, 24 * len(ret) + 60), fecha_x=False)
    f7.add_trace(go.Bar(y=[corto(e_) for e_, _, _ in ret], x=[round(v, 1) for _, _, v in ret], orientation="h", showlegend=False,
                        marker=dict(color=[cs.C3 if v > 0 else cs.C2 for _, _, v in ret], line=dict(width=0)),
                        text=[pct(v, 1, True) for _, _, v in ret], textposition="outside", cliponaxis=False,
                        customdata=[s_ for _, s_, _ in ret], hovertemplate="%{y} (%{customdata}): %{x:+.1f}%<extra></extra>"))
    f7.add_vline(x=0, line=dict(color=cs.INK2, width=1))
    lo_, hi_ = min(0, ret[0][2]), max(0, ret[-1][2])
    f7.update_xaxes(ticksuffix="%", range=[lo_ * 2.2 - 12, hi_ * 1.3 + 5], showgrid=True, gridcolor=cs.GRID)
    f7.update_yaxes(ticksuffix="", tickfont=dict(size=11, color=cs.INK2))
    f7.update_layout(hovermode="closest", bargap=0.25)
    cs.ejes(f7, x="Cambio del precio en 12 meses" if L == "es" else "12-month price change")
    g7 = cs.bloque_grafico(tx("g_acc", L), cs.fig_html(f7, {"notime": True, "noy": True}, "g-em-acciones"), tx("h_acc", L))
    ps = can.groupby("sector")["peso"].sum().sort_values()
    f8 = cs.base(L, height=330, fecha_x=False)
    f8.add_trace(go.Bar(y=list(ps.index), x=ps.round(1).tolist(), orientation="h", showlegend=False, marker=dict(color=cs.C7, line=dict(width=0)),
                        text=[pct(v) for v in ps], textposition="outside", cliponaxis=False, hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
    f8.update_xaxes(ticksuffix="%", range=[0, float(ps.max()) * 1.25], showgrid=True, gridcolor=cs.GRID)
    f8.update_yaxes(ticksuffix="", tickfont=dict(size=12, color=cs.INK2))
    f8.update_layout(hovermode="closest", bargap=0.3)
    cs.ejes(f8, x="% del índice" if L == "es" else "% of the index")
    g8 = cs.bloque_grafico(tx("g_secc", L), cs.fig_html(f8, {"notime": True, "noy": True}, "g-em-colcap-sectores"), tx("h_secc", L))
    pf = float(ps.get("Servicios Financieros", 0))
    r5 = tx("r_acciones", L).format(s=sube, t=len(ret), mx=corto(ret[-1][0]), vmx=pct(ret[-1][2], 1, True), mn=corto(ret[0][0]),
                                    vmn=pct(ret[0][2], 1, True), pf=pct(pf))
    s_ac = seccion("em-acciones", tx("s_acciones", L), r5, f'<div class="grid">{g7}{g8}</div>')

    # ------------------------------------------------ financiacion
    w = pd.DataFrame({"kc": kc, "kt": kt, "tp": tp.resample("MS").mean(), "to": to.resample("MS").mean()}).loc["2008":]
    xw = w.index + pd.offsets.MonthEnd(0)
    f9 = cs.base(L, height=360)
    cs.linea(f9, xw, w["kc"], tx("lbl_kc", L), cs.C1, width=2.6, lang=L)
    cs.linea(f9, xw, w["kt"], tx("lbl_kt", L), cs.C7, width=1.6, lang=L)
    for col, lbl, color in (("tp", "lbl_tp", cs.C2), ("to", "lbl_to", cs.C4)):
        f9.add_trace(go.Scatter(x=list(xw), y=w[col].round(2).tolist(), yaxis="y2", mode="lines", name=tx(lbl, L),
                                line=dict(color=color, width=1.6, dash="dot"), hovertemplate=tx(lbl, L) + ": %{y:.2f}%<extra></extra>"))
    f9.update_layout(yaxis2=dict(overlaying="y", side="right", showgrid=False, zeroline=False, fixedrange=True, ticksuffix="%",
                                 tickfont=dict(size=11.5, color=cs.MUTED)))
    f9.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    cs.ejes(f9, y="Crecimiento real anual" if L == "es" else "Annual real growth", y2="Tasa efectiva anual" if L == "es" else "Effective annual rate")
    g9 = cs.bloque_grafico(tx("g_cart", L), cs.fig_html(f9, {"noy": True}, "g-em-credito"), tx("h_cart", L))
    pos = pd.DataFrame({"snf": B.get("posicion_sociedades_no_financieras"), "sf": B.get("posicion_sociedades_financieras"),
                        "gob": B.get("posicion_gobierno"), "hog": B.get("posicion_hogares")}).dropna(how="all")
    xp = pos.index + pd.offsets.MonthEnd(0)
    f10 = cs.base(L, height=360)
    for col, lbl, color, w_ in (("snf", "lbl_snf", cs.C1, 2.8), ("hog", "lbl_hog", cs.C3, 1.8), ("gob", "lbl_gob", cs.C2, 1.8), ("sf", "lbl_sf", cs.C7, 1.6)):
        cs.linea(f10, xp, pos[col], tx(lbl, L), color, width=w_, lang=L)
    f10.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    cs.ejes(f10, y="% del PIB" if L == "es" else "% of GDP")
    g10 = cs.bloque_grafico(tx("g_pos", L), cs.fig_html(f10, {}, "g-em-posicion"), tx("h_pos", L))
    de = B.get("deuda_externa_privada_musd").dropna()
    r6 = tx("r_fin", L).format(k=pct(kc.iloc[-1], 1, True), kt=pct(kt.iloc[-1], 1, True), tp=pct(tp.iloc[-1], 2), to=pct(to.iloc[-1], 2),
                               sn=pct(abs(pos["snf"].dropna().iloc[-1])), de=num(float(de.iloc[-1]), 0, L), fde=fecha(de.index[-1], "m", L))
    s_fi = seccion("em-financiacion", tx("s_fin", L), r6, f'<div class="grid">{g9}{g10}</div>')

    # ------------------------------------------------ registro mercantil
    s_rg = ""
    if regm is not None:
        pv = regm.assign(cat=np.where(regm["categoria"].str.startswith("SOCIEDAD"), "s", "n")).pivot_table(
            index="mes", columns="cat", values=["matriculas", "cancelaciones"], aggfunc="sum").fillna(0).sort_index()
        r12 = pv.rolling(12).sum().dropna().loc["2012":] / 1000
        xr = r12.index + pd.offsets.MonthEnd(0)
        f11 = cs.base(L, height=380, suffix="")
        for (met, cat), lbl, color, dash, w_ in ((("matriculas", "s"), "lbl_sm", cs.C1, None, 2.6), (("cancelaciones", "s"), "lbl_sc", cs.C1, "dot", 2.0),
                                                 (("matriculas", "n"), "lbl_nm", cs.C4, None, 2.0), (("cancelaciones", "n"), "lbl_nc", cs.C4, "dot", 1.6)):
            cs.linea(f11, xr, r12[(met, cat)], tx(lbl, L), color, width=w_, dash=dash, fmt=".1f", suf=" mil" if L == "es" else "k", lang=L)
        cs.ejes(f11, y="Miles (suma de 12 meses)" if L == "es" else "Thousands (12-month sum)")
        g11 = cs.bloque_grafico(tx("g_reg_m", L), cs.fig_html(f11, {}, "g-em-registro"), tx("h_reg_m", L), ancho=True)
        u12 = pv.tail(12).sum()
        r7 = tx("r_registro", L).format(sm=num(float(u12[("matriculas", "s")]), 0, L), nm=num(float(u12[("matriculas", "n")]), 0, L),
                                        sc=num(float(u12[("cancelaciones", "s")]), 0, L), nc=num(float(u12[("cancelaciones", "n")]), 0, L),
                                        cs=pct(ult_reg[2], 1, True))
        s_rg = seccion("em-registro", tx("s_registro", L), r7, f'<div class="grid">{g11}</div>')

    items = "".join(f'<li><span class="ref">{ref}</span><span class="ref-u">{es if L == "es" else en}</span></li>' for ref, es, en in LITERATURA)
    s_lit = (f'<section id="em-literatura" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{tx("s_lit", L)}</h2></div>'
             f'<ol class="refs">{items}</ol></section>')
    return antes, s_gr + s_se + s_re + s_co, s_ac + s_fi + s_rg + s_lit


# ====================================================================== ventana explicativa
def ventana_empresas(u, a1, L, num) -> str:
    es = L == "es"
    T = (lambda a, b: a if es else b)
    b_ = lambda v: num(float(v), 1, L)
    return f"""<dialog class="explica" id="exp-empresas" aria-labelledby="exp-empresas-t">
<div class="ex-cab"><p class="ex-k">{T("Para entender", "To understand")} · Supersociedades · Confecámaras · Banco de la República</p><h2 id="exp-empresas-t">{T("¿De dónde salen las cifras de las empresas?", "Where do the company figures come from?")}</h2>
<button type="button" class="ex-x" data-cerrar aria-label="{T("Cerrar", "Close")}">✕</button></div>
<div class="ex-cuerpo">
<p class="ex-lede">{T(f"La Superintendencia de Sociedades publica cada año la lista de las 10.000 empresas con más ingresos operacionales del país, con los estados financieros que reportan a sus supervisores, con corte al 31 de diciembre. Para {a1}: ingresos de ${b_(u['ingresos'])} billones, activos de ${b_(u['activos'])} billones, pasivos de ${b_(u['pasivos'])} billones y patrimonio de ${b_(u['patrimonio'])} billones.",
 f"The Superintendence of Companies publishes every year the list of the 10,000 companies with the most operating revenue in the country, using the financial statements they report to their supervisors, as of 31 December. For {a1}: revenue of COP {b_(u['ingresos'])} trillion, assets of {b_(u['activos'])} trillion, liabilities of {b_(u['pasivos'])} trillion and equity of {b_(u['patrimonio'])} trillion.")}</p>
<h3>{T("1. Qué empresas entran", "1. Which companies are included")}</h3>
<ul class="ex-lista">
<li>{T("Empresas vigiladas por las superintendencias de Sociedades, Financiera (emisores del sector real), Salud, Transporte, Vigilancia y Seguridad Privada y Servicios Públicos, ordenadas por ingresos operacionales.", "Companies supervised by the superintendences of Companies, Finance (real-sector issuers), Health, Transport, Private Security and Public Utilities, ranked by operating revenue.")}</li>
<li>{T("No incluye bancos ni aseguradoras, ni empresas que no reportan estados financieros a una superintendencia.", "It excludes banks and insurers, and companies that do not report financial statements to a superintendence.")}</li>
<li>{T("La lista cambia cada año: las cifras de un año y otro no son de las mismas empresas.", "The list changes every year: figures for different years are not for the same companies.")}</li>
<li>{T("Los datos abiertos vienen en billones de pesos con dos decimales; por eso las sumas de esta página pueden diferir levemente del informe oficial.", "The open data come in COP trillion with two decimals, so totals on this page may differ slightly from the official report.")}</li>
</ul>
<h3>{T("2. Cómo leer los indicadores", "2. How to read the indicators")}</h3>
<ul class="ex-lista">
<li><b>{T("Margen neto", "Net margin")}</b>: {T("utilidad ÷ ingresos. Cuántos pesos quedan de ganancia por cada $100 vendidos.", "profit ÷ revenue. How many pesos of profit remain per $100 sold.")}</li>
<li><b>{T("Rentabilidad del patrimonio", "Return on equity")}</b>: {T("utilidad ÷ patrimonio. Lo que gana cada peso que pusieron los dueños.", "profit ÷ equity. What each peso put in by the owners earns.")}</li>
<li><b>{T("Endeudamiento", "Leverage")}</b>: {T("pasivos ÷ activos. Qué parte de lo que tienen las empresas está financiada con deudas.", "liabilities ÷ assets. Which part of what companies own is financed with debt.")}</li>
<li><b>{T("Concentración", "Concentration")}</b>: {T("qué parte de los ingresos generan las N empresas más grandes.", "which part of revenue the N largest companies generate.")}</li>
</ul>
<h3>{T("3. Las otras fuentes de la página", "3. The page's other sources")}</h3>
<ul class="ex-lista">
<li>{T("Registro mercantil (RUES): matrículas y cancelaciones que administran las cámaras de comercio; aquí solo se usan conteos por fecha.", "Business register (RUES): registrations and cancellations managed by the chambers of commerce; only counts by date are used here.")}</li>
<li>{T("Banco de la República: cartera comercial, tasas de crédito, cuentas financieras por sector institucional, deuda externa privada e inversión extranjera directa.", "Banco de la República: commercial loans, lending rates, financial accounts by institutional sector, private external debt and foreign direct investment.")}</li>
<li>{T("Bolsa: COLCAP del Banco de la República y precios de cierre de las acciones de su canasta.", "Stock market: COLCAP from Banco de la República and closing prices of the shares in its basket.")}</li>
</ul>
<h3>{T("Fuentes oficiales", "Official sources")}</h3>
<ul class="ex-fuentes">
<li><a href="https://www.datos.gov.co/Comercio-Industria-y-Turismo/10-000-Empresas-mas-Grandes-del-Pa-s/6cat-2gcs" target="_blank" rel="noopener">Supersociedades — {T("10.000 empresas más grandes del país (datos abiertos)", "10,000 largest companies (open data)")}</a></li>
<li><a href="https://www.supersociedades.gov.co/noticias-supersociedades/-/asset_publisher/atwl/content/las-10.000-empresas-m%C3%A1s-grandes-de-colombia-registraron-ingresos-por-1.852-9-billones-y-utilidades-por-138-1-billones-al-cierre-de-2025" target="_blank" rel="noopener">Supersociedades — {T("informe de resultados 2025", "2025 results report")}</a></li>
<li><a href="https://www.datos.gov.co/Comercio-Industria-y-Turismo/Personas-Naturales-Personas-Jur-dicas-y-Entidades-/c82u-588k" target="_blank" rel="noopener">Confecámaras — {T("registro mercantil (RUES)", "business register (RUES)")}</a></li>
<li><a href="https://suameca.banrep.gov.co/graficador-series/" target="_blank" rel="noopener">{T("Banco de la República — series estadísticas", "Banco de la República — statistical series")}</a></li>
</ul>
</div></dialog>"""
