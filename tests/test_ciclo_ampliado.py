"""Pruebas del ciclo ampliado: filtros, consenso, ciclo mensual, giros y Okun."""

import unittest

import numpy as np
import pandas as pd

from colombiamacro import analitica as am
from colombiamacro import modelo as mt


class TestFiltros(unittest.TestCase):
    def test_cf_elimina_tendencia_lineal(self):
        y = pd.Series(np.arange(80, dtype=float) * 0.7 + 5)
        self.assertLess(np.nanmax(np.abs(am.cf_filter(y))), 1e-8)

    def test_cf_conserva_ciclo_de_banda(self):
        t = np.arange(160)
        y = pd.Series(0.5 * t + 3 * np.sin(2 * np.pi * t / 16))
        c = am.cf_filter(y)
        self.assertGreater(np.corrcoef(c[20:-20], 3 * np.sin(2 * np.pi * t / 16)[20:-20])[0, 1], 0.95)

    def test_bn_paseo_aleatorio_sin_ciclo(self):
        rng = np.random.default_rng(1)
        y = pd.Series(np.cumsum(rng.normal(0.5, 1, 300)))
        self.assertLess(np.nanstd(am.bn_cycle(y)), 0.5)


class TestCicloConDatos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = mt.cargar()

    def test_consenso_resumen_coherente(self):
        c = am.brechas_consenso(self.d.pib, self.d.ciclo).dropna(subset=["mediana"])
        m = c[list(am.NOMBRES_METODOS)]
        self.assertTrue(((c["minimo"] <= c["mediana"]) & (c["mediana"] <= c["maximo"])).all())
        self.assertTrue((c["positivos"] == (m > 0).sum(axis=1)).all())
        self.assertLess(m.abs().max().max(), 30)          # sin valores explosivos en los extremos

    def test_ciclo_mensual(self):
        cm = am.ciclo_mensual(self.d.ise)
        self.assertIn("brecha_secundarias", cm)
        ult = cm.dropna(subset=["brecha"]).iloc[-1]
        self.assertIn(ult["fase"], am.FASES)

    def test_giros_alternan_y_episodios(self):
        nivel = self.d.ise.set_index("fecha")["ise_sa"]
        g = am.giros_clasicos(nivel)
        tipos = [x[1] for x in g]
        self.assertTrue(all(a != b for a, b in zip(tipos, tipos[1:])))
        rec, exp_ = am.episodios(nivel, g)
        self.assertTrue(any(r["desde"].year == 2020 and r["variacion"] < -10 for r in rec))
        self.assertTrue(all(r["variacion"] < 0 for r in rec))

    def test_okun_pendiente_negativa(self):
        c = am.brechas_consenso(self.d.pib, self.d.ciclo)
        o = am.okun(c.set_index("fecha")["brecha_hp_dos_colas"], self.d.laboral.set_index("fecha")["td_sa"])
        self.assertLess(o["pendiente"], 0)
        self.assertGreater(o["n"], 40)


if __name__ == "__main__":
    unittest.main()
