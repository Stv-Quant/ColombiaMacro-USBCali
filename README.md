# ColombiaMacro · ¿Cómo va la economía colombiana?

Tablero abierto (español / inglés) sobre el ciclo económico colombiano, construido con
datos oficiales del **DANE** y el **Banco de la República** (y, para las acciones, la canasta
del fondo iShares COLCAP y precios de Yahoo Finance). Se actualiza solo todos los días
y se publica como sitio web estático en GitHub Pages.

Proyecto académico · Universidad de San Buenaventura Cali.

## Qué muestra

| # | Pregunta | Gráficos principales |
|---|----------|----------------------|
| ◷ | ¿En qué parte del ciclo está la economía? | **Reloj del ciclo interactivo** (fase, nivel y dirección; recorrido por trimestre desde 2014) |
| 1 | ¿Está creciendo la economía? | PIB trimestral e ISE mensual, desempleo |
| 2 | ¿Qué pasa con los precios? | Inflación vs. meta 2–4 %, inflación esperada |
| 3 | ¿Qué hace el Banco de la República? | Tasa de política vs. inflación |
| 4 | ¿Cuánto cobra el mercado por prestarle al Gobierno? | **Curva cero cupón TES** interactiva (cualquier día desde 2003, comparación por años) |
| 5 | ¿Cómo están el dólar y la bolsa? | TRM, COLCAP |
| 6 | ¿Qué empresas mueven la bolsa? | COLCAP vs. equiponderado vs. **7 Magníficas** (base 100), pesos de la canasta, tabla de las 7 |
| 7 | ¿Cómo están las cuentas externas y fiscales? | Cuenta corriente, deuda del Gobierno |
| 8 | Todos los indicadores | Último dato, cambio y nivel frente a su historia |
| 9 | Fuentes | Estado de cada fuente, descargas CSV, metodología |

Cada gráfico muestra arriba el **último dato y su cambio** (frente a hace un año, al trimestre
o al mes anterior), abajo un **panel de barras con ese cambio a lo largo del tiempo**, y el
recuadro flotante indica el cambio de cada punto. Las escalas se ajustan al periodo visible
(2020 incluido). Los métodos técnicos
(brecha del producto HP/Hamilton, reloj del ciclo, tasa real, 5y5y) están en los paneles
"Detalle técnico", siempre explicados.

## Estructura

```
colombiamacro/            paquete de Python
  config.py               rutas (data/, site/, docs/)
  actualizar.py           descarga todas las fuentes (python -m colombiamacro.actualizar)
  validar.py              controles de calidad y estado de fuentes
  analitica.py            fórmulas: Fisher, breakevens, 5y5y, HP en tiempo real, Hamilton, reloj
  modelo.py               instantánea, estados en lenguaje simple, tabla de indicadores
  fuentes/                un módulo por fuente (banrep, pib, ipc, tes, colcap, complementarias)
  sitio/                  generador del sitio estático (construir.py, textos.py, app.js, estilo.css)
data/                     CSV oficiales versionados + registro_actualizacion.log
docs/                     metodología, diccionario de datos, operación, manual, guía y presentación
scripts/                  lanzar_local.py (abrir en su computador), generar_figuras.py (figuras PDF)
tests/                    pruebas (fórmulas, datos, sitio)
certs/                    certificado intermedio GeoTrust que el servidor de BanRep no envía
.github/workflows/        actualización diaria + publicación en GitHub Pages
```

## Verlo en su computador

Windows: doble clic en **`Iniciar ColombiaMacro.bat`**. macOS/Linux: `./iniciar_colombiamacro.sh`.

```bash
python scripts/lanzar_local.py                 # busca un puerto libre desde 8050 (omite 8765 y 8766)
python scripts/lanzar_local.py --actualizar    # descarga los datos oficiales antes de abrir
python scripts/lanzar_local.py --evitar 8765 8766 3000
```

La primera vez crea `.venv` e instala dependencias (1–3 min). Requiere Python 3.10+.

## Automatización

`.github/workflows/actualizar-y-publicar.yml` corre todos los días a las 19:30 (Colombia):

1. Pruebas → descarga DANE/BanRep (`python -m colombiamacro.actualizar`).
2. Si una fuente falla, se conserva su último dato válido y se emite un aviso; **no detiene la publicación**.
3. Validación → pruebas con los datos del día → commit de `data/` → construcción del sitio → GitHub Pages.

El detalle de cada descarga queda en `data/registro_actualizacion.log`.

## Despliegue

**Recomendado: GitHub Pages** (gratis, siempre encendido, sin tiempos de arranque, se publica solo).

1. *Settings → Pages → Build and deployment → Source:* **GitHub Actions**.
2. *Settings → Actions → General → Workflow permissions:* **Read and write**.
3. *Actions → Actualizar datos y publicar sitio → Run workflow*.
4. Dirección: `https://stv-quant.github.io/ColombiaMacro-USBCali/`.

Alternativas (el sitio es una carpeta de archivos estáticos, `site/`):

| Opción | Costo | Cuándo usarla |
|--------|-------|---------------|
| Cloudflare Pages | Gratis | CDN global y dominio propio (p. ej. `macro.usbcali.edu.co`) |
| Netlify | Gratis | Vista previa por cada cambio |
| Render *Static Site* | Gratis | Si ya usa Render (a diferencia del servicio web, no se duerme) |
| Servidor de la universidad | — | Copiar `site/` a cualquier servidor web (Apache, Nginx, IIS) |

Para las alternativas: comando de construcción `pip install -r requirements.txt && python -m colombiamacro.sitio.construir`,
carpeta de salida `site`.

## Comandos útiles

```bash
pip install -r requirements.txt
python -m colombiamacro.actualizar          # descargar fuentes
python -m colombiamacro.validar             # controles de calidad
python -m colombiamacro.sitio.construir     # generar site/
python -m unittest discover -s tests        # pruebas
pip install -r requirements-docs.txt && python scripts/generar_figuras.py   # figuras del manual
```

Documentación: [Metodología](docs/METODOLOGIA.md) · [Diccionario de datos](docs/DICCIONARIO_DATOS.md) ·
[Operación](docs/OPERACION.md) · [Manual (PDF)](docs/Manual_ColombiaMacro.pdf) ·
[Guía de presentación (PDF)](docs/Guia_Presentacion_Academica.pdf)

> Tablero académico. No constituye recomendación de inversión.
