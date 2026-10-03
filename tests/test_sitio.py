"""Pruebas del sitio estatico: construye en una carpeta temporal y revisa lo esencial."""

import json
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from colombiamacro import modelo as mt
from colombiamacro.sitio import construir as cs
from colombiamacro.sitio.textos import T


class TestCambios(unittest.TestCase):
    def test_cambio_pp_y_pct(self):
        x = pd.date_range("2020-01-31", periods=25, freq="ME")
        y = list(range(25))
        pp = cs.serie_cambio(x, y, "pp", "a")
        self.assertTrue(pp.iloc[:12].isna().all())
        self.assertAlmostEqual(pp.iloc[12], 12.0)
        pct = cs.serie_cambio(x, [100.0] * 12 + [110.0] * 13, "pct", "a")
        self.assertAlmostEqual(pct.iloc[12], 10.0)

    def test_sin_dato_cercano_no_inventa_cambio(self):
        x = pd.to_datetime(["2020-01-01", "2021-06-01"])
        self.assertTrue(cs.serie_cambio(x, [1, 2], "pp", "a").isna().all())

    def test_texto_cambio(self):
        self.assertEqual(cs.txt_cambio(0.34, "pp", "es"), "▲ +0,3 pp")
        self.assertEqual(cs.txt_cambio(-2.0, "pct", "en"), "▼ -2.0%")
        self.assertEqual(cs.txt_cambio(float("nan"), "pp", "es"), "")


class TestSitio(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = cs.construir(Path(cls.tmp.name) / "site")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    PAGINAS = {"ciclo": ("ciclo-app", "ciclo-datos"), "crecimiento": ("crecimiento", "crec-medidas", "crec-velocidad", "crec-precios", "crec-quien", "crec-demanda", "crec-inversion", "crec-hogares", "crec-persona", "crec-amplitud", "crec-nivel", "crec-literatura", "sectores"),
               "capacidad": ("capacidad", "cap-medidas", "cap-sectores", "cap-laboral", "cap-regiones", "cap-estructura", "cap-literatura"), "empleo": ("informalidad", "emp-medidas", "emp-ramas", "emp-posicion", "emp-genero", "emp-jovenes", "emp-area", "emp-ciudades", "emp-literatura"), "inflacion": ("precios", "inf-medidas", "inf-aportes", "inf-bienes", "inf-difusion", "inf-ingresos", "inf-ciudades", "inf-literatura"), "tasas": ("banco",),
               "curva-tes": ("curva", "curva-app"), "mercados": ("mercados",), "empresas": ("empresas",),
               "externo": ("externo",), "comercio": ("comercio-cifras", "comercio-flujos", "comercio-vende", "comercio-compra", "comercio-socios"), "indicadores": ("indicadores", "fuentes", "noticias")}

    def leer(self, *partes):
        return (self.out.joinpath(*partes) / "index.html").read_text(encoding="utf-8")

    def test_portada_de_sondeo_sin_graficos(self):
        for raiz in ((), ("en",)):
            html_ = self.leer(*raiz)
            for slug in ("crecimiento", "empleo", "inflacion", "tasas", "curva-tes", "mercados", "externo", "comercio"):
                self.assertIn(f'id="p-{slug}"', html_)
                self.assertIn(f'class="tile-go" href="{slug}/"', html_)
            self.assertIn('class="tile-go" href="crecimiento/#sectores"', html_)    # sectores vive dentro de crecimiento
            for sid in ("lectura", "monitor", "descargas", "noticias"):
                self.assertIn(f'id="{sid}"', html_)
            self.assertIn("class='tbl'", html_)                      # indicadores y fuentes
            self.assertNotIn('.csv" download', html_)                 # la portada solo cita fuentes; descargas en Datos
            self.assertIn('href="indicadores/#fuentes"', html_)
            self.assertEqual(html_.count('class="tile"'), 12)        # rejilla completa (4 filas de 3)
            self.assertNotIn('data-for="', html_)                     # sin graficos en la portada
            self.assertNotIn("plotly.min.js", html_)
            self.assertIn("logo_financialtools.png", html_)
            self.assertIn('href="ciclo/"', html_)
        self.assertIn('lang="es"', self.leer())
        self.assertIn('lang="en"', self.leer("en"))
        self.assertIn('datos/inflacion_clean.csv" download', self.leer("indicadores"))
        self.assertIn('href="../../datos/', self.leer("en", "indicadores"))

    def test_paginas_de_detalle_en_dos_idiomas(self):
        for slug, ids in self.PAGINAS.items():
            for raiz in ((), ("en",)):
                html_ = self.leer(*raiz, slug)
                for sid in ids:
                    self.assertIn(f'id="{sid}"', html_, (raiz, slug, sid))
                self.assertIn('aria-current="page"', html_)
                self.assertIn('class="pager"', html_)
                self.assertIn('assets/estilo.css', html_)

    def test_enlaces_relativos_correctos(self):
        self.assertIn('href="../en/inflacion/"', self.leer("inflacion"))
        self.assertIn('href="../../inflacion/"', self.leer("en", "inflacion"))
        self.assertIn('src="../assets/app.js', self.leer("inflacion"))
        self.assertIn('src="../../assets/app.js', self.leer("en", "inflacion"))
        self.assertIn('href="../../datos/tasas_interes_clean.csv"', self.leer("en", "indicadores"))

    def test_secciones_numeradas_en_orden(self):
        import re
        for slug in self.PAGINAS:
            nums = [int(n) for n in re.findall(r'<span class="sec-num">(\d+)</span>', self.leer(slug))]
            self.assertEqual(nums, list(range(1, len(nums) + 1)), slug)

    def test_menu_no_usa_textos_de_metodo(self):
        es = self.leer()
        menu = es[es.index('<nav class="menu"'):es.index("</nav>")]
        self.assertNotIn("Método", menu)
        self.assertIn("Inflación", menu)
        self.assertIn('class="grp-b"', menu)

    def test_archivos_y_descargas(self):
        for f in ("assets/app.js", "assets/estilo.css", "assets/plotly.min.js", "assets/curva_tes.json",
                  "assets/fondo_andes.svg", "assets/fondo_billete.svg", "assets/fuentes/inter-tight-latin-500-normal.woff2",
                  "resumen.json", ".nojekyll", "datos/tasas_interes_clean.csv"):
            self.assertTrue((self.out / f).exists(), f)

    def test_curva_tes_completa(self):
        c = json.loads((self.out / "assets" / "curva_tes.json").read_text(encoding="utf-8"))
        n = len(c["f"])
        self.assertGreater(n, 4000)
        self.assertEqual(c["f"], sorted(c["f"]))
        for col in cs.TES_COLS:
            self.assertEqual(len(c[col]), n)
        self.assertTrue(all(v is not None for v in c["tes_pesos_10y"]))
        d = mt.cargar()
        ult = d.tasas.dropna(subset=["tes_pesos_10y"]).iloc[-1]
        self.assertAlmostEqual(c["tes_pesos_10y"][-1], round(float(ult["tes_pesos_10y"]), 3))

    def test_graficos_json_validos(self):
        n = 0
        for partes in [(), *[(slug,) for slug in self.PAGINAS]]:
            for bloque in self.leer(*partes).split('<script type="application/json" data-for="')[1:]:
                data = bloque.split('">', 1)[1].split("</script>", 1)[0]
                self.assertIn("data", json.loads(data))
                n += 1
        self.assertGreaterEqual(n, 22)


class TestPanelesDeCambio(unittest.TestCase):
    def test_graficos_principales_tienen_panel_de_cambio(self):
        d = mt.cargar()
        g = cs.Graficos(d, mt.instantanea(d), "es")
        for nombre in ("crecimiento", "inflacion", "expectativas", "bolsa", "brecha", "anclaje"):
            fig, _ = getattr(g, nombre)()
            ejes = {getattr(tr, "yaxis", None) or "y" for tr in fig.data}
            self.assertIn("y2", ejes, nombre)

    def test_2020_no_queda_fuera_de_escala(self):
        d = mt.cargar()
        fig, meta = cs.Graficos(d, mt.instantanea(d), "es").crecimiento()
        self.assertIsNone(fig.layout.yaxis.range)   # el navegador ajusta la escala a los datos visibles
        self.assertNotIn("yfijo", meta)


class TestRelojCiclo(unittest.TestCase):
    def test_datos_del_reloj_coinciden_con_el_modelo(self):
        d = mt.cargar()
        r = cs.datos_ciclo(d, "es")
        c = d.ciclo.dropna(subset=["brecha_hp_tiempo_real", "delta_brecha", "fase"])
        self.assertEqual(len(r["trimestres"]), len(c))
        ult = r["trimestres"][-1]
        self.assertAlmostEqual(ult["x"], round(float(c["brecha_hp_tiempo_real"].iloc[-1]), 3))
        self.assertEqual(ult["fase"], c["fase"].iloc[-1])
        self.assertEqual(set(r["fases"]), {"expansion", "desaceleracion", "contraccion", "recuperacion"})
        for p in r["trimestres"]:   # la fase es coherente con el cuadrante
            esperada = ("expansion" if p["y"] >= 0 else "desaceleracion") if p["x"] >= 0 else (
                "recuperacion" if p["y"] >= 0 else "contraccion")
            self.assertEqual(p["fase"], esperada, p["q"])


class TestTextos(unittest.TestCase):
    def test_todas_las_claves_bilingues(self):
        for k, v in T.items():
            self.assertEqual(len(v), 2, k)
            self.assertTrue(all(isinstance(x, str) and x for x in v), k)


if __name__ == "__main__":
    unittest.main()
