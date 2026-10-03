"""Pagina del ciclo ampliada (v12.3): lectura en cinco medidas, consenso de metodos, ciclo
mensual, motores, amplitud sectorial, ritmo, historia de expansiones y recesiones, empleo y Okun.

Todo describe el presente con datos observados (DANE, Banco de la Republica); nada proyecta.
Las figuras usan la paleta de origen de construir.py: app.js las adapta al tema claro u oscuro.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from colombiamacro import analitica as am

TX = {
    # --- secciones
    "s_lectura": ("La economía en cinco medidas", "The economy in five measures"),
    "s_medicion": ("¿Qué tan seguros estamos de la fase?", "How sure are we about the phase?"),
    "s_motores": ("¿Qué mueve el ciclo?", "What is driving the cycle?"),
    "s_ritmo": ("¿Qué tan fuerte y qué tan larga es esta expansión?", "How strong and how long is this expansion?"),
    "s_empleo": ("¿Cómo se refleja el ciclo en el empleo?", "How does the cycle show up in jobs?"),
    "nuevo": ("Nuevo", "New"),
    # --- lecturas
    "l_trim": ("Fase trimestral", "Quarterly phase"), "l_mes": ("Fase mensual", "Monthly phase"),
    "l_cons": ("Consenso de métodos", "Method consensus"), "l_amp": ("Amplitud", "Breadth"),
    "l_emp": ("Empleo frente al ciclo", "Jobs vs the cycle"),
    "l_trim_d": ("Brecha {g} · {dir}", "Gap {g} · {dir}"),
    "sube": ("subiendo", "rising"), "baja": ("bajando", "falling"),
    "l_mes_d": ("Brecha del ISE {g} en {m}", "ISE gap {g} in {m}"),
    "de_5": ("{n} de 5", "{n} of 5"), "de_12": ("{n} de 12", "{n} of 12"),
    "l_cons_d": ("métodos ven la economía sobre su capacidad · mediana {m}", "methods see output above capacity · median {m}"),
    "l_amp_d_estrecha": ("sectores sobre su tendencia: expansión concentrada", "sectors above trend: narrow expansion"),
    "l_amp_d_amplia": ("sectores sobre su tendencia: expansión generalizada", "sectors above trend: broad-based expansion"),
    "l_emp_d_bajo": ("desempleo por debajo de su tendencia", "unemployment below its trend"),
    "l_emp_d_alto": ("desempleo por encima de su tendencia", "unemployment above its trend"),
    "rib_t": ("Fase de cada trimestre desde {a}", "Phase of each quarter since {a}"),
    "rib_h": ("Cada casilla es un trimestre, del más antiguo (izquierda) al más reciente (derecha). Pase el cursor para ver el trimestre y su brecha.",
              "Each cell is a quarter, oldest (left) to latest (right). Hover to see the quarter and its gap."),
    # --- respuestas (Lo clave)
    "r_lectura": ("{n} de los 5 métodos ven la economía por encima de su capacidad (mediana {m}). "
                  "El indicador mensual (ISE) la ubica en {fm} en {mes}. "
                  "Pero la expansión es estrecha: solo {k} de 12 sectores producen sobre su tendencia. "
                  "{s1} aporta {c1} de los {ct} puntos que suman los 12 sectores en {q}.",
                  "{n} of 5 methods see output above capacity (median {m}). "
                  "The monthly indicator (ISE) puts the economy in {fm} in {mes}. "
                  "But the expansion is narrow: only {k} of 12 sectors produce above trend. "
                  "{s1} contributes {c1} of the {ct} points added by the 12 sectors in {q}."),
    "r_medicion": ("Cinco métodos estándar miden la distancia entre lo que produce la economía y su capacidad. Hoy van de {lo} a {hi}; la mediana es {m}. "
                   "Cuando los métodos discrepan mucho, la fase es incierta y conviene esperar el siguiente dato. "
                   "La versión mensual, con el ISE, se actualiza 45 días antes que el PIB.",
                   "Five standard methods measure the distance between what the economy produces and its capacity. Today they range from {lo} to {hi}; the median is {m}. "
                   "When methods disagree widely the phase is uncertain and it is worth waiting for the next release. "
                   "The monthly version, built on the ISE, updates 45 days before GDP."),
    "r_motores": ("Por grandes ramas del ISE, {r1} están {e1} su tendencia ({g1}). "
                  "En el PIB de {q}, {s1} aporta {c1} puntos y {s2} {c2}; {neg}. "
                  "Solo {k} de 12 sectores producen sobre su tendencia.",
                  "By broad ISE branch, {r1} are {e1} trend ({g1}). "
                  "In {q} GDP, {s1} contributes {c1} points and {s2} {c2}; {neg}. "
                  "Only {k} of 12 sectors produce above trend."),
    "r_neg_si": ("{lista} restan", "{lista} subtract"), "r_neg_no": ("ningún sector resta", "no sector subtracts"),
    "encima": ("por encima de", "above"), "debajo": ("por debajo de", "below"),
    "r_ritmo": ("La actividad crece {y} frente a hace un año y a un ritmo anualizado de {r} en los últimos tres meses: {acel}. "
                "La expansión actual empezó en {ini} y lleva {meses} meses; la actividad acumula {acum} desde el valle.",
                "Activity is growing {y} year on year and at an annualised {r} over the last three months: {acel}. "
                "The current expansion began in {ini} and is {meses} months old; activity is up {acum} since the trough."),
    "acelera": ("el ritmo reciente es mayor que el anual (acelera)", "the recent pace exceeds the annual one (accelerating)"),
    "frena": ("el ritmo reciente es menor que el anual (se modera)", "the recent pace is below the annual one (moderating)"),
    "r_empleo": ("En 12 meses la tasa de desempleo cambió {du} y la de ocupación {do}. "
                 "Según la ley de Okun, por cada punto de brecha del producto el desempleo baja apenas {b} pp (correlación {c}): "
                 "en Colombia el empleo responde poco al ciclo porque la informalidad absorbe los choques.",
                 "Over 12 months the unemployment rate changed {du} and the employment rate {do}. "
                 "Under Okun's law, each point of output gap lowers unemployment by only {b} pp (correlation {c}): "
                 "in Colombia jobs respond little to the cycle because informality absorbs shocks."),
    # --- graficos
    "g_consenso": ("Brecha del producto según cinco métodos ({q})", "Output gap by five methods ({q})"),
    "h_consenso": ("Cada punto es un método. La línea punteada es la mediana; a la derecha del cero la economía produce por encima de su capacidad. Si los puntos están lejos entre sí, la lectura es incierta.",
                   "Each dot is a method. The vertical tick is the median; right of zero the economy produces above capacity. Dots far apart mean an uncertain reading."),
    "g_mensual": ("Ciclo mensual: brecha del ISE", "Monthly cycle: ISE gap"),
    "h_mensual": ("Cada barra es un mes: cuánto se aleja la actividad de su tendencia, coloreada por fase. Franjas grises: recesiones. 2020 se recorta en −8% para no aplastar la escala.",
                  "Each bar is a month: how far activity is from trend, coloured by phase. Grey bands: recessions. 2020 is capped at −8% so the scale stays readable."),
    "g_motores": ("Las tres grandes ramas frente a su tendencia ({m})", "The three broad branches vs their trend ({m})"),
    "h_motores": ("Primarias: agro y minería. Secundarias: industria, construcción y servicios públicos. Terciarias: comercio, servicios y Gobierno. Azul: sobre su tendencia; naranja: debajo.",
                  "Primary: farming and mining. Secondary: manufacturing, construction and utilities. Tertiary: trade, services and government. Blue: above trend; orange: below."),
    "g_aportes": ("¿Quién aporta el crecimiento? Puntos del PIB por sector ({q})", "Who delivers growth? GDP points by sector ({q})"),
    "h_aportes": ("Cada barra son los puntos porcentuales que el sector suma (o resta) al crecimiento anual del PIB. La suma de todas es el crecimiento total.",
                  "Each bar is the percentage points the sector adds to (or subtracts from) annual GDP growth. They add up to total growth."),
    "g_amplitud": ("¿Cuántos sectores están por encima de su tendencia? ({q})", "How many sectors are above trend? ({q})"),
    "h_amplitud": ("Verde: el sector produce por encima de su propia tendencia; naranja: por debajo. Más de 6 en verde indica una expansión generalizada.",
                   "Green: the sector produces above its own trend; orange: below. More than 6 green means a broad-based expansion."),
    "g_ritmo": ("Ritmo de la actividad: anual frente a los últimos 3 meses", "Activity pace: annual vs last 3 months"),
    "h_ritmo": ("Línea azul: crecimiento frente al mismo mes del año anterior. Línea naranja: crecimiento de los últimos 3 meses frente a los 3 anteriores, anualizado. Si la naranja va por encima, la economía acelera.",
                "Blue: growth versus the same month a year earlier. Orange: last 3 months versus the previous 3, annualised. Orange above blue means acceleration."),
    "naranja_lbl": ("Últimos 3 meses (anualizado)", "Last 3 months (annualised)"), "azul_lbl": ("Anual", "Annual"),
    "t_expansiones": ("Expansiones y recesiones desde 2008", "Expansions and recessions since 2008"),
    "h_expansiones": ("Fechas de picos y valles del nivel del ISE (promedio de 3 meses), con la regla de Bry y Boschan. Las recesiones sombrean los gráficos del sitio.",
                      "Peak and trough dates of the ISE level (3-month average), using the Bry-Boschan rule. Recessions shade the site's charts."),
    "col_tipo": ("Fase", "Phase"), "col_desde": ("Desde", "From"), "col_hasta": ("Hasta", "To"),
    "col_meses": ("Meses", "Months"), "col_var": ("Variación del ISE", "ISE change"),
    "expansion": ("Expansión", "Expansion"), "recesion": ("Recesión", "Recession"), "en_curso": ("en curso", "ongoing"),
    "g_empleo": ("Cambio en 12 meses: desempleo y ocupación", "12-month change: unemployment and employment"),
    "h_empleo": ("Puntos porcentuales frente al mismo mes del año anterior (promedio de 3 meses). Un mercado laboral que mejora muestra la línea de ocupación arriba y la de desempleo abajo.",
                 "Percentage points versus the same month a year earlier (3-month average). An improving labour market shows employment up and unemployment down."),
    "lbl_td": ("Tasa de desempleo", "Unemployment rate"), "lbl_to": ("Tasa de ocupación", "Employment rate"),
    "g_okun": ("Ley de Okun: producción y empleo se mueven juntos, pero poco", "Okun's law: output and jobs move together, but little"),
    "h_okun": ("Azul: brecha del producto (%). Verde: cuánto está el desempleo por debajo de su tendencia (pp, eje invertido para que ambas suban juntas). Si la economía crece por encima de su capacidad, el desempleo debería caer bajo su tendencia.",
               "Blue: output gap (%). Green: how far unemployment is below its trend (pp, inverted so both rise together). When output is above capacity, unemployment should fall below trend."),
    "lbl_brecha": ("Brecha del producto", "Output gap"), "lbl_u": ("Desempleo bajo su tendencia", "Unemployment below trend"),
}


def tx(k, L):
    return TX[k][0 if L == "es" else 1]


def _rec_sombras(fig, recesiones):
    for r in recesiones:
        fig.add_vrect(x0=r["desde"], x1=r["hasta"] + pd.offsets.MonthEnd(0), fillcolor="rgba(82,81,78,0.13)",
                      line_width=0, layer="below")


def construir_ciclo(d, s, L):
    """Devuelve (html_antes_del_reloj, html_despues_del_reloj)."""
    from colombiamacro.sitio import construir as cs
    num, fecha, esc = cs.num, cs.fecha, cs.esc
    cs.LANG_ACTUAL[0] = L        # el modulo puede cargarse dos veces (python -m): fija el idioma de las fichas
    FASES = am.FASES
    nf = lambda k: FASES[k][0 if L == "es" else 1].lower() if k in FASES else "—"

    # ------------------------------------------------ datos
    cons = am.brechas_consenso(d.pib, d.ciclo).dropna(subset=["mediana"])
    uc = cons.iloc[-1]
    q = fecha(uc["fecha"], "q", L)
    cm = am.ciclo_mensual(d.ise).dropna(subset=["brecha"])
    um = cm.iloc[-1]
    bs = am.brecha_sectores(d.sectores) if d.sectores is not None else pd.DataFrame()
    bsu = bs.iloc[-1].dropna().sort_values() if not bs.empty else pd.Series(dtype=float)
    k_sobre = int((bsu > 0).sum())
    ise_nivel = d.ise.set_index("fecha")["ise_sa"]
    giros = am.giros_clasicos(ise_nivel)
    recesiones, expansiones = am.episodios(ise_nivel, giros)
    ciclo = d.ciclo.dropna(subset=["fase"])
    uq = ciclo.iloc[-1]
    sec_u = d.sectores[d.sectores["fecha"] == d.sectores["fecha"].max()].sort_values("contribucion", ascending=False)
    ok = am.okun(cons.set_index("fecha")["brecha_hp_dos_colas"], d.laboral.set_index("fecha")["td_sa"])

    # ------------------------------------------------ 1. lecturas + cinta de fases
    def lec(k, v, dsc, tono, href=None):
        tag = "a" if href else "div"
        h = f' href="{href}"' if href else ""
        return (f'<{tag} class="lec {tono}"{h}><span class="lec-k">{k}</span><b class="lec-v">{v}</b>'
                f'<span class="lec-d">{dsc}</span></{tag}>')

    tono_f = {"expansion": "ok", "recuperacion": "ok", "desaceleracion": "warn", "contraccion": "bad"}
    lb = ok["serie"].iloc[-1]
    lecturas = "".join([
        lec(f'{tx("l_trim", L)} · {q}', FASES[uq["fase"]][0 if L == "es" else 1],
            tx("l_trim_d", L).format(g=num(uq["brecha_hp_tiempo_real"], 1, L, True, "%"), dir=tx("sube" if uq["delta_brecha"] >= 0 else "baja", L)),
            tono_f.get(uq["fase"], "neutral"), "#ciclo"),
        lec(f'{tx("l_mes", L)} · {fecha(um["fecha"], "m", L)}', FASES[um["fase"]][0 if L == "es" else 1] if um["fase"] in FASES else "—",
            tx("l_mes_d", L).format(g=num(um["brecha"], 1, L, True, "%"), m=fecha(um["fecha"], "m", L)), tono_f.get(um["fase"], "neutral"), "#ciclo-medicion"),
        lec(tx("l_cons", L), tx("de_5", L).format(n=int(uc["positivos"])),
            tx("l_cons_d", L).format(m=num(uc["mediana"], 1, L, True, "%")), "ok" if uc["positivos"] >= 3 else "warn", "#ciclo-medicion"),
        lec(tx("l_amp", L), tx("de_12", L).format(n=k_sobre),
            tx("l_amp_d_amplia" if k_sobre > 6 else "l_amp_d_estrecha", L), "ok" if k_sobre > 6 else "warn", "#ciclo-motores"),
        lec(tx("l_emp", L), num(lb["brecha_u"], 1, L, True, " pp"),
            tx("l_emp_d_bajo" if lb["brecha_u"] < 0 else "l_emp_d_alto", L), "ok" if lb["brecha_u"] < 0 else "warn", "#ciclo-empleo"),
    ])
    celdas = "".join(
        f'<span class="rib-c ph-{r.fase}" title="{fecha(r.fecha, "q", L)} · {esc(FASES[r.fase][0 if L == "es" else 1])} · {num(r.brecha_hp_tiempo_real, 1, L, True, "%")}"></span>'
        for r in ciclo.itertuples())
    anos = sorted({f.year for f in ciclo["fecha"]})
    marcas = "".join(f'<span style="left:{100 * i / len(ciclo):.2f}%">{a}</span>'
                     for i, f in enumerate(ciclo["fecha"]) for a in [f.year] if f.month == 1 and a % 2 == 1)
    leyenda = "".join(f'<span class="ph"><i class="ph-{k}"></i>{esc(v[0 if L == "es" else 1])}</span>' for k, v in FASES.items())
    cinta = (f'<div class="ribbon"><div class="rib-h"><b>{tx("rib_t", L).format(a=ciclo["fecha"].iloc[0].year)}</b><span class="phases">{leyenda}</span></div>'
             f'<div class="rib-row" role="img" aria-label="{tx("rib_t", L).format(a=ciclo["fecha"].iloc[0].year)}">{celdas}</div><div class="rib-x">{marcas}</div>'
             f'<p class="how"><span>?</span>{tx("rib_h", L)}</p></div>')
    s1 = sec_u.iloc[0]
    resp1 = tx("r_lectura", L).format(
        n=int(uc["positivos"]), m=num(uc["mediana"], 1, L, True, "%"), fm=nf(um["fase"]), mes=fecha(um["fecha"], "m", L),
        k=k_sobre, s1=s1["sector"], c1=num(s1["contribucion"], 1, L), ct=num(sec_u["contribucion"].sum(), 1, L), q=fecha(sec_u["fecha"].iloc[0], "q", L))
    antes = (f'<section id="ciclo-lectura" class="section"><div class="sec-head"><span class="sec-num">0</span>'
             f'<h2>{tx("s_lectura", L)}</h2></div>{cs.respuesta_html(resp1, L)}<div class="lecturas">{lecturas}</div>{cinta}</section>')

    # ------------------------------------------------ 2. medicion: consenso + mensual
    metodos = list(am.NOMBRES_METODOS)
    vals = [float(uc[m]) for m in metodos]
    nombres = [am.NOMBRES_METODOS[m][0 if L == "es" else 1] for m in metodos]
    f1 = cs.base(L, height=300, fecha_x=False)
    lim = max(2.0, max(abs(v) for v in vals) * 1.3)
    f1.add_vrect(x0=0, x1=lim, fillcolor="rgba(27,175,122,0.12)", line_width=0, layer="below")
    f1.add_vline(x=0, line=dict(color=cs.INK2, width=1))
    f1.add_vline(x=float(uc["mediana"]), line=dict(color=cs.INK, width=2, dash="dot"))
    f1.add_annotation(x=float(uc["mediana"]), y=1.02, yref="paper", showarrow=False, yanchor="bottom",
                      text=("Mediana " if L == "es" else "Median ") + num(uc["mediana"], 1, L, True, "%"), font=dict(size=11.5, color=cs.INK))
    orden = list(np.argsort(vals))
    ys = [nombres[i] for i in orden]
    xs = [vals[i] for i in orden]
    f1.add_trace(go.Bar(y=ys, x=xs, orientation="h", width=0.08, marker=dict(color=cs.RULE), hoverinfo="skip", showlegend=False))
    f1.add_trace(go.Scatter(y=ys, x=xs, mode="markers+text", marker=dict(size=15, color=[cs.C1 if v >= 0 else cs.C2 for v in xs],
                            line=dict(color="#fff", width=2)), text=[num(v, 1, L, True, "%") for v in xs],
                            textposition=["middle left" if v < 0 else "middle right" for v in xs], textfont=dict(size=12, color=cs.INK),
                            cliponaxis=False, showlegend=False, hovertemplate="%{y}: %{x:.2f}%<extra></extra>"))
    f1.update_xaxes(range=[-lim, lim], ticksuffix="%", showgrid=True, gridcolor=cs.GRID, zeroline=False)
    f1.update_yaxes(ticksuffix="", tickfont=dict(size=12.5, color=cs.INK2))
    f1.update_layout(hovermode="closest", margin=dict(l=6, r=16, t=26, b=6))
    g_cons = cs.bloque_grafico(tx("g_consenso", L).format(q=q), cs.fig_html(f1, {"notime": True}, "g-consenso"), tx("h_consenso", L))

    f2 = cs.base(L, height=330)
    _rec_sombras(f2, recesiones)
    colores = {k: v[2] for k, v in FASES.items()}
    xm = list(cm["fecha"] + pd.offsets.MonthEnd(0))
    f2.add_trace(go.Bar(x=xm, y=cm["brecha"].clip(lower=-8).round(2), showlegend=False,
                        marker=dict(color=[colores.get(p, cs.GRAY) for p in cm["fase"]], line=dict(width=0)),
                        customdata=[[fecha(f_, "m", L), FASES[p][0 if L == "es" else 1] if p in FASES else "—", num(g, 1, L, True, "%")]
                                    for f_, p, g in zip(cm["fecha"], cm["fase"], cm["brecha"])],
                        hovertemplate="%{customdata[0]} · %{customdata[1]}: %{customdata[2]}<extra></extra>"))
    f2.update_layout(bargap=0.05, hovermode="closest")
    f2.update_yaxes(range=[-8.5, max(5.0, float(cm["brecha"].max()) + 0.5)])
    g_mens = cs.bloque_grafico(tx("g_mensual", L), cs.fig_html(f2, {"noy": True}, "g-ciclo-mensual"), tx("h_mensual", L))
    resp2 = tx("r_medicion", L).format(lo=num(uc["minimo"], 1, L, True, "%"), hi=num(uc["maximo"], 1, L, True, "%"), m=num(uc["mediana"], 1, L, True, "%"))
    med = (f'<section id="ciclo-medicion" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{tx("s_medicion", L)}</h2></div>'
           f'{cs.respuesta_html(resp2, L)}<div class="grid">{g_cons}{g_mens}</div></section>')

    # ------------------------------------------------ 3. motores: ramas, aportes, amplitud
    ramas = [("primarias", ("Primarias", "Primary")), ("secundarias", ("Secundarias", "Secondary")), ("terciarias", ("Terciarias", "Tertiary"))]
    rv = [(n[0 if L == "es" else 1], float(um.get(f"brecha_{r}", np.nan)), float(um.get(f"yoy_{r}", np.nan))) for r, n in ramas]
    f3 = cs.base(L, height=230, fecha_x=False)
    f3.add_trace(go.Bar(y=[r[0] for r in rv][::-1], x=[round(r[1], 2) for r in rv][::-1], orientation="h", showlegend=False,
                        marker=dict(color=[cs.C1 if r[1] >= 0 else cs.C2 for r in rv][::-1], line=dict(width=0)),
                        text=[num(r[1], 1, L, True, "%") for r in rv][::-1], textposition="outside", cliponaxis=False,
                        customdata=[num(r[2], 1, L, True, "%") for r in rv][::-1],
                        hovertemplate="%{y}: %{x:.1f}%<br>" + ("Crecimiento anual" if L == "es" else "Annual growth") + ": %{customdata}<extra></extra>"))
    m3 = max(2.0, max(abs(r[1]) for r in rv) * 1.4)
    f3.add_vline(x=0, line=dict(color=cs.INK2, width=1))
    f3.update_xaxes(range=[-m3, m3], ticksuffix="%", showgrid=True, gridcolor=cs.GRID)
    f3.update_yaxes(ticksuffix="", tickfont=dict(size=13, color=cs.INK2))
    f3.update_layout(hovermode="closest", bargap=0.45)
    g_mot = cs.bloque_grafico(tx("g_motores", L).format(m=fecha(um["fecha"], "m", L)), cs.fig_html(f3, {"notime": True}, "g-motores"), tx("h_motores", L))

    su = sec_u.sort_values("contribucion")
    f4 = cs.base(L, height=380, fecha_x=False, suffix=" pp")
    f4.add_trace(go.Bar(y=list(su["sector"]), x=su["contribucion"].round(2), orientation="h", showlegend=False,
                        marker=dict(color=[cs.C1 if v >= 0 else cs.C2 for v in su["contribucion"]], line=dict(width=0)),
                        text=[num(v, 2, L, True) for v in su["contribucion"]], textposition="outside", cliponaxis=False,
                        customdata=[num(v, 1, L, True, "%") for v in su["yoy"]],
                        hovertemplate="%{y}: %{x:.2f} pp<br>" + ("Crecimiento anual" if L == "es" else "Annual growth") + ": %{customdata}<extra></extra>"))
    f4.add_vline(x=0, line=dict(color=cs.INK2, width=1))
    f4.update_xaxes(ticksuffix=" pp", showgrid=True, gridcolor=cs.GRID, range=[min(-0.3, su["contribucion"].min() * 1.4), su["contribucion"].max() * 1.25])
    f4.update_yaxes(ticksuffix="", tickfont=dict(size=12, color=cs.INK2))
    f4.update_layout(hovermode="closest", bargap=0.3)
    q_sec = fecha(sec_u["fecha"].iloc[0], "q", L)
    g_apo = cs.bloque_grafico(tx("g_aportes", L).format(q=q_sec), cs.fig_html(f4, {"notime": True}, "g-aportes"), tx("h_aportes", L))

    casillas = "".join(
        f'<div class="sq {"sq-up" if v > 0 else "sq-dn"}"><span class="sq-n">{esc(n)}</span><b class="sq-v">{num(v, 1, L, True, "%")}</b></div>'
        for n, v in bsu.sort_values(ascending=False).items())
    g_amp = (f'<figure class="chart wide" data-lupa="v-amplitud-sectores"><figcaption>{tx("g_amplitud", L).format(q=fecha(bs.index[-1], "q", L))}'
             f' <span class="amp-n">{tx("de_12", L).format(n=k_sobre)}</span></figcaption><div class="sq-grid">{casillas}</div>'
             f'<p class="how"><span>?</span>{tx("h_amplitud", L)}</p>{cs.pie_ficha("g-amplitud", L)}</figure>')
    r_top = sorted(rv, key=lambda r: -abs(r[1]))[0]
    neg = su[su["contribucion"] < 0]["sector"].tolist()
    resp3 = tx("r_motores", L).format(
        r1=r_top[0].lower() if L == "es" else r_top[0].lower(), e1=tx("encima" if r_top[1] >= 0 else "debajo", L), g1=num(r_top[1], 1, L, True, "%"),
        q=q_sec, s1=sec_u.iloc[0]["sector"], c1=num(sec_u.iloc[0]["contribucion"], 2, L), s2=sec_u.iloc[1]["sector"], c2=num(sec_u.iloc[1]["contribucion"], 2, L),
        neg=tx("r_neg_si", L).format(lista=", ".join(neg)) if neg else tx("r_neg_no", L), k=k_sobre)
    mot = (f'<section id="ciclo-motores" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{tx("s_motores", L)}</h2></div>'
           f'{cs.respuesta_html(resp3, L)}<div class="grid">{g_mot}{g_apo}{g_amp}</div></section>')

    # ------------------------------------------------ 4. ritmo + expansiones
    rt = cm.dropna(subset=["yoy", "ritmo_3m"])
    f5 = cs.base(L, height=330)
    _rec_sombras(f5, recesiones)
    xr = rt["fecha"] + pd.offsets.MonthEnd(0)
    cs.linea(f5, xr, rt["yoy"].clip(-15, 25), tx("azul_lbl", L), cs.C1, width=2.2, lang=L)
    cs.linea(f5, xr, rt["ritmo_3m"].clip(-15, 25), tx("naranja_lbl", L), cs.C2, width=1.5, lang=L)
    f5.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    g_rit = cs.bloque_grafico(tx("g_ritmo", L), cs.fig_html(f5, {}, "g-ritmo"), tx("h_ritmo", L))

    filas = []
    eventos = sorted([("e", e) for e in expansiones] + [("r", r) for r in recesiones], key=lambda z: z[1]["desde"], reverse=True)
    for tipo, e in eventos:
        nom = tx("expansion" if tipo == "e" else "recesion", L)
        hasta = tx("en_curso", L) if e["en_curso"] else fecha(e["hasta"], "m", L)
        filas.append(f"<tr class='{'tr-e' if tipo == 'e' else 'tr-r'}'><td><i class='dot {'ph-expansion' if tipo == 'e' else 'ph-contraccion'}'></i>{nom}</td>"
                     f"<td>{fecha(e['desde'], 'm', L)}</td><td>{hasta}</td><td class='n'>{e['meses']}</td>"
                     f"<td class='n'><span class='chg {'up' if e['variacion'] >= 0 else 'down'}'>{num(e['variacion'], 1, L, True, '%')}</span></td></tr>")
    head = "".join(f"<th>{tx(k, L)}</th>" for k in ("col_tipo", "col_desde", "col_hasta", "col_meses", "col_var"))
    g_exp = (f'<figure class="chart" data-lupa="v-fases-ciclo"><figcaption>{tx("t_expansiones", L)}</figcaption><div class="table-wrap plano"><table class="tbl">'
             f'<thead><tr>{head}</tr></thead><tbody>{"".join(filas)}</tbody></table></div>'
             f'<p class="how"><span>?</span>{tx("h_expansiones", L)}</p>{cs.pie_ficha("g-expansiones", L)}</figure>')
    ur = rt.iloc[-1]
    actual = expansiones[-1] if expansiones and expansiones[-1]["en_curso"] else None
    resp4 = tx("r_ritmo", L).format(
        y=num(ur["yoy"], 1, L, True, "%"), r=num(ur["ritmo_3m"], 1, L, True, "%"),
        acel=tx("acelera" if ur["ritmo_3m"] > ur["yoy"] else "frena", L),
        ini=fecha(actual["desde"], "m", L) if actual else "—", meses=actual["meses"] if actual else "—",
        acum=num(actual["variacion"], 1, L, True, "%") if actual else "—")
    rit = (f'<section id="ciclo-ritmo" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{tx("s_ritmo", L)}</h2></div>'
           f'{cs.respuesta_html(resp4, L)}<div class="grid">{g_rit}{g_exp}</div></section>')

    # ------------------------------------------------ 5. empleo y Okun
    lab = d.laboral.set_index("fecha").sort_index()
    td3, to3 = lab["td_sa"].rolling(3).mean(), lab["to_sa"].rolling(3).mean()
    dtd, dto = (td3 - td3.shift(12)).dropna(), (to3 - to3.shift(12)).dropna()
    f6 = cs.base(L, height=330, suffix=" pp")
    _rec_sombras(f6, recesiones)
    cs.linea(f6, dto.index + pd.offsets.MonthEnd(0), dto.clip(-6, 6), tx("lbl_to", L), cs.C3, width=2.0, suf=" pp", lang=L)
    cs.linea(f6, dtd.index + pd.offsets.MonthEnd(0), dtd.clip(-6, 6), tx("lbl_td", L), cs.C2, width=2.0, suf=" pp", lang=L)
    f6.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    g_emp = cs.bloque_grafico(tx("g_empleo", L), cs.fig_html(f6, {}, "g-empleo-ciclo"), tx("h_empleo", L))

    J = ok["serie"]
    f7 = cs.base(L, height=330, suffix="")
    xq = J.index + pd.offsets.QuarterEnd(0)
    cs.linea(f7, xq, J["brecha"].clip(-8, 8), tx("lbl_brecha", L) + " (%)", cs.C1, width=2.2, suf="%", lang=L)
    cs.linea(f7, xq, (-J["brecha_u"]).clip(-8, 8), tx("lbl_u", L) + " (pp)", cs.C3, width=2.0, suf=" pp", lang=L)
    f7.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    f7.update_yaxes(ticksuffix="")
    g_okun = cs.bloque_grafico(tx("g_okun", L), cs.fig_html(f7, {}, "g-okun"), tx("h_okun", L))
    resp5 = tx("r_empleo", L).format(du=num(dtd.iloc[-1], 1, L, True, " pp"), do=num(dto.iloc[-1], 1, L, True, " pp"),
                                     b=num(abs(ok["pendiente"]), 2, L), c=num(ok["correlacion"], 2, L))
    emp = (f'<section id="ciclo-empleo" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{tx("s_empleo", L)}</h2></div>'
           f'{cs.respuesta_html(resp5, L)}<div class="grid">{g_emp}{g_okun}</div></section>')

    return antes, med + mot + rit + emp
