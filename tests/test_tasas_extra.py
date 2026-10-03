"""Pagina de tasas: ciclos de la tasa del Banco, traspaso y credito real."""
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from colombiamacro.sitio import tasas_extra as tx


class TestTasasExtra(unittest.TestCase):
    def setUp(self):
        idx = pd.date_range("2020-01-01", periods=400, freq="D")
        v = np.r_[np.full(50, 5.0), np.full(50, 5.5), np.full(50, 6.0), np.full(100, 6.0), np.full(50, 5.75), np.full(100, 5.5)]
        self.tpm = pd.Series(v, index=idx)

    def test_ciclos(self):
        c = tx.ciclos_tpm(self.tpm)
        self.assertEqual(list(c["signo"]), [1, -1])
        self.assertEqual(list(c["decisiones"]), [2, 2])
        self.assertAlmostEqual(c["cambio"].iloc[0], 1.0)
        self.assertAlmostEqual(c["despues"].iloc[1], 5.5)

    def test_traspaso_completo_y_medio(self):
        c = tx.ciclos_tpm(self.tpm).iloc[0]
        igual = self.tpm + 1
        medio = 5 + (self.tpm - 5) / 2
        r = tx.traspaso({"igual": igual, "medio": medio}, self.tpm, c, rezago_meses=1)
        self.assertAlmostEqual(r["igual"], 100.0)
        self.assertAlmostEqual(r["medio"], 50.0)

    def test_real_anual(self):
        idx = pd.date_range("2020-01-01", periods=24, freq="MS")
        saldo = pd.Series(100 * 1.10 ** (np.arange(24) / 12), index=idx)
        inf = pd.Series(10.0, index=idx)
        self.assertAlmostEqual(tx.real_anual(saldo, inf).iloc[-1], 0.0, places=6)

    def test_pagina(self):
        h = Path(__file__).resolve().parents[1] / "site" / "tasas" / "index.html"
        if h.exists():
            t = h.read_text(encoding="utf-8")
            for sid in ("ts-medidas", "ts-ciclos", "ts-transmision", "ts-credito", "ts-ibr", "ts-cartera", "ts-liquidez", 'id="exp-tpm"', 'id="banco"'):
                self.assertIn(sid, t)


if __name__ == "__main__":
    unittest.main()
