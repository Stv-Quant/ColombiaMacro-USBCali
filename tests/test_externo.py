"""Cuentas externas y fiscales: identidades de la balanza de pagos y razones al PIB."""
import unittest
from pathlib import Path

import pandas as pd

from colombiamacro.fuentes import externo_fiscal as xf
from colombiamacro.sitio import externo_extra as ex


class TestExterno(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.X = xf.cargar()

    def test_cuenta_corriente_suma_componentes(self):
        X = self.X
        partes = X["bienes"] + X["servicios"] + X["ingreso_primario"] + X["ingreso_secundario"]
        self.assertLess((partes - X["cc"]).dropna().abs().max(), 1.0)

    def test_cuenta_financiera_igual_cc_mas_errores(self):
        X = self.X
        self.assertLess((X["cf"] - X["cc"] - X["errores"]).dropna().abs().max(), 1.0)

    def test_deuda_externa_publica_mas_privada(self):
        X = self.X
        self.assertLess((X["deuda_externa_publica"] + X["deuda_externa_privada"] - X["deuda_externa"]).dropna().abs().max(), 1.0)

    def test_trimestral_solo_completos(self):
        s = pd.Series(1.0, index=pd.date_range("2025-01-01", periods=8, freq="MS"))
        q = ex.trimestral(s)
        self.assertEqual(list(q.values), [3.0, 3.0])          # el tercer trimestre (2 meses) no cuenta
        self.assertEqual(ex.suma4(pd.Series([1.0] * 5)).iloc[-1], 4.0)

    def test_pagina(self):
        h = Path(__file__).resolve().parents[1] / "site" / "externo" / "index.html"
        if h.exists():
            t = h.read_text(encoding="utf-8")
            for sid in ("ext-medidas", "ext-cc", "ext-financiacion", "ext-entran", "ext-deuda", "fi-gobierno", "fi-financiamiento", 'id="exp-externo"', 'id="externo"'):
                self.assertIn(sid, t)


if __name__ == "__main__":
    unittest.main()
