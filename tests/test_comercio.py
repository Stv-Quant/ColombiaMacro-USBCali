"""Comercio exterior (DANE): coherencia de las tablas sembradas y de los parsers."""
import unittest

import pandas as pd

from colombiamacro.config import DATA_DIR
from colombiamacro.fuentes import comercio as fc
from colombiamacro.sitio import comercio_extra as cx
from colombiamacro.sitio.fichas import FICHAS


class TestTablas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = cx.cargar()

    def test_existen(self):
        self.assertIsNotNone(self.c, "faltan tablas de comercio en data/")

    def test_exportaciones_suman(self):
        e = self.c["expo"]
        dif = (e["tradicionales"] + e["no_tradicionales"] - e["total"]).abs() / e["total"]
        self.assertLess(dif.max(), 0.01)
        trad = e[["cafe", "carbon", "petroleo", "ferroniquel"]].sum(axis=1)
        self.assertLess(((trad - e["tradicionales"]).abs() / e["tradicionales"]).max(), 0.01)

    def test_destinos_y_expo_coinciden(self):
        de = self.c["destinos"].set_index("fecha")["total"]
        ex = self.c["expo"].set_index("fecha")["total"]
        comun = de.index.intersection(ex.index)
        self.assertGreater(len(comun), 100)
        self.assertLess(((de[comun] - ex[comun]).abs() / ex[comun]).max(), 0.01)

    def test_sin_meses_futuros(self):
        fin = self.c["impo"]["fecha"].max()
        self.assertLessEqual(self.c["origen"]["fecha"].max(), fin)
        self.assertFalse(self.c["origen"].duplicated(["fecha", "pais"]).any())

    def test_cuode_grupos_suman(self):
        cu = self.c["cuode"]
        tot = cu.iloc[0]["corrido_actual"]
        grandes = cu[cu["grupo"].map(cx._norm).isin(["bienes de consumo", "materias primas y productos intermedios",
                                                     "bienes de capital y material de construccion", "bienes no clasificados"])]
        self.assertAlmostEqual(grandes["corrido_actual"].sum() / tot, 1, delta=0.02)

    def test_resumen(self):
        R = cx.resumen(self.c)
        self.assertAlmostEqual(R["bal12"], R["expo12"] - R["impo12"])
        self.assertTrue(0 < R["min_sh"] < 100)
        self.assertTrue(20_000 < R["expo12"] < 200_000)      # millones de USD

    def test_fichas(self):
        for gid in ("g-comercio-flujos", "g-balanza", "g-expo-productos", "g-expo-minero", "g-impo-uso",
                    "g-impo-estructura", "g-destinos", "g-origenes"):
            self.assertIn(gid, FICHAS)


class TestParsers(unittest.TestCase):
    def test_origen_recorta_meses_futuros(self):
        filas = [["Cuadro"], ["País", "Mes", 2025, 2026], ["Chile", "Enero", 10.0, 12.0],
                 [None, "Febrero", 11.0, 0], [None, "Marzo", 9.0, None], ["Perú", "Enero", 5.0, 6.0],
                 [None, "Febrero", 4.0, 0], [None, "Marzo", 3.0, None],
                 [None, "Abril", 2.0, None], [None, "Mayo", 2.0, None], [None, "Junio", 1.0, None]]
        filas[1] = ["País", "Mes", 2022, 2023, 2024, 2025, 2026]
        filas = [filas[0], filas[1]] + [r[:2] + [1.0, 1.0, 1.0] + r[2:] for r in filas[2:]]
        df = fc.leer_impo_origen(filas, desde=2025)
        self.assertEqual(df["fecha"].max(), pd.Timestamp(2026, 1, 1))


if __name__ == "__main__":
    unittest.main()
