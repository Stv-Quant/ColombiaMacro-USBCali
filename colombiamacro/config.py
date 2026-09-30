"""Rutas y parametros comunes del proyecto."""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.environ.get("COLOMBIAMACRO_DATA", ROOT / "data"))
CERTS_DIR = ROOT / "certs"
SITE_DIR = Path(os.environ.get("COLOMBIAMACRO_SITE", ROOT / "site"))
DOCS_DIR = ROOT / "docs"


def data(name: str) -> Path:
    return DATA_DIR / name
