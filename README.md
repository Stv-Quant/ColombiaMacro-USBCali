# ColombiaMacro · Monitor del ciclo económico colombiano

**Universidad de San Buenaventura Cali** · Finanzas y Negocios Internacionales

Tablero abierto y reproducible que responde, con datos oficiales actualizados cada día,
**en qué fase del ciclo está Colombia y qué implica para precios, política monetaria y
activos**. Bilingüe (ES/EN), pensado para inversionistas locales y extranjeros y para
revisión académica.

| | |
| --- | --- |
| Metodología | [`METODOLOGIA.md`](METODOLOGIA.md) |
| Manual completo (PDF) | [`docs/Manual_ColombiaMacro.pdf`](docs/Manual_ColombiaMacro.pdf) |
| Guía de presentación académica (PDF) | [`docs/Guia_Presentacion_Academica.pdf`](docs/Guia_Presentacion_Academica.pdf) |
| Diapositivas (Beamer) | [`docs/presentacion/ColombiaMacro_Beamer.pdf`](docs/presentacion/ColombiaMacro_Beamer.pdf) |
| Diccionario de datos | [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md) |
| Operación diaria | [`OPERACION_DATOS.md`](OPERACION_DATOS.md) |

## Qué muestra

0. **Veredicto automático**: fase del ciclo y lectura con las cifras que la sustentan.
1. **Actividad**: brecha del producto (HP en tiempo real, HP dos colas, Hamilton), reloj del ciclo, PIB, ISE y desempleo.
2. **Precios**: inflación total y básica frente al rango meta; inflación implícita en TES (1 año y 5y5y).
3. **Política monetaria y curva**: tasa de política, tasa real ex ante frente a la neutral, curva TES y pendientes.
4. **Mercados y sector externo**: COLCAP en pesos y en dólares, TRM, tasa de cambio real, cuenta corriente y deuda del GNC.
5. **Señales**: percentil histórico de cada indicador, laboratorio de canastas heredadas y descarga de datos.

## Verlo en local (Windows)

1. Instalar [Python 3.10+](https://www.python.org/downloads/) marcando *Add python.exe to PATH*.
2. Doble clic en **`Iniciar ColombiaMacro.bat`**.

El lanzador crea un entorno `.venv`, instala dependencias solo cuando cambian, busca un
**puerto libre** (omite 8765 y 8766 y cualquier puerto ocupado) y abre el navegador.

```bash
python lanzar_local.py                    # puerto libre desde 8050
python lanzar_local.py --evitar 8765 8766 3000
python lanzar_local.py --actualizar       # descarga datos oficiales antes de abrir
python lanzar_local.py --legacy           # tablero anterior (v8)
./iniciar_colombiamacro.sh                # macOS / Linux
```

## Datos y automatización

GitHub Actions ejecuta `actualizar_todo.py` todos los días a las 19:30 (hora Colombia):
descarga DANE y BanRep, valida fórmulas y fechas (`validar_datos.py`), corre 43 pruebas y
publica los CSV solo si todo pasa. El servidor web solo lee CSV versionados.

| Módulo | Función |
| --- | --- |
| `banrep_client.py` | Descarga BanRep con cadena TLS completa y verificación de identidad de series |
| `actualizar_*.py` | PIB, IPC, TES, COLCAP, series complementarias BanRep, ISE y GEIH |
| `analitica_macro.py` | Fórmulas: Fisher, breakevens, 5y5y, HP en tiempo real, Hamilton, reloj del ciclo |
| `modelo_tablero.py` | Instantánea, veredicto y tabla de señales |
| `dashboard_colombia.py` | Presentación (Dash/Plotly) |
| `docs/generar_figuras.py` | Figuras vectoriales para documentos y diapositivas |

## Despliegue

* **Render** (`render.yaml`): conectar el repositorio como *Blueprint*. El plan `free` se
  suspende tras 15 minutos sin tráfico; para uso institucional usar `starter`.
* **Docker** (`Dockerfile`): Google Cloud Run, Fly.io, Railway o un servidor de la universidad.

```bash
docker build -t colombiamacro . && docker run -p 8080:8080 colombiamacro
```

## Pruebas

```bash
python -m pip install -r requirements-update.txt
python -m unittest discover -s tests
```

---
Tablero académico con datos oficiales (DANE, Banco de la República, BVC/MSCI, Ministerio de
Hacienda). No constituye recomendación de inversión.
