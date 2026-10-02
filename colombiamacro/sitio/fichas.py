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

}


def ficha(gid: str, lang: str) -> tuple[str, str] | None:
    f = FICHAS.get(gid)
    if not f:
        return None
    k = 0 if lang == "es" else 1
    return f[0][k], f[1][k]
