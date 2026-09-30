import unittest

import numpy as np
import pandas as pd

import analitica_macro as am


class FisherBreakevenTests(unittest.TestCase):
    def test_exact_fisher(self):
        self.assertAlmostEqual(float(am.fisher_real(10.0, 5.0)), 100 * (1.10 / 1.05 - 1))

    def test_breakeven_uses_uvr_real_yield(self):
        # 12.42% pesos y 4.99% UVR (TES 1A del 2026-09-25) -> 7.08%
        self.assertAlmostEqual(float(am.breakeven(12.42, 4.99)), 7.077, places=2)

    def test_forward_5y5y_equals_flat_curve(self):
        tes = pd.DataFrame({"fecha": pd.to_datetime(["2026-01-05"]),
                            "tes_pesos_1y": [8.0], "tes_pesos_5y": [8.0], "tes_pesos_10y": [8.0],
                            "tes_uvr_1y": [3.0], "tes_uvr_5y": [3.0], "tes_uvr_10y": [3.0]})
        ipc = pd.DataFrame({"fecha": pd.to_datetime(["2025-11-01"]), "inflacion_anual": [5.0]})
        out = am.tabla_tasas(tes, None, ipc)
        self.assertAlmostEqual(out["bei_5y5y"].iloc[0], out["bei_10y"].iloc[0], places=8)

    def test_inflation_not_used_before_publication(self):
        tes = pd.DataFrame({"fecha": pd.to_datetime(["2026-09-05", "2026-09-15"]),
                            **{c: [10.0, 10.0] for c in ["tes_pesos_1y", "tes_pesos_5y", "tes_pesos_10y",
                                                          "tes_uvr_1y", "tes_uvr_5y", "tes_uvr_10y"]}})
        ipc = pd.DataFrame({"fecha": pd.to_datetime(["2026-07-01", "2026-08-01"]),
                            "inflacion_anual": [6.0, 7.0]})
        out = am.tabla_tasas(tes, None, ipc)
        # IPC de agosto se conoce ~7-sep: el 5-sep aun rige julio; el 15-sep rige agosto.
        self.assertEqual(out["inflacion_anual"].tolist(), [6.0, 7.0])

    def test_real_policy_rate(self):
        tes = pd.DataFrame({"fecha": pd.to_datetime(["2026-09-25"]),
                            "tes_pesos_1y": [12.42], "tes_pesos_5y": [12.9], "tes_pesos_10y": [13.06],
                            "tes_uvr_1y": [4.99], "tes_uvr_5y": [6.48], "tes_uvr_10y": [6.64]})
        tpm = pd.DataFrame({"fecha": pd.to_datetime(["2026-09-01"]), "tpm": [12.0]})
        ipc = pd.DataFrame({"fecha": pd.to_datetime(["2026-08-01"]), "inflacion_anual": [6.24]})
        out = am.tabla_tasas(tes, tpm, ipc).iloc[0]
        self.assertAlmostEqual(out["tpm_real_expost"], 100 * (1.12 / 1.0624 - 1), places=6)
        self.assertAlmostEqual(out["pendiente_10y_tpm"], 1.06, places=6)


class OutputGapTests(unittest.TestCase):
    def test_hp_trend_of_linear_series_is_itself(self):
        y = np.linspace(0, 10, 40)
        np.testing.assert_allclose(am.hp_trend(y), y, atol=1e-8)

    def test_one_sided_uses_no_future_data(self):
        idx = pd.date_range("2010-01-01", periods=40, freq="QS")
        y = pd.Series(np.sin(np.arange(40) / 3) + np.arange(40) * 0.5, index=idx)
        y_future_shock = y.copy()
        y_future_shock.iloc[-1] += 50
        a = am.hp_one_sided(y)
        b = am.hp_one_sided(y_future_shock)
        pd.testing.assert_series_equal(a.iloc[:-1], b.iloc[:-1])

    def test_hamilton_recovers_zero_cycle_on_random_walk_with_drift(self):
        idx = pd.date_range("2000-01-01", periods=60, freq="QS")
        y = pd.Series(np.arange(60) * 0.6, index=idx)
        np.testing.assert_allclose(am.hamilton_cycle(y).dropna(), 0, atol=1e-8)

    def test_clock_quadrants(self):
        self.assertEqual(am.fase(1, 0.2), "expansion")
        self.assertEqual(am.fase(1, -0.2), "desaceleracion")
        self.assertEqual(am.fase(-1, -0.2), "contraccion")
        self.assertEqual(am.fase(-1, 0.2), "recuperacion")
        self.assertIsNone(am.fase(np.nan, 1))

    def test_covid_interpolation_only_touches_window(self):
        idx = pd.date_range("2019-01-01", periods=16, freq="QS")
        y = pd.Series(np.arange(16, dtype=float), index=idx)
        y[pd.Timestamp("2020-04-01")] = -99
        clean = am.serie_sin_covid(y)
        self.assertAlmostEqual(clean[pd.Timestamp("2020-04-01")], 5.0, places=2)
        self.assertEqual(clean[pd.Timestamp("2019-01-01")], 0.0)


class InflationAndMarketTests(unittest.TestCase):
    def test_band_and_momentum(self):
        f = pd.date_range("2025-01-01", periods=15, freq="MS")
        ipc = pd.DataFrame({"fecha": f, "inflacion_mensual": [0.5] * 15,
                            "inflacion_anual": np.linspace(2.5, 6.0, 15)})
        out = am.regimen_inflacion(ipc)
        self.assertTrue(out["en_rango"].iloc[0])
        self.assertFalse(out["en_rango"].iloc[-1])
        self.assertAlmostEqual(out["anualizada_3m"].iloc[-1], 100 * (1.005 ** 12 - 1))

    def test_drawdown_and_usd(self):
        colcap = pd.DataFrame({"fecha": pd.to_datetime(["2026-01-02", "2026-01-05", "2026-01-06"]),
                               "colcap_puntos": [100.0, 120.0, 90.0]})
        trm = pd.DataFrame({"fecha": pd.to_datetime(["2026-01-02"]), "trm": [4000.0]})
        out = am.tabla_mercado(colcap, trm, None)
        self.assertAlmostEqual(out["drawdown_pct"].iloc[-1], -25.0)
        self.assertAlmostEqual(out["colcap_usd"].iloc[0], 0.025)

    def test_window_return(self):
        f = pd.Series(pd.to_datetime(["2025-01-01", "2025-06-01", "2026-01-01"]))
        self.assertAlmostEqual(am.retorno_ventana(pd.Series([100, 110, 121]), f, 365), 21.0)


if __name__ == "__main__":
    unittest.main()


class DerivedSpikeTests(unittest.TestCase):
    def test_isolated_derived_spike_masked(self):
        t = pd.DataFrame({"bei_5y5y": [6.0, 6.1, 3.4, 6.1, 6.2], "bei_1y": [6.0, 6.0, 6.1, 6.0, 6.1]})
        out, n = am.depurar_derivadas(t)
        self.assertEqual(n, 1)
        self.assertTrue(np.isnan(out["bei_5y5y"].iloc[2]))
        self.assertEqual(out["bei_1y"].tolist(), t["bei_1y"].tolist())
