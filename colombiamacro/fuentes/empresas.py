"""Sector empresarial: las 10.000 empresas mas grandes (Supersociedades), creacion y cancelacion de empresas
(Registro Unico Empresarial y Social, Confecamaras) y posicion financiera de las sociedades (Banco de la Republica).

Fuentes oficiales (portal de datos abiertos del Estado, datos.gov.co, y BanRep):
  6cat-2gcs  Supersociedades, "10.000 Empresas mas Grandes del Pais" (cifras en billones de pesos, cortes anuales)
  c82u-588k  Confecamaras/RUES, registro mercantil (solo se consultan conteos agregados por fecha; nunca datos personales)
  BanRep     posicion financiera neta por sector institucional (% del PIB) y deuda externa privada

Escribe:
  empresas_10000_agregados.csv  ano, dimension, categoria, empresas, ingresos, ganancia, activos, pasivos, patrimonio
  empresas_10000_top.csv        ano, puesto, empresa, macrosector, region, ingresos, ganancia, activos, pasivos, patrimonio
  empresas_registro.csv         mes, categoria, matriculas, cancelaciones
  empresas_banrep.csv           fecha, serie, valor
Uso: python -m colombiamacro.fuentes.empresas [--local carpeta]
"""

from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import requests

from colombiamacro.config import data
from colombiamacro.fuentes.banrep import banrep_ca_bundle, fetch_series, parse_payload, write_if_changed

SOCRATA = "https://www.datos.gov.co/resource/{id}.{fmt}"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
CIFRAS = ["ingresos", "ganancia", "activos", "pasivos", "patrimonio"]
BANREP = {"posicion_sociedades_no_financieras": 16811, "posicion_sociedades_financieras": 16812,
          "posicion_gobierno": 16813, "posicion_hogares": 16814, "deuda_externa_privada_musd": 15332}
TOP = 25


def leer_10000(texto: str) -> pd.DataFrame:
    d = pd.read_csv(io.StringIO(texto), dtype=str)
    num = lambda s: pd.to_numeric(s.astype(str).str.replace(r"[$\s,]", "", regex=True), errors="coerce")
    out = pd.DataFrame({
        "ano": num(d["a_o_de_corte"]).astype(int), "empresa": d["raz_n_social"].str.strip(),
        "macrosector": d["macrosector"].str.strip().str.upper(), "region": d["regi_n"].str.strip().str.upper(),
        "supervisor": d["supervisor"].str.strip().str.upper(),
        "ingresos": num(d["ingresos_operacionales"]), "ganancia": num(d["ganancia_p_rdida"]),
        "activos": num(d["total_activos"]), "pasivos": num(d["total_pasivos"]), "patrimonio": num(d["total_patrimonio"])})
    if out.groupby("ano").size().min() < 9000:
        raise ValueError("10.000 empresas: algun ano esta incompleto")
    return out


def agregar(e: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    filas = []
    for dim in ("total", "macrosector", "region", "supervisor"):
        g = e.assign(total="TOTAL").groupby(["ano", dim])
        a = g[CIFRAS].sum().join(g.size().rename("empresas")).reset_index().rename(columns={dim: "categoria"})
        a.insert(1, "dimension", dim)
        filas.append(a)
    # concentracion: participacion de las N mayores en los ingresos de cada ano
    for ano, z in e.groupby("ano"):
        z = z.sort_values("ingresos", ascending=False)
        tot = z["ingresos"].sum()
        for n in (10, 50, 100, 500, 1000, 2500, 5000, 10000):
            filas.append(pd.DataFrame([{"ano": ano, "dimension": "concentracion", "categoria": f"top{n}", "empresas": n,
                                        "ingresos": z["ingresos"].head(n).sum() / tot * 100}]))
    agg = pd.concat(filas, ignore_index=True)[["ano", "dimension", "categoria", "empresas", *CIFRAS]]
    top = (e.sort_values(["ano", "ingresos"], ascending=[True, False]).groupby("ano").head(TOP)
           .assign(puesto=lambda x: x.groupby("ano").cumcount() + 1))
    top = top[["ano", "puesto", "empresa", "macrosector", "region", *CIFRAS]]
    return agg, top


def leer_registro(mat: list, can: list) -> pd.DataFrame:
    def mes(lista, col, nombre):
        d = pd.DataFrame(lista)
        if d.empty:
            return pd.DataFrame(columns=["mes", "categoria", nombre])
        d["mes"] = pd.to_datetime(d[col].str[:6], format="%Y%m", errors="coerce")
        d["n"] = pd.to_numeric(d["count"])
        d["categoria"] = d["categoria_matricula"].fillna("SIN DATO").str.upper()
        return d.dropna(subset=["mes"]).groupby(["mes", "categoria"])["n"].sum().rename(nombre).reset_index()
    r = mes(mat, "fecha_matricula", "matriculas").merge(mes(can, "fecha_cancelacion", "cancelaciones"), on=["mes", "categoria"], how="outer")
    r = r[r["mes"] <= pd.Timestamp.today().normalize()].fillna(0)
    if r["matriculas"].sum() < 100000:
        raise ValueError("registro mercantil incompleto")
    r[["matriculas", "cancelaciones"]] = r[["matriculas", "cancelaciones"]].astype(int)
    return r.sort_values(["categoria", "mes"])


def _socrata(id_: str, params: dict, fmt="json", timeout=300):
    r = requests.get(SOCRATA.format(id=id_, fmt=fmt), params=params, headers=UA, timeout=timeout)
    r.raise_for_status()
    return r.text if fmt == "csv" else r.json()


def actualizar(local: Path | None = None) -> bool:
    ok = True
    try:
        if local:
            texto = (Path(local) / "supersociedades_10000.csv").read_text(encoding="utf-8")
        else:
            texto = _socrata("6cat-2gcs", {"$limit": 200000}, fmt="csv")
        agg, top = agregar(leer_10000(texto))
        for nombre, df in (("empresas_10000_agregados.csv", agg), ("empresas_10000_top.csv", top)):
            ch = write_if_changed(df, data(nombre), float_format="%.4f")
            print(f"{nombre}: {len(df)} filas, anos {df['ano'].min()}–{df['ano'].max()} ({'actualizado' if ch else 'sin cambios'})")
    except Exception as exc:
        ok = False
        print(f"  ERROR 10.000 empresas: {exc}")
    try:
        if local:
            reg = json.loads((Path(local) / "rues_conteos.json").read_text(encoding="utf-8"))
            mat, can = reg["mat"], reg["can"]
        else:
            base = {"$limit": 60000}
            mat = _socrata("c82u-588k", {**base, "$select": "fecha_matricula,categoria_matricula,count(*)",
                                         "$group": "fecha_matricula,categoria_matricula", "$where": "fecha_matricula>='20100101'"})
            can = _socrata("c82u-588k", {**base, "$select": "fecha_cancelacion,categoria_matricula,count(*)",
                                         "$group": "fecha_cancelacion,categoria_matricula",
                                         "$where": "fecha_cancelacion>='20100101' AND fecha_cancelacion<'99990000'"})
        r = leer_registro(mat, can)
        r["mes"] = r["mes"].dt.strftime("%Y-%m-%d")
        ch = write_if_changed(r, data("empresas_registro.csv"))
        print(f"empresas_registro.csv: {len(r)} filas ({'actualizado' if ch else 'sin cambios'})")
    except FileNotFoundError:
        print("  (sin conteos del registro mercantil en la carpeta local)")
    except Exception as exc:
        ok = False
        print(f"  ERROR registro mercantil: {exc}")
    try:
        filas = []
        if local:
            crudo = json.loads((Path(local) / "banrep_empresas.json").read_text(encoding="utf-8"))
            for n, sid in BANREP.items():
                filas.append(parse_payload(crudo[str(sid)], sid, None, "valor", drop_future=False).assign(serie=n))
        else:
            with banrep_ca_bundle() as bundle:
                for n, sid in BANREP.items():
                    filas.append(fetch_series(sid, "valor", None, verify=bundle, drop_future=False).assign(serie=n))
        b = pd.concat(filas, ignore_index=True)[["fecha", "serie", "valor"]]
        b["fecha"] = pd.to_datetime(b["fecha"]).dt.to_period("M").dt.to_timestamp().dt.strftime("%Y-%m-%d")
        ch = write_if_changed(b.sort_values(["serie", "fecha"]), data("empresas_banrep.csv"), float_format="%.4f")
        print(f"empresas_banrep.csv: {b['serie'].nunique()} series ({'actualizado' if ch else 'sin cambios'})")
    except Exception as exc:
        ok = False
        print(f"  ERROR series BanRep de empresas: {exc}")
    return ok


def cargar() -> dict | None:
    f = data("empresas_10000_agregados.csv")
    if not f.exists():
        return None
    out = {"agg": pd.read_csv(f), "top": pd.read_csv(data("empresas_10000_top.csv"))}
    r = data("empresas_registro.csv")
    out["registro"] = pd.read_csv(r, parse_dates=["mes"]) if r.exists() else None
    b = data("empresas_banrep.csv")
    out["banrep"] = ({k: g.set_index("fecha")["valor"] for k, g in pd.read_csv(b, parse_dates=["fecha"]).groupby("serie")}
                     if b.exists() else {})
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--local", type=Path)
    a = ap.parse_args()
    sys.exit(0 if actualizar(a.local) else 1)
