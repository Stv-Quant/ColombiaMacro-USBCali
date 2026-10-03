"""Pagina de tasas de interes ampliada (v12.14): ocho medidas, ciclos de la tasa del Banco, transmision a
las tasas del mercado (con cuanto llego de cada ciclo), costo del credito por modalidad, la curva corta del
IBR, control del mercado interbancario, margen de intermediacion, credito (cartera) y liquidez del Banco,
ventana explicativa y literatura.

Solo datos observados del Banco de la Republica (graficador SUAMECA): tasa de politica, IBR, TIB, DTF y CDT,
tasas de colocacion por modalidad (formato 088 de la Superintendencia Financiera), cartera y saldos de
operaciones de mercado abierto.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

TX = {
    "s_medidas": ("Las tasas de interés en ocho medidas", "Interest rates in eight measures"),
    "s_ciclos": ("Los ciclos de la tasa del Banco", "Policy-rate cycles"),
    "s_trans": ("¿Llega la tasa del Banco a los créditos y a los ahorros?", "Does the policy rate reach loans and savings?"),
    "s_credito": ("¿Cuánto cuesta el crédito?", "How much does credit cost?"),
    "s_ibr": ("El mercado de dinero de corto plazo", "The short-term money market"),
    "s_cartera": ("¿Cuánto crédito hay y cuánto crece?", "How much credit is there and how fast is it growing?"),
    "s_liquidez": ("La liquidez que da el Banco", "Liquidity provided by the Bank"),
    "s_lit": ("Bases metodológicas y literatura", "Methodological basis and literature"),
    # lecturas
    "l_tpm": ("Tasa del Banco · desde {f}", "Policy rate · since {f}"), "l_tpm_d": ("última decisión {c} · hace un año {a}", "last decision {c} · a year ago {a}"),
    "l_ciclo": ("Ciclo actual", "Current cycle"), "l_ciclo_d": ("{n} decisiones desde {f} ({de} → {a})", "{n} decisions since {f} ({de} → {a})"),
    "subidas": ("de subidas", "of hikes"), "bajadas": ("de bajadas", "of cuts"),
    "l_real": ("Tasa real ex ante", "Ex-ante real rate"), "l_real_d": ("neutral estimada {lo}–{hi}", "estimated neutral {lo}–{hi}"),
    "l_ibr": ("IBR a un día − tasa del Banco", "Overnight IBR − policy rate"), "l_ibr_d": ("IBR {v} · el Banco controla la tasa a un día", "IBR {v} · the Bank steers the overnight rate"),
    "l_ibr3": ("IBR a 3 meses", "3-month IBR"), "l_ibr3_d": ("{s} frente a la tasa del Banco", "{s} versus the policy rate"),
    "l_cdt": ("CDT a 90 días", "90-day CD rate"), "l_cdt_d": ("lo que pagan los bancos por el ahorro · 12 meses {c}", "what banks pay on savings · 12 months {c}"),
    "l_col": ("Crédito nuevo (promedio)", "New lending (average)"), "l_col_d": ("{c} en 12 meses · margen sobre CDT {m}", "{c} over 12 months · spread over CD {m}"),
    "l_cart": ("Crédito total, crecimiento real", "Total credit, real growth"), "l_cart_d": ("anual, descontada la inflación · {f}", "annual, net of inflation · {f}"),
    # respuestas
    "r_medidas": ("La tasa del Banco de la República es {t} desde el {f}, tras {n} decisiones {dir} desde {fi} ({x}). "
                  "Las tasas de mercado la siguen: el IBR a un día está en {i}, el CDT a 90 días en {c} y el crédito nuevo promedio en {k}. "
                  "Descontada la inflación, el crédito total crece {g} al año.",
                  "The Banco de la República policy rate is {t} since {f}, after {n} decisions {dir_en} since {fi} ({x}). "
                  "Market rates follow it: the overnight IBR is {i}, the 90-day CD {c} and the average new loan {k}. "
                  "Net of inflation, total credit is growing {g} a year."),
    "r_ciclos": ("Desde 2000 la tasa del Banco ha tenido {k} ciclos completos de subidas y bajadas. El más fuerte fue {mx}. "
                 "El ciclo actual, {dir} desde {fi}, suma {x} en {n} decisiones.",
                 "Since 2000 the policy rate has gone through {k} complete cycles of hikes and cuts. The largest was {mx}. "
                 "The current cycle, {dir_en} since {fi}, adds {x} in {n} decisions."),
    "mx_txt": ("{d} entre {a} y {b} ({x})", "{d} between {a} and {b} ({x})"),
    "r_trans": ("En el ciclo anterior (desde {f1}) la tasa del Banco cambió {t1}; tres meses después de la última decisión el IBR a 3 meses había cambiado {i1}, el CDT a 90 días {c1} y el crédito nuevo {k1}. "
                "En el ciclo actual ({t2} desde {f2}) van: IBR a 3 meses {i2}, CDT {c2} y crédito nuevo {k2}. {lect}",
                "In the previous cycle (from {f1}) the policy rate changed {t1}; three months after the last decision the 3-month IBR had changed {i1}, the 90-day CD {c1} and new lending {k1}. "
                "In the current cycle ({t2} since {f2}) so far: 3-month IBR {i2}, CD {c2} and new lending {k2}. {lect}"),
    "lect_lenta": ("Hasta ahora el traspaso es mayor en el mercado interbancario y el crédito que en el ahorro.", "So far pass-through is larger in the interbank market and lending than in savings."),
    "lect_pareja": ("Hasta ahora el traspaso es parecido en el mercado interbancario, el crédito y el ahorro.", "So far pass-through is similar across the interbank market, lending and savings."),
    "r_credito": ("El crédito de consumo cuesta {c}, el comercial ordinario {o}, el corporativo (preferencial) {p} y el de vivienda {v}. "
                  "Descontando la inflación de {inf}, la tasa real del crédito nuevo promedio es {r}. Frente a hace un año, el crédito nuevo cambió {d}.",
                  "Consumer credit costs {c}, ordinary commercial {o}, corporate (preferential) {p} and housing {v}. "
                  "Net of inflation of {inf}, the real rate on average new lending is {r}. Compared with a year ago, new lending changed {d}."),
    "r_ibr": ("El IBR es la tasa a la que los bancos se prestan pesos entre sí. Hoy: un día {on}, 1 mes {m1}, 3 meses {m3}, 6 meses {m6} y 12 meses {m12}. "
              "En el último año el IBR a un día se alejó en promedio {d} de la tasa del Banco: así se ve que la decisión de la Junta se cumple en el mercado.",
              "The IBR is the rate at which banks lend pesos to each other. Today: overnight {on}, 1 month {m1}, 3 months {m3}, 6 months {m6} and 12 months {m12}. "
              "Over the last year the overnight IBR deviated on average {d} from the policy rate: this shows the Board's decision holds in the market."),
    "r_cartera": ("El saldo de crédito en pesos suma ${s} billones. En términos reales crece {g} al año: consumo {c}, comercial {co}, vivienda {v} y microcrédito {m}. "
                  "El crédito comercial es {pc} del total; el de consumo, {pq}.",
                  "Outstanding peso credit totals COP {s} trillion. In real terms it grows {g} a year: consumer {c}, commercial {co}, housing {v} and microcredit {m}. "
                  "Commercial credit is {pc} of the total; consumer, {pq}."),
    "r_liq": ("En el último mes el Banco tuvo en promedio ${e} billones prestados a los bancos mediante repos de expansión y recibió ${c} billones en depósitos de contracción. "
              "Así ajusta la cantidad de pesos para que la tasa a un día quede cerca de la tasa de política.",
              "Last month the Bank had on average COP {e} trillion lent to banks through expansion repos and received COP {c} trillion in contraction deposits. "
              "This is how it adjusts the amount of pesos so the overnight rate stays close to the policy rate."),
    # graficos
    "g_ciclos": ("Tasa del Banco y sus ciclos desde 2000", "Policy rate and its cycles since 2000"),
    "h_ciclos": ("Tasa de política monetaria (último dato de cada semana). Las franjas naranjas son ciclos de subidas y las azules de bajadas (desde la primera hasta la última decisión en la misma dirección).",
                 "Monetary policy rate (last value of each week). Orange bands are hiking cycles and blue bands easing cycles (from the first to the last decision in the same direction)."),
    "tab_ciclos": ("Ciclos de la tasa del Banco", "Policy-rate cycles"),
    "th_ciclos": (("Desde", "Hasta", "Dirección", "Decisiones", "De → a", "Cambio", "Meses"),
                  ("From", "To", "Direction", "Decisions", "From → to", "Change", "Months")),
    "sube": ("Subidas", "Hikes"), "baja": ("Bajadas", "Cuts"), "en_curso": ("en curso", "ongoing"),
    "g_trans": ("Tasa del Banco, interbancaria, ahorro y crédito", "Policy, interbank, savings and lending rates"),
    "h_trans": ("Promedios mensuales. Todas las tasas se mueven con la del Banco; el crédito está por encima (riesgo y costos de los bancos) y el ahorro suele estar por debajo.",
                "Monthly averages. All rates move with the policy rate; lending sits above it (bank risk and costs) and savings usually below."),
    "lbl_tpm": ("Tasa del Banco", "Policy rate"), "lbl_ibr3": ("IBR 3 meses", "3-month IBR"), "lbl_cdt": ("CDT 90 días", "90-day CD"),
    "lbl_col": ("Crédito nuevo (total)", "New lending (total)"), "lbl_cons": ("Consumo", "Consumer"),
    "g_pass": ("¿Cuánto de cada ciclo llegó a cada tasa?", "How much of each cycle reached each rate?"),
    "h_pass": ("Cambio de cada tasa dividido por el cambio de la tasa del Banco, desde el día antes de la primera decisión hasta tres meses después de la última. 100% = traspaso completo; más de 100% = la tasa se movió más que la del Banco.",
               "Change in each rate divided by the change in the policy rate, from the day before the first decision to three months after the last. 100% = full pass-through; above 100% = the rate moved more than the policy rate."),
    "g_mod": ("Tasa del crédito nuevo por modalidad", "New-lending rate by type"),
    "h_mod": ("Tasa efectiva anual del último dato semanal. Barra clara: tasa real (menos la inflación anual). La línea punteada es la tasa del Banco.",
              "Effective annual rate of the latest weekly data. Light bar: real rate (minus annual inflation). The dotted line is the policy rate."),
    "lbl_nom": ("Nominal", "Nominal"), "lbl_realb": ("Real (menos inflación)", "Real (minus inflation)"),
    "g_marg": ("Margen de intermediación y prima del consumo", "Intermediation spread and consumer premium"),
    "h_marg": ("Crédito nuevo total menos CDT a 90 días (lo que cobran los bancos sobre lo que pagan) y consumo menos tasa del Banco, en puntos porcentuales; promedios mensuales.",
               "Total new lending minus 90-day CD (what banks charge over what they pay) and consumer minus policy rate, in percentage points; monthly averages."),
    "lbl_marg": ("Crédito − CDT 90 días", "Lending − 90-day CD"), "lbl_pcons": ("Consumo − tasa del Banco", "Consumer − policy rate"),
    "g_ibr": ("La curva del IBR: hoy, hace 3 meses y hace un año", "The IBR curve: today, 3 months and a year ago"),
    "h_ibr": ("IBR efectivo anual por plazo. Las rayas horizontales son la tasa del Banco en cada fecha. Si los plazos largos están por debajo del de un día, el mercado cobra menos por prestar a más tiempo.",
              "Effective annual IBR by tenor. Horizontal dashes are the policy rate on each date. If longer tenors are below overnight, the market charges less for lending longer."),
    "lbl_hoy": ("Hoy", "Today"), "lbl_3m": ("Hace 3 meses", "3 months ago"), "lbl_1a": ("Hace un año", "A year ago"),
    "g_spread": ("Tasas a un día frente a la tasa del Banco", "Overnight rates versus the policy rate"),
    "h_spread": ("IBR a un día y tasa interbancaria (TIB, préstamos sin garantía) menos la tasa de política, en puntos básicos. Cerca de cero = el Banco controla bien el costo del dinero a un día.",
                 "Overnight IBR and interbank rate (TIB, unsecured loans) minus the policy rate, in basis points. Near zero = the Bank firmly steers the overnight cost of money."),
    "lbl_ibron": ("IBR a un día", "Overnight IBR"), "lbl_tib": ("TIB", "TIB"),
    "g_cart": ("Crecimiento real del crédito por modalidad", "Real credit growth by type"),
    "h_cart": ("Variación anual del saldo de cartera en pesos, descontada la inflación anual del IPC. Desde 2015 la contabilidad bancaria usa NIIF (cambio metodológico).",
               "Annual change in the outstanding peso loan book, net of annual CPI inflation. Since 2015 bank accounting uses IFRS (methodological change)."),
    "g_comp": ("¿Para qué se presta? Composición del crédito", "What is lent for? Credit composition"),
    "h_comp": ("Participación de cada modalidad en el saldo de crédito en pesos.", "Share of each type in the outstanding peso loan book."),
    "lbl_total": ("Total", "Total"), "lbl_comercial": ("Comercial", "Commercial"), "lbl_consumo": ("Consumo", "Consumer"),
    "lbl_vivienda": ("Vivienda", "Housing"), "lbl_micro": ("Microcrédito", "Microcredit"),
    "g_liq": ("Repos de expansión y depósitos de contracción", "Expansion repos and contraction deposits"),
    "h_liq": ("Saldos diarios promediados por mes, en billones de pesos. Arriba: dinero que el Banco presta a los bancos (a un día y a más plazo). Abajo: dinero que los bancos depositan en el Banco.",
              "Daily balances averaged by month, in COP trillion. Above: money the Bank lends to banks (overnight and longer). Below: money banks deposit at the Bank."),
    "lbl_r1": ("Repos a un día", "Overnight repos"), "lbl_rp": ("Repos a más plazo", "Term repos"), "lbl_con": ("Contracción", "Contraction"),
    "plazos": {"on": ("Un día", "Overnight"), "1m": ("1 mes", "1 month"), "3m": ("3 meses", "3 months"), "6m": ("6 meses", "6 months"), "12m": ("12 meses", "12 months")},
    "tasas": {"ibr_on": ("IBR a un día", "Overnight IBR"), "ibr_3m": ("IBR 3 meses", "3-month IBR"), "cdt_90": ("CDT 90 días", "90-day CD"),
              "dtf_90": ("DTF", "DTF"), "col_total": ("Crédito nuevo", "New lending"), "col_consumo": ("Consumo", "Consumer"),
              "col_ordinario": ("Comercial ordinario", "Ordinary commercial"), "col_preferencial": ("Preferencial", "Preferential"),
              "col_tesoreria": ("Tesorería", "Treasury"), "col_vivienda": ("Vivienda", "Housing"), "col_vivienda_vis": ("Vivienda VIS", "Social housing")},
}
LITERATURA = [
    ("Taylor, J. B. (1993). Discretion versus Policy Rules in Practice. <i>Carnegie-Rochester Conference Series on Public Policy</i>, 39, 195–214.",
     "La regla que relaciona la tasa del banco central con la inflación y la brecha del producto.", "The rule linking the central bank rate to inflation and the output gap."),
    ("Clarida, R., Galí, J. y Gertler, M. (1999). The Science of Monetary Policy: A New Keynesian Perspective. <i>Journal of Economic Literature</i>, 37(4), 1661–1707.",
     "Marco moderno de la política monetaria con metas de inflación.", "Modern framework for inflation-targeting monetary policy."),
    ("Bernanke, B. S. y Gertler, M. (1995). Inside the Black Box: The Credit Channel of Monetary Policy Transmission. <i>Journal of Economic Perspectives</i>, 9(4), 27–48.",
     "El canal del crédito: cómo la política monetaria afecta la oferta de préstamos.", "The credit channel: how monetary policy affects loan supply."),
    ("Laubach, T. y Williams, J. C. (2003). Measuring the Natural Rate of Interest. <i>Review of Economics and Statistics</i>, 85(4), 1063–1070.",
     "Qué es la tasa real neutral y cómo se estima.", "What the neutral real rate is and how it is estimated."),
    ("Betancourt, R., Vargas, H. y Rodríguez, N. (2008). Interest Rate Pass-Through in Colombia: A Micro-Banking Perspective. <i>Cuadernos de Economía</i>, 45(131), 29–58.",
     "Traspaso de la tasa de política a las tasas de los bancos en Colombia.", "Pass-through of the policy rate to bank rates in Colombia."),
    ("Chavarro, X., Cristiano, D., Gómez, J. E., González, E. y Huertas, C. (2015). Evaluación de la transmisión de la tasa de interés de referencia a las tasas de interés del sistema financiero. <i>Borradores de Economía</i> 874, Banco de la República.",
     "La transmisión es heterogénea entre modalidades de crédito y simétrica entre subidas y bajadas.", "Transmission is heterogeneous across loan types and symmetric between hikes and cuts."),
    ("Banco de la República. Definiciones de la tasa de política monetaria, IBR, TIB, DTF, CDT y tasas de colocación (catálogo de series estadísticas).",
     "Cómo se calcula cada tasa de esta página.", "How each rate on this page is computed."),
]


def tx(k, L):
    return TX[k][0 if L == "es" else 1]


def ciclos_tpm(tpm: pd.Series) -> pd.DataFrame:
    """Ciclos de la tasa de politica: tramos de decisiones consecutivas en la misma direccion."""
    tpm = tpm.dropna().sort_index()
    mov = tpm.diff()
    mov = mov[mov.abs() > 1e-9]
    filas = []
    for f, v in mov.items():
        sg = int(np.sign(v))
        if filas and filas[-1]["signo"] == sg:
            c = filas[-1]
            c["hasta"], c["decisiones"], c["cambio"] = f, c["decisiones"] + 1, c["cambio"] + float(v)
        else:
            filas.append({"desde": f, "hasta": f, "signo": sg, "decisiones": 1, "cambio": float(v),
                          "antes": float(tpm.loc[:f - pd.Timedelta(days=1)].iloc[-1]) if len(tpm.loc[:f - pd.Timedelta(days=1)]) else np.nan})
    df = pd.DataFrame(filas, columns=["desde", "hasta", "signo", "decisiones", "cambio", "antes"])
    df["despues"] = df["antes"] + df["cambio"]
    df["meses"] = ((df["hasta"] - df["desde"]).dt.days / 30.44).round(0).astype(int) + 1
    return df


def traspaso(series: dict, tpm: pd.Series, ciclo, rezago_meses: int = 3) -> dict:
    """Cambio de cada tasa / cambio de la tasa del Banco entre el dia anterior al ciclo y `rezago_meses` despues."""
    a = ciclo["desde"] - pd.Timedelta(days=1)
    fin = tpm.index[-1]
    b = min(ciclo["hasta"] + pd.DateOffset(months=rezago_meses), fin)
    dt = float(tpm.asof(b) - tpm.asof(a))
    out = {}
    for k, s in series.items():
        s = s.dropna()
        if s.empty or s.index[0] > a or abs(dt) < 1e-9:
            out[k] = np.nan
            continue
        out[k] = float((s.asof(b) - s.asof(a)) / dt * 100)
    return out


def real_anual(saldo: pd.Series, inflacion: pd.Series) -> pd.Series:
    """Crecimiento real anual (%) de un saldo nominal mensual, deflactado con la inflacion anual."""
    g = saldo / saldo.shift(12) - 1
    pi = inflacion.reindex(saldo.index) / 100
    return ((1 + g) / (1 + pi) - 1) * 100


def construir_tasas(d, L):
    """Devuelve (antes, despues)."""
    from colombiamacro import modelo as mt
    from colombiamacro.fuentes import tasas_mercado as tmk
    from colombiamacro.sitio import construir as cs
    num, fecha, esc = cs.num, cs.fecha, cs.esc
    cs.LANG_ACTUAL[0] = L
    k = 0 if L == "es" else 1
    T = tmk.cargar()
    if T is None or d.extra["tpm"].empty:
        return "", ""
    pct = lambda v, dec=2, sg=False: num(float(v), dec, L, sg, "%")
    pp = lambda v, dec=2, sg=True: num(float(v), dec, L, sg, " pp")
    pb = lambda v: num(float(v) * 100, 0, L, True, " pb" if L == "es" else " bp")
    bill = "billones" if L == "es" else "trillion"
    nt = lambda c: TX["tasas"][c][k]
    tpm = d.extra["tpm"].set_index("fecha")["tpm"].sort_index()
    sb = pd.read_csv(cs.DATA_DIR / "series_banrep.csv", parse_dates=["fecha"])
    ibr_on = sb[sb["serie"] == "ibr_overnight"].set_index("fecha")["valor"].sort_index()
    infl = d.inflacion.set_index("fecha")["inflacion_anual"].sort_index()
    infl.index = infl.index.to_period("M").to_timestamp()
    cic = ciclos_tpm(tpm)
    act = cic.iloc[-1]
    hoy = tpm.index[-1]
    m = lambda s: s.dropna().resample("MS").mean()
    R = {"ibr_on": ibr_on, **{c: T[c] for c in ("ibr_3m", "cdt_90", "dtf_90", "col_total", "col_consumo", "col_ordinario",
                                                 "col_preferencial", "col_tesoreria", "col_vivienda", "col_vivienda_vis")}}
    ult = lambda c: float(R[c].dropna().iloc[-1])
    hace = lambda s, meses=12: float(s.dropna().loc[:s.dropna().index[-1] - pd.DateOffset(months=meses)].iloc[-1])
    lo, hi = mt.NEUTRAL_REAL
    real = d.tasas.set_index("fecha")["tpm_real_exante"].dropna()
    cart = T["cartera_total"]
    cart_r = real_anual(cart, infl).dropna()
    marg = m(T["col_total"]) - m(T["cdt_90"])

    def seccion(sid, titulo, resp, cuerpo):
        return (f'<section id="{sid}" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{titulo}</h2></div>'
                f'{cs.respuesta_html(resp, L)}{cuerpo}</section>')

    def lec(kk, v, dsc, tono, href):
        return (f'<a class="lec {tono}" href="{href}"><span class="lec-k">{kk}</span><b class="lec-v">{v}</b>'
                f'<span class="lec-d">{dsc}</span></a>')

    ult_mov = float(tpm.diff()[tpm.diff().abs() > 1e-9].iloc[-1])
    f_vig = tpm[tpm.diff().abs() > 1e-9].index[-1]
    dir_act = tx("subidas" if act["signo"] > 0 else "bajadas", L)
    tiles = [
        lec(tx("l_tpm", L).format(f=fecha(f_vig, "d", L)), pct(tpm.iloc[-1]), tx("l_tpm_d", L).format(c=pp(ult_mov), a=pct(hace(tpm))), "", "#banco"),
        lec(tx("l_ciclo", L), pp(act["cambio"]), tx("l_ciclo_d", L).format(n=int(act["decisiones"]), f=fecha(act["desde"], "m", L),
                                                                          de=pct(act["antes"]), a=pct(act["despues"])), "", "#ts-ciclos"),
        lec(tx("l_real", L), pct(real.iloc[-1], 1), tx("l_real_d", L).format(lo=pct(lo, 1), hi=pct(hi, 1)),
            "warn" if real.iloc[-1] > hi + 0.5 or real.iloc[-1] < lo - 0.5 else "ok", "#banco"),
        lec(tx("l_ibr", L), pb(ult("ibr_on") - tpm.iloc[-1]), tx("l_ibr_d", L).format(v=pct(ult("ibr_on"))), "", "#ts-ibr"),
        lec(tx("l_ibr3", L), pct(ult("ibr_3m")), tx("l_ibr3_d", L).format(s=pb(ult("ibr_3m") - tpm.iloc[-1])), "", "#ts-ibr"),
        lec(tx("l_cdt", L), pct(ult("cdt_90")), tx("l_cdt_d", L).format(c=pp(ult("cdt_90") - hace(R["cdt_90"]))), "", "#ts-transmision"),
        lec(tx("l_col", L), pct(ult("col_total")), tx("l_col_d", L).format(c=pp(ult("col_total") - hace(R["col_total"])), m=pp(float(marg.dropna().iloc[-1]), 1, False)), "", "#ts-credito"),
        lec(tx("l_cart", L), pct(cart_r.iloc[-1], 1, True), tx("l_cart_d", L).format(f=fecha(cart_r.index[-1], "m", L)),
            "warn" if cart_r.iloc[-1] < 0 else "", "#ts-cartera"),
    ]
    r0 = tx("r_medidas", L).format(t=pct(tpm.iloc[-1]), f=fecha(f_vig, "d", L), n=int(act["decisiones"]), dir=dir_act,
                                   dir_en=TX["subidas"][1] if act["signo"] > 0 else TX["bajadas"][1], fi=fecha(act["desde"], "m", L),
                                   x=pp(act["cambio"]), i=pct(ult("ibr_on")), c=pct(ult("cdt_90")), k=pct(ult("col_total")),
                                   g=pct(cart_r.iloc[-1], 1, True))
    antes = seccion("ts-medidas", tx("s_medidas", L), r0, f'<div class="lecturas ocho">{"".join(tiles)}</div>')

    # ------------------------------------------------ ciclos
    c00 = cic[cic["desde"] >= "2000-01-01"].reset_index(drop=True)
    tp_w = tpm.loc["2000":].resample("W-FRI").last().dropna()
    f1 = cs.base(L, height=360)
    for c in c00.itertuples():
        f1.add_vrect(x0=c.desde, x1=c.hasta + pd.Timedelta(days=5), line_width=0, layer="below",
                     fillcolor="rgba(235,104,52,0.14)" if c.signo > 0 else "rgba(42,120,214,0.14)")
    cs.linea(f1, tp_w.index, tp_w, tx("lbl_tpm", L), cs.C1, width=2.4, fmt=".2f", shape="hv", lang=L)
    cs.ejes(f1, y="Tasa de política (% anual)" if L == "es" else "Policy rate (% a year)")
    q_btn = (f'<button type="button" class="ex-q" data-dialog="exp-tpm" aria-haspopup="dialog" '
             f'title="{"¿Cómo funciona la tasa del Banco y cómo llega a la economía?" if L == "es" else "How does the policy rate work and reach the economy?"}">?</button>')
    g1 = cs.bloque_grafico(tx("g_ciclos", L), cs.fig_html(f1, {}, "g-ts-ciclos"), tx("h_ciclos", L), ancho=True)
    g1 = g1.replace("</figcaption>", f" {q_btn}</figcaption>", 1)
    th = TX["th_ciclos"][k]
    filas = "".join(
        f"<tr><td>{fecha(c.desde, 'm', L)}</td><td>{fecha(c.hasta, 'm', L)}{' (' + tx('en_curso', L) + ')' if i == len(c00) - 1 else ''}</td>"
        f"<td>{tx('sube' if c.signo > 0 else 'baja', L)}</td><td class='n'>{c.decisiones}</td>"
        f"<td class='n'>{pct(c.antes)} → {pct(c.despues)}</td><td class='n'>{pp(c.cambio)}</td><td class='n'>{c.meses}</td></tr>"
        for i, c in enumerate(c00.itertuples()))
    tabla = (f'<div class="table-wrap"><table class="tbl"><caption>{tx("tab_ciclos", L)}</caption><thead><tr>'
             f'{"".join(f"<th>{h}</th>" for h in th)}</tr></thead><tbody>{filas}</tbody></table></div>')
    comp = c00.iloc[:-1]
    mx = comp.loc[comp["cambio"].abs().idxmax()]
    r1 = tx("r_ciclos", L).format(k=len(comp), mx=tx("mx_txt", L).format(d=tx("sube" if mx["signo"] > 0 else "baja", L).lower(),
                                                                      a=fecha(mx["desde"], "m", L), b=fecha(mx["hasta"], "m", L), x=pp(mx["cambio"])),
                                  dir=dir_act, dir_en=TX["subidas"][1] if act["signo"] > 0 else TX["bajadas"][1],
                                  fi=fecha(act["desde"], "m", L), x=pp(act["cambio"]), n=int(act["decisiones"]))
    s_cic = seccion("ts-ciclos", tx("s_ciclos", L), r1, f'<div class="grid">{g1}</div>{tabla}') + ventana_tpm(tpm, ibr_on, T, L, num, fecha)

    # ------------------------------------------------ transmision
    mt_ = pd.DataFrame({"tpm": m(tpm), "ibr_3m": m(R["ibr_3m"]), "cdt_90": m(R["cdt_90"]), "col_total": m(R["col_total"]),
                        "col_consumo": m(R["col_consumo"])}).loc["2008":]
    xm = mt_.index + pd.offsets.MonthEnd(0)
    f2 = cs.base(L, height=380)
    for col, lbl, color, w_, dash in (("col_consumo", "lbl_cons", cs.C2, 1.6, "dot"), ("col_total", "lbl_col", cs.C2, 2.4, None),
                                      ("tpm", "lbl_tpm", cs.C1, 2.6, None), ("ibr_3m", "lbl_ibr3", cs.C7, 1.8, None),
                                      ("cdt_90", "lbl_cdt", cs.C3, 2.2, None)):
        cs.linea(f2, xm, mt_[col], tx(lbl, L), color, width=w_, dash=dash, fmt=".2f", lang=L)
    cs.ejes(f2, y="Tasa efectiva anual" if L == "es" else "Effective annual rate")
    g2 = cs.bloque_grafico(tx("g_trans", L), cs.fig_html(f2, {}, "g-ts-transmision"), tx("h_trans", L))
    cols_p = ["ibr_on", "ibr_3m", "cdt_90", "dtf_90", "col_total", "col_ordinario", "col_preferencial", "col_consumo", "col_vivienda"]
    cps = c00[c00["desde"] >= "2008-06-01"].tail(6)
    filas_p = [(f"{fecha(c['desde'], 'm', L)} – {fecha(c['hasta'], 'm', L)}{'*' if i == cps.index[-1] else ''} ({pp(c['cambio'], 2)})",
                traspaso({c_: R[c_] for c_ in cols_p}, tpm, c)) for i, c in cps.iterrows()]
    z = [[None if np.isnan(fp[1][c_]) else round(fp[1][c_]) for c_ in cols_p] for fp in filas_p]
    f3 = cs.base(L, height=360, fecha_x=False, suffix="")
    f3.add_trace(go.Heatmap(x=[nt(c_) for c_ in cols_p], y=[fp[0] for fp in filas_p], z=z, zmin=0, zmax=150,
                            colorscale=[[0, "#f7f6f2"], [0.4, "#bcd3ee"], [0.67, "#2a78d6"], [1, "#4a3aa7"]],
                            text=[[("—" if v is None else f"{v}%") for v in row] for row in z], texttemplate="%{text}",
                            textfont=dict(size=11), colorbar=dict(ticksuffix="%", thickness=10, len=0.7, outlinewidth=0, tickfont=dict(size=11, color=cs.MUTED)),
                            xgap=2, ygap=2, hovertemplate="%{y}<br>%{x}: %{z}%<extra></extra>"))
    f3.update_layout(hovermode="closest", showlegend=False)
    f3.update_xaxes(side="top", tickangle=-30, showline=False, tickfont=dict(size=11, color=cs.INK2))
    f3.update_yaxes(ticksuffix="", tickfont=dict(size=11, color=cs.INK2), gridcolor="rgba(0,0,0,0)")
    g3 = cs.bloque_grafico(tx("g_pass", L), cs.fig_html(f3, {"notime": True, "noy": True}, "g-ts-traspaso"),
                           tx("h_pass", L) + (" * = ciclo en curso." if L == "es" else " * = ongoing cycle."))
    # textos del traspaso: ultimo ciclo completo y ciclo actual (cambios en pp)
    def dif(c, col):
        a = c["desde"] - pd.Timedelta(days=1)
        b = min(c["hasta"] + pd.DateOffset(months=3), hoy)
        s = R[col].dropna()
        return float(s.asof(b) - s.asof(a))
    prev = cps.iloc[-2]
    r2 = tx("r_trans", L).format(f1=fecha(prev["desde"], "m", L), t1=pp(prev["cambio"]), i1=pp(dif(prev, "ibr_3m")), c1=pp(dif(prev, "cdt_90")),
                                 k1=pp(dif(prev, "col_total")), t2=pp(act["cambio"]), f2=fecha(act["desde"], "m", L),
                                 i2=pp(dif(act, "ibr_3m")), c2=pp(dif(act, "cdt_90")), k2=pp(dif(act, "col_total")),
                                 lect=tx("lect_lenta" if abs(dif(act, "cdt_90")) < 0.6 * min(abs(dif(act, "ibr_3m")), abs(dif(act, "col_total"))) else "lect_pareja", L))
    s_tr = seccion("ts-transmision", tx("s_trans", L), r2, f'<div class="grid">{g2}{g3}</div>')

    # ------------------------------------------------ costo del credito
    inf_u = float(infl.dropna().iloc[-1])
    mods = ["col_consumo", "col_ordinario", "col_vivienda", "col_vivienda_vis", "col_preferencial", "col_tesoreria", "col_total"]
    vals = [(c_, ult(c_)) for c_ in mods]
    f4 = cs.base(L, height=360, fecha_x=False)
    f4.add_trace(go.Bar(x=[nt(c_) for c_, _ in vals], y=[round(v, 2) for _, v in vals], name=tx("lbl_nom", L),
                        marker=dict(color=[cs.C2 if c_ == "col_total" else cs.C1 for c_, _ in vals], line=dict(width=0)),
                        text=[pct(v) for _, v in vals], textposition="outside", cliponaxis=False, hovertemplate="%{x}: %{y:.2f}%<extra></extra>"))
    rr = [100 * ((1 + v / 100) / (1 + inf_u / 100) - 1) for _, v in vals]
    f4.add_trace(go.Bar(x=[nt(c_) for c_, _ in vals], y=[round(v, 2) for v in rr], name=tx("lbl_realb", L),
                        marker=dict(color=cs.C4, opacity=0.55, line=dict(width=0)), hovertemplate="%{x} · real: %{y:.2f}%<extra></extra>"))
    f4.add_hline(y=float(tpm.iloc[-1]), line=dict(color=cs.INK2, width=1.2, dash="dot"))
    f4.update_yaxes(range=[0, max(v for _, v in vals) * 1.18])
    f4.update_layout(barmode="group", bargap=0.3, hovermode="closest")
    cs.ejes(f4, y="Tasa efectiva anual" if L == "es" else "Effective annual rate")
    g4 = cs.bloque_grafico(tx("g_mod", L), cs.fig_html(f4, {"notime": True, "noy": True}, "g-ts-modalidades"), tx("h_mod", L))
    mg = pd.DataFrame({"marg": marg, "pcons": m(T["col_consumo"]) - m(tpm)}).loc["2008":].dropna()
    f5 = cs.base(L, height=360, suffix=" pp")
    cs.linea(f5, mg.index + pd.offsets.MonthEnd(0), mg["marg"], tx("lbl_marg", L), cs.C1, width=2.2, fmt=".2f", suf=" pp", lang=L)
    cs.linea(f5, mg.index + pd.offsets.MonthEnd(0), mg["pcons"], tx("lbl_pcons", L), cs.C2, width=2.0, fmt=".2f", suf=" pp", lang=L)
    cs.ejes(f5, y="Puntos porcentuales" if L == "es" else "Percentage points")
    g5 = cs.bloque_grafico(tx("g_marg", L), cs.fig_html(f5, {}, "g-ts-margen"), tx("h_marg", L))
    r3 = tx("r_credito", L).format(c=pct(ult("col_consumo")), o=pct(ult("col_ordinario")), p=pct(ult("col_preferencial")),
                                   v=pct(ult("col_vivienda")), inf=pct(inf_u), r=pct(rr[-1]), d=pp(ult("col_total") - hace(R["col_total"])))
    s_cr = seccion("ts-credito", tx("s_credito", L), r3, f'<div class="grid">{g4}{g5}</div>')

    # ------------------------------------------------ IBR
    pl = [("on", ibr_on), ("1m", T["ibr_1m"]), ("3m", T["ibr_3m"]), ("6m", T["ibr_6m"]), ("12m", T["ibr_12m"])]
    f6 = cs.base(L, height=360, fecha_x=False)
    for off, lbl, col, w_ in ((0, "lbl_hoy", cs.C1, 2.8), (3, "lbl_3m", cs.C7, 2.0), (12, "lbl_1a", cs.C4, 2.0)):
        ref = hoy - pd.DateOffset(months=off)
        ys = [round(float(s.dropna().asof(ref)), 3) if s.dropna().index[0] <= ref else None for _, s in pl]
        f6.add_trace(go.Scatter(x=[TX["plazos"][p][k] for p, _ in pl], y=ys, mode="lines+markers", name=f"{tx(lbl, L)} ({fecha(ref, 'd', L)})",
                                line=dict(color=col, width=w_), marker=dict(size=7, color=col), hovertemplate="%{x}: %{y:.2f}%<extra></extra>"))
        f6.add_trace(go.Scatter(x=[TX["plazos"]["on"][k], TX["plazos"]["12m"][k]], y=[float(tpm.asof(ref))] * 2, mode="lines", showlegend=False,
                                line=dict(color=col, width=1, dash="dash"), hoverinfo="skip"))
    f6.update_layout(hovermode="closest")
    cs.ejes(f6, y="IBR efectivo anual" if L == "es" else "Effective annual IBR", x="Plazo" if L == "es" else "Tenor")
    g6 = cs.bloque_grafico(tx("g_ibr", L), cs.fig_html(f6, {"notime": True, "noy": True}, "g-ts-ibr"), tx("h_ibr", L))
    tb = pd.DataFrame({"ibr": ibr_on, "tib": T["tib"], "tpm": tpm}).ffill().loc["2008":]
    sp = pd.DataFrame({"ibr": (tb["ibr"] - tb["tpm"]) * 100, "tib": (tb["tib"] - tb["tpm"]) * 100}).resample("W-FRI").mean().dropna()
    f7 = cs.base(L, height=360, suffix="")
    cs.linea(f7, sp.index, sp["ibr"], tx("lbl_ibron", L), cs.C1, width=2.0, fmt=".0f", suf=" pb" if L == "es" else " bp", lang=L)
    cs.linea(f7, sp.index, sp["tib"], tx("lbl_tib", L), cs.C2, width=1.6, fmt=".0f", suf=" pb" if L == "es" else " bp", lang=L)
    f7.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    cs.ejes(f7, y="Puntos básicos sobre la tasa del Banco" if L == "es" else "Basis points over the policy rate")
    g7 = cs.bloque_grafico(tx("g_spread", L), cs.fig_html(f7, {}, "g-ts-overnight"), tx("h_spread", L))
    d12 = float((ibr_on - tpm.reindex(ibr_on.index, method="ffill")).loc[hoy - pd.DateOffset(years=1):].abs().mean() * 100)
    r4 = tx("r_ibr", L).format(on=pct(ult("ibr_on")), m1=pct(T["ibr_1m"].iloc[-1]), m3=pct(T["ibr_3m"].iloc[-1]), m6=pct(T["ibr_6m"].iloc[-1]),
                               m12=pct(T["ibr_12m"].iloc[-1]), d=num(d12, 0, L, False, " pb" if L == "es" else " bp"))
    s_ibr = seccion("ts-ibr", tx("s_ibr", L), r4, f'<div class="grid">{g6}{g7}</div>')

    # ------------------------------------------------ cartera
    cm = {"total": T["cartera_total"], "comercial": T["cartera_comercial"], "consumo": T["cartera_consumo"],
          "vivienda": T["cartera_vivienda"], "micro": T["cartera_micro"]}
    reales = pd.DataFrame({c_: real_anual(s, infl) for c_, s in cm.items()}).loc["2008":].dropna(how="all")
    xr = reales.index + pd.offsets.MonthEnd(0)
    f8 = cs.base(L, height=360)
    for c_, col, w_ in (("total", cs.C1, 2.8), ("comercial", cs.C7, 1.8), ("consumo", cs.C2, 1.8), ("vivienda", cs.C3, 1.8), ("micro", cs.C4, 1.4)):
        cs.linea(f8, xr, reales[c_], tx(f"lbl_{c_}", L), col, width=w_, lang=L)
    f8.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    cs.ejes(f8, y="Crecimiento real anual" if L == "es" else "Annual real growth")
    g8 = cs.bloque_grafico(tx("g_cart", L), cs.fig_html(f8, {}, "g-ts-cartera"), tx("h_cart", L))
    tot_parts = sum(cm[c_] for c_ in ("comercial", "consumo", "vivienda", "micro"))
    sh = pd.DataFrame({c_: cm[c_] / tot_parts * 100 for c_ in ("comercial", "consumo", "vivienda", "micro")}).loc["2008":].dropna()
    xs = sh.index + pd.offsets.MonthEnd(0)
    f9 = cs.base(L, height=360)
    for c_, col in (("comercial", cs.C7), ("consumo", cs.C2), ("vivienda", cs.C3), ("micro", cs.C4)):
        f9.add_trace(go.Scatter(x=list(xs), y=sh[c_].round(1).tolist(), mode="lines", stackgroup="uno", name=tx(f"lbl_{c_}", L),
                                line=dict(color=col, width=0.5), fillcolor=col, hovertemplate=tx(f"lbl_{c_}", L) + ": %{y:.1f}%<extra></extra>"))
    f9.update_yaxes(range=[0, 100])
    cs.ejes(f9, y="% del saldo de crédito" if L == "es" else "% of outstanding credit")
    g9 = cs.bloque_grafico(tx("g_comp", L), cs.fig_html(f9, {"noy": True}, "g-ts-composicion"), tx("h_comp", L))
    ur = reales.dropna().iloc[-1]
    r5 = tx("r_cartera", L).format(s=num(float(cart.iloc[-1]) / 1000, 0, L), g=pct(ur["total"], 1, True), c=pct(ur["consumo"], 1, True),
                                   co=pct(ur["comercial"], 1, True), v=pct(ur["vivienda"], 1, True), m=pct(ur["micro"], 1, True),
                                   pc=pct(sh["comercial"].iloc[-1], 0), pq=pct(sh["consumo"].iloc[-1], 0))
    s_ca = seccion("ts-cartera", tx("s_cartera", L), r5, f'<div class="grid">{g8}{g9}</div>')

    # ------------------------------------------------ liquidez
    lq = pd.DataFrame({"r1": T["repo_1d"], "rp": T["repo_plazo"], "con": T["contraccion"]}).fillna(0).resample("MS").mean().loc["2012":] / 1000
    xl = lq.index + pd.offsets.MonthEnd(0)
    f10 = cs.base(L, height=360, suffix="")
    for col, lbl, color, sg in (("r1", "lbl_r1", cs.C1, 1), ("rp", "lbl_rp", cs.C7, 1), ("con", "lbl_con", cs.C4, -1)):
        f10.add_trace(go.Bar(x=list(xl), y=(sg * lq[col]).round(2).tolist(), name=tx(lbl, L), marker=dict(color=color, line=dict(width=0)),
                             hovertemplate=tx(lbl, L) + ": %{y:.1f} " + bill + "<extra></extra>"))
    f10.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    f10.update_layout(barmode="relative", bargap=0.05)
    cs.ejes(f10, y="Billones de pesos" if L == "es" else "COP trillion")
    g10 = cs.bloque_grafico(tx("g_liq", L), cs.fig_html(f10, {}, "g-ts-liquidez"), tx("h_liq", L), ancho=True)
    ul = lq.iloc[-1]
    r6 = tx("r_liq", L).format(e=num(float(ul["r1"] + ul["rp"]), 1, L), c=num(float(ul["con"]), 1, L))
    s_lq = seccion("ts-liquidez", tx("s_liquidez", L), r6, f'<div class="grid">{g10}</div>')

    items = "".join(f'<li><span class="ref">{ref}</span><span class="ref-u">{es if L == "es" else en}</span></li>' for ref, es, en in LITERATURA)
    s_lit = (f'<section id="ts-literatura" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{tx("s_lit", L)}</h2></div>'
             f'<ol class="refs">{items}</ol></section>')
    return antes, s_cic + s_tr + s_cr + s_ibr + s_ca + s_lq + s_lit


# ====================================================================== ventana explicativa: la tasa del Banco
def ventana_tpm(tpm, ibr_on, T, L, num, fecha) -> str:
    es = L == "es"
    Tt = (lambda a, b: a if es else b)
    pct = lambda v: num(float(v), 2, L, False, "%")
    pasos = [(Tt("Junta Directiva", "Board"), Tt(f"Fija la tasa de política: hoy {pct(tpm.iloc[-1])}.", f"Sets the policy rate: today {pct(tpm.iloc[-1])}.")),
             (Tt("Mercado a un día", "Overnight market"), Tt(f"Con repos de expansión y depósitos de contracción, el Banco lleva el IBR a un día a ese nivel: hoy {pct(ibr_on.iloc[-1])}.",
                                                            f"With expansion repos and contraction deposits, the Bank brings the overnight IBR to that level: today {pct(ibr_on.iloc[-1])}.")),
             (Tt("Plazos más largos", "Longer tenors"), Tt(f"Cambian el IBR a 1, 3, 6 y 12 meses (3 meses: {pct(T['ibr_3m'].iloc[-1])}) y las tasas de los TES.",
                                                          f"The 1-, 3-, 6- and 12-month IBR change (3 months: {pct(T['ibr_3m'].iloc[-1])}) as do TES yields.")),
             (Tt("Ahorro y crédito", "Savings and loans"), Tt(f"Los bancos ajustan lo que pagan por los CDT ({pct(T['cdt_90'].iloc[-1])} a 90 días) y lo que cobran por los créditos ({pct(T['col_total'].iloc[-1])} en promedio).",
                                                              f"Banks adjust what they pay on CDs ({pct(T['cdt_90'].iloc[-1])} at 90 days) and charge on loans ({pct(T['col_total'].iloc[-1])} on average).")),
             (Tt("Gasto, dólar y expectativas", "Spending, the dollar and expectations"), Tt("Más caro el crédito, menos gasto e inversión; además se mueven la tasa de cambio, el precio de los activos y lo que la gente espera de la inflación.",
                                                                                             "Costlier credit means less spending and investment; the exchange rate, asset prices and inflation expectations also move.")),
             (Tt("Inflación", "Inflation"), Tt("Con rezago, la menor demanda baja la inflación hacia la meta de 3%.", "With a lag, weaker demand brings inflation towards the 3% target."))]
    escalera = "".join(f'<li style="--i:{i}"><b>{i + 1}</b><span>{a}</span><em>{b}</em></li>' for i, (a, b) in enumerate(pasos))
    defs = [
        (Tt("Tasa de política monetaria", "Monetary policy rate"),
         Tt("Es la tasa de interés mínima que el Banco de la República cobra a las entidades financieras por los préstamos que les hace mediante las operaciones de mercado abierto (OMA) en las subastas de expansión monetaria a un día hábil. La define la Junta Directiva y rige desde el día hábil siguiente a la sesión.",
            "It is the minimum interest rate the Banco de la República charges financial institutions on loans made through open market operations (OMOs) in one-business-day monetary expansion auctions. The Board sets it and it applies from the business day after the meeting.")),
        ("IBR", Tt("Indicador Bancario de Referencia: tasa de corto plazo en pesos que refleja el precio al que los bancos están dispuestos a ofrecer o captar recursos en el mercado monetario. Existe desde 2008 a un día; a 1 y 3 meses desde 2012, a 6 meses desde 2016 y a 12 meses desde 2022.",
                   "Reference Banking Indicator: short-term peso rate reflecting the price at which banks are willing to lend or borrow in the money market. Overnight since 2008; 1 and 3 months since 2012, 6 months since 2016 and 12 months since 2022.")),
        ("TIB", Tt("Tasa interbancaria a un día: promedio ponderado por monto de los préstamos sin garantía entre entidades financieras; refleja la liquidez y el riesgo de crédito entre ellas.",
                   "Overnight interbank rate: amount-weighted average of unsecured loans between financial institutions; it reflects liquidity and credit risk among them.")),
        (Tt("DTF y CDT", "DTF and CDs"), Tt("Tasas de captación: lo que los bancos pagan por los certificados de depósito a término. La DTF es el promedio ponderado semanal de los CDT a 90 días de bancos, corporaciones financieras y compañías de financiamiento.",
                                          "Deposit rates: what banks pay on term certificates of deposit. The DTF is the weekly weighted average of 90-day CDs of banks, financial corporations and finance companies.")),
        (Tt("Tasas de colocación", "Lending rates"), Tt("Tasas de los créditos nuevos por modalidad (consumo, comercial ordinario, preferencial y tesorería, vivienda), calculadas por el Banco con el formato 088 que las entidades reportan a la Superintendencia Financiera.",
                                                        "Rates on new loans by type (consumer, ordinary commercial, preferential and treasury, housing), computed by the Bank from Form 088 reported by institutions to the Financial Superintendence.")),
    ]
    dl = "".join(f"<li><b>{a}.</b> {b}</li>" for a, b in defs)
    return f"""<dialog class="explica" id="exp-tpm" aria-labelledby="exp-tpm-t">
<div class="ex-cab"><p class="ex-k">{Tt("Para entender", "To understand")} · Banco de la República</p><h2 id="exp-tpm-t">{Tt("¿Cómo funciona la tasa del Banco y cómo llega a la economía?", "How does the policy rate work and reach the economy?")}</h2>
<button type="button" class="ex-x" data-cerrar aria-label="{Tt("Cerrar", "Close")}">✕</button></div>
<div class="ex-cuerpo">
<p class="ex-lede">{Tt("El Banco de la República usa la tasa de política monetaria para que la inflación converja a su meta de 3%. La tasa no actúa de inmediato: pasa por una cadena de mercados, cada uno con su ritmo.",
 "The Banco de la República uses the monetary policy rate to bring inflation to its 3% target. The rate does not act immediately: it passes through a chain of markets, each with its own pace.")}</p>
<h3>{Tt("1. La cadena de transmisión (con los datos de hoy)", "1. The transmission chain (with today's data)")}</h3>
<ol class="ex-escalera ex-cadena">{escalera}</ol>
<h3>{Tt("2. Qué mide cada tasa", "2. What each rate measures")}</h3>
<ul class="ex-lista">{dl}</ul>
<h3>{Tt("3. Tasa real y tasa neutral", "3. Real and neutral rate")}</h3>
<p>{Tt("La tasa real ex ante es la tasa del Banco menos la inflación que el mercado espera para el próximo año. Si está por encima de la tasa real neutral (la que ni frena ni estimula la economía), la política es restrictiva; por debajo, expansiva. La neutral no se observa: se estima, por eso se muestra como un rango.",
 "The ex-ante real rate is the policy rate minus the inflation the market expects for the next year. If it is above the neutral real rate (neither slowing nor stimulating the economy), policy is restrictive; below it, expansionary. The neutral rate is not observed: it is estimated, so it is shown as a range.")}</p>
<h3>{Tt("Fuentes oficiales", "Official sources")}</h3>
<ul class="ex-fuentes">
<li><a href="https://suameca.banrep.gov.co/graficador-series/" target="_blank" rel="noopener">Banco de la República — {Tt("graficador de series: definiciones de la tasa de política, IBR, TIB, DTF, CDT y colocación", "series grapher: definitions of the policy rate, IBR, TIB, DTF, CD and lending rates")}</a></li>
<li>Banco de la República. <i>{Tt("Mecanismos de transmisión de la política monetaria en Colombia", "Monetary policy transmission mechanisms in Colombia")}</i>.</li>
<li>Chavarro, X. et al. (2015). <i>Borradores de Economía</i> 874, Banco de la República.</li>
</ul>
</div></dialog>"""
