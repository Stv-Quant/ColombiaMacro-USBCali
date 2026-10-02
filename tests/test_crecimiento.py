"""Crecimiento ampliado: coherencia de los indicadores derivados (solo datos observados)."""
import unittest

import numpy as np

from colombiamacro import modelo as mt
from colombiamacro.sitio import crecimiento_extra as cx


class TestCrecimiento(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = mt.cargar()
        cls.M = cx.medidas(cls.d)

    def test_anual_coincide_con_dane(self):
        p = self.d.pib.set_index("fecha")["pib_real_yoy"]
        dif = (self.M["yoy"].dropna() - p.reindex(self.M["yoy"].dropna().index)).abs()
        self.assertLess(dif.max(), 0.01)

    def test_deflactor(self):
        M = self.M
        # (1 + nominal) = (1 + real)(1 + deflactor)
        lhs = 1 + M["nom"] / 100
        rhs = (1 + M["yoy"] / 100) * (1 + M["defl_y"] / 100)
        self.assertLess((lhs - rhs).abs().dropna().max(), 1e-9)

    def test_sin_gobierno_reconstruye_total(self):
        s = self.d.sectores
        u = s[s["fecha"] == s["fecha"].max()]
        g = u[u["sector"] == "Gobierno, educación y salud"].iloc[0]
        tot_w = u["peso"].sum()
        rec = (self.M["singob"].iloc[-1] * (tot_w - g["peso"]) + 100 * g["contribucion"]) / 100
        self.assertAlmostEqual(rec, u["contribucion"].sum(), places=6)

    def test_grupos_suman_valor_agregado(self):
        self.assertLess((self.M["grupos"].sum(axis=1) - self.M["tot_c"]).abs().max(), 1e-9)

    def test_difusion_en_rango(self):
        c = self.M["crecen"]
        self.assertTrue(((c >= 0) & (c <= 12)).all())

    def test_cagr(self):
        r = self.M["r"]
        y = r.groupby(r.index.year).sum()
        g = cx.cagr(r, 2015, 2019)
        self.assertAlmostEqual((1 + g / 100) ** 5, y[2019] / y[2014], places=9)

    def test_tendencia_log_lineal(self):
        t = np.log(self.M["tend"])
        self.assertLess(np.diff(np.diff(t.values)).__abs__().max(), 1e-12)


if __name__ == "__main__":
    unittest.main()
