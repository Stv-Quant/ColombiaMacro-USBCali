"""Tasa de cambio: datos oficiales coherentes y calculos de la pagina del peso."""
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from colombiamacro import modelo as mt
from colombiamacro.fuentes import cambiario as cb
from colombiamacro.sitio import cambio_extra as cx


class TestCambiario(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.C = cb.cargar()
        cls.trm = mt.cargar().extra["trm"].set_index("fecha")["trm"]

    def test_series(self):
        self.assertEqual(set(self.C), set(cb.BANREP) | set(cb.FREDS))

    def test_cruce_euro(self):
        # COP/EUR de BanRep es coherente con la TRM: 1 euro vale mas de 0,8 y menos de 1,6 dolares
        ratio = (self.C["cop_eur"] / self.trm.reindex(self.C["cop_eur"].index, method="ffill")).dropna()
        self.assertTrue(ratio.between(0.8, 1.7).all())

    def test_itcr_sigue_a_la_trm(self):
        # el ITCR sube cuando el peso se deprecia: correlacion positiva con la TRM mensual
        it = mt.cargar().extra["itcr_ipc"].set_index("fecha")["itcr_ipc"]
        tm = self.trm.resample("MS").mean()
        df = pd.DataFrame({"it": it, "tm": tm}).dropna().loc["2010":]
        self.assertGreater(df["it"].pct_change().corr(df["tm"].pct_change()), 0.6)

    def test_cambio_y_volatilidad(self):
        s = pd.Series([100.0] * 300 + [110.0], index=pd.bdate_range("2024-01-01", periods=301))
        self.assertAlmostEqual(cx.cambio(s), 10.0, places=6)
        rng = np.random.default_rng(1)
        r = pd.Series(np.exp(np.cumsum(rng.normal(0, 0.01, 500))))
        self.assertAlmostEqual(cx.volatilidad(r).iloc[-1], 100 * 0.01 * np.sqrt(252), delta=4)

    def test_pagina(self):
        h = Path(__file__).resolve().parents[1] / "site" / "mercados" / "index.html"
        if h.exists():
            t = h.read_text(encoding="utf-8")
            for sid in ("tc-medidas", "tc-global", "tc-monedas", "tc-real", "tc-petroleo", "tc-flujos", "tc-vol", 'id="exp-peso"'):
                self.assertIn(sid, t)
            self.assertNotIn('id="g-bolsa"', t)   # el COLCAP vive ahora en Empresas


if __name__ == "__main__":
    unittest.main()
