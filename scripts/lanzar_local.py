#!/usr/bin/env python3
"""
Abre ColombiaMacro en este computador.

  1. Crea (una sola vez) el entorno .venv e instala dependencias cuando cambian.
  2. Construye el sitio (carpeta site/) con los datos de data/.
  3. Busca un puerto libre, omitiendo 8765, 8766 y cualquier puerto ocupado.
  4. Sirve el sitio en http://127.0.0.1:PUERTO y abre el navegador.

Uso:
  python scripts/lanzar_local.py                   # puerto libre desde 8050
  python scripts/lanzar_local.py --actualizar      # descarga datos oficiales antes de abrir
  python scripts/lanzar_local.py --puerto 8090 --evitar 8765 8766 3000
  python scripts/lanzar_local.py --solo-puerto     # solo informa el puerto
Hasta crear el entorno solo usa la biblioteca estandar.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import http.server
import os
import socket
import subprocess
import sys
import threading
import time
import urllib.request
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENV = ROOT / ".venv"
REQ = ROOT / "requirements.txt"
HOST = "127.0.0.1"


def log(msg):
    print(f"[ColombiaMacro] {msg}", flush=True)


def port_in_use(port: int) -> bool:
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


def find_free_port(preferred: int, avoid: set[int], span: int = 200):
    skipped = []
    for port in range(preferred, preferred + span):
        if port in avoid or port_in_use(port):
            skipped.append(port)
            continue
        return port, skipped
    raise SystemExit(f"No hay puertos libres entre {preferred} y {preferred + span}")


def venv_python() -> Path:
    return VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def ensure_env():
    if sys.version_info < (3, 10):
        sys.exit("Se requiere Python 3.10 o superior: https://www.python.org/downloads/")
    if not venv_python().exists():
        log("Creando entorno .venv (solo la primera vez)...")
        subprocess.check_call([sys.executable, "-m", "venv", str(VENV)])
    stamp = VENV / ".req_hash"
    digest = hashlib.sha256(REQ.read_bytes()).hexdigest()
    if not stamp.exists() or stamp.read_text() != digest:
        log("Instalando dependencias (1 a 3 minutos la primera vez)...")
        py = str(venv_python())
        subprocess.check_call([py, "-m", "pip", "install", "-q", "--disable-pip-version-check", "--upgrade", "pip"])
        subprocess.check_call([py, "-m", "pip", "install", "-q", "--disable-pip-version-check", "-r", str(REQ)])
        stamp.write_text(digest)


def in_venv() -> bool:
    return Path(sys.prefix).resolve() == VENV.resolve()


class Silencioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class Servidor(http.server.ThreadingHTTPServer):
    daemon_threads = True

    def handle_error(self, request, client_address):
        # El navegador cancela descargas al recargar; no es un error del tablero.
        if isinstance(sys.exc_info()[1], (ConnectionResetError, BrokenPipeError)):
            return
        super().handle_error(request, client_address)


def open_when_ready(url, browser):
    for _ in range(60):
        try:
            with urllib.request.urlopen(url, timeout=1) as r:
                r.read()
                log(f"Tablero listo en {url}   (Ctrl+C para cerrar)")
                if browser:
                    webbrowser.open(url)
                return
        except Exception:
            time.sleep(0.3)


def main():
    ap = argparse.ArgumentParser(description="Abre ColombiaMacro en local")
    ap.add_argument("--puerto", type=int, default=int(os.environ.get("PORT", 8050)))
    ap.add_argument("--evitar", type=int, nargs="*", default=[8765, 8766])
    ap.add_argument("--actualizar", action="store_true", help="descargar datos oficiales antes de abrir")
    ap.add_argument("--sin-navegador", action="store_true")
    ap.add_argument("--solo-puerto", action="store_true")
    ap.add_argument("--_interno", action="store_true", help=argparse.SUPPRESS)
    args = ap.parse_args()

    port, skipped = find_free_port(args.puerto, set(args.evitar))
    if skipped:
        log(f"Puertos omitidos (ocupados o reservados): {', '.join(map(str, skipped))}")
    log(f"Puerto elegido: {port}")
    if args.solo_puerto:
        return

    if not in_venv():
        ensure_env()
        cmd = [str(venv_python()), str(Path(__file__).resolve()), "--puerto", str(port),
               "--evitar", *map(str, args.evitar), "--_interno"]
        cmd += ["--actualizar"] if args.actualizar else []
        cmd += ["--sin-navegador"] if args.sin_navegador else []
        try:
            sys.exit(subprocess.call(cmd, cwd=ROOT))
        except KeyboardInterrupt:
            sys.exit(0)

    os.chdir(ROOT)
    if args.actualizar:
        log("Descargando fuentes oficiales (DANE, BanRep)...")
        subprocess.call([sys.executable, "-m", "colombiamacro.actualizar"])
        subprocess.call([sys.executable, "-m", "colombiamacro.validar"])
    log("Construyendo el sitio...")
    subprocess.check_call([sys.executable, "-m", "colombiamacro.sitio.construir"])

    handler = functools.partial(Silencioso, directory=str(ROOT / "site"))
    server = Servidor((HOST, port), handler)
    url = f"http://{HOST}:{port}/"
    threading.Thread(target=open_when_ready, args=(url, not args.sin_navegador), daemon=True).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("Cerrado.")


if __name__ == "__main__":
    main()
