# ColombiaMacro — Nota metodológica

*Versión 9.0 · septiembre de 2026 · documento de trabajo para revisión académica e institucional*

## 1. Propósito y pregunta de investigación

El tablero responde una sola pregunta, en cinco partes: **¿en qué fase del ciclo está la economía
colombiana y qué implica para precios, política monetaria y activos?**

| Sección | Pregunta | Indicador principal |
| --- | --- | --- |
| 1. Actividad | ¿Crece la economía por encima de su potencial? | Brecha del producto (HP en tiempo real) |
| 2. Precios | ¿Converge la inflación a la meta? | IPC total, básica y expectativas implícitas en TES |
| 3. Política y curva | ¿Cuál es la postura de BanRep? | Tasa real ex ante frente a la neutral |
| 4. Mercados y sector externo | ¿Cómo lo reflejan los activos? | COLCAP (COP/USD), TRM, ITCR, cuenta corriente, deuda |
| 5. Señales | ¿Qué tan extremo es cada dato? | Percentil histórico desde 2010 |

Principios de diseño:

1. **Solo datos oficiales** (DANE, BanRep, BVC/MSCI vía BanRep, MinHacienda vía BanRep), descargados sin
   intervención manual y con identidad verificada (número de serie **y** nombre).
2. **Cada gráfico tiene un solo eje y una sola unidad.** Se eliminaron los ejes dobles del tablero anterior.
3. **Cada frase del veredicto se deriva de una regla explícita** (sección 7) y cita el dato que la sustenta.
4. **La incertidumbre se muestra, no se oculta**: la brecha del producto se presenta con el rango entre métodos.
5. **Sin información futura**: los cálculos en tiempo real solo usan datos disponibles a cada fecha.

## 2. Fuentes

| Tabla | Variable | Fuente | Serie / archivo | Frecuencia |
| --- | --- | --- | --- | --- |
| `pib_colombia.csv` | PIB real original y desestacionalizado, PIB nominal | DANE, anexos PIB por producción | Cuadros 1 y 4, ref. 2015 | Trimestral |
| `inflacion_clean.csv` | IPC, variación mensual y anual | DANE + BanRep | Serie 15000 | Mensual |
| `tasas_interes_clean.csv` | Curvas cero cupón TES pesos y UVR (1, 5, 10 años) | BanRep | 15272–15277 | Diaria |
| `colcap_oficial.csv` | Índice COLCAP | BanRep (BVC/MSCI) | 6 | Diaria |
| `series_banrep.csv` | Tasa de política | BanRep | 59 | Diaria |
| | IBR overnight efectiva | BanRep | 15324 | Diaria |
| | TRM | Superfinanciera vía BanRep | 1 | Diaria |
| | Inflación sin alimentos / sin alimentos ni regulados / núcleo 15 | BanRep | 15388 / 15390 / 15392 | Mensual |
| | Inflación de regulados / de alimentos | BanRep / DANE | 15398 / 15404 | Mensual |
| | Meta de inflación | BanRep | 853 | Anual |
| | ITCR-IPC ponderaciones totales (2010 = 100) | BanRep | 235 | Mensual |
| | Términos de intercambio | BanRep | 15360 | Mensual |
| | Reservas internacionales netas | BanRep | 15051 | Mensual |
| | Cuenta corriente (% PIB) | BanRep | 15290 | Trimestral |
| | IED en Colombia (USD mn) | BanRep | 15133 | Trimestral |
| | Deuda bruta del GNC (% PIB) | MinHacienda vía BanRep | 15328 | Anual |
| | Salario mínimo, variación anual | MinTrabajo vía BanRep | 15418 | Anual |
| `ise_mensual.csv` | Indicador de Seguimiento a la Economía | DANE | `anex-ISE-9actividades-*.xlsx`, cuadros 1 y 2 | Mensual |
| `mercado_laboral.csv` | TGP, TO, TD desestacionalizadas | DANE, GEIH | `anex-GEIH-Desestacionalizado-*.xlsx` | Mensual |

**Vintages.** Cada ejecución guarda la versión vigente de cada fuente. El DANE revisa la historia del PIB y
del ISE en cada publicación; el tablero no es una base de datos en tiempo real de lo que se conocía en cada
fecha pasada (limitación conocida, sección 9).

**Automatización.** GitHub Actions ejecuta `actualizar_todo.py` a diario (19:30 hora Colombia), valida con
`validar_datos.py`, corre las pruebas y solo publica si todo pasa. El servidor de BanRep omite un certificado
intermedio; `banrep_client.py` completa la cadena con el certificado GeoTrust versionado (sin desactivar la
verificación TLS).

## 3. Actividad: brecha del producto y reloj del ciclo

Sea $y_t = 100\,\ln(Y_t)$ con $Y_t$ el PIB real desestacionalizado (DANE, Cuadro 4). La brecha es
$g_t = y_t - \tau_t$, en porcentaje del producto potencial.

### 3.1 Estimación principal: filtro HP en tiempo real

$\tau$ minimiza $\sum_t (y_t-\tau_t)^2 + \lambda \sum_t (\Delta^2 \tau_t)^2$ con $\lambda = 1600$
(Hodrick y Prescott, 1997). El filtro de dos colas usa datos futuros y sufre sesgo de fin de muestra
(Orphanides y van Norden, 2002). Por eso la estimación principal es **en tiempo real**: para cada $t$ se
resuelve el problema con $y_1,\dots,y_t$ y se conserva $\tau_{t|t}$. Se exige un mínimo de 20 trimestres.
La implementación resuelve el sistema $(I+\lambda D'D)\tau=y$ y coincide con `statsmodels.hpfilter` hasta
$2\times10^{-10}$.

### 3.2 Contrastes

* **HP de dos colas** ($\tau_{t|T}$): mejor estimación ex post; se usa también para el crecimiento potencial
  $\;100\,(e^{(\tau_t-\tau_{t-4})/100}-1)$, porque la versión en tiempo real oscila con el rebote de 2021-22.
* **Hamilton (2018)**: residuo de $y_{t+8} = \beta_0 + \sum_{k=0}^{3}\beta_k y_{t-k} + v_{t+8}$ (MCO).

### 3.3 Tratamiento del COVID

Los trimestres 2020-T2 a 2021-T2 (confinamiento y paro nacional) se reemplazan por interpolación lineal
**solo para estimar la tendencia y los coeficientes de Hamilton**; la brecha se mide siempre contra el dato
observado. Sin este tratamiento la tendencia absorbe una caída de 17,6% en un trimestre y deforma la lectura
de 2019-2023.

### 3.4 Reloj del ciclo (OCDE)

Con $\Delta_2 g_t = g_t - g_{t-2}$:

| | $\Delta_2 g_t \ge 0$ | $\Delta_2 g_t < 0$ |
| --- | --- | --- |
| $g_t \ge 0$ | Expansión | Desaceleración |
| $g_t < 0$ | Recuperación | Contracción |

Se usa el cambio en dos trimestres para reducir el ruido de un solo dato.

### 3.5 Robustez (datos al T2 2026, 51 trimestres con los tres métodos, 2013-T4 a 2026-T2)

| Métrica | Valor |
| --- | --- |
| Coincidencia de signo, HP tiempo real vs. HP dos colas | 78% |
| Coincidencia de signo, HP tiempo real vs. Hamilton | 65% |
| Coincidencia de fase, HP tiempo real vs. Hamilton | 43% |
| Revisión media tiempo real − dos colas | −0,52 pp (MAE 0,96 pp; correlación 0,95) |
| Correlación entre métodos sin 2020-21 | 0,66–0,77 |

**Lectura:** el nivel de la brecha es robusto en signo en la mayoría de trimestres, pero la **fase** es
sensible al método. Por eso el tablero muestra la banda mínimo–máximo y la cantidad de métodos con brecha
positiva. Al T2 2026 los tres métodos dan brecha positiva (+0,3% a +2,3%).

**ISE.** Índice mensual del DANE (base 2015). La variación anual usa la serie original, comparable con el
PIB; el ritmo de corto plazo es $100\,[(\bar{x}_{t,3}/\bar{x}_{t-3,3})^4-1]$ sobre la serie desestacionalizada
(promedios móviles de tres meses), anualizado.

## 4. Precios y expectativas

* Inflación anual: $100\,(IPC_t/IPC_{t-12}-1)$; el último mes se reemplaza por la cifra publicada por el DANE
  (el índice BanRep tiene dos decimales y puede diferir 0,01 pp).
* Rango meta: 3% ± 1 pp (BanRep desde 2010; serie 853 para la historia).
* Inflación básica principal: sin alimentos ni regulados (serie 15390).
* **Inflación implícita (breakeven)** por plazo $h$:
  $\pi^{BE}_h = 100\left[\dfrac{1+i^{COP}_h}{1+r^{UVR}_h}-1\right]$ con las curvas cero cupón TES (Fisher exacto).
* **Forward 5y5y**: $\pi^{5y5y} = 100\left[\left(\dfrac{(1+i_{10})^{10}/(1+i_5)^5}{(1+r_{10})^{10}/(1+r_5)^5}\right)^{1/5}-1\right]$.
  Se considera que las expectativas están **desancladas** si el 5y5y supera el techo del rango (4%).

La inflación implícita incluye primas por riesgo inflacionario y por liquidez (los TES UVR son menos
líquidos) y el rezago de indexación de la UVR; no es una expectativa pura (Gürkaynak, Sack y Wright, 2010).

**Validación empírica** (implícita a 1 año, promedio mensual, frente a la inflación realizada 12 meses después,
236 meses entre 2006 y 2025):

| Período | Sesgo (realizada − implícita) | RMSE implícita | RMSE caminata aleatoria |
| --- | --- | --- | --- |
| 2006-2019 | +0,48 pp | 1,70 pp | 2,08 pp |
| 2020-2025 | +2,32 pp | 4,13 pp | 4,07 pp |
| Total | +1,01 pp | 2,64 pp | 2,80 pp |

Antes de 2020 la implícita pronostica mejor que la caminata aleatoria; el choque 2021-23 no fue anticipado
por ningún método. La implícita se presenta como **lo que el mercado descuenta**, no como pronóstico.

## 5. Postura monetaria y curva

* Tasa real ex ante: $r^{ea}_t = 100\left[\dfrac{1+TPM_t}{1+\pi^{BE}_{1,t}}-1\right]$.
* Tasa real ex post: se deflacta con la última inflación **publicada** a cada fecha (el IPC del mes $m$ se
  considera disponible el día 10 del mes $m+1$), sin usar información futura.
* **Tasa neutral de referencia: 2,7%–3,0% real**, estimación del equipo técnico de BanRep (2025, con ajuste al
  alza hacia 2026). Es un parámetro externo, configurable en `modelo_tablero.NEUTRAL_REAL`.
* Postura: *restrictiva* si $r^{ea} > 3{,}0 + 0{,}5$; *expansiva* si $r^{ea} < 2{,}7 - 0{,}5$; *neutral* en otro caso.
* Pendientes: TES 10A − TES 1A y TES 10A − TPM, en puntos porcentuales.

## 6. Mercados y sector externo

* COLCAP oficial (índice de precios, sin dividendos). Transición BVC → MSCI COLCAP el 28-may-2021 con
  continuidad de niveles; el gráfico la marca.
* COLCAP en dólares: puntos / TRM del mismo día (tolerancia máxima de 7 días).
* Retorno a 12 meses: último dato frente al último dato disponible 365 días antes.
* ITCR-IPC (2010 = 100): aumentos = depreciación real del peso.

## 7. Reglas del veredicto automático

| Concepto | Regla | Parámetro |
| --- | --- | --- |
| Posición frente al potencial | cerca si $\lvert g\rvert < 0{,}5$; encima si $g \ge 0{,}5$; debajo si $g \le -0{,}5$ | `UMBRAL_BRECHA` |
| Dirección de la inflación | acelera si el cambio en 3 meses de la anual > 0,1 pp; cede si < −0,1 pp | — |
| Fuera del rango meta | inflación anual > 4% o < 2% | — |
| Postura | ver sección 5 | `NEUTRAL_REAL`, `UMBRAL_POSTURA` |
| Expectativas | desancladas si 5y5y > 4% | `ANCLA_EXPECTATIVAS` |

## 8. Control de calidad de datos

* Identidad de cada serie por id y nombre; rangos plausibles por serie; historia mínima.
* Fechas: sin duplicados, sin futuros, sin meses o trimestres faltantes.
* Fórmulas recalculadas en cada corrida (PIB, IPC, ISE, identidad $TD = 1 - TO/TGP$ de la GEIH).
* **Saltos aislados** (valor que se aleja > 2 pp de ambos vecinos que difieren < 1 pp): se conservan en el CSV,
  se listan en `alertas_datos.csv` y se excluyen de los cálculos. Para las series derivadas (implícitas, tasa
  real) se aplica el mismo criterio con 1 pp / 0,5 pp: 91 observaciones en total entre las cinco series derivadas (de unos 5.800 días cada una).
* Verificación de la inflación: la inflación mensual compuesta a 12 meses reproduce la anual con error
  máximo de 0,04 pp (redondeo de la fuente).

## 9. Limitaciones conocidas

1. **Vintage única**: las cifras históricas corresponden a la última publicación, no a lo que se sabía en cada
   fecha. La brecha "en tiempo real" elimina la información futura del filtro, pero no las revisiones del DANE.
2. La fase del ciclo depende del método (sección 3.5); debe leerse junto con la banda.
3. La tasa neutral es una estimación externa con incertidumbre considerable.
4. Las implícitas contienen primas variables en el tiempo.
5. COLCAP es un índice de precios; no mide retorno total.
6. Las canastas "equiponderada" y "7 Magníficas" del tablero anterior son reconstrucciones sin ajuste por
   dividendos ni eventos corporativos y con composición posterior a 2021 aproximada. Se conservan en el
   laboratorio para revisión y **no alimentan ninguna cifra**.

## 10. Reproducibilidad

```bash
python -m pip install -r requirements-update.txt
python actualizar_todo.py        # descarga todas las fuentes
python validar_datos.py          # controles y estado de fuentes
python -m unittest discover -s tests
python dashboard_colombia.py     # http://127.0.0.1:8050
```

Módulos: `banrep_client.py` (descarga), `actualizar_*.py` (fuentes), `analitica_macro.py` (fórmulas),
`modelo_tablero.py` (indicadores y veredicto), `dashboard_colombia.py` (presentación).

## Referencias

* Banco de la República (2025). *Informe de Política Monetaria* (enero, abril y octubre de 2025) y estimaciones de la tasa de interés neutral del equipo técnico.
* Gürkaynak, R., Sack, B. y Wright, J. (2010). The TIPS Yield Curve and Inflation Compensation. *American Economic Journal: Macroeconomics*, 2(1), 70-92.
* Hamilton, J. D. (2018). Why You Should Never Use the Hodrick-Prescott Filter. *Review of Economics and Statistics*, 100(5), 831-843.
* Hodrick, R. y Prescott, E. (1997). Postwar U.S. Business Cycles: An Empirical Investigation. *Journal of Money, Credit and Banking*, 29(1), 1-16.
* MSCI (2021). *MSCI COLCAP Index Methodology*.
* OECD. *Business Cycle Clock* — metodología del sistema de indicadores adelantados compuestos.
* Orphanides, A. y van Norden, S. (2002). The Unreliability of Output-Gap Estimates in Real Time. *Review of Economics and Statistics*, 84(4), 569-583.
