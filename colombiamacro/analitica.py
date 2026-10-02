"""Analitica macro-financiera derivada de las tablas oficiales.

Todas las funciones son puras (entran DataFrames/Series, salen DataFrames/
Series) para poder probarlas y reproducirlas. Ninguna inventa datos: si falta
un insumo devuelven NaN o tablas vacias. Formulas y referencias en
METODOLOGIA.md.

Convenciones
------------
* Tasas en porcentaje efectivo anual (12.4 = 12.4 %).
* Conversiones entre nominal y real usan la identidad de Fisher exacta
  (1+i) = (1+r)(1+pi), no la aproximacion i - pi.
* Las brechas se calculan sobre 100*ln(PIB real desestacionalizado), de modo que
  la brecha se lee en % del producto potencial.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

META_INFLACION = 3.0          # Meta puntual BanRep desde 2010
BANDA_INFLACION = 1.0         # Rango +-1 pp
HP_LAMBDA_TRIMESTRAL = 1600   # Hodrick y Prescott (1997)
HAMILTON_H, HAMILTON_P = 8, 4 # Hamilton (2018): 2 anos adelante, 4 rezagos
MIN_OBS_HP = 20               # 5 anos minimos antes de publicar una brecha en tiempo real


# ---------------------------------------------------------------- Fisher
def fisher_real(nominal_pct, inflation_pct):
    """Tasa real exacta: (1+i)/(1+pi) - 1, en %."""
    return 100 * ((1 + np.asarray(nominal_pct, float) / 100)
                  / (1 + np.asarray(inflation_pct, float) / 100) - 1)


def breakeven(tes_pesos_pct, tes_uvr_pct):
    """Inflacion implicita (breakeven) = (1+y_pesos)/(1+y_uvr) - 1, en %.

    Incluye prima por riesgo inflacionario y diferencias de liquidez entre TES
    pesos y UVR; no es una expectativa pura. El rezago de indexacion de la UVR
    (~1 mes) se ignora en plazos >= 1 ano.
    """
    return fisher_real(tes_pesos_pct, tes_uvr_pct)


def tabla_tasas(tes: pd.DataFrame, tpm: pd.DataFrame | None, ipc: pd.DataFrame) -> pd.DataFrame:
    """Tabla diaria de curva, breakevens y tasas reales.

    tes: fecha, tes_pesos_{1,5,10}y, tes_uvr_{1,5,10}y
    tpm: fecha, tpm (tasa de politica, opcional)
    ipc: fecha (mes), inflacion_anual
    """
    out = tes[["fecha", "tes_pesos_1y", "tes_pesos_5y", "tes_pesos_10y",
               "tes_uvr_1y", "tes_uvr_5y", "tes_uvr_10y"]].copy().sort_values("fecha")
    for h in ("1y", "5y", "10y"):
        out[f"bei_{h}"] = breakeven(out[f"tes_pesos_{h}"], out[f"tes_uvr_{h}"])
    # Forward 5y5y de inflacion implicita: ancla de largo plazo usada por bancos centrales.
    f_nom = ((1 + out["tes_pesos_10y"] / 100) ** 10 / (1 + out["tes_pesos_5y"] / 100) ** 5) ** (1 / 5)
    f_real = ((1 + out["tes_uvr_10y"] / 100) ** 10 / (1 + out["tes_uvr_5y"] / 100) ** 5) ** (1 / 5)
    out["bei_5y5y"] = 100 * (f_nom / f_real - 1)
    out["pendiente_10y_1y"] = out["tes_pesos_10y"] - out["tes_pesos_1y"]

    # Inflacion observada vigente en cada dia: la del ultimo mes publicado, no la del
    # mes calendario (el IPC de agosto se conoce en septiembre). Rezago conservador de
    # un mes + 10 dias para no usar un dato antes de su publicacion.
    inf = ipc[["fecha", "inflacion_anual"]].dropna().copy()
    inf["disponible"] = inf["fecha"] + pd.offsets.MonthBegin(1) + pd.Timedelta(days=10)
    out = pd.merge_asof(out, inf[["disponible", "inflacion_anual"]].sort_values("disponible"),
                        left_on="fecha", right_on="disponible", direction="backward")
    out = out.drop(columns="disponible")
    if tpm is not None and not tpm.empty:
        out = pd.merge_asof(out, tpm[["fecha", "tpm"]].sort_values("fecha"),
                            on="fecha", direction="backward")
        out["tpm_real_exante"] = fisher_real(out["tpm"], out["bei_1y"])
        out["tpm_real_expost"] = fisher_real(out["tpm"], out["inflacion_anual"])
        out["pendiente_10y_tpm"] = out["tes_pesos_10y"] - out["tpm"]
    return out


def saltos_aislados(s: pd.Series, umbral: float = 1.0, tolerancia: float = 0.5) -> pd.Series:
    """Punto que se aleja > umbral de ambos vecinos mientras los vecinos difieren < tolerancia.

    Generaliza el control de validar_datos (2 pp / 1 pp) para series derivadas, donde un
    salto de un dia en una sola tasa UVR se amplifica (p. ej. el forward 5y5y).
    """
    prev, nxt = s.shift(1), s.shift(-1)
    return ((s - prev).abs() > umbral) & ((s - nxt).abs() > umbral) & ((prev - nxt).abs() < tolerancia)


def depurar_derivadas(tasas: pd.DataFrame, cols=("bei_1y", "bei_5y", "bei_10y", "bei_5y5y",
                                                  "tpm_real_exante")) -> tuple[pd.DataFrame, int]:
    out = tasas.copy()
    n = 0
    for col in cols:
        if col in out:
            mask = saltos_aislados(out[col])
            n += int(mask.sum())
            out.loc[mask, col] = np.nan
    return out, n


# ---------------------------------------------------------------- brecha del producto
def hp_trend(y: np.ndarray, lamb: float = HP_LAMBDA_TRIMESTRAL) -> np.ndarray:
    """Filtro HP de dos colas resolviendo (I + lamb*D'D) tau = y (sistema denso)."""
    y = np.asarray(y, float)
    n = y.size
    if n < 3:
        return y.copy()
    d = np.zeros((n - 2, n))
    for i in range(n - 2):
        d[i, i:i + 3] = (1.0, -2.0, 1.0)
    return np.linalg.solve(np.eye(n) + lamb * d.T @ d, y)


def hp_one_sided(y: pd.Series, lamb: float = HP_LAMBDA_TRIMESTRAL,
                 min_obs: int = MIN_OBS_HP) -> pd.Series:
    """HP en tiempo real: para cada t se filtra solo y[0..t] y se toma el ultimo punto.

    Evita el sesgo de fin de muestra y el uso de informacion futura del HP de dos
    colas (Orphanides y van Norden, 2002). Devuelve la tendencia.
    """
    y = y.dropna()
    trend = pd.Series(np.nan, index=y.index)
    values = y.to_numpy()
    for t in range(min_obs - 1, len(values)):
        trend.iloc[t] = hp_trend(values[: t + 1], lamb)[-1]
    return trend


def hamilton_cycle(y: pd.Series, h: int = HAMILTON_H, p: int = HAMILTON_P,
                   regressors: pd.Series | None = None) -> pd.Series:
    """Hamilton (2018): y_{t+h} - E[y_{t+h} | 1, x_t, ..., x_{t-p+1}].

    `regressors` permite estimar con una serie depurada (p. ej. sin COVID) y medir
    el ciclo contra el dato observado `y`.
    """
    y = y.dropna()
    x_src = (regressors if regressors is not None else y).reindex(y.index)
    frame = pd.DataFrame({"target": x_src})
    for k in range(p):
        frame[f"lag{k}"] = x_src.shift(h + k)
    frame = frame.dropna()
    x = np.column_stack([np.ones(len(frame)), frame.filter(like="lag").to_numpy()])
    beta, *_ = np.linalg.lstsq(x, frame["target"].to_numpy(), rcond=None)
    fitted = pd.Series(x @ beta, index=frame.index)
    return (y - fitted).reindex(y.index)


# Trimestres tratados como choque atipico al estimar la tendencia: confinamiento
# (2020-T2) hasta el paro nacional (2021-T2). La brecha se sigue midiendo contra el
# dato observado; solo la tendencia se estima con la serie interpolada.
COVID_DESDE, COVID_HASTA = "2020-04-01", "2021-04-01"


def serie_sin_covid(y: pd.Series) -> pd.Series:
    mask = (y.index >= pd.Timestamp(COVID_DESDE)) & (y.index <= pd.Timestamp(COVID_HASTA))
    clean = y.copy()
    clean[mask] = np.nan
    return clean.interpolate(method="index", limit_area="inside")


FASES = {
    "expansion": ("Expansión", "Expansion", "#1a7f4b"),
    "desaceleracion": ("Desaceleración", "Slowdown", "#b7791f"),
    "contraccion": ("Contracción", "Contraction", "#c0392b"),
    "recuperacion": ("Recuperación", "Recovery", "#2b6cb0"),
}


def fase(gap: float, delta: float) -> str | None:
    """Reloj del ciclo (OECD): cuadrante segun nivel de la brecha y su direccion."""
    if pd.isna(gap) or pd.isna(delta):
        return None
    if gap >= 0:
        return "expansion" if delta >= 0 else "desaceleracion"
    return "recuperacion" if delta >= 0 else "contraccion"


def tabla_ciclo(pib: pd.DataFrame) -> pd.DataFrame:
    """Brecha del producto (HP tiempo real, HP dos colas, Hamilton) y fase del ciclo.

    pib: fecha, trimestre, pib_real_ajustado_miles_millones_ref2015, pib_real_yoy, pib_real_qoq_sa
    """
    df = pib.sort_values("fecha").set_index("fecha")
    y = 100 * np.log(df["pib_real_ajustado_miles_millones_ref2015"].astype(float))
    out = pd.DataFrame(index=df.index)
    out["trimestre"] = df["trimestre"]
    out["pib_real_yoy"] = df["pib_real_yoy"]
    out["pib_real_qoq_sa"] = df["pib_real_qoq_sa"]
    out["pib_real_qoq_saar"] = 100 * ((1 + df["pib_real_qoq_sa"] / 100) ** 4 - 1)
    y_trend_input = serie_sin_covid(y)
    tr = hp_one_sided(y_trend_input)
    out["brecha_hp_tiempo_real"] = y - tr
    out["brecha_hp_dos_colas"] = y - pd.Series(hp_trend(y_trend_input.to_numpy()), index=y.index)
    out["brecha_hamilton"] = hamilton_cycle(y, regressors=y_trend_input)
    # Crecimiento potencial: tendencia HP de dos colas (mejor estimacion ex post; la
    # version en tiempo real se reporta aparte porque oscila con el rebote de 2021-22).
    tr2 = pd.Series(hp_trend(y_trend_input.to_numpy()), index=y.index)
    out["crecimiento_potencial_hp"] = 100 * (np.exp((tr2 - tr2.shift(4)) / 100) - 1)
    out["crecimiento_potencial_hp_rt"] = 100 * (np.exp((tr - tr.shift(4)) / 100) - 1)
    gaps = out[["brecha_hp_tiempo_real", "brecha_hp_dos_colas", "brecha_hamilton"]]
    out["brecha_min"] = gaps.min(axis=1)
    out["brecha_max"] = gaps.max(axis=1)
    out["metodos_brecha_positiva"] = (gaps > 0).sum(axis=1)
    out["metodos_disponibles"] = gaps.notna().sum(axis=1)
    # Direccion suavizada: cambio de la brecha en 2 trimestres (reduce ruido de 1 dato).
    out["delta_brecha"] = out["brecha_hp_tiempo_real"].diff(2)
    out["fase"] = [fase(g, d) for g, d in zip(out["brecha_hp_tiempo_real"], out["delta_brecha"])]
    ham_delta = out["brecha_hamilton"].diff(2)
    out["fase_hamilton"] = [fase(g, d) for g, d in zip(out["brecha_hamilton"], ham_delta)]
    out["fases_coinciden"] = out["fase"].eq(out["fase_hamilton"]) & out["fase_hamilton"].notna()
    return out.reset_index()


# ---------------------------------------------------------------- inflacion
def regimen_inflacion(ipc: pd.DataFrame) -> pd.DataFrame:
    """Posicion frente a la meta 3% +-1 y direccion (cambio de 3 meses de la anual)."""
    df = ipc[["fecha", "inflacion_mensual", "inflacion_anual"]].dropna(subset=["inflacion_anual"]).copy()
    df = df.sort_values("fecha").reset_index(drop=True)
    df["desvio_meta_pp"] = df["inflacion_anual"] - META_INFLACION
    df["cambio_3m_pp"] = df["inflacion_anual"].diff(3)
    # Anualizada 3 meses (momentum). Sin desestacionalizar: la columna se muestra como
    # referencia y se advierte la estacionalidad de enero-marzo.
    comp = (1 + df["inflacion_mensual"] / 100).rolling(3).apply(np.prod, raw=True)
    df["anualizada_3m"] = 100 * (comp ** 4 - 1)
    df["en_rango"] = df["inflacion_anual"].between(META_INFLACION - BANDA_INFLACION,
                                                   META_INFLACION + BANDA_INFLACION)
    return df


# ---------------------------------------------------------------- mercados
def tabla_mercado(colcap: pd.DataFrame, trm: pd.DataFrame | None, ipc: pd.DataFrame) -> pd.DataFrame:
    """COLCAP en COP, USD y real; drawdown desde maximo."""
    df = colcap[["fecha", "colcap_puntos"]].dropna().sort_values("fecha").copy()
    df["drawdown_pct"] = 100 * (df["colcap_puntos"] / df["colcap_puntos"].cummax() - 1)
    if trm is not None and not trm.empty:
        df = pd.merge_asof(df, trm[["fecha", "trm"]].sort_values("fecha"), on="fecha",
                           direction="backward", tolerance=pd.Timedelta(days=7))
        df["colcap_usd"] = df["colcap_puntos"] / df["trm"]
    return df


def retorno_ventana(series: pd.Series, fechas: pd.Series, dias: int) -> float:
    """Retorno % entre el ultimo dato y el ultimo dato disponible hace `dias` dias."""
    s = pd.Series(series.to_numpy(), index=pd.to_datetime(fechas)).dropna()
    if s.empty:
        return np.nan
    fin = s.index.max()
    base = s[s.index <= fin - pd.Timedelta(days=dias)]
    if base.empty:
        return np.nan
    return 100 * (s.iloc[-1] / base.iloc[-1] - 1)


def percentil(series: pd.Series, value: float, desde: str | None = "2010-01-01",
              fechas: pd.Series | None = None) -> float:
    """Percentil historico (0-100) del valor actual, para leer que tan extremo es."""
    s = series
    if fechas is not None and desde is not None:
        s = series[pd.to_datetime(fechas) >= pd.Timestamp(desde)]
    s = s.dropna()
    if s.empty or pd.isna(value):
        return np.nan
    return float(100 * (s <= value).mean())


# ============================================================ ciclo ampliado (v12.3)
# Todo lo de esta seccion describe el presente con datos observados: no proyecta.

HP_LAMBDA_MENSUAL = 129600          # Ravn y Uhlig (2002): equivalente mensual de 1.600
COVID_MES_DESDE, COVID_MES_HASTA = "2020-03-01", "2021-06-01"
CF_BANDA = (6, 32)                   # Baxter y King / Christiano y Fitzgerald: 1,5 a 8 anos
BN_REZAGOS = 4


def cf_filter(y: pd.Series, low: int = CF_BANDA[0], high: int = CF_BANDA[1]) -> pd.Series:
    """Christiano y Fitzgerald (2003), filtro asimetrico de paso de banda para un paseo
    aleatorio con deriva. Devuelve el componente ciclico (periodos entre low y high)."""
    s = y.dropna()
    x = s.to_numpy(dtype=float)
    n = len(x)
    x = x - (x[-1] - x[0]) / (n - 1) * np.arange(n)          # quitar la deriva
    a, b = 2 * np.pi / high, 2 * np.pi / low
    j = np.arange(1, n + 1)
    Bj = np.r_[(b - a) / np.pi, (np.sin(j * b) - np.sin(j * a)) / (j * np.pi)]
    c = np.empty(n)
    for i in range(n):
        # pesos de los extremos elegidos para que el filtro sume cero (elimina la raiz unitaria)
        w_fin = -0.5 * Bj[0] - np.sum(Bj[1:-i - 2])
        w_ini = -Bj[0] - np.sum(Bj[1:-i - 2]) - np.sum(Bj[1:i]) - w_fin
        c[i] = (Bj[0] * x[i] + np.dot(Bj[1:-i - 2], x[i + 1:-1]) + w_fin * x[-1]
                + np.dot(Bj[1:i], x[1:i][::-1]) + w_ini * x[0])
    return pd.Series(c, index=s.index).reindex(y.index)


def bn_cycle(y: pd.Series, p: int = BN_REZAGOS, estimar_con: pd.Series | None = None) -> pd.Series:
    """Descomposicion de Beveridge y Nelson (1981) con un AR(p) para el crecimiento.
    Ciclo = -(crecimiento esperado futuro por encima de la media). Se estima con la serie
    depurada (estimar_con) y se evalua sobre el dato observado."""
    base = (estimar_con if estimar_con is not None else y).dropna()
    dy = base.diff().dropna()
    mu = dy.mean()
    x = (dy - mu).to_numpy()
    X = np.column_stack([x[p - k - 1:len(x) - k - 1] for k in range(p)])
    phi = np.linalg.lstsq(X, x[p:], rcond=None)[0]
    F = np.zeros((p, p))
    F[0] = phi
    F[1:, :-1] = np.eye(p - 1)
    A = F @ np.linalg.inv(np.eye(p) - F)
    dyo = (y.diff() - mu).to_numpy()
    out = np.full(len(y), np.nan)
    for t in range(p, len(y)):
        estado = dyo[t - p + 1:t + 1][::-1]
        if not np.isnan(estado).any():
            out[t] = -(A @ estado)[0]
    return pd.Series(out, index=y.index)


NOMBRES_METODOS = {
    "brecha_hp_tiempo_real": ("HP en tiempo real", "Real-time HP"),
    "brecha_hp_dos_colas": ("HP dos colas", "Two-sided HP"),
    "brecha_hamilton": ("Hamilton (2018)", "Hamilton (2018)"),
    "brecha_cf": ("Christiano-Fitzgerald", "Christiano-Fitzgerald"),
    "brecha_bn": ("Beveridge-Nelson", "Beveridge-Nelson"),
}


def brechas_consenso(pib: pd.DataFrame, ciclo: pd.DataFrame) -> pd.DataFrame:
    """Cinco medidas de la brecha del producto y su resumen (mediana, rango, cuantas positivas)."""
    df = pib.sort_values("fecha").set_index("fecha")
    y = 100 * np.log(df["pib_real_ajustado_miles_millones_ref2015"].astype(float))
    yc = serie_sin_covid(y)
    out = ciclo.set_index("fecha")[["brecha_hp_tiempo_real", "brecha_hp_dos_colas", "brecha_hamilton"]].copy()
    trend_cf = yc - cf_filter(yc)
    out["brecha_cf"] = (y - trend_cf).reindex(out.index)
    out["brecha_bn"] = bn_cycle(y, estimar_con=yc).reindex(out.index)
    m = out[list(NOMBRES_METODOS)]
    out["mediana"] = m.median(axis=1)
    out["minimo"] = m.min(axis=1)
    out["maximo"] = m.max(axis=1)
    out["positivos"] = (m > 0).sum(axis=1)
    out["disponibles"] = m.notna().sum(axis=1)
    return out.reset_index()


def _sin_covid_mensual(s: pd.Series) -> pd.Series:
    c = s.copy()
    c[(c.index >= pd.Timestamp(COVID_MES_DESDE)) & (c.index <= pd.Timestamp(COVID_MES_HASTA))] = np.nan
    return c.interpolate(method="index", limit_area="inside")


def brecha_mensual(nivel: pd.Series, min_obs: int = 36) -> pd.Series:
    """Brecha mensual (%): log del indice frente a su tendencia HP en tiempo real (lambda 129.600)."""
    y = 100 * np.log(nivel.astype(float).dropna())
    tr = hp_one_sided(_sin_covid_mensual(y), lamb=HP_LAMBDA_MENSUAL, min_obs=min_obs)
    return y - tr


def ciclo_mensual(ise: pd.DataFrame) -> pd.DataFrame:
    """Brecha del ISE y fase mensual; tambien la brecha de las tres grandes ramas."""
    s = ise.set_index("fecha").sort_index()
    out = pd.DataFrame(index=s.index)
    out["brecha"] = brecha_mensual(s["ise_sa"])
    out["delta_3m"] = out["brecha"].diff(3)
    out["fase"] = [fase(g, dl) for g, dl in zip(out["brecha"], out["delta_3m"])]
    for rama in ("primarias", "secundarias", "terciarias"):
        col = f"{rama}_sa"
        if col in s:
            out[f"brecha_{rama}"] = brecha_mensual(s[col])
            out[f"yoy_{rama}"] = 100 * (s[col] / s[col].shift(12) - 1)
    out["yoy"] = s.get("ise_sa_yoy")
    out["ritmo_3m"] = s.get("ise_sa_3m3m_saar")
    return out.reset_index()


def brecha_sectores(sectores: pd.DataFrame) -> pd.DataFrame:
    """Brecha de cada sector del PIB frente a su propia tendencia HP en tiempo real."""
    niv = sectores.pivot(index="fecha", columns="sector", values="nivel").sort_index()
    out = {}
    for s_ in niv:
        y = 100 * np.log(niv[s_].astype(float))
        out[s_] = y - hp_one_sided(serie_sin_covid(y))
    return pd.DataFrame(out)


def difusion(brechas: pd.DataFrame) -> pd.Series:
    """Indice de difusion: % de sectores sobre su tendencia (promedio de 2 trimestres)."""
    pct = (brechas > 0).sum(axis=1) / brechas.notna().sum(axis=1) * 100
    return pct.where(brechas.notna().sum(axis=1) > 0).rolling(2).mean()


def giros_clasicos(nivel: pd.Series, ventana: int = 6) -> list[tuple[pd.Timestamp, str, float]]:
    """Picos (P) y valles (V) del nivel, en la linea de Bry y Boschan (1971): extremos locales
    del promedio movil de 3 meses en ventanas de +/- `ventana` meses, alternados."""
    s = nivel.astype(float).rolling(3, center=True).mean().dropna()
    v, idx = s.to_numpy(), s.index
    giros = []
    for i in range(ventana, len(v) - ventana):
        tramo = v[i - ventana:i + ventana + 1]
        if v[i] == tramo.max():
            giros.append((idx[i], "P", float(v[i])))
        elif v[i] == tramo.min():
            giros.append((idx[i], "V", float(v[i])))
    alt = []
    for g in giros:
        if alt and alt[-1][1] == g[1]:
            if (g[1] == "P" and g[2] > alt[-1][2]) or (g[1] == "V" and g[2] < alt[-1][2]):
                alt[-1] = g
        else:
            alt.append(g)
    while alt and alt[0][1] == "V" and len(alt) > 1 and alt[1][1] == "P" and alt[0][0] < alt[1][0] and \
            (alt[1][0].to_period("M") - alt[0][0].to_period("M")).n < 6:
        alt.pop(0)                                             # valle espurio al inicio de la muestra
    return alt


def episodios(nivel: pd.Series, giros: list) -> tuple[list[dict], list[dict]]:
    """Recesiones (pico->valle) y expansiones (valle->pico o valle->hoy) con duracion y variacion."""
    s = nivel.astype(float).rolling(3, center=True).mean()
    rec, exp_ = [], []
    for a, b in zip(giros, giros[1:]):
        meses = (b[0].to_period("M") - a[0].to_period("M")).n
        reg = {"desde": a[0], "hasta": b[0], "meses": meses, "variacion": 100 * (b[2] / a[2] - 1), "en_curso": False}
        (rec if a[1] == "P" else exp_).append(reg)
    if giros and giros[-1][1] == "V":
        a = giros[-1]
        ult = nivel.dropna()
        exp_.append({"desde": a[0], "hasta": ult.index[-1], "meses": (ult.index[-1].to_period("M") - a[0].to_period("M")).n,
                     "variacion": 100 * (float(s.dropna().iloc[-1]) / a[2] - 1), "en_curso": True})
    return rec, exp_


def okun(brecha: pd.Series, desempleo_mensual: pd.Series) -> dict:
    """Ley de Okun en brechas: desempleo frente a su tendencia (pp) contra brecha del producto (%).
    Excluye 2020-2021. Devuelve la serie trimestral de ambas y la pendiente estimada."""
    td = desempleo_mensual.astype(float).resample("QS").mean()
    tdc = serie_sin_covid(td).dropna()
    brecha_u = td - pd.Series(hp_trend(tdc.to_numpy()), index=tdc.index)
    J = pd.concat([brecha.rename("brecha"), brecha_u.rename("brecha_u")], axis=1, sort=True).dropna()
    Jn = J[(J.index < "2020-01-01") | (J.index > "2021-12-31")]
    pend, cte = np.polyfit(Jn["brecha"], Jn["brecha_u"], 1)
    return {"serie": J, "pendiente": float(pend), "constante": float(cte), "correlacion": float(Jn.corr().iloc[0, 1]), "n": len(Jn)}
