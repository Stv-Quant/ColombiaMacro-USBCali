"""Mercado laboral en detalle: coherencia de las tablas de la GEIH."""
import unittest

import pandas as pd

from colombiamacro import modelo as mt
from colombiamacro.fuentes import empleo as fe
from colombiamacro.sitio import empleo_extra as ex


class TestEmpleo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.E = ex.cargar()

    def test_existen(self):
        self.assertIsNotNone(self.E)

    def test_ramas_suman_ocupados(self):
        r = self.E["ramas"].groupby("fecha")["ocupados"].sum()
        s = self.E["sexo"].pivot(index="fecha", columns="sexo", values="ocupados").sum(axis=1)
        comun = r.index.intersection(s.index)
        self.assertGreater(len(comun), 100)
        self.assertLess(((r[comun] - s[comun]).abs() / s[comun]).max(), 0.01)

    def test_posicion_suma_ocupados(self):
        p = self.E["posicion"].groupby("fecha")["ocupados"].sum()
        s = self.E["sexo"].pivot(index="fecha", columns="sexo", values="ocupados").sum(axis=1)
        comun = p.index.intersection(s.index)
        self.assertLess(((p[comun] - s[comun]).abs() / s[comun]).max(), 0.01)

    def test_nini_suma(self):
        j = self.E["jovenes"].dropna(subset=["nini", "nini_h", "nini_m"])
        self.assertLess((j["nini_h"] + j["nini_m"] - j["nini"]).abs().max(), 0.05)

    def test_medidas(self):
        M = ex.medidas(self.E)
        self.assertLess((M["sh"].sum(axis=1) - 100).abs().max(), 1e-6)
        self.assertTrue(M["asal"].between(30, 70).all())

    def test_periodos(self):
        self.assertEqual(fe._fin_periodo("May - Jul 26"), pd.Timestamp(2026, 7, 1))
        self.assertEqual(fe._fin_periodo("Nov 25 - Ene 26"), pd.Timestamp(2026, 1, 1))
        f = fe._fechas_mensuales([None, 2025, None], [None, "Nov - Ene", "Dic - Feb"])
        self.assertEqual(f[1], pd.Timestamp(2026, 1, 1))


if __name__ == "__main__":
    unittest.main()
