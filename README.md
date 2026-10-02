# ColombiaMacro · ¿Cómo va la economía colombiana?

Tablero abierto (español / inglés) sobre el ciclo económico colombiano, construido con
datos oficiales del **DANE** y el **Banco de la República** (y, para las acciones, la canasta
del fondo iShares COLCAP y precios de Yahoo Finance). Se actualiza solo todos los días
y se publica como sitio web estático en GitHub Pages.

Proyecto académico · Universidad de San Buenaventura Cali.

## Qué muestra

**Portada: lectura en un vistazo, sin gráficos.** La respuesta en tres frases y la fase del ciclo;
seis cifras clave con su tendencia; ocho temas en una frase con sus dos cifras (cada uno abre su
página de análisis); los 16 indicadores con su nivel histórico; el estado de las fuentes con las
**descargas CSV**; y las últimas publicaciones oficiales.

Páginas de análisis (menú agrupado):

| Grupo | Página | Contenido |
|-------|--------|-----------|
| Actividad | `/ciclo/` | Reloj del ciclo interactivo y recorrido trimestral desde 2014 |
| | `/crecimiento/` | PIB trimestral, ISE mensual y crecimiento real por año |
| | `/sectores/` | Los 12 sectores del PIB en cualquier trimestre desde 2010 y mapa de calor |
| | `/capacidad/` | Producción frente a su capacidad (brecha del producto) |
| | `/empleo/` | Desempleo e informalidad nacional, por sector y por ciudad |
| Precios y tasas | `/inflacion/` | Inflación vs. meta, qué precios suben más, inflación esperada y trayectoria a 10 años |
| | `/tasas/` | Tasa del Banco de la República y tasa real |
| | `/curva-tes/` | Curva cero cupón TES interactiva desde 2003 |
| Mercados y cuentas | `/mercados/` | Dólar (TRM) y COLCAP |
| | `/empresas/` | COLCAP vs. equiponderado vs. 7 Magníficas, pesos de la canasta |
| | `/externo/` | Cuenta corriente y deuda del Gobierno |
| | `/comercio/` | Comercio exterior (DANE con registros de la DIAN): exportaciones e importaciones en 12 meses, balanza por año, qué vende (petróleo, carbón, café, no tradicionales), qué compra por uso (CUODE), destinos y orígenes |
| Datos | `/indicadores/` | Indicadores, publicaciones oficiales, fuentes, descargas y glosario |

Todas las páginas existen en español (`/`) e inglés (`/en/`). Cada gráfico lleva su **fuente**, un
**?** con la metodología y un botón **⤢** para ampliarlo.

Proyecto académico de la Universidad de San Buenaventura Cali, con el apoyo de **FinancialTools.io**
en el Laboratorio de Trading.

**Interfaz.** Tema claro "Andes" por defecto (papel, curvas de nivel, Source Serif 4 + Inter Tight) y
tema oscuro "Banco central" (azul tinta, latón, grabado tipo billete, Newsreader + IBM Plex) con el
botón ☀/☾. Paneles de vidrio esmerilado; fuentes servidas desde el propio sitio (sin Google Fonts).
Respeta `prefers-reduced-motion` y funciona desde 375 px de ancho.

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
