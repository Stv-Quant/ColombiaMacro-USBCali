"""Genera los documentos PDF de ColombiaMacro a partir del sitio construido.

  docs/Manual_ColombiaMacro.pdf  Codex de lectura: como usar el sitio, fundamentos con formulas, atlas de todos los
                                 graficos (captura + lupa: que cuenta, como se lee, por que importa, como interpretarlo,
                                 formulas, metodologia y fuente), interpretacion en conjunto y referencia.
  docs/METODOLOGIA.pdf           Nota metodologica (docs/METODOLOGIA.md convertida con pandoc + XeLaTeX).

Requisitos: sitio construido en site/ (python -m colombiamacro.sitio.construir), Playwright con Chromium, XeLaTeX y
pandoc. Uso: python scripts/codex.py [--sin-capturas] [--solo manual|metodologia]
"""
from __future__ import annotations

import argparse
import asyncio
import html as H
import io
import re
import shutil
import subprocess
import sys
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
SITIO = RAIZ / "site"
DOCS = RAIZ / "docs"
MAN = DOCS / "manual"
FIG = MAN / "fig"
ORDEN = ["ciclo", "crecimiento", "capacidad", "empleo", "inflacion", "tasas", "curva-tes", "mercados", "empresas",
         "externo", "comercio"]


# ------------------------------------------------------------------ HTML -> LaTeX
_ESC = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
_MATE = {"Δ": r"\Delta", "Σ": r"\Sigma", "≈": r"\approx", "≤": r"\le", "≥": r"\ge", "≠": r"\neq", "λ": r"\lambda",
         "π": r"\pi", "β": r"\beta", "σ": r"\sigma", "μ": r"\mu", "ε": r"\varepsilon", "τ": r"\tau", "ρ": r"\rho",
         "α": r"\alpha", "γ": r"\gamma", "θ": r"\theta", "φ": r"\phi", "ω": r"\omega", "δ": r"\delta", "√": r"\surd",
         "∞": r"\infty", "→": r"\rightarrow", "←": r"\leftarrow", "↔": r"\leftrightarrow", "±": r"\pm", "∈": r"\in",
         "∑": r"\Sigma", "∆": r"\Delta", "·": r"\cdot", "⋅": r"\cdot", "×": r"\times", "÷": r"\div", "∂": r"\partial",
         "κ": r"\kappa", "ȳ": r"\bar{y}", "Ȳ": r"\bar{Y}", "ŷ": r"\hat{y}", "ŝ": r"\hat{s}", "η": r"\eta", "ν": r"\nu", "ξ": r"\xi", "χ": r"\chi", "ψ": r"\psi", "Π": r"\Pi",
         "Ω": r"\Omega", "Γ": r"\Gamma", "Λ": r"\Lambda", "Φ": r"\Phi", "Θ": r"\Theta", "∏": r"\Pi", "≡": r"\equiv",
         "∝": r"\propto", "⇒": r"\Rightarrow", "∀": r"\forall", "∧": r"\wedge", "∨": r"\vee", "⌊": r"\lfloor",
         "⌋": r"\rfloor", "′": r"'", "∣": r"\mid", "‖": r"\|", "∫": r"\int", "ϕ": r"\phi", "ℓ": r"\ell"}
_SUBS = {"₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4", "₅": "5", "₆": "6", "₇": "7", "₈": "8", "₉": "9",
         "ₜ": "t", "ᵢ": "i", "ⱼ": "j", "ₖ": "k", "ₙ": "n"}
_SUPS = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
         "⁻": "−", "ⁿ": "n", "ᵗ": "t"}


def _texto(s: str) -> str:
    """Escapa texto plano (sin etiquetas) para LaTeX."""
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        nxt = s[i + 1] if i + 1 < len(s) else ""
        if nxt in ("\u0304", "\u0305"):                      # letra con barra (promedio)
            out.append(r"$\bar{\mathrm{" + c + "}}$" if c.isupper() else r"$\bar{" + c + "}$")
            i += 2
            continue
        if c == "\u0302":
            i += 1
            continue
        if c in _ESC:
            out.append(_ESC[c])
        elif c in _MATE:
            out.append("$" + _MATE[c] + "$")
        elif c in _SUBS:
            out.append(r"\textsubscript{" + _SUBS[c] + "}")
        elif c in _SUPS:
            out.append(r"\textsuperscript{" + _SUPS[c] + "}")
        elif c in "\u200b\ufeff":
            pass
        else:
            out.append(c)
        i += 1
    return "".join(out).replace("$$", "")


def tex(h: str) -> str:
    """Convierte el HTML limitado de las lupas y fichas (b, i, em, strong, sub, sup, br) a LaTeX."""
    if not h:
        return ""
    h = H.unescape(str(h))
    partes = re.split(r"(</?[a-zA-Z][^<>]*>)", h)
    out = []
    for p in partes:
        if not re.match(r"</?[a-zA-Z]", p):
            out.append(_texto(p))
            continue
        t = p.lower().replace(" ", "")
        mapa = {"<sub>": r"\textsubscript{", "<sup>": r"\textsuperscript{", "<b>": r"\textbf{", "<strong>": r"\textbf{",
                "<i>": r"\emph{", "<em>": r"\emph{"}
        if t in mapa:
            out.append(mapa[t])
        elif t in ("</sub>", "</sup>", "</b>", "</strong>", "</i>", "</em>"):
            out.append("}")
        elif t.startswith("<br"):
            out.append(r"\newline ")
    return "".join(out)


# ------------------------------------------------------------------ lectura del sitio
def leer_pagina(slug: str, L: str = "es") -> dict:
    f = SITIO / (("en/" if L == "en" else "") + slug) / "index.html"
    s = f.read_text(encoding="utf-8")
    titulo = H.unescape(re.sub("<[^>]+>", "", re.search(r"<h1>(.*?)</h1>", s, re.S).group(1)))
    lede = H.unescape(re.sub("<[^>]+>", "", (re.search(r'<p class="summary">(.*?)</p>', s, re.S) or [None, ""])[1]))
    ruta = re.search(r'<nav class="crumbs"[^>]*>(.*?)</nav>', s, re.S)
    nav = H.unescape(re.sub("<[^>]+>", "|", ruta.group(1))).split("|")[-1].strip() if ruta else slug
    secciones = []
    for m in re.finditer(r'<section id="([^"]+)" class="(?:section|cycle)[^"]*">(.*?)</section>', s, re.S):
        sid, cuerpo = m.group(1), m.group(2)
        h2 = re.search(r"<h2>(.*?)</h2>", cuerpo, re.S)
        figs = []
        for fm in re.finditer(r'<figure class="chart[^"]*"(?: data-lupa="([^"]+)")?>(.*?)</figure>', cuerpo, re.S):
            pl = re.search(r'class="plot[^"]*" id="([^"]+)"', fm.group(2))
            k = fm.group(1) or (pl.group(1) if pl else None)
            cap = re.search(r"<figcaption>(.*?)</figcaption>", fm.group(2), re.S)
            cap_t = re.sub(r"<button.*?</button>|<span class=\"amp-n\">.*?</span>", "", cap.group(1) if cap else "", flags=re.S)
            if k:
                figs.append((k, H.unescape(re.sub("<[^>]+>", "", cap_t)).strip()))
        refs = [(H.unescape(re.sub("<[^>]+>", "", a)), H.unescape(re.sub("<[^>]+>", "", b)))
                for a, b in re.findall(r'<span class="ref">(.*?)</span><span class="ref-u">(.*?)</span>', cuerpo, re.S)]
        secciones.append({"id": sid, "titulo": H.unescape(re.sub("<[^>]+>", "", h2.group(1))) if h2 else "",
                          "figs": figs, "refs": refs})
    return {"slug": slug, "titulo": titulo, "lede": lede, "nav": nav, "secciones": secciones}


# ------------------------------------------------------------------ capturas
class _Silencioso(SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


async def _capturar(claves_por_pagina: dict[str, list[str]], puerto: int) -> None:
    from playwright.async_api import async_playwright
    from PIL import Image
    FIG.mkdir(parents=True, exist_ok=True)
    css = (".rv{opacity:1!important;transform:none!important}.lupa-btn,.exp-btn,.ex-q,.how,.ficha,.note,.info"
           "{display:none!important}figure.chart{box-shadow:none!important}")
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1280, "height": 900}, device_scale_factor=1.5)
        for slug, claves in claves_por_pagina.items():
            await pg.goto(f"http://127.0.0.1:{puerto}/{slug}/")
            await pg.evaluate("document.documentElement.setAttribute('data-theme','light')")
            await pg.add_style_tag(content=css)
            await pg.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
            await pg.wait_for_timeout(1500)
            for k in claves:
                sel = f'figure[data-lupa="{k}"]' if k.startswith("v-") else f'figure.chart:has(#{k})'
                el = pg.locator(sel).first
                try:
                    await el.scroll_into_view_if_needed()
                    await pg.wait_for_timeout(250)
                    png = await el.screenshot()
                except Exception as exc:                       # un grafico que no se pudo capturar no detiene el resto
                    print(f"  sin captura {k}: {exc}")
                    continue
                im = Image.open(io.BytesIO(png)).convert("RGB")
                if im.width > 1500:
                    im = im.resize((1500, round(im.height * 1500 / im.width)), Image.LANCZOS)
                im.save(FIG / f"{k}.jpg", "JPEG", quality=74, optimize=True, progressive=True)
            print(f"  capturas {slug}: {len(claves)}")
        await b.close()


def capturas(paginas: list[dict]) -> None:
    srv = ThreadingHTTPServer(("127.0.0.1", 0), partial(_Silencioso, directory=str(SITIO)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        asyncio.run(_capturar({p["slug"]: [k for s in p["secciones"] for k, _ in s["figs"]] for p in paginas},
                              srv.server_address[1]))
    finally:
        srv.shutdown()


# ------------------------------------------------------------------ atlas
def atlas(paginas: list[dict], L: str = "es") -> str:
    from colombiamacro.sitio import lupas
    from colombiamacro.sitio.fichas import ficha
    T = {"es": dict(parte="Atlas de los gráficos", intro=(
        "Esta parte recorre, página por página, todos los gráficos del sitio. Cada ficha reproduce la captura del gráfico "
        "y la explicación de su lupa: qué nos cuenta, cómo se lee, por qué importa, cómo interpretarlo, las fórmulas que "
        "producen las cifras y la metodología con su fuente oficial. Las capturas muestran los datos disponibles en la "
        "fecha de generación de este documento; en el sitio cada gráfico se actualiza solo."),
        que="Qué nos cuenta", leer="Cómo se lee", importa="Por qué importa", interp="Cómo interpretarlo",
        form="Fórmulas", met="Metodología", fuente="Fuente", lit="Lecturas de la página", pag="Página del sitio"),
         "en": dict(parte="Chart atlas", intro="", que="What it tells us", leer="How to read it", importa="Why it matters",
                    interp="How to interpret it", form="Formulas", met="Methodology", fuente="Source",
                    lit="Readings for this page", pag="Site page")}[L]
    o = [r"\part{" + T["parte"] + "}", "", tex(T["intro"]), ""]
    for p in paginas:
        o += [r"\chapter{" + tex(p["nav"]) + "}", r"\label{atlas:" + p["slug"] + "}", "",
              r"{\large\sffamily\bfseries " + tex(p["titulo"]) + r"\par}\medskip", "", tex(p["lede"]), "",
              r"{\small\color{cmmuted}" + T["pag"] + r": \url{https://stv-quant.github.io/ColombiaMacro-USBCali/" +
              p["slug"] + "/}}", ""]
        refs = []
        for s in p["secciones"]:
            refs += s["refs"]
            if not s["figs"]:
                continue
            o += [r"\section{" + tex(s["titulo"]) + "}", ""]
            for k, cap in s["figs"]:
                v = lupas.LUPAS.get(k, {}).get(L)
                if not v:
                    continue
                o += [r"\subsection{" + tex(cap) + "}", r"\label{g:" + k + "}"]
                if (FIG / f"{k}.jpg").exists():
                    o += [r"\begin{center}\includegraphics[width=\linewidth,height=0.42\textheight,keepaspectratio]{fig/"
                          + k + r".jpg}\end{center}"]
                o += [r"\paragraph{" + T["que"] + "}", tex(v["que"]), "",
                      r"\begin{leer}[" + T["leer"] + "]", tex(v["leer"]), r"\end{leer}", "",
                      r"\paragraph{" + T["importa"] + "}", tex(v["importa"]), "",
                      r"\paragraph{" + T["interp"] + "}", r"\begin{itemize}"]
                o += [r"\item " + tex(x) for x in v.get("interpretar", [])]
                o += [r"\end{itemize}"]
                if v.get("formulas"):
                    o += [r"\begin{formulas}[" + T["form"] + "]"]
                    for n, fx, d in v["formulas"]:
                        o += [r"\formula{" + tex(n) + "}{" + tex(fx) + "}{" + tex(d) + "}"]
                    o += [r"\end{formulas}"]
                f = ficha(k, L)
                if f:
                    o += [r"\begin{metodo}[" + T["met"] + "]", tex(f[1]), r"\par\smallskip{\small\textbf{" + T["fuente"] +
                          ":} " + tex(f[0]) + "}", r"\end{metodo}"]
                o += [""]
        if refs:
            o += [r"\section*{" + T["lit"] + "}", r"\begin{itemize}\small"]
            o += [r"\item \textbf{" + tex(a) + "} " + tex(b) for a, b in refs]
            o += [r"\end{itemize}", ""]
    return "\n".join(o)


# ------------------------------------------------------------------ referencias
def referencias_md(md: Path) -> str:
    s = md.read_text(encoding="utf-8")
    i = s.find("## 10. Referencias")
    bloque = s[i:].split("\n", 1)[1] if i >= 0 else ""
    entradas = [re.sub(r"\s+", " ", e).strip() for e in re.split(r"\n\s*\n", bloque) if e.strip()]
    out = [r"\chapter{Referencias}", r"\label{es:r:referencias}", r"\begin{itemize}[leftmargin=1.2em,itemindent=-1.2em]",
           r"\small"]
    for e in entradas:
        if e.startswith("#"):
            break
        e = tex(e)
        e = re.sub(r"\*([^*]+)\*", r"\\emph{\1}", e)
        out.append(r"\item[] " + e)
    out.append(r"\end{itemize}")
    return "\n".join(out)


# ------------------------------------------------------------------ documento
PREAMBULO = r"""\documentclass[11pt,a4paper,openany]{report}
\usepackage{../latex/colombiamacro}
\usepackage{url}
\renewcommand{\chaptermark}[1]{\markboth{#1}{}}
\titleformat{\part}[display]{\sffamily\huge\bfseries\centering\color{cmink}}{\color{cmblue}\large\MakeUppercase{\partname}~\thepart}{1em}{}
\titleformat{\chapter}[hang]{\sffamily\LARGE\bfseries\color{cmink}}{\color{cmblue}\thechapter}{0.6em}{}
\titlespacing*{\chapter}{0pt}{0pt}{1.6em}
\titleformat{\paragraph}[hang]{\sffamily\small\bfseries\color{cmblue}\MakeUppercase}{}{0em}{}
\titlespacing*{\paragraph}{0pt}{1.1ex}{0.4ex}
\setcounter{secnumdepth}{2}\setcounter{tocdepth}{1}
\newfontfamily\formfont{DejaVu Serif}[Scale=0.95]
\newtcolorbox{formulas}[1][Fórmulas]{enhanced,breakable,colback=white,colframe=cmrule,boxrule=0.6pt,arc=2pt,
  left=8pt,right=8pt,top=6pt,bottom=6pt,fonttitle=\sffamily\bfseries\small,coltitle=cmblue,title={#1},
  colbacktitle=white,toptitle=2pt,bottomtitle=0pt}
\newcommand{\formula}[3]{{\sffamily\footnotesize\color{cmmuted}\MakeUppercase{#1}}\par
  {\formfont\large #2}\par{\small\color{cmmuted}#3}\par\smallskip}
\newtcolorbox{metodo}[1][Metodología]{enhanced,breakable,colback=cmsoft!50,colframe=cmrule,boxrule=0pt,leftrule=2pt,
  arc=0pt,left=8pt,right=8pt,top=4pt,bottom=4pt,fontupper=\small,fonttitle=\sffamily\bfseries\small,coltitle=cmmuted,
  attach title to upper={\ },title={#1.}}
\graphicspath{{./}}
\setlength{\emergencystretch}{3em}
\hypersetup{pdftitle={ColombiaMacro · Codex de lectura},pdfauthor={ColombiaMacro · USB Cali}}
"""

PORTADA = r"""\begin{titlepage}
\centering\vspace*{3cm}
{\sffamily\color{cmblue}\large COLOMBIAMACRO · USB CALI\par}\vspace{1.2cm}
{\sffamily\bfseries\fontsize{40}{44}\selectfont Codex\par}\vspace{0.4cm}
{\sffamily\Large Cómo leer, usar e interpretar\\el monitor de la economía colombiana\par}\vspace{1.6cm}
{\color{cmmuted}\rule{0.5\linewidth}{0.4pt}\par}\vspace{0.8cm}
{\large Guía completa de lectura de los gráficos, con sus fórmulas,\\su metodología y las fuentes oficiales\par}
\vfill
{\sffamily\small\color{cmmuted} Versión @@VERSION@@ · @@FECHA@@\\
Datos oficiales: DANE · Banco de la República · Ministerio de Hacienda · Supersociedades · Confecámaras\\
\url{https://stv-quant.github.io/ColombiaMacro-USBCali/}\par}
\end{titlepage}
"""


def xelatex(carpeta: Path, nombre: str) -> None:
    for _ in range(3):
        r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", nombre], cwd=carpeta,
                           capture_output=True, text=True)
        if r.returncode != 0:
            log = (carpeta / nombre.replace(".tex", ".log")).read_text(errors="ignore")
            err = re.findall(r"^!.*?(?:\n.*){0,4}", log, re.M)
            raise SystemExit(f"XeLaTeX falló en {nombre}:\n" + "\n".join(err[:3]))


def manual(version: str, fecha: str, paginas: list[dict]) -> Path:
    (MAN / "atlas_es.tex").write_text(atlas(paginas, "es"), encoding="utf-8")
    ref = (MAN / "es" / "05_referencia_base.tex").read_text(encoding="utf-8") + "\n" + referencias_md(DOCS / "METODOLOGIA.md")
    (MAN / "es" / "05_referencia.tex").write_text(ref, encoding="utf-8")
    cuerpo = (PREAMBULO + r"\begin{document}" + "\n" + PORTADA.replace("@@VERSION@@", version).replace("@@FECHA@@", fecha)
              + r"""\pagenumbering{roman}
\tableofcontents
\clearpage\pagenumbering{arabic}
\chapter*{Cómo está organizado este Codex}
\addcontentsline{toc}{chapter}{Cómo está organizado este Codex}
Este documento es la guía de lectura de ColombiaMacro. No describe cómo está construido el sistema: explica qué muestra
cada gráfico, cómo leerlo, qué fórmulas producen sus cifras y cómo interpretar la información, solo y en conjunto.
\begin{itemize}
\item \textbf{Parte I · Cómo usar ColombiaMacro:} el mapa del sitio, la portada y la anatomía de cada página.
\item \textbf{Parte II · Fundamentos:} los conceptos y fórmulas que se repiten en todo el sitio, con ejemplos.
\item \textbf{Parte III · Atlas de los gráficos:} cada gráfico del sitio con su explicación completa.
\item \textbf{Parte IV · Interpretar en conjunto:} cómo se conectan las piezas, una rutina de lectura, preguntas para el
  inversionista, las reglas de los estados automáticos y los errores frecuentes.
\item \textbf{Parte V · Referencia:} limitaciones, glosario español--inglés, siglas, calendario y bibliografía.
\end{itemize}
La metodología estadística detallada está en la \emph{Nota metodológica} (documento PDF aparte).
\begin{alerta}[Aviso]
ColombiaMacro presenta datos oficiales y cálculos descriptivos. No contiene proyecciones ni pronósticos y no constituye
asesoría de inversión.
\end{alerta}
\input{es/01_uso}
\input{es/02_fundamentos}
\input{atlas_es}
\input{es/04_interpretar}
\input{es/05_referencia}
\end{document}
""")
    (MAN / "manual.tex").write_text(cuerpo, encoding="utf-8")
    xelatex(MAN, "manual.tex")
    destino = DOCS / "Manual_ColombiaMacro.pdf"
    shutil.copy(MAN / "manual.pdf", destino)
    return destino


METODO_DOC = r"""\documentclass[11pt,a4paper]{article}
\usepackage{../latex/colombiamacro}
\usepackage{url}
\usepackage{calc}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\providecommand{\pandocbounded}[1]{#1}
\setcounter{secnumdepth}{0}
\setlength{\emergencystretch}{3em}
\fancyhead[R]{\sffamily\footnotesize\color{cmmuted}Nota metodológica}
\hypersetup{pdftitle={ColombiaMacro · Nota metodológica},pdfauthor={ColombiaMacro · USB Cali}}
\begin{document}
\begin{titlepage}
\centering\vspace*{3cm}
{\sffamily\color{cmblue}\large COLOMBIAMACRO · USB CALI\par}\vspace{1.2cm}
{\sffamily\bfseries\fontsize{34}{40}\selectfont Nota metodológica\par}\vspace{0.6cm}
{\sffamily\Large Fuentes, transformaciones, métodos y reglas\\del monitor de la economía colombiana\par}
\vfill
{\sffamily\small\color{cmmuted}Versión @@VERSION@@ · @@FECHA@@\\ \url{https://stv-quant.github.io/ColombiaMacro-USBCali/}\par}
\end{titlepage}
\tableofcontents\clearpage
\input{metodologia_cuerpo}
\end{document}
"""


def metodologia(version: str, fecha: str) -> Path:
    carpeta = DOCS / "metodologia"
    carpeta.mkdir(exist_ok=True)
    md = (DOCS / "METODOLOGIA.md").read_text(encoding="utf-8")
    md = re.sub(r"\A# .*?\n+\*[^\n]*\*\n", "", md, count=1)              # titulo y version van en la portada
    r = subprocess.run(["pandoc", "-f", "markdown", "-t", "latex", "--top-level-division=section", "-o",
                        str(carpeta / "metodologia_cuerpo.tex")], input=md, text=True, capture_output=True)
    if r.returncode != 0:
        raise SystemExit("pandoc: " + r.stderr)
    cuerpo = (carpeta / "metodologia_cuerpo.tex").read_text(encoding="utf-8")
    cuerpo = cuerpo.replace(r"\section{", r"\section{", ).replace("\\begin{longtable}[]", "\\small\\begin{longtable}[]")
    cuerpo = re.sub(r"(\\end\{longtable\})", r"\1\\normalsize", cuerpo)
    (carpeta / "metodologia_cuerpo.tex").write_text(cuerpo, encoding="utf-8")
    (carpeta / "metodologia.tex").write_text(METODO_DOC.replace("@@VERSION@@", version).replace("@@FECHA@@", fecha),
                                             encoding="utf-8")
    xelatex(carpeta, "metodologia.tex")
    destino = DOCS / "METODOLOGIA.pdf"
    shutil.copy(carpeta / "metodologia.pdf", destino)
    return destino


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--sin-capturas", action="store_true", help="usa las capturas que ya existen en docs/manual/fig")
    ap.add_argument("--solo", choices=["manual", "metodologia"])
    ap.add_argument("--version", default="12.19")
    ap.add_argument("--fecha", default="octubre de 2026")
    a = ap.parse_args()
    if a.solo != "metodologia":
        paginas = [leer_pagina(s) for s in ORDEN if (SITIO / s / "index.html").exists()]
        if not a.sin_capturas:
            capturas(paginas)
        print("Manual:", manual(a.version, a.fecha, paginas))
    if a.solo != "manual":
        print("Metodología:", metodologia(a.version, a.fecha))


if __name__ == "__main__":
    main()
