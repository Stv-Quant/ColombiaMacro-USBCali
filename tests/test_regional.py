"""Datos regionales y holgura laboral: coherencia de las tablas y del mapa."""
import unittest

from colombiamacro import modelo as mt
from colombiamacro.sitio import capacidad_extra as cx


class TestRegional(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.R = cx.cargar()

    def test_existen(self):
        self.assertIsNotNone(self.R)

    def test_departamentos_suman_nacional(self):
        dep = self.R["dep"]
        a = dep["anio"].max()
        u = dep[dep["anio"] == a]
        nac = u[u["codigo"] == "00"]["pib_corriente"].iloc[0]
        self.assertAlmostEqual(u[u["codigo"] != "00"]["pib_corriente"].sum() / nac, 1, delta=0.01)
        self.assertEqual(u["codigo"].nunique(), 34)

    def test_ramas_suman_pib(self):
        dep, ram = self.R["dep"], self.R["ramas"]
        a = dep["anio"].max()
        x = ram[(ram["anio"] == a)].groupby("codigo")["va_corriente"].sum()
        y = dep[dep["anio"] == a].set_index("codigo")["pib_corriente"]
        self.assertLess(((x - y.reindex(x.index)).abs() / y.reindex(x.index)).max(), 0.01)

    def test_mapa_cubre_todos(self):
        dep = self.R["dep"]
        self.assertEqual(set(cx.TILES), set(dep["codigo"]) - {"00"})
        posiciones = [(c, f) for c, f, _ in cx.TILES.values()]
        self.assertEqual(len(posiciones), len(set(posiciones)))       # sin casillas superpuestas
        self.assertTrue(set(cx.CAPITAL.values()) <= set(self.R["ciudades"]["ciudad"]))

    def test_medidas(self):
        M = cx.medidas(self.R, mt.cargar())
        self.assertTrue(((M["neq"] >= 1) & (M["neq"] <= 12)).all())
        self.assertAlmostEqual(M["pc_idx"]["00"], 100)
        sub = M["sub12"].dropna()
        self.assertTrue((sub["mcsft"] >= sub["tcsd"]).all() and (sub["tcsd"] >= sub["td"]).all())

    def test_bucket(self):
        self.assertEqual(cx._bucket(-10, [-2, -1, 0, 1, 2, 3]), "-3")
        self.assertEqual(cx._bucket(10, [-2, -1, 0, 1, 2, 3]), "3")
        self.assertEqual(cx._bucket(None, [0] * 6), "na")


if __name__ == "__main__":
    unittest.main()
