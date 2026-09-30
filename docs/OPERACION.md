# Operación

## Rutina diaria (automática)

GitHub Actions (`.github/workflows/actualizar-y-publicar.yml`) corre a las 00:30 UTC (19:30 Colombia):

1. `python -m unittest discover -s tests`
2. `python -m colombiamacro.actualizar` — cada fuente corre en su propio proceso; si una falla, las demás continúan.
3. Avisos (`::warning`) por cada fuente con falla, sin detener la publicación.
4. `python -m colombiamacro.validar` — escribe `data/estado_fuentes.csv` y `data/alertas_datos.csv`.
5. Pruebas con los datos del día; commit de `data/` por `github-actions[bot]`.
6. `python -m colombiamacro.sitio.construir` y despliegue a GitHub Pages.

Un `push` a `main` reconstruye y publica el sitio sin descargar datos.

## Qué hacer si una fuente falla

1. Abrir `data/registro_actualizacion.log` en el repositorio (no requiere iniciar sesión).
2. El resumen final indica `[OK]` o `[FALLO]` por fuente.
3. Las series de BanRep se validan una por una: una serie inválida se excluye y se conserva
   su versión anterior; las demás se escriben normalmente.
4. Si BanRep cambia su certificado, actualizar `certs/GeoTrustEVRSACAG2.pem`.
5. Si el DANE cambia la estructura de un anexo, ajustar el módulo en `colombiamacro/fuentes/`.
6. Acciones: si una acción cambia de ticker, agregar el anterior en `ALIAS` de
   `colombiamacro/fuentes/acciones.py`; si una empresa nueva no tiene nombre corto, agregarlo en
   `NOMBRES_CORTOS` de `colombiamacro/modelo.py`.

## Estados de las fuentes

| Estado | Regla |
|--------|-------|
| Al día | Último dato dentro del rezago normal de publicación |
| Retrasado | Supera el rezago: PIB 150 días, IPC 45, ISE 110, GEIH 100, diarias 7–10, canasta y acciones 10, informalidad 110, PIB por sectores 230 (desde el inicio del trimestre), deuda anual 800 |
| Pendiente | Aún no hay archivo (primera descarga pendiente) |

## En local

`Iniciar ColombiaMacro.bat` (Windows) o `python scripts/lanzar_local.py [--actualizar]`.
Busca un puerto libre desde 8050 y omite 8765 y 8766.

## Publicar cambios de código

Todo cambio se sube a `main`; el flujo reconstruye el sitio. No hay servidor que mantener.
