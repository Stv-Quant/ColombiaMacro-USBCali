"""Cliente unico para el graficador de series de BanRep (suameca).

Motivo: suameca.banrep.gov.co envia su certificado hoja sin el intermedio
GeoTrust EV RSA CA G2. Los navegadores lo completan (AIA), pero OpenSSL en
GitHub Actions no. Antes solo `actualizar_tes.py` completaba la cadena; COLCAP
e IPC usaban `truststore` y fallaban en Linux (COLCAP quedo congelado el
2026-09-24 mientras TES seguia actualizando). Todas las series BanRep pasan
ahora por este modulo.
"""

from __future__ import annotations

import datetime as _dt
import tempfile
import unicodedata
from contextlib import contextmanager
from pathlib import Path

import pandas as pd
import requests

BASE_DIR = Path(__file__).resolve().parent
INTERMEDIATE_CERT = BASE_DIR / "certs" / "GeoTrustEVRSACAG2.pem"

API = ("https://suameca.banrep.gov.co/graficador-series/rest/"
       "graficadorService/consultaSerieParaGraficar")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    "Accept": "application/json",
    "Referer": "https://suameca.banrep.gov.co/graficador-series/",
}


@contextmanager
def banrep_ca_bundle():
    """Raices certifi + intermedio GeoTrust en un archivo temporal."""
    roots = Path(requests.certs.where()).read_bytes()
    intermediate = INTERMEDIATE_CERT.read_bytes()
    with tempfile.TemporaryDirectory() as directory:
        bundle = Path(directory) / "banrep-ca-bundle.pem"
        bundle.write_bytes(roots.rstrip() + b"\n" + intermediate)
        yield str(bundle)


def _to_date(ts_ms: float) -> _dt.date:
    # BanRep marca medianoche de Colombia (05:00 UTC): la fecha UTC coincide.
    return (_dt.datetime(1970, 1, 1, tzinfo=_dt.timezone.utc)
            + _dt.timedelta(milliseconds=ts_ms)).date()


def _fold(text: str) -> str:
    """Minusculas sin tildes, para comparar nombres de series."""
    norm = unicodedata.normalize("NFKD", str(text))
    return "".join(ch for ch in norm if not unicodedata.combining(ch)).lower()


def parse_payload(payload, serie_id: int, expected_name: str | None,
                  column: str, today: _dt.date | None = None,
                  drop_future: bool = True) -> pd.DataFrame:
    """Convierte la respuesta JSON en DataFrame [fecha, column]. Valida identidad."""
    if not payload or len(payload) != 1:
        raise ValueError(f"BanRep serie {serie_id}: respuesta vacia o multiple")
    item = payload[0]
    if str(item.get("id")) != str(serie_id):
        raise ValueError(f"BanRep devolvio la serie {item.get('id')} en lugar de {serie_id}")
    if expected_name and _fold(expected_name) not in _fold(item.get("nombre", "")):
        raise ValueError(f"BanRep serie {serie_id} ya no es '{expected_name}': {item.get('nombre')}")
    today = today or _dt.datetime.now().date()
    rows = [(_to_date(ts), float(v)) for ts, v in item["data"]
            if v is not None and (not drop_future or _to_date(ts) <= today)]
    df = pd.DataFrame(rows, columns=["fecha", column])
    df["fecha"] = pd.to_datetime(df["fecha"])
    return (df.drop_duplicates("fecha", keep="last")
              .sort_values("fecha").reset_index(drop=True))


def fetch_series(serie_id: int, column: str, expected_name: str | None = None,
                 verify: str | None = None, session=None, timeout: int = 40,
                 drop_future: bool = True) -> pd.DataFrame:
    """Descarga una serie completa. Si `verify` es None abre su propio bundle."""
    http = session or requests
    if verify is None:
        with banrep_ca_bundle() as bundle:
            return fetch_series(serie_id, column, expected_name, bundle, session, timeout,
                                drop_future)
    response = http.get(API, params={"idSerie": serie_id}, headers=HEADERS,
                        timeout=timeout, verify=verify)
    response.raise_for_status()
    return parse_payload(response.json(), serie_id, expected_name, column,
                         drop_future=drop_future)


def write_if_changed(df: pd.DataFrame, path: Path, float_format: str | None = None) -> bool:
    """Escribe CSV con LF solo si el contenido cambia. Devuelve True si escribio."""
    text = df.to_csv(index=False, lineterminator="\n", float_format=float_format)
    path = Path(path)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    with path.open("w", encoding="utf-8", newline="") as target:
        target.write(text)
    return True
