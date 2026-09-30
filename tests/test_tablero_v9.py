import unittest

import pandas as pd

import analitica_macro as am
import dashboard_colombia as dash_app
import modelo_tablero as mt


class ModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = mt.cargar()
        cls.s = mt.instantanea(cls.d)

    def test_snapshot_matches_source_tables(self):
        pib = self.d.pib.dropna(subset=["pib_real_yoy"]).iloc[-1]
        self.assertAlmostEqual(self.s["ciclo"]["pib_real_yoy"], pib["pib_real_yoy"])
        self.assertAlmostEqual(self.s["inflacion"]["total"], self.d.ipc.iloc[-1]["inflacion_anual"])
        tes = self.d.tes.dropna(subset=["tes_pesos_10y"]).iloc[-1]
        self.assertAlmostEqual(self.s["tasas"]["tes_pesos_10y"], tes["tes_pesos_10y"])
        self.assertAlmostEqual(self.s["mercado"]["colcap"], self.d.colcap.iloc[-1]["colcap_puntos"])

    def test_breakeven_in_snapshot_is_fisher_of_latest_rates(self):
        t = self.s["tasas"]
        row = self.d.tes.dropna(subset=["tes_pesos_10y"]).iloc[-1]
        self.assertAlmostEqual(t["bei_1y"], float(am.breakeven(row["tes_pesos_1y"], row["tes_uvr_1y"])))

    def test_phase_is_consistent_with_gap_and_direction(self):
        c = self.s["ciclo"]
        self.assertEqual(c["fase"], am.fase(c["brecha_hp_tiempo_real"], c["delta_brecha"]))
        self.assertLessEqual(c["brecha_min"], c["brecha_hp_tiempo_real"])
        self.assertGreaterEqual(c["brecha_max"], c["brecha_hp_tiempo_real"])

    def test_verdict_quotes_the_numbers(self):
        for lang in ("es", "en"):
            v = mt.veredicto(self.s, lang)
            total = mt._n(self.s["inflacion"]["total"], 2, lang)
            self.assertIn(total, v["titular"])
            self.assertIn(mt._n(self.s["ciclo"]["pib_real_yoy"], 1, lang), v["actividad"])

    def test_stance_thresholds(self):
        lo, hi = mt.NEUTRAL_REAL
        self.assertEqual(mt.postura_monetaria(hi + mt.UMBRAL_POSTURA + 0.01), "restrictiva")
        self.assertEqual(mt.postura_monetaria(lo - mt.UMBRAL_POSTURA - 0.01), "expansiva")
        self.assertEqual(mt.postura_monetaria((lo + hi) / 2), "neutral")
        self.assertIsNone(mt.postura_monetaria(None))
        self.assertEqual(mt.anclaje(4.5), "desancladas")

    def test_signal_percentiles_in_range(self):
        table = mt.tabla_senales(self.d, self.s)
        self.assertGreaterEqual(len(table), 8)
        self.assertTrue(table["percentil"].dropna().between(0, 100).all())


class DashboardTests(unittest.TestCase):
    def test_page_renders_all_languages_and_horizons(self):
        for lang in ("es", "en"):
            for periodo in ("3A", "10A", "MAX"):
                page = dash_app.pagina(lang, periodo)
                self.assertGreaterEqual(len(page), 7)

    def test_single_axis_everywhere(self):
        figs = [dash_app.fig_brecha("es", "10A"), dash_app.fig_actividad("es", "10A"),
                dash_app.fig_inflacion("es", "10A"), dash_app.fig_expectativas("es", "10A"),
                dash_app.fig_pendiente("es", "10A"), dash_app.fig_colcap("es", "10A")]
        for fig in figs:
            self.assertFalse(any(getattr(tr, "yaxis", None) not in (None, "y") for tr in fig.data))

    def test_download_whitelist(self):
        client = dash_app.server.test_client()
        self.assertEqual(client.get("/datos/pib_colombia.csv").status_code, 200)
        self.assertEqual(client.get("/datos/dashboard_colombia.py").status_code, 404)
        self.assertEqual(client.get("/datos/../render.yaml").status_code, 404)

    def test_colcap_usd_uses_same_day_trm(self):
        m = dash_app.D.mercado
        if "colcap_usd" in m:
            row = m.dropna(subset=["colcap_usd"]).iloc[-1]
            self.assertAlmostEqual(row["colcap_usd"], row["colcap_puntos"] / row["trm"])


if __name__ == "__main__":
    unittest.main()
