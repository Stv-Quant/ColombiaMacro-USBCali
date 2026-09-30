"""Pruebas de PIB por sectores e informalidad laboral."""

import unittest

import pandas as pd

from colombiamacro import modelo as mt
from colombiamacro.fuentes import informalidad as inf
from colombiamacro.fuentes import pib


class TestSectores(unittest.TestCase):
    def niveles(self):
        f = pd.date_range("2020-01-01", periods=9, freq="QS")
        d = {code: [100.0 + 10 * k for k in range(9)] for code in pib.SECTORES}
        d["C"] = [100.0] * 4 + [110.0] * 5          # industria +10% a/a desde 2021
        df = pd.DataFrame(d, index=f)
        df["VA"] = df.sum(axis=1)
        return df

    def test_crecimiento_peso_y_aporte(self):
        s = pib.build_sectores(self.niveles())
        c = s[(s["codigo"] == "C") & (s["fecha"] == "2021-01-01")].iloc[0]
        self.assertAlmostEqual(c["yoy"], 10.0)
        va = self.niveles()["VA"]
        self.assertAlmostEqual(c["contribucion"], 10 / va.iloc[0] * 100)
        self.assertEqual(s.groupby("fecha")["codigo"].nunique().min(), 12)
        pesos = s[s["fecha"] == "2021-01-01"]["peso"].sum()
        self.assertAlmostEqual(pesos, 100.0)

    def test_datos_del_repositorio(self):
        d = mt.cargar()
        if d.sectores is None:
            self.skipTest("sin pib_sectores.csv")
        ult = d.sectores[d.sectores["fecha"] == d.sectores["fecha"].max()]
        self.assertEqual(len(ult), 12)
        # volumenes encadenados: no aditivos, la suma de pesos se aparta levemente de 100
        self.assertAlmostEqual(ult["peso"].sum(), 100.0, delta=2)
        self.assertEqual(d.sectores["fecha"].max(), d.pib["fecha"].max())


class TestInformalidad(unittest.TestCase):
    def test_secuencia_de_trimestres_moviles(self):
        anos = (None, 2021, None, None, None)
        rotulos = (None, "Ene - mar", "Feb - abr", "Mar - may", "Abr - jun")
        f = inf.fechas_columnas(anos, rotulos)
        self.assertEqual(f[1], pd.Timestamp("2021-03-01"))
        self.assertEqual(f[4], pd.Timestamp("2021-06-01"))

    def test_cambio_de_ano_en_rotulos(self):
        anos = (None, 2021, None, None)
        rotulos = (None, "Oct - dic", "Nov 21 - ene 22", "Dic 21 - feb 22")
        f = inf.fechas_columnas(anos, rotulos)
        self.assertEqual(f[3], pd.Timestamp("2022-02-01"))

    def test_secuencia_rota_falla(self):
        with self.assertRaises(ValueError):
            inf.fechas_columnas((None, 2021, None), (None, "Ene - mar", "Mar - may"))

    def test_ramas_cortas(self):
        self.assertEqual(inf.rama_corta("Agricultura, ganadería, caza, silvicultura y pesca"), "Agro y pesca")
        self.assertEqual(inf.rama_corta("Administración pública y defensa, educación"), "Gobierno, educación y salud")
        self.assertIsNone(inf.rama_corta("No informa"))

    def test_datos_del_repositorio(self):
        d = mt.cargar()
        if d.informalidad is None:
            self.skipTest("sin informalidad.csv")
        i = d.informalidad
        self.assertTrue(i["nacional"].between(40, 70).all())
        self.assertTrue((i["ciudades_13"] < i["nacional"]).all())   # las ciudades son menos informales
        self.assertEqual(list(i["fecha"]), list(pd.date_range(i["fecha"].min(), i["fecha"].max(), freq="MS")))
        r = d.informalidad_ramas
        u = r[r["fecha"] == r["fecha"].max()]
        self.assertEqual(len(u), 13)
        # la suma por ramas reproduce la tasa nacional publicada
        tasa = 100 * u["informales"].sum() / u["ocupados"].sum()
        self.assertAlmostEqual(tasa, i.iloc[-1]["nacional"], delta=0.2)


if __name__ == "__main__":
    unittest.main()


class TestNoticias(unittest.TestCase):
    def test_publicaciones_oficiales(self):
        from colombiamacro import noticias as nt
        d = mt.cargar()
        s = mt.instantanea(d)
        for lang in ("es", "en"):
            items = nt.publicaciones(d, s, lang)
            self.assertGreaterEqual(len(items), 5)
            fechas = [i["fecha"] for i in items]
            self.assertEqual(fechas, sorted(fechas, reverse=True))
            self.assertTrue(all(i["enlace"].startswith("https://") for i in items))
            self.assertTrue(all(i["fecha"] <= pd.Timestamp.today().normalize() for i in items))
            fuentes = {i["fuente"] for i in items}
            self.assertIn("DANE", fuentes)


class TestTrayectoria(unittest.TestCase):
    def test_tramos_reproducen_el_breakeven_a_10_anos(self):
        from colombiamacro.sitio import construir as cs
        d = mt.cargar()
        fig, meta, tramos = cs.Graficos(d, mt.instantanea(d), "es").trayectoria_inflacion()
        if fig is None:
            self.skipTest("sin breakevens")
        (a0, a1, b1), (_, _, f15), (_, _, f510) = tramos
        prod = (1 + b1 / 100) * (1 + f15 / 100) ** 4 * (1 + f510 / 100) ** 5
        ult = d.tasas.dropna(subset=["bei_10y"]).iloc[-1]
        self.assertAlmostEqual(prod ** 0.1 - 1, ult["bei_10y"] / 100, places=8)
        self.assertAlmostEqual(f510, ult["bei_5y5y"], places=6)
