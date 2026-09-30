"""Actualiza todas las fuentes oficiales en secuencia.

    python -m colombiamacro.actualizar

Cada fuente corre en su propio proceso: si una falla, las demas continuan.
Todo lo que se imprime queda tambien en data/registro_actualizacion.log, que se
publica en el repositorio para diagnosticar fallas sin entrar a GitHub Actions.
Termina con codigo 1 si alguna fuente fallo (para que GitHub envie la alerta).
"""

from __future__ import annotations

import datetime as dt
import subprocess
import sys

from colombiamacro.config import ROOT, data

PASOS = [
    ("IPC — DANE y BanRep", "colombiamacro.fuentes.ipc", []),
    ("Curvas TES — BanRep", "colombiamacro.fuentes.tes", []),
    ("PIB real y nominal — DANE", "colombiamacro.fuentes.pib", []),
    ("COLCAP — BanRep", "colombiamacro.fuentes.colcap", []),
    ("Politica, TRM, inflacion basica, externo — BanRep", "colombiamacro.fuentes.complementarias", ["--solo", "banrep"]),
    ("ISE y mercado laboral — DANE", "colombiamacro.fuentes.complementarias", ["--solo", "dane"]),
]
LOG = data("registro_actualizacion.log")


def correr(nombre: str, modulo: str, extra: list[str], log) -> bool:
    cab = f"\n{'=' * 60}\n  {nombre}\n{'=' * 60}\n"
    print(cab, end="", flush=True)
    log.write(cab)
    try:
        res = subprocess.run([sys.executable, "-m", modulo, *extra], cwd=ROOT, timeout=240,
                             capture_output=True, text=True)
        salida = (res.stdout or "") + (res.stderr or "")
        ok = res.returncode == 0
    except subprocess.TimeoutExpired:
        salida, ok = "ERROR: tiempo limite (240 s)\n", False
    # Las trazas largas se recortan a sus ultimas lineas para mantener el registro legible.
    lineas = salida.strip().splitlines()
    if not ok and len(lineas) > 40:
        lineas = lineas[:5] + ["[...]"] + lineas[-30:]
    texto = "\n".join(lineas) + "\n"
    print(texto, end="", flush=True)
    log.write(texto)
    return ok


def main() -> int:
    inicio = dt.datetime.now(dt.timezone.utc)
    with LOG.open("w", encoding="utf-8", newline="\n") as log:
        log.write(f"Actualizacion ColombiaMacro — {inicio:%Y-%m-%d %H:%M} UTC\n")
        resultados = [(n, correr(n, m, e, log)) for n, m, e in PASOS]
        resumen = "\nRESUMEN\n" + "\n".join(f"  [{'OK' if ok else 'FALLO'}] {n}" for n, ok in resultados) + "\n"
        print(resumen)
        log.write(resumen)
    return 0 if all(ok for _, ok in resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
