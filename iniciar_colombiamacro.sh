#!/usr/bin/env bash
# macOS / Linux: ./iniciar_colombiamacro.sh [--actualizar] [--puerto 8090]
cd "$(dirname "$0")"
exec python3 lanzar_local.py "$@"
