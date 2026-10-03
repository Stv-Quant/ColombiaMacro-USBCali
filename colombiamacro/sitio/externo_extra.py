"""Pagina de cuentas externas y fiscales (v12.16): doce medidas, de donde viene el deficit externo, como se
financia, inversion extranjera por sector y remesas, deuda externa y posicion de inversion internacional,
reservas, las cuentas del Gobierno (ingresos, gastos, intereses y balance), financiamiento y deuda publica,
ventana explicativa y literatura.

Solo datos observados del Banco de la Republica (balanza de pagos MBP6, deuda externa, PII, reservas, balance
fiscal de caja del GNC y del SPNF, empalme DNP-MinHacienda) y del DANE (PIB nominal para las razones al PIB).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

TX = {
    "s_medidas": ("Las cuentas externas y fiscales en doce medidas", "External and fiscal accounts in twelve measures"),
    "s_cc": ("¿De dónde viene el déficit externo?", "Where does the external deficit come from?"),
    "s_fin": ("¿Cómo se financia?", "How is it financed?"),
    "s_entran": ("Los dólares que llegan: inversión extranjera y remesas", "Dollars coming in: foreign investment and remittances"),
    "s_deuda": ("¿Cuánto le debe Colombia al exterior?", "How much does Colombia owe abroad?"),
    "s_gob": ("Las cuentas del Gobierno", "Government accounts"),
    "s_gfin": ("¿Cómo se financia el Gobierno y cuánto le cuesta?", "How does the Government finance itself and at what cost?"),
    "s_lit": ("Bases metodológicas y literatura", "Methodological basis and literature"),
    # lecturas
    "l_cc": ("Cuenta corriente · 4 trimestres a {f}", "Current account · 4 quarters to {f}"), "l_cc_d": ("del PIB · US${v} millones · solo el último trimestre: {q}", "of GDP · US${v} million · latest quarter alone: {q}"),
    "l_bie": ("Balanza de bienes", "Goods balance"), "l_bie_d": ("del PIB · exportaciones {x} en un año", "of GDP · exports {x} over a year"),
    "l_rem": ("Remesas · 12 meses a {f}", "Remittances · 12 months to {f}"), "l_rem_d": ("US$ millones · {p} del PIB · {c} en un año", "US$ million · {p} of GDP · {c} over a year"),
    "l_ied": ("Inversión extranjera directa", "Foreign direct investment"), "l_ied_d": ("del PIB · cubre {c} del déficit corriente", "of GDP · covers {c} of the current-account deficit"),
    "l_dext": ("Deuda externa · {f}", "External debt · {f}"), "l_dext_d": ("del PIB · pública {pu} y privada {pr}", "of GDP · public {pu} and private {pr}"),
    "l_res": ("Reservas internacionales", "International reserves"), "l_res_d": ("meses de importaciones de bienes · US${v} millones", "months of goods imports · US${v} million"),
    "l_pii": ("Posición de inversión internacional", "International investment position"), "l_pii_d": ("del PIB (neta) · lo que el país debe menos lo que tiene afuera", "of GDP (net) · what the country owes minus what it holds abroad"),
    "l_bal": ("Balance del Gobierno · 12 meses a {f}", "Government balance · 12 months to {f}"), "l_bal_d": ("del PIB, caja · año anterior {a}", "of GDP, cash basis · previous year {a}"),
    "l_dgnc": ("Deuda bruta del Gobierno · {a}", "Government gross debt · {a}"), "l_dgnc_d": ("del PIB · en {b}: {v}", "of GDP · in {b}: {v}"),
    "l_int": ("Intereses de la deuda", "Interest on debt"), "l_int_d": ("de cada $100 de ingresos del Gobierno · {p} del PIB", "of every $100 of government revenue · {p} of GDP"),
    "l_gas": ("Gasto del Gobierno", "Government spending"), "l_gas_d": ("del PIB · ingresos {i} del PIB", "of GDP · revenue {i} of GDP"),
    "l_fext": ("Financiamiento del Gobierno · 12 meses", "Government financing · 12 months"), "l_fext_d": ("del PIB · interno {i} y externo neto {e}", "of GDP · domestic {i} and net external {e}"),
    # respuestas
    "r_medidas": ("Colombia gasta en el exterior más de lo que recibe: el déficit de cuenta corriente es {cc} del PIB, y la inversión extranjera directa cubre {cub} de él. "
                  "Las remesas suman US${rem} millones al año. "
                  "El Gobierno gasta {gas} del PIB y recibe {ing}: su déficit de caja es {bal} del PIB y su deuda llega a {deu} del PIB.",
                  "Colombia spends abroad more than it receives: the current-account deficit is {cc} of GDP, and foreign direct investment covers {cub} of it. "
                  "Remittances total US${rem} million a year. "
                  "The Government spends {gas} of GDP and takes in {ing}: its cash deficit is {bal} of GDP and its debt reaches {deu} of GDP."),
    "r_cc": ("En los últimos cuatro trimestres el déficit de bienes fue US${b} millones y el de servicios US${s} millones. Las utilidades, intereses y dividendos que salen del país (ingreso primario) restaron US${p} millones, "
             "mientras las remesas y otras transferencias (ingreso secundario) sumaron US${t} millones. Resultado: un déficit corriente de US${cc} millones.",
             "Over the last four quarters the goods deficit was US${b} million and the services deficit US${s} million. Profits, interest and dividends leaving the country (primary income) subtracted US${p} million, "
             "while remittances and other transfers (secondary income) added US${t} million. Result: a current-account deficit of US${cc} million."),
    "r_fin": ("El déficit se cubre con capital que llega: en cuatro trimestres entraron en términos netos US${d} millones por inversión directa, US${c} millones por inversión de cartera y US${o} millones por otra inversión (préstamos y depósitos). "
              "Las reservas del Banco de la República cambiaron US${r} millones.",
              "The deficit is covered by incoming capital: over four quarters net inflows were US${d} million of direct investment, US${c} million of portfolio investment and US${o} million of other investment (loans and deposits). "
              "Banco de la República reserves changed US${r} million."),
    "r_entran": ("La inversión extranjera directa sumó US${ied} millones en cuatro trimestres; {s1} recibió la mayor parte ({p1}), seguido de {s2} ({p2}). "
                 "Las remesas de los trabajadores en el exterior sumaron US${rem} millones en 12 meses, {cr} frente al año anterior.",
                 "Foreign direct investment totalled US${ied} million over four quarters; {s1} received the largest share ({p1}), followed by {s2} ({p2}). "
                 "Workers' remittances totalled US${rem} million over 12 months, {cr} vs the previous year."),
    "r_deuda": ("La deuda externa suma US${t} millones ({p} del PIB): US${pu} millones del sector público y US${pr} millones del privado. "
                "Contando todos los activos y pasivos con el exterior (no solo deuda), Colombia debe en términos netos US${pii} millones ({ppii} del PIB).",
                "External debt totals US${t} million ({p} of GDP): US${pu} million public and US${pr} million private. "
                "Counting all assets and liabilities with the rest of the world (not only debt), Colombia owes in net terms US${pii} million ({ppii} of GDP)."),
    "r_gob": ("En los últimos 12 meses el Gobierno nacional recibió {i} del PIB y gastó {g}, de los cuales {int} fueron intereses. El balance de caja fue {b} del PIB; sin intereses (balance primario) {bp}. "
              "Su deuda bruta cerró {a} en {d} del PIB.",
              "Over the last 12 months the national Government took in {i} of GDP and spent {g}, of which {int} was interest. The cash balance was {b} of GDP; excluding interest (primary balance) {bp}. "
              "Its gross debt ended {a} at {d} of GDP."),
    "r_gfin": ("De cada $100 que recibe el Gobierno, ${pi} se van a pagar intereses (en caja). En 12 meses se financió con {fi} del PIB de fuentes internas y {fe} de fuentes externas netas (negativo = pagó más de lo que recibió en préstamos externos). "
               "{nota}",
               "Of every $100 the Government receives, ${pi} goes to interest (cash basis). Over 12 months it financed itself with {fi} of GDP from domestic sources and {fe} from net external ones (negative = it repaid more than it borrowed abroad). "
               "{nota}"),
    "nota_int": ("La serie de intereses en caja tiene {n} meses con valores negativos en los últimos dos años; por eso este indicador puede ser menor que el costo de la deuda en causación que reporta el Ministerio de Hacienda.",
                 "The cash interest series has {n} months with negative values over the last two years, so this indicator may be lower than the accrual-basis debt cost reported by the Ministry of Finance."),
    # graficos
    "g_cc": ("Cuenta corriente por componentes (4 trimestres)", "Current account by component (4 quarters)"),
    "h_cc": ("Miles de millones de dólares, suma de 4 trimestres. Barras: aporte de cada componente; línea: cuenta corriente total.",
             "Billions of dollars, 4-quarter sum. Bars: each component's contribution; line: total current account."),
    "lbl_bie": ("Bienes", "Goods"), "lbl_ser": ("Servicios", "Services"), "lbl_ip": ("Ingreso primario (utilidades, intereses)", "Primary income (profits, interest)"),
    "lbl_is": ("Ingreso secundario (remesas)", "Secondary income (remittances)"), "lbl_cc": ("Cuenta corriente", "Current account"),
    "g_xm": ("Exportaciones e importaciones de bienes (4 trimestres)", "Goods exports and imports (4 quarters)"),
    "h_xm": ("Miles de millones de dólares, balanza de pagos. La distancia entre las líneas es el déficit de bienes.", "Billions of dollars, balance of payments. The gap between the lines is the goods deficit."),
    "lbl_x": ("Exportaciones", "Exports"), "lbl_m": ("Importaciones", "Imports"),
    "g_fin": ("Entradas netas de capital por tipo (4 trimestres)", "Net capital inflows by type (4 quarters)"),
    "h_fin": ("Miles de millones de dólares. Positivo = entra financiación neta. La línea punteada es el déficit corriente que hay que financiar.",
              "Billions of dollars. Positive = net financing comes in. The dotted line is the current-account deficit to be financed."),
    "lbl_fd": ("Inversión directa", "Direct investment"), "lbl_fc": ("Inversión de cartera", "Portfolio investment"), "lbl_fo": ("Otra inversión", "Other investment"),
    "lbl_fr": ("Reservas (− = acumulación)", "Reserves (− = accumulation)"), "lbl_fx": ("Derivados", "Derivatives"), "lbl_def": ("Déficit corriente", "Current-account deficit"),
    "g_ieds": ("Inversión extranjera directa por sector (4 trimestres)", "Foreign direct investment by sector (4 quarters)"),
    "h_ieds": ("Millones de dólares de los últimos cuatro trimestres frente a los cuatro anteriores.", "Millions of dollars over the last four quarters vs the previous four."),
    "lbl_ult": ("Últimos 4 trimestres", "Last 4 quarters"), "lbl_ant": ("4 trimestres anteriores", "Previous 4 quarters"),
    "g_rem": ("Remesas de los trabajadores", "Workers' remittances"),
    "h_rem": ("Suma de 12 meses en miles de millones de dólares (eje izquierdo) y como porcentaje del PIB (eje derecho).", "12-month sum in billions of dollars (left axis) and as a percentage of GDP (right axis)."),
    "lbl_rem": ("Remesas (12 meses)", "Remittances (12 months)"), "lbl_remp": ("% del PIB", "% of GDP"),
    "g_dext": ("Deuda externa pública y privada", "Public and private external debt"),
    "h_dext": ("Saldo en miles de millones de dólares (áreas) y total como % del PIB (línea, eje derecho).", "Balance in billions of dollars (areas) and total as % of GDP (line, right axis)."),
    "lbl_pu": ("Pública", "Public"), "lbl_pr": ("Privada", "Private"), "lbl_dp": ("Total, % del PIB", "Total, % of GDP"),
    "g_pii": ("Posición de inversión internacional", "International investment position"),
    "h_pii": ("Activos y pasivos financieros con el exterior (miles de millones de dólares) y posición neta como % del PIB (eje derecho). Las reservas en meses de importaciones están en la tarjeta de medidas.",
              "Financial assets and liabilities with the rest of the world (billions of dollars) and net position as % of GDP (right axis). Reserves in months of imports are in the measures card."),
    "lbl_act": ("Activos", "Assets"), "lbl_pas": ("Pasivos", "Liabilities"), "lbl_net": ("Neta, % del PIB", "Net, % of GDP"),
    "g_gob": ("Ingresos, gastos e intereses del Gobierno (% del PIB)", "Government revenue, spending and interest (% of GDP)"),
    "h_gob": ("Gobierno nacional central, metodología de caja, suma de 12 meses (por trimestres completos) sobre el PIB nominal de los mismos cuatro trimestres.",
              "Central government, cash basis, 12-month sum (complete quarters) over nominal GDP for the same four quarters."),
    "lbl_ing": ("Ingresos", "Revenue"), "lbl_gas": ("Gastos", "Spending"), "lbl_int": ("Intereses", "Interest"),
    "g_bal": ("Balance total y primario del Gobierno (% del PIB)", "Government total and primary balance (% of GDP)"),
    "h_bal": ("Balance = ingresos − gastos; primario = sin intereses. Negativo = déficit.", "Balance = revenue − spending; primary = excluding interest. Negative = deficit."),
    "lbl_bal": ("Balance total", "Total balance"), "lbl_bp": ("Balance primario", "Primary balance"),
    "g_dgnc": ("Deuda bruta del Gobierno nacional central (% del PIB)", "Central government gross debt (% of GDP)"),
    "h_dgnc": ("Saldo al cierre de cada año.", "End-of-year balance."),
    "g_gfin": ("Financiamiento del Gobierno e intereses", "Government financing and interest"),
    "h_gfin": ("Barras: financiamiento interno y externo (suma de 12 meses, % del PIB). Línea: intereses por cada $100 de ingresos (eje derecho).",
               "Bars: domestic and external financing (12-month sum, % of GDP). Line: interest per $100 of revenue (right axis)."),
    "lbl_fi": ("Financiamiento interno", "Domestic financing"), "lbl_fe": ("Financiamiento externo", "External financing"), "lbl_ii": ("Intereses / ingresos", "Interest / revenue"),
    "ied_sec": {"petroleo": ("Petróleo", "Oil"), "mineria": ("Minería", "Mining"), "industria": ("Industria", "Manufacturing"),
                "financiero": ("Servicios financieros y empresariales", "Financial and business services"), "comercio": ("Comercio, restaurantes y hoteles", "Trade, restaurants and hotels"),
                "transporte": ("Transporte y comunicaciones", "Transport and communications"), "electricidad": ("Electricidad, gas y agua", "Electricity, gas and water"),
                "construccion": ("Construcción", "Construction"), "servicios": ("Servicios comunales y personales", "Community and personal services"), "agro": ("Agro", "Agriculture")},
}
LITERATURA = [
    ("Obstfeld, M. y Rogoff, K. (1995). The Intertemporal Approach to the Current Account. En <i>Handbook of International Economics</i>, vol. 3, 1731–1799.",
     "Por qué un país ahorra o se endeuda con el exterior.", "Why a country saves or borrows abroad."),
    ("Calvo, G. A., Leiderman, L. y Reinhart, C. M. (1993). Capital Inflows and Real Exchange Rate Appreciation in Latin America. <i>IMF Staff Papers</i>, 40(1), 108–151.",
     "El papel de los flujos de capital y los factores externos en América Latina.", "The role of capital flows and external factors in Latin America."),
    ("Lane, P. R. y Milesi-Ferretti, G. M. (2007). The External Wealth of Nations Mark II. <i>Journal of International Economics</i>, 73(2), 223–250.",
     "Cómo se mide y qué revela la posición de inversión internacional.", "How the international investment position is measured and what it reveals."),
    ("Reinhart, C. M. y Rogoff, K. S. (2009). <i>This Time Is Different: Eight Centuries of Financial Folly</i>. Princeton University Press.",
     "Deuda pública y externa en perspectiva histórica.", "Public and external debt in historical perspective."),
    ("Blanchard, O. (2019). Public Debt and Low Interest Rates. <i>American Economic Review</i>, 109(4), 1197–1229.",
     "Cuándo la deuda pública es sostenible: tasa de interés frente a crecimiento.", "When public debt is sustainable: interest rate versus growth."),
    ("FMI (2009). <i>Manual de Balanza de Pagos y Posición de Inversión Internacional</i>, sexta edición (MBP6).",
     "Metodología con la que el Banco de la República elabora la balanza de pagos.", "Methodology Banco de la República uses for the balance of payments."),
    ("Ley 1473 de 2011 y Ley 2155 de 2021: regla fiscal de Colombia y Comité Autónomo de la Regla Fiscal.",
     "Marco legal que limita el déficit y la deuda del Gobierno nacional central.", "Legal framework limiting central government deficit and debt."),
]


def tx(k, L):
    return TX[k][0 if L == "es" else 1]


def suma4(s: pd.Series) -> pd.Series:
    """Suma movil de cuatro trimestres."""
    return s.sort_index().rolling(4).sum()


def trimestral(s: pd.Series) -> pd.Series:
    """Suma por trimestre de una serie mensual; solo trimestres completos (tres meses)."""
    s = s.dropna().sort_index()
    q = s.groupby(s.index.to_period("Q"))
    out = q.sum()[q.size() == 3]
    out.index = out.index.to_timestamp()
    return out


def construir_externo(d, L):
    """Devuelve (antes, despues)."""
    from colombiamacro.fuentes import externo_fiscal as xf
    from colombiamacro.sitio import construir as cs
    num, fecha = cs.num, cs.fecha
    cs.LANG_ACTUAL[0] = L
    k = 0 if L == "es" else 1
    X = xf.cargar()
    if X is None:
        return "", ""
    pct = lambda v, dec=1, sg=False: num(float(v), dec, L, sg, "%")
    usd = lambda v: num(float(v), 0, L)
    mm = " mil M" if L == "es" else " bn"
    # PIB nominal: billones de pesos por trimestre; en dolares con la TRM promedio del trimestre
    pib = pd.read_csv(cs.DATA_DIR / "pib_colombia.csv", parse_dates=["fecha"]).set_index("fecha")["pib_nominal_billones_cop"].dropna().sort_index()
    trm = d.extra["trm"].set_index("fecha")["trm"].sort_index()
    trm_q = trm.groupby(trm.index.to_period("Q")).mean()
    trm_q.index = trm_q.index.to_timestamp()
    pib_usd = (pib * 1e6 / trm_q.reindex(pib.index)).dropna()        # millones de dolares
    pib4, pibu4 = suma4(pib).dropna(), suma4(pib_usd).dropna()
    al_pib_usd = lambda s4: (s4 / pibu4.reindex(s4.index) * 100).dropna()
    s4 = {k_: suma4(X[k_]).dropna() for k_ in ("cc", "bienes", "servicios", "ingreso_primario", "ingreso_secundario", "cf_directa", "cf_cartera",
                                                 "cf_otra", "cf_reservas", "cf_derivados", "ied", "exportaciones_bienes", "importaciones_bienes")}
    fq = s4["cc"].index[-1]
    ccp = al_pib_usd(s4["cc"])
    rem12 = X["remesas"].rolling(12).sum().dropna()
    pibu_m = pibu4.copy()
    pibu_m.index = pibu_m.index + pd.offsets.QuarterEnd(0) - pd.offsets.MonthBegin(1)   # ultimo mes de cada trimestre
    rem_p = (rem12 / pibu_m.reindex(rem12.index, method="ffill") * 100).dropna()
    dext = X["deuda_externa"].dropna()
    res = d.extra["reservas_netas_musd"].set_index("fecha")["reservas_netas_musd"].sort_index()
    imp_mes = s4["importaciones_bienes"].iloc[-1] / 12
    pii = X["pii_neta"].dropna()
    piip = (pii / pibu4.reindex(pii.index) * 100).dropna()
    # Gobierno: trimestres completos, suma de 4 trimestres, % del PIB nominal
    gq = {k_: suma4(trimestral(X[f"gnc_{k_}"])).dropna() / 1000 for k_ in ("ingresos", "gastos", "intereses", "balance", "fin_interno", "fin_externo")}
    gp = {k_: (v / pib4.reindex(v.index) * 100).dropna() for k_, v in gq.items()}
    fg = gp["balance"].index[-1]
    bal_ant = float(gp["balance"].loc[:fg - pd.DateOffset(years=1)].iloc[-1])
    dg = X["deuda_gnc_pib"].dropna()
    ffq = lambda f: fecha(f, "q", L)

    def seccion(sid, titulo, resp, cuerpo):
        return (f'<section id="{sid}" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{titulo}</h2></div>'
                f'{cs.respuesta_html(resp, L)}{cuerpo}</section>')

    def lec(kk, v, dsc, tono, href):
        return (f'<a class="lec {tono}" href="{href}"><span class="lec-k">{kk}</span><b class="lec-v">{v}</b>'
                f'<span class="lec-d">{dsc}</span></a>')

    cub = float(s4["ied"].iloc[-1] / abs(s4["cc"].iloc[-1]) * 100) if s4["cc"].iloc[-1] < 0 else np.nan
    x_ch = float((s4["exportaciones_bienes"].iloc[-1] / s4["exportaciones_bienes"].iloc[-5] - 1) * 100)
    f_rem = rem12.index[-1]
    tiles = [
        lec(tx("l_cc", L).format(f=ffq(fq)), pct(ccp.iloc[-1], 1, True), tx("l_cc_d", L).format(v=usd(s4["cc"].iloc[-1]), q=pct(X["cc"].iloc[-1] / pib_usd.reindex([X["cc"].index[-1]]).iloc[0] * 100, 1, True)), "warn" if ccp.iloc[-1] < -4 else "", "#ext-cc"),
        lec(tx("l_bie", L), pct(al_pib_usd(s4["bienes"]).iloc[-1], 1, True), tx("l_bie_d", L).format(x=pct(x_ch, 1, True)), "", "#ext-cc"),
        lec(tx("l_rem", L).format(f=fecha(f_rem, "m", L)), "US$" + usd(rem12.iloc[-1]),
            tx("l_rem_d", L).format(p=pct(rem_p.iloc[-1]), c=pct((rem12.iloc[-1] / rem12.iloc[-13] - 1) * 100, 1, True)), "", "#ext-entran"),
        lec(tx("l_ied", L), pct(al_pib_usd(s4["ied"]).iloc[-1]), tx("l_ied_d", L).format(c=pct(cub, 0)), "", "#ext-entran"),
        lec(tx("l_dext", L).format(f=fecha(dext.index[-1], "m", L)), pct(X["deuda_externa_pib"].dropna().iloc[-1]),
            tx("l_dext_d", L).format(pu="US$" + num(float(X["deuda_externa_publica"].dropna().iloc[-1]) / 1000, 0, L) + mm,
                                     pr="US$" + num(float(X["deuda_externa_privada"].dropna().iloc[-1]) / 1000, 0, L) + mm), "", "#ext-deuda"),
        lec(tx("l_res", L), num(float(res.iloc[-1] / imp_mes), 1, L), tx("l_res_d", L).format(v=usd(res.iloc[-1])), "", "#ext-deuda"),
        lec(tx("l_pii", L), pct(piip.iloc[-1], 1, True), tx("l_pii_d", L), "", "#ext-deuda"),
        lec(tx("l_bal", L).format(f=ffq(fg)), pct(gp["balance"].iloc[-1], 1, True), tx("l_bal_d", L).format(a=pct(bal_ant, 1, True)),
            "warn" if gp["balance"].iloc[-1] < -3 else "", "#fi-gobierno"),
        lec(tx("l_dgnc", L).format(a=dg.index[-1].year), pct(dg.iloc[-1]), tx("l_dgnc_d", L).format(b=dg.index[-6].year, v=pct(dg.iloc[-6])),
            "warn" if dg.iloc[-1] > 60 else "", "#fi-gobierno"),
        lec(tx("l_int", L), "$" + num(float(gq["intereses"].iloc[-1] / gq["ingresos"].iloc[-1] * 100), 1, L),
            tx("l_int_d", L).format(p=pct(gp["intereses"].iloc[-1])), "", "#fi-financiamiento"),
        lec(tx("l_gas", L), pct(gp["gastos"].iloc[-1]), tx("l_gas_d", L).format(i=pct(gp["ingresos"].iloc[-1])), "", "#fi-gobierno"),
        lec(tx("l_fext", L), pct(gp["fin_interno"].iloc[-1] + gp["fin_externo"].iloc[-1]),
            tx("l_fext_d", L).format(i=pct(gp["fin_interno"].iloc[-1]), e=pct(gp["fin_externo"].iloc[-1], 1, True)), "", "#fi-financiamiento"),
    ]
    r0 = tx("r_medidas", L).format(cc=pct(abs(ccp.iloc[-1])), cub=pct(cub, 0), rem=usd(rem12.iloc[-1]), gas=pct(gp["gastos"].iloc[-1]),
                                   ing=pct(gp["ingresos"].iloc[-1]), bal=pct(abs(gp["balance"].iloc[-1])), deu=pct(dg.iloc[-1]))
    antes = seccion("ext-medidas", tx("s_medidas", L), r0, f'<div class="lecturas ocho">{"".join(tiles)}</div>')

    # ------------------------------------------------ cuenta corriente por componentes
    comp = pd.DataFrame({c: s4[c] for c in ("bienes", "servicios", "ingreso_primario", "ingreso_secundario", "cc")}).loc["2005":].dropna() / 1000
    xq = comp.index + pd.offsets.QuarterEnd(0)
    f1 = cs.base(L, height=380, suffix="")
    for col, lbl, color in (("bienes", "lbl_bie", cs.C1), ("servicios", "lbl_ser", cs.C7), ("ingreso_primario", "lbl_ip", cs.C2), ("ingreso_secundario", "lbl_is", cs.C3)):
        f1.add_trace(go.Bar(x=list(xq), y=comp[col].round(2).tolist(), name=tx(lbl, L), marker=dict(color=color, line=dict(width=0)),
                            hovertemplate=tx(lbl, L) + ": US$%{y:.1f}" + mm + "<extra></extra>"))
    cs.linea(f1, xq, comp["cc"], tx("lbl_cc", L), cs.C4, width=2.6, fmt=".1f", suf=mm, lang=L)
    f1.update_layout(barmode="relative", bargap=0.1)
    f1.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    cs.ejes(f1, y="Miles de millones de dólares (4 trimestres)" if L == "es" else "US$ billions (4 quarters)")
    q_btn = (f'<button type="button" class="ex-q" data-dialog="exp-externo" aria-haspopup="dialog" '
             f'title="{"¿Cómo leer la balanza de pagos y las cuentas del Gobierno?" if L == "es" else "How to read the balance of payments and government accounts?"}">?</button>')
    g1 = cs.bloque_grafico(tx("g_cc", L), cs.fig_html(f1, {}, "g-ext-cc"), tx("h_cc", L))
    g1 = g1.replace("</figcaption>", f" {q_btn}</figcaption>", 1)
    xm = pd.DataFrame({"x": s4["exportaciones_bienes"], "m": s4["importaciones_bienes"]}).loc["2005":].dropna() / 1000
    f2 = cs.base(L, height=380, suffix="")
    cs.linea(f2, xm.index + pd.offsets.QuarterEnd(0), xm["x"], tx("lbl_x", L), cs.C3, width=2.4, fmt=".1f", suf=mm, lang=L)
    cs.linea(f2, xm.index + pd.offsets.QuarterEnd(0), xm["m"], tx("lbl_m", L), cs.C2, width=2.4, fmt=".1f", suf=mm, lang=L)
    cs.ejes(f2, y="Miles de millones de dólares (4 trimestres)" if L == "es" else "US$ billions (4 quarters)")
    g2 = cs.bloque_grafico(tx("g_xm", L), cs.fig_html(f2, {}, "g-ext-xm"), tx("h_xm", L))
    u4 = {c: float(s4[c].iloc[-1]) for c in s4}
    r1 = tx("r_cc", L).format(b=usd(abs(u4["bienes"])), s=usd(abs(u4["servicios"])), p=usd(abs(u4["ingreso_primario"])),
                              t=usd(u4["ingreso_secundario"]), cc=usd(abs(u4["cc"])))
    s_cc = seccion("ext-cc", tx("s_cc", L), r1, f'<div class="grid">{g1}{g2}</div>') + ventana_externo(L)

    # ------------------------------------------------ financiacion
    fi = pd.DataFrame({c: -s4[c] for c in ("cf_directa", "cf_cartera", "cf_otra", "cf_reservas", "cf_derivados")}).loc["2005":].dropna() / 1000
    defi = (-comp["cc"]).reindex(fi.index)
    xf_ = fi.index + pd.offsets.QuarterEnd(0)
    f3 = cs.base(L, height=380, suffix="")
    for col, lbl, color in (("cf_directa", "lbl_fd", cs.C1), ("cf_cartera", "lbl_fc", cs.C7), ("cf_otra", "lbl_fo", cs.C3),
                            ("cf_derivados", "lbl_fx", cs.C4), ("cf_reservas", "lbl_fr", cs.C2)):
        f3.add_trace(go.Bar(x=list(xf_), y=fi[col].round(2).tolist(), name=tx(lbl, L), marker=dict(color=color, line=dict(width=0)),
                            hovertemplate=tx(lbl, L) + ": US$%{y:.1f}" + mm + "<extra></extra>"))
    cs.linea(f3, xf_, defi, tx("lbl_def", L), cs.INK2, width=2.0, dash="dot", fmt=".1f", suf=mm, lang=L)
    f3.update_layout(barmode="relative", bargap=0.1)
    f3.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    cs.ejes(f3, y="Miles de millones de dólares (4 trimestres)" if L == "es" else "US$ billions (4 quarters)")
    g3 = cs.bloque_grafico(tx("g_fin", L), cs.fig_html(f3, {}, "g-ext-financiacion"), tx("h_fin", L), ancho=True)
    r2 = tx("r_fin", L).format(d=usd(-u4["cf_directa"]), c=usd(-u4["cf_cartera"]), o=usd(-u4["cf_otra"]), r=num(u4["cf_reservas"], 0, L, True))
    s_fi = seccion("ext-financiacion", tx("s_fin", L), r2, f'<div class="grid">{g3}</div>')

    # ------------------------------------------------ IED por sector y remesas
    secs = list(TX["ied_sec"])
    ult = {s_: float(suma4(X[f"ied_{s_}"]).dropna().iloc[-1]) for s_ in secs}
    ant = {s_: float(suma4(X[f"ied_{s_}"]).dropna().iloc[-5]) for s_ in secs}
    orden = sorted(secs, key=lambda s_: ult[s_])
    f4 = cs.base(L, height=400, fecha_x=False, suffix="")
    for dic, lbl, color in ((ant, "lbl_ant", cs.C4), (ult, "lbl_ult", cs.C1)):
        f4.add_trace(go.Bar(y=[TX["ied_sec"][s_][k] for s_ in orden], x=[round(dic[s_], 0) for s_ in orden], orientation="h", name=tx(lbl, L),
                            marker=dict(color=color, line=dict(width=0)), hovertemplate="%{y}: US$%{x:,.0f}<extra></extra>"))
    f4.update_xaxes(showgrid=True, gridcolor=cs.GRID, tickprefix="$")
    f4.update_yaxes(ticksuffix="", tickfont=dict(size=11.5, color=cs.INK2))
    f4.update_layout(barmode="group", bargap=0.25, hovermode="closest")
    cs.ejes(f4, x="Millones de dólares" if L == "es" else "US$ million")
    g4 = cs.bloque_grafico(tx("g_ieds", L), cs.fig_html(f4, {"notime": True, "noy": True}, "g-ext-ied-sectores"), tx("h_ieds", L))
    rr = (rem12 / 1000).loc["2005":]
    f5 = cs.base(L, height=400, suffix="")
    cs.linea(f5, rr.index + pd.offsets.MonthEnd(0), rr, tx("lbl_rem", L), cs.C3, width=2.6, fmt=".2f", suf=mm, lang=L)
    rp = rem_p.loc["2005":]
    f5.add_trace(go.Scatter(x=list(rp.index + pd.offsets.MonthEnd(0)), y=rp.round(2).tolist(), yaxis="y2", mode="lines", name=tx("lbl_remp", L),
                            line=dict(color=cs.C7, width=1.6, dash="dot"), hovertemplate="%{y:.2f}% " + ("del PIB" if L == "es" else "of GDP") + "<extra></extra>"))
    f5.update_layout(yaxis2=dict(overlaying="y", side="right", showgrid=False, zeroline=False, fixedrange=True, ticksuffix="%", tickfont=dict(size=11.5, color=cs.MUTED)))
    cs.ejes(f5, y="Miles de millones de dólares (12 meses)" if L == "es" else "US$ billions (12 months)", y2="% del PIB" if L == "es" else "% of GDP")
    g5 = cs.bloque_grafico(tx("g_rem", L), cs.fig_html(f5, {"noy": True}, "g-ext-remesas"), tx("h_rem", L))
    tot_ied = sum(ult.values())
    top = sorted(secs, key=lambda s_: -ult[s_])
    nm = lambda s_: TX["ied_sec"][s_][k].lower() if L == "es" else TX["ied_sec"][s_][k]
    r3 = tx("r_entran", L).format(ied=usd(u4["ied"]), s1=TX["ied_sec"][top[0]][k], p1=pct(ult[top[0]] / tot_ied * 100, 0), s2=nm(top[1]),
                                  p2=pct(ult[top[1]] / tot_ied * 100, 0), rem=usd(rem12.iloc[-1]), cr=pct((rem12.iloc[-1] / rem12.iloc[-13] - 1) * 100, 1, True))
    s_en = seccion("ext-entran", tx("s_entran", L), r3, f'<div class="grid">{g4}{g5}</div>')

    # ------------------------------------------------ deuda externa y PII
    de = pd.DataFrame({"pu": X["deuda_externa_publica"], "pr": X["deuda_externa_privada"], "p": X["deuda_externa_pib"]}).dropna().loc["2005":]
    xd = de.index + pd.offsets.MonthEnd(0)
    f6 = cs.base(L, height=380, suffix="")
    for col, lbl, color in (("pu", "lbl_pu", cs.C1), ("pr", "lbl_pr", cs.C7)):
        f6.add_trace(go.Scatter(x=list(xd), y=(de[col] / 1000).round(1).tolist(), mode="lines", stackgroup="d", name=tx(lbl, L),
                                line=dict(color=color, width=0.5), fillcolor=color, hovertemplate=tx(lbl, L) + ": US$%{y:.1f}" + mm + "<extra></extra>"))
    f6.add_trace(go.Scatter(x=list(xd), y=de["p"].round(1).tolist(), yaxis="y2", mode="lines", name=tx("lbl_dp", L),
                            line=dict(color=cs.C2, width=2.2), hovertemplate="%{y:.1f}% " + ("del PIB" if L == "es" else "of GDP") + "<extra></extra>"))
    f6.update_layout(yaxis2=dict(overlaying="y", side="right", showgrid=False, zeroline=False, fixedrange=True, ticksuffix="%", rangemode="tozero", tickfont=dict(size=11.5, color=cs.MUTED)))
    cs.ejes(f6, y="Miles de millones de dólares" if L == "es" else "US$ billions", y2="% del PIB" if L == "es" else "% of GDP")
    g6 = cs.bloque_grafico(tx("g_dext", L), cs.fig_html(f6, {"noy": True}, "g-ext-deuda"), tx("h_dext", L))
    pi_ = pd.DataFrame({"a": X["pii_activos"], "p": X["pii_pasivos"]}).dropna().loc["2005":] / 1000
    xp = pi_.index + pd.offsets.QuarterEnd(0)
    f7 = cs.base(L, height=380, suffix="")
    cs.linea(f7, xp, pi_["a"], tx("lbl_act", L), cs.C3, width=2.2, fmt=".0f", suf=mm, lang=L)
    cs.linea(f7, xp, pi_["p"], tx("lbl_pas", L), cs.C2, width=2.2, fmt=".0f", suf=mm, lang=L)
    pp_ = piip.loc["2005":]
    f7.add_trace(go.Scatter(x=list(pp_.index + pd.offsets.QuarterEnd(0)), y=pp_.round(1).tolist(), yaxis="y2", mode="lines", name=tx("lbl_net", L),
                            line=dict(color=cs.C7, width=1.8, dash="dot"), hovertemplate="%{y:.1f}% " + ("del PIB" if L == "es" else "of GDP") + "<extra></extra>"))
    f7.update_layout(yaxis2=dict(overlaying="y", side="right", showgrid=False, zeroline=False, fixedrange=True, ticksuffix="%", tickfont=dict(size=11.5, color=cs.MUTED)))
    cs.ejes(f7, y="Miles de millones de dólares" if L == "es" else "US$ billions", y2="Neta, % del PIB" if L == "es" else "Net, % of GDP")
    g7 = cs.bloque_grafico(tx("g_pii", L), cs.fig_html(f7, {"noy": True}, "g-ext-pii"), tx("h_pii", L))
    r4 = tx("r_deuda", L).format(t=usd(dext.iloc[-1]), p=pct(X["deuda_externa_pib"].dropna().iloc[-1]), pu=usd(X["deuda_externa_publica"].dropna().iloc[-1]),
                                 pr=usd(X["deuda_externa_privada"].dropna().iloc[-1]), pii=usd(abs(pii.iloc[-1])), ppii=pct(abs(piip.iloc[-1])))
    s_de = seccion("ext-deuda", tx("s_deuda", L), r4, f'<div class="grid">{g6}{g7}</div>')

    # ------------------------------------------------ Gobierno: ingresos, gastos, balance y deuda
    gdf = pd.DataFrame(gp).loc["2005":]
    xg = gdf.index + pd.offsets.QuarterEnd(0)
    f8 = cs.base(L, height=360)
    for col, lbl, color, w_ in (("ingresos", "lbl_ing", cs.C3, 2.4), ("gastos", "lbl_gas", cs.C2, 2.4), ("intereses", "lbl_int", cs.C7, 1.8)):
        cs.linea(f8, xg, gdf[col], tx(lbl, L), color, width=w_, lang=L)
    cs.ejes(f8, y="% del PIB (12 meses)" if L == "es" else "% of GDP (12 months)")
    g8 = cs.bloque_grafico(tx("g_gob", L), cs.fig_html(f8, {}, "g-fi-gobierno"), tx("h_gob", L))
    bp = gdf["balance"] + gdf["intereses"]
    f9 = cs.base(L, height=360)
    cs.linea(f9, xg, gdf["balance"], tx("lbl_bal", L), cs.C2, width=2.6, lang=L)
    cs.linea(f9, xg, bp, tx("lbl_bp", L), cs.C1, width=2.0, lang=L)
    f9.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    cs.ejes(f9, y="% del PIB (12 meses)" if L == "es" else "% of GDP (12 months)")
    g9 = cs.bloque_grafico(tx("g_bal", L), cs.fig_html(f9, {}, "g-fi-balance"), tx("h_bal", L))
    dd = dg.loc["1995":]
    f10 = cs.base(L, height=330, fecha_x=False)
    f10.add_trace(go.Bar(x=[str(a.year) for a in dd.index], y=dd.round(1).tolist(), showlegend=False,
                         marker=dict(color=[cs.C2 if v > 60 else cs.C1 for v in dd], line=dict(width=0)),
                         hovertemplate="%{x}: %{y:.1f}%<extra></extra>"))
    f10.update_layout(bargap=0.2, hovermode="closest")
    cs.ejes(f10, y="% del PIB" if L == "es" else "% of GDP")
    g10 = cs.bloque_grafico(tx("g_dgnc", L), cs.fig_html(f10, {"notime": True, "noy": True}, "g-fi-deuda"), tx("h_dgnc", L), ancho=True)
    r5 = tx("r_gob", L).format(i=pct(gp["ingresos"].iloc[-1]), g=pct(gp["gastos"].iloc[-1]), int=pct(gp["intereses"].iloc[-1]),
                               b=pct(gp["balance"].iloc[-1], 1, True), bp=pct(bp.iloc[-1], 1, True), a=dg.index[-1].year, d=pct(dg.iloc[-1]))
    s_go = seccion("fi-gobierno", tx("s_gob", L), r5, f'<div class="grid">{g8}{g9}{g10}</div>')

    # ------------------------------------------------ financiamiento e intereses
    fdf = pd.DataFrame({"fi": gp["fin_interno"], "fe": gp["fin_externo"]}).loc["2005":]
    ii = (gq["intereses"] / gq["ingresos"] * 100).loc["2005":]
    xf2 = fdf.index + pd.offsets.QuarterEnd(0)
    f11 = cs.base(L, height=380)
    for col, lbl, color in (("fi", "lbl_fi", cs.C1), ("fe", "lbl_fe", cs.C4)):
        f11.add_trace(go.Bar(x=list(xf2), y=fdf[col].round(2).tolist(), name=tx(lbl, L), marker=dict(color=color, line=dict(width=0)),
                             hovertemplate=tx(lbl, L) + ": %{y:.1f}%<extra></extra>"))
    f11.add_trace(go.Scatter(x=list(ii.index + pd.offsets.QuarterEnd(0)), y=ii.round(1).tolist(), yaxis="y2", mode="lines", name=tx("lbl_ii", L),
                             line=dict(color=cs.C2, width=2.4), hovertemplate="%{y:.1f}%<extra></extra>"))
    f11.update_layout(barmode="relative", bargap=0.1, yaxis2=dict(overlaying="y", side="right", showgrid=False, zeroline=False, fixedrange=True,
                                                                   ticksuffix="%", rangemode="tozero", tickfont=dict(size=11.5, color=cs.MUTED)))
    f11.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    cs.ejes(f11, y="% del PIB (12 meses)" if L == "es" else "% of GDP (12 months)", y2="Intereses / ingresos" if L == "es" else "Interest / revenue")
    g11 = cs.bloque_grafico(tx("g_gfin", L), cs.fig_html(f11, {"noy": True}, "g-fi-financiamiento"), tx("h_gfin", L), ancho=True)
    neg = int((X["gnc_intereses"].dropna().iloc[-24:] < 0).sum())
    r6 = tx("r_gfin", L).format(pi=num(float(ii.iloc[-1]), 1, L), fi=pct(gp["fin_interno"].iloc[-1]), fe=pct(gp["fin_externo"].iloc[-1], 1, True),
                                nota=tx("nota_int", L).format(n=neg) if neg else "")
    s_gf = seccion("fi-financiamiento", tx("s_gfin", L), r6, f'<div class="grid">{g11}</div>')

    items = "".join(f'<li><span class="ref">{ref}</span><span class="ref-u">{es if L == "es" else en}</span></li>' for ref, es, en in LITERATURA)
    s_lit = (f'<section id="ext-literatura" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{tx("s_lit", L)}</h2></div>'
             f'<ol class="refs">{items}</ol></section>')
    return antes, s_cc + s_fi + s_en + s_de + s_go + s_gf + s_lit


# ====================================================================== ventana explicativa
def ventana_externo(L) -> str:
    es = L == "es"
    T = (lambda a, b: a if es else b)
    pasos = [(T("Bienes y servicios", "Goods and services"), T("Lo que el país vende y compra al exterior.", "What the country sells to and buys from abroad.")),
             (T("Ingreso primario", "Primary income"), T("Utilidades de empresas extranjeras, dividendos e intereses que se pagan o reciben.", "Profits of foreign companies, dividends and interest paid or received.")),
             (T("Ingreso secundario", "Secondary income"), T("Transferencias sin contrapartida, sobre todo remesas de colombianos en el exterior.", "Transfers without counterpart, mainly remittances from Colombians abroad.")),
             (T("Cuenta corriente", "Current account"), T("La suma de lo anterior. Si es negativa, el país gasta más de lo que recibe del exterior.", "The sum of the above. If negative, the country spends more than it receives from abroad.")),
             (T("Cuenta financiera", "Financial account"), T("Cómo se financia: inversión directa, de cartera, otra inversión (préstamos) y reservas. Tiene el mismo signo de la cuenta corriente.", "How it is financed: direct, portfolio and other investment (loans) and reserves. It has the same sign as the current account."))]
    esc_ = "".join(f'<li style="--i:{i}"><b>{i + 1}</b><span>{a}</span><em>{b}</em></li>' for i, (a, b) in enumerate(pasos))
    return f"""<dialog class="explica" id="exp-externo" aria-labelledby="exp-externo-t">
<div class="ex-cab"><p class="ex-k">{T("Para entender", "To understand")} · Banco de la República · MinHacienda</p><h2 id="exp-externo-t">{T("¿Cómo leer la balanza de pagos y las cuentas del Gobierno?", "How to read the balance of payments and government accounts?")}</h2>
<button type="button" class="ex-x" data-cerrar aria-label="{T("Cerrar", "Close")}">✕</button></div>
<div class="ex-cuerpo">
<p class="ex-lede">{T("La balanza de pagos registra los flujos reales y financieros que Colombia intercambia con el resto del mundo. El Banco de la República la elabora con el Manual de Balanza de Pagos del FMI (sexta versión) y tiene dos grandes cuentas: la cuenta corriente y la cuenta financiera.",
 "The balance of payments records the real and financial flows Colombia exchanges with the rest of the world. Banco de la República compiles it following the IMF Balance of Payments Manual (sixth edition), and it has two main accounts: the current account and the financial account.")}</p>
<h3>{T("1. Las piezas de la balanza de pagos", "1. The pieces of the balance of payments")}</h3>
<ol class="ex-escalera">{esc_}</ol>
<p class="ex-nota">{T("Los errores y omisiones cierran la diferencia estadística entre las dos cuentas.", "Errors and omissions close the statistical gap between the two accounts.")}</p>
<h3>{T("2. Deuda externa y posición de inversión internacional", "2. External debt and international investment position")}</h3>
<ul class="ex-lista">
<li>{T("Deuda externa: pasivos desembolsados y pendientes de pago que los residentes tienen con no residentes (préstamos, créditos de proveedores, bonos y arrendamiento financiero). No incluye las inversiones de portafolio en Colombia.", "External debt: disbursed, outstanding liabilities of residents to non-residents (loans, supplier credits, bonds and financial leases). It excludes portfolio investment in Colombia.")}</li>
<li>{T("Posición de inversión internacional: el saldo de todos los activos y pasivos financieros del país con el exterior; es el estado complementario de la balanza de pagos.", "International investment position: the balance of all the country's financial assets and liabilities with the rest of the world; it complements the balance of payments.")}</li>
</ul>
<h3>{T("3. Las cuentas del Gobierno", "3. Government accounts")}</h3>
<ul class="ex-lista">
<li>{T("Las cifras del Gobierno nacional central y del sector público no financiero son de caja: un empalme de las series históricas del DNP con las del Ministerio de Hacienda, sin causaciones. Para las cifras oficiales en metodología de causación, la fuente es el Ministerio de Hacienda.", "Central government and non-financial public sector figures are on a cash basis: a splice of DNP historical series with Ministry of Finance series, without accruals. For official accrual-basis figures, the source is the Ministry of Finance.")}</li>
<li>{T("Balance = ingresos − gastos. Balance primario = balance sin los intereses: muestra si el Gobierno cubre sus gastos corrientes sin contar el costo de la deuda.", "Balance = revenue − spending. Primary balance = balance excluding interest: it shows whether the Government covers its spending before the cost of debt.")}</li>
<li>{T("Todas las razones al PIB de esta página usan el PIB nominal del DANE de los mismos cuatro trimestres (en dólares, con la TRM promedio).", "All ratios to GDP on this page use DANE nominal GDP for the same four quarters (in dollars, at the average TRM).")}</li>
</ul>
<h3>{T("Fuentes oficiales", "Official sources")}</h3>
<ul class="ex-fuentes">
<li><a href="https://suameca.banrep.gov.co/graficador-series/" target="_blank" rel="noopener">{T("Banco de la República — balanza de pagos, deuda externa, posición de inversión internacional y balance fiscal (series estadísticas)", "Banco de la República — balance of payments, external debt, international investment position and fiscal balance (statistical series)")}</a></li>
<li><a href="https://www.minhacienda.gov.co" target="_blank" rel="noopener">{T("Ministerio de Hacienda y Crédito Público — estadísticas fiscales", "Ministry of Finance — fiscal statistics")}</a></li>
<li>{T("FMI (2009). Manual de Balanza de Pagos y Posición de Inversión Internacional, sexta edición.", "IMF (2009). Balance of Payments and International Investment Position Manual, sixth edition.")}</li>
</ul>
</div></dialog>"""
