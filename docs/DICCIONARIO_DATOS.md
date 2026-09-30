# Diccionario de datos

Esta es la especificacion de las tablas que alimentan el dashboard. La fecha
de una observacion es el periodo medido, no necesariamente el dia en que el
dato se conocio. Cada archivo mantiene su frecuencia propia.

| Tabla | Grano | Fuente | Uso |
| --- | --- | --- | --- |
| `pib_colombia.csv` | Un trimestre, fechado al primer dia | [DANE, anexos PIB produccion](https://www.dane.gov.co/index.php/estadisticas-por-tema/cuentas-nacionales/cuentas-nacionales-trimestrales/pib-informacion-tecnica) | Actividad real y nominal |
| `inflacion_clean.csv` | Un mes, fechado al primer dia | [DANE, IPC](https://www.dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/indice-de-precios-al-consumidor-ipc/ipc-informacion-tecnica) y BanRep, serie 15000 | Inflacion |
| `tasas_interes_clean.csv` | Dia de observacion | BanRep, series 15272 a 15277 | Curva cero cupon TES |
| `colcap_oficial.csv` | Dia de mercado | [BanRep/BVC, indice COLCAP](https://suameca.banrep.gov.co/estadisticas-economicas/informacionSerie/2500/indice_mercado_accionario_colcap), serie 6 | Mercado accionario oficial |
| `pib_sectores.csv` | Sector × trimestre (largo) | DANE, anexo PIB producción a precios constantes (Cuadro 1) | Crecimiento, peso y aporte de las 12 agrupaciones |
| `informalidad.csv` | Trimestre móvil, fechado al último mes | [DANE, empleo informal y seguridad social](https://www.dane.gov.co/index.php/estadisticas-por-tema/mercado-laboral/empleo-informal-y-seguridad-social) | Proporción de informales: nacional, 13 y 23 ciudades |
| `informalidad_ciudades.csv` | Ciudad × trimestre móvil (largo) | DANE, mismo anexo (hoja Prop informalidad) | Tasa de informalidad de las 23 ciudades; `grupo` = 13 (principales) o 23 |
| `informalidad_ramas.csv` | Rama × trimestre móvil (largo) | DANE, mismo anexo (hoja Ramas de actividad) | Ocupados, informales y tasa por sector |
| `colcap_canasta.csv` | Una accion de la canasta vigente | [iShares MSCI COLCAP (BlackRock)](https://www.blackrock.com/co/productos/251708/ishares-colcap-fund), composicion diaria | Pesos del COLCAP y 7 Magnificas |
| `acciones_semanal.csv` | Accion × semana (largo), fechada al viernes | Yahoo Finance, simbolos `<TICKER>.CL` | Equiponderado y 7 Magnificas |
| `series_banrep.csv` | Serie × fecha (largo) | BanRep, ids en `colombiamacro/fuentes/complementarias.py` | Politica, TRM, inflacion basica, externo, fiscal |
| `ise_mensual.csv` | Un mes | DANE, anexo ISE 9 actividades | Actividad mensual |
| `mercado_laboral.csv` | Un mes | DANE, anexo GEIH desestacionalizado | Mercado laboral |
| `estado_fuentes.csv` | Una fila por fuente | `colombiamacro/validar.py` | Fecha y estado de las fuentes |
| `alertas_datos.csv` | Una alerta por observacion | `colombiamacro/validar.py` | Valores TES aislados bajo revision |

## PIB trimestral

El actualizador lee el ultimo anexo de produccion a precios constantes y el
ultimo a precios corrientes. Usa la fila **Producto Interno Bruto** del
`Cuadro 1` (serie original) y `Cuadro 4` (serie ajustada por estacionalidad).
El DANE puede revisar toda la historia: cada ejecucion guarda una sola
**vintage** de los anexos vigentes.

| Columna | Unidad | Definicion |
| --- | --- | --- |
| `fecha`, `trimestre` | Fecha / Tn AAAA | Periodo de referencia |
| `pib_real_miles_millones_ref2015` | Miles de millones, volumen encadenado ref. 2015 | PIB original, excluye efecto de precios |
| `pib_real_ajustado_miles_millones_ref2015` | Misma unidad | PIB ajustado por estacionalidad y calendario |
| `pib_real_yoy` | % | `100 * (real_original_t / real_original_t-4 - 1)` |
| `pib_real_qoq_sa` | % | `100 * (real_ajustado_t / real_ajustado_t-1 - 1)` |
| `pib_nominal_billones_cop` | Billones COP corrientes | Valor corriente / 1000 |
| `pib_nominal_yoy` | % | `100 * (nominal_t / nominal_t-4 - 1)` |
| `fecha_publicacion_vintage` | Fecha | Fecha del anexo vigente; **no** fecha historica de primera publicacion de cada trimestre |
| `fuente`, `estado_dato` | Texto | URL del anexo real y condicion de revision |

El grafico y la tarjeta muestran solo `pib_real_yoy`. El archivo anterior
`pib_crecimiento_yoy` era crecimiento nominal y ya no se consume. El valor
2026-T2 calculado de la serie real es 3.5234%, coherente con el 3.5% publicado
por el DANE al redondear a un decimal.

## IPC mensual

| Columna | Unidad | Definicion |
| --- | --- | --- |
| `inflacion_mensual` | % | Variacion mensual reportada en la tabla historica DANE cuando esta disponible; en meses anteriores, `100 * (IPC_t / IPC_t-1 - 1)` con indice BanRep |
| `inflacion_anual` | % | `100 * (IPC_t / IPC_t-12 - 1)` con indice BanRep; el ultimo mes se reemplaza con la cifra reportada DANE |
| `fuente_mensual`, `fuente_anual` | Texto | Indican cual de los dos metodos produjo cada valor |
| `fecha_publicacion_vintage` | Fecha / `no_disponible` | Fecha verificable del ultimo mes; no se inventan fechas de publicacion historicas |

El indice BanRep tiene dos decimales; calcular variaciones con el indice
redondeado puede diferir 0.01 puntos de las tasas publicadas por el DANE.
Por ejemplo, agosto de 2026 da 6.25% calculado y 6.24% reportado.

## TES diario

`tes_pesos_1y`, `tes_pesos_5y`, `tes_pesos_10y` son porcentajes anuales
de la curva cero cupon TES en pesos para 1, 5 y 10 anos. Las columnas
`tes_uvr_*` son tasas de la curva TES UVR y no se dibujan. El spread de la
tarjeta se calcula como `tes_pesos_10y - tes_pesos_1y`, en puntos porcentuales.
No representa la tasa de un bono individual ni una prediccion automatica.
La tabla original conserva valores publicados. `alertas_datos.csv` registra
un punto si cambia mas de 2 pp respecto de ambos vecinos y los vecinos
difieren menos de 1 pp. Solo el trazo omite esos puntos; su significado
economico y la fuente deben investigarse antes de corregir la tabla.

## COLCAP diario

`colcap_puntos` es el nivel publicado por BanRep (fuente original BVC).
`colcap_base100 = 100 * colcap_puntos / colcap_puntos(2009-02-09)`.
La tarjeta muestra puntos, la linea muestra la serie normalizada. El indice
paso de la metodologia BVC a la de MSCI COLCAP el 2021-05-28. MSCI tomo como
inicio el ultimo nivel BVC del 2021-05-27 y conservo la historia previa: la
continuidad numerica no implica una canasta o ponderaciones constantes. El
grafico senala esta fecha cuando esta dentro del periodo visible. Se refresca
la historia completa para captar correcciones de la fuente.
La transicion y la continuidad de niveles estan documentadas en la
[metodologia MSCI COLCAP de mayo de 2021](https://www.msci.com/eqb/methodology/meth_docs/MSCI_COLCAP_Index_Methodology_May2021.pdf).

## PIB por sectores

`pib_sectores.csv`: `fecha` (primer día del trimestre), `codigo` (secciones CIIU, p. ej. `G + H + I`),
`sector` (nombre corto), `nivel` (miles de millones de pesos de 2015, datos originales), `yoy` (%),
`peso` (% del valor agregado del mismo trimestre), `contribucion` (pp: cambio anual del nivel del
sector / valor agregado de hace un año). Los volúmenes encadenados no son aditivos: pesos y aportes
suman aproximadamente, no exactamente, 100 % y el crecimiento total.

## Informalidad

`informalidad.csv`: `fecha` (último mes del trimestre móvil), `periodo`, `nacional`, `ciudades_13`,
`ciudades_23` (% de ocupados informales). `informalidad_ramas.csv`: `fecha`, `rama`, `ocupados` e
`informales` (miles de personas, total nacional) y `tasa` (%). Serie desde 2021 (definición vigente
del DANE); no se empalma con la serie anterior.

## Acciones del COLCAP

`colcap_canasta.csv`

| Columna | Descripcion |
| --- | --- |
| `ticker` | Nemotecnico BVC |
| `nombre` | Nombre en la canasta del fondo |
| `emisor` | Empresa sin la clase de accion (agrupa ordinaria y preferencial) |
| `sector` | Sector segun iShares |
| `peso` | Peso en el fondo, % (efectivo excluido) |
| `precio` | Precio de valoracion del fondo, COP |
| `fecha_canasta` | Fecha de la composicion |

`acciones_semanal.csv`

| Columna | Descripcion |
| --- | --- |
| `fecha` | Viernes de la semana (la semana en curso se fecha con el dia de descarga) |
| `ticker` | Nemotecnico BVC |
| `simbolo` | Simbolo(s) de Yahoo usados; `+` indica empalme con un ticker anterior |
| `cierre` | Cierre semanal en COP, sin ajuste por dividendos |

Las canastas heredadas (ICOLCAP, sintetico, "grandes") se retiraron en la v10; la seccion
"¿Qué empresas mueven la bolsa?" las reemplaza con fuentes que se actualizan solas.

## Interpretacion temporal

- El grafico macro conserva puntos mensuales y barras trimestrales en filas
  separadas. No convierte PIB o IPC a datos diarios.
- El grafico TES usa solo fechas publicadas por BanRep. La linea bursatil
  oficial usa fechas publicadas de COLCAP; las dos lineas punteadas son
  reconstrucciones historicas separadas. Una fuente rezagada no recorta otra.
- Las tarjetas muestran la ultima observacion del periodo seleccionado y
  su propia fecha. Las cifras historicas usan la vintage actual; no son una
  base de datos de lo que se sabia exactamente en cada fecha pasada.


## Series complementarias (v9)

`series_banrep.csv` guarda cada serie en formato largo. `fecha` se normaliza al
primer dia del mes (mensuales), del trimestre (trimestrales) o del ano (anuales);
las diarias conservan el dia. `id_banrep` permite auditar contra el graficador de
BanRep (`consultaSerieParaGraficar?idSerie=<id>`).

| serie | id | unidad |
| --- | --- | --- |
| `tpm` | 59 | % e.a. |
| `ibr_overnight` | 15324 | % e.a. |
| `trm` | 1 | COP por USD |
| `inflacion_sin_alimentos` / `inflacion_basica_sar` / `inflacion_nucleo15` | 15388 / 15390 / 15392 | % anual |
| `inflacion_regulados` / `inflacion_alimentos` | 15398 / 15404 | % anual |
| `meta_inflacion` | 853 | % |
| `itcr_ipc` | 235 | indice 2010=100 |
| `terminos_intercambio` | 15360 | indice |
| `reservas_netas_musd` | 15051 | millones USD |
| `cuenta_corriente_pct_pib` | 15290 | % PIB |
| `ied_musd` | 15133 | millones USD |
| `deuda_bruta_gnc_pct_pib` | 15328 | % PIB |
| `salario_minimo_var` | 15418 | % anual |

`ise_mensual.csv`: `ise_original`, `ise_sa` e indices desestacionalizados de
actividades primarias, secundarias y terciarias (2015 = 100); `ise_yoy =
100*(ise_original_t/ise_original_t-12 - 1)`; `ise_sa_mom`; `ise_sa_3m3m_saar`
(promedio movil de 3 meses frente a los 3 previos, anualizado).

`mercado_laboral.csv`: `tgp_sa`, `to_sa`, `td_sa` (%, total nacional
desestacionalizado) y `td_sa_3m`. El validador comprueba `TD = 100*(1 - TO/TGP)`.

## Indicadores derivados (no se guardan; se calculan al cargar)

Definidos en `colombiamacro/analitica.py` y documentados en `METODOLOGIA.md`: inflacion
implicita por plazo y forward 5y5y, tasa real ex ante y ex post, pendientes,
brecha del producto (tres metodos), crecimiento potencial, fase del ciclo,
COLCAP en dolares, drawdown y percentiles historicos.
