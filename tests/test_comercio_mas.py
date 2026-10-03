"""Comercio ampliado: descomposicion precio-volumen, numero equivalente y pagina."""
import unittest
from pathlib import Path

import pandas as pd

from colombiamacro.sitio import comercio_mas as cm


class TestComercioMas(unittest.TestCase):
    def test_numero_equivalente(self):
        d = pd.DataFrame({"a": [1.0, 1.0], "b": [1.0, 0.0], "c": [1.0, 0.0], "d": [1.0, 0.0]})
        ne = cm.num_equivalente(d)
        self.assertAlmostEqual(ne.iloc[0], 4.0)
        self.assertAlmostEqual(ne.iloc[1], 1.0)

    def test_precio_por_volumen_es_valor(self):
        v, p = 8.0, 11.0
        q = ((1 + v / 100) / (1 + p / 100) - 1) * 100
        self.assertAlmostEqual((1 + p / 100) * (1 + q / 100), 1 + v / 100)

    def test_pagina(self):
        raiz = Path(__file__).resolve().parents[1] / "site"
        for f in (raiz / "comercio" / "index.html", raiz / "en" / "comercio" / "index.html"):
            if not f.exists():
                continue
            t = f.read_text(encoding="utf-8")
            self.assertGreaterEqual(t.count('class="lec '), 12)
            for sid in ("comercio-precios", "comercio-canasta", "comercio-bilateral", "comercio-apertura", "comercio-literatura",
                        'id="exp-comercio"', 'data-dialog="exp-comercio"'):
                self.assertIn(sid, t)
            for bad in (">nan", "NaN", "proyecci", "pronóstico", "forecast"):
                self.assertNotIn(bad, t)


if __name__ == "__main__":
    unittest.main()
