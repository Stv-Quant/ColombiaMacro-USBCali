#!/usr/bin/env python3
"""
Lanzador local de ColombiaMacro.

Hace todo lo necesario para ver el tablero en este computador:
  1. Crea (una sola vez) un entorno virtual .venv junto al proyecto.
  2. Instala o actualiza dependencias solo si cambiaron los requirements.
  3. Busca un puerto libre, saltando los ocupados y los reservados (8765, 8766 por defecto).
  4. Levanta el servidor (waitress) y abre el navegador cuando responde.

Uso:
  python lanzar_local.py                      # puerto libre desde 8050
  python lanzar_local.py --puerto 8090        # preferir un puerto (si esta ocupado busca otro)
  python lanzar_local.py --evitar 8765 8766 3000
  python lanzar_local.py --actualizar         # descarga datos oficiales antes de abrir
  python lanzar_local.py --legacy             # abre el tablero v8
  python lanzar_local.py --solo-puerto        # solo informa que puerto usaria
Solo usa la biblioteca estandar hasta que el entorno virtual existe.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import socket
import subprocess
import sys
import threading
import time
import urllib.request
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV = ROOT / ".venv"
REQ_VIEW = [ROOT / "requirements.txt", ROOT / "requirements-local.txt"]
REQ_UPDATE = ROOT / "requirements-update.txt"
DEFAULT_START = 8050
DEFAULT_AVOID = [8765, 8766]
HOST = "127.0.0.1"


def log(msg: str) -> None:
    print(f"[ColombiaMacro] {msg}", flush=True)


# ------------------------------------------------------------------ puertos
def port_in_use(port: int) -> bool:
    """True si algo escucha en el puerto (IPv4 o IPv6) o si no se puede reservar."""
    for family, addr in ((socket.AF_INET, HOST), (socket.AF_INET6, "::1")):
        try:
            with socket.socket(family, socket.SOCK_STREAM) as s:
                s.settimeout(0.3)
                if s.connect_ex((addr, port)) == 0:
                    return True
        except OSError:
            pass
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, port))
    except OSError:
        return True
    return False


def find_free_port(preferred: int, avoid: set[int], span: int = 200) -> tuple[int, list[int]]:
    busy = []
    for port in range(preferred, preferred + span):
        if port in avoid:
            busy.append(port)
            continue
        if port_in_use(port):
            busy.append(port)
            continue
        return port, busy
    raise RuntimeError(f"No hay puertos libres entre {preferred} y {preferred + span}")


# ------------------------------------------------------------------ entorno
def venv_python() -> Path:
    return VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def in_venv() -> bool:
    return Path(sys.prefix).resolve() == VENV.resolve()


def req_hash(files: list[Path]) -> str:
    h = hashlib.sha256()
    for f in files:
        if f.exists():
            h.update(f.read_bytes())
    return h.hexdigest()


def ensure_env(with_update: bool) -> None:
    if sys.version_info < (3, 10):
        sys.exit("Se requiere Python 3.10 o superior (https://www.python.org/downloads/).")
    if not venv_python().exists():
        log("Creando entorno virtual .venv (solo la primera vez)...")
        subprocess.check_call([sys.executable, "-m", "venv", str(VENV)])
    files = REQ_VIEW + ([REQ_UPDATE] if with_update else [])
    stamp = VENV / (".req_update" if with_update else ".req_view")
    digest = req_hash(files)
    if not stamp.exists() or stamp.read_text() != digest:
        log("Instalando dependencias (puede tardar 1-3 minutos la primera vez)...")
        py = str(venv_python())
        subprocess.check_call([py, "-m", "pip", "install", "--disable-pip-version-check", "-q", "--upgrade", "pip"])
        for f in files:
            if f.exists():
                subprocess.check_call([py, "-m", "pip", "install", "--disable-pip-version-check", "-q", "-r", str(f)])
        stamp.write_text(digest)


# ------------------------------------------------------------------ servidor
def wait_and_open(url: str, open_browser: bool) -> None:
    for _ in range(120):
        try:
            with urllib.request.urlopen(url, timeout=1) as r:
                if r.status == 200:
                    log(f"Tablero listo en {url}  (Ctrl+C para detener)")
                    if open_browser:
                        webbrowser.open(url)
                    return
        except Exception:
            time.sleep(0.5)
    log("El servidor tarda en responder; revise los mensajes de arriba.")


def serve(port: int, legacy: bool, open_browser: bool) -> None:
    os.chdir(ROOT)
    sys.path.insert(0, str(ROOT))
    module = __import__("dashboard_legacy" if legacy else "dashboard_colombia")
    url = f"http://{HOST}:{port}/"
    threading.Thread(target=wait_and_open, args=(url, open_browser), daemon=True).start()
    try:
        from waitress import serve as wserve
        log(f"Servidor waitress en {url}")
        wserve(module.server, host=HOST, port=port, threads=8, _quiet=True)
    except ImportError:
        log(f"Servidor Dash en {url}")
        module.app.run(host=HOST, port=port, debug=False)


def main() -> None:
    ap = argparse.ArgumentParser(description="Abre ColombiaMacro en local con un puerto libre.")
    ap.add_argument("--puerto", type=int, default=int(os.environ.get("PORT", DEFAULT_START)))
    ap.add_argument("--evitar", type=int, nargs="*", default=DEFAULT_AVOID)
    ap.add_argument("--actualizar", action="store_true", help="descargar datos oficiales antes de abrir")
    ap.add_argument("--legacy", action="store_true", help="abrir el tablero anterior (v8)")
    ap.add_argument("--sin-navegador", action="store_true")
    ap.add_argument("--solo-puerto", action="store_true", help="solo mostrar el puerto elegido")
    ap.add_argument("--_interno", action="store_true", help=argparse.SUPPRESS)
    args = ap.parse_args()

    port, busy = find_free_port(args.puerto, set(args.evitar))
    if busy:
        log(f"Puertos omitidos (ocupados o reservados): {', '.join(map(str, busy))}")
    log(f"Puerto elegido: {port}")
    if args.solo_puerto:
        return

    if not in_venv():
        ensure_env(args.actualizar)
        cmd = [str(venv_python()), str(Path(__file__).resolve()), "--puerto", str(port),
               "--evitar", *map(str, args.evitar), "--_interno"]
        cmd += ["--actualizar"] if args.actualizar else []
        cmd += ["--legacy"] if args.legacy else []
        cmd += ["--sin-navegador"] if args.sin_navegador else []
        try:
            sys.exit(subprocess.call(cmd))
        except KeyboardInterrupt:
            sys.exit(0)

    if args.actualizar:
        log("Descargando fuentes oficiales (DANE, BanRep)...")
        subprocess.call([sys.executable, str(ROOT / "actualizar_todo.py")])
        subprocess.call([sys.executable, str(ROOT / "validar_datos.py")])
    try:
        serve(port, args.legacy, not args.sin_navegador)
    except KeyboardInterrupt:
        log("Detenido.")


if __name__ == "__main__":
    main()
