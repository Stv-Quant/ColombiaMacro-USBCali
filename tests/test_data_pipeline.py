import unittest
import hashlib
import ssl
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd

from actualizar_tes import INTERMEDIATE_CERT, banrep_ca_bundle, descargar_serie
from actualizar_pib import build_table
from construir_tablas_experimentales import calculate
from validar_datos import isolated_tes_spikes


class DataPipelineTests(unittest.TestCase):
    def test_tes_ca_bundle_completes_verified_chain(self):
        certificate = INTERMEDIATE_CERT.read_text(encoding="ascii")
        fingerprint = hashlib.sha256(ssl.PEM_cert_to_DER_cert(certificate)).hexdigest()
        self.assertEqual(fingerprint, "2d140f20b8a96e2b4d2f1cc5aca5e5a1e7dc56a7491e510906960f38d2d21aef")
        with banrep_ca_bundle() as bundle:
            contents = Path(bundle).read_text(encoding="ascii")
            self.assertIn(certificate.strip(), contents)
            self.assertGreater(contents.count("-----BEGIN CERTIFICATE-----"), 100)
        self.assertFalse(Path(bundle).exists())

    def test_tes_request_uses_ca_bundle(self):
        response = Mock()
        response.json.return_value = [{"id": 15272, "data": [[1726617600000, 12.38]]}]
        with patch("actualizar_tes.requests.get", return_value=response) as get:
            result = descargar_serie("tes_pesos_1y", 15272, "verified-bundle.pem")
        self.assertEqual(result.iloc[0]["tes_pesos_1y"], 12.38)
        self.assertEqual(get.call_args.kwargs["verify"], "verified-bundle.pem")

    def test_real_and_nominal_growth_are_distinct(self):
        dates = pd.date_range("2023-01-01", periods=9, freq="QS")
        real = pd.Series([100, 100, 100, 100, 110, 110, 110, 110, 121], index=dates)
        adjusted = pd.Series([100, 102, 104, 106, 108, 110, 112, 114, 116], index=dates)
        nominal = pd.Series([200, 200, 200, 200, 300, 300, 300, 300, 450], index=dates)
        table = build_table(real, adjusted, nominal, pd.Timestamp("2025-08-01"), "DANE")
        self.assertAlmostEqual(table.iloc[-1]["pib_real_yoy"], 10)
        self.assertAlmostEqual(table.iloc[-1]["pib_nominal_yoy"], 50)
        self.assertEqual(table.iloc[-1]["trimestre"], "T1 2025")

    def test_incomplete_month_does_not_publish_return(self):
        tickers = ["ECOPETROL", "PFBCOLOM", "GRUPOSURA", "GRUPOARGOS",
                   "PFAVAL", "ISA", "NUTRESA"]
        dates = pd.to_datetime(["2026-01-01", "2026-02-01", "2026-03-01"])
        prices = pd.DataFrame([[100] * 7, [105] * 7, [110, 110] + [None] * 5],
                              index=dates, columns=tickers)
        baskets = {date: frozenset(tickers) for date in dates}
        table = calculate(prices, baskets, today="2026-03-20")
        self.assertAlmostEqual(table.iloc[0]["retorno_equiponderado_pct"], 5)
        self.assertTrue(pd.isna(table.iloc[1]["retorno_equiponderado_pct"]))
        self.assertEqual(table.iloc[1]["estado"], "sin_cobertura_o_atipicos")

    def test_isolated_tes_spike_is_flagged(self):
        flags = isolated_tes_spikes(pd.Series([10.0, 10.2, 0.5, 10.1, 10.2]))
        self.assertEqual(flags.tolist(), [False, False, True, False, False])


if __name__ == "__main__":
    unittest.main()


class BanrepClientTests(unittest.TestCase):
    def test_payload_identity_and_accents(self):
        from banrep_client import parse_payload
        payload = [{"id": 59, "nombre": "Tasa de política monetaria",
                    "data": [[1790658000000, 12.0], [1790744400000, None]]}]
        df = parse_payload(payload, 59, "politica monetaria", "tpm")
        self.assertEqual(df["tpm"].tolist(), [12.0])
        with self.assertRaises(ValueError):
            parse_payload(payload, 60, None, "tpm")
        with self.assertRaises(ValueError):
            parse_payload(payload, 59, "Tasa Representativa", "tpm")

    def test_colcap_and_ipc_use_banrep_bundle(self):
        import actualizar_colcap, actualizar_inflacion
        self.assertTrue(hasattr(actualizar_colcap, "banrep_ca_bundle"))
        self.assertTrue(hasattr(actualizar_inflacion, "banrep_ca_bundle"))
        self.assertNotIn("truststore", Path("actualizar_colcap.py").read_text(encoding="utf-8"))
        self.assertNotIn("truststore", Path("actualizar_inflacion.py").read_text(encoding="utf-8"))


class DaneAnnexTests(unittest.TestCase):
    def test_parse_dane_block_years_months(self):
        from actualizar_macro_extra import parse_dane_block
        rows = [["titulo"], ["Concepto", 2025, None, 2026],
                [None, "Enero", "Febrero", "Ene"],
                ["Indicador de Seguimiento a la Economía", 100.0, 101.0, 102.5],
                ["Fuente: DANE"],
                ["Indicador de Seguimiento a la Economía", 9, 9, 9]]
        df = parse_dane_block(rows, {"Indicador de Seguimiento a la Economía": "ise"})
        self.assertEqual(df["fecha"].dt.strftime("%Y-%m").tolist(), ["2025-01", "2025-02", "2026-01"])
        self.assertEqual(df["ise"].tolist(), [100.0, 101.0, 102.5])

    def test_long_table_drops_future_and_normalizes(self):
        from actualizar_macro_extra import build_long, MIN_OBS
        dates = pd.date_range("2010-01-31", periods=200, freq="ME")
        frame = pd.DataFrame({"fecha": list(dates) + [pd.Timestamp("2099-12-31")],
                              "itcr_ipc": [100.0] * 201})
        out = build_long({"itcr_ipc": frame})
        self.assertEqual(out["fecha"].min(), pd.Timestamp("2010-01-01"))
        self.assertLess(out["fecha"].max(), pd.Timestamp("2099-01-01"))
        self.assertTrue((out["id_banrep"] == 235).all())
