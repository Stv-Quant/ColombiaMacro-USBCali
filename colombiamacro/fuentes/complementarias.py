"""Series complementarias para leer el ciclo: politica monetaria, tipo de cambio,
inflacion basica, sector externo y fiscal (BanRep) + ISE y mercado laboral (DANE).

Salidas
-------
series_banrep.csv   formato largo: fecha, serie, valor, frecuencia, unidad, id_banrep
ise_mensual.csv     ISE DANE (indice 2015=100): original y desestacionalizado, 3 grandes ramas
mercado_laboral.csv GEIH DANE desestacionalizado, total nacional: TGP, TO, TD

Reglas
------
* Cada serie se valida por id y por nombre antes de aceptarse (si BanRep reasigna un
  id el proceso falla en lugar de publicar otra variable).
* Las fechas mensuales se normalizan al primer dia del mes y las trimestrales al
  primer dia del trimestre, igual que pib_colombia.csv e inflacion_clean.csv.
* Se descartan fechas futuras (la meta de inflacion se publica por adelantado).
* Si una fuente falla, las demas se conservan y el proceso termina con codigo 1.

Uso: python -m colombiamacro.fuentes.complementarias [--solo banrep|dane]
"""

from __future__ import annotations

import argparse
import io
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests

from colombiamacro.fuentes.banrep import banrep_ca_bundle, fetch_series, write_if_changed

from colombiamacro.config import data

OUT_BANREP = data("series_banrep.csv")
OUT_ISE = data("ise_mensual.csv")
OUT_LABORAL = data("mercado_laboral.csv")

# serie: (id BanRep, texto esperado en el nombre, frecuencia, unidad, rango valido)
SERIES = {
    "tpm":                     (59,    "politica monetaria",        "diaria",     "% e.a.",        (0, 40)),
    "ibr_overnight":           (15324, "IBR) overnight, efectiva",  "diaria",     "% e.a.",        (0, 40)),
    "trm":                     (1,     "Representativa del Mercado","diaria",     "COP por USD",   (500, 10000)),
    "inflacion_sin_alimentos": (15388, "Inflación sin alimentos",   "mensual",    "% anual",       (-5, 40)),
    "inflacion_basica_sar":    (15390, "sin alimentos ni regulados","mensual",    "% anual",       (-5, 40)),
    "inflacion_nucleo15":      (15392, "núcleo 15",                 "mensual",    "% anual",       (-5, 40)),
    "inflacion_regulados":     (15398, "regulados",                 "mensual",    "% anual",       (-20, 60)),
    "inflacion_alimentos":     (15404, "Alimentos y bebidas",       "mensual",    "% anual",       (-20, 60)),
    "meta_inflacion":          (853,   "Meta de inflación",         "anual",      "%",             (0, 40)),
    "itcr_ipc":                (235,   "tasa de cambio real",       "mensual",    "indice 2010=100", (30, 250)),
    "terminos_intercambio":    (15360, "términos de intercambio",   "mensual",    "indice",        (20, 400)),
    "reservas_netas_musd":     (15051, "Reservas internacionales netas", "mensual", "millones USD", (-1000, 500000)),  # negativas en los anos sesenta
    "cuenta_corriente_pct_pib":(15290, "Cuenta corriente, porcentaje del PIB, trimestral", "trimestral", "% PIB", (-20, 20)),
    "ied_musd":                (15133, "Inversión Extranjera Directa en Colombia", "trimestral", "millones USD", (-20000, 40000)),
    "deuda_bruta_gnc_pct_pib": (15328, "Deuda Bruta del GNC",       "anual",      "% PIB",         (0, 200)),
    "salario_minimo_var":      (15418, "Salario mínimo mensual, variación anual", "anual", "% anual", (-5, 60)),
}
MIN_OBS = {"diaria": 1000, "mensual": 60, "trimestral": 40, "anual": 10}


def normalize_dates(fechas: pd.Series, frecuencia: str) -> pd.Series:
    if frecuencia == "mensual":
        return fechas.dt.to_period("M").dt.to_timestamp()
    if frecuencia == "trimestral":
        return fechas.dt.to_period("Q").dt.to_timestamp()
    if frecuencia == "anual":
        return fechas.dt.to_period("Y").dt.to_timestamp()
    return fechas


def validar_serie(name: str, df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza fechas y aplica los controles de una serie. Lanza ValueError si falla."""
    serie_id, _, freq, unit, (lo, hi) = SERIES[name]
    d = df.rename(columns={name: "valor"}).copy()
    d["fecha"] = normalize_dates(d["fecha"], freq)
    # Periodo aun no iniciado = dato futuro (p. ej. meta del ano siguiente).
    d = d[d["fecha"] <= pd.Timestamp.today().normalize()]
    d = d.drop_duplicates("fecha", keep="last")
    if len(d) < MIN_OBS[freq]:
        raise ValueError(f"solo {len(d)} observaciones (minimo {MIN_OBS[freq]})")
    fuera = d.loc[~d["valor"].between(lo, hi)]
    if not fuera.empty:
        raise ValueError(f"{len(fuera)} valores fuera de [{lo}, {hi}], p. ej. "
                         f"{fuera.iloc[0]['fecha']:%Y-%m-%d}={fuera.iloc[0]['valor']}")
    d["serie"], d["frecuencia"], d["unidad"], d["id_banrep"] = name, freq, unit, serie_id
    return d[["fecha", "serie", "valor", "frecuencia", "unidad", "id_banrep"]]


def build_long(frames: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, list[str]]:
    """Tabla larga con las series validas y lista de errores de las que no pasan.

    Una serie que no pasa sus controles se excluye; nunca bloquea a las demas.
    """
    rows, errores = [], []
    for name, df in frames.items():
        try:
            rows.append(validar_serie(name, df))
        except ValueError as exc:
            errores.append(f"{name}: {exc}")
    if not rows:
        return pd.DataFrame(columns=["fecha", "serie", "valor", "frecuencia", "unidad", "id_banrep"]), errores
    out = pd.concat(rows, ignore_index=True)
    return out.sort_values(["serie", "fecha"]).reset_index(drop=True), errores


def descargar_con_reintentos(serie_id, name, expected, bundle, intentos=3):
    ultimo = None
    for k in range(intentos):
        try:
            return fetch_series(serie_id, name, expected, verify=bundle, drop_future=False)
        except Exception as exc:  # red intermitente o limite de tasa del servidor
            ultimo = exc
            time.sleep(2 * (k + 1))
    raise ultimo


def actualizar_banrep() -> bool:
    frames, errores = {}, []
    with banrep_ca_bundle() as bundle:
        for name, (serie_id, expected, *_rest) in SERIES.items():
            try:
                frames[name] = descargar_con_reintentos(serie_id, name, expected, bundle)
                print(f"  {name:<26} id {serie_id:<6} {len(frames[name]):>6} obs "
                      f"hasta {frames[name]['fecha'].max().date()}")
            except Exception as exc:  # una serie caida no borra las demas
                errores.append(f"{name}: descarga fallida: {exc}")
            time.sleep(0.5)  # cortesia con el servidor de BanRep
    table, invalidas = build_long(frames)
    errores += invalidas
    if OUT_BANREP.exists():
        # Conservar la ultima version valida de las series que fallaron hoy.
        old = pd.read_csv(OUT_BANREP, parse_dates=["fecha"])
        faltan = set(old["serie"]) - set(table["serie"])
        if faltan:
            table = (pd.concat([table, old[old["serie"].isin(faltan)]], ignore_index=True)
                     .sort_values(["serie", "fecha"]).reset_index(drop=True))
            print(f"  Se conserva la version anterior de: {', '.join(sorted(faltan))}")
    if not table.empty:
        changed = write_if_changed(table, OUT_BANREP, float_format="%.6g")
        print(f"series_banrep.csv: {'actualizado' if changed else 'sin cambios'} "
              f"({table['serie'].nunique()} de {len(SERIES)} series)")
    for e in errores:
        print(f"  ERROR {e}")
    return not errores


# ------------------------------------------------------------------ DANE
MESES = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7,
         "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}
DANE_ISE_PAGE = ("https://www.dane.gov.co/index.php/estadisticas-por-tema/cuentas-nacionales/"
                 "indicador-de-seguimiento-a-la-economia-ise")
DANE_GEIH_PAGE = ("https://www.dane.gov.co/index.php/estadisticas-por-tema/mercado-laboral/"
                  "empleo-y-desempleo")


def parse_dane_block(rows: list[list], labels: dict[str, str]) -> pd.DataFrame:
    """Lee un cuadro DANE con fila 'Concepto' (anos) seguida de fila de meses.

    rows: valores de la hoja (lista de filas). labels: {texto exacto en col A: columna}.
    Solo se lee el primer bloque (hasta 'Fuente'), que contiene los indices o tasas.
    """
    header = next(i for i, r in enumerate(rows) if r and str(r[0]).strip() == "Concepto")
    years, months = rows[header], rows[header + 1]
    end = next((i for i in range(header + 2, len(rows))
                if rows[i] and str(rows[i][0] or "").strip().startswith("Fuente")), len(rows))
    fechas, year = [], None
    for c in range(1, len(months)):
        if c < len(years) and years[c] not in (None, ""):
            year = int(re.match(r"\d{4}", str(years[c]).strip()).group(0))
        if months[c] in (None, ""):
            continue
        month = MESES[str(months[c]).strip().lower()[:3]]
        fechas.append((c, pd.Timestamp(year, month, 1)))
    data = {"fecha": [f for _, f in fechas]}
    body = rows[header + 2:end]
    for label, col in labels.items():
        match = [r for r in body if r and str(r[0] or "").strip() == label]
        if len(match) != 1:
            raise ValueError(f"DANE: fila '{label}' encontrada {len(match)} veces")
        data[col] = [float(match[0][c]) if c < len(match[0]) and match[0][c] not in (None, "") else None
                     for c, _ in fechas]
    df = pd.DataFrame(data).dropna(how="all", subset=list(labels.values()))
    if df["fecha"].duplicated().any() or not df["fecha"].is_monotonic_increasing:
        raise ValueError("DANE: fechas duplicadas o desordenadas")
    return df.reset_index(drop=True)


def _sheet_rows(content: bytes, sheet: str) -> list[list]:
    from openpyxl import load_workbook
    wb = load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    try:
        return [list(r) for r in wb[sheet].values]
    finally:
        wb.close()


def _latest_link(page: str, pattern: str) -> str:
    from bs4 import BeautifulSoup
    html = requests.get(page, timeout=40)
    html.raise_for_status()
    links = [a["href"] for a in BeautifulSoup(html.text, "html.parser").select("a[href]")
             if re.search(pattern, a["href"], re.I)]
    links = list(dict.fromkeys(links))
    if len(links) != 1:
        raise ValueError(f"DANE: se esperaba un anexo vigente para {pattern}, hay {len(links)}")
    return urljoin(page, links[0])


def actualizar_ise() -> None:
    url = _latest_link(DANE_ISE_PAGE, r"/anex-ISE-9actividades-[a-z]{3}20\d{2}\.xlsx$")
    content = requests.get(url, timeout=60).content
    labels = {"Indicador de Seguimiento a la Economía": "ise",
              "Actividades primarias": "primarias",
              "Actividades secundarias": "secundarias",
              "Actividades terciarias": "terciarias"}
    orig = parse_dane_block(_sheet_rows(content, "Cuadro 1"), labels)
    sa = parse_dane_block(_sheet_rows(content, "Cuadro 2"), labels)
    table = (orig[["fecha", "ise"]].rename(columns={"ise": "ise_original"})
             .merge(sa.rename(columns={c: f"{c}_sa" for c in labels.values()}), on="fecha", how="outer"))
    table["ise_yoy"] = 100 * (table["ise_original"] / table["ise_original"].shift(12) - 1)
    table["ise_sa_mom"] = 100 * (table["ise_sa"] / table["ise_sa"].shift(1) - 1)
    table["ise_sa_3m3m_saar"] = 100 * ((table["ise_sa"].rolling(3).mean()
                                        / table["ise_sa"].rolling(3).mean().shift(3)) ** 4 - 1)
    table["fuente"] = url
    if len(table) < 200 or not table["ise_sa"].between(20, 400).all():
        raise ValueError("ISE: historia incompleta o fuera de rango")
    changed = write_if_changed(table, OUT_ISE, float_format="%.6f")
    print(f"ISE: {len(table)} meses hasta {table['fecha'].max().date()} "
          f"({'actualizado' if changed else 'sin cambios'})")


def actualizar_laboral() -> None:
    url = _latest_link(DANE_GEIH_PAGE, r"/anex-GEIH-Desestacionalizado-[a-z]{3}20\d{2}\.xlsx$")
    content = requests.get(url, timeout=60).content
    labels = {"Tasa Global de Participación (TGP)": "tgp_sa",
              "Tasa de Ocupación (TO)": "to_sa",
              "Tasa de Desocupación (TD)": "td_sa",
              "Población ocupada": "ocupados_miles_sa",
              "Población desocupada": "desocupados_miles_sa",
              "Población fuera de la fuerza de trabajo": "fuera_ft_miles_sa"}
    table = parse_dane_block(_sheet_rows(content, "Total nacional"), labels)
    table["td_sa_3m"] = table["td_sa"].rolling(3).mean()
    table["fuente"] = url
    if len(table) < 200 or not table["td_sa"].between(2, 35).all():
        raise ValueError("GEIH: historia incompleta o fuera de rango")
    changed = write_if_changed(table, OUT_LABORAL, float_format="%.6f")
    print(f"Mercado laboral: {len(table)} meses hasta {table['fecha'].max().date()} "
          f"({'actualizado' if changed else 'sin cambios'})")


def actualizar_dane() -> bool:
    ok = True
    for fn in (actualizar_ise, actualizar_laboral):
        try:
            fn()
        except Exception as exc:
            ok = False
            print(f"  ERROR {fn.__name__}: {exc}")
    return ok


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--solo", choices=["banrep", "dane"])
    args = parser.parse_args()
    ok = True
    if args.solo in (None, "banrep"):
        ok &= actualizar_banrep()
    if args.solo in (None, "dane"):
        ok &= actualizar_dane()
    sys.exit(0 if ok else 1)
