"""Pagina de inflacion ampliada (v12.9): ocho medidas, aportes por division, bienes frente a servicios,
difusion entre las 188 subclases, inflacion por nivel de ingreso y por ciudad (23 ciudades).

Solo datos observados (DANE, IPC base 2018). Colores de origen; app.js los adapta al tema.
"""

from __future__ import annotations

import re

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from colombiamacro.config import DATA_DIR

TX = {
    "s_medidas": ("La inflación en ocho medidas", "Inflation in eight measures"),
    "s_aportes": ("¿Qué explica la inflación?", "What explains inflation?"),
    "s_bienes": ("¿Suben más los bienes o los servicios?", "Are goods or services rising faster?"),
    "s_difusion": ("¿Qué tan generalizada es la inflación?", "How widespread is inflation?"),
    "s_ingresos": ("¿Quién siente más la inflación?", "Who feels inflation most?"),
    "s_ciudades": ("Inflación en 23 ciudades", "Inflation in 23 cities"),
    "s_lit": ("Bases metodológicas y literatura", "Methodological basis and literature"),
    # lecturas
    "l_total": ("Inflación anual · {m}", "Annual inflation · {m}"), "l_total_d": ("meta 3% (rango 2%–4%) · mensual {v}", "target 3% (2%–4% range) · monthly {v}"),
    "l_serv": ("Servicios", "Services"), "l_serv_d": ("anual · hace un año {v}", "annual · a year ago {v}"),
    "l_bien": ("Bienes no durables", "Non-durable goods"), "l_dur": ("Bienes durables", "Durable goods"),
    "l_ener": ("Energéticos", "Energy"), "l_ener_d": ("gas, energía y combustibles · hace un año {v}", "gas, power and fuel · a year ago {v}"),
    "l_dif": ("Difusión", "Diffusion"), "l_dif_d": ("de 188 subclases suben más de 4% anual · {w} del gasto", "of 188 subclasses rise more than 4% a year · {w} of spending"),
    "l_ciu": ("Rango entre ciudades", "Range across cities"), "l_ciu_d": ("de {c1} ({v1}) a {c2} ({v2})", "from {c1} ({v1}) to {c2} ({v2})"),
    "l_ing": ("Hogares de ingresos altos − pobres", "High-income − poor households"), "l_ing_d": ("pobres {p} · ingresos altos {a}", "poor {p} · high income {a}"),
    # respuestas
    "r_medidas": ("La inflación anual es {t} en {m}, por encima del rango meta (2%–4%). "
                  "La presión está en los servicios ({s}), que dependen de salarios y arriendos, más que en los bienes ({b} los no durables y {d} los durables). "
                  "{dif} de las 188 subclases suben más de 4% al año: la inflación no es un problema de pocos precios.",
                  "Annual inflation is {t} in {m}, above the target range (2%–4%). "
                  "Pressure is in services ({s}), which depend on wages and rents, more than in goods ({b} for non-durables and {d} for durables). "
                  "{dif} of the 188 subclasses rise more than 4% a year: inflation is not a problem of a few prices."),
    "r_aportes": ("De los {t} puntos de inflación anual, {d1} aporta {c1}, {d2} {c2} y {d3} {c3}. "
                  "{d4} es la división que más sube ({v4}); {d5}, la que menos ({v5}).",
                  "Of the {t} points of annual inflation, {d1} contributes {c1}, {d2} {c2} and {d3} {c3}. "
                  "{d4} is the division rising fastest ({v4}); {d5}, the slowest ({v5})."),
    "r_bienes": ("Los servicios suben {s} en un año y los bienes no durables {b}; los durables cambian {d}. "
                 "Sin alimentos ni energéticos, la inflación es {c}: una medida de la presión de fondo que depende menos del clima y de los precios internacionales.",
                 "Services are up {s} over a year and non-durable goods {b}; durables change {d}. "
                 "Excluding food and energy, inflation is {c}: a measure of underlying pressure that depends less on weather and international prices."),
    "r_difusion": ("{dif} de las subclases suben más de 4% al año ({dw} del gasto de los hogares) y {dif6} más de 6%. "
                   "Las que más aportan a la inflación son {top}. Las que más la frenan: {bot}.",
                   "{dif} of subclasses rise more than 4% a year ({dw} of household spending) and {dif6} more than 6%. "
                   "The largest contributors to inflation are {top}. The biggest drags: {bot}."),
    "r_ingresos": ("La inflación de los hogares pobres es {p} y la de los hogares de ingresos altos {a}. "
                   "{txt}",
                   "Inflation for poor households is {p} and for high-income households {a}. "
                   "{txt}"),
    "ing_altos": ("La diferencia es de {x} pp: hoy la inflación golpea algo más a los hogares de ingresos altos, cuya canasta tiene más servicios.",
                  "The difference is {x} pp: today inflation hits high-income households somewhat harder, whose basket includes more services."),
    "ing_pobres": ("La diferencia es de {x} pp: hoy la inflación golpea más a los hogares pobres, cuya canasta tiene más alimentos.",
                   "The difference is {x} pp: today inflation hits poor households harder, whose basket includes more food."),
    "r_ciudades": ("La inflación anual va de {lo} en {c1} a {hi} en {c2}. {n} de 23 ciudades están por encima del total nacional ({t}). "
                   "En {cmax} la división que más sube es {dmax} ({vmax}).",
                   "Annual inflation ranges from {lo} in {c1} to {hi} in {c2}. {n} of 23 cities are above the national total ({t}). "
                   "In {cmax} the fastest-rising division is {dmax} ({vmax})."),
    # graficos
    "g_aportes": ("Aporte de cada división a la inflación anual ({m})", "Contribution of each division to annual inflation ({m})"),
    "h_aportes": ("Puntos porcentuales que cada división suma a la inflación anual; la suma es la inflación total. Entre paréntesis, su peso en la canasta.",
                  "Percentage points each division adds to annual inflation; they add up to total inflation. In brackets, its weight in the basket."),
    "g_divs": ("Inflación anual de cada división", "Annual inflation by division"),
    "h_divs": ("Variación anual de los precios de cada división de gasto. La franja verde es el rango meta del Banco de la República (2%–4%).",
               "Annual price change for each spending division. The green band is the Banco de la República target range (2%–4%)."),
    "g_bs": ("Inflación de servicios y de bienes", "Services and goods inflation"),
    "h_bs": ("Variación anual del IPC de cada tipo de bien según su durabilidad. Los servicios suelen moverse con salarios y arriendos; los durables, con el dólar.",
             "Annual CPI change by type of good according to durability. Services tend to move with wages and rents; durables, with the dollar."),
    "g_core": ("Energéticos frente a la inflación sin alimentos ni energéticos", "Energy versus inflation excluding food and energy"),
    "h_core": ("Variación anual. Los energéticos (gas, electricidad y combustibles) son volátiles; la inflación sin alimentos ni energéticos muestra la presión persistente.",
               "Annual change. Energy (gas, electricity and fuel) is volatile; inflation excluding food and energy shows persistent pressure."),
    "lbl_serv": ("Servicios", "Services"), "lbl_nd": ("No durables", "Non-durables"), "lbl_sd": ("Semidurables", "Semi-durables"),
    "lbl_dur": ("Durables", "Durables"), "lbl_ener": ("Energéticos", "Energy"), "lbl_core": ("Sin alimentos ni energéticos", "Excluding food and energy"),
    "g_hist": ("Distribución de la inflación anual entre 188 subclases ({m})", "Distribution of annual inflation across 188 subclasses ({m})"),
    "h_hist": ("Cada barra cuenta cuántas subclases de la canasta tienen una inflación anual en ese rango. La franja verde es el rango meta; a la derecha de 4% están las que lo superan.",
               "Each bar counts how many basket subclasses have annual inflation in that range. The green band is the target range; to the right of 4% are those above it."),
    "g_top": ("Las subclases que más suman y más restan", "The subclasses adding and subtracting most"),
    "h_top": ("Aporte a la inflación anual, en puntos porcentuales: las 8 que más suman y las 4 que más restan. Pase el cursor para ver su inflación anual.",
              "Contribution to annual inflation, in percentage points: the 8 adding most and the 4 subtracting most. Hover to see their annual inflation."),
    "g_ing": ("Inflación anual por nivel de ingreso del hogar", "Annual inflation by household income level"),
    "h_ing": ("El DANE calcula el IPC con la canasta de cada grupo de hogares (pobres, vulnerables, clase media e ingresos altos). La línea punteada es el total.",
              "DANE computes the CPI with each household group's basket (poor, vulnerable, middle class and high income). The dotted line is the total."),
    "ing": {"pobres": ("Pobres", "Poor"), "vulnerables": ("Vulnerables", "Vulnerable"), "media": ("Clase media", "Middle class"), "altos": ("Ingresos altos", "High income")},
    "g_ciu": ("Inflación anual por ciudad ({m})", "Annual inflation by city ({m})"),
    "h_ciu": ("Variación anual del IPC total en cada una de las 23 ciudades. La línea punteada es el total nacional.",
              "Annual change in total CPI in each of the 23 cities. The dotted line is the national total."),
    "g_mapa": ("¿Qué sube más en cada ciudad?", "What rises most in each city?"),
    "h_mapa": ("Inflación anual por ciudad y división de gasto. Más oscuro = sube más. Las ciudades van ordenadas por su inflación total.",
               "Annual inflation by city and spending division. Darker = rising faster. Cities are ordered by total inflation."),
}
DIV = {"alimentos": ("Alimentos", "Food"), "alcohol_tabaco": ("Alcohol y tabaco", "Alcohol and tobacco"), "vestuario": ("Ropa y calzado", "Clothing and footwear"),
       "vivienda": ("Vivienda y servicios públicos", "Housing and utilities"), "muebles": ("Muebles y hogar", "Furnishings and household"),
       "salud": ("Salud", "Health"), "transporte": ("Transporte", "Transport"), "comunicaciones": ("Comunicaciones", "Communications"),
       "recreacion": ("Recreación y cultura", "Recreation and culture"), "educacion": ("Educación", "Education"),
       "restaurantes": ("Restaurantes y hoteles", "Restaurants and hotels"), "diversos": ("Otros bienes y servicios", "Other goods and services")}
LITERATURA = [
    ("Bryan, M. F. y Cecchetti, S. G. (1994). Measuring Core Inflation. En N. G. Mankiw (ed.), <i>Monetary Policy</i>, 195–215. University of Chicago Press (NBER).",
     "Medidas de inflación de fondo que excluyen los precios más volátiles.", "Core inflation measures that exclude the most volatile prices."),
    ("Baumol, W. J. (1967). Macroeconomics of Unbalanced Growth: The Anatomy of Urban Crisis. <i>American Economic Review</i>, 57(3), 415–426.",
     "Por qué los servicios tienden a encarecerse más que los bienes.", "Why services tend to become more expensive than goods."),
    ("Cecchetti, S. G. (1997). Measuring Short-Run Inflation for Central Bankers. <i>Federal Reserve Bank of St. Louis Review</i>, 79(3), 143–155.",
     "Dispersión y difusión de los cambios de precios.", "Dispersion and diffusion of price changes."),
    ("Jaravel, X. (2021). Inflation Inequality: Measurement, Causes, and Policy Implications. <i>Annual Review of Economics</i>, 13, 599–629.",
     "Inflación distinta según el nivel de ingreso de los hogares.", "Different inflation by household income level."),
    ("DANE. Índice de Precios al Consumidor, base diciembre 2018: metodología y canasta (2019).",
     "Divisiones COICOP, ponderaciones, subclases, ciudades y niveles de ingreso.", "COICOP divisions, weights, subclasses, cities and income levels."),
]


def tx(k, L):
    return TX[k][0 if L == "es" else 1]


def cargar():
    arch = {k: f"ipc_{k}.csv" for k in ("divisiones", "ingresos", "ciudades", "subclases", "clasificaciones")}
    if not all((DATA_DIR / f).exists() for f in arch.values()):
        return None
    return {k: pd.read_csv(DATA_DIR / f, parse_dates=["fecha"], dtype={"codigo": str}) for k, f in arch.items()}


def construir_inflacion(d, L):
    """Devuelve (antes, despues)."""
    from colombiamacro.sitio import construir as cs
    num, fecha, esc = cs.num, cs.fecha, cs.esc
    cs.LANG_ACTUAL[0] = L
    k = 0 if L == "es" else 1
    pct = lambda v, dec=1, sg=False: num(float(v), dec, L, sg, "%")
    I = cargar()
    if I is None:
        return "", ""
    dv = I["divisiones"].set_index("division")
    tot = dv.loc["total"]
    m = fecha(I["divisiones"]["fecha"].iloc[0], "m", L)
    cl = I["clasificaciones"].pivot(index="fecha", columns="serie", values="indice").sort_index()
    ya = (cl / cl.shift(12) - 1) * 100
    ua, ha = ya.iloc[-1], ya.iloc[-13]
    sub = I["subclases"]
    dif = 100 * (sub["var_anual"] > 4).mean()
    dif6 = 100 * (sub["var_anual"] > 6).mean()
    sub_w = con_ponderaciones(sub)
    dif_w = (sub_w.loc[sub_w["var_anual"] > 4, "peso"].sum() / sub_w["peso"].sum() * 100) if sub_w["peso"].notna().any() else float("nan")
    q_btn = (f'<button type="button" class="ex-q" data-dialog="exp-canasta" aria-haspopup="dialog" '
             f'title="{"¿Qué son las 188 subclases?" if L == "es" else "What are the 188 subclasses?"}">?</button>')
    ci = I["ciudades"]
    ct = ci[(ci["division"] == "total") & (ci["ciudad"] != "Total")].set_index("ciudad")["var_anual"]
    ct23 = ct.drop("Otras Areas Urbanas", errors="ignore").sort_values()
    ing = I["ingresos"].set_index("grupo")["var_anual"]
    nom_c = lambda c: {"Bogotá, D.C.": "Bogotá", "Cartagena De Indias": "Cartagena"}.get(c, c)

    def seccion(sid, titulo, resp, cuerpo):
        return (f'<section id="{sid}" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{titulo}</h2></div>'
                f'{cs.respuesta_html(resp, L)}{cuerpo}</section>')

    def lec(kk, v, dsc, tono, href):
        return (f'<a class="lec {tono}" href="{href}"><span class="lec-k">{kk}</span><b class="lec-v">{v}</b>'
                f'<span class="lec-d">{dsc}</span></a>')

    meta = lambda v: "ok" if 2 <= v <= 4 else "warn"
    tiles = [
        lec(tx("l_total", L).format(m=m), pct(tot["var_anual"], 2), tx("l_total_d", L).format(v=pct(tot["var_mensual"], 2)), meta(tot["var_anual"]), "#precios"),
        lec(tx("l_serv", L), pct(ua["servicios"]), tx("l_serv_d", L).format(v=pct(ha["servicios"])), meta(ua["servicios"]), "#inf-bienes"),
        lec(tx("l_bien", L), pct(ua["no_durables"]), tx("l_serv_d", L).format(v=pct(ha["no_durables"])), meta(ua["no_durables"]), "#inf-bienes"),
        lec(tx("l_dur", L), pct(ua["durables"]), tx("l_serv_d", L).format(v=pct(ha["durables"])), "ok" if ua["durables"] <= 4 else "warn", "#inf-bienes"),
        lec(tx("l_ener", L), pct(ua["energeticos"]), tx("l_ener_d", L).format(v=pct(ha["energeticos"])), meta(ua["energeticos"]), "#inf-bienes"),
        lec(tx("l_dif", L), pct(dif, 0), tx("l_dif_d", L).format(w=pct(dif_w, 0)), "warn" if dif > 50 else "ok", "#inf-difusion"),
        lec(tx("l_ciu", L), num(ct23.iloc[-1] - ct23.iloc[0], 1, L, False, " pp"),
            tx("l_ciu_d", L).format(c1=nom_c(ct23.index[0]), v1=pct(ct23.iloc[0]), c2=nom_c(ct23.index[-1]), v2=pct(ct23.iloc[-1])), "", "#inf-ciudades"),
        lec(tx("l_ing", L), num(ing["altos"] - ing["pobres"], 2, L, True, " pp"), tx("l_ing_d", L).format(p=pct(ing["pobres"], 2), a=pct(ing["altos"], 2)), "", "#inf-ingresos"),
    ]
    r0 = tx("r_medidas", L).format(t=pct(tot["var_anual"], 2), m=m, s=pct(ua["servicios"]), b=pct(ua["no_durables"]), d=pct(ua["durables"], 1, True),
                                   dif=pct(dif, 0))
    antes = seccion("inf-medidas", tx("s_medidas", L), r0, f'<div class="lecturas ocho">{"".join(tiles)}</div>')

    # ------------------------------------------------ aportes por division
    dd = dv.drop("total").sort_values("contrib_anual")
    f1 = cs.base(L, height=420, fecha_x=False, suffix=" pp")
    f1.add_trace(go.Bar(y=[f"{DIV[x][k]} ({num(dd.loc[x, 'ponderacion'], 0, L)}%)" for x in dd.index], x=dd["contrib_anual"].round(2), orientation="h",
                        showlegend=False, marker=dict(color=cs.C1, line=dict(width=0)), text=[num(v, 2, L) for v in dd["contrib_anual"]],
                        textposition="outside", cliponaxis=False, hovertemplate="%{y}: %{x:.2f} pp<extra></extra>"))
    f1.update_xaxes(range=[min(0, dd["contrib_anual"].min() * 1.3), dd["contrib_anual"].max() * 1.25], showgrid=True, gridcolor=cs.GRID)
    f1.update_yaxes(ticksuffix="", tickfont=dict(size=12, color=cs.INK2))
    f1.update_layout(hovermode="closest", bargap=0.3)
    g1 = cs.bloque_grafico(tx("g_aportes", L).format(m=m), cs.fig_html(f1, {"notime": True}, "g-inf-aportes"), tx("h_aportes", L))
    dv2 = dv.drop("total").sort_values("var_anual")
    f2 = cs.base(L, height=420, fecha_x=False)
    f2.add_vrect(x0=2, x1=4, fillcolor="rgba(27,175,122,0.12)", line_width=0, layer="below")
    f2.add_trace(go.Bar(y=[DIV[x][k] for x in dv2.index], x=dv2["var_anual"].round(2), orientation="h", showlegend=False,
                        marker=dict(color=[cs.C2 if v > 4 else cs.C1 for v in dv2["var_anual"]], line=dict(width=0)),
                        text=[pct(v) for v in dv2["var_anual"]], textposition="outside", cliponaxis=False, hovertemplate="%{y}: %{x:.2f}%<extra></extra>"))
    f2.update_xaxes(range=[min(0, dv2["var_anual"].min() * 1.3), dv2["var_anual"].max() * 1.2], ticksuffix="%", showgrid=True, gridcolor=cs.GRID)
    f2.update_yaxes(ticksuffix="", tickfont=dict(size=12, color=cs.INK2))
    f2.update_layout(hovermode="closest", bargap=0.3)
    g2 = cs.bloque_grafico(tx("g_divs", L), cs.fig_html(f2, {"notime": True}, "g-inf-divisiones"), tx("h_divs", L))
    top = dd.sort_values("contrib_anual", ascending=False)
    dn = lambda x: DIV[x][k].lower() if L == "es" else DIV[x][k]
    r1 = tx("r_aportes", L).format(t=num(tot["var_anual"], 2, L), d1=DIV[top.index[0]][k], c1=num(top["contrib_anual"].iloc[0], 2, L),
                                   d2=dn(top.index[1]), c2=num(top["contrib_anual"].iloc[1], 2, L), d3=dn(top.index[2]), c3=num(top["contrib_anual"].iloc[2], 2, L),
                                   d4=DIV[dv2.index[-1]][k], v4=pct(dv2["var_anual"].iloc[-1]), d5=dn(dv2.index[0]), v5=pct(dv2["var_anual"].iloc[0]))
    s_ap = seccion("inf-aportes", tx("s_aportes", L), r1, f'<div class="grid">{g1}{g2}</div>')

    # ------------------------------------------------ bienes y servicios
    yy = ya.loc["2012":].dropna(how="all")
    xm = yy.index + pd.offsets.MonthEnd(0)
    f3 = cs.base(L, height=340)
    cs.meta_banda(f3, L)
    for col, lbl, color, w in (("servicios", "lbl_serv", cs.C1, 2.6), ("no_durables", "lbl_nd", cs.C2, 2.0),
                               ("semidurables", "lbl_sd", cs.C3, 1.8), ("durables", "lbl_dur", cs.C7, 1.8)):
        cs.linea(f3, xm, yy[col], tx(lbl, L), color, width=w, lang=L)
    f3.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    g3 = cs.bloque_grafico(tx("g_bs", L), cs.fig_html(f3, {}, "g-inf-bienes-servicios"), tx("h_bs", L))
    f4 = cs.base(L, height=340)
    cs.meta_banda(f4, L)
    cs.linea(f4, xm, yy["energeticos"].clip(-20, 40), tx("lbl_ener", L), cs.C4, width=1.8, lang=L)
    cs.linea(f4, xm, yy["sin_alimentos_energeticos"], tx("lbl_core", L), cs.C1, width=2.6, lang=L)
    f4.add_hline(y=0, line=dict(color=cs.INK2, width=1))
    g4 = cs.bloque_grafico(tx("g_core", L), cs.fig_html(f4, {}, "g-inf-energia"), tx("h_core", L))
    r2 = tx("r_bienes", L).format(s=pct(ua["servicios"]), b=pct(ua["no_durables"]), d=pct(ua["durables"], 1, True), c=pct(ua["sin_alimentos_energeticos"]))
    s_bs = seccion("inf-bienes", tx("s_bienes", L), r2, f'<div class="grid">{g3}{g4}</div>')

    # ------------------------------------------------ difusion
    v = sub["var_anual"].clip(-10, 20)
    bins = np.arange(-10, 21, 1)
    cnt, edges = np.histogram(v, bins=bins)
    centros = (edges[:-1] + edges[1:]) / 2
    f5 = cs.base(L, height=340, fecha_x=False, suffix="")
    f5.add_vrect(x0=2, x1=4, fillcolor="rgba(27,175,122,0.12)", line_width=0, layer="below")
    f5.add_trace(go.Bar(x=centros, y=cnt, showlegend=False, marker=dict(color=[cs.C2 if c_ > 4 else cs.C1 for c_ in centros], line=dict(width=0)),
                        customdata=[f"{int(a)}% – {int(b)}%" for a, b in zip(edges[:-1], edges[1:])],
                        hovertemplate="%{customdata}: %{y}<extra></extra>"))
    f5.update_xaxes(ticksuffix="%", dtick=2)
    f5.update_layout(bargap=0.08, hovermode="closest")
    g5 = cs.bloque_grafico(tx("g_hist", L).format(m=m), cs.fig_html(f5, {"notime": True}, "g-inf-difusion"), tx("h_hist", L))
    g5 = g5.replace("</figcaption>", f" {q_btn}</figcaption>", 1)
    tp = pd.concat([sub.nlargest(8, "contrib_anual"), sub.nsmallest(4, "contrib_anual")]).sort_values("contrib_anual")
    corto = lambda s_: (s_[:38] + "…") if len(s_) > 39 else s_
    f6 = cs.base(L, height=420, fecha_x=False, suffix=" pp")
    f6.add_trace(go.Bar(y=[corto(s_) for s_ in tp["subclase"]], x=tp["contrib_anual"].round(2), orientation="h", showlegend=False,
                        marker=dict(color=[cs.C2 if c_ > 0 else cs.C3 for c_ in tp["contrib_anual"]], line=dict(width=0)),
                        text=[num(c_, 2, L, True) for c_ in tp["contrib_anual"]], textposition="outside", cliponaxis=False,
                        customdata=[pct(v_, 1, True) for v_ in tp["var_anual"]],
                        hovertemplate="%{y}: %{x:.2f} pp<br>" + ("Inflación anual" if L == "es" else "Annual inflation") + ": %{customdata}<extra></extra>"))
    f6.add_vline(x=0, line=dict(color=cs.INK2, width=1))
    f6.update_xaxes(range=[tp["contrib_anual"].min() * 6 - 0.1, tp["contrib_anual"].max() * 1.25], showgrid=True, gridcolor=cs.GRID)
    f6.update_yaxes(ticksuffix="", tickfont=dict(size=11, color=cs.INK2))
    f6.update_layout(hovermode="closest", bargap=0.3)
    g6 = cs.bloque_grafico(tx("g_top", L), cs.fig_html(f6, {"notime": True}, "g-inf-subclases"), tx("h_top", L))
    def breve(s_):
        s_ = re.split(r"[,;(]", s_)[0].strip()
        return s_ if len(s_) <= 48 else s_[:48].rsplit(" ", 1)[0] + "…"
    lista = lambda df: ", ".join(f"{breve(s_).lower()} ({num(c_, 2, L, True)} pp)" for s_, c_ in zip(df["subclase"], df["contrib_anual"]))
    r3 = tx("r_difusion", L).format(dif=pct(dif, 0), dif6=pct(dif6, 0), dw=pct(dif_w, 0), top=lista(sub.nlargest(3, "contrib_anual")), bot=lista(sub.nsmallest(2, "contrib_anual")))
    s_dif = seccion("inf-difusion", tx("s_difusion", L), r3, f'<div class="grid">{g5}{g6}</div>') + ventana_canasta(sub_w, I["divisiones"], L, num, esc)

    # ------------------------------------------------ ingresos
    gi = ["pobres", "vulnerables", "media", "altos"]
    f7 = cs.base(L, height=330, fecha_x=False)
    f7.add_trace(go.Bar(x=[TX["ing"][g_][k] for g_ in gi], y=[round(float(ing[g_]), 2) for g_ in gi], showlegend=False,
                        marker=dict(color=[cs.C1, cs.C3, cs.C7, cs.C2], line=dict(width=0)), text=[pct(ing[g_], 2) for g_ in gi],
                        textposition="outside", cliponaxis=False, hovertemplate="%{x}: %{y:.2f}%<extra></extra>"))
    f7.add_hline(y=float(ing["total"]), line=dict(color=cs.INK, width=1.2, dash="dot"))
    f7.update_yaxes(range=[0, float(ing.max()) * 1.2])
    f7.update_layout(bargap=0.45, hovermode="closest")
    g7 = cs.bloque_grafico(tx("g_ing", L), cs.fig_html(f7, {"notime": True}, "g-inf-ingresos"), tx("h_ing", L))
    r4 = tx("r_ingresos", L).format(p=pct(ing["pobres"], 2), a=pct(ing["altos"], 2), txt=tx("ing_altos" if ing["altos"] > ing["pobres"] else "ing_pobres", L).format(x=num(abs(ing["altos"] - ing["pobres"]), 2, L)))
    s_ing = seccion("inf-ingresos", tx("s_ingresos", L), r4, f'<div class="grid">{g7}</div>')

    # ------------------------------------------------ ciudades
    f8 = cs.base(L, height=600, fecha_x=False)
    f8.add_trace(go.Bar(y=[nom_c(c_) for c_ in ct23.index], x=ct23.round(2), orientation="h", showlegend=False,
                        marker=dict(color=[cs.C2 if v_ > float(tot["var_anual"]) else cs.C1 for v_ in ct23], line=dict(width=0)),
                        text=[pct(v_, 2) for v_ in ct23], textposition="outside", cliponaxis=False, textfont=dict(size=10.5, color=cs.INK2),
                        hovertemplate="%{y}: %{x:.2f}%<extra></extra>"))
    f8.add_vline(x=float(tot["var_anual"]), line=dict(color=cs.INK, width=1.2, dash="dot"))
    f8.update_xaxes(range=[0, ct23.max() * 1.18], ticksuffix="%", showgrid=True, gridcolor=cs.GRID)
    f8.update_yaxes(ticksuffix="", tickfont=dict(size=11, color=cs.INK2))
    f8.update_layout(hovermode="closest", bargap=0.25)
    g8 = cs.bloque_grafico(tx("g_ciu", L).format(m=m), cs.fig_html(f8, {"notime": True}, "g-inf-ciudades"), tx("h_ciu", L))
    hm = ci[(ci["division"] != "total") & (ci["ciudad"].isin(ct23.index))].pivot(index="ciudad", columns="division", values="var_anual")
    cols = list(DIV)
    hm = hm.reindex(ct23.index[::-1])[cols]
    f9 = cs.base(L, height=600, fecha_x=False)
    f9.add_trace(go.Heatmap(x=[DIV[c_][k] for c_ in cols], y=[nom_c(c_) for c_ in hm.index], z=hm.round(1).values.tolist(), zmin=0, zmax=12,
                            colorscale=[[0, "#f7f6f2"], [0.25, "#f3c9b3"], [0.6, "#eb6834"], [1, "#b04a17"]],
                            colorbar=dict(ticksuffix="%", thickness=10, len=0.6, outlinewidth=0, tickfont=dict(size=11, color=cs.MUTED)),
                            xgap=1, ygap=1, hovertemplate="<b>%{y}</b> · %{x}: %{z:.1f}%<extra></extra>"))
    f9.update_layout(hovermode="closest", showlegend=False)
    f9.update_yaxes(ticksuffix="", tickfont=dict(size=11, color=cs.INK2), gridcolor="rgba(0,0,0,0)")
    f9.update_xaxes(side="top", tickangle=-40, showline=False, tickfont=dict(size=11, color=cs.INK2))
    g9 = cs.bloque_grafico(tx("g_mapa", L), cs.fig_html(f9, {"notime": True}, "g-inf-ciudad-division"), tx("h_mapa", L))
    cmax = ct23.index[-1]
    rowmax = hm.loc[cmax].sort_values()
    r5 = tx("r_ciudades", L).format(lo=pct(ct23.iloc[0], 2), c1=nom_c(ct23.index[0]), hi=pct(ct23.iloc[-1], 2), c2=nom_c(cmax),
                                    n=int((ct23 > float(tot["var_anual"])).sum()), t=pct(tot["var_anual"], 2), cmax=nom_c(cmax),
                                    dmax=dn(rowmax.index[-1]), vmax=pct(rowmax.iloc[-1]))
    s_ciu = seccion("inf-ciudades", tx("s_ciudades", L), r5, f'<div class="grid">{g8}{g9}</div>')

    items = "".join(f'<li><span class="ref">{ref}</span><span class="ref-u">{es if L == "es" else en}</span></li>' for ref, es, en in LITERATURA)
    s_lit = (f'<section id="inf-literatura" class="section"><div class="sec-head"><span class="sec-num">0</span><h2>{tx("s_lit", L)}</h2></div>'
             f'<ol class="refs">{items}</ol></section>')
    return antes, s_ap + s_bs + s_dif + s_ing + s_ciu + s_lit


# ====================================================================== ventana explicativa: la canasta del IPC
def _n(s):
    import unicodedata
    return re.sub(r"[^a-z0-9]+", " ", unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()).strip()


def con_ponderaciones(sub: pd.DataFrame) -> pd.DataFrame:
    """Une las subclases del anexo con sus ponderaciones oficiales. Las dos listas siguen el orden COICOP:
    si coinciden en posicion (95% de nombres iguales) se alinean por posicion; si no, por nombre."""
    f = DATA_DIR / "ipc_ponderaciones.csv"
    if not f.exists():
        return sub.assign(peso=np.nan, peso_pobres=np.nan, peso_altos=np.nan)
    w = pd.read_csv(f)
    s = sub.reset_index(drop=True).copy()
    if len(w) == len(s) and np.mean([_n(a) == _n(b) for a, b in zip(w["subclase"], s["subclase"])]) >= 0.95:
        s["peso"], s["peso_pobres"], s["peso_altos"] = w["total"].values, w["pobres"].values, w["altos"].values
        return s
    m = dict(zip(w["subclase"].map(_n), w[["total", "pobres", "altos"]].values.tolist()))
    vals = [m.get(_n(x), [np.nan] * 3) for x in s["subclase"]]
    s["peso"], s["peso_pobres"], s["peso_altos"] = zip(*vals)
    return s


CIUDADES_PESO = [("Bogotá", 40.45), ("Medellín", 15.03), ("Cali", 9.15), ("Barranquilla", 5.31), ("Bucaramanga", 4.63),
                 ("Otras áreas urbanas", 3.38), ("Cartagena", 3.15), ("Cúcuta", 2.31), ("Pereira", 2.06), ("Villavicencio", 1.82)]


def ventana_canasta(sub_w: pd.DataFrame, divisiones: pd.DataFrame, L: str, num, esc) -> str:
    """<dialog> con la explicacion oficial de la canasta: estructura COICOP, ponderaciones, ingresos, cobertura."""
    es = L == "es"
    pct = lambda v, d=1: num(float(v), d, L, False, "%")
    w = sub_w.dropna(subset=["peso"])
    top = w.nlargest(10, "peso")
    breve = lambda s_: (lambda x: x[:1].upper() + x[1:].lower())(re.split(r"[;:(]", s_)[0].strip()[:70])
    filas_top = "".join(f"<tr><td>{esc(breve(r.subclase))}</td><td class='n'>{pct(r.peso, 2)}</td><td class='n'>{pct(r.var_anual)}</td></tr>"
                        for r in top.itertuples())
    pesado = w["peso"].nlargest(10).sum()
    dif_n = 100 * (w["var_anual"] > 4).mean()
    dif_w = w.loc[w["var_anual"] > 4, "peso"].sum() / w["peso"].sum() * 100
    dv = divisiones.set_index("division").drop("total")
    # contraste pobres vs ingresos altos (subclases con mayor diferencia de peso)
    w2 = w.assign(dif=w["peso_pobres"] - w["peso_altos"]).dropna(subset=["dif"])
    contraste = pd.concat([w2.nlargest(3, "dif"), w2.nsmallest(3, "dif")])
    filas_ing = "".join(f"<tr><td>{esc(breve(r.subclase))}</td><td class='n'>{pct(r.peso_pobres, 2)}</td><td class='n'>{pct(r.peso_altos, 2)}</td></tr>"
                        for r in contraste.itertuples())
    niveles = [("12", "divisiones", "divisions", "Alimentos y bebidas no alcohólicas", "Food and non-alcoholic beverages"),
               ("42", "grupos", "groups", "Alimentos", "Food"),
               ("84", "clases", "classes", "Pan y cereales", "Bread and cereals"),
               ("188", "subclases", "subclasses", "Arroz", "Rice"),
               ("443", "artículos", "items", "El arroz que se cotiza en cada establecimiento", "The rice priced in each store")]
    escalera = "".join(f'<li style="--i:{k}"><b>{n}</b><span>{a if es else b}</span><em>{c if es else d}</em></li>'
                       for k, (n, a, b, c, d) in enumerate(niveles))
    pmax = max(p for _, p in CIUDADES_PESO)
    ciudades = "".join(f"<li><span>{esc(c)}</span><i style='width:{p / pmax * 100:.1f}%'></i><b>{num(p, 1, L)}%</b></li>" for c, p in CIUDADES_PESO)
    T = (lambda a, b: a if es else b)
    return f"""<dialog class="explica" id="exp-canasta" aria-labelledby="exp-canasta-t">
<div class="ex-cab"><p class="ex-k">{T("Para entender", "To understand")} · DANE</p><h2 id="exp-canasta-t">{T("¿Qué son las 188 subclases de la canasta del IPC?", "What are the 188 subclasses of the CPI basket?")}</h2>
<button type="button" class="ex-x" data-cerrar aria-label="{T("Cerrar", "Close")}">✕</button></div>
<div class="ex-cuerpo">
<p class="ex-lede">{T("El Índice de Precios al Consumidor (IPC) mide cuánto cambian, mes a mes, los precios de los bienes y servicios que compran los hogares colombianos. El DANE no sigue «todos los precios»: sigue una <b>canasta</b> representativa del gasto de los hogares, organizada en niveles. Las <b>188 subclases</b> son el nivel en el que el DANE publica resultados detallados.",
 "The Consumer Price Index (CPI) measures how much the prices of the goods and services bought by Colombian households change month by month. DANE does not track 'all prices': it tracks a <b>basket</b> representative of household spending, organised in levels. The <b>188 subclasses</b> are the level at which DANE publishes detailed results.")}</p>

<h3>{T("1. Cómo está organizada la canasta", "1. How the basket is organised")}</h3>
<p>{T("Desde 2019 (base diciembre de 2018 = 100) la canasta usa la nomenclatura basada en la COICOP, la clasificación de las Naciones Unidas del consumo individual por finalidad. Cada nivel se abre en el siguiente; por ejemplo, el arroz:",
 "Since 2019 (base December 2018 = 100) the basket uses the COICOP-based nomenclature, the United Nations classification of individual consumption by purpose. Each level opens into the next; for example, rice:")}</p>
<ol class="ex-escalera">{escalera}</ol>
<p>{T("Las 188 subclases reúnen 443 artículos, que son los productos concretos cuyos precios recolecta el DANE en los establecimientos. Ejemplos de subclases: arroz, pan, carne de res, electricidad, transporte urbano, arriendo, comidas fuera del hogar, matrículas universitarias o servicios de comunicación.",
 "The 188 subclasses group 443 items, the specific products whose prices DANE collects in stores. Examples of subclasses: rice, bread, beef, electricity, urban transport, rent, meals away from home, university fees or communication services.")}</p>

<h3>{T("2. No todas pesan lo mismo", "2. They do not all weigh the same")}</h3>
<p>{T(f"Cada subclase pesa según lo que los hogares gastan en ella, de acuerdo con la Encuesta Nacional de Presupuestos de los Hogares (ENPH). Las 10 subclases más pesadas suman <b>{pct(pesado)}</b> de la canasta:",
 f"Each subclass weighs according to what households spend on it, based on the National Household Budget Survey (ENPH). The 10 heaviest subclasses add up to <b>{pct(pesado)}</b> of the basket:")}</p>
<div class="table-wrap plano"><table class="tbl"><thead><tr><th>{T("Subclase", "Subclass")}</th><th>{T("Peso en la canasta", "Basket weight")}</th><th>{T("Inflación anual hoy", "Annual inflation today")}</th></tr></thead><tbody>{filas_top}</tbody></table></div>
<p class="ex-nota">{T("El «arriendo imputado» es lo que pagaría en arriendo quien vive en vivienda propia: el DANE lo incluye para medir el costo del servicio de vivienda de todos los hogares.",
 "'Imputed rent' is what owner-occupiers would pay in rent: DANE includes it to measure the cost of housing services for all households.")}</p>

<h3>{T("3. Una canasta distinta para cada nivel de ingreso", "3. A different basket for each income level")}</h3>
<p>{T("El DANE calcula el IPC para cuatro grupos de hogares definidos con un criterio absoluto de ingreso (pobres, vulnerables, clase media e ingresos altos). Por eso la misma subida de precios pesa distinto en cada uno:",
 "DANE computes the CPI for four household groups defined by an absolute income criterion (poor, vulnerable, middle class and high income). That is why the same price rise weighs differently on each:")}</p>
<div class="table-wrap plano"><table class="tbl"><thead><tr><th>{T("Subclase", "Subclass")}</th><th>{T("Peso · pobres", "Weight · poor")}</th><th>{T("Peso · ingresos altos", "Weight · high income")}</th></tr></thead><tbody>{filas_ing}</tbody></table></div>

<h3>{T("4. Dónde se miden los precios", "4. Where prices are measured")}</h3>
<p>{T("La actualización de 2019 amplió la cobertura de 24 a 38 ciudades (32 capitales de departamento y 6 municipios priorizados) e incluyó por primera vez a los hogares unipersonales. Se publican 23 ciudades por separado y un agregado de «otras áreas urbanas». Cada ciudad pesa según el gasto de sus hogares:",
 "The 2019 update widened coverage from 24 to 38 cities (32 department capitals and 6 priority municipalities) and included single-person households for the first time. 23 cities are published separately plus an 'other urban areas' aggregate. Each city weighs according to its households' spending:")}</p>
<ul class="ex-barras">{ciudades}</ul>

<h3>{T("5. Cómo leer el gráfico de difusión", "5. How to read the diffusion chart")}</h3>
<p>{T(f"El histograma cuenta subclases sin ponderar: hoy <b>{pct(dif_n, 0)}</b> de las 188 suben más de 4% al año, el techo del rango meta del Banco de la República. Si se ponderan por su peso en la canasta, esas subclases representan <b>{pct(dif_w, 0)}</b> del gasto de los hogares. Cuando ambas cifras son altas, la inflación es generalizada y no depende de unos pocos precios.",
 f"The histogram counts subclasses without weights: today <b>{pct(dif_n, 0)}</b> of the 188 rise more than 4% a year, the ceiling of the Banco de la República target range. Weighted by their basket share, those subclasses represent <b>{pct(dif_w, 0)}</b> of household spending. When both figures are high, inflation is broad-based rather than driven by a few prices.")}</p>

<h3>{T("Fuentes oficiales", "Official sources")}</h3>
<ul class="ex-fuentes">
<li><a href="https://www.dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/indice-de-precios-al-consumidor-ipc/ipc-actualizacion-metodologica-2019" target="_blank" rel="noopener">DANE — {T("IPC: actualización metodológica 2019", "CPI: 2019 methodological update")}</a></li>
<li><a href="https://www.dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/indice-de-precios-al-consumidor-ipc/ipc-actualizacion-metodologica-2019/ipc-nomenclatura-basada-en-la-coicop" target="_blank" rel="noopener">DANE — {T("Nomenclatura basada en la COICOP y estructura IPC 2018", "COICOP-based nomenclature and 2018 CPI structure")}</a></li>
<li><a href="https://www.dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/indice-de-precios-al-consumidor-ipc/ipc-actualizacion-metodologica-2019/ipc-ponderadores" target="_blank" rel="noopener">DANE — {T("Ponderaciones del nuevo IPC por división, grupo, clase, subclase y ciudad", "New CPI weights by division, group, class, subclass and city")}</a></li>
<li>FMI, OIT, OCDE, Eurostat, CEPE de la ONU y Banco Mundial (2004/2006). <i>{T("Manual del índice de precios al consumidor: teoría y práctica", "Consumer Price Index Manual: Theory and Practice")}</i>.</li>
<li>Naciones Unidas (1999). <i>{T("Clasificación del consumo individual por finalidades (COICOP)", "Classification of Individual Consumption According to Purpose (COICOP)")}</i>.</li>
</ul>
</div></dialog>"""
