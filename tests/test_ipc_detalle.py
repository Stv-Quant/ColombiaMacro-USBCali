"""IPC en detalle: coherencia de los anexos del DANE."""
import unittest

import pandas as pd

from colombiamacro.config import DATA_DIR
from colombiamacro.sitio import inflacion_extra as ix


class TestIPC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.I = ix.cargar()

    def test_existen(self):
        self.assertIsNotNone(self.I)

    def test_aportes_suman_total(self):
        d = self.I["divisiones"].set_index("division")
        self.assertAlmostEqual(d.drop("total")["contrib_anual"].sum(), d.loc["total", "var_anual"], delta=0.05)
        self.assertAlmostEqual(d.drop("total")["ponderacion"].sum(), 100, delta=0.2)

    def test_total_coincide_con_serie(self):
        d = self.I["divisiones"].set_index("division").loc["total"]
        inf = pd.read_csv(DATA_DIR / "inflacion_clean.csv", parse_dates=["fecha"]).set_index("fecha")["inflacion_anual"]
        f = self.I["divisiones"]["fecha"].iloc[0]
        if f in inf.index:
            self.assertAlmostEqual(inf[f], d["var_anual"], delta=0.02)

    def test_subclases_y_ciudades(self):
        self.assertGreaterEqual(len(self.I["subclases"]), 180)
        c = self.I["ciudades"]
        self.assertGreaterEqual(c["ciudad"].nunique(), 24)
        self.assertEqual(c["division"].nunique(), 13)

    def test_clasificaciones(self):
        cl = self.I["clasificaciones"].pivot(index="fecha", columns="serie", values="indice")
        self.assertAlmostEqual(cl.loc["2018-12-01"].mean(), 100, delta=0.6)   # base dic 2018 = 100


if __name__ == "__main__":
    unittest.main()
