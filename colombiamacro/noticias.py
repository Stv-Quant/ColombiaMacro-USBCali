"""Publicaciones oficiales recientes, generadas a partir de los datos descargados.

No se copian titulares de prensa: cada entrada resume el ultimo dato que publico una
entidad oficial (DANE, Banco de la Republica, BVC) y enlaza a su pagina oficial.
Asi la seccion es verificable, se actualiza sola y no depende de sitios que bloquean
lectores automaticos.
"""

from __future__ import annotations

import pandas as pd

from colombiamacro import modelo as mt

ENLACES = {
    "pib": "https://www.dane.gov.co/index.php/estadisticas-por-tema/cuentas-nacionales/cuentas-nacionales-trimestrales/pib-informacion-tecnica",
    "ipc": "https://www.dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/indice-de-precios-al-consumidor-ipc",
    "empleo": "https://www.dane.gov.co/index.php/estadisticas-por-tema/mercado-laboral/empleo-y-desempleo",
    "informal": "https://www.dane.gov.co/index.php/estadisticas-por-tema/mercado-laboral/empleo-informal-y-seguridad-social",
    "ise": "https://www.dane.gov.co/index.php/estadisticas-por-tema/cuentas-nacionales/indicador-de-seguimiento-a-la-economia-ise",
    "tpm": "https://suameca.banrep.gov.co/estadisticas-economicas/informacionSerie/59/tasas_interes_politica_monetaria",
    "comunicados": "https://suameca.banrep.gov.co/estadisticas-economicas/informacionSerie/59/tasas_interes_politica_monetaria",
    "trm": "https://suameca.banrep.gov.co/estadisticas-economicas/informacionSerie/1/tasa_cambio_peso_colombiano_trm_dolar_usd",
    "bop": "https://suameca.banrep.gov.co/estadisticas-economicas/informacionSerie/4130/cuenta_corriente_como_porcentaje_pib",
    "tes": "https://suameca.banrep.gov.co/estadisticas-economicas/informacionSerie/220002/tasas_interes_cero_cupon_tes",
    "colcap": "https://suameca.banrep.gov.co/estadisticas-economicas/informacionSerie/2500/indice_mercado_accionario_colcap",
}
SALAS = [  # salas de prensa oficiales (enlaces fijos)
    ("Banco de la República · comunicados y minutas", "https://www.banrep.gov.co/es/noticias"),
    ("DANE · sala de prensa", "https://www.dane.gov.co/index.php/sala-de-prensa"),
    ("Ministerio de Hacienda · noticias", "https://www.minhacienda.gov.co"),
    ("Superintendencia Financiera · noticias", "https://www.superfinanciera.gov.co"),
]


def _n(x, dec=1, lang="es", signo=False):
    s = f"{x:+,.{dec}f}" if signo else f"{x:,.{dec}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".") if lang == "es" else s


MESES = {"es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
                "noviembre", "diciembre"],
         "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                "November", "December"]}


def _mes(f, lang):
    f = pd.Timestamp(f)
    return f"{MESES[lang][f.month - 1]} {f.year}" if lang == "en" else f"{MESES[lang][f.month - 1]} de {f.year}"


def _trim(f, lang):
    f = pd.Timestamp(f)
    q = (f.month - 1) // 3 + 1
    return f"T{q} {f.year}" if lang == "es" else f"Q{q} {f.year}"


def _sube(v, lang, fem=False):
    if lang == "en":
        return "rose" if v > 0.05 else ("fell" if v < -0.05 else "was unchanged")
    return "subió" if v > 0.05 else ("bajó" if v < -0.05 else ("se mantuvo estable" if not fem else "se mantuvo estable"))


def _pub(df, col="fecha_publicacion_vintage"):
    if df is None or col not in df:
        return None
    f = pd.to_datetime(df[col], format="%Y-%m-%d", errors="coerce").dropna()
    return None if f.empty else f.max()


def publicaciones(d: mt.Datos, s: dict, lang: str = "es") -> list[dict]:
    """Lista de publicaciones (mas reciente primero): fecha, fuente, titular, detalle, enlace."""
    es = lang == "es"
    out = []

    def add(fecha, fuente, titular, detalle, enlace, aprox=False):
        if fecha is not None and not pd.isna(fecha):
            out.append({"fecha": pd.Timestamp(fecha), "fuente": fuente, "titular": titular, "detalle": detalle,
                        "enlace": enlace, "aprox": aprox})

    c = s.get("ciclo") or {}
    if c:
        pub = _pub(d.pib)
        add(pub, "DANE",
            (f"La economía creció {_n(c['pib_real_yoy'], 1, lang)}% en el {_trim(c['fecha'], lang)}" if es else
             f"The economy grew {_n(c['pib_real_yoy'], 1, lang)}% in {_trim(c['fecha'], lang)}"),
            (f"Producto interno bruto real frente al mismo trimestre del año anterior. Ritmo habitual estimado: "
             f"{_n(c['crecimiento_potencial_hp'], 1, lang)}%." if es else
             f"Real GDP versus the same quarter a year earlier. Estimated usual pace: {_n(c['crecimiento_potencial_hp'], 1, lang)}%."),
            ENLACES["pib"])
    i = s.get("inflacion") or {}
    if i:
        pub = _pub(d.ipc) or (i["fecha"] + pd.DateOffset(months=1, days=4))
        cambio = i["total"] - i["hace_12m"] if i.get("hace_12m") is not None else 0
        add(pub, "DANE",
            (f"La inflación anual fue {_n(i['total'], 2, lang)}% en {_mes(i['fecha'], lang)}" if es else
             f"Annual inflation was {_n(i['total'], 2, lang)}% in {_mes(i['fecha'], lang)}"),
            (f"Variación del mes: {_n(i['mensual'], 2, lang)}%. Hace un año: {_n(i['hace_12m'], 1, lang)}% "
             f"({_n(cambio, 1, lang, True)} pp). Meta del Banco de la República: 3%." if es else
             f"Monthly change: {_n(i['mensual'], 2, lang)}%. A year ago: {_n(i['hace_12m'], 1, lang)}% "
             f"({_n(cambio, 1, lang, True)} pp). Central bank target: 3%."),
            ENLACES["ipc"])
    lb = s.get("laboral") or {}
    if lb:
        add(lb["fecha"] + pd.DateOffset(months=1, days=29), "DANE",
            (f"El desempleo fue {_n(lb['td'], 1, lang)}% en {_mes(lb['fecha'], lang)}" if es else
             f"Unemployment was {_n(lb['td'], 1, lang)}% in {_mes(lb['fecha'], lang)}"),
            (f"Serie desestacionalizada. Hace un año: {_n(lb['td_hace_12m'], 1, lang)}%." if es else
             f"Seasonally adjusted. A year ago: {_n(lb['td_hace_12m'], 1, lang)}%."),
            ENLACES["empleo"], aprox=True)
    inf = d.informalidad
    if inf is not None and not inf.empty:
        u = inf.iloc[-1]
        prev = inf[inf["fecha"] <= u["fecha"] - pd.DateOffset(years=1)]
        dv = u["nacional"] - prev.iloc[-1]["nacional"] if not prev.empty else 0
        add(u["fecha"] + pd.DateOffset(months=1, days=10), "DANE",
            (f"La informalidad laboral fue {_n(u['nacional'], 1, lang)}% (trimestre terminado en {_mes(u['fecha'], lang)})" if es else
             f"Labour informality was {_n(u['nacional'], 1, lang)}% (quarter ending {_mes(u['fecha'], lang)})"),
            (f"{_sube(dv, lang, True).capitalize()} {_n(abs(dv), 1, lang)} pp en un año. 13 ciudades: {_n(u['ciudades_13'], 1, lang)}%." if es else
             f"{_sube(dv, lang).capitalize()} {_n(abs(dv), 1, lang)} pp over a year. 13 cities: {_n(u['ciudades_13'], 1, lang)}%."),
            ENLACES["informal"], aprox=True)
    ise = s.get("ise") or {}
    if ise:
        add(ise["fecha"] + pd.DateOffset(months=1, days=18), "DANE",
            (f"La actividad económica (ISE) creció {_n(ise['yoy'], 1, lang)}% anual en {_mes(ise['fecha'], lang)}" if es else
             f"Economic activity (ISE) grew {_n(ise['yoy'], 1, lang)}% y/y in {_mes(ise['fecha'], lang)}"),
            ("Indicador mensual de seguimiento a la economía, sin efectos de temporada." if es else
             "Monthly economic activity indicator, seasonally adjusted."),
            ENLACES["ise"], aprox=True)
    tt = s.get("tasas") or {}
    if tt.get("tpm") is not None:
        uc = tt.get("tpm_ultimo_cambio") or {}
        if uc:
            dlt = uc["delta"]
            verbo = ("subió" if dlt > 0 else "bajó") if es else ("raised" if dlt > 0 else "cut")
            add(uc["fecha"], "Banco de la República",
                (f"El Banco de la República {verbo} su tasa en {_n(abs(dlt) * 100, 0, lang)} puntos básicos, a {_n(tt['tpm'], 2, lang)}%" if es else
                 f"Banco de la República {verbo} its policy rate by {_n(abs(dlt) * 100, 0, lang)} bp to {_n(tt['tpm'], 2, lang)}%"),
                (f"Última decisión con cambio de tasa (vigente desde esta fecha). Hace un año la tasa era {_n(tt['tpm_hace_12m'], 2, lang)}%." if es else
                 f"Latest rate change (effective from this date). A year ago the rate was {_n(tt['tpm_hace_12m'], 2, lang)}%."),
                ENLACES["comunicados"])
    an = tt.get("tpm_anunciada") if tt else None
    if an:
        sube = an["tasa"] > an["anterior"]
        add(an["anuncio"], "Banco de la República",
            (f"La Junta del Banco de la República {'subió' if sube else 'bajó'} la tasa de política a {_n(an['tasa'], 2, lang)}%" if es else
             f"Banco de la República's board {'raised' if sube else 'cut'} the policy rate to {_n(an['tasa'], 2, lang)}%"),
            (f"Anuncio del {an['anuncio']:%d/%m/%Y}; antes {_n(an['anterior'], 2, lang)}%. Rige desde el {an['vigente']:%d/%m/%Y}, cuando entra a la serie oficial." if es else
             f"Announced {an['anuncio']:%Y-%m-%d}; previously {_n(an['anterior'], 2, lang)}%. Effective {an['vigente']:%Y-%m-%d}, when it enters the official series."),
            an["enlace"] or ENLACES["tpm"])
    m = s.get("mercado") or {}
    if m.get("trm") is not None:
        add(m["trm_fecha"], "Banco de la República",
            (f"El dólar (TRM) quedó en ${_n(m['trm'], 0, lang)}" if es else f"The dollar (TRM) stood at COP {_n(m['trm'], 0, lang)}"),
            (f"{_n(m['trm_12m'], 1, lang, True)}% en un año (una cifra negativa significa peso más fuerte)." if es else
             f"{_n(m['trm_12m'], 1, lang, True)}% over a year (negative means a stronger peso)."),
            ENLACES["trm"])
    if m.get("colcap") is not None:
        add(m["fecha"], "BVC",
            (f"El COLCAP cerró en {_n(m['colcap'], 0, lang)} puntos" if es else f"The COLCAP closed at {_n(m['colcap'], 0, lang)} points"),
            (f"{_n(m['colcap_12m'], 1, lang, True)}% en doce meses." if es else f"{_n(m['colcap_12m'], 1, lang, True)}% over twelve months."),
            ENLACES["colcap"])
    if tt.get("tes_pesos_10y") is not None:
        add(tt["fecha"], "Banco de la República",
            (f"El bono del Gobierno a 10 años (TES) rinde {_n(tt['tes_pesos_10y'], 2, lang)}%" if es else
             f"The 10-year government bond (TES) yields {_n(tt['tes_pesos_10y'], 2, lang)}%"),
            (f"Inflación que descuenta el mercado para el próximo año: {_n(tt['bei_1y'], 1, lang)}%; para los años 5 a 10: "
             f"{_n(tt['bei_5y5y'], 1, lang)}%." if es else
             f"Market-implied inflation next year: {_n(tt['bei_1y'], 1, lang)}%; for years 5 to 10: {_n(tt['bei_5y5y'], 1, lang)}%."),
            ENLACES["tes"])
    cc = s.get("cc")
    if cc:
        add(cc["fecha"] + pd.DateOffset(months=5, days=20), "Banco de la República",
            (f"Déficit de cuenta corriente: {_n(abs(cc['valor']), 1, lang)}% del PIB en el {_trim(cc['fecha'], lang)}" if es else
             f"Current account deficit: {_n(abs(cc['valor']), 1, lang)}% of GDP in {_trim(cc['fecha'], lang)}"),
            ("Balanza de pagos: lo que el país necesita financiar con recursos del exterior." if es else
             "Balance of payments: what the country needs to finance from abroad."),
            ENLACES["bop"], aprox=True)
    hoy = pd.Timestamp.today().normalize()
    for o in out:  # una fecha aproximada nunca puede quedar en el futuro
        if o["fecha"] > hoy:
            o["fecha"] = hoy
    return sorted(out, key=lambda o: o["fecha"], reverse=True)
