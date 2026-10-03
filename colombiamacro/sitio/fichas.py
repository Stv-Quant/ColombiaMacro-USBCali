"""Ficha de cada grafico: fuente de los datos y metodologia (ES, EN).

La fuente se muestra al pie del grafico; la metodologia aparece al pasar el cursor
(o tocar, en celular) sobre el signo de interrogacion.
"""

DANE_PIB = ("DANE, PIB trimestral (anexos de producción a precios constantes y corrientes)",
            "DANE, quarterly GDP (production annexes at constant and current prices)")
DANE_GEIH = ("DANE, Gran Encuesta Integrada de Hogares (GEIH)", "DANE, Integrated Household Survey (GEIH)")
DANE_INF = ("DANE, GEIH – empleo informal y seguridad social", "DANE, GEIH – informal employment and social security")
BR_TES = ("Banco de la República, curvas cero cupón de los TES (series 15272–15277)",
          "Banco de la República, TES zero-coupon curves (series 15272–15277)")

DANE_EXPO = ("DANE con registros de la DIAN: exportaciones (anexos estadísticos)", "DANE with DIAN records: exports (statistical annexes)")
DANE_IMPO = ("DANE con registros de la DIAN: importaciones (anexos estadísticos)", "DANE with DIAN records: imports (statistical annexes)")
DANE_EXPO_IMPO = ("DANE con registros de la DIAN: exportaciones e importaciones", "DANE with DIAN records: exports and imports")

FICHAS = {
    "g-crec": (("DANE: PIB trimestral e Indicador de Seguimiento a la Economía (ISE)",
                "DANE: quarterly GDP and Economic Tracking Indicator (ISE)"),
               ("Barras: variación del PIB real (datos originales) frente al mismo trimestre del año anterior. Línea naranja: "
                "ISE desestacionalizado, variación anual. Punteada: crecimiento de la tendencia (filtro de Hodrick-Prescott, "
                "λ = 1.600, sin el choque de 2020T2–2021T2). Panel inferior: cambio frente al trimestre anterior, en puntos.",
                "Bars: real GDP (original data) versus the same quarter a year earlier. Orange line: seasonally adjusted ISE, "
                "annual change. Dotted: trend growth (Hodrick-Prescott, λ = 1,600, excluding the 2020Q2–2021Q2 shock). "
                "Lower panel: change versus the previous quarter, in points.")),
    "g-desempleo": (DANE_GEIH,
                    ("Tasa de desempleo = desocupados / fuerza de trabajo, serie desestacionalizada del DANE; la línea azul "
                     "promedia 3 meses. Panel inferior: cambio frente a un año antes, en puntos.",
                     "Unemployment rate = unemployed / labour force, DANE seasonally adjusted series; the blue line is a "
                     "3-month average. Lower panel: change versus a year earlier, in points.")),
    "g-capacidad": (("DANE, PIB real desestacionalizado (Cuadro 4); cálculo propio de la capacidad",
                     "DANE, seasonally adjusted real GDP (Table 4); own estimate of capacity"),
                    ("Capacidad (PIB potencial) = tendencia del PIB estimada con un filtro de Hodrick-Prescott en tiempo real "
                     "(λ = 1.600, una cola: cada trimestre solo usa datos disponibles hasta ese momento), excluyendo el choque "
                     "de 2020T2–2021T2. Brecha = 100 × (ln PIB − ln capacidad). Como contraste se calculan también un HP de "
                     "dos colas y el método de Hamilton (2018); los tres coinciden en el signo casi siempre. Valores en billones "
                     "de COP (pesos colombianos) de 2015 por trimestre.",
                     "Capacity (potential GDP) = GDP trend from a real-time Hodrick-Prescott filter (λ = 1,600, one-sided: each "
                     "quarter only uses data available then), excluding the 2020Q2–2021Q2 shock. Gap = 100 × (ln GDP − ln "
                     "capacity). A two-sided HP and Hamilton's (2018) method are computed as checks; the three usually agree on "
                     "the sign. Values in COP (Colombian peso) trillions at 2015 prices per quarter.")),
    "g-pib-anual": (("DANE, PIB trimestral a precios constantes (datos originales, base 2015)",
                     "DANE, quarterly GDP at constant prices (original data, base 2015)"),
                    ("Crecimiento real anual = 100 × (PIB real del año / PIB real del año anterior − 1), sumando los cuatro "
                     "trimestres de cada año (volúmenes encadenados, sin efecto de la inflación). Barra clara: últimos 12 meses "
                     "frente a los 12 meses previos. Ritmo habitual: promedio anual del crecimiento de la tendencia (HP). "
                     "Referencia: promedio simple 2010–2019.",
                     "Annual real growth = 100 × (real GDP of the year / real GDP of the previous year − 1), summing the four "
                     "quarters of each year (chain-linked volumes, net of inflation). Light bar: last 12 months versus the "
                     "previous 12 months. Usual pace: annual average of trend (HP) growth. Reference: simple 2010–2019 average.")),
    "g-sec-barras": (DANE_PIB,
                     ("12 agrupaciones CIIU Rev. 4 (volúmenes encadenados, año base 2015, datos originales). Crecimiento anual "
                      "frente al mismo trimestre del año anterior; la raya vertical es el dato de un año antes. Aporte = cambio del "
                      "nivel del sector en un año / valor agregado total de hace un año.",
                      "12 ISIC Rev. 4 groupings (chain-linked volumes, base 2015, original data). Annual growth versus the "
                      "same quarter a year earlier; the vertical tick is the figure a year before. Contribution = one-year change "
                      "of the sector's level / total value added a year earlier.")),
    "g-sec-mapa": (DANE_PIB,
                   ("Crecimiento anual de cada sector por trimestre. La escala de color se recorta en ±12% para que 2020 no "
                    "oculte el resto; el recuadro flotante muestra el valor exacto.",
                    "Annual growth of each sector by quarter. The colour scale is clipped at ±12% so 2020 does not hide the "
                    "rest; the hover box shows the exact value.")),
    "g-informal": (DANE_INF,
                   ("Proporción de ocupados informales (definición DANE 2023, alineada con la OIT): sin seguridad social o en "
                    "unidades no registradas. Trimestres móviles desde 2021; no comparable con la serie anterior.",
                    "Share of informal workers (DANE 2023 definition, ILO-aligned): no social security or unregistered units. "
                    "Rolling quarters since 2021; not comparable with the earlier series.")),
    "g-inf-ramas": (DANE_INF, ("Informales / ocupados de cada rama, total nacional. La raya vertical es el dato de un año antes.",
                               "Informal / employed in each sector, national total. The vertical tick is the figure a year before.")),
    "g-inf-ciudades": (DANE_INF, ("Proporción de ocupados informales en cada una de las 23 ciudades y áreas metropolitanas "
                                  "(A.M.); en azul las 13 principales. La raya es el dato de un año antes.",
                                  "Share of informal workers in each of the 23 cities and metropolitan areas (A.M.); the 13 "
                                  "main ones in blue. The tick is the figure a year before.")),
    "g-inf": (("DANE, IPC; Banco de la República, inflación sin alimentos ni regulados",
               "DANE, CPI; Banco de la República, inflation excluding food and regulated prices"),
              ("Inflación anual = variación del IPC en 12 meses. Inflación de fondo = sin alimentos ni precios regulados "
               "(cálculo del Banco de la República). Franja verde: meta de 3% ± 1 punto.",
               "Annual inflation = 12-month CPI change. Underlying inflation = excluding food and regulated prices (Banco "
               "de la República). Green band: 3% ± 1 point target.")),
    "g-espera": (BR_TES,
                 ("Inflación esperada a 1 año (breakeven) = (1 + tasa TES en pesos) / (1 + tasa TES en UVR) − 1. Incluye "
                  "primas por riesgo y liquidez, por lo que es una cota de la expectativa pura.",
                  "1-year expected inflation (breakeven) = (1 + peso TES yield) / (1 + UVR TES yield) − 1. It includes risk "
                  "and liquidity premia, so it is an upper bound of pure expectations.")),
    "g-tray": (BR_TES,
               ("Tramos implícitos: año 1 = b1; años 1–5 = [(1+b5)^5/(1+b1)]^(1/4) − 1; años 5–10 = "
                "[(1+b10)^10/(1+b5)^5]^(1/5) − 1 (la «5y5y»). Encadenan exactamente el breakeven a 10 años.",
                "Implied segments: year 1 = b1; years 1–5 = [(1+b5)^5/(1+b1)]^(1/4) − 1; years 5–10 = "
                "[(1+b10)^10/(1+b5)^5]^(1/5) − 1 (the \"5y5y\"). They chain exactly to the 10-year breakeven.")),
    "g-anclaje": (BR_TES, ("Forward 5y5y = [(1+b10)^10/(1+b5)^5]^(1/5) − 1, promedio semanal. Mide la inflación que el "
                           "mercado espera entre 5 y 10 años adelante.",
                           "5y5y forward = [(1+b10)^10/(1+b5)^5]^(1/5) − 1, weekly average. Measures the inflation the "
                           "market expects between 5 and 10 years ahead.")),
    "g-politica": (("Banco de la República, tasa de política monetaria; DANE, IPC",
                    "Banco de la República, policy rate; DANE, CPI"),
                   ("Tasa de interés de intervención fijada por la Junta Directiva (escalones en cada decisión) frente a la "
                    "inflación anual.", "Policy rate set by the Board (steps at each decision) versus annual inflation.")),
    "g-real": (("Banco de la República: tasa de política y curvas TES; cálculo propio",
                "Banco de la República: policy rate and TES curves; own calculation"),
               ("Tasa real ex ante = (1 + tasa del Banco) / (1 + inflación esperada a 1 año) − 1 (ecuación de Fisher). "
                "Neutral estimada por el equipo técnico del Banco: 2,7%–3,0%.",
                "Ex-ante real rate = (1 + policy rate) / (1 + 1-year expected inflation) − 1 (Fisher equation). Neutral "
                "estimated by the Bank's staff: 2.7%–3.0%.")),
    "g-dolar": (("Banco de la República, Tasa Representativa del Mercado (TRM), certificada por la Superfinanciera",
                 "Banco de la República, market exchange rate (TRM), certified by the Financial Superintendence"),
                ("Pesos por dólar, promedio semanal. Panel inferior: variación porcentual frente a un año antes.",
                 "Pesos per dollar, weekly average. Lower panel: percent change versus a year earlier.")),
    "g-bolsa": (("Bolsa de Valores de Colombia (BVC), índice COLCAP, publicado por el Banco de la República",
                 "Colombian Stock Exchange (BVC), COLCAP index, published by Banco de la República"),
                ("Índice de capitalización de las acciones más líquidas, sin dividendos; cierre semanal.",
                 "Cap-weighted index of the most liquid stocks, price only; weekly close.")),
    "g-itcr": (("Banco de la República, Índice de la Tasa de Cambio Real (ITCR-IPC)",
                "Banco de la República, Real Exchange Rate Index (ITCR-CPI)"),
               ("Tasa de cambio ajustada por la inflación de Colombia frente a la de sus socios comerciales. Por encima "
                "de 100 el peso está más barato (en términos reales) que en el año base.",
                "Exchange rate adjusted for Colombian versus trading partners' inflation. Above 100 the peso is cheaper "
                "(in real terms) than in the base year.")),
    "g-indices": (("BVC/Banco de la República (COLCAP); Yahoo Finance (precios); iShares MSCI COLCAP (canasta)",
                   "BVC/Banco de la República (COLCAP); Yahoo Finance (prices); iShares MSCI COLCAP (basket)"),
                  ("Equiponderado y 7 Magníficas: promedio simple de retornos semanales de sus acciones (rebalanceo semanal), "
                   "sin dividendos; se descartan retornos semanales mayores a ±60%. Base 100 al inicio del periodo elegido. "
                   "Usa la canasta actual hacia atrás (sesgo de supervivencia).",
                   "Equal-weighted and Magnificent 7: simple average of weekly stock returns (weekly rebalancing), price "
                   "only; weekly returns beyond ±60% are dropped. Base 100 at the start of the chosen period. The current "
                   "basket is applied backwards (survivorship bias).")),
    "g-pesos": (("iShares MSCI COLCAP (BlackRock), composición diaria del fondo",
                 "iShares MSCI COLCAP (BlackRock), daily fund holdings"),
                ("Peso de cada acción en el fondo que replica el COLCAP (sin efectivo). Aproxima los pesos oficiales de la BVC.",
                 "Weight of each stock in the fund tracking the COLCAP (cash excluded). Approximates official BVC weights.")),
    "g-cc": (("Banco de la República, balanza de pagos", "Banco de la República, balance of payments"),
             ("Saldo de la cuenta corriente como porcentaje del PIB, trimestral. Negativo = déficit que se financia con "
              "recursos del exterior.", "Current account balance as % of GDP, quarterly. Negative = deficit financed from abroad.")),
    "g-deuda": (("Ministerio de Hacienda, vía Banco de la República", "Ministry of Finance, via Banco de la República"),
                ("Deuda bruta del Gobierno Nacional Central como porcentaje del PIB, cierre de cada año.",
                 "Central government gross debt as % of GDP, end of each year.")),
    "g-ciclo-reloj": (("DANE, PIB real desestacionalizado; cálculo propio", "DANE, seasonally adjusted real GDP; own calculation"),
                      ("Reloj del ciclo (metodología OCDE): eje horizontal = brecha del producto (HP en tiempo real); eje "
                       "vertical = su cambio en 2 trimestres. La fase es el cuadrante.",
                       "Business-cycle clock (OECD method): horizontal axis = output gap (real-time HP); vertical axis = its "
                       "2-quarter change. The phase is the quadrant.")),
    "g-ciclo-hist": (("DANE, PIB real desestacionalizado; cálculo propio", "DANE, seasonally adjusted real GDP; own calculation"),
                     ("Barras: brecha del producto por trimestre, coloreada por fase. Línea punteada: cambio de la brecha en 2 "
                      "trimestres.", "Bars: output gap by quarter, coloured by phase. Dotted line: 2-quarter change of the gap.")),
    "g-curva-tes": (BR_TES, ("Tasas cero cupón a 1, 5 y 10 años del día elegido; líneas finas: cierre de cada año marcado.",
                             "Zero-coupon yields at 1, 5 and 10 years on the chosen day; thin lines: year-end of each ticked year.")),
    "g-curva-hist": (BR_TES, ("Serie diaria de las tasas cero cupón a 1, 5 y 10 años.", "Daily series of 1-, 5- and 10-year zero-coupon yields.")),
    "g-cp-barras": (("Banco de la República (IPC por grupos: alimentos, regulados, sin alimentos, sin alimentos ni regulados) y DANE, IPC",
                     "Banco de la República (CPI groups: food, regulated, ex food, ex food & regulated) and DANE, CPI"),
                    ("Variación anual del índice de precios de cada grupo en el último mes publicado; la raya es el mismo dato 12 meses "
                     "antes. Los grupos se solapan (el total contiene a todos), por eso no suman.",
                     "Annual change of each group's price index in the latest published month; the tick is the same figure 12 months "
                     "earlier. Groups overlap (headline contains all of them), so they do not add up.")),
    "g-cp-lineas": (("Banco de la República, inflación por grupos de precios", "Banco de la República, inflation by price group"),
                    ("Variación anual mensual de cada grupo. Regulados: servicios públicos, combustibles, transporte y educación con "
                     "precio fijado por el Estado.", "Monthly annual change of each group. Regulated: utilities, fuel, transport and "
                     "education with state-set prices.")),
    "g-consenso": (("DANE, PIB real desestacionalizado; cálculo propio", "DANE, seasonally adjusted real GDP; own calculation"),
                   ("Cinco brechas del producto (log del PIB menos su tendencia): HP en tiempo real (λ = 1.600, solo datos hasta cada trimestre); "
                    "HP de dos colas; Hamilton (2018), error de proyección a 8 trimestres con 4 rezagos; Christiano y Fitzgerald (2003), filtro de "
                    "banda de 6 a 32 trimestres; Beveridge y Nelson (1981) con un AR(4) del crecimiento. La tendencia se estima sin 2020T2–2021T2. "
                    "La mediana es el consenso; el rango mide la incertidumbre.",
                    "Five output gaps (log GDP minus trend): real-time HP (λ = 1,600, data up to each quarter only); two-sided HP; Hamilton (2018), "
                    "8-quarter-ahead projection error with 4 lags; Christiano-Fitzgerald (2003) band-pass of 6 to 32 quarters; Beveridge-Nelson (1981) "
                    "with an AR(4) of growth. Trend estimated excluding 2020Q2–2021Q2. The median is the consensus; the range measures uncertainty.")),
    "g-ciclo-mensual": (("DANE, Indicador de Seguimiento a la Economía (ISE), serie desestacionalizada", "DANE, Economic Tracking Indicator (ISE), seasonally adjusted"),
                        ("Brecha = 100 × (log ISE − tendencia HP en tiempo real, λ = 129.600 de Ravn y Uhlig). La tendencia excluye mar-2020 a jun-2021. "
                         "Fase: signo de la brecha y su cambio en 3 meses (reloj del ciclo de la OCDE).",
                         "Gap = 100 × (log ISE − real-time HP trend, λ = 129,600 per Ravn-Uhlig). Trend excludes Mar-2020 to Jun-2021. "
                         "Phase: sign of the gap and its 3-month change (OECD cycle clock).")),
    "g-motores": (("DANE, ISE por grandes ramas, series desestacionalizadas", "DANE, ISE by broad branch, seasonally adjusted"),
                  ("Misma brecha mensual del ISE, calculada para actividades primarias, secundarias y terciarias por separado.",
                   "Same monthly ISE gap, computed separately for primary, secondary and tertiary activities.")),
    "g-aportes": ((DANE_PIB[0], DANE_PIB[1]),
                  ("Aporte = crecimiento anual real del sector × su peso en el PIB del mismo trimestre del año anterior (precios constantes). "
                   "La suma de los aportes es el crecimiento del PIB a precios básicos.",
                   "Contribution = sector's real annual growth × its GDP share in the same quarter a year earlier (constant prices). "
                   "Contributions add up to GDP growth at basic prices.")),
    "g-amplitud": ((DANE_PIB[0], DANE_PIB[1]),
                   ("Para cada uno de los 12 sectores: 100 × (log del valor agregado real − tendencia HP en tiempo real, λ = 1.600, sin 2020T2–2021T2). "
                    "Es un índice de difusión al estilo de los de la Reserva Federal de Filadelfia.",
                    "For each of the 12 sectors: 100 × (log real value added − real-time HP trend, λ = 1,600, excluding 2020Q2–2021Q2). "
                    "A diffusion index in the style of the Philadelphia Fed.")),
    "g-ritmo": (("DANE, ISE desestacionalizado", "DANE, seasonally adjusted ISE"),
                ("Anual: variación frente al mismo mes del año anterior. Últimos 3 meses: (promedio de los 3 últimos / promedio de los 3 anteriores)^4 − 1. "
                 "Ambas se recortan en −15% y 25% para que 2020 no aplaste la escala.",
                 "Annual: change versus the same month a year earlier. Last 3 months: (average of last 3 / previous 3)^4 − 1. "
                 "Both capped at −15% and 25% so 2020 does not flatten the scale.")),
    "g-expansiones": (("DANE, ISE desestacionalizado; cálculo propio", "DANE, seasonally adjusted ISE; own calculation"),
                      ("Picos y valles: máximos y mínimos locales del promedio móvil de 3 meses en ventanas de ±6 meses, alternados (Bry y Boschan, 1971; "
                       "Harding y Pagan, 2002). Variación: cambio del ISE entre el inicio y el fin de cada fase. Es un fechado académico, no oficial.",
                       "Peaks and troughs: local maxima and minima of the 3-month moving average in ±6-month windows, alternating (Bry-Boschan, 1971; "
                       "Harding-Pagan, 2002). Change: ISE change between start and end of each phase. An academic dating, not an official one.")),
    "g-empleo-ciclo": ((DANE_GEIH[0], DANE_GEIH[1]),
                       ("Diferencia en puntos porcentuales entre el promedio de 3 meses de cada tasa (desestacionalizada) y el mismo promedio 12 meses antes.",
                        "Percentage-point difference between the 3-month average of each (seasonally adjusted) rate and the same average 12 months earlier.")),
    "g-okun": (("DANE: PIB real y GEIH; cálculo propio", "DANE: real GDP and GEIH; own calculation"),
               ("Okun (1962) en brechas: (desempleo − tendencia HP) = β × brecha del producto (HP dos colas). Se estima por MCO con 2009–2025 sin 2020–2021. "
                "Una β cercana a cero indica que el empleo responde poco a la producción.",
                "Okun (1962) in gaps: (unemployment − HP trend) = β × output gap (two-sided HP). OLS over 2009–2025 excluding 2020–2021. "
                "A β close to zero means employment responds little to output.")),
    # --- comercio exterior (DANE con registros administrativos de la DIAN)
    "g-comercio-flujos": (DANE_EXPO_IMPO,
                          ("Exportaciones FOB (valor en el puerto colombiano) e importaciones CIF (incluyen seguro y flete), en dólares corrientes. "
                           "Cada punto es la suma móvil de 12 meses, que elimina la estacionalidad sin modelos. Las cifras del último año son provisionales.",
                           "Exports FOB (value at the Colombian port) and imports CIF (including insurance and freight), in current dollars. "
                           "Each point is a 12-month moving sum, which removes seasonality without models. Latest-year figures are provisional.")),
    "g-balanza": (DANE_EXPO_IMPO,
                  ("Balanza = exportaciones FOB − importaciones CIF de cada año calendario (sumas mensuales del DANE). Como las importaciones incluyen "
                   "flete y seguro, este saldo es algo más negativo que el de la balanza de pagos del Banco de la República (que usa FOB en ambos lados).",
                   "Balance = FOB exports − CIF imports for each calendar year (DANE monthly sums). Because imports include freight and insurance, "
                   "this balance is somewhat more negative than the Banco de la República balance-of-payments figure (FOB on both sides).")),
    "g-expo-productos": (DANE_EXPO,
                         ("Suma de los últimos 12 meses por grupo del DANE: café, carbón, petróleo y derivados, ferroníquel (tradicionales) y no tradicionales. "
                          "Variación: frente a los 12 meses anteriores, en dólares.",
                          "Sum of the last 12 months by DANE group: coffee, coal, oil and derivatives, ferronickel (traditional) and non-traditional. "
                          "Change: versus the previous 12 months, in dollars.")),
    "g-expo-minero": (DANE_EXPO,
                      ("(Petróleo y derivados + carbón) / exportaciones totales, con sumas móviles de 12 meses. Depende de precios internacionales y volúmenes.",
                       "(Oil and derivatives + coal) / total exports, using 12-month moving sums. Driven by international prices and volumes.")),
    "g-impo-uso": (DANE_IMPO,
                   ("Cuadro A13 del anexo de importaciones: clasificación CUODE (uso o destino económico), valor CIF del periodo enero–último mes "
                    "frente al mismo periodo del año anterior. Entre paréntesis: participación en el total del periodo.",
                    "Table A13 of the imports annex: CUODE classification (economic use), CIF value for January–latest month versus the same period "
                    "a year earlier. In brackets: share of the period total.")),
    "g-impo-estructura": (DANE_IMPO,
                          ("Participación de los tres grandes grupos CUODE en el valor CIF anual (sin «no clasificados»). El año en curso (*) es acumulado a la fecha.",
                           "Share of the three main CUODE groups in annual CIF value (excluding 'not classified'). The current year (*) is year-to-date.")),
    "g-destinos": (DANE_EXPO,
                   ("Anexo de exportaciones por principales destinos (valor FOB). Participación de la suma de 12 meses; «Resto» incluye los demás países.",
                    "Exports annex by main destination (FOB value). Share of the 12-month sum; 'Rest' includes the remaining countries.")),
    "g-origenes": (DANE_IMPO,
                   ("Anexo de importaciones por principales países de origen (valor CIF). Participación de la suma de 12 meses sobre las importaciones totales publicadas.",
                    "Imports annex by main country of origin (CIF value). Share of the 12-month sum over total published imports.")),
    # --- crecimiento ampliado
    "g-velocidades": (DANE_PIB,
                      ("Anual: PIB real original frente al mismo trimestre del año anterior. 12 meses: suma de los últimos 4 trimestres frente a los 4 anteriores. "
                       "Trimestre anualizado: ((PIB desestacionalizado t / t−1)^4 − 1) × 100, la convención de la Oficina de Análisis Económico de EE. UU. (BEA).",
                       "Annual: original real GDP versus the same quarter a year earlier. 12 months: sum of the last 4 quarters versus the previous 4. "
                       "Annualised quarter: ((seasonally adjusted GDP t / t−1)^4 − 1) × 100, the US Bureau of Economic Analysis (BEA) convention.")),
    "g-periodos": (DANE_PIB,
                   ("Tasa compuesta anual: (PIB del último año / PIB del año previo al periodo)^(1/años) − 1, con PIB real anual (suma de trimestres). "
                    "Los periodos siguen hitos conocidos: auge del petróleo (2010–2014), caída del precio y ajuste (2015–2019), pandemia (2020–2021).",
                    "Compound annual rate: (GDP in the final year / GDP in the year before the period)^(1/years) − 1, using annual real GDP (sum of quarters). "
                    "Periods follow known milestones: oil boom (2010–2014), price slump and adjustment (2015–2019), pandemic (2020–2021).")),
    "g-real-nominal": (DANE_PIB,
                       ("Variación anual del PIB a precios corrientes (billones de pesos) y a precios constantes de 2015 (series originales).",
                        "Annual change of GDP at current prices (trillion pesos) and at constant 2015 prices (original series).")),
    "g-deflactor": (("DANE (PIB nominal y real) y DANE-IPC; cálculo propio", "DANE (nominal and real GDP) and DANE CPI; own calculation"),
                    ("Deflactor implícito = PIB nominal / PIB real; se muestra su variación anual. El IPC es el promedio trimestral de la inflación anual. "
                     "La diferencia refleja sobre todo los términos de intercambio: el deflactor incluye exportaciones y excluye importaciones (Kohli, 2004).",
                     "Implicit deflator = nominal GDP / real GDP; its annual change is shown. CPI is the quarterly average of annual inflation. "
                     "The gap mostly reflects the terms of trade: the deflator includes exports and excludes imports (Kohli, 2004).")),
    "g-aportes-grupos": (("DANE, PIB por actividad económica; cálculo propio", "DANE, GDP by economic activity; own calculation"),
                         ("Aporte del sector = variación anual × participación en el valor agregado del año anterior (precios constantes); los 12 sectores se agrupan en 4. "
                          "Los aportes suman el valor agregado, no el PIB: falta el aporte de los impuestos netos de subvenciones, y el encadenamiento genera pequeñas diferencias.",
                          "Sector contribution = annual change × share of the previous year's value added (constant prices); the 12 sectors are grouped into 4. "
                          "Contributions add up to value added, not GDP: net taxes are missing, and chain-linking creates small differences.")),
    "g-sin-gobierno": (("DANE, PIB por actividad económica; cálculo propio", "DANE, GDP by economic activity; own calculation"),
                       ("Crecimiento sin el sector X = (suma de aportes − aporte de X) / (suma de participaciones − participación de X). "
                        "El sector «Gobierno, educación y salud» (secciones O, P y Q del CIIU) incluye también educación y salud privadas: es una aproximación al sector público.",
                        "Growth excluding sector X = (sum of contributions − contribution of X) / (sum of shares − share of X). "
                        "The 'Government, education and health' sector (ISIC sections O, P and Q) also includes private education and health: it approximates the public sector.")),
    "g-sectores-crecen": (("DANE, PIB por actividad económica; cálculo propio", "DANE, GDP by economic activity; own calculation"),
                          ("Índice de difusión (Burns y Mitchell, 1946): número de los 12 sectores con variación anual positiva en cada trimestre.",
                           "Diffusion index (Burns and Mitchell, 1946): number of the 12 sectors with positive annual change in each quarter.")),
    "g-sector-historia": (("DANE, PIB por actividad económica; cálculo propio", "DANE, GDP by economic activity; own calculation"),
                          ("Promedio simple de la variación anual de cada sector en 2015T1–2019T4 frente al promedio de los últimos 4 trimestres publicados.",
                           "Simple average of each sector's annual change in 2015Q1–2019Q4 versus the average of the latest 4 published quarters.")),
    "g-nivel": (("DANE, PIB real desestacionalizado; cálculo propio", "DANE, seasonally adjusted real GDP; own calculation"),
                ("Índice T4 2019 = 100. Camino previo: regresión log-lineal del PIB desestacionalizado de 2015T1–2019T4, prolongada con la misma pendiente. "
                 "Es un contrafactual descriptivo, no un pronóstico. Ver Cerra y Saxena (2008) sobre pérdidas permanentes de nivel tras las crisis.",
                 "Index 2019 Q4 = 100. Earlier path: log-linear regression of seasonally adjusted GDP over 2015Q1–2019Q4, extended with the same slope. "
                 "A descriptive counterfactual, not a forecast. See Cerra and Saxena (2008) on permanent level losses after crises.")),

    # --- demanda, inversion, hogares y por persona
    "g-demanda-aportes": (("DANE, PIB por el enfoque del gasto (anexos a precios constantes y corrientes)", "DANE, GDP by expenditure (constant and current price annexes)"),
                          ("Aporte = (componente_t − componente_t−4) / PIB_t−4 × 100, con volúmenes encadenados en datos originales. Comercio neto = aporte de exportaciones − aporte de importaciones. "
                           "«Existencias y discrepancia» es el residuo hasta el crecimiento del PIB: variación de inventarios más la no aditividad de los índices encadenados.",
                           "Contribution = (component_t − component_t−4) / GDP_t−4 × 100, using chain-linked volumes (original data). Net trade = exports contribution − imports contribution. "
                           "'Inventories and discrepancy' is the residual up to GDP growth: change in inventories plus the non-additivity of chain-linked indices.")),
    "g-demanda-crec": (("DANE, PIB por el enfoque del gasto (anexos a precios constantes y corrientes)", "DANE, GDP by expenditure (constant and current price annexes)"),
                       ("Variación anual de los volúmenes encadenados (datos originales) del último trimestre publicado. Consumo de los hogares incluye las ISFLH.",
                        "Annual change of chain-linked volumes (original data) in the latest published quarter. Household consumption includes NPISHs.")),
    "g-tasa-inversion": (("DANE, PIB por el enfoque del gasto (anexos a precios constantes y corrientes)", "DANE, GDP by expenditure (constant and current price annexes)"),
                         ("Formación bruta de capital fijo / PIB, ambos a precios corrientes y como suma de los últimos 4 trimestres. No incluye variación de existencias.",
                          "Gross fixed capital formation / GDP, both at current prices and summed over the latest 4 quarters. Excludes change in inventories.")),
    "g-inversion-activos": (("DANE, PIB por el enfoque del gasto (anexos a precios constantes y corrientes)", "DANE, GDP by expenditure (constant and current price annexes)"),
                            ("Cuadro 6 del anexo de gasto: formación bruta de capital fijo por tipo de activo (AN111 vivienda, AN112 otros edificios y estructuras, AN113+AN114 maquinaria y equipo, AN117 propiedad intelectual), volúmenes desestacionalizados; índice T4 2019 = 100.",
                             "Table 6 of the expenditure annex: gross fixed capital formation by asset (AN111 housing, AN112 other buildings and structures, AN113+AN114 machinery and equipment, AN117 intellectual property), seasonally adjusted volumes; index 2019 Q4 = 100.")),
    "g-consumo-durabilidad": (("DANE, PIB por el enfoque del gasto (anexos a precios constantes y corrientes)", "DANE, GDP by expenditure (constant and current price annexes)"),
                              ("Cuadro 3: gasto de consumo final de los hogares en el territorio por durabilidad, volúmenes en datos originales; variación de la suma de 4 trimestres frente a los 4 anteriores.",
                               "Table 3: household final consumption in the territory by durability, volumes in original data; change of the 4-quarter sum versus the previous 4.")),
    "g-consumo-finalidad": (("DANE, PIB por el enfoque del gasto (anexos a precios constantes y corrientes)", "DANE, GDP by expenditure (constant and current price annexes)"),
                            ("Cuadro 3: consumo de los hogares por división COICOP (12 finalidades), volúmenes en datos originales; variación de 12 meses. La participación usa la suma de volúmenes encadenados (aproximada).",
                             "Table 3: household consumption by COICOP division (12 purposes), volumes in original data; 12-month change. Shares use the sum of chain-linked volumes (approximate).")),
    "g-pib-persona": (("DANE: PIB real y proyecciones de población (Censo 2018, actualización 2025); cálculo propio", "DANE: real GDP and population projections (2018 Census, 2025 update); own calculation"),
                      ("PIB real anual (suma de 4 trimestres, pesos de 2015) / población total nacional a 30 de junio. La población de 2018 en adelante es la proyección oficial vigente del DANE; antes de 2018, la retroproyección.",
                       "Annual real GDP (sum of 4 quarters, 2015 pesos) / total national population at 30 June. Population from 2018 onwards is DANE's current official projection; before 2018, the back-projection.")),
    "g-pib-persona-usd": (("DANE (PIB nominal, población) y Banco de la República (TRM); cálculo propio", "DANE (nominal GDP, population) and Banco de la República (TRM); own calculation"),
                          ("PIB nominal anual / población / TRM promedio del año calendario. Método Atlas no aplicado: es la conversión simple a la tasa de mercado.",
                           "Annual nominal GDP / population / calendar-year average TRM. The Atlas method is not applied: it is a simple conversion at the market rate.")),
    "g-productividad": (("DANE: PIB real y GEIH desestacionalizada (población ocupada); cálculo propio", "DANE: real GDP and seasonally adjusted GEIH (employed population); own calculation"),
                        ("Productividad laboral aparente (OECD, 2001) = PIB real de 4 trimestres / promedio de ocupados de 12 meses; índices 2015 = 100. No corrige por horas trabajadas ni por informalidad.",
                         "Apparent labour productivity (OECD, 2001) = 4-quarter real GDP / 12-month average employment; indices 2015 = 100. Not adjusted for hours worked or informality.")),
    # --- capacidad ampliada
    "g-cap-sectores": (("DANE, PIB trimestral por actividad; cálculo propio", "DANE, quarterly GDP by activity; own calculation"),
                       ("Brecha = 100 × (ln nivel real − ln tendencia), con tendencia Hodrick-Prescott de una cola (λ = 1.600) calculada sin 2020T2–2021T2: en cada trimestre solo usa datos disponibles hasta ese momento.",
                        "Gap = 100 × (ln real level − ln trend), with a one-sided Hodrick-Prescott trend (λ = 1,600) computed excluding 2020Q2–2021Q2: each quarter uses only data available up to then.")),
    "g-cap-sectores-hoy": (("DANE, PIB trimestral por actividad; cálculo propio", "DANE, quarterly GDP by activity; own calculation"),
                           ("Último trimestre de la brecha de cada sector frente a su tendencia HP de una cola.",
                            "Latest quarter of each sector's gap versus its one-sided HP trend.")),
    "g-cap-subutilizacion": (("DANE, Gran Encuesta Integrada de Hogares (GEIH)", "DANE, Integrated Household Survey (GEIH)"),
                             ("Indicadores de subutilización de la 19.ª CIET (OIT, 2013), total nacional, sin desestacionalizar, promedio móvil de 12 meses: TD = desocupados / fuerza de trabajo; "
                              "TCSD = (desocupados + subocupados por horas) / fuerza de trabajo; MCSFT = (desocupados + subocupados + fuerza de trabajo potencial) / fuerza de trabajo ampliada.",
                              "Underutilisation indicators from the 19th ICLS (ILO, 2013), national total, not seasonally adjusted, 12-month moving average: UR = unemployed / labour force; "
                              "LU2 = (unemployed + time-related underemployed) / labour force; LU4 = (unemployed + underemployed + potential labour force) / extended labour force.")),
    "g-cap-desempleo": (("DANE, GEIH desestacionalizada; cálculo propio", "DANE, seasonally adjusted GEIH; own calculation"),
                        ("Promedio trimestral de la tasa de desempleo desestacionalizada y su tendencia Hodrick-Prescott (λ = 1.600) estimada sin 2020–2021 e interpolada en esos años.",
                         "Quarterly average of the seasonally adjusted unemployment rate and its Hodrick-Prescott trend (λ = 1,600), estimated excluding 2020–2021 and interpolated over those years.")),
    "g-cap-mapa": (("DANE: Cuentas departamentales y GEIH (32 ciudades, año móvil); cálculo propio", "DANE: departmental accounts and GEIH (32 cities, rolling year); own calculation"),
                   ("Mapa esquemático (cartograma de casillas), no a escala. Crecimiento y tamaño frente a 2019: PIB real (volúmenes encadenados). PIB por persona: precios corrientes, Colombia = 100. "
                    "Desempleo: ciudad capital del departamento (Bogotá para Cundinamarca no se asigna). El último año es preliminar.",
                    "Schematic map (tile cartogram), not to scale. Growth and size versus 2019: real GDP (chain-linked volumes). GDP per person: current prices, Colombia = 100. "
                    "Unemployment: the department's capital city (Bogotá is not assigned to Cundinamarca). The latest year is preliminary.")),
    "g-cap-regiones": (("DANE, Cuentas nacionales departamentales, base 2015 (anexos de PIB por departamento y por actividad)", "DANE, departmental national accounts, base 2015 (GDP by department and by activity annexes)"),
                       ("PIB real de cada departamento en el último año publicado frente a 2019 (volúmenes encadenados, base 2015). Último año preliminar.",
                        "Real GDP of each department in the latest published year versus 2019 (chain-linked volumes, base 2015). Latest year preliminary.")),
    "g-cap-estructura": (("DANE, Cuentas nacionales departamentales, base 2015 (anexos de PIB por departamento y por actividad)", "DANE, departmental national accounts, base 2015 (GDP by department and by activity annexes)"),
                         ("Participación de cada una de las 12 agrupaciones CIIU en el valor agregado del departamento (sin impuestos), a precios corrientes del último año.",
                          "Share of each of the 12 ISIC groupings in the department's value added (excluding taxes), at current prices in the latest year.")),
    "g-cap-diversificacion": (("DANE, Cuentas nacionales departamentales, base 2015 (anexos de PIB por departamento y por actividad)", "DANE, departmental national accounts, base 2015 (GDP by department and by activity annexes)"),
                              ("Número equivalente = 1 / Σ sᵢ², donde sᵢ es la participación de la rama i en el valor agregado del departamento (Herfindahl, 1950; Hirschman, 1964).",
                               "Equivalent number = 1 / Σ sᵢ², where sᵢ is branch i's share of the department's value added (Herfindahl, 1950; Hirschman, 1964).")),
    "g-cap-ciudades": (("DANE, Gran Encuesta Integrada de Hogares (GEIH)", "DANE, Integrated Household Survey (GEIH)"),
                       ("Tasa de desocupación de cada una de las 32 ciudades capitales (13 con su área metropolitana), en año móvil de 12 meses, frente al año móvil terminado 12 meses antes.",
                        "Unemployment rate of each of the 32 capital cities (13 with their metropolitan area), as a 12-month rolling year, versus the rolling year ending 12 months earlier.")),
    # --- empleo ampliado
    "g-emp-ramas": (("DANE, Gran Encuesta Integrada de Hogares (GEIH), anexo mensual", "DANE, Integrated Household Survey (GEIH), monthly annex"),
                    ("Población ocupada por rama de actividad (CIIU Rev. 4 A.C., 13 agrupaciones de la GEIH), total nacional, sin desestacionalizar: promedio de los últimos 3 meses menos el promedio de los mismos 3 meses del año anterior. "
                     "La GEIH agrupa la minería con los servicios públicos.",
                     "Employed population by sector (ISIC Rev. 4, 13 GEIH groupings), national total, not seasonally adjusted: average of the latest 3 months minus the same 3 months a year earlier. "
                     "The GEIH groups mining with utilities.")),
    "g-emp-ramas-2019": (("DANE, Gran Encuesta Integrada de Hogares (GEIH), anexo mensual", "DANE, Integrated Household Survey (GEIH), monthly annex"), ("Promedio de los últimos 12 meses frente al promedio de 2019.", "Average of the latest 12 months versus the 2019 average.")),
    "g-emp-posicion": (("DANE, Gran Encuesta Integrada de Hogares (GEIH), anexo mensual", "DANE, Integrated Household Survey (GEIH), monthly annex"),
                       ("Posición ocupacional según la CISE-93 (OIT): participación de cada categoría en los ocupados, con promedios móviles de 12 meses. Se omite la categoría «otro» (menos de 0,1%).",
                        "Status in employment following ICSE-93 (ILO): share of each category in total employment, 12-month moving averages. The 'other' category (under 0.1%) is omitted.")),
    "g-emp-posicion-cambio": (("DANE, Gran Encuesta Integrada de Hogares (GEIH), anexo mensual", "DANE, Integrated Household Survey (GEIH), monthly annex"), ("Promedio de los últimos 3 meses menos el mismo periodo del año anterior, en miles de personas.", "Average of the latest 3 months minus the same period a year earlier, in thousands.")),
    "g-emp-genero-td": (("DANE, Gran Encuesta Integrada de Hogares (GEIH), anexo mensual", "DANE, Integrated Household Survey (GEIH), monthly annex"), ("Tasa de desocupación por sexo, total nacional, promedio móvil de 12 meses (elimina la estacionalidad sin modelos).",
                               "Unemployment rate by sex, national total, 12-month moving average (removes seasonality without models).")),
    "g-emp-genero-tgp": (("DANE, Gran Encuesta Integrada de Hogares (GEIH), anexo mensual", "DANE, Integrated Household Survey (GEIH), monthly annex"), ("Tasa global de participación = fuerza de trabajo / población en edad de trabajar (15 años y más), por sexo, promedio móvil de 12 meses.",
                                "Participation rate = labour force / working-age population (15 and over), by sex, 12-month moving average.")),
    "g-emp-jovenes": (("DANE, GEIH: mercado laboral de la juventud (15 a 28 años)", "DANE, GEIH: youth labour market (15 to 28)"), ("Tasa de desocupación de las personas de 15 a 28 años (Ley 1622 de 2013), trimestre móvil. La referencia nacional es la serie desestacionalizada mensual.",
                             "Unemployment rate of 15–28 year-olds (Law 1622 of 2013), rolling quarter. The national reference is the seasonally adjusted monthly series.")),
    "g-emp-nini": (("DANE, GEIH: mercado laboral de la juventud (15 a 28 años)", "DANE, GEIH: youth labour market (15 to 28)"), ("Jóvenes de 15 a 28 años que no estudian ni están ocupados, como porcentaje del total de jóvenes; la serie de mujeres y la de hombres suman el total.",
                          "15–28 year-olds who neither study nor are employed, as a share of all young people; the women and men series add up to the total.")),
    "g-emp-area": (("DANE, Gran Encuesta Integrada de Hogares (GEIH), anexo mensual", "DANE, Integrated Household Survey (GEIH), monthly annex"), ("Tasa de desocupación en cabeceras y en centros poblados y rural disperso, trimestre móvil, sin desestacionalizar.",
                          "Unemployment rate in urban centres and in villages and dispersed rural areas, rolling quarter, not seasonally adjusted.")),
    "g-emp-fuera": (("DANE, Gran Encuesta Integrada de Hogares (GEIH), anexo mensual", "DANE, Integrated Household Survey (GEIH), monthly annex"), ("Población fuera de la fuerza de trabajo según su actividad principal (estudiando, oficios del hogar, otros), total nacional, promedio de 12 meses, en millones.",
                           "Population outside the labour force by main activity (studying, household work, other), national total, 12-month average, in millions.")),
    # --- inflacion ampliada
    "g-inf-aportes": (("DANE, IPC base diciembre 2018 (anexos mensuales)", "DANE, CPI base December 2018 (monthly annexes)"), ("Aporte de cada división (COICOP) a la variación anual del IPC total, calculado por el DANE con las ponderaciones de la canasta 2018 y la evolución de precios relativos.",
                             "Each COICOP division's contribution to the annual change in total CPI, computed by DANE with the 2018 basket weights and the evolution of relative prices.")),
    "g-inf-divisiones": (("DANE, IPC base diciembre 2018 (anexos mensuales)", "DANE, CPI base December 2018 (monthly annexes)"), ("Variación anual del índice de cada división de gasto, total nacional.", "Annual change in each spending division's index, national total.")),
    "g-inf-bienes-servicios": (("DANE, IPC base diciembre 2018 (anexos mensuales)", "DANE, CPI base December 2018 (monthly annexes)"), ("Índices del DANE por durabilidad (servicios, bienes durables, semidurables y no durables), base diciembre 2018 = 100; variación frente al mismo mes del año anterior.",
                                      "DANE indices by durability (services, durable, semi-durable and non-durable goods), base December 2018 = 100; change versus the same month a year earlier.")),
    "g-inf-energia": (("DANE, IPC base diciembre 2018 (anexos mensuales)", "DANE, CPI base December 2018 (monthly annexes)"), ("IPC de energéticos (gas, energía eléctrica y combustibles) e IPC total sin alimentos ni energéticos, publicados por el DANE; variación anual.",
                             "Energy CPI (gas, electricity and fuel) and total CPI excluding food and energy, published by DANE; annual change.")),
    "g-inf-difusion": (("DANE, IPC base diciembre 2018 (anexos mensuales)", "DANE, CPI base December 2018 (monthly annexes)"), ("Histograma de la variación anual de las 188 subclases de la canasta (sin ponderar), en intervalos de 1 pp; valores extremos agrupados en −10% y 20%.",
                              "Histogram of the annual change in the 188 basket subclasses (unweighted), in 1 pp bins; extreme values grouped at −10% and 20%.")),
    "g-inf-subclases": (("DANE, IPC base diciembre 2018 (anexos mensuales)", "DANE, CPI base December 2018 (monthly annexes)"), ("Contribución de cada subclase a la variación anual del IPC total (DANE), en puntos porcentuales.", "Each subclass's contribution to the annual change in total CPI (DANE), in percentage points.")),
    "g-inf-ingresos": (("DANE, IPC base diciembre 2018 (anexos mensuales)", "DANE, CPI base December 2018 (monthly annexes)"), ("IPC calculado con la canasta de cada nivel de ingreso definido por el DANE (pobres, vulnerables, clase media e ingresos altos, según la línea de pobreza).",
                              "CPI computed with the basket of each income level defined by DANE (poor, vulnerable, middle class and high income, based on the poverty line).")),
    "g-inf-ciudades": (("DANE, IPC base diciembre 2018 (anexos mensuales)", "DANE, CPI base December 2018 (monthly annexes)"), ("Variación anual del IPC total en las 23 ciudades capitales con canasta propia.", "Annual change in total CPI in the 23 capital cities with their own basket.")),
    "g-inf-ciudad-division": (("DANE, IPC base diciembre 2018 (anexos mensuales)", "DANE, CPI base December 2018 (monthly annexes)"), ("Variación anual por ciudad y división de gasto (cuadro 6 del anexo).", "Annual change by city and spending division (table 6 of the annex).")),
    "g-cv-factores": (("Banco de la República, curva cero cupón TES (SEN y MEC, Nelson-Siegel)", "Banco de la República, TES zero-coupon curve (SEN and MEC, Nelson-Siegel)"), ("Factores calculados con las tasas cero cupón en pesos a 1, 5 y 10 años: nivel = promedio; pendiente = 10a − 1a; curvatura = 2×5a − 1a − 10a. Serie semanal (último dato de cada viernes).",
                      "Factors computed from the 1-, 5- and 10-year peso zero-coupon rates: level = average; slope = 10y − 1y; curvature = 2×5y − 1y − 10y. Weekly series (last value each Friday).")),
    "g-cv-invertida": (("Banco de la República, curva cero cupón TES (SEN y MEC, Nelson-Siegel)", "Banco de la República, TES zero-coupon curve (SEN and MEC, Nelson-Siegel)"), ("Episodios: tramos de al menos 5 días hábiles consecutivos con pendiente 10a − 1a negativa (datos diarios).",
                       "Episodes: runs of at least 5 consecutive business days with a negative 10y − 1y slope (daily data).")),
    "g-cv-cambios": (("Banco de la República, curva cero cupón TES (SEN y MEC, Nelson-Siegel)", "Banco de la República, TES zero-coupon curve (SEN and MEC, Nelson-Siegel)"), ("Diferencia entre la tasa cero cupón del último día y la del último día hábil disponible hace 1, 3 y 12 meses, en puntos básicos.",
                     "Difference between the latest zero-coupon rate and the one on the last available business day 1, 3 and 12 months earlier, in basis points.")),
    "g-cv-descomposicion": (("Banco de la República, curva cero cupón TES (SEN y MEC, Nelson-Siegel)", "Banco de la República, TES zero-coupon curve (SEN and MEC, Nelson-Siegel)"), ("Cambio en 12 meses de la tasa en pesos = cambio de la tasa UVR (real) + cambio de la diferencia nominal − real.",
                            "12-month change in the peso rate = change in the UVR (real) rate + change in the nominal − real gap.")),
    "g-cv-fisher": (("Banco de la República, curva cero cupón TES (SEN y MEC, Nelson-Siegel)", "Banco de la República, TES zero-coupon curve (SEN and MEC, Nelson-Siegel)"), ("Tasa UVR más la diferencia hasta la tasa en pesos. La compensación por inflación exacta es (1 + nominal)/(1 + real) − 1 (Fisher) e incluye primas por riesgo y liquidez.",
                    "UVR rate plus the gap to the peso rate. Exact inflation compensation is (1 + nominal)/(1 + real) − 1 (Fisher) and includes risk and liquidity premia.")),
    "g-cv-real": (("Banco de la República, curva cero cupón TES (SEN y MEC, Nelson-Siegel)", "Banco de la República, TES zero-coupon curve (SEN and MEC, Nelson-Siegel)"), ("Tasa cero cupón UVR a 10 años y compensación por inflación implícita (Fisher) a 10 años. Serie semanal.",
                  "10-year UVR zero-coupon rate and 10-year implied inflation compensation (Fisher). Weekly series.")),
    "g-cv-prima": (("Banco de la República (curva cero cupón TES y tasa de política monetaria)", "Banco de la República (TES zero-coupon curve and monetary policy rate)"),
                   ("Tasa cero cupón en pesos menos la tasa de política monetaria vigente ese día, en puntos porcentuales. Serie semanal.",
                    "Peso zero-coupon rate minus the monetary policy rate in force that day, in percentage points. Weekly series.")),
    "g-cv-volatilidad": (("Banco de la República, curva cero cupón TES (SEN y MEC, Nelson-Siegel)", "Banco de la República, TES zero-coupon curve (SEN and MEC, Nelson-Siegel)"), ("Desviación estándar móvil de 60 días hábiles de los cambios diarios de la tasa a 10 años, × √252, en puntos básicos. La línea punteada es el promedio desde 2003.",
                         "60-business-day rolling standard deviation of daily changes in the 10-year rate, × √252, in basis points. The dotted line is the average since 2003.")),
    "g-tc-pares": (("Banco de la República (TRM, real y sol); Reserva Federal, H.10, vía FRED (peso mexicano e índice amplio del dólar)", "Banco de la República (TRM, real and sol); Federal Reserve, H.10, via FRED (Mexican peso and broad dollar index)"),
                   ("Variación porcentual entre el último dato y el último disponible hace 12 meses de las unidades de cada moneda por dólar. Índice amplio del dólar: 26 economías ponderadas por comercio con EE. UU.",
                    "Percentage change between the latest value and the last available 12 months earlier in units of each currency per dollar. Broad dollar index: 26 economies weighted by trade with the US.")),
    "g-tc-dolar-global": (("Banco de la República (TRM); Reserva Federal, H.10, vía FRED", "Banco de la República (TRM); Federal Reserve, H.10, via FRED"),
                          ("Variación de 52 semanas de la TRM y del índice amplio nominal del dólar (último dato de cada viernes).", "52-week change in the TRM and the nominal broad dollar index (last value each Friday).")),
    "g-tc-monedas": (("Banco de la República (tasas medias COP por EUR y CNY; TRM; real por dólar); Reserva Federal vía FRED (peso mexicano)", "Banco de la República (mean COP per EUR and CNY rates; TRM; real per dollar); Federal Reserve via FRED (Mexican peso)"),
                     ("Pesos por unidad de cada moneda. Real y peso mexicano: tasa cruzada = TRM ÷ (unidades de la moneda por dólar). Serie semanal; base 100 al inicio del horizonte.",
                      "Pesos per unit of each currency. Real and Mexican peso: cross rate = TRM ÷ (units of the currency per dollar). Weekly series; 100 at the start of the horizon.")),
    "g-tc-cruces": (("Banco de la República; Reserva Federal vía FRED", "Banco de la República; Federal Reserve via FRED"),
                    ("Variación en 12 meses de los pesos por unidad de cada moneda (tasas medias del Banco de la República; cruces con la TRM para real, peso mexicano y sol).",
                     "12-month change in pesos per unit of each currency (Banco de la República mean rates; crosses with the TRM for real, Mexican peso and sol).")),
    "g-tc-itcr": (("Banco de la República", "Banco de la República"), ("ITCR según IPC con ponderaciones totales (22 socios) e ITCR-C (competitividad en el mercado de EE. UU.), base 2010 = 100. Línea punteada: promedio del ITCR desde 2000.",
                       "CPI-based ITCR with total-trade weights (22 partners) and ITCR-C (competitiveness in the US market), base 2010 = 100. Dotted line: ITCR average since 2000.")),
    "g-tc-bilateral": (("Banco de la República", "Banco de la República"), ("ITCR bilateral según IPP, último mes frente a su promedio desde 2000, en porcentaje.", "PPI-based bilateral ITCR, latest month versus its average since 2000, in percent.")),
    "g-tc-brent": (("EIA vía FRED (Brent); Banco de la República (TRM)", "EIA via FRED (Brent); Banco de la República (TRM)"),
                   ("Promedios mensuales; variación anual de cada uno. Líneas: ajuste por mínimos cuadrados (TRM = a + b × Brent) en cada periodo; describen la asociación observada, no un pronóstico.",
                    "Monthly averages; annual change of each. Lines: least-squares fit (TRM = a + b × Brent) in each period; they describe the observed association, not a forecast.")),
    "g-tc-petroleo-exportaciones": (("DANE-DIAN (exportaciones); Banco de la República (términos de intercambio)", "DANE-DIAN (exports); Banco de la República (terms of trade)"),
                                    ("Exportaciones de petróleo y derivados y de carbón sobre el total, valores FOB en dólares sumados en 12 meses. Términos de intercambio: índice de precios de exportación sobre índice de precios de importación (BanRep).",
                                     "Exports of oil and derivatives and of coal over the total, FOB dollar values summed over 12 months. Terms of trade: export price index over import price index (BanRep).")),
    "g-tc-correlacion": (("EIA y Reserva Federal vía FRED; Banco de la República", "EIA and Federal Reserve via FRED; Banco de la República"),
                         ("Correlación de Pearson móvil de 52 semanas entre variaciones semanales porcentuales.", "52-week rolling Pearson correlation between weekly percentage changes.")),
    "g-tc-balanza": (("Banco de la República", "Banco de la República"), ("Balanza cambiaria mensual (operaciones canalizadas por el mercado cambiario), suma móvil de 12 meses en miles de millones de dólares.",
                          "Monthly foreign-exchange balance (operations channelled through the FX market), 12-month rolling sum in billions of dollars.")),
    "g-tc-reservas": (("Banco de la República", "Banco de la República"), ("Reservas internacionales netas (fin de mes) y monto aprobado en las subastas de opciones PUT para acumulación de reservas, sumado por año.",
                           "Net international reserves (end of month) and amount approved in PUT option auctions for reserve accumulation, summed by year.")),
    "g-tc-volatilidad": (("Banco de la República (TRM, real); Reserva Federal vía FRED (peso mexicano)", "Banco de la República (TRM, real); Federal Reserve via FRED (Mexican peso)"),
                         ("Desviación estándar móvil de 60 días hábiles de los cambios logarítmicos diarios, × √252.", "60-business-day rolling standard deviation of daily log changes, × √252.")),
    "g-ts-ciclos": (("Banco de la República", "Banco de la República"), ("Tasa de política monetaria diaria. Ciclo = decisiones consecutivas en la misma dirección; termina cuando la siguiente decisión va en sentido contrario (las pausas no cortan el ciclo).",
                       "Daily monetary policy rate. Cycle = consecutive decisions in the same direction; it ends when the next decision goes the other way (pauses do not end a cycle).")),
    "g-ts-transmision": (("Banco de la República con información de la Superintendencia Financiera (formato 088)", "Banco de la República with Financial Superintendence data (Form 088)"), ("Promedios mensuales de datos diarios (tasa del Banco, IBR, CDT) y semanales (colocación). Tasas efectivas anuales.",
                            "Monthly averages of daily (policy rate, IBR, CD) and weekly (lending) data. Effective annual rates.")),
    "g-ts-traspaso": (("Banco de la República con información de la Superintendencia Financiera (formato 088)", "Banco de la República with Financial Superintendence data (Form 088)"), ("Traspaso = (tasa en t1 − tasa en t0) / (tasa del Banco en t1 − tasa del Banco en t0) × 100, con t0 = día anterior a la primera decisión del ciclo y t1 = tres meses después de la última (o el último dato). Ciclos desde 2008; «—» = la serie aún no existía.",
                         "Pass-through = (rate at t1 − rate at t0) / (policy rate at t1 − policy rate at t0) × 100, with t0 = day before the cycle's first decision and t1 = three months after the last (or latest data). Cycles since 2008; '—' = series did not yet exist.")),
    "g-ts-modalidades": (("Banco de la República con información de la Superintendencia Financiera (formato 088)", "Banco de la República with Financial Superintendence data (Form 088)"), ("Último dato semanal de cada modalidad. Tasa real = (1 + nominal)/(1 + inflación anual del IPC) − 1.", "Latest weekly data for each type. Real rate = (1 + nominal)/(1 + annual CPI inflation) − 1.")),
    "g-ts-margen": (("Banco de la República con información de la Superintendencia Financiera (formato 088)", "Banco de la República with Financial Superintendence data (Form 088)"), ("Diferencias de promedios mensuales: colocación total − CDT a 90 días; consumo − tasa de política.", "Differences of monthly averages: total lending − 90-day CD; consumer − policy rate.")),
    "g-ts-ibr": (("Banco de la República", "Banco de la República"), ("IBR efectivo anual por plazo en la última fecha, hace 3 meses y hace un año (último dato disponible en o antes de cada fecha).", "Effective annual IBR by tenor on the latest date, 3 months and a year earlier (last data on or before each date).")),
    "g-ts-overnight": (("Banco de la República con información de la Superintendencia Financiera", "Banco de la República with Financial Superintendence data"),
                       ("Promedio semanal de (IBR a un día − tasa de política) y (TIB − tasa de política), en puntos básicos.", "Weekly average of (overnight IBR − policy rate) and (TIB − policy rate), in basis points.")),
    "g-ts-cartera": (("Banco de la República (cartera en moneda legal); DANE (IPC)", "Banco de la República (peso loan book); DANE (CPI)"),
                     ("Crecimiento real = (1 + variación anual del saldo)/(1 + inflación anual) − 1. Cartera bruta sin ajuste por titularización; vivienda: cartera hipotecaria ajustada. Desde 2015, NIIF.",
                      "Real growth = (1 + annual change in the balance)/(1 + annual inflation) − 1. Gross loan book without securitisation adjustment; housing: adjusted mortgage book. IFRS since 2015.")),
    "g-ts-composicion": (("Banco de la República", "Banco de la República"), ("Participación de cada modalidad en la suma de comercial, consumo, vivienda (ajustada) y microcrédito en moneda legal.", "Share of each type in the sum of commercial, consumer, housing (adjusted) and microcredit in local currency.")),
    "g-ts-liquidez": (("Banco de la República", "Banco de la República"), ("Saldos diarios de subastas de expansión a un día y a otros plazos, y de la ventanilla de contracción, promediados por mes (billones de pesos).", "Daily balances of overnight and term expansion auctions and of the contraction window, averaged by month (COP trillion).")),
    "g-em-tamano": (("Superintendencia de Sociedades, 10.000 empresas más grandes (datos.gov.co)", "Superintendence of Companies, 10,000 largest companies (datos.gov.co)"), ("Suma de ingresos operacionales y de ganancia (pérdida) de las 10.000 empresas de cada año, en billones de pesos corrientes.", "Sum of operating revenue and profit (loss) of each year's 10,000 companies, in current COP trillion.")),
    "g-em-razones": (("Superintendencia de Sociedades, 10.000 empresas más grandes (datos.gov.co)", "Superintendence of Companies, 10,000 largest companies (datos.gov.co)"), ("Razones calculadas con las sumas del agregado: ganancia/ingresos, ganancia/patrimonio y pasivos/activos.", "Ratios computed from aggregate sums: profit/revenue, profit/equity and liabilities/assets.")),
    "g-em-sectores": (("Superintendencia de Sociedades, 10.000 empresas más grandes (datos.gov.co)", "Superintendence of Companies, 10,000 largest companies (datos.gov.co)"), ("Participación de cada macrosector de Supersociedades en los ingresos operacionales del año.", "Share of each Supersociedades macro-sector in the year's operating revenue.")),
    "g-em-sectores-rentabilidad": (("Superintendencia de Sociedades, 10.000 empresas más grandes (datos.gov.co)", "Superintendence of Companies, 10,000 largest companies (datos.gov.co)"), ("Margen neto y rentabilidad del patrimonio con las sumas de cada macrosector.", "Net margin and return on equity from each macro-sector's sums.")),
    "g-em-regiones": (("Superintendencia de Sociedades, 10.000 empresas más grandes (datos.gov.co)", "Superintendence of Companies, 10,000 largest companies (datos.gov.co)"), ("Región según el domicilio de la empresa, como la clasifica Supersociedades.", "Region by company address, as classified by Supersociedades.")),
    "g-em-concentracion": (("Superintendencia de Sociedades, 10.000 empresas más grandes (datos.gov.co)", "Superintendence of Companies, 10,000 largest companies (datos.gov.co)"), ("Ingresos de las N empresas más grandes sobre los ingresos de las 10.000, para el primer y el último año disponibles.", "Revenue of the N largest companies over the 10,000's revenue, for the first and latest years available.")),
    "g-em-acciones": (("Precios de cierre de las acciones de la canasta del COLCAP", "Closing prices of the COLCAP basket shares"),
                      ("Variación del cierre semanal frente al de 52 semanas antes, sin dividendos; para empresas con varias clases de acción se usa la de mayor peso.", "Change in weekly close vs 52 weeks earlier, excluding dividends; for companies with several share classes the one with the largest weight is used.")),
    "g-em-colcap-sectores": (("Canasta vigente del COLCAP (pesos del fondo iShares MSCI COLCAP)", "Current COLCAP basket (iShares MSCI COLCAP fund weights)"), ("Suma de pesos por sector.", "Sum of weights by sector.")),
    "g-em-credito": (("Banco de la República (cartera y tasas de colocación); DANE (IPC)", "Banco de la República (loan book and lending rates); DANE (CPI)"),
                     ("Crecimiento real = (1 + variación anual del saldo)/(1 + inflación anual) − 1. Tasas: promedio mensual de datos semanales, efectiva anual.", "Real growth = (1 + annual change in the balance)/(1 + annual inflation) − 1. Rates: monthly average of weekly data, effective annual.")),
    "g-em-posicion": (("Banco de la República, cuentas financieras (saldos)", "Banco de la República, financial accounts (balances)"),
                      ("Posición neta = activos financieros − pasivos de cada sector institucional, en porcentaje del PIB, trimestral.", "Net position = financial assets − liabilities of each institutional sector, as % of GDP, quarterly.")),
    "g-em-registro": (("Confecámaras, Registro Único Empresarial y Social (datos.gov.co)", "Confecámaras, Single Business and Social Register (datos.gov.co)"),
                      ("Conteo de matrículas por fecha de matrícula y de cancelaciones por fecha de cancelación; suma móvil de 12 meses. Se descarta el último mes si aún está incompleto.", "Count of registrations by registration date and cancellations by cancellation date; 12-month rolling sum. The latest month is dropped if still incomplete.")),
    "g-ext-cc": (("Banco de la República, balanza de pagos (MBP6)", "Banco de la República, balance of payments (BPM6)"), ("Suma móvil de 4 trimestres de bienes, servicios, ingreso primario e ingreso secundario; su suma es la cuenta corriente.", "4-quarter rolling sum of goods, services, primary income and secondary income; they add up to the current account.")),
    "g-ext-xm": (("Banco de la República, balanza de pagos (MBP6)", "Banco de la República, balance of payments (BPM6)"), ("Exportaciones (crédito) e importaciones (débito) de bienes, suma de 4 trimestres.", "Goods exports (credit) and imports (debit), 4-quarter sum.")),
    "g-ext-financiacion": (("Banco de la República, balanza de pagos (MBP6)", "Banco de la República, balance of payments (BPM6)"), ("Cuenta financiera por tipo de flujo con signo invertido (positivo = entrada neta), suma de 4 trimestres. Reservas: positivo = disminución.", "Financial account by flow type with inverted sign (positive = net inflow), 4-quarter sum. Reserves: positive = decrease.")),
    "g-ext-ied-sectores": (("Banco de la República, flujos de inversión extranjera directa por actividad", "Banco de la República, foreign direct investment flows by activity"), ("Suma de los últimos 4 trimestres y de los 4 anteriores.", "Sum of the last 4 quarters and of the previous 4.")),
    "g-ext-remesas": (("Banco de la República (remesas); DANE (PIB nominal)", "Banco de la República (remittances); DANE (nominal GDP)"), ("Ingresos de remesas de trabajadores, suma de 12 meses; % del PIB en dólares de los últimos 4 trimestres disponibles.", "Workers' remittance inflows, 12-month sum; % of dollar GDP over the latest 4 available quarters.")),
    "g-ext-deuda": (("Banco de la República, deuda externa", "Banco de la República, external debt"), ("Saldos mensuales de deuda externa pública y privada; total como % del PIB según el Banco de la República.", "Monthly public and private external debt balances; total as % of GDP per Banco de la República.")),
    "g-ext-pii": (("Banco de la República, posición de inversión internacional; DANE (PIB)", "Banco de la República, international investment position; DANE (GDP)"), ("Activos y pasivos financieros externos al cierre de cada trimestre; posición neta sobre el PIB en dólares de 4 trimestres.", "External financial assets and liabilities at each quarter-end; net position over 4-quarter dollar GDP.")),
    "g-fi-gobierno": (("Banco de la República (balance fiscal de caja, empalme DNP–MinHacienda); DANE (PIB nominal)", "Banco de la República (cash fiscal balance, DNP–MinHacienda splice); DANE (nominal GDP)"), ("Ingresos, gastos e intereses del Gobierno nacional central: suma de 4 trimestres completos sobre el PIB nominal de esos trimestres.", "Central government revenue, spending and interest: sum of 4 complete quarters over nominal GDP for those quarters.")),
    "g-fi-balance": (("Banco de la República (balance fiscal de caja, empalme DNP–MinHacienda); DANE (PIB nominal)", "Banco de la República (cash fiscal balance, DNP–MinHacienda splice); DANE (nominal GDP)"), ("Balance total = déficit/superávit de caja; primario = balance total + intereses.", "Total balance = cash deficit/surplus; primary = total balance + interest.")),
    "g-fi-deuda": (("Banco de la República (deuda bruta del GNC, % del PIB)", "Banco de la República (central government gross debt, % of GDP)"), ("Saldo anual; en naranja los años por encima de 60% del PIB.", "Annual balance; orange for years above 60% of GDP.")),
    "g-fi-financiamiento": (("Banco de la República (balance fiscal de caja, empalme DNP–MinHacienda); DANE (PIB nominal)", "Banco de la República (cash fiscal balance, DNP–MinHacienda splice); DANE (nominal GDP)"), ("Financiamiento interno y externo, suma de 4 trimestres sobre el PIB; intereses sobre ingresos de los mismos 4 trimestres.", "Domestic and external financing, 4-quarter sum over GDP; interest over revenue for the same 4 quarters.")),
}


def ficha(gid: str, lang: str) -> tuple[str, str] | None:
    f = FICHAS.get(gid)
    if not f:
        return None
    k = 0 if lang == "es" else 1
    return f[0][k], f[1][k]
