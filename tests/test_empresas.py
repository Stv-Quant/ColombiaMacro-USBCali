"""Sector empresarial: agregados de las 10.000 empresas, registro mercantil y pagina."""
import unittest
from pathlib import Path

import pandas as pd

from colombiamacro.fuentes import empresas as fe
from colombiamacro.sitio import empresas_extra as ex


class TestEmpresas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.E = fe.cargar()

    def test_totales_cuadran_con_partes(self):
        a = self.E["agg"]
        tot = a[a["dimension"] == "total"].set_index("ano")["ingresos"]
        for dim in ("macrosector", "region", "supervisor"):
            s = a[a["dimension"] == dim].groupby("ano")["ingresos"].sum()
            self.assertTrue(((s - tot).abs() < 0.5).all(), dim)
        self.assertTrue((a[a["dimension"] == "total"]["empresas"] >= 9000).all())

    def test_ingresos_2025_oficiales(self):
        # Supersociedades reporta $1.853,8 billones de ingresos operacionales a diciembre de 2025
        a = self.E["agg"]
        v = a[(a["dimension"] == "total") & (a["ano"] == 2025)]["ingresos"].iloc[0]
        self.assertAlmostEqual(v, 1853.8, delta=5)

    def test_concentracion_creciente(self):
        a = self.E["agg"]
        c = a[(a["dimension"] == "concentracion") & (a["ano"] == a["ano"].max())].sort_values("empresas")["ingresos"]
        self.assertTrue(c.is_monotonic_increasing)
        self.assertAlmostEqual(c.iloc[-1], 100.0, places=3)

    def test_razones(self):
        df = pd.DataFrame({"ingresos": [100.0], "ganancia": [10.0], "patrimonio": [50.0], "pasivos": [60.0], "activos": [110.0]})
        r = ex.razones(df).iloc[0]
        self.assertAlmostEqual(r["margen"], 10.0)
        self.assertAlmostEqual(r["roe"], 20.0)
        self.assertAlmostEqual(r["endeudamiento"], 60 / 110 * 100)

    def test_registro_sin_mes_incompleto(self):
        r = ex.meses_completos(self.E["registro"])
        tot = r.groupby("mes")["matriculas"].sum()
        self.assertGreaterEqual(tot.iloc[-1], 0.5 * tot.iloc[-13:-1].median())

    def test_pagina(self):
        h = Path(__file__).resolve().parents[1] / "site" / "empresas" / "index.html"
        if h.exists():
            t = h.read_text(encoding="utf-8")
            for sid in ("em-medidas", "em-grandes", "em-sectores", "em-regiones", "em-concentracion", "em-acciones",
                        "em-financiacion", "em-registro", 'id="exp-empresas"', 'id="g-bolsa"'):
                self.assertIn(sid, t)


if __name__ == "__main__":
    unittest.main()
