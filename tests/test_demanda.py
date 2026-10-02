"""PIB por el gasto, poblacion y productividad: coherencia de las tablas y del parser."""
import unittest

import pandas as pd

from colombiamacro import modelo as mt
from colombiamacro.config import DATA_DIR
from colombiamacro.fuentes import demanda as fd
from colombiamacro.sitio import crecimiento_extra as cx


class TestTablas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.D = cx.cargar_demanda()
        cls.d = mt.cargar()

    def test_existen(self):
        self.assertIsNotNone(self.D)

    def test_pib_coincide_con_produccion(self):
        g = self.D["gasto"]
        p = g[g["componente"] == "pib"].set_index("fecha")["real"]
        ref = pd.read_csv(DATA_DIR / "pib_colombia.csv", parse_dates=["fecha"]).set_index("fecha")["pib_real_miles_millones_ref2015"]
        comun = p.index.intersection(ref.index)
        self.assertGreater(len(comun), 60)
        self.assertLess(((p[comun] - ref[comun]).abs() / ref[comun]).max(), 0.002)

    def test_identidad_nominal(self):
        # a precios corrientes el PIB = consumo final + FBK + X − M (aditivo)
        n = self.D["gasto"].pivot(index="fecha", columns="componente", values="nominal")
        res = n["consumo_final"] + n["formacion_capital"] + n["exportaciones"] - n["importaciones"] - n["pib"]
        self.assertLess((res.abs() / n["pib"]).max(), 0.01)

    def test_aportes_suman_pib(self):
        X = cx.medidas_demanda(self.D, self.d)
        tot = X["ap"].sum(axis=1)
        self.assertLess((tot - X["pib_y"].loc[tot.index]).abs().max(), 1e-9)

    def test_poblacion(self):
        p = self.D["poblacion"].set_index("anio")["poblacion"]
        self.assertTrue(p.is_monotonic_increasing)
        self.assertTrue(40e6 < p.loc[2015] < 60e6)
        g = self.D["gasto"]
        self.assertLessEqual(p.index.max(), pd.to_datetime(g["fecha"]).max().year)

    def test_tasa_inversion_en_rango(self):
        X = cx.medidas_demanda(self.D, self.d)
        self.assertTrue(X["tinv"].between(8, 35).all())


class TestParser(unittest.TestCase):
    def test_bloque_trimestral(self):
        anos = [None, "Concepto"] + sum([[a, None, None, None] for a in range(2005, 2021)], [])
        trims = [None, None] + ["I", "II", "III", "IV"] * 16
        fila = ["P.3 ", "Gasto de consumo final"] + [float(i + 1) for i in range(64)]
        rows = [["titulo"], anos, trims, [None], fila, ["Fuente: DANE"], ["P.3", "otro bloque"] + [9.0] * 64]
        out = fd.bloque_trimestral(rows, lambda a, b: fd.GASTO.get(fd._codigo(a)))
        s = out["consumo_final"]
        self.assertEqual(len(s), 64)
        self.assertEqual(s[pd.Timestamp(2005, 4, 1)], 2.0)
        self.assertEqual(s.index.max(), pd.Timestamp(2020, 10, 1))


if __name__ == "__main__":
    unittest.main()
