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

    def test_paginas_en_dos_idiomas(self):
        es = (self.out / "index.html").read_text(encoding="utf-8")
        en = (self.out / "en" / "index.html").read_text(encoding="utf-8")
        for html_ in (es, en):
            for sid in ("crecimiento", "precios", "banco", "curva", "mercados", "empresas", "externo", "indicadores", "fuentes"):
                self.assertIn(f'id="{sid}"', html_)
            self.assertIn('id="curva-app"', html_)
            self.assertIn('id="ciclo-app"', html_)
            self.assertIn('id="ciclo-datos"', html_)
            self.assertIn('class="stats"', html_)
        self.assertIn('lang="es"', es)
        self.assertIn('lang="en"', en)

    def test_menu_no_usa_textos_de_metodo(self):
        es = (self.out / "index.html").read_text(encoding="utf-8")
        menu = es[es.index('<nav class="menu">'):es.index("</nav>")]
        self.assertNotIn("Método", menu)
        self.assertIn("Curva TES", menu)

    def test_archivos_y_descargas(self):
        for f in ("assets/app.js", "assets/estilo.css", "assets/plotly.min.js", "assets/curva_tes.json",
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
        es = (self.out / "index.html").read_text(encoding="utf-8")
        n = 0
        for bloque in es.split('<script type="application/json" data-for="')[1:]:
            data = bloque.split('">', 1)[1].split("</script>", 1)[0]
            fig = json.loads(data)
            self.assertIn("data", fig)
            n += 1
        self.assertGreaterEqual(n, 8)


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
