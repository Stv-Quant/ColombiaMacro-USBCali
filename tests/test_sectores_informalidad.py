"""Pruebas de PIB por sectores e informalidad laboral."""

import unittest

import pandas as pd

from colombiamacro import modelo as mt
from colombiamacro.fuentes import informalidad as inf
from colombiamacro.fuentes import pib


class TestSectores(unittest.TestCase):
    def niveles(self):
        f = pd.date_range("2020-01-01", periods=9, freq="QS")
        d = {code: [100.0 + 10 * k for k in range(9)] for code in pib.SECTORES}
        d["C"] = [100.0] * 4 + [110.0] * 5          # industria +10% a/a desde 2021
        df = pd.DataFrame(d, index=f)
        df["VA"] = df.sum(axis=1)
        return df

    def test_crecimiento_peso_y_aporte(self):
        s = pib.build_sectores(self.niveles())
        c = s[(s["codigo"] == "C") & (s["fecha"] == "2021-01-01")].iloc[0]
        self.assertAlmostEqual(c["yoy"], 10.0)
        va = self.niveles()["VA"]
        self.assertAlmostEqual(c["contribucion"], 10 / va.iloc[0] * 100)
        self.assertEqual(s.groupby("fecha")["codigo"].nunique().min(), 12)
        pesos = s[s["fecha"] == "2021-01-01"]["peso"].sum()
        self.assertAlmostEqual(pesos, 100.0)

    def test_datos_del_repositorio(self):
        d = mt.cargar()
        if d.sectores is None:
            self.skipTest("sin pib_sectores.csv")
        ult = d.sectores[d.sectores["fecha"] == d.sectores["fecha"].max()]
        self.assertEqual(len(ult), 12)
        # volumenes encadenados: no aditivos, la suma de pesos se aparta levemente de 100
        self.assertAlmostEqual(ult["peso"].sum(), 100.0, delta=2)
        self.assertEqual(d.sectores["fecha"].max(), d.pib["fecha"].max())


class TestInformalidad(unittest.TestCase):
    def test_secuencia_de_trimestres_moviles(self):
        anos = (None, 2021, None, None, None)
        rotulos = (None, "Ene - mar", "Feb - abr", "Mar - may", "Abr - jun")
        f = inf.fechas_columnas(anos, rotulos)
        self.assertEqual(f[1], pd.Timestamp("2021-03-01"))
        self.assertEqual(f[4], pd.Timestamp("2021-06-01"))

    def test_cambio_de_ano_en_rotulos(self):
        anos = (None, 2021, None, None)
        rotulos = (None, "Oct - dic", "Nov 21 - ene 22", "Dic 21 - feb 22")
        f = inf.fechas_columnas(anos, rotulos)
        self.assertEqual(f[3], pd.Timestamp("2022-02-01"))

    def test_secuencia_rota_falla(self):
        with self.assertRaises(ValueError):
            inf.fechas_columnas((None, 2021, None), (None, "Ene - mar", "Mar - may"))

    def test_ramas_cortas(self):
        self.assertEqual(inf.rama_corta("Agricultura, ganadería, caza, silvicultura y pesca"), "Agro y pesca")
        self.assertEqual(inf.rama_corta("Administración pública y defensa, educación"), "Gobierno, educación y salud")
        self.assertIsNone(inf.rama_corta("No informa"))

    def test_datos_del_repositorio(self):
        d = mt.cargar()
        if d.informalidad is None:
            self.skipTest("sin informalidad.csv")
        i = d.informalidad
        self.assertTrue(i["nacional"].between(40, 70).all())
        self.assertTrue((i["ciudades_13"] < i["nacional"]).all())   # las ciudades son menos informales
        self.assertEqual(list(i["fecha"]), list(pd.date_range(i["fecha"].min(), i["fecha"].max(), freq="MS")))
        r = d.informalidad_ramas
        u = r[r["fecha"] == r["fecha"].max()]
        self.assertEqual(len(u), 13)
        # la suma por ramas reproduce la tasa nacional publicada
        tasa = 100 * u["informales"].sum() / u["ocupados"].sum()
        self.assertAlmostEqual(tasa, i.iloc[-1]["nacional"], delta=0.2)


class TestNoticias(unittest.TestCase):
    def test_publicaciones_oficiales(self):
        from colombiamacro import noticias as nt
        d = mt.cargar()
        s = mt.instantanea(d)
        for lang in ("es", "en"):
            items = nt.publicaciones(d, s, lang)
            self.assertGreaterEqual(len(items), 5)
            fechas = [i["fecha"] for i in items]
            self.assertEqual(fechas, sorted(fechas, reverse=True))
            self.assertTrue(all(i["enlace"].startswith("https://") for i in items))
            self.assertTrue(all(i["fecha"] <= pd.Timestamp.today().normalize() for i in items))
            fuentes = {i["fuente"] for i in items}
            self.assertIn("DANE", fuentes)


class TestTrayectoria(unittest.TestCase):
    def test_tramos_reproducen_el_breakeven_a_10_anos(self):
        from colombiamacro.sitio import construir as cs
        d = mt.cargar()
        fig, meta, tramos = cs.Graficos(d, mt.instantanea(d), "es").trayectoria_inflacion()
        if fig is None:
            self.skipTest("sin breakevens")
        (a0, a1, b1), (_, _, f15), (_, _, f510) = tramos
        prod = (1 + b1 / 100) * (1 + f15 / 100) ** 4 * (1 + f510 / 100) ** 5
        ult = d.tasas.dropna(subset=["bei_10y"]).iloc[-1]
        self.assertAlmostEqual(prod ** 0.1 - 1, ult["bei_10y"] / 100, places=8)
        self.assertAlmostEqual(f510, ult["bei_5y5y"], places=6)


class TestV112(unittest.TestCase):
    def test_trece_ciudades(self):
        from colombiamacro.fuentes import informalidad as inf
        d = mt.cargar()
        if d.informalidad_ciudades is None:
            self.skipTest("sin informalidad_ciudades.csv")
        ic = d.informalidad_ciudades
        trece = sorted(ic[ic["grupo"] == "13"]["ciudad"].unique())
        self.assertEqual(trece, sorted(inf.CIUDADES_13))
        self.assertGreaterEqual(ic["ciudad"].nunique(), 23)

    def test_enlaces_banrep_verificados(self):
        from colombiamacro import noticias as nt
        for k, u in nt.ENLACES.items():
            self.assertNotIn("banrep.gov.co/es/estadisticas", u, k)   # esas rutas no existen

    def test_capacidad_reproduce_la_brecha(self):
        import numpy as np
        from colombiamacro.sitio import construir as cs
        d = mt.cargar()
        fig, meta, u = cs.Graficos(d, mt.instantanea(d), "es").capacidad()
        self.assertAlmostEqual(100 * np.log(u["y"] / u["pot"]), u["gap"], places=8)


class TestFichas(unittest.TestCase):
    def test_cada_grafico_tiene_fuente_y_metodologia(self):
        import re
        import tempfile
        from pathlib import Path
        from colombiamacro.sitio import construir as cs
        from colombiamacro.sitio.fichas import FICHAS
        with tempfile.TemporaryDirectory() as tmp:
            out = cs.construir(Path(tmp) / "site")
            paginas = [p for p in out.rglob("index.html")]
            self.assertGreaterEqual(len(paginas), 26)
            for pag in paginas:
                html_ = pag.read_text(encoding="utf-8")
                ids = set(re.findall(r'class="plot" id="(g-[^"]+)"', html_))
                faltan = [i for i in ids if i not in FICHAS and i != "g-inf-ciudad"]
                self.assertEqual(faltan, [], pag)
                self.assertGreaterEqual(html_.count('class="ficha"'), len(ids) - 1)
                self.assertIn('id="menu-toggle"', html_)
            for raiz in (out, out / "en"):
                html_ = (raiz / "indicadores" / "index.html").read_text(encoding="utf-8")
                self.assertLess(html_.index('id="noticias"'), html_.index('id="fuentes"'))
                self.assertGreater(html_.index('id="noticias"'), html_.index('id="indicadores"'))


class TestDecisionAnunciada(unittest.TestCase):
    def serie(self, valores, fin="2026-09-30"):
        f = pd.date_range(end=fin, periods=len(valores), freq="D")
        return pd.DataFrame({"fecha": f, "tpm": valores})

    def test_pendiente_hasta_que_la_serie_la_registra(self):
        import tempfile
        from pathlib import Path
        from unittest import mock
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "decisiones_banrep.csv").write_text(
                "fecha_anuncio,vigente_desde,tasa,nota,enlace\n2026-09-30,2026-10-01,12.25,x,\n", encoding="utf-8")
            with mock.patch.object(mt, "DATA_DIR", Path(tmp)):
                an = mt.decision_pendiente(None, self.serie([12.0] * 5))
                self.assertEqual(an["tasa"], 12.25)
                self.assertEqual(an["anterior"], 12.0)
                ya = mt.decision_pendiente(None, self.serie([12.0] * 5 + [12.25], fin="2026-10-01"))
                self.assertIsNone(ya)

    def test_modo_rapido_solo_series_diarias(self):
        from colombiamacro import actualizar as ac
        rapidos = [m for _, m, _ in ac.pasos(True)]
        self.assertIn("colombiamacro.fuentes.complementarias", rapidos)
        self.assertNotIn("colombiamacro.fuentes.pib", rapidos)
        self.assertEqual(len(ac.pasos(False)), len(ac.PASOS))


class TestAmpliar(unittest.TestCase):
    """v11.4: cada grafico se puede ampliar como superposicion sin mover la pagina."""

    def test_js_y_css(self):
        from pathlib import Path
        base = Path(__file__).resolve().parents[1] / "colombiamacro" / "sitio"
        js = (base / "app.js").read_text(encoding="utf-8")
        css = (base / "estilo.css").read_text(encoding="utf-8")
        for clave in ("function ampliar", "exp-hueco", "Escape", "overflowAnchor", "seguro(ampliar)"):
            self.assertIn(clave, js)
        for clave in ("figure.chart.expandida", ".exp-btn", ".exp-fondo", ".exp-hueco"):
            self.assertIn(clave, css)


if __name__ == "__main__":
    unittest.main()
