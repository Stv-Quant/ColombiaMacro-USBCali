"""Lupas (explicaciones ampliadas) de los gráficos de las páginas Ciclo y Capacidad.

Grupo g1_ciclo_capacidad. Cada entrada describe el gráfico tal como lo construyen
capacidad_extra.py, ciclo_extra.py, construir.py (Graficos.capacidad y reloj del ciclo) y analitica.py.
Solo hechos y métodos: sin proyecciones ni recomendaciones, sin cifras ni fechas que caduquen.
"""

LUPAS = {
    # ------------------------------------------------------------------ CAPACIDAD
    "g-capacidad": {
        "es": {
            "que": "Compara lo que la economía colombiana produce cada trimestre (PIB real desestacionalizado) con su capacidad, "
                   "es decir, el PIB potencial: el nivel que puede sostener sin generar presiones de inflación. La distancia entre "
                   "ambos es la brecha del producto, el termómetro central del ciclo: dice si la economía está recalentada o si tiene "
                   "capacidad ociosa.",
            "leer": "Panel superior: la línea azul es el PIB real y la línea gris discontinua la capacidad, en billones de pesos de "
                    "2015 por trimestre (eje izquierdo). El área verde aparece cuando el PIB supera la capacidad y la naranja cuando "
                    "queda por debajo. Panel inferior: barras con la brecha en porcentaje, verdes si es positiva y naranjas si es "
                    "negativa, con una línea en cero. La vista inicial muestra los últimos diez años; la serie de brecha empieza "
                    "cinco años después del primer dato del PIB, porque el filtro necesita al menos 20 trimestres.",
            "importa": "La brecha resume el balance entre demanda y oferta. Una brecha positiva suele acompañar presiones de precios y "
                       "un mercado laboral apretado, y es una de las variables que el Banco de la República (BanRep) sigue para fijar "
                       "su tasa de política monetaria (TPM). Para un inversionista, ubicar la economía frente a su capacidad ayuda a "
                       "leer el contexto de inflación, tasas y utilidades empresariales.",
            "interpretar": [
                "Brecha positiva: la economía produce por encima de lo sostenible; negativa: hay holgura (capacidad ociosa, desempleo). Valores entre −0,5% y +0,5% se leen como cercanos al potencial.",
                "El potencial no se observa: se estima. Este gráfico usa un filtro Hodrick-Prescott (HP) en tiempo real, que en cada trimestre solo usa la información disponible hasta ese momento, para no reescribir la historia con datos posteriores.",
                "El colapso de 2020 aparece como una brecha muy negativa; los trimestres 2020T2–2021T2 se excluyen al estimar la tendencia para que el choque no deforme la capacidad.",
                "El último dato del PIB se revisa en publicaciones siguientes y el filtro es menos preciso al final de la muestra: conviene contrastar con la página Ciclo, donde la brecha se mide con cinco métodos.",
            ],
            "formulas": [
                ["Brecha del producto", "brecha<sub>t</sub> = 100 × (ln Y<sub>t</sub> − ln Y*<sub>t</sub>)",
                 "Y = PIB real desestacionalizado del trimestre t; Y* = capacidad (tendencia HP en tiempo real)"],
                ["Filtro HP en tiempo real", "Y*<sub>t</sub> = último punto de τ que minimiza Σ<sub>s≤t</sub>(y<sub>s</sub> − τ<sub>s</sub>)<sup>2</sup> + λ Σ(Δ<sup>2</sup>τ<sub>s</sub>)<sup>2</sup>",
                 "y = 100 × ln PIB; τ = tendencia; λ = 1.600 (trimestral); solo datos hasta t; 2020T2–2021T2 interpolados"],
                ["Capacidad en pesos", "Y*<sub>t</sub> = Y<sub>t</sub> × e<sup>−brecha<sub>t</sub> ÷ 100</sup>",
                 "convierte la brecha en el nivel de capacidad graficado (billones de COP de 2015)"],
            ],
        },
        "en": {
            "que": "Compares what Colombia's economy produces each quarter (seasonally adjusted real GDP) with its capacity, i.e. potential "
                   "GDP: the level it can sustain without generating inflationary pressure. The distance between the two is the output "
                   "gap, the core thermometer of the cycle: it tells whether the economy is overheating or has idle capacity.",
            "leer": "Top panel: the blue line is real GDP and the grey dashed line is capacity, in trillions of 2015 pesos per quarter "
                    "(left axis). The green area appears when GDP exceeds capacity and the orange area when it falls below. Bottom "
                    "panel: bars with the gap in percent, green when positive and orange when negative, with a zero line. The initial "
                    "view shows the last ten years; the gap series starts five years after the first GDP observation because the "
                    "filter needs at least 20 quarters.",
            "importa": "The gap summarises the balance between demand and supply. A positive gap usually comes with price pressure and a "
                       "tight labour market, and it is one of the variables Banco de la República (BanRep, the central bank) monitors "
                       "when setting its policy rate (TPM). For an investor, placing the economy against its capacity helps read the "
                       "backdrop for inflation, interest rates and corporate earnings.",
            "interpretar": [
                "Positive gap: output is above its sustainable level; negative: there is slack (idle capacity, unemployment). Values between −0.5% and +0.5% read as close to potential.",
                "Potential output is not observed; it is estimated. This chart uses a real-time Hodrick-Prescott (HP) filter that, at each quarter, only uses information available at that time, so history is not rewritten with later data.",
                "The 2020 collapse shows up as a deeply negative gap; quarters 2020Q2–2021Q2 are excluded when estimating the trend so the shock does not distort capacity.",
                "The latest GDP figure is revised in later releases and the filter is less precise at the end of the sample: cross-check with the Cycle page, where the gap is measured with five methods.",
            ],
            "formulas": [
                ["Output gap", "gap<sub>t</sub> = 100 × (ln Y<sub>t</sub> − ln Y*<sub>t</sub>)",
                 "Y = seasonally adjusted real GDP in quarter t; Y* = capacity (real-time HP trend)"],
                ["Real-time HP filter", "Y*<sub>t</sub> = last point of the τ minimising Σ<sub>s≤t</sub>(y<sub>s</sub> − τ<sub>s</sub>)<sup>2</sup> + λ Σ(Δ<sup>2</sup>τ<sub>s</sub>)<sup>2</sup>",
                 "y = 100 × ln GDP; τ = trend; λ = 1,600 (quarterly); data up to t only; 2020Q2–2021Q2 interpolated"],
                ["Capacity in pesos", "Y*<sub>t</sub> = Y<sub>t</sub> × e<sup>−gap<sub>t</sub> ÷ 100</sup>",
                 "turns the gap into the plotted capacity level (trillions of 2015 COP)"],
            ],
        },
    },
    "g-cap-sectores": {
        "es": {
            "que": "Muestra, trimestre a trimestre, si cada una de las 12 grandes ramas de actividad de las cuentas nacionales produce "
                   "por encima o por debajo de su propia tendencia. Permite ver si la holgura o el recalentamiento de la economía es "
                   "general o se concentra en unos pocos sectores, y cómo ha cambiado ese mapa en el tiempo.",
            "leer": "Cada fila es un sector y cada columna un trimestre, desde 2016. El color es la brecha del sector en porcentaje: "
                    "azul cuando produce por encima de su tendencia, naranja cuando produce por debajo y casi blanco cuando está cerca "
                    "de ella. La escala de color va de −8% a +8%; valores más extremos (como los de 2020) se muestran con el color del "
                    "límite. Las filas están ordenadas según la brecha del último trimestre. Al pasar el cursor se ve el valor exacto.",
            "importa": "Una brecha agregada positiva puede esconder sectores con mucha holgura. Saber dónde está la presión sirve para "
                       "entender qué precios y qué mercados laborales se tensan, y qué ramas tienen espacio para crecer sin cuellos de "
                       "botella. Para un inversionista, es una lectura del momento cíclico de cada industria.",
            "interpretar": [
                "Columnas mayoritariamente azules indican una expansión generalizada; una mezcla de azules y naranjas, un ciclo desigual entre sectores.",
                "Un sector que pasa de naranja a azul ha cerrado su holgura; el cambio inverso señala pérdida de dinamismo frente a su propia historia.",
                "Los niveles sectoriales del DANE vienen sin desestacionalizar: se usa la suma de 4 trimestres, que elimina la estacionalidad, antes de filtrar. Eso suaviza la serie y hace que los giros aparezcan con algo de rezago.",
                "Cada brecha se mide contra la tendencia del propio sector (no contra la economía): un sector en declive estructural puede verse cerca de cero aunque se contraiga. Complementa al gráfico de barras contiguo y a la casilla de amplitud de la página Ciclo.",
            ],
            "formulas": [
                ["Nivel anualizado", "N<sub>i,t</sub> = Σ<sub>k=0..3</sub> X<sub>i,t−k</sub>",
                 "X = valor agregado real trimestral (datos originales) del sector i"],
                ["Brecha sectorial", "b<sub>i,t</sub> = 100 × (ln N<sub>i,t</sub> − ln T<sub>i,t</sub>)",
                 "T = tendencia HP en tiempo real (λ = 1.600, solo datos hasta t, 2020T2–2021T2 interpolados)"],
            ],
        },
        "en": {
            "que": "Shows, quarter by quarter, whether each of the 12 broad industries in the national accounts is producing above or below "
                   "its own trend. It reveals whether slack or overheating is economy-wide or concentrated in a few sectors, and how that "
                   "picture has shifted over time.",
            "leer": "Each row is a sector and each column a quarter, from 2016. Colour is the sector's gap in percent: blue when producing "
                    "above trend, orange when below and near-white when close to it. The colour scale runs from −8% to +8%; more extreme "
                    "values (such as those of 2020) take the colour of the bound. Rows are ordered by the latest quarter's gap. Hover "
                    "for the exact value.",
            "importa": "A positive aggregate gap can hide sectors with ample slack. Knowing where pressure sits helps understand which prices "
                       "and labour markets are tightening and which industries have room to grow without bottlenecks. For an investor, it "
                       "is a reading of each industry's cyclical position.",
            "interpretar": [
                "Mostly blue columns signal a broad-based expansion; a mix of blue and orange, an uneven cycle across sectors.",
                "A sector moving from orange to blue has closed its slack; the reverse signals a loss of momentum relative to its own history.",
                "DANE's sector levels are not seasonally adjusted: a 4-quarter sum, which removes seasonality, is taken before filtering. This smooths the series and makes turns appear with some lag.",
                "Each gap is measured against the sector's own trend (not the economy's): a sector in structural decline can sit near zero while shrinking. It complements the adjacent bar chart and the breadth panel on the Cycle page.",
            ],
            "formulas": [
                ["Annualised level", "N<sub>i,t</sub> = Σ<sub>k=0..3</sub> X<sub>i,t−k</sub>",
                 "X = quarterly real value added (original data) of sector i"],
                ["Sector gap", "b<sub>i,t</sub> = 100 × (ln N<sub>i,t</sub> − ln T<sub>i,t</sub>)",
                 "T = real-time HP trend (λ = 1,600, data up to t only, 2020Q2–2021Q2 interpolated)"],
            ],
        },
    },
    "g-cap-sectores-hoy": {
        "es": {
            "que": "Es la última columna del mapa de calor de sectores, presentada como ranking: la distancia porcentual entre lo que "
                   "produce cada una de las 12 ramas en el trimestre más reciente y su tendencia. Muestra de un vistazo qué sectores "
                   "trabajan sin holgura y cuáles tienen capacidad disponible.",
            "leer": "Barras horizontales, una por sector, con la brecha en porcentaje sobre el eje horizontal y el valor escrito al "
                    "final de cada barra. Azul: el sector produce por encima de su tendencia; naranja: por debajo. La línea vertical "
                    "marca el cero. Los sectores están ordenados de mayor brecha (arriba) a menor (abajo) y el eje es simétrico "
                    "alrededor de cero.",
            "importa": "Cuando pocos sectores están por encima de su tendencia, el crecimiento puede convivir con presiones de precios "
                       "acotadas; cuando la mayoría lo está, la presión tiende a ser más general. El ranking también identifica las "
                       "ramas que hoy jalonan o frenan la actividad, útil para leer la exposición sectorial de empresas y carteras.",
            "interpretar": [
                "Barras azules largas: sectores con poca holgura, donde pueden aparecer cuellos de botella o presiones de costos.",
                "Barras naranjas: producción por debajo de la tendencia del propio sector; no implica necesariamente caída anual, sino menor ritmo que su historia.",
                "El número de barras azules es el mismo que la casilla de amplitud («sectores sobre su tendencia») de la página Ciclo.",
                "El dato del último trimestre es el más expuesto a revisiones del DANE y al sesgo de fin de muestra del filtro.",
            ],
            "formulas": [
                ["Brecha sectorial", "b<sub>i,T</sub> = 100 × (ln N<sub>i,T</sub> − ln T<sub>i,T</sub>)",
                 "N = suma de 4 trimestres del valor agregado real del sector i; T = tendencia HP en tiempo real (λ = 1.600); T = último trimestre"],
            ],
        },
        "en": {
            "que": "This is the last column of the sector heatmap, shown as a ranking: the percentage distance between what each of the 12 "
                   "industries produces in the latest quarter and its trend. It shows at a glance which sectors run without slack and "
                   "which have spare capacity.",
            "leer": "Horizontal bars, one per sector, with the gap in percent on the horizontal axis and the value printed at the end of "
                    "each bar. Blue: the sector produces above its trend; orange: below. The vertical line marks zero. Sectors are "
                    "ordered from largest gap (top) to smallest (bottom) and the axis is symmetric around zero.",
            "importa": "When few sectors are above trend, growth can coexist with contained price pressure; when most are, pressure tends "
                       "to be broader. The ranking also identifies which industries are currently pulling activity up or holding it back, "
                       "useful for reading the sector exposure of companies and portfolios.",
            "interpretar": [
                "Long blue bars: sectors with little slack, where bottlenecks or cost pressures can emerge.",
                "Orange bars: output below the sector's own trend; this does not necessarily mean an annual decline, only a slower pace than its history.",
                "The number of blue bars matches the breadth panel («sectors above trend») on the Cycle page.",
                "The latest quarter is the most exposed to DANE revisions and to the filter's end-of-sample bias.",
            ],
            "formulas": [
                ["Sector gap", "b<sub>i,T</sub> = 100 × (ln N<sub>i,T</sub> − ln T<sub>i,T</sub>)",
                 "N = 4-quarter sum of sector i's real value added; T = real-time HP trend (λ = 1,600); T = latest quarter"],
            ],
        },
    },
    "g-cap-subutilizacion": {
        "es": {
            "que": "Mide la holgura del mercado laboral con tres indicadores de la Organización Internacional del Trabajo (OIT), del más "
                   "estrecho al más amplio. La tasa de desempleo solo cuenta a quienes buscan empleo y no lo tienen; las otras dos "
                   "suman a quienes trabajan menos horas de las que quieren y a quienes quieren trabajar pero no buscan.",
            "leer": "Tres líneas mensuales, cada una como promedio móvil de 12 meses, en porcentaje: azul, tasa de desempleo (TD); verde, "
                    "desempleo más subempleo por horas (TCSD); naranja y más gruesa, la medida compuesta de subutilización (MCSFT), que "
                    "agrega la fuerza de trabajo potencial. El eje vertical parte de cero. Datos del total nacional de la Gran Encuesta "
                    "Integrada de Hogares (GEIH) del DANE, sin desestacionalizar.",
            "importa": "El desempleo por sí solo subestima la holgura cuando muchas personas trabajan pocas horas o se desaniman y dejan de "
                       "buscar. Las medidas amplias dan una visión más completa del espacio que tiene la economía para crecer sin presionar "
                       "los salarios, algo que pesa en la lectura de inflación y de política monetaria.",
            "interpretar": [
                "Si la distancia entre la línea naranja y la azul crece, la holgura oculta (subempleo y desaliento) aumenta aunque el desempleo no cambie.",
                "Las tres medidas bajando juntas indican un mercado laboral que absorbe trabajadores de forma amplia.",
                "El promedio de 12 meses elimina la estacionalidad y el ruido de la encuesta, pero hace que los giros se vean con rezago; por eso la TD de este gráfico no coincide con la tasa desestacionalizada mensual que se usa en otras páginas.",
                "La MCSFT usa un denominador distinto (fuerza de trabajo ampliada), así que no es la suma simple de las otras dos tasas.",
            ],
            "formulas": [
                ["Tasa de desempleo", "TD = D ÷ FT × 100", "D = desocupados; FT = fuerza de trabajo (ocupados + desocupados)"],
                ["Desempleo + subempleo", "TCSD = (D + S) ÷ FT × 100", "S = subocupados por insuficiencia de horas"],
                ["Medida compuesta", "MCSFT = (D + S + FTP) ÷ (FT + FTP) × 100", "FTP = fuerza de trabajo potencial: personas disponibles que quieren trabajar pero no buscan"],
                ["Promedio móvil", "x̄<sub>t</sub> = (1 ÷ 12) × Σ<sub>k=0..11</sub> x<sub>t−k</sub>", "x = cada tasa mensual"],
            ],
        },
        "en": {
            "que": "Measures labour-market slack with three International Labour Organization (ILO) indicators, from narrowest to broadest. "
                   "The unemployment rate only counts people searching for work without a job; the other two add those working fewer "
                   "hours than they want and those who want to work but are not searching.",
            "leer": "Three monthly lines, each a 12-month moving average, in percent: blue, unemployment rate (TD); green, unemployment plus "
                    "time-related underemployment (TCSD); orange and thicker, the composite underutilisation measure (MCSFT), which adds "
                    "the potential labour force. The vertical axis starts at zero. National totals from DANE's Integrated Household "
                    "Survey (GEIH), not seasonally adjusted.",
            "importa": "Unemployment alone understates slack when many people work short hours or become discouraged and stop searching. "
                       "Broader measures give a fuller picture of how much room the economy has to grow without pushing up wages, which "
                       "matters for reading inflation and monetary policy.",
            "interpretar": [
                "A widening distance between the orange and blue lines means hidden slack (underemployment and discouragement) is rising even if unemployment is flat.",
                "All three measures falling together signal a labour market absorbing workers broadly.",
                "The 12-month average removes seasonality and survey noise but makes turns appear late; that is why the TD here differs from the monthly seasonally adjusted rate used on other pages.",
                "MCSFT uses a different denominator (extended labour force), so it is not the simple sum of the other two rates.",
            ],
            "formulas": [
                ["Unemployment rate", "TD = D ÷ LF × 100", "D = unemployed; LF = labour force (employed + unemployed)"],
                ["Unemployment + underemployment", "TCSD = (D + S) ÷ LF × 100", "S = time-related underemployed"],
                ["Composite measure", "MCSFT = (D + S + PLF) ÷ (LF + PLF) × 100", "PLF = potential labour force: available people who want to work but are not searching"],
                ["Moving average", "x̄<sub>t</sub> = (1 ÷ 12) × Σ<sub>k=0..11</sub> x<sub>t−k</sub>", "x = each monthly rate"],
            ],
        },
    },
    "g-cap-desempleo": {
        "es": {
            "que": "Compara la tasa de desempleo con su propia tendencia de largo plazo. La tendencia aproxima el desempleo compatible con "
                   "una economía en su capacidad; la distancia entre ambas es la «brecha de desempleo», la contraparte laboral de la "
                   "brecha del producto.",
            "leer": "Línea azul: tasa de desempleo desestacionalizada (GEIH, DANE), promedio de los tres meses de cada trimestre, en "
                    "porcentaje. Línea gris punteada: su tendencia estimada con un filtro Hodrick-Prescott de dos colas (λ = 1.600). El "
                    "eje vertical va de 0% a 25% y el gráfico arranca en 2010. El salto de 2020 se ve en la línea azul, pero no arrastra "
                    "la tendencia porque esos trimestres se excluyen e interpolan al estimarla.",
            "importa": "Un desempleo por debajo de su tendencia indica un mercado laboral apretado, con más presión sobre salarios y, por "
                       "esa vía, sobre la inflación de servicios. Por encima, hay trabajadores disponibles y la presión es menor. Es una de "
                       "las señales que se combinan con la brecha del producto para juzgar cuánta holgura tiene la economía.",
            "interpretar": [
                "Azul debajo de la punteada: mercado laboral apretado; azul encima: holgura laboral.",
                "La tendencia no es una tasa «natural» oficial: es un suavizado estadístico. Su valor final cambia a medida que llegan datos nuevos, porque el filtro de dos colas usa toda la muestra.",
                "Se excluyen 2020T2–2021T2 al estimar la tendencia y se interpolan esos trimestres (la nota del gráfico dice «sin 2020–2021»).",
                "La relación con la brecha del producto se mide en el gráfico de la ley de Okun de la página Ciclo.",
            ],
            "formulas": [
                ["Promedio trimestral", "u<sub>q</sub> = (u<sub>m1</sub> + u<sub>m2</sub> + u<sub>m3</sub>) ÷ 3", "u = tasa de desempleo desestacionalizada de cada mes del trimestre"],
                ["Brecha de desempleo", "b<sup>u</sup><sub>q</sub> = u<sub>q</sub> − u*<sub>q</sub>", "u* = tendencia HP de dos colas (λ = 1.600), en puntos porcentuales (pp)"],
            ],
        },
        "en": {
            "que": "Compares the unemployment rate with its own long-run trend. The trend approximates the unemployment rate consistent with "
                   "an economy at capacity; the distance between the two is the «unemployment gap», the labour-market counterpart of the "
                   "output gap.",
            "leer": "Blue line: seasonally adjusted unemployment rate (GEIH, DANE), average of the three months in each quarter, in percent. "
                    "Grey dotted line: its trend from a two-sided Hodrick-Prescott filter (λ = 1,600). The vertical axis runs from 0% to "
                    "25% and the chart starts in 2010. The 2020 spike is visible in the blue line but does not drag the trend, because "
                    "those quarters are excluded and interpolated when estimating it.",
            "importa": "Unemployment below trend points to a tight labour market, with more pressure on wages and, through them, on services "
                       "inflation. Above trend, workers are available and pressure is lower. It is one of the signals combined with the "
                       "output gap to judge how much slack the economy has.",
            "interpretar": [
                "Blue below dotted: tight labour market; blue above: labour slack.",
                "The trend is not an official «natural» rate: it is a statistical smoother. Its end value changes as new data arrive, because the two-sided filter uses the whole sample.",
                "Quarters 2020Q2–2021Q2 are excluded and interpolated when estimating the trend (the chart note says «excluding 2020–2021»).",
                "The link with the output gap is measured in the Okun's law chart on the Cycle page.",
            ],
            "formulas": [
                ["Quarterly average", "u<sub>q</sub> = (u<sub>m1</sub> + u<sub>m2</sub> + u<sub>m3</sub>) ÷ 3", "u = seasonally adjusted unemployment rate in each month of the quarter"],
                ["Unemployment gap", "b<sup>u</sup><sub>q</sub> = u<sub>q</sub> − u*<sub>q</sub>", "u* = two-sided HP trend (λ = 1,600), in percentage points (pp)"],
            ],
        },
    },
    "g-cap-regiones": {
        "es": {
            "que": "Compara el tamaño real de la economía de cada uno de los 33 departamentos (incluida Bogotá) en el último año publicado "
                   "con su tamaño en 2019, el último año antes de la pandemia. Muestra qué regiones ya superaron su nivel previo al "
                   "choque y cuáles siguen rezagadas.",
            "leer": "Una barra horizontal por departamento con la variación porcentual del PIB real entre 2019 y el último año disponible; "
                    "el valor aparece al final de cada barra. Azul: la economía es más grande que en 2019; naranja: más pequeña. La línea "
                    "vertical continua marca el cero y la punteada el resultado de Colombia en conjunto. Los departamentos van de mayor "
                    "variación (arriba) a menor (abajo).",
            "importa": "La recuperación nacional puede ocultar regiones que no han vuelto a su nivel previo. Las diferencias reflejan la "
                       "estructura productiva de cada departamento (por ejemplo, la dependencia de la minería) y orientan sobre dónde está "
                       "el dinamismo de la demanda, el empleo y la base de clientes regional.",
            "interpretar": [
                "Barras a la derecha de la línea punteada: el departamento creció más que el país desde 2019; a la izquierda, menos.",
                "Una variación negativa indica que la economía departamental aún produce menos, en términos reales, que antes de la pandemia.",
                "Las cuentas departamentales se publican con rezago anual y el último año es preliminar: puede revisarse en la siguiente publicación.",
                "Para ver de qué vive cada región y qué tan concentrada está, compare con los gráficos de estructura productiva y diversificación.",
            ],
            "formulas": [
                ["Variación frente a 2019", "v<sub>d</sub> = (Y<sub>d,A</sub> ÷ Y<sub>d,2019</sub> − 1) × 100",
                 "Y = PIB real del departamento d (volúmenes encadenados, base 2015); A = último año publicado"],
            ],
        },
        "en": {
            "que": "Compares the real size of the economy of each of the 33 departments (including Bogotá) in the latest published year "
                   "with its size in 2019, the last year before the pandemic. It shows which regions have already exceeded their pre-shock "
                   "level and which are still lagging.",
            "leer": "One horizontal bar per department with the percentage change in real GDP between 2019 and the latest year available; "
                    "the value is printed at the end of each bar. Blue: the economy is larger than in 2019; orange: smaller. The solid "
                    "vertical line marks zero and the dotted one the result for Colombia as a whole. Departments run from largest change "
                    "(top) to smallest (bottom).",
            "importa": "The national recovery can mask regions that have not returned to their earlier level. The differences reflect each "
                       "department's production structure (for example, reliance on mining) and indicate where demand, jobs and the "
                       "regional customer base are most dynamic.",
            "interpretar": [
                "Bars to the right of the dotted line: the department grew more than the country since 2019; to the left, less.",
                "A negative change means the departmental economy still produces less, in real terms, than before the pandemic.",
                "Departmental accounts are released with an annual lag and the latest year is preliminary: it can be revised in the next release.",
                "To see what each region lives on and how concentrated it is, compare with the production-structure and diversification charts.",
            ],
            "formulas": [
                ["Change versus 2019", "v<sub>d</sub> = (Y<sub>d,A</sub> ÷ Y<sub>d,2019</sub> − 1) × 100",
                 "Y = real GDP of department d (chain-linked volumes, base 2015); A = latest published year"],
            ],
        },
    },
    "g-cap-estructura": {
        "es": {
            "que": "Muestra de qué vive cada departamento: el peso de cada una de las 12 grandes ramas de actividad en su valor agregado. "
                   "Revela regiones dominadas por un solo sector (minería, agro, Gobierno) frente a economías más mezcladas de industria "
                   "y servicios.",
            "leer": "Mapa de calor: cada fila es un departamento y cada columna una rama (agro, minería, industria, energía y agua, "
                    "construcción, comercio y transporte, comunicaciones, finanzas, inmobiliarias, servicios profesionales, Gobierno-"
                    "educación-salud, arte y otros). El color es la participación en porcentaje, de blanco (0%) a azul oscuro; la escala "
                    "se satura en 40%, así que pesos mayores se ven con el tono más oscuro. Los departamentos van ordenados por tamaño de "
                    "su PIB, del más grande arriba al más pequeño abajo. Cada fila suma 100%.",
            "importa": "La composición sectorial determina cómo responde cada región a los choques: precios del petróleo y del carbón, "
                       "clima, gasto público o crédito. Para un inversionista, indica la sensibilidad regional a ciclos de materias primas "
                       "y la profundidad de los mercados de servicios en cada territorio.",
            "interpretar": [
                "Una celda muy oscura aislada en una fila señala dependencia de un sector; filas con tonos medios repartidos indican una economía diversificada.",
                "Se usan precios corrientes del último año: un salto en el precio de un producto (por ejemplo, el petróleo) puede aumentar la participación de la minería sin que cambie el volumen producido.",
                "Las participaciones se calculan sobre el valor agregado sin impuestos, por lo que difieren levemente de las del PIB.",
                "El gráfico de diversificación contiguo resume cada fila en un solo número.",
            ],
            "formulas": [
                ["Participación sectorial", "s<sub>i,d</sub> = VA<sub>i,d</sub> ÷ Σ<sub>j</sub> VA<sub>j,d</sub> × 100",
                 "VA = valor agregado a precios corrientes de la rama i en el departamento d; suma sobre las 12 ramas (sin impuestos)"],
            ],
        },
        "en": {
            "que": "Shows what each department lives on: the weight of each of the 12 broad industries in its value added. It reveals regions "
                   "dominated by a single sector (mining, farming, government) versus more mixed economies of manufacturing and services.",
            "leer": "Heatmap: each row is a department and each column an industry (farming, mining, manufacturing, utilities, "
                    "construction, trade and transport, communications, finance, real estate, professional services, government-"
                    "education-health, arts and other). Colour is the share in percent, from white (0%) to dark blue; the scale saturates "
                    "at 40%, so larger shares take the darkest shade. Departments are ordered by GDP size, largest at the top. Each row "
                    "adds up to 100%.",
            "importa": "Sector mix determines how each region responds to shocks: oil and coal prices, weather, public spending or credit. "
                       "For an investor, it indicates regional sensitivity to commodity cycles and the depth of service markets in each "
                       "territory.",
            "interpretar": [
                "A single very dark cell in a row signals dependence on one sector; rows with mid-tones spread across columns indicate a diversified economy.",
                "Current prices of the latest year are used: a jump in a product's price (oil, for example) can raise mining's share without any change in volume.",
                "Shares are computed on value added excluding taxes, so they differ slightly from GDP shares.",
                "The adjacent diversification chart summarises each row in a single number.",
            ],
            "formulas": [
                ["Sector share", "s<sub>i,d</sub> = VA<sub>i,d</sub> ÷ Σ<sub>j</sub> VA<sub>j,d</sub> × 100",
                 "VA = value added at current prices of industry i in department d; sum over the 12 industries (excluding taxes)"],
            ],
        },
    },
    "g-cap-diversificacion": {
        "es": {
            "que": "Resume en un número qué tan diversificada es la economía de cada departamento: el «número equivalente de sectores», "
                   "es decir, cuántos sectores del mismo tamaño producirían la misma concentración observada. Es el inverso del índice "
                   "de Herfindahl-Hirschman, una medida estándar de concentración.",
            "leer": "Una barra horizontal por departamento, con el valor escrito al final. El eje va de 0 a 12: 12 sería el máximo "
                    "teórico (las 12 ramas con el mismo peso) y 1 una economía que depende de un único sector. Los departamentos están "
                    "ordenados del más diversificado (arriba) al más concentrado (abajo). Se calcula con las participaciones del "
                    "gráfico de estructura productiva.",
            "importa": "Las regiones concentradas son más vulnerables cuando su sector principal se frena, por ejemplo ante una caída "
                       "de precios de materias primas o un cambio regulatorio. Las diversificadas suelen tener ciclos más estables. Para "
                       "evaluar riesgos regionales, este número complementa al crecimiento y al tamaño de cada economía.",
            "interpretar": [
                "Un valor alto (cerca de 8 o más) indica una economía repartida entre muchas ramas; un valor bajo (cerca de 2 o 3), una fuerte dependencia de una o dos.",
                "El índice no dice cuál es el sector dominante: para eso, vea la fila del departamento en el mapa de estructura productiva.",
                "Como usa precios corrientes, puede moverse con los precios relativos (por ejemplo, del petróleo) aunque la estructura física no cambie.",
                "La desagregación en 12 ramas limita el valor máximo y oculta la diversificación dentro de cada rama.",
            ],
            "formulas": [
                ["Índice de Herfindahl-Hirschman", "HHI<sub>d</sub> = Σ<sub>i</sub> s<sub>i,d</sub><sup>2</sup>",
                 "s = participación (en tanto por uno) de la rama i en el valor agregado del departamento d"],
                ["Número equivalente de sectores", "N<sub>d</sub> = 1 ÷ HHI<sub>d</sub>", "va de 1 (un solo sector) a 12 (12 ramas iguales)"],
            ],
        },
        "en": {
            "que": "Summarises in one number how diversified each department's economy is: the «equivalent number of sectors», i.e. how many "
                   "equal-sized sectors would produce the observed concentration. It is the inverse of the Herfindahl-Hirschman index, a "
                   "standard concentration measure.",
            "leer": "One horizontal bar per department, with the value printed at the end. The axis runs from 0 to 12: 12 would be the "
                    "theoretical maximum (all 12 industries with the same weight) and 1 an economy relying on a single sector. Departments "
                    "are ordered from most diversified (top) to most concentrated (bottom). It is computed from the shares in the "
                    "production-structure chart.",
            "importa": "Concentrated regions are more vulnerable when their main sector slows, for instance after a fall in commodity prices "
                       "or a regulatory change. Diversified ones tend to have steadier cycles. When assessing regional risk, this number "
                       "complements each economy's growth and size.",
            "interpretar": [
                "A high value (around 8 or more) indicates an economy spread across many industries; a low value (around 2 or 3), heavy reliance on one or two.",
                "The index does not say which sector dominates: for that, look at the department's row in the production-structure map.",
                "Because it uses current prices, it can move with relative prices (oil, for example) even if the physical structure is unchanged.",
                "The 12-industry breakdown caps the maximum value and hides diversification within each industry.",
            ],
            "formulas": [
                ["Herfindahl-Hirschman index", "HHI<sub>d</sub> = Σ<sub>i</sub> s<sub>i,d</sub><sup>2</sup>",
                 "s = share (as a fraction) of industry i in department d's value added"],
                ["Equivalent number of sectors", "N<sub>d</sub> = 1 ÷ HHI<sub>d</sub>", "ranges from 1 (one sector) to 12 (12 equal industries)"],
            ],
        },
    },
    "v-mapa-regiones": {
        "es": {
            "que": "Es un mapa esquemático de Colombia en el que cada casilla es un departamento, ubicado aproximadamente en su posición "
                   "geográfica. Permite ver la geografía de cuatro medidas regionales: el crecimiento del último año, el tamaño de la "
                   "economía frente a 2019, el PIB por persona y el desempleo de la ciudad capital.",
            "leer": "Los botones eligen la medida (al abrir, «Frente a 2019»). Cada casilla lleva la abreviatura del departamento y su "
                    "valor; el color sigue una escala divergente de siete tonos: azul para valores altos, tonos crema para valores "
                    "intermedios y naranja-terracota para valores bajos. En desempleo la escala se invierte: más desempleo es naranja. "
                    "Tramos centrales: crecimiento entre −0,25% y 0,25%; frente a 2019 entre −1% y 1%; PIB por persona entre 85 y 115 "
                    "(Colombia = 100); desempleo entre 10% y 12%. Al pasar el cursor se ven todas las medidas y el sector principal.",
            "importa": "Las cifras nacionales esconden grandes diferencias territoriales. El mapa permite identificar de un vistazo "
                       "regiones dinámicas o rezagadas, de ingreso alto o bajo y con mercados laborales holgados o apretados, información "
                       "útil para decisiones de localización, distribución comercial o análisis de riesgo regional.",
            "interpretar": [
                "Crecimiento: variación real del PIB del departamento frente al año anterior. Frente a 2019: tamaño real de la economía comparado con el año previo a la pandemia.",
                "PIB por persona a precios corrientes, con Colombia = 100: 150 significa un ingreso por habitante 50% mayor al promedio nacional. Departamentos mineros con poca población pueden tener valores altos sin que eso refleje el ingreso de los hogares.",
                "Desempleo: tasa de la ciudad capital en año móvil (GEIH, 32 ciudades), no la del departamento; Cundinamarca queda sin dato porque Bogotá se muestra aparte. Las casillas sin dato tienen borde punteado.",
                "Mapa no a escala: el área de cada casilla no refleja superficie ni población. El último año de las cuentas departamentales es preliminar.",
            ],
            "formulas": [
                ["Crecimiento anual", "g<sub>d</sub> = (Y<sub>d,A</sub> ÷ Y<sub>d,A−1</sub> − 1) × 100", "Y = PIB real del departamento d; A = último año"],
                ["Frente a 2019", "v<sub>d</sub> = (Y<sub>d,A</sub> ÷ Y<sub>d,2019</sub> − 1) × 100", "Y = PIB real (volúmenes encadenados, base 2015)"],
                ["PIB por persona relativo", "I<sub>d</sub> = 100 × pc<sub>d</sub> ÷ pc<sub>COL</sub>", "pc = PIB corriente por habitante del departamento y de Colombia"],
            ],
        },
        "en": {
            "que": "A schematic map of Colombia in which each tile is a department, placed roughly where it lies. It shows the geography of "
                   "four regional measures: last year's growth, the size of the economy versus 2019, GDP per person and capital-city "
                   "unemployment.",
            "leer": "Buttons pick the measure (it opens on «Versus 2019»). Each tile shows the department's abbreviation and value; colour "
                    "follows a seven-step diverging scale: blue for high values, cream tones for middling values and terracotta-orange for "
                    "low values. For unemployment the scale is inverted: more unemployment is orange. Central bands: growth between −0.25% "
                    "and 0.25%; versus 2019 between −1% and 1%; GDP per person between 85 and 115 (Colombia = 100); unemployment between "
                    "10% and 12%. Hover to see every measure and the main sector.",
            "importa": "National figures hide large territorial differences. The map identifies at a glance dynamic or lagging regions, high- "
                       "or low-income ones, and loose or tight labour markets, information useful for location decisions, commercial "
                       "distribution or regional risk analysis.",
            "interpretar": [
                "Growth: real GDP change of the department versus the previous year. Versus 2019: real size of the economy compared with the year before the pandemic.",
                "GDP per person at current prices, with Colombia = 100: 150 means income per head 50% above the national average. Mining departments with small populations can score high without that reflecting household income.",
                "Unemployment: the capital city's rate over a rolling year (GEIH, 32 cities), not the department's; Cundinamarca has no value because Bogotá is shown separately. Tiles without data have a dashed border.",
                "Not to scale: tile area reflects neither land area nor population. The latest year of departmental accounts is preliminary.",
            ],
            "formulas": [
                ["Annual growth", "g<sub>d</sub> = (Y<sub>d,A</sub> ÷ Y<sub>d,A−1</sub> − 1) × 100", "Y = real GDP of department d; A = latest year"],
                ["Versus 2019", "v<sub>d</sub> = (Y<sub>d,A</sub> ÷ Y<sub>d,2019</sub> − 1) × 100", "Y = real GDP (chain-linked volumes, base 2015)"],
                ["Relative GDP per person", "I<sub>d</sub> = 100 × pc<sub>d</sub> ÷ pc<sub>COL</sub>", "pc = current-price GDP per inhabitant of the department and of Colombia"],
            ],
        },
    },
    # ------------------------------------------------------------------ CICLO
    "g-ciclo-reloj": {
        "es": {
            "que": "El reloj del ciclo, una herramienta de la OCDE, ubica cada trimestre según dos preguntas: ¿la economía produce por "
                   "encima o por debajo de su capacidad? y ¿esa distancia está aumentando o disminuyendo? La combinación define cuatro "
                   "fases: expansión, desaceleración, contracción y recuperación.",
            "leer": "Eje horizontal: brecha del producto en porcentaje (a la derecha del cero, por encima de la capacidad). Eje vertical: "
                    "cambio de la brecha en los últimos 2 trimestres, en puntos porcentuales (arriba, la brecha aumenta). Los cuadrantes "
                    "llevan el color de su fase: verde expansión (arriba a la derecha), ámbar desaceleración (abajo a la derecha), rojo "
                    "contracción (abajo a la izquierda) y azul recuperación (arriba a la izquierda). Cada punto es un trimestre, las "
                    "flechas unen trimestres consecutivos y el punto grande es el elegido con el deslizador; los botones muestran la "
                    "estela de 1, 2 o 3 años. Los ejes se ajustan al recorrido visible.",
            "importa": "No basta saber si la economía está por encima de su capacidad: importa hacia dónde se mueve. Una economía recalentada "
                       "que pierde impulso (desaceleración) se lee de forma muy distinta a una que sigue acelerando (expansión). La fase es "
                       "un marco común para interpretar inflación, tasas de interés y desempeño de los activos.",
            "interpretar": [
                "Las economías tienden a recorrer el reloj en el sentido de las agujas: expansión → desaceleración → contracción → recuperación; pero el recorrido puede saltarse fases o retroceder.",
                "Puntos cerca del centro indican una economía próxima a su capacidad y sin dirección clara: la fase en esos casos es frágil.",
                "La dirección usa el cambio en 2 trimestres para reducir el ruido de un solo dato.",
                "La brecha es la del filtro HP en tiempo real del gráfico de capacidad; otros métodos pueden ubicar el punto en otro cuadrante (vea el consenso de cinco métodos).",
            ],
            "formulas": [
                ["Nivel (eje horizontal)", "brecha<sub>t</sub> = 100 × (ln Y<sub>t</sub> − ln Y*<sub>t</sub>)", "Y = PIB real desestacionalizado; Y* = tendencia HP en tiempo real (λ = 1.600)"],
                ["Dirección (eje vertical)", "Δ<sub>t</sub> = brecha<sub>t</sub> − brecha<sub>t−2</sub>", "cambio en 2 trimestres, en pp"],
                ["Fase", "expansión: brecha ≥ 0 y Δ ≥ 0; desaceleración: brecha ≥ 0 y Δ < 0;<br>contracción: brecha < 0 y Δ < 0; recuperación: brecha < 0 y Δ ≥ 0", "cuadrante del reloj"],
            ],
        },
        "en": {
            "que": "The business-cycle clock, an OECD tool, places each quarter according to two questions: is the economy producing above or "
                   "below capacity? and is that distance widening or narrowing? The combination defines four phases: expansion, slowdown, "
                   "contraction and recovery.",
            "leer": "Horizontal axis: output gap in percent (right of zero, above capacity). Vertical axis: change in the gap over the last "
                    "2 quarters, in percentage points (up, the gap is rising). Quadrants carry their phase colour: green expansion (top "
                    "right), amber slowdown (bottom right), red contraction (bottom left) and blue recovery (top left). Each dot is a "
                    "quarter, arrows join consecutive quarters and the large dot is the one chosen with the slider; buttons show a trail "
                    "of 1, 2 or 3 years. Axes adjust to the visible path.",
            "importa": "Knowing whether the economy is above capacity is not enough: its direction matters. An overheated economy losing "
                       "momentum (slowdown) reads very differently from one still accelerating (expansion). The phase is a common framework "
                       "for interpreting inflation, interest rates and asset performance.",
            "interpretar": [
                "Economies tend to move clockwise: expansion → slowdown → contraction → recovery; but the path can skip phases or reverse.",
                "Dots near the centre indicate an economy close to capacity with no clear direction: the phase is fragile in those cases.",
                "Direction uses the 2-quarter change to reduce the noise of a single release.",
                "The gap is the real-time HP gap from the capacity chart; other methods may place the dot in another quadrant (see the five-method consensus).",
            ],
            "formulas": [
                ["Level (horizontal axis)", "gap<sub>t</sub> = 100 × (ln Y<sub>t</sub> − ln Y*<sub>t</sub>)", "Y = seasonally adjusted real GDP; Y* = real-time HP trend (λ = 1,600)"],
                ["Direction (vertical axis)", "Δ<sub>t</sub> = gap<sub>t</sub> − gap<sub>t−2</sub>", "2-quarter change, in pp"],
                ["Phase", "expansion: gap ≥ 0 and Δ ≥ 0; slowdown: gap ≥ 0 and Δ < 0;<br>contraction: gap < 0 and Δ < 0; recovery: gap < 0 and Δ ≥ 0", "quadrant of the clock"],
            ],
        },
    },
    "g-ciclo-hist": {
        "es": {
            "que": "Es la historia completa del reloj del ciclo: la brecha del producto de cada trimestre, coloreada según la fase en que "
                   "estaba la economía. Permite ver cuánto duran las fases, qué tan profundas son y cómo se suceden.",
            "leer": "Barras: brecha del producto (HP en tiempo real) en porcentaje, una por trimestre; el color indica la fase: verde "
                    "expansión, ámbar desaceleración, rojo contracción y azul recuperación. Línea negra punteada: cambio de la brecha en 2 "
                    "trimestres, en puntos porcentuales, que define la dirección. La franja gris sombrea los trimestres que se ven en el "
                    "reloj; al mover el deslizador del reloj la franja se desplaza. La línea horizontal marca el cero.",
            "importa": "La secuencia de fases muestra si la economía viene de un período largo de holgura o de recalentamiento, contexto "
                       "clave para leer la inflación y las decisiones de política monetaria. También permite comparar el momento actual con "
                       "episodios anteriores, como el colapso de 2020 y su rebote.",
            "interpretar": [
                "Barras verdes y ámbar arriba del cero: economía por encima de su capacidad; rojas y azules abajo: por debajo.",
                "Cuando la línea punteada cruza el cero, la brecha cambia de dirección y la fase rota (por ejemplo, de expansión a desaceleración).",
                "Cada barra usa solo la información disponible hasta ese trimestre (tiempo real), pero el PIB de los trimestres recientes puede revisarse.",
                "La versión mensual con el ISE (Ciclo mensual) se actualiza antes y sirve para anticipar el dato trimestral.",
            ],
            "formulas": [
                ["Brecha", "brecha<sub>t</sub> = 100 × (ln Y<sub>t</sub> − ln Y*<sub>t</sub>)", "Y* = tendencia HP en tiempo real (λ = 1.600), sin 2020T2–2021T2"],
                ["Dirección", "Δ<sub>t</sub> = brecha<sub>t</sub> − brecha<sub>t−2</sub>", "línea punteada, en pp"],
            ],
        },
        "en": {
            "que": "This is the full history behind the cycle clock: the output gap in each quarter, coloured by the phase the economy was in. "
                   "It shows how long phases last, how deep they are and how they follow each other.",
            "leer": "Bars: output gap (real-time HP) in percent, one per quarter; colour shows the phase: green expansion, amber slowdown, red "
                    "contraction and blue recovery. Black dotted line: 2-quarter change in the gap, in percentage points, which defines the "
                    "direction. The grey band shades the quarters shown in the clock; moving the clock's slider shifts the band. The "
                    "horizontal line marks zero.",
            "importa": "The sequence of phases shows whether the economy is coming out of a long stretch of slack or overheating, key context "
                       "for reading inflation and monetary policy decisions. It also allows comparing the current moment with earlier "
                       "episodes, such as the 2020 collapse and its rebound.",
            "interpretar": [
                "Green and amber bars above zero: output above capacity; red and blue below: output below capacity.",
                "When the dotted line crosses zero the gap changes direction and the phase rotates (for example, from expansion to slowdown).",
                "Each bar uses only information available up to that quarter (real time), but GDP for recent quarters can be revised.",
                "The monthly version based on the ISE (Monthly cycle) updates earlier and gives an early read of the quarterly figure.",
            ],
            "formulas": [
                ["Gap", "gap<sub>t</sub> = 100 × (ln Y<sub>t</sub> − ln Y*<sub>t</sub>)", "Y* = real-time HP trend (λ = 1,600), excluding 2020Q2–2021Q2"],
                ["Direction", "Δ<sub>t</sub> = gap<sub>t</sub> − gap<sub>t−2</sub>", "dotted line, in pp"],
            ],
        },
    },
    "g-consenso": {
        "es": {
            "que": "La brecha del producto no se observa: hay que estimarla, y cada método da una respuesta algo distinta. Este gráfico "
                   "muestra la brecha del último trimestre según cinco métodos estándar de la literatura y su mediana, para separar lo "
                   "que es una señal robusta de lo que depende del método elegido.",
            "leer": "Cada fila es un método y su punto marca la brecha en porcentaje, con el valor escrito al lado: azul si es positiva, "
                    "naranja si es negativa; una varilla gris une el cero con cada punto. La zona sombreada en verde, a la derecha del "
                    "cero, corresponde a producir por encima de la capacidad. La línea negra punteada vertical es la mediana de los cinco, "
                    "con su valor arriba. Los métodos van ordenados de menor (abajo) a mayor brecha (arriba).",
            "importa": "Las decisiones basadas en una sola estimación de la brecha pueden ser frágiles. Cuando los cinco métodos coinciden en "
                       "el signo, la lectura del ciclo es sólida; cuando se reparten a ambos lados del cero, la fase es incierta. Esto pesa "
                       "en cómo se interpretan la inflación y la postura del Banco de la República.",
            "interpretar": [
                "Puntos agrupados y del mismo lado del cero: lectura robusta. Puntos dispersos: incertidumbre alta; el rango (mínimo a máximo) mide esa incertidumbre.",
                "El HP en tiempo real solo usa datos hasta cada trimestre; el HP de dos colas, Christiano-Fitzgerald y Beveridge-Nelson usan toda la muestra, por lo que su valor reciente cambia cuando llegan datos nuevos.",
                "Hamilton compara el PIB con lo que anticipaba una regresión sobre su historia de hace 2 a 3 años; Beveridge-Nelson define el ciclo a partir del crecimiento esperado según un modelo autorregresivo.",
                "En todos los métodos la tendencia se estima sin 2020T2–2021T2. Valores de la mediana entre −0,5% y +0,5% se leen como economía cerca de su potencial.",
            ],
            "formulas": [
                ["Brecha (genérica)", "brecha<sub>m,t</sub> = 100 × ln Y<sub>t</sub> − τ<sub>m,t</sub>", "Y = PIB real desestacionalizado; τ<sub>m</sub> = tendencia (en 100 × log) según el método m"],
                ["Hamilton (2018)", "c<sub>t</sub> = y<sub>t</sub> − (β<sub>0</sub> + Σ<sub>k=0..3</sub> β<sub>k+1</sub> y<sub>t−8−k</sub>)", "y = 100 × ln PIB; β estimados por MCO (mínimos cuadrados ordinarios); horizonte 8 trimestres, 4 rezagos"],
                ["Christiano-Fitzgerald (2003)", "τ<sub>t</sub> = y<sub>t</sub> − CF<sub>6–32</sub>(y)<sub>t</sub>", "CF = filtro de banda que aísla ciclos de 6 a 32 trimestres (1,5 a 8 años)"],
                ["Consenso", "mediana = med(brecha<sub>1</sub>, …, brecha<sub>5</sub>); rango = máx − mín", "los cinco métodos del gráfico"],
            ],
        },
        "en": {
            "que": "The output gap is not observed: it has to be estimated, and each method gives a somewhat different answer. This chart shows "
                   "the latest quarter's gap under five standard methods from the literature and their median, to separate robust signals "
                   "from results that depend on the chosen method.",
            "leer": "Each row is a method and its dot marks the gap in percent, with the value printed beside it: blue if positive, orange if "
                    "negative; a grey stem joins zero to each dot. The green shaded area right of zero corresponds to output above "
                    "capacity. The black dotted vertical line is the median of the five, with its value on top. Methods are ordered from "
                    "smallest (bottom) to largest gap (top).",
            "importa": "Decisions based on a single gap estimate can be fragile. When all five methods agree on the sign, the cycle reading is "
                       "solid; when they straddle zero, the phase is uncertain. This weighs on how inflation and Banco de la República's "
                       "stance are interpreted.",
            "interpretar": [
                "Clustered dots on the same side of zero: a robust reading. Scattered dots: high uncertainty; the range (minimum to maximum) measures it.",
                "Real-time HP uses data only up to each quarter; two-sided HP, Christiano-Fitzgerald and Beveridge-Nelson use the full sample, so their recent values change as new data arrive.",
                "Hamilton compares GDP with what a regression on its history from 2 to 3 years earlier anticipated; Beveridge-Nelson defines the cycle from expected growth under an autoregressive model.",
                "In every method the trend is estimated excluding 2020Q2–2021Q2. A median between −0.5% and +0.5% reads as an economy close to potential.",
            ],
            "formulas": [
                ["Gap (generic)", "gap<sub>m,t</sub> = 100 × ln Y<sub>t</sub> − τ<sub>m,t</sub>", "Y = seasonally adjusted real GDP; τ<sub>m</sub> = trend (in 100 × log) under method m"],
                ["Hamilton (2018)", "c<sub>t</sub> = y<sub>t</sub> − (β<sub>0</sub> + Σ<sub>k=0..3</sub> β<sub>k+1</sub> y<sub>t−8−k</sub>)", "y = 100 × ln GDP; β estimated by OLS (ordinary least squares); 8-quarter horizon, 4 lags"],
                ["Christiano-Fitzgerald (2003)", "τ<sub>t</sub> = y<sub>t</sub> − CF<sub>6–32</sub>(y)<sub>t</sub>", "CF = band-pass filter isolating cycles of 6 to 32 quarters (1.5 to 8 years)"],
                ["Consensus", "median = med(gap<sub>1</sub>, …, gap<sub>5</sub>); range = max − min", "the five methods in the chart"],
            ],
        },
    },
    "g-ciclo-mensual": {
        "es": {
            "que": "Versión mensual de la brecha del producto, construida con el Indicador de Seguimiento a la Economía (ISE) del DANE, que "
                   "mide la actividad económica cada mes y se publica unos 45 días antes que el PIB trimestral. Muestra cuánto se aleja la "
                   "actividad de su tendencia y en qué fase del ciclo está cada mes.",
            "leer": "Cada barra es un mes: la brecha del ISE en porcentaje frente a su tendencia, coloreada por fase (verde expansión, ámbar "
                    "desaceleración, rojo contracción, azul recuperación). Las franjas grises sombrean las recesiones fechadas en la tabla de "
                    "expansiones y recesiones. Los meses de 2020 con brechas menores a −8% se recortan en ese valor para que no aplasten la "
                    "escala; el valor real aparece al pasar el cursor.",
            "importa": "Al llegar antes que el PIB, la brecha mensual da una lectura temprana del ciclo y permite detectar giros con menos "
                       "rezago. Es útil para seguir la economía entre publicaciones trimestrales y para contrastar la fase que muestra el reloj "
                       "del ciclo.",
            "interpretar": [
                "Barras positivas: actividad por encima de su tendencia; negativas: por debajo. El color indica además si la brecha sube o baja frente a 3 meses antes.",
                "Una racha de varios meses del mismo color es más informativa que un mes aislado: el ISE es volátil y se revisa.",
                "La tendencia es un HP en tiempo real con λ = 129.600, el equivalente mensual del λ = 1.600 trimestral (Ravn y Uhlig), y excluye marzo de 2020 a junio de 2021.",
                "Las recesiones sombreadas son caídas del nivel del ISE, un concepto distinto de la brecha negativa: puede haber brecha negativa sin recesión.",
            ],
            "formulas": [
                ["Brecha mensual", "b<sub>t</sub> = 100 × ln ISE<sub>t</sub> − τ<sub>t</sub>", "ISE desestacionalizado; τ = tendencia HP en tiempo real de 100 × ln ISE (λ = 129.600, solo datos hasta t)"],
                ["Dirección", "Δ<sub>t</sub> = b<sub>t</sub> − b<sub>t−3</sub>", "cambio en 3 meses; la fase combina el signo de b y de Δ"],
            ],
        },
        "en": {
            "que": "A monthly version of the output gap, built with DANE's Economic Tracking Indicator (ISE), which measures economic activity "
                   "every month and is released about 45 days before quarterly GDP. It shows how far activity is from trend and which cycle "
                   "phase each month is in.",
            "leer": "Each bar is a month: the ISE gap in percent versus its trend, coloured by phase (green expansion, amber slowdown, red "
                    "contraction, blue recovery). Grey bands shade the recessions dated in the expansions and recessions table. Months of 2020 "
                    "with gaps below −8% are capped at that value so they do not flatten the scale; the actual value appears on hover.",
            "importa": "Because it arrives before GDP, the monthly gap gives an early reading of the cycle and helps detect turning points with "
                       "less delay. It is useful for tracking the economy between quarterly releases and for cross-checking the phase shown by "
                       "the cycle clock.",
            "interpretar": [
                "Positive bars: activity above trend; negative: below. Colour also shows whether the gap is rising or falling versus 3 months earlier.",
                "A run of several months of the same colour is more informative than a single month: the ISE is volatile and gets revised.",
                "The trend is a real-time HP with λ = 129,600, the monthly equivalent of the quarterly λ = 1,600 (Ravn and Uhlig), and excludes March 2020 to June 2021.",
                "Shaded recessions are declines in the ISE level, a different concept from a negative gap: there can be a negative gap without a recession.",
            ],
            "formulas": [
                ["Monthly gap", "b<sub>t</sub> = 100 × ln ISE<sub>t</sub> − τ<sub>t</sub>", "seasonally adjusted ISE; τ = real-time HP trend of 100 × ln ISE (λ = 129,600, data up to t only)"],
                ["Direction", "Δ<sub>t</sub> = b<sub>t</sub> − b<sub>t−3</sub>", "3-month change; the phase combines the signs of b and Δ"],
            ],
        },
    },
    "g-motores": {
        "es": {
            "que": "Descompone la brecha mensual del ISE en las tres grandes ramas de la economía: actividades primarias (agro y minería), "
                   "secundarias (industria, construcción y servicios públicos) y terciarias (comercio, servicios y Gobierno). Muestra qué "
                   "parte de la economía está por encima o por debajo de su propia tendencia en el último mes publicado.",
            "leer": "Tres barras horizontales, una por rama, con la brecha en porcentaje y su valor escrito al final. Azul: la rama produce "
                    "por encima de su tendencia; naranja: por debajo. La línea vertical marca el cero y el eje es simétrico. Al pasar el "
                    "cursor también se ve el crecimiento anual de cada rama frente al mismo mes del año anterior.",
            "importa": "Las ramas responden a fuerzas distintas: las primarias, a precios internacionales, clima y producción petrolera; las "
                       "secundarias, a la inversión y la construcción; las terciarias, al consumo de los hogares y el gasto público. Saber cuál "
                       "empuja o frena el ciclo ayuda a entender su naturaleza y su sensibilidad a tasas de interés o a choques externos.",
            "interpretar": [
                "Las terciarias son la mayor parte de la economía, así que su brecha pesa más en la brecha total del ISE.",
                "Una rama puede crecer frente al año anterior y aun así estar por debajo de su tendencia (y al revés): brecha y crecimiento anual miden cosas distintas.",
                "Las primarias son las más volátiles mes a mes; conviene mirar varios meses antes de sacar conclusiones.",
                "Para el detalle por sector (12 ramas, trimestral) vea los aportes al crecimiento y la amplitud sectorial.",
            ],
            "formulas": [
                ["Brecha por rama", "b<sub>r,t</sub> = 100 × ln X<sub>r,t</sub> − τ<sub>r,t</sub>", "X = ISE desestacionalizado de la rama r; τ = tendencia HP en tiempo real (λ = 129.600), sin mar-2020 a jun-2021"],
                ["Crecimiento anual (en el cursor)", "g<sub>r,t</sub> = (X<sub>r,t</sub> ÷ X<sub>r,t−12</sub> − 1) × 100", "mismo mes del año anterior"],
            ],
        },
        "en": {
            "que": "Breaks the monthly ISE gap down into the economy's three broad branches: primary activities (farming and mining), secondary "
                   "(manufacturing, construction and utilities) and tertiary (trade, services and government). It shows which part of the "
                   "economy is above or below its own trend in the latest published month.",
            "leer": "Three horizontal bars, one per branch, with the gap in percent and its value printed at the end. Blue: the branch produces "
                    "above trend; orange: below. The vertical line marks zero and the axis is symmetric. Hovering also shows each branch's "
                    "annual growth versus the same month a year earlier.",
            "importa": "Branches respond to different forces: primary to international prices, weather and oil output; secondary to investment "
                       "and construction; tertiary to household consumption and public spending. Knowing which one drives or holds back the "
                       "cycle helps understand its nature and its sensitivity to interest rates or external shocks.",
            "interpretar": [
                "Tertiary activities are the bulk of the economy, so their gap weighs most in the overall ISE gap.",
                "A branch can grow year on year and still be below trend (and vice versa): the gap and annual growth measure different things.",
                "Primary activities are the most volatile month to month; look at several months before drawing conclusions.",
                "For sector detail (12 industries, quarterly) see the growth contributions and sector breadth.",
            ],
            "formulas": [
                ["Branch gap", "b<sub>r,t</sub> = 100 × ln X<sub>r,t</sub> − τ<sub>r,t</sub>", "X = seasonally adjusted ISE of branch r; τ = real-time HP trend (λ = 129,600), excluding Mar-2020 to Jun-2021"],
                ["Annual growth (on hover)", "g<sub>r,t</sub> = (X<sub>r,t</sub> ÷ X<sub>r,t−12</sub> − 1) × 100", "same month a year earlier"],
            ],
        },
    },
    "g-aportes": {
        "es": {
            "que": "Reparte el crecimiento anual de la economía entre las 12 grandes ramas de actividad: cuántos puntos porcentuales suma o "
                   "resta cada sector en el último trimestre publicado. Responde a la pregunta de quién está generando el crecimiento.",
            "leer": "Barras horizontales, una por sector, con su aporte en puntos porcentuales (pp) y el valor escrito al final; azul si suma, "
                    "naranja si resta. La línea vertical marca el cero y los sectores van ordenados del mayor aporte (arriba) al menor "
                    "(abajo). Al pasar el cursor se ve también el crecimiento anual del sector. La suma de las barras se aproxima al "
                    "crecimiento anual del valor agregado.",
            "importa": "Un mismo crecimiento total puede venir de sectores muy distintos: no es igual que lo impulse la agricultura que la "
                       "construcción o los servicios financieros. El aporte combina el ritmo del sector con su tamaño, por lo que muestra qué "
                       "actividades sostienen realmente la expansión y qué tan concentrada está.",
            "interpretar": [
                "Un sector pequeño con crecimiento alto puede aportar menos que uno grande con crecimiento moderado; el aporte refleja ambos.",
                "Si pocos sectores explican casi todo el crecimiento, la expansión depende de pocas fuentes; compárelo con la amplitud sectorial.",
                "Los datos son originales (sin desestacionalizar) y comparan con el mismo trimestre del año anterior, lo que neutraliza la estacionalidad, pero no los efectos de calendario (como la Semana Santa) ni las bases de comparación atípicas.",
                "Como los volúmenes encadenados no son aditivos, la suma de aportes difiere levemente del crecimiento total publicado por el DANE; el peso usado es el del valor agregado, no el del PIB con impuestos.",
            ],
            "formulas": [
                ["Aporte del sector", "a<sub>i,t</sub> = (X<sub>i,t</sub> − X<sub>i,t−4</sub>) ÷ VA<sub>t−4</sub> × 100", "X = valor agregado real del sector i; VA = valor agregado real total; t−4 = mismo trimestre del año anterior"],
                ["Forma equivalente", "a<sub>i,t</sub> = g<sub>i,t</sub> × w<sub>i,t−4</sub>", "g = crecimiento anual del sector (%); w = peso del sector en el valor agregado un año antes (tanto por uno)"],
                ["Suma", "Σ<sub>i</sub> a<sub>i,t</sub> ≈ crecimiento anual del valor agregado", "aproximación por la no aditividad de los encadenados"],
            ],
        },
        "en": {
            "que": "Splits the economy's annual growth among the 12 broad industries: how many percentage points each sector adds or subtracts "
                   "in the latest published quarter. It answers the question of who is generating growth.",
            "leer": "Horizontal bars, one per sector, with its contribution in percentage points (pp) and the value printed at the end; blue if it "
                    "adds, orange if it subtracts. The vertical line marks zero and sectors are ordered from largest contribution (top) to "
                    "smallest (bottom). Hovering also shows the sector's annual growth. The bars add up approximately to annual growth in "
                    "value added.",
            "importa": "The same total growth can come from very different sectors: growth led by farming is not the same as growth led by "
                       "construction or financial services. The contribution combines a sector's pace with its size, so it shows which "
                       "activities actually sustain the expansion and how concentrated it is.",
            "interpretar": [
                "A small sector growing fast can contribute less than a large one growing moderately; the contribution reflects both.",
                "If a few sectors explain almost all growth, the expansion relies on few sources; compare with sector breadth.",
                "Data are original (not seasonally adjusted) and compared with the same quarter a year earlier, which neutralises seasonality but not calendar effects (such as Easter) or unusual comparison bases.",
                "Because chain-linked volumes are not additive, the sum of contributions differs slightly from DANE's published total growth; the weight used is the value-added share, not the share of GDP including taxes.",
            ],
            "formulas": [
                ["Sector contribution", "a<sub>i,t</sub> = (X<sub>i,t</sub> − X<sub>i,t−4</sub>) ÷ VA<sub>t−4</sub> × 100", "X = real value added of sector i; VA = total real value added; t−4 = same quarter a year earlier"],
                ["Equivalent form", "a<sub>i,t</sub> = g<sub>i,t</sub> × w<sub>i,t−4</sub>", "g = sector annual growth (%); w = sector's share of value added a year earlier (fraction)"],
                ["Sum", "Σ<sub>i</sub> a<sub>i,t</sub> ≈ annual growth of value added", "approximate because chain-linked volumes are not additive"],
            ],
        },
    },
    "v-amplitud-sectores": {
        "es": {
            "que": "Cuenta cuántos de los 12 grandes sectores de la economía producen por encima de su propia tendencia en el último trimestre. "
                   "Es un índice de difusión: mide si la expansión es amplia, con la mayoría de los sectores participando, o estrecha, "
                   "concentrada en unos pocos.",
            "leer": "Una casilla por sector, ordenadas de mayor a menor brecha, con el nombre y la brecha en porcentaje. Verde: el sector está "
                    "por encima de su tendencia; rojo-naranja: por debajo. Junto al título se indica cuántos de los 12 están en verde. Más de "
                    "6 sectores en verde se considera una expansión generalizada.",
            "importa": "Una expansión amplia suele ser más sólida y generar presiones de precios más extendidas; una estrecha depende de pocos "
                       "motores y es más vulnerable a que alguno se frene. La amplitud complementa a la brecha agregada, que puede ser positiva "
                       "aunque la mayoría de sectores tenga holgura.",
            "interpretar": [
                "7 o más casillas verdes: expansión generalizada; 6 o menos: expansión concentrada.",
                "La brecha de cada sector se mide frente a su propia tendencia, calculada con la suma de 4 trimestres de su valor agregado real (datos originales) y un filtro HP en tiempo real.",
                "Las casillas son la misma información que el gráfico de barras «Brecha de cada sector hoy» de la página Capacidad.",
                "Un sector justo por encima o por debajo de cero puede cambiar de color con revisiones pequeñas del DANE.",
            ],
            "formulas": [
                ["Brecha sectorial", "b<sub>i,t</sub> = 100 × (ln N<sub>i,t</sub> − ln T<sub>i,t</sub>)", "N = suma de 4 trimestres del valor agregado real del sector i; T = tendencia HP en tiempo real (λ = 1.600), sin 2020T2–2021T2"],
                ["Amplitud", "A<sub>t</sub> = Σ<sub>i=1..12</sub> 1[b<sub>i,t</sub> > 0]", "1[·] vale 1 si el sector está sobre su tendencia y 0 si no"],
            ],
        },
        "en": {
            "que": "Counts how many of the economy's 12 broad sectors are producing above their own trend in the latest quarter. It is a "
                   "diffusion index: it measures whether the expansion is broad, with most sectors taking part, or narrow, concentrated in "
                   "a few.",
            "leer": "One tile per sector, ordered from largest to smallest gap, with the name and the gap in percent. Green: the sector is above "
                    "its trend; red-orange: below. Next to the title is the number of the 12 that are green. More than 6 green sectors is "
                    "considered a broad-based expansion.",
            "importa": "A broad expansion tends to be more solid and to generate more widespread price pressure; a narrow one relies on few "
                       "engines and is more exposed to any of them stalling. Breadth complements the aggregate gap, which can be positive even "
                       "when most sectors have slack.",
            "interpretar": [
                "7 or more green tiles: broad-based expansion; 6 or fewer: narrow expansion.",
                "Each sector's gap is measured against its own trend, computed from the 4-quarter sum of its real value added (original data) and a real-time HP filter.",
                "The tiles carry the same information as the «Each sector's gap today» bar chart on the Capacity page.",
                "A sector just above or below zero can change colour with small DANE revisions.",
            ],
            "formulas": [
                ["Sector gap", "b<sub>i,t</sub> = 100 × (ln N<sub>i,t</sub> − ln T<sub>i,t</sub>)", "N = 4-quarter sum of sector i's real value added; T = real-time HP trend (λ = 1,600), excluding 2020Q2–2021Q2"],
                ["Breadth", "A<sub>t</sub> = Σ<sub>i=1..12</sub> 1[b<sub>i,t</sub> > 0]", "1[·] equals 1 if the sector is above trend and 0 otherwise"],
            ],
        },
    },
    "g-ritmo": {
        "es": {
            "que": "Compara dos velocidades de la actividad económica medida con el ISE: el crecimiento anual, que mira 12 meses hacia atrás, "
                   "y el ritmo de los últimos tres meses, que capta el impulso más reciente. Cuando ambas difieren, la economía está "
                   "cambiando de marcha.",
            "leer": "Línea azul: variación del ISE desestacionalizado frente al mismo mes del año anterior, en porcentaje. Línea naranja, más "
                    "delgada: promedio de los últimos 3 meses frente a los 3 anteriores, llevado a tasa anual. Las franjas grises son "
                    "recesiones y la línea horizontal marca el cero. Ambas series se recortan entre −15% y 25% para que los extremos de 2020 "
                    "y su rebote no aplasten la escala.",
            "importa": "El crecimiento anual es estable pero lento para reflejar giros; el ritmo de 3 meses los muestra antes, a costa de más "
                       "ruido. Leerlos juntos ayuda a distinguir una economía que acelera de una que se modera, información relevante para la "
                       "lectura de la inflación, las tasas y las utilidades empresariales.",
            "interpretar": [
                "Naranja por encima de azul: el impulso reciente supera al promedio del año (aceleración); por debajo: moderación.",
                "Naranja por debajo de cero con azul aún positivo: la actividad ya cae en el margen aunque la comparación anual siga favorable.",
                "Anualizar multiplica el ruido mensual por cuatro: un solo dato atípico o una revisión puede mover mucho la línea naranja.",
                "La comparación anual hereda efectos de base: un año anterior muy débil o muy fuerte infla o reduce la variación sin reflejar el momento actual.",
            ],
            "formulas": [
                ["Crecimiento anual", "g<sub>t</sub> = (ISE<sub>t</sub> ÷ ISE<sub>t−12</sub> − 1) × 100", "ISE desestacionalizado del mes t"],
                ["Ritmo de 3 meses anualizado", "r<sub>t</sub> = [(M3<sub>t</sub> ÷ M3<sub>t−3</sub>)<sup>4</sup> − 1] × 100", "M3<sub>t</sub> = promedio del ISE desestacionalizado en t, t−1 y t−2"],
            ],
        },
        "en": {
            "que": "Compares two speeds of economic activity measured by the ISE: annual growth, which looks back 12 months, and the pace of "
                   "the last three months, which captures the most recent momentum. When the two differ, the economy is changing gear.",
            "leer": "Blue line: change in the seasonally adjusted ISE versus the same month a year earlier, in percent. Thinner orange line: "
                    "average of the last 3 months versus the previous 3, expressed at an annual rate. Grey bands are recessions and the "
                    "horizontal line marks zero. Both series are capped between −15% and 25% so the 2020 extremes and their rebound do not "
                    "flatten the scale.",
            "importa": "Annual growth is stable but slow to reflect turns; the 3-month pace shows them earlier at the cost of more noise. Reading "
                       "them together helps distinguish an accelerating economy from a moderating one, relevant for reading inflation, "
                       "interest rates and corporate earnings.",
            "interpretar": [
                "Orange above blue: recent momentum exceeds the year's average (acceleration); below: moderation.",
                "Orange below zero with blue still positive: activity is already falling at the margin even though the annual comparison remains favourable.",
                "Annualising multiplies monthly noise by four: a single outlier or revision can move the orange line a lot.",
                "The annual comparison inherits base effects: a very weak or very strong year earlier inflates or shrinks the change without reflecting the current moment.",
            ],
            "formulas": [
                ["Annual growth", "g<sub>t</sub> = (ISE<sub>t</sub> ÷ ISE<sub>t−12</sub> − 1) × 100", "seasonally adjusted ISE in month t"],
                ["Annualised 3-month pace", "r<sub>t</sub> = [(M3<sub>t</sub> ÷ M3<sub>t−3</sub>)<sup>4</sup> − 1] × 100", "M3<sub>t</sub> = average of the seasonally adjusted ISE in t, t−1 and t−2"],
            ],
        },
    },
    "v-fases-ciclo": {
        "es": {
            "que": "Fecha las expansiones y recesiones de la economía colombiana a partir del nivel del ISE: una recesión va de un pico a un "
                   "valle de la actividad y una expansión de un valle al siguiente pico. Es el «ciclo clásico», basado en caídas absolutas "
                   "de la producción, distinto del ciclo de brechas del reloj.",
            "leer": "Tabla con una fila por fase, de la más reciente arriba a la más antigua abajo. Columnas: tipo de fase (punto verde "
                    "expansión, rojo recesión), mes de inicio, mes de fin («en curso» si no ha terminado), duración en meses y variación "
                    "porcentual del ISE entre el inicio y el fin de la fase (verde si sube, rojo si baja). Las recesiones de esta tabla son "
                    "las franjas grises de los gráficos mensuales del sitio.",
            "importa": "La duración y la profundidad de recesiones y expansiones pasadas son la vara para medir el ciclo actual: cuánto lleva "
                       "la expansión en curso y cuánto ha crecido la actividad desde el último valle. Colombia no tiene un comité oficial de "
                       "fechado del ciclo, por lo que este fechado académico ofrece una referencia sistemática.",
            "interpretar": [
                "Picos y valles son máximos y mínimos locales del promedio móvil centrado de 3 meses del ISE desestacionalizado, dentro de ventanas de ±6 meses, y se fuerzan a alternarse (método en la línea de Bry y Boschan, 1971).",
                "Por construcción, un giro solo puede confirmarse cuando hay al menos 7 meses de datos posteriores: la última fase puede figurar «en curso» aunque la actividad ya haya girado.",
                "La variación de una fase en curso se mide hasta el último promedio centrado disponible y cambia con cada dato y con las revisiones del ISE.",
                "Es un fechado estadístico, no oficial; recesiones muy cortas o suaves pueden no detectarse o fecharse distinto con otras reglas.",
            ],
            "formulas": [
                ["Serie suavizada", "S<sub>t</sub> = (ISE<sub>t−1</sub> + ISE<sub>t</sub> + ISE<sub>t+1</sub>) ÷ 3", "ISE desestacionalizado; promedio móvil centrado de 3 meses"],
                ["Pico (valle)", "S<sub>t</sub> = máx (mín) {S<sub>t−6</sub>, …, S<sub>t+6</sub>}", "extremo local en una ventana de ±6 meses; picos y valles alternados"],
                ["Variación de la fase", "v = (S<sub>fin</sub> ÷ S<sub>inicio</sub> − 1) × 100", "S en el giro final (o el último disponible si la fase sigue en curso) frente al giro inicial"],
            ],
        },
        "en": {
            "que": "Dates the expansions and recessions of Colombia's economy from the level of the ISE: a recession runs from a peak to a trough "
                   "in activity and an expansion from a trough to the next peak. This is the «classical cycle», based on absolute declines in "
                   "output, different from the gap cycle shown in the clock.",
            "leer": "Table with one row per phase, most recent at the top. Columns: phase type (green dot expansion, red recession), start month, "
                    "end month («ongoing» if not finished), length in months and percentage change in the ISE between the start and end of "
                    "the phase (green if up, red if down). The recessions in this table are the grey bands on the site's monthly charts.",
            "importa": "The length and depth of past recessions and expansions are the yardstick for the current cycle: how long the ongoing "
                       "expansion has lasted and how much activity has grown since the last trough. Colombia has no official cycle-dating "
                       "committee, so this academic dating provides a systematic reference.",
            "interpretar": [
                "Peaks and troughs are local maxima and minima of the centred 3-month moving average of the seasonally adjusted ISE within ±6-month windows, forced to alternate (a method in the spirit of Bry and Boschan, 1971).",
                "By construction, a turn can only be confirmed once at least 7 months of later data exist: the last phase may show as «ongoing» even if activity has already turned.",
                "The change for an ongoing phase is measured up to the latest available centred average and moves with each release and with ISE revisions.",
                "It is a statistical dating, not an official one; very short or mild recessions may go undetected or be dated differently under other rules.",
            ],
            "formulas": [
                ["Smoothed series", "S<sub>t</sub> = (ISE<sub>t−1</sub> + ISE<sub>t</sub> + ISE<sub>t+1</sub>) ÷ 3", "seasonally adjusted ISE; centred 3-month moving average"],
                ["Peak (trough)", "S<sub>t</sub> = max (min) {S<sub>t−6</sub>, …, S<sub>t+6</sub>}", "local extreme within a ±6-month window; peaks and troughs alternate"],
                ["Phase change", "v = (S<sub>end</sub> ÷ S<sub>start</sub> − 1) × 100", "S at the closing turn (or the latest available if the phase is ongoing) versus the opening turn"],
            ],
        },
    },
    "g-empleo-ciclo": {
        "es": {
            "que": "Muestra cómo se transmite el ciclo al mercado laboral: el cambio en 12 meses de la tasa de desempleo y de la tasa de "
                   "ocupación. Permite ver si la actividad económica se está traduciendo en más empleo o si el mercado laboral se debilita.",
            "leer": "Dos líneas mensuales en puntos porcentuales (pp): verde, cambio de la tasa de ocupación; naranja, cambio de la tasa de "
                    "desempleo. Cada punto compara el promedio de los últimos 3 meses de la tasa desestacionalizada con el mismo promedio un "
                    "año antes. La línea horizontal marca el cero, las franjas grises son recesiones y los valores se recortan en ±6 pp para "
                    "que el choque de 2020 no aplaste la escala.",
            "importa": "El empleo es el canal por el que el ciclo llega a los hogares: sostiene el consumo y la confianza. Un mercado laboral "
                       "que mejora refuerza la demanda interna; uno que se deteriora la debilita. Además, la presión salarial que genera un "
                       "mercado laboral apretado es un insumo clave para la inflación y la política monetaria.",
            "interpretar": [
                "Verde por encima de cero y naranja por debajo: mercado laboral que mejora (más ocupados, menos desempleo). Lo contrario indica deterioro.",
                "El desempleo puede bajar sin que suba la ocupación si menos personas buscan trabajo; por eso conviene mirar las dos líneas juntas.",
                "Promediar 3 meses reduce el ruido de la encuesta (GEIH), pero los cambios se reflejan con algo de rezago.",
                "En Colombia el empleo responde poco al ciclo (vea la ley de Okun), en parte porque la informalidad absorbe los choques.",
            ],
            "formulas": [
                ["Promedio de 3 meses", "x̄<sub>t</sub> = (x<sub>t</sub> + x<sub>t−1</sub> + x<sub>t−2</sub>) ÷ 3", "x = tasa de desempleo o de ocupación desestacionalizada"],
                ["Cambio en 12 meses", "Δ<sub>12</sub>x̄<sub>t</sub> = x̄<sub>t</sub> − x̄<sub>t−12</sub>", "en puntos porcentuales"],
                ["Tasas", "TD = D ÷ FT × 100; TO = O ÷ PET × 100", "D = desocupados; O = ocupados; FT = fuerza de trabajo; PET = población en edad de trabajar"],
            ],
        },
        "en": {
            "que": "Shows how the cycle reaches the labour market: the 12-month change in the unemployment rate and in the employment rate. It "
                   "reveals whether economic activity is translating into more jobs or whether the labour market is weakening.",
            "leer": "Two monthly lines in percentage points (pp): green, change in the employment rate; orange, change in the unemployment rate. "
                    "Each point compares the latest 3-month average of the seasonally adjusted rate with the same average a year earlier. The "
                    "horizontal line marks zero, grey bands are recessions and values are capped at ±6 pp so the 2020 shock does not flatten "
                    "the scale.",
            "importa": "Jobs are the channel through which the cycle reaches households: they sustain consumption and confidence. An improving "
                       "labour market reinforces domestic demand; a deteriorating one weakens it. In addition, the wage pressure created by a "
                       "tight labour market is a key input for inflation and monetary policy.",
            "interpretar": [
                "Green above zero and orange below: an improving labour market (more employed, less unemployment). The opposite signals deterioration.",
                "Unemployment can fall without employment rising if fewer people look for work; that is why both lines should be read together.",
                "Averaging 3 months reduces survey (GEIH) noise, but changes show up with some delay.",
                "In Colombia jobs respond little to the cycle (see Okun's law), partly because informality absorbs shocks.",
            ],
            "formulas": [
                ["3-month average", "x̄<sub>t</sub> = (x<sub>t</sub> + x<sub>t−1</sub> + x<sub>t−2</sub>) ÷ 3", "x = seasonally adjusted unemployment or employment rate"],
                ["12-month change", "Δ<sub>12</sub>x̄<sub>t</sub> = x̄<sub>t</sub> − x̄<sub>t−12</sub>", "in percentage points"],
                ["Rates", "UR = U ÷ LF × 100; ER = E ÷ WAP × 100", "U = unemployed; E = employed; LF = labour force; WAP = working-age population"],
            ],
        },
    },
    "g-okun": {
        "es": {
            "que": "Pone a prueba la ley de Okun, la regularidad según la cual cuando la economía produce por encima de su capacidad el "
                   "desempleo cae por debajo de su nivel de tendencia. Compara la brecha del producto con la brecha de desempleo para ver "
                   "cuánto se mueven juntas en Colombia.",
            "leer": "Dos líneas trimestrales: azul, brecha del producto en porcentaje (filtro HP de dos colas); verde, cuánto está el desempleo "
                    "por debajo de su tendencia, en puntos porcentuales. La verde está invertida (desempleo bajo la tendencia = valor positivo) "
                    "para que ambas suban juntas en una economía recalentada. La línea horizontal marca el cero y ambas se recortan en ±8 para "
                    "que 2020 no aplaste la escala.",
            "importa": "La fuerza de la relación indica cuánto empleo genera un punto adicional de actividad. Si es débil, el crecimiento se "
                       "traduce poco en empleo formal y la holgura laboral puede persistir aunque la economía crezca, lo que afecta la lectura "
                       "de presiones salariales e inflación y el diagnóstico del Banco de la República.",
            "interpretar": [
                "Líneas que suben y bajan juntas confirman la relación; si se separan, el empleo no está acompañando a la producción.",
                "La pendiente β se estima por mínimos cuadrados ordinarios (MCO) con todos los trimestres disponibles excepto 2020–2021; una β cercana a cero indica que el desempleo responde poco a la producción. Su valor y la correlación se muestran en el texto de la sección.",
                "En Colombia la relación es débil, en parte porque la informalidad absorbe los choques: en las recesiones muchas personas pasan a empleos informales en lugar de al desempleo.",
                "Ambas tendencias usan filtros HP de dos colas, que se reestiman con cada dato nuevo: los valores recientes de las dos brechas pueden cambiar.",
            ],
            "formulas": [
                ["Brecha de desempleo", "b<sup>u</sup><sub>t</sub> = u<sub>t</sub> − u*<sub>t</sub>", "u = promedio trimestral del desempleo desestacionalizado; u* = tendencia HP de dos colas (λ = 1.600), sin 2020T2–2021T2"],
                ["Línea verde", "−b<sup>u</sup><sub>t</sub>", "positiva cuando el desempleo está por debajo de su tendencia"],
                ["Ley de Okun en brechas", "b<sup>u</sup><sub>t</sub> = α + β × brecha<sub>t</sub> + ε<sub>t</sub>", "brecha = brecha del producto (HP dos colas); β < 0 esperado; estimado por MCO sin 2020–2021"],
            ],
        },
        "en": {
            "que": "Tests Okun's law, the regularity whereby unemployment falls below its trend level when the economy produces above capacity. "
                   "It compares the output gap with the unemployment gap to see how closely they move together in Colombia.",
            "leer": "Two quarterly lines: blue, output gap in percent (two-sided HP filter); green, how far unemployment is below its trend, in "
                    "percentage points. The green line is inverted (unemployment below trend = positive value) so both rise together in an "
                    "overheating economy. The horizontal line marks zero and both are capped at ±8 so 2020 does not flatten the scale.",
            "importa": "The strength of the link indicates how many jobs an extra point of activity generates. If it is weak, growth translates "
                       "little into formal employment and labour slack can persist even as the economy grows, which affects the reading of wage "
                       "pressure and inflation and Banco de la República's assessment.",
            "interpretar": [
                "Lines rising and falling together confirm the relationship; if they diverge, jobs are not keeping up with output.",
                "The slope β is estimated by ordinary least squares (OLS) on all available quarters except 2020–2021; a β close to zero means unemployment responds little to output. Its value and the correlation appear in the section text.",
                "In Colombia the link is weak, partly because informality absorbs shocks: in downturns many people move into informal jobs rather than into unemployment.",
                "Both trends use two-sided HP filters, re-estimated with each new data point: recent values of both gaps can change.",
            ],
            "formulas": [
                ["Unemployment gap", "b<sup>u</sup><sub>t</sub> = u<sub>t</sub> − u*<sub>t</sub>", "u = quarterly average of seasonally adjusted unemployment; u* = two-sided HP trend (λ = 1,600), excluding 2020Q2–2021Q2"],
                ["Green line", "−b<sup>u</sup><sub>t</sub>", "positive when unemployment is below its trend"],
                ["Okun's law in gaps", "b<sup>u</sup><sub>t</sub> = α + β × gap<sub>t</sub> + ε<sub>t</sub>", "gap = output gap (two-sided HP); β < 0 expected; OLS estimate excluding 2020–2021"],
            ],
        },
    },
}
