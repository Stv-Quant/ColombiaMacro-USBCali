"""Cada grafico del sitio tiene su lupa (que cuenta, como se lee, por que importa, como interpretarlo) en ES y EN."""
import re
import unittest
from pathlib import Path

from colombiamacro.sitio import lupas


class TestLupas(unittest.TestCase):
    def test_contenido_completo(self):
        for gid, v in lupas.LUPAS.items():
            for L in ("es", "en"):
                d = v[L]
                for k in ("que", "leer", "importa"):
                    self.assertGreater(len(d[k]), 60, f"{gid}.{L}.{k}")
                self.assertGreaterEqual(len(d["interpretar"]), 2, gid)
                self.assertTrue(all(len(f) == 3 for f in d.get("formulas", [])), gid)
            self.assertEqual(len(v["es"].get("formulas", [])), len(v["en"].get("formulas", [])), gid)

    def test_sin_proyecciones(self):
        malo = re.compile(r"pronóstic|predic|forecast|recomend|recommend", re.I)
        for gid, v in lupas.LUPAS.items():
            self.assertIsNone(malo.search(str(v)), gid)

    def test_cada_grafico_tiene_lupa(self):
        raiz = Path(__file__).resolve().parents[1] / "site"
        paginas = list(raiz.glob("*/index.html")) + list(raiz.glob("en/*/index.html"))
        if not paginas:
            self.skipTest("sitio no construido")
        n = 0
        for f in paginas:
            t = f.read_text(encoding="utf-8")
            for k in lupas.claves(t):
                n += 1
                self.assertIn(k, lupas.LUPAS, f"{f}: {k} sin lupa")
            if lupas.claves(t):
                self.assertIn('id="lupa-datos"', t)
                self.assertIn('id="dlg-lupa"', t)
        self.assertGreater(n, 250)


if __name__ == "__main__":
    unittest.main()
