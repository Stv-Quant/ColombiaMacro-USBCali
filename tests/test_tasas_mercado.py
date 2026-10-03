"""Tasas de mercado (BanRep): series completas y coherentes."""
import unittest

from colombiamacro.fuentes import tasas_mercado as tm


class TestTasasMercado(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.T = tm.cargar()

    def test_series(self):
        self.assertIsNotNone(self.T)
        self.assertEqual(set(self.T), set(tm.SERIES))

    def test_coherencia(self):
        ibr, cdt, col = self.T["ibr_3m"], self.T["cdt_90"], self.T["col_total"]
        self.assertTrue(3 < ibr.iloc[-1] < 25)
        # el credito cuesta mas que el ahorro a plazo
        self.assertGreater(col.iloc[-1], cdt.iloc[-1])
        car = self.T["cartera_total"]
        partes = sum(self.T[k] for k in ("cartera_comercial", "cartera_consumo", "cartera_vivienda", "cartera_micro"))
        self.assertAlmostEqual(float(partes.iloc[-1] / car.iloc[-1]), 1.0, delta=0.08)


if __name__ == "__main__":
    unittest.main()
