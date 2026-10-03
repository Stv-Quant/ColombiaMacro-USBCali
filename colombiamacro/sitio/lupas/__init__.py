"""Lupa de cada grafico: que cuenta, como se lee, por que importa, como interpretarlo y formulas (ES, EN).

El contenido vive en los modulos g*.py (uno por grupo de paginas). inyectar() agrega a cada pagina los textos de los
graficos que contiene, junto con la fuente y la metodologia de fichas.py, y la ventana que app.js llena al abrir.
"""
from __future__ import annotations

import importlib
import json
import pkgutil
import re

LUPAS: dict = {}
for _m in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
    LUPAS.update(importlib.import_module(f"{__name__}.{_m.name}").LUPAS)

ETIQ = {
    "es": {"k": "Lupa · cómo leer este gráfico", "que": "Qué nos cuenta", "hoy": "Lo que muestra hoy", "leer": "Cómo se lee",
           "importa": "Por qué importa", "interpretar": "Cómo interpretarlo", "formulas": "Fórmulas", "metodo": "Metodología y fuente",
           "fuente": "Fuente", "cerrar": "Cerrar", "abrir": "Lupa: cómo leer e interpretar este gráfico"},
    "en": {"k": "Magnifier · how to read this chart", "que": "What it tells us", "hoy": "What it shows today", "leer": "How to read it",
           "importa": "Why it matters", "interpretar": "How to interpret it", "formulas": "Formulas", "metodo": "Methodology and source",
           "fuente": "Source", "cerrar": "Close", "abrir": "Magnifier: how to read and interpret this chart"},
}
_ID = re.compile(r'<figure class="chart[^"]*"(?: data-lupa="([^"]+)")?>.*?(?:class="plot[^"]*" id="([^"]+)"|</figure>)', re.S)


def claves(html: str) -> list[str]:
    out = []
    for a, b in _ID.findall(html):
        k = a or b
        if k and k not in out:
            out.append(k)
    return out


def inyectar(html: str, L: str) -> str:
    """Agrega los textos de las lupas de los graficos de la pagina y la ventana comun."""
    from colombiamacro.sitio.fichas import ficha
    datos = {}
    for k in claves(html):
        v = LUPAS.get(k, {}).get(L)
        if not v:
            continue
        f = ficha(k, L)
        datos[k] = {**v, "fuente": f[0] if f else "", "metodo": f[1] if f else ""}
    if not datos:
        return html
    e = ETIQ[L]
    js = json.dumps({"t": e, "d": datos}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    dlg = (f'<dialog class="explica lupa-dlg" id="dlg-lupa" aria-labelledby="dlg-lupa-t"><div class="ex-cab"><p class="ex-k">{e["k"]}</p>'
           f'<h2 id="dlg-lupa-t"></h2><button type="button" class="ex-x" data-cerrar aria-label="{e["cerrar"]}">✕</button></div>'
           f'<div class="ex-cuerpo"></div></dialog>'
           f'<script type="application/json" id="lupa-datos">{js}</script>')
    return html.replace("</body>", dlg + "</body>", 1)
