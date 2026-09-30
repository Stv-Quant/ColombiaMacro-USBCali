"""Pruebas de la canasta del COLCAP, los precios de acciones y los indices de la seccion de empresas."""

import unittest

import numpy as np
import pandas as pd

from colombiamacro import modelo as mt
from colombiamacro.fuentes import acciones as ac

CSV = '''A fecha de,"29 sept 2026"
 
Ticker,Name,Sector,Asset Class,Market Value,Weight (%),Notional Value,Shares,Price,Location,Exchange,Currency,FX Rate,Market Currency
"PFCIBEST","GRUPO CIBEST PREF SA","Servicios Financieros","Equity","1,00","40,00","1,00","1,00","76.540,00","Colombia","Bolsa De Valores De Colombia","COP","1,00","COP"
"CIBEST","GRUPO CIBEST SA","Servicios Financieros","Equity","1,00","10,00","1,00","1,00","90.000,00","Colombia","Bolsa De Valores De Colombia","COP","1,00","COP"
''' + "\n".join(
    f'"T{i}","EMPRESA {i} SA","Energía","Equity","1,00","{w}","1,00","1,00","1.000,00","Colombia","Bolsa De Valores De Colombia","COP","1,00","COP"'
    for i, w in enumerate(["9,00", "8,00", "7,00", "6,00", "5,00", "4,00", "3,00", "2,00", "1,50", "0,50"])) + '''
"COP","COP CASH","Efectivo y/o Derivados","Cash","1,00","1,45","1,00","1,00","100,00","Colombia","-","COP","1,00","COP"
"AXL","ARROW","Energía","Equity","1,00","0,00","1,00","1,00","1,00","Canadá","TSX Venture Exchange","COP","0,00","CAD"
'''


class TestCanasta(unittest.TestCase):
    def test_parse_canasta(self):
        c = ac.parse_canasta(CSV)
        self.assertEqual(len(c), 12)                      # sin efectivo ni acciones fuera de la BVC
        self.assertEqual(c["fecha_canasta"].iloc[0], "2026-09-29")
        self.assertAlmostEqual(c.loc[c["ticker"] == "PFCIBEST", "precio"].iloc[0], 76540.0)
        self.assertAlmostEqual(c["peso"].sum(), 96.0)

    def test_emisor_agrupa_clases(self):
        self.assertEqual(ac.emisor("GRUPO CIBEST PREF SA"), ac.emisor("GRUPO CIBEST SA"))
        self.assertEqual(ac.emisor("INVERSIONES ARGOS PREF"), ac.emisor("INVERSIONES ARGOS"))
        self.assertEqual(ac.emisor("DAVIVIENDA GROUP PRF SA"), "DAVIVIENDA GROUP")

    def test_magnificas_suma_clases_y_toma_siete(self):
        m = mt.magnificas(ac.parse_canasta(CSV))
        self.assertEqual(len(m), 7)
        self.assertEqual(m.iloc[0]["emisor"], "GRUPO CIBEST")
        self.assertAlmostEqual(m.iloc[0]["peso"], 50.0)
        self.assertEqual(m.iloc[0]["ticker"], "PFCIBEST")   # la clase de mayor peso
        self.assertEqual(m.iloc[0]["clases"], "PFCIBEST + CIBEST")

    def test_canasta_incompleta_falla(self):
        corta = "\n".join(CSV.splitlines()[:5])
        with self.assertRaises(ValueError):
            ac.parse_canasta(corta)


class TestPrecios(unittest.TestCase):
    def test_parse_yahoo_fechas_viernes_y_limpieza(self):
        ts = [int(pd.Timestamp(x).timestamp()) for x in ("2024-01-01", "2024-01-08", "2024-01-15")]
        j = {"chart": {"result": [{"timestamp": ts, "indicators": {"quote": [{"close": [10.0, None, 12.0]}]}}]}}
        df = ac.parse_yahoo(j)
        self.assertEqual(list(df["fecha"].dt.dayofweek), [4, 4])
        self.assertEqual(list(df["cierre"]), [10.0, 12.0])

    def test_semana_en_curso_no_es_futura(self):
        hoy = pd.Timestamp.today().normalize()
        self.assertLessEqual(ac.viernes(pd.Series([hoy])).iloc[0], hoy)

    def test_yahoo_sin_datos_falla(self):
        with self.assertRaises(ValueError):
            ac.parse_yahoo({"chart": {"result": None, "error": {"code": "Not Found"}}})

    def test_empalme_sin_salto(self):
        viejo = pd.DataFrame({"fecha": pd.date_range("2020-01-03", periods=5, freq="W-FRI"), "cierre": [10, 11, 12, 13, 14.0]})
        nuevo = pd.DataFrame({"fecha": pd.date_range("2020-01-24", periods=3, freq="W-FRI"), "cierre": [26, 28, 30.0]})
        out = ac.empalmar(nuevo, viejo)
        self.assertEqual(len(out), 6)
        r = out["cierre"].pct_change().dropna()
        self.assertAlmostEqual(r.iloc[1], 12 / 11 - 1)       # retornos historicos intactos
        self.assertAlmostEqual(out["cierre"].iloc[3], 26.0)  # sin salto en la union

    def test_combinar_conserva_acciones_que_fallaron(self):
        f = pd.date_range("2020-01-03", periods=30, freq="W-FRI")
        previo = pd.DataFrame({"fecha": list(f) * 2, "ticker": ["A"] * 30 + ["B"] * 30,
                               "simbolo": ["A.CL"] * 30 + ["B.CL"] * 30, "cierre": [1.0] * 60})
        nuevo = pd.DataFrame({"fecha": f, "cierre": [2.0] * 30})
        out = ac.combinar(previo, {"A": (nuevo, "A.CL")})
        self.assertEqual(set(out["ticker"]), {"A", "B"})
        self.assertTrue((out.loc[out["ticker"] == "A", "cierre"] == 2).all())
        self.assertTrue((out.loc[out["ticker"] == "B", "cierre"] == 1).all())


class TestIndices(unittest.TestCase):
    def test_equiponderado_promedia_retornos(self):
        f = pd.date_range("2024-01-05", periods=3, freq="W-FRI")
        acc = pd.DataFrame({"fecha": list(f) * 2, "ticker": ["A"] * 3 + ["B"] * 3,
                            "cierre": [100, 110, 121, 100, 90, 90]})
        r = mt.retornos_semanales(acc)
        ix = mt.indice_equiponderado(r)
        self.assertAlmostEqual(ix.iloc[0], 100)
        self.assertAlmostEqual(ix.iloc[1], 100 * (1 + (0.10 - 0.10) / 2))
        self.assertAlmostEqual(ix.iloc[2], ix.iloc[1] * (1 + (0.10 + 0.0) / 2))

    def test_saltos_de_fuente_se_descartan(self):
        f = pd.date_range("2024-01-05", periods=3, freq="W-FRI")
        acc = pd.DataFrame({"fecha": f, "ticker": "A", "cierre": [100, 1000, 1000]})
        self.assertTrue(np.isnan(mt.retornos_semanales(acc)["A"].iloc[1]))

    def test_bolsa_por_dentro_con_datos_del_repositorio(self):
        d = mt.cargar()
        b = mt.bolsa_por_dentro(d)
        if b is None:
            self.skipTest("sin datos de acciones")
        ix = b["indices"]
        self.assertEqual(list(ix.columns), ["fecha", "colcap", "equiponderado", "magnificas"])
        self.assertTrue(np.allclose(ix.iloc[0, 1:].astype(float), 100))
        self.assertLessEqual(ix["fecha"].max(), pd.Timestamp.today().normalize())
        self.assertEqual(len(b["magnificas"]), 7)
        self.assertTrue(0 < b["peso_magnificas"] <= 100)


if __name__ == "__main__":
    unittest.main()
