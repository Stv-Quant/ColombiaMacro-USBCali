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
| 1 | ¿Está creciendo la economía? | PIB trimestral e ISE mensual, desempleo, **producción frente a su capacidad** (frontera de producción) y **tamaño de la economía en pesos y dólares** |
| 2 | ¿Qué sectores impulsan la economía? | Crecimiento de los 12 sectores del PIB (cualquier trimestre desde 2010 vs. un año antes) y mapa de calor |
| 3 | ¿Cuánto del empleo es informal? | Informalidad nacional y 13 ciudades, por sector y por cada una de las 23 ciudades (selector de ciudad) |
| 4 | ¿Qué pasa con los precios? | Inflación vs. meta 2–4 %, inflación esperada y **trayectoria que descuenta el mercado para los próximos 10 años** (1 año, años 1–5 y 5y5y) |
| 5 | ¿Qué hace el Banco de la República? | Tasa de política vs. inflación |
| 6 | ¿Cuánto cobra el mercado por prestarle al Gobierno? | **Curva cero cupón TES** interactiva (cualquier día desde 2003, comparación por años) |
| 7 | ¿Cómo están el dólar y la bolsa? | TRM, COLCAP |
| 8 | ¿Qué empresas mueven la bolsa? | COLCAP vs. equiponderado vs. **7 Magníficas** (base 100), pesos de la canasta, tabla de las 7 |
| 9 | ¿Cómo están las cuentas externas y fiscales? | Cuenta corriente, deuda del Gobierno |
| 10 | Todos los indicadores | Último dato, cambio y nivel frente a su historia |
| — | Nota: últimas publicaciones oficiales | Último dato de DANE, BanRep y BVC en una línea, con enlace oficial (discreta, al final) |
| 11 | Fuentes | Estado de cada fuente, descargas CSV, metodología |

Cada gráfico lleva al pie su **fuente** y un **?** que muestra la metodología. Muestra arriba el **último dato y su cambio** (frente a hace un año, al trimestre
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

`.github/workflows/actualizar-y-publicar.yml` corre **cada hora en días hábiles** (7:07 a 18:07, hora de
Colombia) con las series diarias del Banco de la República (tasa de política, TRM, TES, COLCAP) y publica
solo si llegó un dato nuevo; a las 19:30 hace la actualización completa (DANE, acciones, informalidad):

1. Pruebas → descarga DANE/BanRep (`python -m colombiamacro.actualizar`).
2. Si una fuente falla, se conserva su último dato válido y se emite un aviso; **no detiene la publicación**.
3. Validación → pruebas con los datos del día → commit de `data/` → construcción del sitio → GitHub Pages.

El detalle de cada descarga queda en `data/registro_actualizacion.log`. Para forzar una actualización:
*Actions → Actualizar datos y publicar sitio → Run workflow*.

**Decisiones de la Junta del Banco de la República.** La nueva tasa entra a la serie oficial el día en que
empieza a regir (normalmente el día hábil siguiente al anuncio). Para mostrarla desde el mismo día del
anuncio se agrega una fila a `data/decisiones_banrep.csv` (`fecha_anuncio,vigente_desde,tasa,nota,enlace`);
el tablero la marca como "Anunciada" y deja de usarla sola cuando la serie oficial la registra.

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
