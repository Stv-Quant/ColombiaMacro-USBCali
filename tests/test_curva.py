"""Curva TES ampliada: factores, episodios de curva invertida, movimientos y pagina."""
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from colombiamacro import modelo as mt
from colombiamacro.sitio import curva_extra as cx


class TestCurva(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        d = mt.cargar()
        cls.c = d.tasas.dropna(subset=["tes_pesos_1y", "tes_pesos_5y", "tes_pesos_10y"]).set_index("fecha")
        cls.tpm = d.tasas.set_index("fecha")["tpm"].dropna()

    def test_factores(self):
        F = cx.factores(self.c)
        u = self.c.iloc[-1]
        self.assertAlmostEqual(F["pendiente"].iloc[-1], u["tes_pesos_10y"] - u["tes_pesos_1y"], places=6)
        self.assertAlmostEqual(F["nivel"].iloc[-1], (u["tes_pesos_1y"] + u["tes_pesos_5y"] + u["tes_pesos_10y"]) / 3, places=6)

    def test_episodios(self):
        s = pd.Series([1, -0.1, -0.2, -0.3, -0.1, -0.2, 0.5, -0.1, 0.2], index=pd.bdate_range("2024-01-01", periods=9))
        ep = cx.episodios_invertida(s, min_dias=5)
        self.assertEqual(len(ep), 1)
        self.assertEqual(ep.iloc[0]["dias"], 5)
        self.assertAlmostEqual(ep.iloc[0]["minimo"], -0.3)
        ep_real = cx.episodios_invertida(cx.factores(self.c)["pendiente"], self.tpm)
        self.assertTrue((ep_real["minimo"] < 0).all())

    def test_tipo_movimiento(self):
        self.assertEqual(cx.tipo_movimiento(0.5, -0.4), "bear_flat")
        self.assertEqual(cx.tipo_movimiento(-0.5, 0.4), "bull_steep")
        self.assertEqual(cx.tipo_movimiento(0.02, 0.03), "quieto")

    def test_volatilidad(self):
        rng = np.random.default_rng(0)
        s = pd.Series(np.cumsum(rng.normal(0, 0.05, 400)))   # 5 pb diarios
        v = cx.volatilidad(s).dropna()
        self.assertAlmostEqual(v.iloc[-1], 5 * np.sqrt(252), delta=20)

    def test_pagina(self):
        h = Path(__file__).resolve().parents[1] / "site" / "curva-tes" / "index.html"
        if h.exists():
            t = h.read_text(encoding="utf-8")
            for sid in ("cv-medidas", "cv-factores", "cv-movimientos", "cv-real", "cv-riesgo", "cv-literatura", 'id="exp-curva"', 'id="curva-app"'):
                self.assertIn(sid, t)


if __name__ == "__main__":
    unittest.main()
