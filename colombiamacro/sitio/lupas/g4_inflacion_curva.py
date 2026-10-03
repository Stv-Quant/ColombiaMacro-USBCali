"""Lupas (explicaciones ampliadas) del grupo g4: página Inflación (IPC total, grupos de precios, expectativas
implícitas en los TES, divisiones, durabilidad, difusión, ingresos y ciudades) y página Curva TES (explorador de la
curva cero cupón, factores, curva invertida, movimientos, Fisher, prima sobre la tasa del Banco y volatilidad).

Cada entrada describe el gráfico tal como lo construyen construir.py (Graficos.inflacion, componentes_barras,
componentes_lineas, expectativas, trayectoria_inflacion, anclaje), app.js (curvaTES), inflacion_extra.py,
curva_extra.py y analitica.py (tabla_tasas). Solo hechos y métodos: sin cifras ni fechas que caduquen.
"""

LUPAS = {
    # =========================================================================================== CURVA TES
    "g-curva-tes": {
        "es": {
            "que": "Muestra la curva de rendimientos de los TES (Títulos de Tesorería, los bonos con que el Gobierno nacional se financia en pesos): la tasa que el mercado exige para prestarle al Gobierno a 1, 5 y 10 años. Son tasas cero cupón, es decir, de un pago único al vencimiento, que el Banco de la República estima cada día con el modelo de Nelson y Siegel a partir de las operaciones del SEN y del MEC. La forma de la curva resume cómo el mercado valora el dinero en el tiempo.",
            "leer": "Eje horizontal: plazo (1, 5 y 10 años); eje vertical: tasa efectiva anual en %. La línea azul gruesa, con su valor rotulado sobre cada punto, es la curva del día elegido (por defecto, el último dato). Las líneas finas de colores son la curva al cierre de los años marcados (último día hábil de cada año; por defecto, los dos últimos años completos), que se activan o quitan con los botones de años. El selector cambia entre TES en pesos (tasa nominal) y TES en UVR (tasa real); el deslizador y el gráfico de historia cambian la fecha. La escala vertical se fija con el mínimo y el máximo de toda la historia para que las fechas sean comparables.",
            "importa": "La curva TES es la referencia con la que se valoran los demás activos en pesos: crédito, bonos corporativos, valoración de empresas y cualquier flujo de caja que se descuente a una tasa. Su nivel refleja el costo de financiación del Gobierno y la postura monetaria; su pendiente, cómo el mercado reparte en el tiempo la remuneración por plazo, inflación y riesgo.",
            "interpretar": [
                "Curva normal (creciente): los plazos largos pagan más que los cortos. El tablero la llama normal si la pendiente 10 − 1 años supera 0,3 pp, plana entre 0 y 0,3 pp e invertida si es negativa.",
                "Si la curva del día queda por encima de la de un cierre anterior, el costo de endeudarse en pesos subió en todos los plazos; si cambia la inclinación, el movimiento fue distinto en el corto y en el largo plazo.",
                "Una curva que baja de izquierda a derecha suele leerse como señal de tasas de política más bajas en el futuro, pero la pendiente también contiene la prima por plazo, que varía con el riesgo y la liquidez.",
                "Al pasar el cursor, cada punto muestra su cambio frente al dato más cercano a 365 días antes (si existe uno a menos de 20 días).",
                "Son tasas estimadas por un modelo, no precios de bonos individuales: en días de poca negociación pueden reflejar pocas operaciones."
            ],
            "formulas": [
                ["Precio de un bono cero cupón", "P = 100 ÷ (1 + y<sub>n</sub>)<sup>n</sup>", "y<sub>n</sub> = tasa cero cupón efectiva anual al plazo n (en años); P = precio por cada 100 pagados al vencimiento"],
                ["Pendiente", "S<sub>t</sub> = y<sub>10,t</sub> − y<sub>1,t</sub>", "y<sub>10</sub>, y<sub>1</sub> = tasas a 10 y 1 año del día t, en pp"],
                ["Cambio frente a hace un año", "Δy<sub>n</sub> = y<sub>n,t</sub> − y<sub>n,t−365d</sub>", "t−365d = dato disponible más cercano a 365 días antes, en pp"]
            ]
        },
        "en": {
            "que": "Shows the TES yield curve (TES are Treasury Securities, the bonds the national Government uses to borrow in pesos): the rate the market demands to lend to the Government at 1, 5 and 10 years. These are zero-coupon rates, i.e. for a single payment at maturity, estimated daily by the Banco de la República with the Nelson-Siegel model from trades on SEN and MEC. The shape of the curve summarises how the market prices money over time.",
            "leer": "Horizontal axis: maturity (1, 5 and 10 years); vertical axis: effective annual yield in %. The thick blue line, with its value labelled above each point, is the curve on the selected date (by default the latest). The thin coloured lines are the curve at the close of the ticked years (last business day of each year; by default the two latest complete years), toggled with the year buttons. The selector switches between peso TES (nominal yield) and UVR TES (real yield); the slider and the history chart change the date. The vertical scale is fixed at the full-history minimum and maximum so dates are comparable.",
            "importa": "The TES curve is the benchmark against which other peso assets are valued: loans, corporate bonds, company valuations and any cash flow discounted at a rate. Its level reflects the Government's funding cost and the monetary stance; its slope shows how the market spreads compensation for time, inflation and risk across maturities.",
            "interpretar": [
                "Normal (upward) curve: long maturities pay more than short ones. The dashboard calls it normal when the 10 − 1 year slope exceeds 0.3 pp, flat between 0 and 0.3 pp and inverted when negative.",
                "If the current curve sits above a past year-end curve, peso borrowing costs rose at all maturities; a change in tilt means the short and long ends moved differently.",
                "A downward-sloping curve is often read as a sign of lower policy rates ahead, but the slope also carries the term premium, which varies with risk and liquidity.",
                "On hover, each point shows its change against the observation closest to 365 days earlier (if one exists within 20 days).",
                "These are model-estimated rates, not prices of individual bonds: on thin trading days they may rest on few transactions."
            ],
            "formulas": [
                ["Zero-coupon bond price", "P = 100 ÷ (1 + y<sub>n</sub>)<sup>n</sup>", "y<sub>n</sub> = effective annual zero-coupon rate at maturity n (years); P = price per 100 paid at maturity"],
                ["Slope", "S<sub>t</sub> = y<sub>10,t</sub> − y<sub>1,t</sub>", "y<sub>10</sub>, y<sub>1</sub> = 10- and 1-year rates on day t, in pp"],
                ["Change versus a year ago", "Δy<sub>n</sub> = y<sub>n,t</sub> − y<sub>n,t−365d</sub>", "t−365d = available observation closest to 365 days earlier, in pp"]
            ]
        },
    },
    "g-curva-hist": {
        "es": {
            "que": "Recorre la historia diaria de las tasas cero cupón de los TES a 1, 5 y 10 años desde 2003. Permite ver los grandes ciclos de tasas en Colombia: periodos de alzas y recortes de la tasa del Banco de la República, episodios de tensión en los mercados y fases en que los plazos largos y cortos se acercan o se separan. Además sirve de control: cada fecha de esta historia alimenta la curva del gráfico vecino.",
            "leer": "Eje horizontal: fecha (datos diarios); eje vertical: tasa efectiva anual en %. Tres líneas en tonos de azul: la más clara es el plazo de 1 año, la intermedia el de 5 años y la más oscura y gruesa el de 10 años. Al pasar el cursor se ven las tres tasas del día y la curva vecina se redibuja para esa fecha; un clic la fija (la línea vertical pasa de punteada negra a continua roja) y otro clic la suelta. El selector pesos/UVR cambia ambas gráficas.",
            "importa": "Ver los tres plazos juntos distingue los movimientos de la política monetaria, que dominan el corto plazo, de los cambios en la percepción de riesgo fiscal e inflación, que pesan más en el largo plazo. Para un inversionista es la forma más directa de ubicar el nivel actual de tasas frente a su propia historia y de identificar episodios comparables.",
            "interpretar": [
                "Si la línea clara (1 año) se mueve mucho más que la oscura (10 años), el movimiento viene de la política monetaria; si las tres se desplazan juntas, cambió el nivel general de las tasas.",
                "Cuando la línea clara cruza por encima de la oscura, la curva se invierte; los episodios se detallan en el gráfico «Pendiente y episodios de curva invertida».",
                "En la vista UVR las tasas son reales (por encima de la inflación) y por eso son más bajas; la diferencia con la vista en pesos se analiza en la sección de compensación por inflación.",
                "Los saltos aislados de un día que se revierten (más de 2 pp) se ocultan en los cálculos derivados; la serie diaria puede tener días sin dato por feriados o falta de operaciones."
            ],
            "formulas": [
                ["Tasa cero cupón", "y<sub>n</sub> = (100 ÷ P<sub>n</sub>)<sup>1/n</sup> − 1", "P<sub>n</sub> = precio de un pago de 100 dentro de n años implícito en la curva estimada; n = 1, 5 o 10"]
            ]
        },
        "en": {
            "que": "Traces the daily history of TES zero-coupon yields at 1, 5 and 10 years since 2003. It reveals Colombia's major interest-rate cycles: periods of Banco de la República hikes and cuts, episodes of market stress and phases when short and long maturities converge or diverge. It also works as a control: each date in this history feeds the curve in the neighbouring chart.",
            "leer": "Horizontal axis: date (daily data); vertical axis: effective annual yield in %. Three lines in shades of blue: the lightest is the 1-year, the middle one the 5-year and the darkest, thickest one the 10-year. Hovering shows the three yields for that day and redraws the neighbouring curve for that date; a click pins it (the vertical line turns from dotted black to solid red) and another click releases it. The pesos/UVR selector changes both charts.",
            "importa": "Seeing the three maturities together separates monetary-policy moves, which dominate the short end, from changes in perceived fiscal and inflation risk, which weigh more on the long end. For an investor it is the most direct way to place today's rates against their own history and to spot comparable episodes.",
            "interpretar": [
                "If the light line (1 year) moves much more than the dark one (10 years), the move comes from monetary policy; if all three shift together, the general level of rates changed.",
                "When the light line crosses above the dark one, the curve inverts; the episodes are detailed in the chart 'Slope and inverted-curve episodes'.",
                "In the UVR view yields are real (above inflation) and therefore lower; the gap with the peso view is analysed in the inflation-compensation section.",
                "Isolated one-day jumps that reverse (over 2 pp) are hidden in derived calculations; the daily series may skip days due to holidays or lack of trades."
            ],
            "formulas": [
                ["Zero-coupon rate", "y<sub>n</sub> = (100 ÷ P<sub>n</sub>)<sup>1/n</sup> − 1", "P<sub>n</sub> = price of a payment of 100 in n years implied by the estimated curve; n = 1, 5 or 10"]
            ]
        },
    },
    "g-cv-factores": {
        "es": {
            "que": "Resume toda la curva de TES en pesos en tres números: el nivel (qué tan altas están las tasas en general), la pendiente (cuánto más pagan los plazos largos que los cortos) y la curvatura (si la parte media de la curva está arqueada hacia arriba o hacia abajo). La literatura (Litterman y Scheinkman, 1991) muestra que estos tres factores explican casi todo el movimiento de una curva de rendimientos.",
            "leer": "Eje horizontal: fecha, desde 2003; eje vertical en % para el nivel y en puntos porcentuales (pp) para la pendiente y la curvatura, todos en la misma escala. Línea azul gruesa: nivel; línea naranja: pendiente; línea verde: curvatura. La línea horizontal en cero sirve de referencia para la pendiente y la curvatura. Serie semanal: último dato disponible de cada viernes, calculado con las tasas cero cupón en pesos a 1, 5 y 10 años.",
            "importa": "Separar nivel, pendiente y curvatura permite entender qué tipo de movimiento tuvo la curva: un cambio general del costo del dinero, una reacción a la política monetaria que mueve sobre todo el corto plazo o un cambio en la prima que se exige por los plazos largos. Es el lenguaje con que los administradores de portafolios de renta fija miden y cubren su exposición.",
            "interpretar": [
                "Nivel al alza: todas las tasas suben (los precios de los TES caen); a la baja, se abaratan las condiciones de financiación en pesos.",
                "Pendiente positiva y amplia: curva empinada, con plazos largos que pagan mucho más que los cortos; cerca de cero o negativa: curva plana o invertida.",
                "Curvatura positiva: el plazo de 5 años está alto frente al promedio de 1 y 10 años; negativa: la parte media está hundida.",
                "Son medidas simples con tres plazos, no factores estimados estadísticamente; el tramo medio de la curva solo se representa con el plazo de 5 años."
            ],
            "formulas": [
                ["Nivel", "N<sub>t</sub> = (y<sub>1</sub> + y<sub>5</sub> + y<sub>10</sub>) ÷ 3", "y<sub>n</sub> = tasa cero cupón en pesos a n años (%)"],
                ["Pendiente", "S<sub>t</sub> = y<sub>10</sub> − y<sub>1</sub>", "en pp"],
                ["Curvatura", "C<sub>t</sub> = 2 × y<sub>5</sub> − y<sub>1</sub> − y<sub>10</sub>", "en pp; positiva si el plazo de 5 años está por encima del promedio de los extremos"]
            ]
        },
        "en": {
            "que": "Summarises the whole peso TES curve in three numbers: the level (how high rates are overall), the slope (how much more long maturities pay than short ones) and the curvature (whether the middle of the curve bends up or down). The literature (Litterman and Scheinkman, 1991) shows that these three factors explain almost all of a yield curve's movements.",
            "leer": "Horizontal axis: date, since 2003; vertical axis in % for the level and in percentage points (pp) for slope and curvature, all on the same scale. Thick blue line: level; orange line: slope; green line: curvature. The horizontal line at zero is the reference for slope and curvature. Weekly series: last available value each Friday, computed from the 1-, 5- and 10-year peso zero-coupon rates.",
            "importa": "Splitting level, slope and curvature shows what kind of move the curve made: a general change in the cost of money, a reaction to monetary policy that mostly moves the short end, or a change in the premium demanded for long maturities. It is the language fixed-income portfolio managers use to measure and hedge their exposure.",
            "interpretar": [
                "Rising level: all yields go up (TES prices fall); falling level: peso funding conditions ease.",
                "Large positive slope: a steep curve, with long maturities paying much more than short ones; near zero or negative: a flat or inverted curve.",
                "Positive curvature: the 5-year rate is high relative to the average of the 1- and 10-year; negative: the belly is depressed.",
                "These are simple three-point measures, not statistically estimated factors; the belly is represented only by the 5-year rate."
            ],
            "formulas": [
                ["Level", "N<sub>t</sub> = (y<sub>1</sub> + y<sub>5</sub> + y<sub>10</sub>) ÷ 3", "y<sub>n</sub> = peso zero-coupon rate at n years (%)"],
                ["Slope", "S<sub>t</sub> = y<sub>10</sub> − y<sub>1</sub>", "in pp"],
                ["Curvature", "C<sub>t</sub> = 2 × y<sub>5</sub> − y<sub>1</sub> − y<sub>10</sub>", "in pp; positive when the 5-year rate is above the average of the two ends"]
            ]
        },
    },
    "g-cv-invertida": {
        "es": {
            "que": "Sigue la pendiente de la curva de TES en pesos, la diferencia entre la tasa a 10 años y la tasa a 1 año, y marca los periodos en que fue negativa, es decir, en que la curva estuvo invertida: prestarle al Gobierno a un año pagaba más que hacerlo a diez. Las inversiones suelen coincidir con fases de política monetaria restrictiva, cuando la tasa del Banco de la República está alta frente a lo que el mercado considera sostenible.",
            "leer": "Eje horizontal: fecha, desde 2003; eje vertical: pendiente en puntos porcentuales (pp). La línea naranja es la pendiente semanal (último dato de cada viernes) y la línea horizontal marca el cero. Las franjas naranjas sombreadas señalan los episodios de curva invertida, identificados con datos diarios: tramos de al menos 5 días hábiles seguidos con pendiente negativa. Debajo del gráfico, una tabla lista cada episodio con sus fechas, duración, pendiente mínima y la tasa del Banco al inicio.",
            "importa": "La pendiente es uno de los indicadores más seguidos de la estructura de tasas: la literatura (Estrella y Hardouvelis, 1991) documenta su contenido informativo sobre la actividad económica. Una curva invertida indica que el mercado exige más por el corto plazo que por el largo, algo que afecta el margen de los bancos (que se fondean a corto y prestan a largo) y las decisiones de financiación de empresas y Gobierno.",
            "interpretar": [
                "Pendiente positiva y creciente: la curva se empina; cerca de cero: curva plana; bajo cero: curva invertida (franja sombreada).",
                "Una inversión breve puede deberse a un movimiento puntual del plazo de 1 año; los episodios largos y profundos son los relevantes, por eso se exige un mínimo de 5 días hábiles.",
                "Conviene leerla junto con la tasa del Banco (gráfico «TES frente a la tasa del Banco»): las inversiones suelen aparecer cuando la tasa de política está en niveles altos.",
                "La relación entre curva invertida y desaceleración documentada en otros países no es mecánica; en Colombia también influyen la prima por plazo, el riesgo fiscal y los flujos de inversionistas extranjeros."
            ],
            "formulas": [
                ["Pendiente", "S<sub>t</sub> = y<sub>10,t</sub> − y<sub>1,t</sub>", "y<sub>10</sub>, y<sub>1</sub> = tasas cero cupón en pesos a 10 y 1 año, en pp"],
                ["Episodio invertido", "S<sub>d</sub> < 0 durante k ≥ 5 días hábiles consecutivos", "d = día hábil con dato; k = longitud del tramo"]
            ]
        },
        "en": {
            "que": "Tracks the slope of the peso TES curve, the difference between the 10-year and the 1-year rate, and marks the periods when it was negative, i.e. when the curve was inverted: lending to the Government for one year paid more than lending for ten. Inversions tend to coincide with tight monetary policy, when the Banco de la República rate is high relative to what the market sees as sustainable.",
            "leer": "Horizontal axis: date, since 2003; vertical axis: slope in percentage points (pp). The orange line is the weekly slope (last value each Friday) and the horizontal line marks zero. The shaded orange bands mark inverted-curve episodes, identified on daily data: runs of at least 5 consecutive business days with a negative slope. Below the chart, a table lists each episode with its dates, length, lowest slope and the policy rate at the start.",
            "importa": "The slope is one of the most closely watched features of the rate structure: the literature (Estrella and Hardouvelis, 1991) documents its information content about economic activity. An inverted curve means the market demands more for the short term than the long term, which squeezes bank margins (banks fund short and lend long) and shapes the financing choices of companies and the Government.",
            "interpretar": [
                "Positive and rising slope: the curve steepens; near zero: a flat curve; below zero: an inverted curve (shaded band).",
                "A brief inversion may come from a one-off move in the 1-year rate; long, deep episodes are the relevant ones, hence the 5-business-day minimum.",
                "Read it together with the policy rate (chart 'TES versus the policy rate'): inversions tend to appear when the policy rate is high.",
                "The link between inversion and slowdown documented in other countries is not mechanical; in Colombia the term premium, fiscal risk and foreign investor flows also matter."
            ],
            "formulas": [
                ["Slope", "S<sub>t</sub> = y<sub>10,t</sub> − y<sub>1,t</sub>", "y<sub>10</sub>, y<sub>1</sub> = 10- and 1-year peso zero-coupon rates, in pp"],
                ["Inverted episode", "S<sub>d</sub> < 0 for k ≥ 5 consecutive business days", "d = business day with data; k = length of the run"]
            ]
        },
    },
    "g-cv-cambios": {
        "es": {
            "que": "Muestra cuánto se movió la tasa cero cupón de los TES en pesos en cada plazo (1, 5 y 10 años) durante el último mes, los últimos tres meses y el último año. Permite ver de un vistazo si las tasas subieron o bajaron y si el movimiento fue parejo a lo largo de la curva o se concentró en el corto o en el largo plazo.",
            "leer": "Eje horizontal: plazo (1, 5 y 10 años); eje vertical: cambio en puntos básicos (pb; 100 pb = 1 punto porcentual). Para cada plazo hay tres barras: verde para el cambio en 1 mes, azul para 3 meses y naranja para 12 meses, con su valor rotulado. La línea horizontal marca el cero: las barras hacia arriba indican alzas de tasa y hacia abajo, bajas. La comparación se hace contra el último día hábil disponible en o antes de la fecha de hace 1, 3 y 12 meses.",
            "importa": "Los cambios de tasas determinan la rentabilidad de quien tiene TES: cuando la tasa sube, el precio del bono cae, y la caída es mayor cuanto más largo es el plazo. Además, el patrón por plazos revela la causa probable del movimiento (política monetaria, inflación o riesgo), información útil para gestionar la duración de un portafolio y el costo de financiación de empresas y Gobierno.",
            "interpretar": [
                "Alza con empinamiento: las tasas suben más en el largo plazo; alza con aplanamiento: suben más en el corto. Las bajas se leen igual en sentido contrario.",
                "Si las barras de 1 mes y de 12 meses tienen signos distintos, el movimiento reciente va en contra de la tendencia del año.",
                "Como referencia, la sensibilidad del precio de un bono cero cupón es aproximadamente su plazo: un alza de 100 pb a 10 años reduce su precio cerca de 10%.",
                "Son diferencias entre dos días puntuales: un dato atípico en cualquiera de las dos fechas altera el resultado."
            ],
            "formulas": [
                ["Cambio en pb", "Δ<sub>h</sub>y<sub>n</sub> = (y<sub>n,t</sub> − y<sub>n,t−h</sub>) × 100", "y<sub>n,t</sub> = tasa en pesos a n años del último día (%); t−h = último día hábil en o antes de hace h = 1, 3 o 12 meses"],
                ["Efecto aproximado en precio", "ΔP ÷ P ≈ −D × Δy", "D = duración modificada (≈ n ÷ (1 + y) en un cero cupón); Δy en tanto por uno"]
            ]
        },
        "en": {
            "que": "Shows how much the peso TES zero-coupon rate moved at each maturity (1, 5 and 10 years) over the last month, the last three months and the last year. It shows at a glance whether rates rose or fell and whether the move was even along the curve or concentrated at the short or long end.",
            "leer": "Horizontal axis: maturity (1, 5 and 10 years); vertical axis: change in basis points (bp; 100 bp = 1 percentage point). Each maturity has three bars: green for the 1-month change, blue for 3 months and orange for 12 months, with their values labelled. The horizontal line marks zero: bars pointing up are rate increases and bars pointing down are declines. The comparison is against the last business day available on or before the date 1, 3 and 12 months earlier.",
            "importa": "Rate changes drive returns for TES holders: when the yield rises the bond price falls, and the fall is larger the longer the maturity. The pattern across maturities also points to the likely cause of the move (monetary policy, inflation or risk), useful for managing portfolio duration and for gauging corporate and Government funding costs.",
            "interpretar": [
                "Bear steepening: yields rise more at the long end; bear flattening: they rise more at the short end. Declines read the same way in reverse (bull steepening/flattening).",
                "If the 1-month and 12-month bars have opposite signs, the recent move runs against the year's trend.",
                "As a benchmark, a zero-coupon bond's price sensitivity is roughly its maturity: a 100 bp rise at 10 years cuts its price by about 10%.",
                "These are differences between two single days: an outlier on either date distorts the result."
            ],
            "formulas": [
                ["Change in bp", "Δ<sub>h</sub>y<sub>n</sub> = (y<sub>n,t</sub> − y<sub>n,t−h</sub>) × 100", "y<sub>n,t</sub> = n-year peso rate on the latest day (%); t−h = last business day on or before h = 1, 3 or 12 months earlier"],
                ["Approximate price effect", "ΔP ÷ P ≈ −D × Δy", "D = modified duration (≈ n ÷ (1 + y) for a zero-coupon bond); Δy in decimal form"]
            ]
        },
    },
    "g-cv-descomposicion": {
        "es": {
            "que": "Separa el cambio de las tasas de los TES en pesos durante el último año en dos partes: la que vino de la tasa real, medida con los TES en UVR (Unidad de Valor Real, una unidad de cuenta que se ajusta con la inflación), y la que vino de la diferencia entre la tasa nominal y la real, que aproxima la compensación por inflación. Responde si las tasas se movieron porque cambió el costo real del dinero o porque cambió la inflación que el mercado incorpora.",
            "leer": "Eje horizontal: plazo (1, 5 y 10 años); eje vertical: cambio en 12 meses en puntos básicos (pb). Las barras están apiladas: azul, cambio de la tasa real (TES UVR); amarillo, cambio de la diferencia nominal − real. Sobre cada plazo, el rótulo «Total» indica el cambio de la tasa en pesos, que es la suma de las dos barras. Las barras por debajo de cero restan; la línea horizontal marca el cero. La comparación es contra el último día hábil disponible hace 12 meses.",
            "importa": "Un alza de tasas nominales por mayor inflación esperada tiene implicaciones distintas que un alza de la tasa real: la primera afecta el poder adquisitivo y la credibilidad de la meta de inflación; la segunda endurece las condiciones financieras de verdad, encarece la inversión y suele asociarse a política monetaria o a primas de riesgo. Esta distinción es clave para leer la curva más allá de su nivel.",
            "interpretar": [
                "Barra azul dominante: el movimiento vino de la tasa real (política monetaria, riesgo país, demanda de bonos); barra amarilla dominante: vino de la compensación por inflación.",
                "Barras de signo opuesto indican que la tasa real y la compensación se compensaron parcialmente; el «Total» muestra el efecto neto.",
                "La diferencia nominal − real es una aproximación lineal de la compensación de Fisher; para la cifra exacta ver el gráfico «Nominal = real + compensación por inflación».",
                "La compensación incluye primas por riesgo inflacionario y por liquidez (los TES UVR se negocian menos), así que no equivale a la inflación esperada pura."
            ],
            "formulas": [
                ["Descomposición", "Δy<sub>n</sub><sup>$</sup> = Δr<sub>n</sub> + Δ(y<sub>n</sub><sup>$</sup> − r<sub>n</sub>)", "y<sup>$</sup> = tasa TES en pesos; r = tasa TES en UVR; Δ = cambio en 12 meses, en pb"],
                ["Brecha nominal − real", "B<sub>n</sub> = y<sub>n</sub><sup>$</sup> − r<sub>n</sub>", "n = 1, 5 o 10 años; aproximación de la compensación por inflación"]
            ]
        },
        "en": {
            "que": "Splits the 12-month change in peso TES yields into two parts: the part that came from the real rate, measured with UVR TES (UVR, the Real Value Unit, is a unit of account indexed to inflation), and the part that came from the gap between the nominal and the real rate, which approximates inflation compensation. It answers whether yields moved because the real cost of money changed or because the inflation priced by the market changed.",
            "leer": "Horizontal axis: maturity (1, 5 and 10 years); vertical axis: 12-month change in basis points (bp). Bars are stacked: blue is the change in the real rate (UVR TES); yellow is the change in the nominal − real gap. Above each maturity, the 'Total' label gives the change in the peso yield, which is the sum of the two bars. Bars below zero subtract; the horizontal line marks zero. The comparison is against the last business day available 12 months earlier.",
            "importa": "A rise in nominal yields driven by higher priced inflation has different implications from a rise in the real rate: the former bears on purchasing power and the credibility of the inflation target; the latter genuinely tightens financial conditions, makes investment more expensive and is usually tied to monetary policy or risk premia. This distinction is key to reading the curve beyond its level.",
            "interpretar": [
                "Blue bar dominant: the move came from the real rate (monetary policy, country risk, demand for bonds); yellow bar dominant: it came from inflation compensation.",
                "Bars with opposite signs mean the real rate and compensation partly offset each other; 'Total' shows the net effect.",
                "The nominal − real gap is a linear approximation of Fisher compensation; for the exact figure see the chart 'Nominal = real + inflation compensation'.",
                "Compensation includes inflation-risk and liquidity premia (UVR TES trade less), so it is not pure expected inflation."
            ],
            "formulas": [
                ["Decomposition", "Δy<sub>n</sub><sup>$</sup> = Δr<sub>n</sub> + Δ(y<sub>n</sub><sup>$</sup> − r<sub>n</sub>)", "y<sup>$</sup> = peso TES yield; r = UVR TES yield; Δ = 12-month change, in bp"],
                ["Nominal − real gap", "B<sub>n</sub> = y<sub>n</sub><sup>$</sup> − r<sub>n</sub>", "n = 1, 5 or 10 years; approximation of inflation compensation"]
            ]
        },
    },
    "g-cv-fisher": {
        "es": {
            "que": "Descompone la tasa de los TES en pesos del último día en sus dos componentes según la ecuación de Fisher: la tasa real, que pagan los TES en UVR por encima de la inflación, y lo que falta para llegar a la tasa nominal, que es la compensación que el mercado exige por la inflación (más primas por riesgo y liquidez). Se presenta para los plazos de 1, 5 y 10 años.",
            "leer": "Eje horizontal: plazo (1, 5 y 10 años); eje vertical: tasa en %, empezando en cero. Cada barra apilada tiene una parte azul, la tasa real del TES UVR (rotulada en %), y una parte amarilla, la diferencia hasta la tasa del TES en pesos (rotulada en pp). El número sobre cada barra es la tasa nominal en pesos. Al pasar el cursor por la parte amarilla aparece la compensación por inflación exacta de Fisher, que difiere levemente de la resta simple.",
            "importa": "Un inversionista que compra TES en pesos asume el riesgo de inflación; uno que compra TES UVR, no. Comparar ambas tasas muestra cuánta inflación tendría que ocurrir para que las dos inversiones rindan igual, una referencia para elegir entre instrumentos nominales e indexados y para evaluar la credibilidad de la meta de inflación del 3% del Banco de la República.",
            "interpretar": [
                "Parte amarilla grande frente a la meta de 3%: el mercado incorpora inflación alta o exige una prima elevada por el riesgo inflacionario.",
                "Si la parte amarilla crece con el plazo, la compensación por inflación es mayor a largo plazo; si se reduce, el mercado incorpora inflación decreciente.",
                "La parte azul alta indica condiciones financieras reales restrictivas: el dinero es caro aun descontando la inflación.",
                "El eje empieza en cero: en periodos en que alguna tasa real fue negativa, esa parte no se vería; la compensación incluye primas, por lo que no es la inflación esperada pura."
            ],
            "formulas": [
                ["Ecuación de Fisher", "(1 + y<sub>n</sub><sup>$</sup>) = (1 + r<sub>n</sub>) × (1 + π<sub>n</sub><sup>e</sup>)", "y<sup>$</sup> = tasa TES en pesos; r = tasa TES UVR; π<sup>e</sup> = compensación por inflación (todo en tanto por uno)"],
                ["Compensación exacta", "π<sub>n</sub><sup>e</sup> = (1 + y<sub>n</sub><sup>$</sup>) ÷ (1 + r<sub>n</sub>) − 1", "se muestra en el recuadro flotante"],
                ["Diferencia apilada", "B<sub>n</sub> = y<sub>n</sub><sup>$</sup> − r<sub>n</sub>", "altura de la parte amarilla, en pp; B ≈ π<sup>e</sup> para tasas bajas"]
            ]
        },
        "en": {
            "que": "Breaks the latest peso TES yield into its two components under the Fisher equation: the real rate, paid by UVR TES above inflation, and the remainder up to the nominal yield, which is the compensation the market demands for inflation (plus risk and liquidity premia). It is shown for the 1-, 5- and 10-year maturities.",
            "leer": "Horizontal axis: maturity (1, 5 and 10 years); vertical axis: yield in %, starting at zero. Each stacked bar has a blue part, the real UVR TES yield (labelled in %), and a yellow part, the gap up to the peso TES yield (labelled in pp). The number above each bar is the nominal peso yield. Hovering over the yellow part shows the exact Fisher inflation compensation, which differs slightly from the simple subtraction.",
            "importa": "An investor buying peso TES bears inflation risk; one buying UVR TES does not. Comparing both yields shows how much inflation would have to occur for the two investments to return the same, a benchmark for choosing between nominal and indexed instruments and for judging the credibility of the Banco de la República's 3% inflation target.",
            "interpretar": [
                "A large yellow part relative to the 3% target: the market prices high inflation or demands a large inflation-risk premium.",
                "If the yellow part grows with maturity, inflation compensation is higher at long horizons; if it shrinks, the market prices declining inflation.",
                "A tall blue part signals tight real financial conditions: money is expensive even after inflation.",
                "The axis starts at zero: in periods when a real yield was negative that part would not show; compensation includes premia, so it is not pure expected inflation."
            ],
            "formulas": [
                ["Fisher equation", "(1 + y<sub>n</sub><sup>$</sup>) = (1 + r<sub>n</sub>) × (1 + π<sub>n</sub><sup>e</sup>)", "y<sup>$</sup> = peso TES yield; r = UVR TES yield; π<sup>e</sup> = inflation compensation (all in decimal form)"],
                ["Exact compensation", "π<sub>n</sub><sup>e</sup> = (1 + y<sub>n</sub><sup>$</sup>) ÷ (1 + r<sub>n</sub>) − 1", "shown in the hover box"],
                ["Stacked gap", "B<sub>n</sub> = y<sub>n</sub><sup>$</sup> − r<sub>n</sub>", "height of the yellow part, in pp; B ≈ π<sup>e</sup> for low rates"]
            ]
        },
    },
    "g-cv-real": {
        "es": {
            "que": "Sigue en el tiempo los dos componentes de la tasa de los TES a 10 años: la tasa real que pagan los TES en UVR y la compensación por inflación implícita, que surge de comparar los TES en pesos con los TES UVR mediante la ecuación de Fisher. Muestra si el costo real del endeudamiento de largo plazo y la inflación que el mercado incorpora a diez años se han movido juntos o en direcciones distintas.",
            "leer": "Eje horizontal: fecha, desde 2003; eje vertical: % anual. Línea azul: tasa cero cupón del TES UVR a 10 años (tasa real). Línea amarilla: compensación por inflación a 10 años. La franja verde marca el rango meta del Banco de la República (2% a 4%) y la línea verde, la meta puntual de 3%: es la referencia para la línea amarilla. Serie semanal (último dato de cada viernes).",
            "importa": "La tasa real de largo plazo es el costo de financiación relevante para la inversión en infraestructura, vivienda y empresas, y una medida de la prima que se exige al riesgo soberano colombiano. La compensación por inflación a 10 años indica si el mercado confía en que la inflación converja a la meta en el largo plazo, un factor central de la credibilidad del Banco de la República.",
            "interpretar": [
                "Línea amarilla dentro de la franja verde: la compensación de largo plazo es coherente con la meta; por encima de 4%, el mercado incorpora inflación o primas de riesgo inflacionario elevadas.",
                "Si la línea azul sube mientras la amarilla se mantiene, el encarecimiento del crédito a largo plazo es real (riesgo fiscal, tasas globales o política monetaria), no inflacionario.",
                "La suma aproximada de ambas líneas da la tasa del TES en pesos a 10 años; la descomposición de los cambios recientes está en «¿Tasa real o inflación?».",
                "La compensación contiene primas por riesgo inflacionario y por liquidez de los TES UVR; el gráfico de la página de inflación «Inflación esperada a largo plazo» aísla el tramo de 5 a 10 años."
            ],
            "formulas": [
                ["Compensación por inflación a 10 años", "π<sub>10</sub> = [(1 + y<sub>10</sub><sup>$</sup>) ÷ (1 + r<sub>10</sub>) − 1] × 100", "y<sup>$</sup><sub>10</sub> = tasa cero cupón en pesos a 10 años; r<sub>10</sub> = tasa cero cupón UVR a 10 años (tanto por uno)"],
                ["Serie semanal", "x<sub>s</sub> = x<sub>d*</sub>", "d* = último día con dato de la semana que termina el viernes s"]
            ]
        },
        "en": {
            "que": "Tracks over time the two components of the 10-year TES yield: the real rate paid by UVR TES and implied inflation compensation, obtained by comparing peso TES with UVR TES through the Fisher equation. It shows whether the real cost of long-term borrowing and the inflation the market prices ten years out have moved together or apart.",
            "leer": "Horizontal axis: date, since 2003; vertical axis: % a year. Blue line: 10-year UVR TES zero-coupon yield (real rate). Yellow line: 10-year inflation compensation. The green band marks the Banco de la República target range (2% to 4%) and the green line the 3% point target: the benchmark for the yellow line. Weekly series (last value each Friday).",
            "importa": "The long-term real rate is the relevant funding cost for investment in infrastructure, housing and businesses, and a gauge of the premium demanded on Colombian sovereign risk. Ten-year inflation compensation shows whether the market trusts inflation to converge to target in the long run, a central element of the Banco de la República's credibility.",
            "interpretar": [
                "Yellow line inside the green band: long-run compensation is consistent with the target; above 4%, the market prices high inflation or high inflation-risk premia.",
                "If the blue line rises while the yellow one holds, the increase in long-term borrowing costs is real (fiscal risk, global rates or monetary policy), not inflationary.",
                "The two lines roughly add up to the 10-year peso TES yield; the breakdown of recent changes is in 'Real rate or inflation?'.",
                "Compensation contains inflation-risk and UVR-liquidity premia; the inflation page chart 'Long-term expected inflation' isolates the 5-to-10-year segment."
            ],
            "formulas": [
                ["10-year inflation compensation", "π<sub>10</sub> = [(1 + y<sub>10</sub><sup>$</sup>) ÷ (1 + r<sub>10</sub>) − 1] × 100", "y<sup>$</sup><sub>10</sub> = 10-year peso zero-coupon yield; r<sub>10</sub> = 10-year UVR zero-coupon yield (decimal form)"],
                ["Weekly series", "x<sub>s</sub> = x<sub>d*</sub>", "d* = last day with data in the week ending Friday s"]
            ]
        },
    },
    "g-cv-prima": {
        "es": {
            "que": "Compara las tasas de los TES en pesos a 1 y a 10 años con la tasa de política monetaria (TPM), la tasa con la que el Banco de la República presta liquidez a los bancos a un día. La diferencia indica cuánto más (o menos) que la tasa del Banco exige el mercado por prestarle al Gobierno a esos plazos, y refleja tanto lo que el mercado espera de la política monetaria como las primas por plazo y por riesgo.",
            "leer": "Eje horizontal: fecha, desde 2003; eje vertical: diferencia en puntos porcentuales (pp). Línea azul: TES a 10 años menos la TPM. Línea naranja: TES a 1 año menos la TPM. La línea horizontal marca el cero: por encima, el TES rinde más que la tasa del Banco; por debajo, menos. Se usa la TPM vigente cada día y la serie es semanal (último dato de cada viernes).",
            "importa": "La TPM es el ancla de corto plazo de todo el sistema de tasas; la distancia de los TES frente a ella mide cómo se transmite la política monetaria a los plazos largos, que son los que importan para el crédito hipotecario, la inversión y el costo de la deuda pública. Un diferencial amplio a 10 años encarece la financiación de largo plazo aun cuando el Banco recorta su tasa.",
            "interpretar": [
                "Diferencial de 1 año negativo: el mercado incorpora recortes de la TPM en los próximos meses; positivo: incorpora alzas o exige prima.",
                "Diferencial de 10 años alto y creciente: mayor prima por plazo o por riesgo fiscal, o expectativa de tasas más altas a largo plazo.",
                "Las dos líneas suelen caer cuando el Banco sube la TPM (el denominador común se mueve primero) y subir cuando la recorta; conviene leerlas junto con el gráfico de la tasa de política en la página de tasas.",
                "La TPM cambia en saltos discretos en las reuniones de la Junta Directiva, mientras los TES se mueven a diario; los cambios bruscos del diferencial suelen coincidir con esas decisiones."
            ],
            "formulas": [
                ["Diferencial frente a la TPM", "Sp<sub>n,t</sub> = y<sub>n,t</sub> − TPM<sub>t</sub>", "y<sub>n</sub> = tasa cero cupón en pesos a n = 1 o 10 años; TPM<sub>t</sub> = tasa de política vigente el día t; en pp"]
            ]
        },
        "en": {
            "que": "Compares 1- and 10-year peso TES yields with the monetary policy rate (TPM, its Spanish acronym), the rate at which the Banco de la República lends overnight liquidity to banks. The spread shows how much more (or less) than the policy rate the market demands to lend to the Government at those maturities, reflecting both expected monetary policy and term and risk premia.",
            "leer": "Horizontal axis: date, since 2003; vertical axis: spread in percentage points (pp). Blue line: 10-year TES minus the policy rate. Orange line: 1-year TES minus the policy rate. The horizontal line marks zero: above it, the TES yields more than the policy rate; below it, less. The policy rate in force each day is used and the series is weekly (last value each Friday).",
            "importa": "The policy rate is the short-term anchor of the entire rate system; the distance of TES from it measures how monetary policy passes through to long maturities, which matter for mortgages, investment and public debt costs. A wide 10-year spread keeps long-term funding expensive even when the Bank cuts its rate.",
            "interpretar": [
                "Negative 1-year spread: the market prices policy-rate cuts over the coming months; positive: it prices hikes or demands a premium.",
                "High and rising 10-year spread: a larger term or fiscal-risk premium, or expectations of higher long-term rates.",
                "Both lines tend to fall when the Bank hikes (the common benchmark moves first) and rise when it cuts; read them with the policy-rate chart on the rates page.",
                "The policy rate changes in discrete steps at Board meetings while TES move daily; sharp shifts in the spread usually coincide with those decisions."
            ],
            "formulas": [
                ["Spread over the policy rate", "Sp<sub>n,t</sub> = y<sub>n,t</sub> − TPM<sub>t</sub>", "y<sub>n</sub> = peso zero-coupon yield at n = 1 or 10 years; TPM<sub>t</sub> = policy rate in force on day t; in pp"]
            ]
        },
    },
    "g-cv-volatilidad": {
        "es": {
            "que": "Mide qué tan bruscos han sido los movimientos diarios de la tasa del TES a 10 años: es la desviación estándar de sus cambios diarios durante los últimos 60 días hábiles (unos tres meses), expresada en términos anuales. Sirve como termómetro del riesgo de mercado de la deuda pública colombiana y de la incertidumbre de los inversionistas.",
            "leer": "Eje horizontal: fecha, desde 2003; eje vertical: volatilidad anualizada en puntos básicos (pb). La línea morada es la volatilidad móvil de 60 días hábiles, mostrada semanalmente (último dato de cada viernes). La línea punteada gris horizontal es el promedio de toda la serie desde 2003, la referencia para saber si el mercado está más o menos agitado que lo habitual. Se exige un mínimo de 48 cambios diarios en la ventana para calcular cada punto.",
            "importa": "La volatilidad determina el riesgo de mantener TES: con mayor volatilidad, las pérdidas o ganancias de valoración en un periodo dado pueden ser mayores, lo que lleva a fondos y bancos a reducir posiciones o exigir más prima. Los picos suelen coincidir con choques globales, episodios de riesgo fiscal o salidas de inversionistas extranjeros, y afectan el costo de financiación del Gobierno.",
            "interpretar": [
                "Por encima de la línea punteada: el mercado de TES está más agitado que su promedio histórico; por debajo, más calmado.",
                "Un pico aislado indica un choque puntual; una volatilidad alta persistente refleja incertidumbre prolongada sobre inflación, política monetaria o finanzas públicas.",
                "Como orden de magnitud, una volatilidad anualizada de 100 pb equivale a una desviación diaria de unos 6 pb (100 ÷ √252).",
                "Es una medida histórica (mira hacia atrás) y reacciona con rezago; los saltos aislados de un día que se revierten se depuran antes del cálculo."
            ],
            "formulas": [
                ["Cambio diario", "Δy<sub>d</sub> = (y<sub>10,d</sub> − y<sub>10,d−1</sub>) × 100", "y<sub>10</sub> = tasa cero cupón en pesos a 10 años (%); en pb"],
                ["Volatilidad anualizada", "σ<sub>t</sub> = √252 × √[Σ (Δy<sub>d</sub> − Δȳ)<sup>2</sup> ÷ (k − 1)]", "suma sobre los k ≤ 60 últimos días hábiles (mínimo 48); Δȳ = promedio de esos cambios; 252 = días hábiles por año"]
            ]
        },
        "en": {
            "que": "Measures how abrupt the daily moves in the 10-year TES yield have been: it is the standard deviation of its daily changes over the last 60 business days (about three months), expressed in annual terms. It serves as a gauge of market risk in Colombian public debt and of investor uncertainty.",
            "leer": "Horizontal axis: date, since 2003; vertical axis: annualised volatility in basis points (bp). The purple line is the 60-business-day rolling volatility, shown weekly (last value each Friday). The grey dotted horizontal line is the average of the whole series since 2003, the benchmark for telling whether the market is more or less turbulent than usual. A minimum of 48 daily changes in the window is required for each point.",
            "importa": "Volatility determines the risk of holding TES: with higher volatility, mark-to-market gains or losses over a given period can be larger, leading funds and banks to cut positions or demand more premium. Spikes usually coincide with global shocks, fiscal-risk episodes or foreign investor outflows, and they affect the Government's funding cost.",
            "interpretar": [
                "Above the dotted line: the TES market is more turbulent than its historical average; below, calmer.",
                "An isolated spike signals a one-off shock; persistently high volatility reflects prolonged uncertainty about inflation, monetary policy or public finances.",
                "As an order of magnitude, an annualised volatility of 100 bp equals a daily standard deviation of about 6 bp (100 ÷ √252).",
                "It is a backward-looking measure and reacts with a lag; isolated one-day jumps that reverse are cleaned before the calculation."
            ],
            "formulas": [
                ["Daily change", "Δy<sub>d</sub> = (y<sub>10,d</sub> − y<sub>10,d−1</sub>) × 100", "y<sub>10</sub> = 10-year peso zero-coupon yield (%); in bp"],
                ["Annualised volatility", "σ<sub>t</sub> = √252 × √[Σ (Δy<sub>d</sub> − Δȳ)<sup>2</sup> ÷ (k − 1)]", "sum over the last k ≤ 60 business days (minimum 48); Δȳ = mean of those changes; 252 = business days per year"]
            ]
        },
    },
    # =========================================================================================== INFLACIÓN
    "g-inf": {
        "es": {
            "que": "Muestra la inflación anual de Colombia, medida con el Índice de Precios al Consumidor (IPC) del DANE, frente a la meta del Banco de la República, y la compara con la inflación de fondo, que excluye alimentos y precios regulados para aislar la presión persistente. Cuenta la historia de los ciclos de inflación: los choques que la alejan de la meta y el proceso de regreso.",
            "leer": "Panel superior, en % anual: línea azul gruesa, inflación total; línea naranja, inflación sin alimentos ni regulados (cálculo del Banco de la República). La franja verde es el rango meta (2% a 4%) y la línea verde, la meta puntual de 3%. Panel inferior: barras con el cambio de la inflación total frente al mismo mes del año anterior, en puntos porcentuales (pp); azules si subió y naranjas si bajó. La vista inicial abarca los últimos diez años; el recuadro flotante muestra el cambio anual de cada línea.",
            "importa": "La inflación erosiona el poder adquisitivo de salarios y ahorros, y es el objetivo principal del Banco de la República: cuando se aleja de la meta, el Banco ajusta su tasa de interés, lo que mueve el costo del crédito, la curva de TES y la tasa de cambio. Para un inversionista determina el rendimiento real de los activos en pesos y el ciclo de tasas.",
            "interpretar": [
                "Línea azul por encima de la franja: la inflación supera el rango meta; dentro de ella, es coherente con el objetivo del Banco.",
                "Si la línea naranja está por encima de la azul, la presión es de fondo (servicios, salarios, indexación) y suele ceder más despacio; si está por debajo, la inflación total la empujan alimentos o regulados.",
                "Varias barras naranjas seguidas en el panel inferior indican desinflación; barras azules seguidas, que la inflación se acelera.",
                "La inflación anual compara con el mismo mes del año anterior, de modo que un alza o una caída fuerte de hace doce meses produce efectos base cuando sale del cálculo."
            ],
            "formulas": [
                ["Inflación anual", "π<sub>t</sub> = (IPC<sub>t</sub> ÷ IPC<sub>t−12</sub> − 1) × 100", "IPC<sub>t</sub> = índice de precios al consumidor del mes t (base diciembre 2018 = 100)"],
                ["Cambio anual (panel inferior)", "Δπ<sub>t</sub> = π<sub>t</sub> − π<sub>t−12</sub>", "en pp"]
            ]
        },
        "en": {
            "que": "Shows Colombia's annual inflation, measured with DANE's Consumer Price Index (CPI), against the Banco de la República target, and compares it with underlying inflation, which excludes food and regulated prices to isolate persistent pressure. It tells the story of inflation cycles: the shocks that push it away from target and the path back.",
            "leer": "Top panel, in % a year: thick blue line, headline inflation; orange line, inflation excluding food and regulated prices (computed by the Banco de la República). The green band is the target range (2% to 4%) and the green line the 3% point target. Bottom panel: bars with the change in headline inflation versus the same month a year earlier, in percentage points (pp); blue when it rose and orange when it fell. The initial view covers the last ten years; the hover box shows each line's annual change.",
            "importa": "Inflation erodes the purchasing power of wages and savings and is the Banco de la República's main objective: when it drifts from target the Bank adjusts its policy rate, moving loan costs, the TES curve and the exchange rate. For an investor it sets the real return on peso assets and the rate cycle.",
            "interpretar": [
                "Blue line above the band: inflation exceeds the target range; inside it, it is consistent with the Bank's objective.",
                "If the orange line sits above the blue one, the pressure is underlying (services, wages, indexation) and tends to ease more slowly; if below, headline is being pushed by food or regulated prices.",
                "Several orange bars in a row in the bottom panel mean disinflation; several blue bars, that inflation is accelerating.",
                "Annual inflation compares with the same month a year earlier, so a sharp rise or fall twelve months ago creates base effects when it drops out of the calculation."
            ],
            "formulas": [
                ["Annual inflation", "π<sub>t</sub> = (CPI<sub>t</sub> ÷ CPI<sub>t−12</sub> − 1) × 100", "CPI<sub>t</sub> = consumer price index for month t (base December 2018 = 100)"],
                ["Annual change (bottom panel)", "Δπ<sub>t</sub> = π<sub>t</sub> − π<sub>t−12</sub>", "in pp"]
            ]
        },
    },
    "g-cp-barras": {
        "es": {
            "que": "Compara la inflación anual más reciente de los grandes grupos de precios que sigue el Banco de la República: alimentos, regulados (energía, gas, transporte, combustibles y otros precios fijados o supervisados por el Estado), todo menos alimentos, la inflación de fondo (sin alimentos ni regulados) y el total. Muestra qué parte de la canasta presiona más y cómo ha cambiado frente a un año antes.",
            "leer": "Barras horizontales ordenadas de menor a mayor, en % anual, con el valor rotulado al final. Las barras naranjas están por encima del techo del rango meta (4%) y las azules en o por debajo de él. La franja verde vertical marca el rango meta (2% a 4%). La raya vertical negra sobre cada barra es el dato del mismo grupo doce meses antes: si la barra termina a la derecha de la raya, la inflación del grupo aumentó en el año. Corresponde al último mes publicado.",
            "importa": "No toda la inflación responde igual a la política monetaria: alimentos y regulados dependen del clima, de los precios internacionales y de decisiones administrativas, mientras que la inflación de fondo refleja la demanda y la indexación de precios y salarios, que es lo que la tasa del Banco busca moderar. Saber qué grupo explica la inflación ayuda a evaluar su persistencia.",
            "interpretar": [
                "Si la inflación de fondo está en naranja, la presión no se limita a choques de oferta y suele tardar más en ceder.",
                "Alimentos o regulados muy por encima del total indican un choque concentrado; su efecto en la inflación anual tiende a reducirse cuando el choque cumple doce meses.",
                "Barra a la izquierda de su raya: el grupo se desinfló en el año; a la derecha, se aceleró.",
                "Los grupos se solapan (el total contiene a todos y «todo menos alimentos» contiene a regulados), por lo que no suman ni se promedian entre sí."
            ],
            "formulas": [
                ["Inflación anual del grupo", "π<sub>g,t</sub> = (I<sub>g,t</sub> ÷ I<sub>g,t−12</sub> − 1) × 100", "I<sub>g,t</sub> = índice de precios del grupo g en el último mes publicado t"],
                ["Raya de hace un año", "π<sub>g,t−12</sub>", "mismo cálculo doce meses antes"]
            ]
        },
        "en": {
            "que": "Compares the latest annual inflation of the main price groups tracked by the Banco de la República: food, regulated prices (energy, gas, transport, fuel and other prices set or supervised by the State), everything except food, underlying inflation (excluding food and regulated prices) and the headline. It shows which part of the basket is pushing hardest and how that has changed from a year earlier.",
            "leer": "Horizontal bars ordered from lowest to highest, in % a year, with the value labelled at the end. Orange bars are above the top of the target range (4%) and blue bars at or below it. The vertical green band marks the target range (2% to 4%). The black vertical tick on each bar is the same group's figure twelve months earlier: if the bar ends to the right of the tick, the group's inflation rose over the year. It refers to the latest published month.",
            "importa": "Not all inflation responds the same way to monetary policy: food and regulated prices depend on weather, international prices and administrative decisions, while underlying inflation reflects demand and the indexation of prices and wages, which is what the policy rate aims to restrain. Knowing which group drives inflation helps judge its persistence.",
            "interpretar": [
                "If underlying inflation is orange, the pressure is not limited to supply shocks and tends to take longer to ease.",
                "Food or regulated prices far above the headline signal a concentrated shock; its effect on annual inflation tends to fade once the shock is twelve months old.",
                "Bar left of its tick: the group disinflated over the year; right of it: it accelerated.",
                "The groups overlap (the headline contains all of them and 'all except food' contains regulated prices), so they neither add up nor average to each other."
            ],
            "formulas": [
                ["Group annual inflation", "π<sub>g,t</sub> = (I<sub>g,t</sub> ÷ I<sub>g,t−12</sub> − 1) × 100", "I<sub>g,t</sub> = price index of group g in the latest published month t"],
                ["Year-ago tick", "π<sub>g,t−12</sub>", "same calculation twelve months earlier"]
            ]
        },
    },
    "g-cp-lineas": {
        "es": {
            "que": "Sigue en el tiempo la inflación anual de tres grupos de precios: alimentos, regulados y la inflación de fondo (sin alimentos ni regulados). Permite ver cómo los choques de alimentos y de precios regulados suben y bajan con rapidez, mientras la inflación de fondo se mueve más despacio y refleja la presión persistente que el Banco de la República busca controlar con su tasa de interés.",
            "leer": "Eje horizontal: fecha; eje vertical: inflación anual en %. Línea naranja: alimentos; línea morada: regulados (servicios públicos, combustibles, transporte y otros precios fijados por el Estado); línea azul: inflación de fondo. La franja verde es el rango meta (2% a 4%) y la línea verde, la meta de 3%. Datos mensuales con vista inicial de los últimos diez años; el recuadro flotante muestra el valor de cada grupo y su cambio frente a un año antes en pp.",
            "importa": "Distinguir choques transitorios de presiones persistentes es central para leer las decisiones de política monetaria: el Banco puede tolerar un choque de alimentos que se revierte, pero responde con más fuerza cuando la inflación de fondo se aleja de la meta. Para un inversionista, la trayectoria de la línea azul es una guía sobre la persistencia de la inflación y del ciclo de tasas.",
            "interpretar": [
                "Picos de la línea naranja suelen asociarse a fenómenos climáticos (El Niño, La Niña) o a la tasa de cambio; tienden a revertirse en meses.",
                "La línea morada refleja ajustes de tarifas de energía, gas, combustibles y transporte, a veces decididos por el Gobierno y escalonados en el tiempo.",
                "Una línea azul que se mantiene por encima de 4% indica presión de fondo amplia; cuando gira a la baja, la desinflación es más sólida.",
                "Los choques en alimentos y regulados pueden contagiar a la inflación de fondo con rezago, por la indexación de salarios, arriendos y contratos a la inflación pasada."
            ],
            "formulas": [
                ["Inflación anual del grupo", "π<sub>g,t</sub> = (I<sub>g,t</sub> ÷ I<sub>g,t−12</sub> − 1) × 100", "I<sub>g,t</sub> = índice de precios del grupo g en el mes t"],
                ["Cambio anual (recuadro)", "Δπ<sub>g,t</sub> = π<sub>g,t</sub> − π<sub>g,t−12</sub>", "en pp"]
            ]
        },
        "en": {
            "que": "Tracks the annual inflation of three price groups over time: food, regulated prices and underlying inflation (excluding food and regulated prices). It shows how food and regulated-price shocks rise and fall quickly, while underlying inflation moves more slowly and reflects the persistent pressure the Banco de la República aims to control with its policy rate.",
            "leer": "Horizontal axis: date; vertical axis: annual inflation in %. Orange line: food; purple line: regulated prices (utilities, fuel, transport and other state-set prices); blue line: underlying inflation. The green band is the target range (2% to 4%) and the green line the 3% target. Monthly data with an initial view of the last ten years; the hover box shows each group's value and its change versus a year earlier in pp.",
            "importa": "Telling transitory shocks from persistent pressure is central to reading monetary policy: the Bank can look through a food shock that reverses, but responds more forcefully when underlying inflation drifts from target. For an investor, the path of the blue line is a guide to the persistence of inflation and of the rate cycle.",
            "interpretar": [
                "Spikes in the orange line are usually linked to weather events (El Niño, La Niña) or the exchange rate; they tend to reverse within months.",
                "The purple line reflects adjustments in energy, gas, fuel and transport tariffs, sometimes set by the Government and phased over time.",
                "A blue line staying above 4% signals broad underlying pressure; when it turns down, disinflation is more solid.",
                "Food and regulated-price shocks can spill into underlying inflation with a lag, through indexation of wages, rents and contracts to past inflation."
            ],
            "formulas": [
                ["Group annual inflation", "π<sub>g,t</sub> = (I<sub>g,t</sub> ÷ I<sub>g,t−12</sub> − 1) × 100", "I<sub>g,t</sub> = price index of group g in month t"],
                ["Annual change (hover)", "Δπ<sub>g,t</sub> = π<sub>g,t</sub> − π<sub>g,t−12</sub>", "in pp"]
            ]
        },
    },
    "g-espera": {
        "es": {
            "que": "Muestra la inflación que el mercado de deuda pública incorpora para los próximos doce meses (inflación de equilibrio o breakeven a 1 año) y la compara con la inflación observada. Se obtiene de los TES: la diferencia entre los que pagan una tasa fija en pesos y los que pagan una tasa real sobre la UVR, que se ajusta con la inflación. Es una medida diaria de expectativas basada en precios de mercado, no en encuestas.",
            "leer": "Panel superior, en % anual: línea morada, inflación esperada a 1 año (serie semanal, último dato de cada viernes); línea gris, inflación anual observada del IPC (mensual). La franja verde es el rango meta (2% a 4%) y la línea verde, la meta de 3%. Panel inferior: barras con el cambio de la inflación esperada a 1 año frente a un año antes, en pp; azules si subió y naranjas si bajó. La vista inicial abarca los últimos diez años.",
            "importa": "Las expectativas de inflación influyen en la fijación de salarios, arriendos y precios, y por eso el Banco de la República las sigue de cerca: si se alejan de la meta, la inflación tiende a volverse más persistente. Para un inversionista, comparar la expectativa con la inflación actual indica qué desinflación ya incorpora el mercado y sirve para elegir entre TES en pesos y TES UVR.",
            "interpretar": [
                "Línea morada por encima de la franja verde: el mercado incorpora una inflación superior al rango meta para el próximo año; dentro de ella, coherente con la meta.",
                "Línea morada por debajo de la gris: el mercado incorpora que la inflación será menor que la actual; por encima, mayor.",
                "La medida incluye una prima por riesgo inflacionario (la eleva) y una prima por la menor liquidez de los TES UVR (tiende a reducirla), así que no es la expectativa pura.",
                "El plazo de 1 año es sensible a datos mensuales de inflación y a la indexación de la UVR, que usa la inflación del mes anterior; conviene contrastarla con la Encuesta de Expectativas del Banco de la República."
            ],
            "formulas": [
                ["Breakeven a 1 año", "b<sub>1</sub> = [(1 + y<sub>1</sub><sup>$</sup>) ÷ (1 + r<sub>1</sub>) − 1] × 100", "y<sub>1</sub><sup>$</sup> = tasa cero cupón TES en pesos a 1 año; r<sub>1</sub> = tasa cero cupón TES UVR a 1 año (tanto por uno)"],
                ["Cambio anual (panel inferior)", "Δb<sub>1,t</sub> = b<sub>1,t</sub> − b<sub>1,t−1 año</sub>", "en pp"]
            ]
        },
        "en": {
            "que": "Shows the inflation the public-debt market prices for the next twelve months (the 1-year breakeven inflation rate) and compares it with actual inflation. It is derived from TES: the gap between those paying a fixed peso rate and those paying a real rate on the UVR, which is indexed to inflation. It is a daily, market-price-based measure of expectations, not a survey.",
            "leer": "Top panel, in % a year: purple line, 1-year expected inflation (weekly series, last value each Friday); grey line, actual annual CPI inflation (monthly). The green band is the target range (2% to 4%) and the green line the 3% target. Bottom panel: bars with the change in 1-year expected inflation versus a year earlier, in pp; blue when it rose and orange when it fell. The initial view covers the last ten years.",
            "importa": "Inflation expectations shape wage, rent and price setting, which is why the Banco de la República watches them closely: if they drift from target, inflation tends to become more persistent. For an investor, comparing expectations with current inflation shows how much disinflation the market already prices and helps choose between peso and UVR TES.",
            "interpretar": [
                "Purple line above the green band: the market prices inflation above the target range for the next year; inside it, consistent with the target.",
                "Purple line below the grey one: the market prices lower inflation than today's; above it, higher.",
                "The measure includes an inflation-risk premium (which raises it) and a premium for the lower liquidity of UVR TES (which tends to lower it), so it is not pure expectations.",
                "The 1-year tenor is sensitive to monthly inflation prints and to UVR indexation, which uses the previous month's inflation; compare it with the Banco de la República's Expectations Survey."
            ],
            "formulas": [
                ["1-year breakeven", "b<sub>1</sub> = [(1 + y<sub>1</sub><sup>$</sup>) ÷ (1 + r<sub>1</sub>) − 1] × 100", "y<sub>1</sub><sup>$</sup> = 1-year peso TES zero-coupon yield; r<sub>1</sub> = 1-year UVR TES zero-coupon yield (decimal form)"],
                ["Annual change (bottom panel)", "Δb<sub>1,t</sub> = b<sub>1,t</sub> − b<sub>1,t−1 year</sub>", "in pp"]
            ]
        },
    },
    "g-tray": {
        "es": {
            "que": "Une en una misma línea de tiempo la inflación que ya ocurrió y la que hoy incorporan los precios de los TES para los próximos diez años, dividida en tres tramos: el próximo año, los años 1 a 5 y los años 5 a 10. Los tramos se obtienen de las inflaciones de equilibrio (breakeven) a 1, 5 y 10 años, encadenadas para aislar la inflación promedio de cada periodo futuro. Es la lectura del mercado, no una estimación propia del tablero.",
            "leer": "Eje horizontal: tiempo calendario, desde cuatro años atrás hasta diez años adelante; eje vertical: inflación anual en %. A la izquierda de la línea vertical punteada («hoy»), la línea gris es la inflación anual observada del IPC. A la derecha, los tres escalones morados gruesos son la inflación promedio por año que incorporan los TES en cada tramo, con su valor rotulado. Los escalones grises punteados son la misma lectura hecha hace un año, ubicados desde esa fecha. La franja verde es el rango meta (2% a 4%) y la línea verde, la meta de 3%.",
            "importa": "La forma de esta trayectoria resume cuánto tiempo cree el mercado que tomará el regreso de la inflación a la meta y dónde ubica la inflación de largo plazo, información clave para valorar activos en pesos, contratos indexados y deuda de largo plazo. Comparar con la lectura de hace un año muestra si la confianza en la desinflación ha mejorado o empeorado.",
            "interpretar": [
                "Escalones que descienden hacia la franja verde: el mercado incorpora una convergencia gradual a la meta; escalones planos por encima de 4% indican expectativas altas y persistentes.",
                "Escalones morados por encima de los grises: el mercado incorpora hoy más inflación que hace un año para los mismos horizontes; por debajo, menos.",
                "El tramo de 5 a 10 años (la «5y5y») es el más usado para medir el anclaje de largo plazo; su historia está en el gráfico «Inflación esperada a largo plazo».",
                "Cada tramo incluye primas por riesgo inflacionario y por liquidez; los tramos encadenados reproducen exactamente el breakeven a 10 años, pero no son expectativas puras."
            ],
            "formulas": [
                ["Año 1", "f<sub>0,1</sub> = b<sub>1</sub>", "b<sub>n</sub> = breakeven a n años = (1 + y<sub>n</sub><sup>$</sup>) ÷ (1 + r<sub>n</sub>) − 1"],
                ["Años 1 a 5", "f<sub>1,5</sub> = [(1 + b<sub>5</sub>)<sup>5</sup> ÷ (1 + b<sub>1</sub>)]<sup>1/4</sup> − 1", "inflación promedio anual implícita entre el año 1 y el 5"],
                ["Años 5 a 10 (5y5y)", "f<sub>5,10</sub> = [(1 + b<sub>10</sub>)<sup>10</sup> ÷ (1 + b<sub>5</sub>)<sup>5</sup>]<sup>1/5</sup> − 1", "inflación promedio anual implícita entre el año 5 y el 10"],
                ["Encadenamiento", "(1 + f<sub>0,1</sub>) × (1 + f<sub>1,5</sub>)<sup>4</sup> × (1 + f<sub>5,10</sub>)<sup>5</sup> = (1 + b<sub>10</sub>)<sup>10</sup>", "los tres tramos reproducen el breakeven a 10 años"]
            ]
        },
        "en": {
            "que": "Places on a single timeline the inflation that has already happened and the inflation TES prices currently embed for the next ten years, split into three segments: next year, years 1 to 5 and years 5 to 10. The segments come from the 1-, 5- and 10-year breakeven inflation rates, chained to isolate average inflation in each future period. It is the market's reading, not an estimate by this dashboard.",
            "leer": "Horizontal axis: calendar time, from four years back to ten years ahead; vertical axis: annual inflation in %. Left of the dotted vertical line ('today'), the grey line is actual annual CPI inflation. To the right, the three thick purple steps are the average annual inflation priced by TES in each segment, with their values labelled. The grey dotted steps are the same reading taken a year ago, placed from that date. The green band is the target range (2% to 4%) and the green line the 3% target.",
            "importa": "The shape of this path summarises how long the market thinks inflation will take to return to target and where it places long-run inflation, key information for valuing peso assets, indexed contracts and long-term debt. Comparing with the reading a year ago shows whether confidence in disinflation has improved or worsened.",
            "interpretar": [
                "Steps falling towards the green band: the market prices gradual convergence to target; flat steps above 4% signal high, persistent expectations.",
                "Purple steps above the grey ones: the market now prices more inflation than a year ago for the same horizons; below, less.",
                "The 5-to-10-year segment (the '5y5y') is the most widely used gauge of long-run anchoring; its history is in the chart 'Long-term expected inflation'.",
                "Each segment includes inflation-risk and liquidity premia; the chained segments reproduce the 10-year breakeven exactly, but they are not pure expectations."
            ],
            "formulas": [
                ["Year 1", "f<sub>0,1</sub> = b<sub>1</sub>", "b<sub>n</sub> = n-year breakeven = (1 + y<sub>n</sub><sup>$</sup>) ÷ (1 + r<sub>n</sub>) − 1"],
                ["Years 1 to 5", "f<sub>1,5</sub> = [(1 + b<sub>5</sub>)<sup>5</sup> ÷ (1 + b<sub>1</sub>)]<sup>1/4</sup> − 1", "implied average annual inflation between years 1 and 5"],
                ["Years 5 to 10 (5y5y)", "f<sub>5,10</sub> = [(1 + b<sub>10</sub>)<sup>10</sup> ÷ (1 + b<sub>5</sub>)<sup>5</sup>]<sup>1/5</sup> − 1", "implied average annual inflation between years 5 and 10"],
                ["Chaining", "(1 + f<sub>0,1</sub>) × (1 + f<sub>1,5</sub>)<sup>4</sup> × (1 + f<sub>5,10</sub>)<sup>5</sup> = (1 + b<sub>10</sub>)<sup>10</sup>", "the three segments reproduce the 10-year breakeven"]
            ]
        },
    },
    "g-anclaje": {
        "es": {
            "que": "Muestra la historia de la inflación que el mercado de TES incorpora, en promedio anual, para el periodo entre 5 y 10 años adelante (el forward 5y5y). Al mirar tan lejos, la medida deja de lado los choques transitorios de hoy y refleja la confianza en que el Banco de la República lleve la inflación a su meta de 3% en el largo plazo: es la medida de mercado más usada del anclaje de las expectativas.",
            "leer": "Panel superior, en % anual: la línea morada es el 5y5y semanal (último dato de cada viernes); cada punto es lo que el mercado incorporaba ese día para el tramo de 5 a 10 años adelante desde esa fecha. La franja verde es el rango meta (2% a 4%) y la línea verde, la meta de 3%. Panel inferior: barras con el cambio del 5y5y frente a un año antes, en pp; azules si subió y naranjas si bajó. La vista inicial abarca los últimos diez años.",
            "importa": "Si las expectativas de largo plazo se mantienen ancladas a la meta, los choques de inflación tienden a disiparse sin contagiar salarios y precios, y el Banco necesita menos ajuste de tasas para controlarlos. Un desanclaje encarece la deuda de largo plazo y exige una política monetaria más restrictiva. Para un inversionista es una lectura directa de la credibilidad del Banco y de la prima por inflación en los TES largos.",
            "interpretar": [
                "Cerca de 3% y dentro de la franja: expectativas ancladas; por encima de 4% el tablero las considera desancladas.",
                "Si el 5y5y sube junto con la inflación observada, el mercado duda de que el choque sea transitorio; si se mantiene estable mientras la inflación sube, el anclaje funciona.",
                "Barras azules persistentes en el panel inferior indican un deterioro gradual de la confianza de largo plazo.",
                "Al ser un forward de largo plazo amplifica primas por riesgo inflacionario y por liquidez de los TES UVR, y es sensible a errores en las tasas a 5 y 10 años; los saltos aislados de un día se depuran."
            ],
            "formulas": [
                ["Forward 5y5y", "f<sub>5,10</sub> = [(1 + b<sub>10</sub>)<sup>10</sup> ÷ (1 + b<sub>5</sub>)<sup>5</sup>]<sup>1/5</sup> − 1", "b<sub>n</sub> = breakeven a n años = (1 + y<sub>n</sub><sup>$</sup>) ÷ (1 + r<sub>n</sub>) − 1"],
                ["Forma equivalente", "f<sub>5,10</sub> = F<sup>$</sup> ÷ F<sup>UVR</sup> − 1", "F = [(1 + y<sub>10</sub>)<sup>10</sup> ÷ (1 + y<sub>5</sub>)<sup>5</sup>]<sup>1/5</sup>, factor forward nominal ($) o real (UVR)"],
                ["Cambio anual (panel inferior)", "Δf<sub>t</sub> = f<sub>t</sub> − f<sub>t−1 año</sub>", "en pp"]
            ]
        },
        "en": {
            "que": "Shows the history of the average annual inflation the TES market prices for the period between 5 and 10 years ahead (the 5y5y forward). By looking that far out, the measure sets aside today's transitory shocks and reflects confidence that the Banco de la República will bring inflation to its 3% target in the long run: it is the most widely used market gauge of expectation anchoring.",
            "leer": "Top panel, in % a year: the purple line is the weekly 5y5y (last value each Friday); each point is what the market priced that day for the 5-to-10-year window ahead of that date. The green band is the target range (2% to 4%) and the green line the 3% target. Bottom panel: bars with the change in the 5y5y versus a year earlier, in pp; blue when it rose and orange when it fell. The initial view covers the last ten years.",
            "importa": "If long-run expectations stay anchored to the target, inflation shocks tend to fade without spilling into wages and prices, and the Bank needs less rate adjustment to contain them. De-anchoring raises long-term borrowing costs and calls for tighter monetary policy. For an investor it is a direct reading of the Bank's credibility and of the inflation premium in long TES.",
            "interpretar": [
                "Near 3% and inside the band: anchored expectations; above 4% the dashboard considers them de-anchored.",
                "If the 5y5y rises along with actual inflation, the market doubts the shock is transitory; if it stays stable while inflation rises, anchoring is working.",
                "Persistent blue bars in the bottom panel signal a gradual erosion of long-run confidence.",
                "Being a long-dated forward, it amplifies inflation-risk and UVR-liquidity premia and is sensitive to errors in the 5- and 10-year rates; isolated one-day jumps are cleaned."
            ],
            "formulas": [
                ["5y5y forward", "f<sub>5,10</sub> = [(1 + b<sub>10</sub>)<sup>10</sup> ÷ (1 + b<sub>5</sub>)<sup>5</sup>]<sup>1/5</sup> − 1", "b<sub>n</sub> = n-year breakeven = (1 + y<sub>n</sub><sup>$</sup>) ÷ (1 + r<sub>n</sub>) − 1"],
                ["Equivalent form", "f<sub>5,10</sub> = F<sup>$</sup> ÷ F<sup>UVR</sup> − 1", "F = [(1 + y<sub>10</sub>)<sup>10</sup> ÷ (1 + y<sub>5</sub>)<sup>5</sup>]<sup>1/5</sup>, nominal ($) or real (UVR) forward factor"],
                ["Annual change (bottom panel)", "Δf<sub>t</sub> = f<sub>t</sub> − f<sub>t−1 year</sub>", "in pp"]
            ]
        },
    },
    "g-inf-aportes": {
        "es": {
            "que": "Descompone la inflación anual total en el aporte de cada una de las 12 divisiones de gasto de la canasta del IPC (clasificación COICOP de Naciones Unidas: alimentos, vivienda y servicios públicos, transporte, restaurantes y hoteles, etc.). Combina cuánto suben los precios de cada división con cuánto pesa en el gasto de los hogares, y responde qué rubros explican la inflación del último mes publicado.",
            "leer": "Barras horizontales azules, ordenadas de menor a mayor aporte (el mayor arriba), con el valor rotulado en puntos porcentuales (pp). Entre paréntesis, junto al nombre de cada división, su ponderación en la canasta del IPC (en % del gasto total). La suma de todas las barras es la inflación anual total. Una barra negativa indica una división cuyos precios bajaron y restan a la inflación. Corresponde al último mes publicado por el DANE.",
            "importa": "Una división puede subir mucho y aportar poco si pesa poco, o subir moderadamente y explicar buena parte de la inflación si pesa mucho, como vivienda (que incluye arriendos y servicios públicos) o alimentos. Identificar los aportes ayuda a evaluar si la inflación es de oferta (alimentos, energía) o de demanda y de indexación (servicios, arriendos), y por tanto su persistencia.",
            "interpretar": [
                "Las divisiones con más peso (alimentos, vivienda, transporte) suelen dominar los aportes; un aporte grande de una división pequeña señala un choque fuerte de precios en ella.",
                "Conviene leerlo con el gráfico vecino «Inflación anual de cada división»: aquel muestra cuánto suben los precios; este, cuánto pesa ese aumento en el total.",
                "Si el aporte de vivienda es alto y estable, la inflación tiene un componente persistente asociado a arriendos e indexación.",
                "El aporte usa el peso efectivo de cada división, que cambia con los precios relativos desde la base 2018; por eso no es exactamente la ponderación por la variación."
            ],
            "formulas": [
                ["Aporte de la división i", "A<sub>i,t</sub> = w<sub>i</sub> × (I<sub>i,t−12</sub> ÷ I<sub>t−12</sub>) × π<sub>i,t</sub>", "w<sub>i</sub> = ponderación base 2018; I<sub>i</sub> = índice de la división; I = IPC total; π<sub>i,t</sub> = inflación anual de la división (%)"],
                ["Suma de aportes", "Σ<sub>i</sub> A<sub>i,t</sub> = π<sub>t</sub>", "π<sub>t</sub> = inflación anual total; resultado en pp"]
            ]
        },
        "en": {
            "que": "Breaks headline annual inflation into the contribution of each of the 12 spending divisions of the CPI basket (the United Nations COICOP classification: food, housing and utilities, transport, restaurants and hotels, etc.). It combines how much each division's prices rise with how much it weighs in household spending, answering which items explain inflation in the latest published month.",
            "leer": "Horizontal blue bars, ordered from smallest to largest contribution (largest at the top), labelled in percentage points (pp). In brackets next to each division's name is its weight in the CPI basket (% of total spending). All bars add up to headline annual inflation. A negative bar marks a division whose prices fell and that subtracts from inflation. It refers to the latest month published by DANE.",
            "importa": "A division can rise sharply yet contribute little if it weighs little, or rise moderately and explain much of inflation if it weighs a lot, like housing (which includes rents and utilities) or food. Identifying contributions helps judge whether inflation is supply-driven (food, energy) or driven by demand and indexation (services, rents), and therefore how persistent it is.",
            "interpretar": [
                "The heaviest divisions (food, housing, transport) usually dominate; a large contribution from a small division signals a strong price shock there.",
                "Read it with the neighbouring chart 'Annual inflation by division': that one shows how much prices rise; this one, how much that rise weighs in the total.",
                "If housing's contribution is high and steady, inflation has a persistent component tied to rents and indexation.",
                "The contribution uses each division's effective weight, which shifts with relative prices since the 2018 base; so it is not exactly the weight times the change."
            ],
            "formulas": [
                ["Contribution of division i", "A<sub>i,t</sub> = w<sub>i</sub> × (I<sub>i,t−12</sub> ÷ I<sub>t−12</sub>) × π<sub>i,t</sub>", "w<sub>i</sub> = 2018 base weight; I<sub>i</sub> = division index; I = headline CPI; π<sub>i,t</sub> = division annual inflation (%)"],
                ["Sum of contributions", "Σ<sub>i</sub> A<sub>i,t</sub> = π<sub>t</sub>", "π<sub>t</sub> = headline annual inflation; result in pp"]
            ]
        },
    },
    "g-inf-divisiones": {
        "es": {
            "que": "Compara la inflación anual de cada una de las 12 divisiones de gasto del IPC (clasificación COICOP): alimentos, alcohol y tabaco, ropa y calzado, vivienda y servicios públicos, muebles y hogar, salud, transporte, comunicaciones, recreación y cultura, educación, restaurantes y hoteles, y otros bienes y servicios. Muestra qué tan generalizada es la inflación entre los grandes rubros del gasto de los hogares en el último mes publicado.",
            "leer": "Barras horizontales ordenadas de menor a mayor inflación (la mayor arriba), en % anual, con el valor rotulado. Las barras naranjas superan el techo del rango meta (4%) y las azules están en o por debajo de él. La franja verde vertical marca el rango meta del Banco de la República (2% a 4%). Una barra a la izquierda de cero indica que los precios de esa división bajaron en el último año. Datos del total nacional.",
            "importa": "La dispersión entre divisiones revela la naturaleza de la inflación: si casi todas están en naranja, la presión es amplia y responde a la demanda y a la indexación; si solo unas pocas, se trata de choques sectoriales. Para empresas e inversionistas indica qué sectores enfrentan mayores aumentos de costos o tienen más poder para subir precios.",
            "interpretar": [
                "Muchas barras naranjas: inflación generalizada; pocas barras naranjas con valores muy altos: choques concentrados.",
                "Educación suele ajustarse una vez al año (a comienzos del año escolar) y salud con decisiones regulatorias, por lo que su inflación anual cambia en escalones.",
                "La inflación de una división no dice cuánto aporta al total: para eso está el gráfico vecino «Aporte de cada división».",
                "Las divisiones agrupan bienes muy distintos; el detalle por subclase está en los gráficos de difusión y de subclases que más suman y restan."
            ],
            "formulas": [
                ["Inflación anual de la división", "π<sub>i,t</sub> = (I<sub>i,t</sub> ÷ I<sub>i,t−12</sub> − 1) × 100", "I<sub>i,t</sub> = índice de precios de la división i en el mes t (base diciembre 2018 = 100), total nacional"]
            ]
        },
        "en": {
            "que": "Compares annual inflation in each of the 12 CPI spending divisions (COICOP classification): food, alcohol and tobacco, clothing and footwear, housing and utilities, furnishings and household, health, transport, communications, recreation and culture, education, restaurants and hotels, and other goods and services. It shows how widespread inflation is across the main household spending categories in the latest published month.",
            "leer": "Horizontal bars ordered from lowest to highest inflation (highest at the top), in % a year, with the value labelled. Orange bars exceed the top of the target range (4%) and blue bars are at or below it. The vertical green band marks the Banco de la República target range (2% to 4%). A bar left of zero means that division's prices fell over the last year. National-total data.",
            "importa": "Dispersion across divisions reveals the nature of inflation: if nearly all bars are orange, pressure is broad and driven by demand and indexation; if only a few, it reflects sector-specific shocks. For companies and investors it shows which sectors face larger cost increases or have more power to raise prices.",
            "interpretar": [
                "Many orange bars: broad-based inflation; a few orange bars with very high values: concentrated shocks.",
                "Education usually adjusts once a year (at the start of the school year) and health with regulatory decisions, so their annual inflation changes in steps.",
                "A division's inflation does not say how much it contributes to the total: the neighbouring chart 'Contribution of each division' does.",
                "Divisions group very different goods; subclass detail is in the diffusion chart and the chart of subclasses adding and subtracting most."
            ],
            "formulas": [
                ["Division annual inflation", "π<sub>i,t</sub> = (I<sub>i,t</sub> ÷ I<sub>i,t−12</sub> − 1) × 100", "I<sub>i,t</sub> = price index of division i in month t (base December 2018 = 100), national total"]
            ]
        },
    },
    "g-inf-bienes-servicios": {
        "es": {
            "que": "Compara la inflación anual de los servicios con la de los bienes, separados por su durabilidad según la clasificación del DANE: no durables (alimentos, combustibles, aseo), semidurables (ropa, calzado, utensilios) y durables (vehículos, electrodomésticos, muebles). Cada grupo responde a fuerzas distintas, y su comparación ayuda a entender de dónde viene la inflación.",
            "leer": "Eje horizontal: fecha, desde 2012; eje vertical: variación anual en %. Línea azul gruesa: servicios; línea naranja: bienes no durables; línea verde: semidurables; línea morada: durables. La franja verde es el rango meta (2% a 4%) con la línea de la meta de 3%, y la línea horizontal gris marca el cero. Datos mensuales; el recuadro flotante muestra los cuatro valores a la vez.",
            "importa": "Los servicios dependen sobre todo de salarios, arriendos e indexación, por lo que su inflación es persistente y sensible a la demanda interna y al salario mínimo; los durables, en buena parte importados, se mueven con la tasa de cambio; los no durables, con alimentos y energía. Saber qué grupo lidera indica si la inflación responde más a la política monetaria o a choques externos y de oferta.",
            "interpretar": [
                "Servicios por encima de los bienes por un periodo largo: presión de fondo ligada a salarios e indexación, que suele ceder despacio.",
                "Durables al alza tras una depreciación del peso: transmisión de la tasa de cambio; su inflación puede ser negativa cuando el peso se aprecia o la demanda cae.",
                "Los no durables reaccionan primero a choques de alimentos y combustibles y son los más volátiles.",
                "Las series se calculan como variación anual de índices del DANE (base diciembre 2018 = 100); el inicio en 2012 permite comparar varios ciclos."
            ],
            "formulas": [
                ["Inflación anual por durabilidad", "π<sub>k,t</sub> = (I<sub>k,t</sub> ÷ I<sub>k,t−12</sub> − 1) × 100", "I<sub>k,t</sub> = índice del DANE del grupo k (servicios, no durables, semidurables o durables) en el mes t"]
            ]
        },
        "en": {
            "que": "Compares annual services inflation with goods inflation, split by durability under DANE's classification: non-durables (food, fuel, cleaning products), semi-durables (clothing, footwear, utensils) and durables (vehicles, appliances, furniture). Each group responds to different forces, and comparing them helps explain where inflation is coming from.",
            "leer": "Horizontal axis: date, since 2012; vertical axis: annual change in %. Thick blue line: services; orange line: non-durable goods; green line: semi-durables; purple line: durables. The green band is the target range (2% to 4%) with the 3% target line, and the grey horizontal line marks zero. Monthly data; the hover box shows all four values at once.",
            "importa": "Services depend mainly on wages, rents and indexation, so their inflation is persistent and sensitive to domestic demand and the minimum wage; durables, largely imported, move with the exchange rate; non-durables, with food and energy. Knowing which group leads shows whether inflation responds more to monetary policy or to external and supply shocks.",
            "interpretar": [
                "Services above goods for a long period: underlying pressure tied to wages and indexation, which tends to ease slowly.",
                "Durables rising after a peso depreciation: exchange-rate pass-through; their inflation can turn negative when the peso appreciates or demand weakens.",
                "Non-durables react first to food and fuel shocks and are the most volatile.",
                "The series are annual changes of DANE indices (base December 2018 = 100); starting in 2012 allows comparison across several cycles."
            ],
            "formulas": [
                ["Annual inflation by durability", "π<sub>k,t</sub> = (I<sub>k,t</sub> ÷ I<sub>k,t−12</sub> − 1) × 100", "I<sub>k,t</sub> = DANE index of group k (services, non-durables, semi-durables or durables) in month t"]
            ]
        },
    },
    "g-inf-energia": {
        "es": {
            "que": "Contrasta la inflación de los energéticos (gas, energía eléctrica y combustibles) con la inflación sin alimentos ni energéticos, la medida de inflación básica más usada internacionalmente. Los energéticos son de los precios más volátiles de la canasta; la medida básica los excluye, junto con los alimentos, para mostrar la presión de precios persistente.",
            "leer": "Eje horizontal: fecha, desde 2012; eje vertical: variación anual en %. Línea amarilla: energéticos; línea azul gruesa: IPC sin alimentos ni energéticos. La franja verde es el rango meta (2% a 4%) con la línea de la meta de 3%, y la línea horizontal gris marca el cero. Para que los picos no aplasten el resto del gráfico, la línea de energéticos se recorta entre −20% y 40%. Datos mensuales del DANE.",
            "importa": "Los precios de la energía dependen del petróleo, del clima (que afecta la generación hidroeléctrica), de la tasa de cambio y de decisiones regulatorias sobre tarifas y combustibles. Separarlos de la inflación básica permite ver si un alza de la inflación total es un choque energético que puede revertirse o una presión generalizada que exige más respuesta de la política monetaria.",
            "interpretar": [
                "Energéticos muy por encima de la línea azul: la inflación total la empuja un choque de energía; si la línea azul también sube, el choque se está transmitiendo al resto de precios.",
                "Línea azul por encima de 4% con energéticos estables: la presión es de fondo y no depende de la energía.",
                "Los ajustes graduales de precios de combustibles o tarifas definidos por el Gobierno pueden mantener alta la inflación de energéticos por varios meses.",
                "Esta medida básica (sin alimentos ni energéticos, del DANE) no es la misma que la inflación sin alimentos ni regulados del Banco de la República mostrada en «Inflación anual frente a la meta»."
            ],
            "formulas": [
                ["Inflación anual", "π<sub>k,t</sub> = (I<sub>k,t</sub> ÷ I<sub>k,t−12</sub> − 1) × 100", "I<sub>k,t</sub> = índice del DANE de energéticos o del IPC sin alimentos ni energéticos en el mes t"],
                ["Recorte visual", "π̃<sub>E,t</sub> = min(max(π<sub>E,t</sub>, −20), 40)", "solo para la línea de energéticos (E)"]
            ]
        },
        "en": {
            "que": "Contrasts energy inflation (gas, electricity and fuel) with inflation excluding food and energy, the most widely used core measure internationally. Energy prices are among the most volatile in the basket; the core measure excludes them, along with food, to show persistent price pressure.",
            "leer": "Horizontal axis: date, since 2012; vertical axis: annual change in %. Yellow line: energy; thick blue line: CPI excluding food and energy. The green band is the target range (2% to 4%) with the 3% target line, and the grey horizontal line marks zero. So that spikes do not flatten the rest of the chart, the energy line is clipped between −20% and 40%. Monthly DANE data.",
            "importa": "Energy prices depend on oil, weather (which affects hydropower generation), the exchange rate and regulatory decisions on tariffs and fuel. Separating them from core inflation shows whether a rise in headline inflation is an energy shock that may reverse or broad pressure that calls for a stronger monetary-policy response.",
            "interpretar": [
                "Energy far above the blue line: headline is being pushed by an energy shock; if the blue line also rises, the shock is passing through to other prices.",
                "Blue line above 4% with stable energy: the pressure is underlying and does not depend on energy.",
                "Gradual fuel-price or tariff adjustments set by the Government can keep energy inflation high for several months.",
                "This core measure (excluding food and energy, from DANE) is not the same as the Banco de la República's inflation excluding food and regulated prices shown in 'Annual inflation vs target'."
            ],
            "formulas": [
                ["Annual inflation", "π<sub>k,t</sub> = (I<sub>k,t</sub> ÷ I<sub>k,t−12</sub> − 1) × 100", "I<sub>k,t</sub> = DANE index for energy or for CPI excluding food and energy in month t"],
                ["Visual clipping", "π̃<sub>E,t</sub> = min(max(π<sub>E,t</sub>, −20), 40)", "energy line (E) only"]
            ]
        },
    },
    "g-inf-difusion": {
        "es": {
            "que": "Muestra cómo se reparte la inflación anual entre las 188 subclases de la canasta del IPC, el nivel más detallado que publica el DANE (por ejemplo arroz, arriendo, electricidad o comidas fuera del hogar). En lugar de un promedio, enseña la distribución completa: si la mayoría de precios suben a un ritmo parecido o si unos pocos suben mucho mientras el resto se mantiene estable.",
            "leer": "Histograma: el eje horizontal es la inflación anual en intervalos de 1 punto porcentual (de −10% a 20%) y el eje vertical, el número de subclases en cada intervalo. Las subclases no se ponderan: cada una cuenta igual. Las barras naranjas son los intervalos por encima de 4% (el techo del rango meta) y las azules, los de 4% o menos. La franja verde marca el rango meta (2% a 4%). Los valores extremos se acumulan en los intervalos de los bordes. Corresponde al último mes publicado.",
            "importa": "La difusión mide qué tan generalizada es la inflación, algo que el promedio no revela: una inflación del 6% puede venir de unos pocos precios disparados o de un alza amplia de casi todos. Cuando la mayoría de subclases supera la meta, la inflación tiende a ser más persistente y la política monetaria más exigente; cuando la masa está en la franja verde, los focos son puntuales.",
            "interpretar": [
                "Masa de barras a la derecha de 4% (naranja): inflación generalizada; masa en la franja verde: la mayoría de precios es coherente con la meta.",
                "Una distribución ancha indica gran dispersión de precios relativos, típica de choques de oferta; una estrecha, de presiones comunes como la indexación.",
                "Al no ponderar, una subclase de poco peso cuenta lo mismo que el arriendo; la ventana «¿Qué son las 188 subclases?» muestra también la proporción del gasto que supera 4%.",
                "Para saber qué subclases explican la inflación total, ver el gráfico vecino «Las subclases que más suman y más restan»."
            ],
            "formulas": [
                ["Frecuencia del intervalo", "n<sub>j</sub> = #{ s : a<sub>j</sub> ≤ min(max(π<sub>s</sub>, −10), 20) < a<sub>j</sub> + 1 }", "π<sub>s</sub> = inflación anual de la subclase s (%); a<sub>j</sub> = límite inferior del intervalo j; el último intervalo incluye el 20"],
                ["Difusión", "D = #{ s : π<sub>s</sub> > 4 } ÷ 188 × 100", "proporción de subclases por encima del techo del rango meta, sin ponderar"]
            ]
        },
        "en": {
            "que": "Shows how annual inflation is spread across the 188 subclasses of the CPI basket, the most detailed level DANE publishes (for example rice, rent, electricity or meals away from home). Instead of an average, it shows the whole distribution: whether most prices rise at a similar pace or a few rise sharply while the rest stay stable.",
            "leer": "Histogram: the horizontal axis is annual inflation in 1-percentage-point bins (from −10% to 20%) and the vertical axis the number of subclasses in each bin. Subclasses are unweighted: each counts equally. Orange bars are bins above 4% (the top of the target range) and blue bars those at 4% or below. The green band marks the target range (2% to 4%). Extreme values pile up in the edge bins. It refers to the latest published month.",
            "importa": "Diffusion measures how widespread inflation is, which the average does not reveal: 6% inflation can come from a few runaway prices or from a broad rise in almost all of them. When most subclasses exceed the target, inflation tends to be more persistent and monetary policy more demanding; when the bulk sits in the green band, the hot spots are isolated.",
            "interpretar": [
                "Bulk of bars right of 4% (orange): broad-based inflation; bulk in the green band: most prices are consistent with the target.",
                "A wide distribution signals large relative-price dispersion, typical of supply shocks; a narrow one, common pressures such as indexation.",
                "Being unweighted, a small subclass counts as much as rent; the window 'What are the 188 subclasses?' also shows the share of spending rising above 4%.",
                "To see which subclasses drive headline inflation, see the neighbouring chart 'The subclasses adding and subtracting most'."
            ],
            "formulas": [
                ["Bin frequency", "n<sub>j</sub> = #{ s : a<sub>j</sub> ≤ min(max(π<sub>s</sub>, −10), 20) < a<sub>j</sub> + 1 }", "π<sub>s</sub> = annual inflation of subclass s (%); a<sub>j</sub> = lower bound of bin j; the last bin includes 20"],
                ["Diffusion", "D = #{ s : π<sub>s</sub> > 4 } ÷ 188 × 100", "share of subclasses above the top of the target range, unweighted"]
            ]
        },
    },
    "g-inf-subclases": {
        "es": {
            "que": "Identifica las subclases de la canasta del IPC que más empujan la inflación anual hacia arriba y las que más la frenan. El aporte de cada subclase combina cuánto subió su precio con cuánto pesa en el gasto de los hogares, de modo que permite ver qué productos y servicios concretos explican la inflación del último mes publicado.",
            "leer": "Barras horizontales con el aporte de cada subclase a la inflación anual total, en puntos porcentuales (pp), con su valor rotulado: las 8 que más suman y las 4 de menor aporte (las que más restan), ordenadas de menor a mayor. Las barras naranjas suman a la inflación y las verdes restan; la línea vertical marca el cero. Al pasar el cursor se ve la inflación anual de la subclase. Los nombres largos se recortan.",
            "importa": "Unas pocas subclases de gran peso, como el arriendo, la electricidad, las comidas fuera del hogar o el transporte urbano, pueden explicar buena parte de la inflación. Conocerlas permite distinguir si la presión viene de bienes con precios volátiles o de servicios indexados, e identificar qué rubros pesan hoy en los costos de hogares y empresas.",
            "interpretar": [
                "Si las mayores barras naranjas son servicios (arriendos, restaurantes, educación), la inflación tiene un componente persistente; si son alimentos o energía, uno más volátil.",
                "Una subclase puede aportar mucho con una inflación moderada si su peso es grande; el recuadro flotante muestra su inflación para distinguir ambos efectos.",
                "Las barras verdes señalan precios que bajaron en el año y contienen la inflación; si hay menos de cuatro subclases con aporte negativo, alguna barra del grupo inferior puede ser positiva (y se ve naranja).",
                "Los aportes los calcula el DANE con ponderaciones de la canasta base 2018; la suma de las 188 subclases da la inflación total."
            ],
            "formulas": [
                ["Aporte de la subclase s", "A<sub>s,t</sub> = w<sub>s</sub> × (I<sub>s,t−12</sub> ÷ I<sub>t−12</sub>) × π<sub>s,t</sub>", "w<sub>s</sub> = ponderación base 2018; I<sub>s</sub> = índice de la subclase; I = IPC total; π<sub>s,t</sub> = inflación anual de la subclase (%)"],
                ["Suma de aportes", "Σ<sub>s=1..188</sub> A<sub>s,t</sub> = π<sub>t</sub>", "π<sub>t</sub> = inflación anual total; en pp"]
            ]
        },
        "en": {
            "que": "Identifies the CPI subclasses pushing annual inflation up the most and those holding it back the most. Each subclass's contribution combines how much its price rose with how much it weighs in household spending, showing which specific goods and services explain inflation in the latest published month.",
            "leer": "Horizontal bars with each subclass's contribution to headline annual inflation, in percentage points (pp), with the value labelled: the 8 adding most and the 4 with the lowest contribution (subtracting most), ordered from lowest to highest. Orange bars add to inflation and green bars subtract; the vertical line marks zero. Hovering shows the subclass's annual inflation. Long names are truncated.",
            "importa": "A few heavily weighted subclasses, such as rent, electricity, meals away from home or urban transport, can explain much of inflation. Knowing them separates pressure from volatile-price goods from pressure from indexed services, and shows which items weigh on household and business costs.",
            "interpretar": [
                "If the largest orange bars are services (rents, restaurants, education), inflation has a persistent component; if they are food or energy, a more volatile one.",
                "A subclass can contribute a lot with moderate inflation if its weight is large; the hover box shows its inflation to tell the two effects apart.",
                "Green bars mark prices that fell over the year and restrain inflation; if fewer than four subclasses have a negative contribution, a bar in the bottom group may be positive (and shown orange).",
                "Contributions are computed by DANE with 2018 basket weights; the 188 subclasses add up to headline inflation."
            ],
            "formulas": [
                ["Contribution of subclass s", "A<sub>s,t</sub> = w<sub>s</sub> × (I<sub>s,t−12</sub> ÷ I<sub>t−12</sub>) × π<sub>s,t</sub>", "w<sub>s</sub> = 2018 base weight; I<sub>s</sub> = subclass index; I = headline CPI; π<sub>s,t</sub> = subclass annual inflation (%)"],
                ["Sum of contributions", "Σ<sub>s=1..188</sub> A<sub>s,t</sub> = π<sub>t</sub>", "π<sub>t</sub> = headline annual inflation; in pp"]
            ]
        },
    },
    "g-inf-ingresos": {
        "es": {
            "que": "Compara la inflación anual que enfrentan cuatro grupos de hogares según su nivel de ingreso: pobres, vulnerables, clase media e ingresos altos. El DANE calcula un IPC para cada grupo con su propia canasta, porque los hogares de menores ingresos destinan más a alimentos y los de mayores ingresos más a servicios, de modo que un mismo cambio de precios los afecta de forma distinta.",
            "leer": "Eje horizontal: grupo de ingreso; eje vertical: inflación anual en %. Cuatro barras con su valor rotulado: azul para hogares pobres, verde para vulnerables, morada para clase media y naranja para ingresos altos. La línea horizontal negra punteada es la inflación total nacional. Corresponde al último mes publicado; los grupos se definen con un criterio absoluto de ingreso basado en las líneas de pobreza.",
            "importa": "La inflación es un impuesto regresivo cuando golpea más a los hogares pobres, que tienen menos margen para sustituir consumo o protegerse. La diferencia entre grupos tiene implicaciones para el consumo agregado, la pobreza monetaria, el ajuste del salario mínimo y las transferencias, y ayuda a entender la composición de la inflación: si los pobres enfrentan más inflación, suelen pesar los alimentos; si los de ingresos altos, los servicios.",
            "interpretar": [
                "Barra azul por encima de la naranja: la inflación golpea más a los hogares pobres, normalmente por alimentos; al revés, la presión está en servicios con más peso en canastas de ingresos altos.",
                "Barras cerca de la línea punteada: la inflación afecta de forma similar a todos los grupos.",
                "Las diferencias entre grupos suelen ser de décimas de punto porcentual, pero acumuladas por varios años cambian el costo de vida relativo.",
                "Cada IPC usa las ponderaciones de gasto del grupo según la encuesta de presupuestos de los hogares de la base 2018; los precios son los mismos para todos."
            ],
            "formulas": [
                ["IPC del grupo h", "IPC<sub>h,t</sub> = Σ<sub>s</sub> w<sub>s</sub><sup>h</sup> × I<sub>s,t</sub>", "w<sup>h</sup><sub>s</sub> = peso de la subclase s en la canasta del grupo h (Σ w = 1); I<sub>s,t</sub> = índice de la subclase"],
                ["Inflación anual del grupo", "π<sub>h,t</sub> = (IPC<sub>h,t</sub> ÷ IPC<sub>h,t−12</sub> − 1) × 100", "h = pobres, vulnerables, clase media o ingresos altos"]
            ]
        },
        "en": {
            "que": "Compares the annual inflation faced by four household groups by income level: poor, vulnerable, middle class and high income. DANE computes a CPI for each group with its own basket, because lower-income households spend more on food and higher-income households more on services, so the same price change affects them differently.",
            "leer": "Horizontal axis: income group; vertical axis: annual inflation in %. Four bars with their values labelled: blue for poor households, green for vulnerable, purple for middle class and orange for high income. The dotted black horizontal line is national headline inflation. It refers to the latest published month; groups are defined with an absolute income criterion based on poverty lines.",
            "importa": "Inflation acts as a regressive tax when it hits poor households harder, as they have less room to substitute consumption or protect themselves. The gap between groups matters for aggregate consumption, monetary poverty, minimum-wage setting and transfers, and helps read the composition of inflation: if the poor face higher inflation, food usually weighs; if high-income households do, services.",
            "interpretar": [
                "Blue bar above the orange one: inflation hits poor households harder, usually through food; the reverse means pressure is in services that weigh more in high-income baskets.",
                "Bars close to the dotted line: inflation affects all groups similarly.",
                "Gaps between groups are usually tenths of a percentage point, but accumulated over several years they change relative living costs.",
                "Each CPI uses the group's spending weights from the household budget survey behind the 2018 base; prices are the same for everyone."
            ],
            "formulas": [
                ["CPI of group h", "CPI<sub>h,t</sub> = Σ<sub>s</sub> w<sub>s</sub><sup>h</sup> × I<sub>s,t</sub>", "w<sup>h</sup><sub>s</sub> = weight of subclass s in group h's basket (Σ w = 1); I<sub>s,t</sub> = subclass index"],
                ["Group annual inflation", "π<sub>h,t</sub> = (CPI<sub>h,t</sub> ÷ CPI<sub>h,t−12</sub> − 1) × 100", "h = poor, vulnerable, middle class or high income"]
            ]
        },
    },
    "g-inf-ciudades": {
        "es": {
            "que": "Compara la inflación anual del IPC total en las 23 ciudades que el DANE publica por separado, cada una con su propia canasta. Muestra qué tan homogénea es la inflación en el territorio: las diferencias reflejan la composición del gasto local, la dependencia de alimentos de distintas zonas productoras, las tarifas de servicios públicos de cada región y las condiciones de demanda locales.",
            "leer": "Barras horizontales ordenadas de menor a mayor inflación (la mayor arriba), en % anual, con el valor rotulado. Las barras naranjas son ciudades con inflación por encima del total nacional y las azules, en o por debajo de él. La línea vertical negra punteada es la inflación total nacional. No se incluye el agregado de «otras áreas urbanas». Corresponde al último mes publicado.",
            "importa": "Para empresas con operaciones regionales, la inflación local determina costos, salarios y precios de venta en cada mercado; para inversionistas en finca raíz o consumo, revela diferencias en el poder adquisitivo regional. Las ciudades grandes, en especial Bogotá, Medellín y Cali, pesan mucho más en el total nacional, que por eso se parece más a ellas.",
            "interpretar": [
                "El número de barras naranjas no tiene por qué ser la mitad: el total nacional es un promedio ponderado por el gasto, dominado por las ciudades grandes.",
                "Las diferencias grandes entre ciudades suelen venir de tarifas de energía (muy distintas por región) y de choques de alimentos en zonas específicas.",
                "El detalle por división de gasto de cada ciudad está en el mapa de calor «¿Qué sube más en cada ciudad?».",
                "Las canastas de ciudades pequeñas tienen menos observaciones de precios y pueden ser más volátiles mes a mes."
            ],
            "formulas": [
                ["Inflación anual de la ciudad", "π<sub>c,t</sub> = (IPC<sub>c,t</sub> ÷ IPC<sub>c,t−12</sub> − 1) × 100", "IPC<sub>c,t</sub> = índice de precios al consumidor de la ciudad c en el mes t"],
                ["Total nacional", "IPC<sub>t</sub> = Σ<sub>c</sub> ω<sub>c</sub> × IPC<sub>c,t</sub>", "ω<sub>c</sub> = peso de la ciudad según el gasto de sus hogares (incluye otras áreas urbanas)"]
            ]
        },
        "en": {
            "que": "Compares headline annual CPI inflation in the 23 cities DANE publishes separately, each with its own basket. It shows how uniform inflation is across the country: the differences reflect the composition of local spending, reliance on food from different producing regions, each region's utility tariffs and local demand conditions.",
            "leer": "Horizontal bars ordered from lowest to highest inflation (highest at the top), in % a year, with the value labelled. Orange bars are cities with inflation above the national total and blue bars at or below it. The dotted black vertical line is national headline inflation. The 'other urban areas' aggregate is not included. It refers to the latest published month.",
            "importa": "For companies with regional operations, local inflation drives costs, wages and selling prices in each market; for real-estate or consumer investors it reveals differences in regional purchasing power. The large cities, especially Bogotá, Medellín and Cali, weigh far more in the national total, which therefore resembles them more.",
            "interpretar": [
                "The number of orange bars need not be half: the national total is a spending-weighted average dominated by the large cities.",
                "Large gaps between cities usually stem from energy tariffs (which differ widely by region) and food shocks in specific areas.",
                "Each city's breakdown by spending division is in the heat map 'What rises most in each city?'.",
                "Smaller cities' baskets rest on fewer price quotes and can be more volatile month to month."
            ],
            "formulas": [
                ["City annual inflation", "π<sub>c,t</sub> = (CPI<sub>c,t</sub> ÷ CPI<sub>c,t−12</sub> − 1) × 100", "CPI<sub>c,t</sub> = consumer price index of city c in month t"],
                ["National total", "CPI<sub>t</sub> = Σ<sub>c</sub> ω<sub>c</sub> × CPI<sub>c,t</sub>", "ω<sub>c</sub> = city weight based on its households' spending (includes other urban areas)"]
            ]
        },
    },
    "g-inf-ciudad-division": {
        "es": {
            "que": "Cruza las 23 ciudades del IPC con las 12 divisiones de gasto para mostrar qué rubros suben más en cada lugar. Permite ver si la inflación de una ciudad se explica por un rubro particular, como vivienda y servicios públicos o alimentos, o si el alza es amplia, y comparar el mismo rubro entre regiones.",
            "leer": "Mapa de calor: cada fila es una ciudad y cada columna una división de gasto (nombres arriba). El color de cada casilla indica la inflación anual de esa división en esa ciudad: casi blanco cerca de 0%, naranja intermedio alrededor de 7% y naranja oscuro desde 12%; la barra de color a la derecha da la escala. Los valores por debajo de 0% se ven como 0% y los superiores a 12%, con el tono más oscuro; el recuadro flotante muestra el valor exacto. Las filas siguen el orden de la inflación total de cada ciudad. Corresponde al último mes publicado.",
            "importa": "Las diferencias regionales de inflación suelen concentrarse en pocos rubros: tarifas de energía que dependen del operador regional, arriendos en ciudades con alta demanda de vivienda o alimentos según la cercanía a zonas productoras. Para empresas y para el análisis de política, este cruce indica si un choque es local o nacional y en qué rubros se concentra.",
            "interpretar": [
                "Una columna oscura en casi todas las filas indica un choque nacional en esa división; una casilla oscura aislada, un choque local.",
                "Una fila mayoritariamente oscura señala una ciudad con inflación amplia, no explicada por un solo rubro.",
                "La escala se recorta entre 0% y 12% para que los valores extremos no borren las diferencias; use el recuadro flotante para valores negativos o muy altos.",
                "Las divisiones con poco peso local pueden mostrar variaciones grandes con pocas observaciones de precios; contraste con el aporte de cada división en el total nacional."
            ],
            "formulas": [
                ["Inflación anual por ciudad y división", "π<sub>c,i,t</sub> = (I<sub>c,i,t</sub> ÷ I<sub>c,i,t−12</sub> − 1) × 100", "I<sub>c,i,t</sub> = índice de la división i en la ciudad c en el mes t (cuadro 6 del anexo del DANE)"],
                ["Escala de color", "z = min(max(π<sub>c,i,t</sub>, 0), 12)", "valor usado para el color; el recuadro flotante muestra π sin recortar"]
            ]
        },
        "en": {
            "que": "Crosses the 23 CPI cities with the 12 spending divisions to show which items are rising most in each place. It reveals whether a city's inflation comes from one particular item, such as housing and utilities or food, or from a broad rise, and lets the same item be compared across regions.",
            "leer": "Heat map: each row is a city and each column a spending division (names at the top). Each cell's colour gives that division's annual inflation in that city: almost white near 0%, mid orange around 7% and dark orange from 12%; the colour bar on the right gives the scale. Values below 0% show as 0% and those above 12% take the darkest shade; the hover box shows the exact value. Rows follow the order of each city's headline inflation. It refers to the latest published month.",
            "importa": "Regional inflation differences tend to concentrate in a few items: energy tariffs that depend on the regional operator, rents in cities with strong housing demand, or food depending on proximity to producing areas. For companies and policy analysis, this cross-section shows whether a shock is local or national and which items it concentrates in.",
            "interpretar": [
                "A column that is dark in almost every row signals a national shock in that division; an isolated dark cell, a local shock.",
                "A mostly dark row marks a city with broad inflation not explained by a single item.",
                "The scale is clipped between 0% and 12% so extreme values do not wash out the differences; use the hover box for negative or very high values.",
                "Divisions with little local weight can show large changes based on few price quotes; compare with each division's contribution to the national total."
            ],
            "formulas": [
                ["Annual inflation by city and division", "π<sub>c,i,t</sub> = (I<sub>c,i,t</sub> ÷ I<sub>c,i,t−12</sub> − 1) × 100", "I<sub>c,i,t</sub> = index of division i in city c in month t (table 6 of DANE's annex)"],
                ["Colour scale", "z = min(max(π<sub>c,i,t</sub>, 0), 12)", "value used for colour; the hover box shows the unclipped π"]
            ]
        },
    },
}
