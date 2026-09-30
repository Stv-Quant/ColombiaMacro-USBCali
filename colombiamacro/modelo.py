"""Modelo de datos del tablero: carga tablas, calcula indicadores y redacta la lectura.

Separado de la capa Dash para poder probar cada cifra que aparece en pantalla.
Todas las frases del veredicto se derivan de reglas explicitas (umbrales abajo);
no hay texto escrito a mano que pueda quedar desactualizado.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

from colombiamacro import analitica as am
from colombiamacro.config import DATA_DIR


# Tasa real neutral de referencia: estimacion del equipo tecnico de BanRep de 2,7% (2025)
# con senal de subida hacia 3,0% (2026). Parametro externo, documentado en METODOLOGIA.md.
NEUTRAL_REAL = (2.7, 3.0)
UMBRAL_BRECHA = 0.5      # |brecha| < 0,5% del PIB potencial = "cerca del potencial"
UMBRAL_POSTURA = 0.5     # pp sobre/bajo el rango neutral para calificar la postura
ANCLA_EXPECTATIVAS = 4.0 # techo del rango meta: 5y5y por encima = expectativas desancladas


def _read(name: str, **kw) -> pd.DataFrame | None:
    path = DATA_DIR / name
    return pd.read_csv(path, **kw) if path.exists() else None


def _serie(long: pd.DataFrame | None, name: str) -> pd.DataFrame:
    if long is None:
        return pd.DataFrame(columns=["fecha", name])
    sub = long.loc[long["serie"] == name, ["fecha", "valor"]].rename(columns={"valor": name})
    return sub.sort_values("fecha").reset_index(drop=True)


TES_COLS = ["tes_pesos_1y", "tes_pesos_5y", "tes_pesos_10y", "tes_uvr_1y", "tes_uvr_5y", "tes_uvr_10y"]


def limpiar_saltos_tes(tes: pd.DataFrame) -> pd.DataFrame:
    """Oculta en los calculos derivados los saltos aislados de un dia (> 2 pp y revertidos).

    Mismo criterio que validar_datos.isolated_tes_spikes; el CSV original no se modifica.
    """
    from colombiamacro.validar import isolated_tes_spikes
    out = tes.copy()
    for col in TES_COLS:
        if col in out:
            out.loc[isolated_tes_spikes(out[col]), col] = np.nan
    return out


@dataclass
class Datos:
    pib: pd.DataFrame
    ipc: pd.DataFrame
    tes: pd.DataFrame
    colcap: pd.DataFrame
    estado: pd.DataFrame
    ciclo: pd.DataFrame
    inflacion: pd.DataFrame
    tasas: pd.DataFrame
    mercado: pd.DataFrame
    ise: pd.DataFrame | None
    laboral: pd.DataFrame | None
    extra: dict = field(default_factory=dict)
    canasta: pd.DataFrame | None = None
    acciones: pd.DataFrame | None = None


def cargar() -> Datos:
    pib = _read("pib_colombia.csv", parse_dates=["fecha"]).dropna(subset=["pib_real_yoy"])
    ipc = _read("inflacion_clean.csv", parse_dates=["fecha"])
    tes = _read("tasas_interes_clean.csv", parse_dates=["fecha"])
    colcap = _read("colcap_oficial.csv", parse_dates=["fecha"])
    estado = _read("estado_fuentes.csv")
    long = _read("series_banrep.csv", parse_dates=["fecha"])
    extra = {k: _serie(long, k) for k in (
        "tpm", "trm", "ibr_overnight", "inflacion_basica_sar", "inflacion_sin_alimentos",
        "inflacion_nucleo15", "inflacion_regulados", "inflacion_alimentos", "meta_inflacion",
        "itcr_ipc", "terminos_intercambio", "reservas_netas_musd", "cuenta_corriente_pct_pib",
        "ied_musd", "deuda_bruta_gnc_pct_pib", "salario_minimo_var")}
    tpm = extra["tpm"] if not extra["tpm"].empty else None
    trm = extra["trm"] if not extra["trm"].empty else None

    tes = limpiar_saltos_tes(tes)
    inflacion = am.regimen_inflacion(ipc)
    for k in ("inflacion_basica_sar", "inflacion_sin_alimentos", "inflacion_alimentos",
              "inflacion_regulados"):
        if not extra[k].empty:
            inflacion = inflacion.merge(extra[k], on="fecha", how="left")
    ise = _read("ise_mensual.csv", parse_dates=["fecha"])
    if ise is not None:
        # Variacion anual de la serie desestacionalizada: menos ruido de calendario que la original.
        ise["ise_sa_yoy"] = 100 * (ise["ise_sa"] / ise["ise_sa"].shift(12) - 1)
    laboral = _read("mercado_laboral.csv", parse_dates=["fecha"])
    return Datos(pib=pib, ipc=ipc, tes=tes, colcap=colcap, estado=estado,
                 ciclo=am.tabla_ciclo(pib), inflacion=inflacion,
                 tasas=am.depurar_derivadas(am.tabla_tasas(tes, tpm, ipc))[0],
                 mercado=am.tabla_mercado(colcap, trm, ipc),
                 ise=ise, laboral=laboral, extra=extra,
                 canasta=_read("colcap_canasta.csv"),
                 acciones=_read("acciones_semanal.csv", parse_dates=["fecha"]))


# ---------------------------------------------------------------- bolsa por dentro
N_MAGNIFICAS = 7
NOMBRES_CORTOS = {
    "GRUPO CIBEST": "Grupo Cibest", "GRUPO DE INVERSIONES SURAMERICANA": "Grupo Sura", "ECOPETROL": "Ecopetrol",
    "INTERCONEXION ELECTRICA": "ISA", "INVERSIONES ARGOS": "Grupo Argos", "GRUPO ENERGIA BOGOTA": "Grupo Energía Bogotá",
    "CEMENTOS ARGOS": "Cementos Argos", "DAVIVIENDA GROUP": "Davivienda", "GRUPO AVAL ACCIONES Y VALORES": "Grupo Aval",
    "CELSIA": "Celsia", "PATRIMONIO ESTRATEGIAS INMOBIL REI": "PEI", "MINEROS": "Mineros",
    "CORPORACION FINANCIERA COLOMBIANA": "Corficolombiana", "GRUPO BOLIVAR": "Grupo Bolívar",
    "BANCO DE BOGOTA": "Banco de Bogotá", "ORGANIZACION TERPEL": "Terpel", "ALMACENES EXITO": "Grupo Éxito",
    "PROMIGAS": "Promigas", "CANACOL ENERGY LTD": "Canacol", "GRUPO NUTRESA": "Grupo Nutresa",
}


def nombre_corto(emisor: str) -> str:
    return NOMBRES_CORTOS.get(str(emisor), str(emisor).title())
SALTO_MAX = 0.6  # retorno semanal por encima de +/-60% = error de precio de la fuente


def magnificas(canasta: pd.DataFrame, n: int = N_MAGNIFICAS) -> pd.DataFrame:
    """Las n empresas (emisores) de mayor peso en el COLCAP. Si una empresa tiene acciones
    ordinarias y preferenciales se suman sus pesos y se usa la clase de mayor peso."""
    c = canasta.sort_values("peso", ascending=False)
    g = (c.groupby("emisor", sort=False)
          .agg(peso=("peso", "sum"), ticker=("ticker", "first"), nombre=("nombre", "first"),
               sector=("sector", "first"), clases=("ticker", lambda x: " + ".join(x)))
          .sort_values("peso", ascending=False).head(n).reset_index())
    return g


def retornos_semanales(acciones: pd.DataFrame) -> pd.DataFrame:
    precios = acciones.pivot_table(index="fecha", columns="ticker", values="cierre").sort_index()
    r = precios.pct_change(fill_method=None)
    return r.where(r.abs() <= SALTO_MAX)


def indice_equiponderado(r: pd.DataFrame, tickers=None) -> pd.Series:
    """Indice base 100: cada semana todas las acciones disponibles pesan igual (rebalanceo semanal)."""
    sub = r if tickers is None else r[[t for t in tickers if t in r]]
    prom = sub.mean(axis=1, skipna=True)
    prom.iloc[0] = 0.0
    return 100 * (1 + prom.fillna(0)).cumprod()


def bolsa_por_dentro(d: "Datos") -> dict | None:
    """COLCAP oficial (ponderado por capitalizacion) frente a un equiponderado de su canasta
    y frente a las 7 Magnificas, en frecuencia semanal y base 100."""
    if d.canasta is None or d.acciones is None or d.canasta.empty or d.acciones.empty:
        return None
    canasta = d.canasta
    top = magnificas(canasta)
    acc = d.acciones[d.acciones["ticker"].isin(canasta["ticker"])].copy()
    acc["fecha"] = acc["fecha"].dt.to_period("W-FRI").dt.end_time.dt.normalize()
    acc = acc.drop_duplicates(["ticker", "fecha"], keep="last")
    r = retornos_semanales(acc)
    eq = indice_equiponderado(r)
    m7 = indice_equiponderado(r, top["ticker"])
    col = d.colcap.dropna(subset=["colcap_puntos"]).set_index("fecha")["colcap_puntos"]
    col = col.resample("W-FRI").last()
    tabla = pd.DataFrame({"colcap": col, "equiponderado": eq, "magnificas": m7}).dropna(how="all")
    tabla = tabla[tabla.index >= max(eq.index.min(), col.index.min())]
    # La semana en curso se fecha con el ultimo dato observado, no con el viernes futuro.
    ultimo = max(d.acciones["fecha"].max(), d.colcap["fecha"].max())
    tabla = tabla.ffill()
    tabla.index = tabla.index.where(tabla.index <= ultimo, ultimo)
    base = tabla.iloc[0]
    tabla = 100 * tabla / base
    precios = d.acciones.pivot_table(index="fecha", columns="ticker", values="cierre").sort_index()
    filas = []
    for _, e in top.iterrows():
        p = precios[e["ticker"]].dropna()
        if p.empty:
            continue
        f = p.index[-1]

        def var(dias):
            prev = p[p.index <= f - pd.Timedelta(days=dias)]
            return None if prev.empty else 100 * (p.iloc[-1] / prev.iloc[-1] - 1)
        ini_ano = p[p.index < pd.Timestamp(f.year, 1, 1)]
        filas.append({"emisor": nombre_corto(e["emisor"]), "ticker": e["ticker"], "clases": e["clases"], "sector": e["sector"],
                      "peso": e["peso"], "precio": float(p.iloc[-1]), "fecha": f,
                      "var_1m": var(28), "var_12m": var(364),
                      "var_ano": None if ini_ano.empty else 100 * (p.iloc[-1] / ini_ano.iloc[-1] - 1)})
    return {"indices": tabla.reset_index(names="fecha"), "magnificas": pd.DataFrame(filas),
            "canasta": canasta, "fecha_canasta": canasta["fecha_canasta"].iloc[0],
            "peso_magnificas": float(top["peso"].sum())}


# ---------------------------------------------------------------- instantanea
def _last(df: pd.DataFrame | None, col: str):
    if df is None or col not in df or df[col].dropna().empty:
        return None
    row = df.dropna(subset=[col]).iloc[-1]
    return {"valor": float(row[col]), "fecha": pd.Timestamp(row["fecha"])}


def _hace(df: pd.DataFrame, col: str, fecha: pd.Timestamp, dias: int):
    sub = df.dropna(subset=[col])
    sub = sub[sub["fecha"] <= fecha - pd.Timedelta(days=dias)]
    return None if sub.empty else float(sub.iloc[-1][col])


def instantanea(d: Datos) -> dict:
    s: dict = {}
    c = d.ciclo.dropna(subset=["brecha_hp_tiempo_real"]).iloc[-1]
    s["ciclo"] = {k: (float(c[k]) if isinstance(c[k], (int, float, np.floating)) else c[k])
                  for k in ("trimestre", "pib_real_yoy", "pib_real_qoq_saar", "brecha_hp_tiempo_real",
                            "brecha_min", "brecha_max", "delta_brecha", "fase", "fase_hamilton",
                            "crecimiento_potencial_hp", "metodos_brecha_positiva",
                            "metodos_disponibles")}
    s["ciclo"]["fecha"] = pd.Timestamp(c["fecha"])

    inf = d.inflacion.iloc[-1]
    s["inflacion"] = {"total": float(inf["inflacion_anual"]), "fecha": pd.Timestamp(inf["fecha"]),
                      "mensual": float(inf["inflacion_mensual"]),
                      "cambio_3m": float(inf["cambio_3m_pp"]),
                      "hace_12m": _hace(d.inflacion, "inflacion_anual", inf["fecha"], 360)}
    b = _last(d.inflacion, "inflacion_basica_sar")
    s["inflacion"]["basica"] = b["valor"] if b else None

    t = d.tasas.dropna(subset=["tes_pesos_10y"]).iloc[-1]
    s["tasas"] = {k: (float(t[k]) if k in t and pd.notna(t[k]) else None) for k in (
        "tes_pesos_1y", "tes_pesos_5y", "tes_pesos_10y", "bei_1y", "bei_5y", "bei_10y", "bei_5y5y",
        "pendiente_10y_1y", "tpm", "tpm_real_exante", "tpm_real_expost", "pendiente_10y_tpm")}
    s["tasas"]["fecha"] = pd.Timestamp(t["fecha"])
    s["tasas"]["tes10_hace_3m"] = _hace(d.tasas, "tes_pesos_10y", t["fecha"], 91)
    tpm = d.extra["tpm"]
    if not tpm.empty:
        cambios = tpm[tpm["tpm"].diff().fillna(0) != 0]
        ultimo = cambios.iloc[-1] if not cambios.empty else None
        s["tasas"]["tpm_ultimo_cambio"] = None if ultimo is None else {
            "fecha": pd.Timestamp(ultimo["fecha"]),
            "delta": float(ultimo["tpm"] - tpm[tpm["fecha"] < ultimo["fecha"]]["tpm"].iloc[-1])}
        s["tasas"]["tpm_hace_12m"] = _hace(tpm, "tpm", tpm["fecha"].max(), 365)

    m = d.mercado.iloc[-1]
    s["mercado"] = {"colcap": float(m["colcap_puntos"]), "fecha": pd.Timestamp(m["fecha"]),
                    "drawdown": float(m["drawdown_pct"]),
                    "colcap_12m": am.retorno_ventana(d.mercado["colcap_puntos"], d.mercado["fecha"], 365)}
    if "colcap_usd" in d.mercado:
        s["mercado"]["colcap_usd_12m"] = am.retorno_ventana(d.mercado["colcap_usd"], d.mercado["fecha"], 365)
    trm = d.extra["trm"]
    if not trm.empty:
        s["mercado"]["trm"] = float(trm["trm"].iloc[-1])
        s["mercado"]["trm_fecha"] = pd.Timestamp(trm["fecha"].iloc[-1])
        s["mercado"]["trm_12m"] = am.retorno_ventana(trm["trm"], trm["fecha"], 365)

    for key, col in (("itcr", "itcr_ipc"), ("cc", "cuenta_corriente_pct_pib"),
                     ("deuda", "deuda_bruta_gnc_pct_pib")):
        s[key] = _last(d.extra[col], col)
    s["ise"] = None
    if d.ise is not None:
        r = d.ise.dropna(subset=["ise_sa"]).iloc[-1]
        s["ise"] = {"fecha": pd.Timestamp(r["fecha"]), "yoy": float(r["ise_sa_yoy"]),
                    "yoy_original": float(r["ise_yoy"]),
                    "saar_3m": float(r["ise_sa_3m3m_saar"])}
    s["laboral"] = None
    if d.laboral is not None:
        r = d.laboral.dropna(subset=["td_sa"]).iloc[-1]
        s["laboral"] = {"fecha": pd.Timestamp(r["fecha"]), "td": float(r["td_sa"]),
                        "td_hace_12m": _hace(d.laboral, "td_sa", r["fecha"], 360)}
    return s


# ---------------------------------------------------------------- clasificaciones
def lectura_brecha(g: float) -> str:
    if g >= UMBRAL_BRECHA:
        return "encima"
    if g <= -UMBRAL_BRECHA:
        return "debajo"
    return "cerca"


def postura_monetaria(real_exante: float | None) -> str | None:
    if real_exante is None or pd.isna(real_exante):
        return None
    lo, hi = NEUTRAL_REAL
    if real_exante > hi + UMBRAL_POSTURA:
        return "restrictiva"
    if real_exante < lo - UMBRAL_POSTURA:
        return "expansiva"
    return "neutral"


def anclaje(bei_5y5y: float | None) -> str | None:
    if bei_5y5y is None or pd.isna(bei_5y5y):
        return None
    return "desancladas" if bei_5y5y > ANCLA_EXPECTATIVAS else "ancladas"


# ---------------------------------------------------------------- texto
def _n(x, dec=1, lang="es", signo=False):
    if x is None or pd.isna(x):
        return "—"
    txt = f"{x:+,.{dec}f}" if signo else f"{x:,.{dec}f}"
    if lang == "es":
        txt = txt.replace(",", "§").replace(".", ",").replace("§", ".")
    return txt


FASE_TXT = {k: {"es": v[0], "en": v[1]} for k, v in am.FASES.items()}


def veredicto(s: dict, lang: str = "es") -> dict:
    """Titular y cuatro parrafos cortos. Cada frase cita el dato que la sustenta."""
    c, i, t, m = s["ciclo"], s["inflacion"], s["tasas"], s["mercado"]
    brecha = lectura_brecha(c["brecha_hp_tiempo_real"])
    post = postura_monetaria(t.get("tpm_real_exante"))
    ancla = anclaje(t.get("bei_5y5y"))
    fase = FASE_TXT[c["fase"]][lang]
    acelera = i["cambio_3m"] > 0.1
    cede = i["cambio_3m"] < -0.1
    fuera = i["total"] > 4 or i["total"] < 2

    if lang == "es":
        pos = {"encima": "por encima de", "debajo": "por debajo de", "cerca": "cerca de"}[brecha]
        dir_inf = "acelerando" if acelera else ("cediendo" if cede else "estable")
        titular = (f"{fase}: la economía opera {pos} su potencial y la inflación "
                   f"({_n(i['total'], 2, lang)}%) está {dir_inf}"
                   + (" fuera del rango meta." if fuera else " dentro del rango meta."))
        act = (f"PIB real {c['trimestre']}: {_n(c['pib_real_yoy'], 1, lang)}% anual. Brecha del producto "
               f"{_n(c['brecha_hp_tiempo_real'], 1, lang, True)}% del potencial (rango entre métodos "
               f"{_n(c['brecha_min'], 1, lang, True)} a {_n(c['brecha_max'], 1, lang, True)}); crecimiento "
               f"potencial estimado {_n(c['crecimiento_potencial_hp'], 1, lang)}%.")
        if s.get("ise"):
            act += (f" El ISE a {s['ise']['fecha']:%m/%Y} crece {_n(s['ise']['yoy'], 1, lang)}% anual y "
                    f"{_n(s['ise']['saar_3m'], 1, lang)}% anualizado en el último trimestre móvil.")
        pre = (f"IPC {i['fecha']:%m/%Y}: {_n(i['total'], 2, lang)}% anual, "
               f"{_n(i['cambio_3m'], 2, lang, True)} pp en tres meses; meta 3% ±1 pp.")
        if i.get("basica") is not None:
            pre += f" Inflación básica (sin alimentos ni regulados): {_n(i['basica'], 2, lang)}%."
        pol = ""
        if t.get("tpm") is not None:
            pol = (f"Tasa de política {_n(t['tpm'], 2, lang)}%; tasa real ex ante "
                   f"{_n(t['tpm_real_exante'], 1, lang)}% frente a una neutral estimada de "
                   f"{_n(NEUTRAL_REAL[0], 1, lang)}–{_n(NEUTRAL_REAL[1], 1, lang)}%: postura {post}.")
        exp = (f"Los TES descuentan inflación de {_n(t['bei_1y'], 1, lang)}% a un año y "
               f"{_n(t['bei_5y5y'], 1, lang)}% en el tramo 5 a 10 años: expectativas {ancla} "
               f"respecto al techo de 4%.")
        mer = (f"TES 10 años {_n(t['tes_pesos_10y'], 2, lang)}%; COLCAP "
               f"{_n(m['colcap_12m'], 1, lang, True)}% en 12 meses")
        if m.get("colcap_usd_12m") is not None:
            mer += f" ({_n(m['colcap_usd_12m'], 1, lang, True)}% en dólares)"
        if m.get("trm") is not None:
            mer += f"; TRM {_n(m['trm'], 0, lang)} COP/USD ({_n(m['trm_12m'], 1, lang, True)}% en 12 meses)"
        mer += "."
    else:
        pos = {"encima": "above", "debajo": "below", "cerca": "close to"}[brecha]
        dir_inf = "accelerating" if acelera else ("easing" if cede else "stable")
        titular = (f"{fase}: the economy is operating {pos} potential and inflation "
                   f"({_n(i['total'], 2, lang)}%) is {dir_inf}"
                   + (" outside the target range." if fuera else " inside the target range."))
        act = (f"Real GDP {c['trimestre'].replace('T', 'Q')}: {_n(c['pib_real_yoy'], 1, lang)}% y/y. Output gap "
               f"{_n(c['brecha_hp_tiempo_real'], 1, lang, True)}% of potential (range across methods "
               f"{_n(c['brecha_min'], 1, lang, True)} to {_n(c['brecha_max'], 1, lang, True)}); estimated "
               f"potential growth {_n(c['crecimiento_potencial_hp'], 1, lang)}%.")
        if s.get("ise"):
            act += (f" The monthly activity index (ISE, {s['ise']['fecha']:%m/%Y}) grows "
                    f"{_n(s['ise']['yoy'], 1, lang)}% y/y and {_n(s['ise']['saar_3m'], 1, lang)}% 3m/3m annualised.")
        pre = (f"CPI {i['fecha']:%m/%Y}: {_n(i['total'], 2, lang)}% y/y, "
               f"{_n(i['cambio_3m'], 2, lang, True)} pp over three months; target 3% ±1 pp.")
        if i.get("basica") is not None:
            pre += f" Core inflation (ex food and regulated): {_n(i['basica'], 2, lang)}%."
        post_en = {"restrictiva": "restrictive", "neutral": "neutral", "expansiva": "expansionary", None: "n/a"}[post]
        pol = ""
        if t.get("tpm") is not None:
            pol = (f"Policy rate {_n(t['tpm'], 2, lang)}%; ex-ante real rate "
                   f"{_n(t['tpm_real_exante'], 1, lang)}% vs an estimated neutral of "
                   f"{_n(NEUTRAL_REAL[0], 1, lang)}–{_n(NEUTRAL_REAL[1], 1, lang)}%: {post_en} stance.")
        ancla_en = {"desancladas": "de-anchored", "ancladas": "anchored", None: "n/a"}[ancla]
        exp = (f"TES breakevens price {_n(t['bei_1y'], 1, lang)}% inflation one year ahead and "
               f"{_n(t['bei_5y5y'], 1, lang)}% in the 5y5y forward: expectations {ancla_en} "
               f"relative to the 4% ceiling.")
        mer = (f"10-year TES {_n(t['tes_pesos_10y'], 2, lang)}%; COLCAP "
               f"{_n(m['colcap_12m'], 1, lang, True)}% over 12 months")
        if m.get("colcap_usd_12m") is not None:
            mer += f" ({_n(m['colcap_usd_12m'], 1, lang, True)}% in USD)"
        if m.get("trm") is not None:
            mer += f"; USD/COP {_n(m['trm'], 0, lang)} ({_n(m['trm_12m'], 1, lang, True)}% over 12 months)"
        mer += "."
    return {"titular": titular, "actividad": act, "precios": pre, "politica": pol,
            "expectativas": exp, "mercados": mer, "fase": c["fase"], "brecha": brecha,
            "postura": post, "anclaje": ancla}


def tabla_senales(d: Datos, s: dict, lang: str = "es") -> pd.DataFrame:
    """Indicador (nombre sin jerga), ultimo dato, cambio y percentil historico desde 2010."""
    rows = []
    pib_u = "% PIB" if lang == "es" else "% GDP"

    def add(key_es, key_en, df, col, unidad, dias, freq, dec=2, relativo=False):
        if df is None or col not in df or df[col].dropna().empty:
            return
        sub = df.dropna(subset=[col])
        last = sub.iloc[-1]
        prev = _hace(sub, col, last["fecha"], dias)
        rows.append({
            "indicador": key_es if lang == "es" else key_en,
            "valor": float(last[col]), "unidad": unidad, "dec": dec, "freq": freq,
            "fecha": pd.Timestamp(last["fecha"]),
            "cambio": None if prev is None else (100 * (float(last[col]) / prev - 1) if relativo
                                                 else float(last[col] - prev)),
            "relativo": relativo,
            "ventana": dias,
            "percentil": am.percentil(sub[col], float(last[col]), fechas=sub["fecha"]),
        })

    add("Crecimiento de la economía (PIB real, anual)", "Economic growth (real GDP, y/y)",
        d.ciclo, "pib_real_yoy", "%", 365, "q", dec=1)
    add("Producción frente a su capacidad (brecha)", "Output vs capacity (output gap)",
        d.ciclo, "brecha_hp_tiempo_real", "%", 365, "q", dec=1)
    if d.ise is not None:
        add("Actividad económica mensual (ISE, anual)", "Monthly economic activity (ISE, y/y)",
            d.ise, "ise_sa_yoy", "%", 365, "m", dec=1)
    if d.laboral is not None:
        add("Desempleo", "Unemployment rate", d.laboral, "td_sa", "%", 365, "m", dec=1)
    add("Inflación anual", "Inflation, y/y", d.inflacion, "inflacion_anual", "%", 365, "m")
    add("Inflación de fondo (sin alimentos ni regulados)", "Underlying inflation (ex food & regulated)",
        d.inflacion, "inflacion_basica_sar", "%", 365, "m")
    add("Inflación que espera el mercado (próximo año)", "Market-expected inflation (next year)",
        d.tasas, "bei_1y", "%", 91, "d")
    add("Inflación que espera el mercado (largo plazo)", "Market-expected inflation (long term)",
        d.tasas, "bei_5y5y", "%", 91, "d")
    add("Tasa de interés del Banco de la República", "Banco de la República policy rate",
        d.tasas, "tpm", "%", 365, "d")
    add("Tasa de interés real (descontada la inflación esperada)", "Real interest rate (net of expected inflation)",
        d.tasas, "tpm_real_exante", "%", 365, "d")
    add("Bonos del Gobierno a 10 años (TES)", "10-year government bonds (TES)",
        d.tasas, "tes_pesos_10y", "%", 91, "d")
    if not d.extra["trm"].empty:
        add("Dólar (TRM, pesos por dólar)", "US dollar (TRM, pesos per USD)",
            d.extra["trm"], "trm", "", 365, "d", dec=0, relativo=True)
    if not d.extra["itcr_ipc"].empty:
        add("Tasa de cambio real (2010 = 100)", "Real exchange rate (2010 = 100)",
            d.extra["itcr_ipc"], "itcr_ipc", "", 365, "m", dec=1, relativo=True)
    add("Bolsa de Colombia (COLCAP)", "Colombian stock index (COLCAP)",
        d.mercado, "colcap_puntos", "pts", 365, "d", dec=0, relativo=True)
    if not d.extra["cuenta_corriente_pct_pib"].empty:
        add("Cuenta corriente", "Current account", d.extra["cuenta_corriente_pct_pib"],
            "cuenta_corriente_pct_pib", pib_u, 365, "q", dec=1)
    if not d.extra["deuda_bruta_gnc_pct_pib"].empty:
        add("Deuda bruta del Gobierno", "Central government gross debt", d.extra["deuda_bruta_gnc_pct_pib"],
            "deuda_bruta_gnc_pct_pib", pib_u, 365, "y", dec=1)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- lectura para no especialistas
# Estados descriptivos (no recomendaciones). Cada uno se deriva de un umbral explicito.
def estado_crecimiento(pib_yoy: float, potencial: float) -> str:
    if pib_yoy < 0:
        return "contraccion"
    if pib_yoy >= potencial + 1:
        return "fuerte"
    if pib_yoy >= potencial - 1:
        return "normal"
    return "lento"


def estado_inflacion(total: float) -> str:
    if 2 <= total <= 4:
        return "en_meta"
    if total < 2:
        return "baja"
    return "alta" if total > 5 else "sobre_meta"


def estado_desempleo(td: float, td_hace_12m: float | None) -> str:
    if td_hace_12m is None or pd.isna(td_hace_12m):
        return "estable"
    if td < td_hace_12m - 0.3:
        return "mejora"
    if td > td_hace_12m + 0.3:
        return "empeora"
    return "estable"


def nivel_historico(pct: float | None) -> str | None:
    """Traduce un percentil (0-100) a una palabra."""
    if pct is None or pd.isna(pct):
        return None
    if pct < 10:
        return "muy_bajo"
    if pct < 30:
        return "bajo"
    if pct <= 70:
        return "normal"
    if pct <= 90:
        return "alto"
    return "muy_alto"


def resumen_simple(s: dict, lang: str = "es") -> str:
    """Tres frases sin jerga, derivadas de los mismos datos del veredicto tecnico."""
    c, i, t = s["ciclo"], s["inflacion"], s["tasas"]
    ec = estado_crecimiento(c["pib_real_yoy"], c["crecimiento_potencial_hp"])
    ei = estado_inflacion(i["total"])
    post = postura_monetaria(t.get("tpm_real_exante"))
    sube = i["cambio_3m"] > 0.1
    baja = i["cambio_3m"] < -0.1
    if lang == "es":
        crec = {"fuerte": "crece por encima de su ritmo habitual", "normal": "crece a un ritmo normal",
                "lento": "crece lentamente", "contraccion": "se está contrayendo"}[ec]
        f1 = f"La economía {crec} ({_n(c['pib_real_yoy'], 1, lang)}% en el último año)."
        mov = "está subiendo" if sube else ("está bajando" if baja else "se mantiene estable")
        pos = {"en_meta": "dentro del rango meta del Banco de la República (2% a 4%)",
               "baja": "por debajo del rango meta (2% a 4%)",
               "sobre_meta": "por encima del rango meta (2% a 4%)",
               "alta": f"muy por encima de la meta del 3%"}[ei]
        f2 = f"La inflación ({_n(i['total'], 1, lang)}%) {mov} y está {pos}."
        f3 = ""
        if t.get("tpm") is not None:
            efecto = {"restrictiva": "busca frenar la inflación encareciendo el crédito",
                      "neutral": "ni frena ni estimula la economía",
                      "expansiva": "busca estimular la economía abaratando el crédito"}.get(post, "")
            f3 = f"El Banco de la República tiene su tasa de interés en {_n(t['tpm'], 2, lang)}%, un nivel que {efecto}."
    else:
        crec = {"fuerte": "is growing faster than its usual pace", "normal": "is growing at a normal pace",
                "lento": "is growing slowly", "contraccion": "is contracting"}[ec]
        f1 = f"The economy {crec} ({_n(c['pib_real_yoy'], 1, lang)}% over the past year)."
        mov = "rising" if sube else ("falling" if baja else "stable")
        pos = {"en_meta": "within Banco de la República's 2%–4% target range",
               "baja": "below the 2%–4% target range",
               "sobre_meta": "above the 2%–4% target range",
               "alta": "well above the 3% target"}[ei]
        f2 = f"Inflation ({_n(i['total'], 1, lang)}%) is {mov} and {pos}."
        f3 = ""
        if t.get("tpm") is not None:
            efecto = {"restrictiva": "aims to curb inflation by making credit more expensive",
                      "neutral": "neither slows nor stimulates the economy",
                      "expansiva": "aims to stimulate the economy with cheaper credit"}.get(post, "")
            f3 = f"Banco de la República's policy rate is {_n(t['tpm'], 2, lang)}%, a level that {efecto}."
    return " ".join(x for x in (f1, f2, f3) if x)
