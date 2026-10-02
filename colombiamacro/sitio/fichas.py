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
}


def ficha(gid: str, lang: str) -> tuple[str, str] | None:
    f = FICHAS.get(gid)
    if not f:
        return None
    k = 0 if lang == "es" else 1
    return f[0][k], f[1][k]
