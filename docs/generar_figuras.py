"""Figuras vectoriales (PDF) para el manual y la presentacion academica.

Usa exactamente los mismos calculos del tablero (modelo_tablero / analitica_macro),
de modo que cada numero de las diapositivas coincide con el tablero en linea.

    python docs/generar_figuras.py            # escribe docs/figuras/*.pdf y *.png
    MACRO_DATA_DIR=/ruta python docs/...      # otra carpeta de datos
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import analitica_macro as am  # noqa: E402
import modelo_tablero as mt  # noqa: E402

OUT = Path(__file__).resolve().parent / "figuras"
OUT.mkdir(exist_ok=True)

C1, C2, C3, C4, C7 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#4a3aa7"
GRAY, INK, MUTED = "#a3a19b", "#1f1f1d", "#6b6a66"
FASE_COLOR = {k: v[2] for k, v in am.FASES.items()}

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "axes.titlesize": 11, "axes.labelsize": 10,
    "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#c9c7c1",
    "axes.grid": True, "grid.color": "#ecebe6", "grid.linewidth": 0.8, "axes.axisbelow": True,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.labelcolor": MUTED,
    "legend.frameon": False, "legend.fontsize": 9, "figure.dpi": 150, "savefig.bbox": "tight",
    "lines.linewidth": 1.8,
})


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf")
    fig.savefig(OUT / f"{name}.png", dpi=220)
    plt.close(fig)


def qend(s):
    return s + pd.offsets.QuarterEnd(0)


def fmt_dates(ax):
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))


def main():
    d = mt.cargar()
    s = mt.instantanea(d)
    desde = pd.Timestamp("2012-01-01")

    # 1. Brecha del producto con banda entre metodos
    c = d.ciclo.dropna(subset=["brecha_hp_tiempo_real"])
    c = c[c["fecha"] >= desde]
    x = qend(c["fecha"])
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.fill_between(x, c["brecha_min"], c["brecha_max"], color=C1, alpha=0.15, lw=0, label="Rango entre métodos")
    ax.plot(x, c["brecha_hamilton"], color=GRAY, lw=1.1, label="Hamilton (2018)")
    ax.plot(x, c["brecha_hp_dos_colas"], color=C7, lw=1.1, ls="--", label="HP dos colas")
    ax.plot(x, c["brecha_hp_tiempo_real"], color=C1, marker="o", ms=3, label="HP en tiempo real")
    ax.axhline(0, color=INK, lw=0.8)
    ax.axvspan(pd.Timestamp(am.COVID_DESDE), pd.Timestamp("2021-06-30"), color="black", alpha=0.05, lw=0)
    ax.set_ylim(-4, 6)
    ax.annotate("2020: −17% (fuera de escala)", xy=(pd.Timestamp("2020-06-30"), -4), xytext=(pd.Timestamp("2022-06-01"), -3.5),
                fontsize=8, color=MUTED, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))
    ax.set_ylabel("% del PIB potencial")
    fmt_dates(ax)
    ax.legend(ncol=4, loc="upper left", bbox_to_anchor=(0, 1.13))
    save(fig, "brecha_producto")

    # 2. Reloj del ciclo
    r = d.ciclo.dropna(subset=["brecha_hp_tiempo_real", "delta_brecha"]).tail(12)
    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    lim_x = max(2.0, r["brecha_hp_tiempo_real"].abs().max() * 1.25)
    lim_y = max(1.5, r["delta_brecha"].abs().max() * 1.25)
    ax.axhline(0, color="#c9c7c1", lw=0.8); ax.axvline(0, color="#c9c7c1", lw=0.8)
    ax.plot(r["brecha_hp_tiempo_real"], r["delta_brecha"], color=GRAY, lw=0.8)
    ax.scatter(r["brecha_hp_tiempo_real"], r["delta_brecha"], s=[22] * (len(r) - 1) + [110],
               c=[FASE_COLOR[f] for f in r["fase"]], edgecolor="white", linewidth=1.2, zorder=3)
    last = r.iloc[-1]
    ax.annotate(last["trimestre"], (last["brecha_hp_tiempo_real"], last["delta_brecha"]), xytext=(8, 8),
                textcoords="offset points", fontsize=9, color=INK)
    for k, (sx, sy) in {"expansion": (1, 1), "desaceleracion": (1, -1), "contraccion": (-1, -1), "recuperacion": (-1, 1)}.items():
        ax.text(sx * lim_x * 0.95, sy * lim_y * 0.92, am.FASES[k][0], color=FASE_COLOR[k], fontsize=9,
                ha="right" if sx > 0 else "left", va="top" if sy > 0 else "bottom")
    ax.set_xlim(-lim_x, lim_x); ax.set_ylim(-lim_y, lim_y)
    ax.set_xlabel("Brecha del producto (%)"); ax.set_ylabel("Cambio en 2 trimestres (pp)")
    save(fig, "reloj_ciclo")

    # 3. Inflacion total, basica y rango meta
    inf = d.inflacion[d.inflacion["fecha"] >= desde]
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    ax.axhspan(2, 4, color=C3, alpha=0.10, lw=0); ax.axhline(3, color=C3, lw=0.9)
    ax.plot(inf["fecha"], inf["inflacion_anual"], color=C1, label="IPC total")
    if "inflacion_basica_sar" in inf:
        ax.plot(inf["fecha"], inf["inflacion_basica_sar"], color=C2, label="Básica sin alimentos ni regulados")
    ax.text(inf["fecha"].min(), 4.15, "Meta 3% ± 1 pp", color=C3, fontsize=8)
    ax.set_ylabel("% anual"); fmt_dates(ax); ax.legend(loc="upper left")
    save(fig, "inflacion")

    # 4. Expectativas: implicitas
    t = d.tasas.set_index("fecha")[["bei_1y", "bei_5y5y", "tpm_real_exante", "tpm_real_expost", "tpm",
                                     "pendiente_10y_1y"] if "tpm" in d.tasas else ["bei_1y", "bei_5y5y", "pendiente_10y_1y"]]
    w = t.resample("W-FRI").last()
    w = w[w.index >= desde]
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    ax.axhspan(2, 4, color=C3, alpha=0.10, lw=0)
    ax.plot(inf["fecha"], inf["inflacion_anual"], color=GRAY, lw=1.2, label="IPC observado")
    ax.plot(w.index, w["bei_1y"], color=C1, lw=1.4, label="Implícita 1 año")
    ax.plot(w.index, w["bei_5y5y"], color=C7, lw=1.4, label="Implícita 5y5y")
    ax.set_ylabel("%"); fmt_dates(ax); ax.legend(loc="upper left", ncol=3)
    save(fig, "expectativas")

    # 5. Tasa real frente a neutral
    if "tpm_real_exante" in w:
        fig, ax = plt.subplots(figsize=(7.2, 3.3))
        lo, hi = mt.NEUTRAL_REAL
        ax.axhspan(lo, hi, color="#52514e", alpha=0.12, lw=0)
        ax.text(w.index.min(), hi + 0.45, f"Neutral estimada BanRep {lo:.1f}–{hi:.1f}%".replace(".", ","), fontsize=8, color=MUTED)
        ax.plot(w.index, w["tpm_real_exante"], color=C1, label="Ex ante (deflactada con implícita 1A)")
        ax.plot(w.index, w["tpm_real_expost"], color=GRAY, lw=1.2, label="Ex post (deflactada con IPC)")
        ax.axhline(0, color=INK, lw=0.8)
        ax.set_ylabel("% real"); fmt_dates(ax); ax.legend(loc="lower left")
        save(fig, "tasa_real")

    # 6. Curva de rendimientos
    tt = d.tasas.dropna(subset=["tes_pesos_10y"])
    hoy = tt["fecha"].max()
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    for dias, color, lab in ((0, C1, "hoy"), (91, C2, "hace 3 meses"), (365, GRAY, "hace 12 meses")):
        row = tt[tt["fecha"] <= hoy - pd.Timedelta(days=dias)].iloc[-1]
        ax.plot([1, 5, 10], [row["tes_pesos_1y"], row["tes_pesos_5y"], row["tes_pesos_10y"]], marker="o",
                color=color, label=f"{row['fecha']:%d-%m-%Y} ({lab})")
    ax.set_xticks([1, 5, 10]); ax.set_xticklabels(["1 año", "5 años", "10 años"])
    ax.set_ylabel("% e.a."); ax.legend(loc="lower right")
    save(fig, "curva_tes")

    # 7. Validacion: implicita 1A vs inflacion realizada 12 meses despues
    bei = d.tasas.set_index("fecha")["bei_1y"].resample("MS").mean()
    ipc = d.ipc.set_index("fecha")["inflacion_anual"]
    v = pd.DataFrame({"bei": bei, "real12": ipc.shift(-12), "hoy": ipc}).dropna()
    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    pre = v[v.index < "2020-01-01"]; post = v[v.index >= "2020-01-01"]
    ax.scatter(pre["bei"], pre["real12"], s=12, color=C1, alpha=0.7, label="2006–2019")
    ax.scatter(post["bei"], post["real12"], s=12, color=C2, alpha=0.7, label="2020–2025")
    lim = [0, max(v.max()) + 1]
    ax.plot(lim, lim, color=INK, lw=0.8)
    ax.set_xlim(lim); ax.set_ylim(lim)
    ax.set_xlabel("Inflación implícita a 1 año en t (%)"); ax.set_ylabel("Inflación realizada en t+12 (%)")
    ax.legend(loc="upper left")
    save(fig, "validacion_bei")
    e = v["real12"] - v["bei"]; rw = v["real12"] - v["hoy"]
    stats = {}
    for name, sub in (("2006-2019", v[v.index < "2020-01-01"]), ("2020-2025", v[v.index >= "2020-01-01"]), ("total", v)):
        ee = sub["real12"] - sub["bei"]; rr = sub["real12"] - sub["hoy"]
        stats[name] = {"n": int(len(sub)), "sesgo": round(float(ee.mean()), 2),
                       "rmse_bei": round(float(np.sqrt((ee ** 2).mean())), 2),
                       "rmse_rw": round(float(np.sqrt((rr ** 2).mean())), 2)}

    # 8. COLCAP pesos y dolares
    m = d.mercado[d.mercado["fecha"] >= desde].set_index("fecha")
    mw = m.resample("W-FRI").last()
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    ax.plot(mw.index, 100 * mw["colcap_puntos"] / mw["colcap_puntos"].dropna().iloc[0], color=C1, label="COLCAP en pesos")
    if "colcap_usd" in mw and mw["colcap_usd"].notna().any():
        u = mw["colcap_usd"].dropna()
        ax.plot(u.index, 100 * u / u.iloc[0], color=C2, label="COLCAP en dólares")
    ax.axvline(pd.Timestamp("2021-05-28"), color=MUTED, lw=0.8, ls=":")
    ax.text(pd.Timestamp("2021-06-15"), ax.get_ylim()[1] * 0.95, "BVC → MSCI", fontsize=8, color=MUTED)
    ax.axhline(100, color=INK, lw=0.8)
    ax.set_ylabel(f"Índice ({desde.year} = 100)"); fmt_dates(ax); ax.legend(loc="upper left")
    save(fig, "colcap")

    resumen = {
        "fase": s["ciclo"]["fase"], "trimestre": s["ciclo"]["trimestre"],
        "pib_yoy": round(s["ciclo"]["pib_real_yoy"], 2), "brecha": round(s["ciclo"]["brecha_hp_tiempo_real"], 2),
        "brecha_min": round(s["ciclo"]["brecha_min"], 2), "brecha_max": round(s["ciclo"]["brecha_max"], 2),
        "potencial": round(s["ciclo"]["crecimiento_potencial_hp"], 2),
        "ipc": s["inflacion"]["total"], "ipc_mes": f"{s['inflacion']['fecha']:%Y-%m}",
        "basica": s["inflacion"].get("basica"), "tpm": s["tasas"].get("tpm"),
        "real_exante": None if s["tasas"].get("tpm_real_exante") is None else round(s["tasas"]["tpm_real_exante"], 2),
        "bei_1y": round(s["tasas"]["bei_1y"], 2), "bei_5y5y": round(s["tasas"]["bei_5y5y"], 2),
        "tes10": s["tasas"]["tes_pesos_10y"], "colcap_12m": round(float(s["mercado"]["colcap_12m"]), 1),
        "validacion_bei": stats,
    }
    (OUT / "resumen.json").write_text(json.dumps(resumen, indent=2, ensure_ascii=False, default=str))
    print(json.dumps(resumen, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
