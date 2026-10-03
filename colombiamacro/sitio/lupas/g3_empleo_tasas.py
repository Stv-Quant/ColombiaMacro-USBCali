"""Lupas (explicaciones de cada gráfico) del grupo g3: mercado laboral (página Empleo y desempleo por ciudad)
y tasas de interés (página Tasas: política monetaria, transmisión, crédito, IBR y liquidez). Español e inglés."""

LUPAS = {
    # =========================================================================================== EMPLEO
    "g-desempleo": {
        "es": {
            "que": "Muestra la tasa de desempleo nacional: la proporción de la fuerza de trabajo (personas que trabajan o buscan trabajo) que busca empleo y no lo consigue. Es la serie desestacionalizada que publica el DANE a partir de la Gran Encuesta Integrada de Hogares (GEIH), la encuesta mensual con la que se mide el mercado laboral. Resume en un número la holgura del mercado de trabajo y su evolución a lo largo del ciclo económico.",
            "leer": "Panel superior, en porcentaje: la línea gris delgada es el dato mensual desestacionalizado y la línea azul gruesa es su promedio móvil de 3 meses, que filtra el ruido de muestreo de la encuesta. Panel inferior: barras con el cambio del promedio de 3 meses frente al mismo mes un año antes, en puntos porcentuales (pp); azules cuando el desempleo sube y naranjas cuando baja. La vista inicial abarca los últimos diez años; el recuadro flotante muestra ambos paneles a la vez.",
            "importa": "El desempleo es el termómetro más directo del bienestar de los hogares y de la presión sobre salarios e ingresos. Un mercado laboral holgado limita el consumo y las presiones de costos; uno estrecho los impulsa. Por eso el Banco de la República lo sigue para calibrar la tasa de interés, y los inversionistas lo usan para leer la demanda interna, la calidad de la cartera de los bancos y el entorno social y fiscal.",
            "interpretar": [
                "Barras naranjas persistentes indican que el desempleo está por debajo del de un año antes; barras azules seguidas, que el mercado laboral se debilita.",
                "Conviene mirar la línea azul y no el dato mensual aislado: movimientos de 0,3–0,5 pp en un solo mes pueden ser ruido de la encuesta.",
                "El salto de 2020 (pandemia) es el episodio extremo de la serie y distorsiona los cambios anuales del año siguiente (efecto base).",
                "La tasa puede bajar porque se crean empleos o porque menos personas buscan trabajo; contrástela con la participación laboral (gráfico de mujeres y hombres) y con los empleos por rama.",
                "El DANE revisa la desestacionalización cuando llegan datos nuevos, por lo que los últimos meses pueden cambiar levemente."
            ],
            "formulas": [
                ["Tasa de desempleo", "TD<sub>t</sub> = D<sub>t</sub> ÷ FT<sub>t</sub> × 100", "D = desocupados; FT = fuerza de trabajo (ocupados + desocupados); serie desestacionalizada del DANE"],
                ["Promedio de 3 meses", "TD3<sub>t</sub> = (TD<sub>t</sub> + TD<sub>t−1</sub> + TD<sub>t−2</sub>) ÷ 3", "t = mes"],
                ["Cambio anual (panel inferior)", "ΔTD3<sub>t</sub> = TD3<sub>t</sub> − TD3<sub>t−12</sub>", "en puntos porcentuales"]
            ]
        },
        "en": {
            "que": "This chart shows the national unemployment rate: the share of the labour force (people working or looking for work) who are seeking a job and cannot find one. It is the seasonally adjusted series published by DANE from the Integrated Household Survey (GEIH), the monthly survey used to measure the labour market. It sums up in one number how much slack there is in the labour market and how it moves through the business cycle.",
            "leer": "Top panel, in percent: the thin grey line is the monthly seasonally adjusted figure and the thick blue line is its 3-month moving average, which filters out survey sampling noise. Bottom panel: bars with the change in the 3-month average versus the same month a year earlier, in percentage points (pp); blue when unemployment rises and orange when it falls. The initial view covers the last ten years; the hover box shows both panels at once.",
            "importa": "Unemployment is the most direct gauge of household welfare and of pressure on wages and incomes. A slack labour market restrains consumption and cost pressures; a tight one fuels them. That is why the Banco de la República tracks it when setting interest rates, and investors use it to read domestic demand, bank asset quality and the social and fiscal backdrop.",
            "interpretar": [
                "Persistent orange bars mean unemployment is below its level a year earlier; a run of blue bars means the labour market is weakening.",
                "Focus on the blue line rather than a single monthly print: moves of 0.3–0.5 pp in one month can be survey noise.",
                "The 2020 spike (pandemic) is the extreme episode in the series and distorts annual changes the following year (base effect).",
                "The rate can fall because jobs are created or because fewer people look for work; cross-check with participation (women and men chart) and with jobs by sector.",
                "DANE revises its seasonal adjustment as new data arrive, so the latest months may change slightly."
            ],
            "formulas": [
                ["Unemployment rate", "UR<sub>t</sub> = U<sub>t</sub> ÷ LF<sub>t</sub> × 100", "U = unemployed; LF = labour force (employed + unemployed); DANE seasonally adjusted series"],
                ["3-month average", "UR3<sub>t</sub> = (UR<sub>t</sub> + UR<sub>t−1</sub> + UR<sub>t−2</sub>) ÷ 3", "t = month"],
                ["Annual change (bottom panel)", "ΔUR3<sub>t</sub> = UR3<sub>t</sub> − UR3<sub>t−12</sub>", "in percentage points"]
            ]
        },
    },
    "g-informal": {
        "es": {
            "que": "Muestra qué porcentaje de las personas ocupadas trabaja en la informalidad según la definición vigente del DANE, alineada con la Organización Internacional del Trabajo (OIT): ocupados sin afiliación a la seguridad social o que trabajan en unidades económicas no registradas. Compara el total nacional con el agregado de las 13 ciudades principales y sus áreas metropolitanas, donde la informalidad es menor que en el resto del país.",
            "leer": "Panel superior, en porcentaje de los ocupados: línea azul = total nacional; línea verde = 13 ciudades y áreas metropolitanas. Cada punto es un trimestre móvil (tres meses que terminan en el mes indicado). Panel inferior: cambio de la tasa nacional frente al mismo trimestre móvil de un año antes, en pp; barras naranjas cuando la informalidad baja y azules cuando sube. La serie comienza en 2021 con la nueva definición.",
            "importa": "La informalidad es uno de los rasgos estructurales del mercado laboral colombiano: limita la base tributaria y de cotizantes a pensiones y salud, reduce la productividad y deja a los hogares con ingresos más volátiles. Para un inversionista indica la calidad del empleo detrás de las cifras de desempleo, la profundidad del mercado de consumo formal y el margen fiscal del Estado.",
            "interpretar": [
                "Una caída sostenida (barras naranjas) significa que una mayor parte de los ocupados cotiza a la seguridad social o trabaja en empresas registradas.",
                "La brecha entre el total nacional y las 13 ciudades refleja el peso del campo y de las ciudades intermedias, donde predominan el trabajo por cuenta propia y el agro.",
                "Cambios menores a 1 pp en un año pueden estar dentro del error de muestreo de la encuesta.",
                "No es comparable con las cifras anteriores a 2021 (otra definición y otro marco muestral); compárela con la composición del empleo por posición ocupacional y con la informalidad por sector."
            ],
            "formulas": [
                ["Proporción de informalidad", "INF<sub>t</sub> = I<sub>t</sub> ÷ O<sub>t</sub> × 100", "I = ocupados informales; O = ocupados; trimestre móvil que termina en el mes t"],
                ["Cambio anual (panel inferior)", "ΔINF<sub>t</sub> = INF<sub>t</sub> − INF<sub>t−12</sub>", "en puntos porcentuales"]
            ]
        },
        "en": {
            "que": "This chart shows what share of employed people work informally under DANE's current definition, aligned with the International Labour Organization (ILO): workers without social security coverage or working in unregistered economic units. It compares the national total with the aggregate for the 13 main cities and their metropolitan areas, where informality is lower than in the rest of the country.",
            "leer": "Top panel, as a percentage of the employed: blue line = national total; green line = 13 cities and metropolitan areas. Each point is a rolling quarter (three months ending in the month shown). Bottom panel: change in the national rate versus the same rolling quarter a year earlier, in pp; orange bars when informality falls and blue when it rises. The series starts in 2021 with the new definition.",
            "importa": "Informality is a structural feature of Colombia's labour market: it narrows the tax base and the pool of pension and health contributors, lowers productivity and leaves households with more volatile incomes. For an investor it signals the quality of the jobs behind the unemployment figures, the depth of the formal consumer market and the state's fiscal room.",
            "interpretar": [
                "A sustained decline (orange bars) means a larger share of workers contribute to social security or work in registered firms.",
                "The gap between the national total and the 13 cities reflects the weight of rural areas and smaller cities, where self-employment and farming dominate.",
                "Changes below 1 pp over a year may be within the survey's sampling error.",
                "Not comparable with figures before 2021 (different definition and sampling frame); compare with employment by occupational status and informality by sector."
            ],
            "formulas": [
                ["Informality share", "INF<sub>t</sub> = I<sub>t</sub> ÷ E<sub>t</sub> × 100", "I = informal workers; E = employed; rolling quarter ending in month t"],
                ["Annual change (bottom panel)", "ΔINF<sub>t</sub> = INF<sub>t</sub> − INF<sub>t−12</sub>", "in percentage points"]
            ]
        },
    },
    "g-inf-ramas": {
        "es": {
            "que": "Compara la informalidad entre las 13 ramas de actividad en que la GEIH agrupa el empleo, para el último trimestre móvil disponible. Muestra que la informalidad no es pareja: es casi generalizada en el agro, el comercio, el alojamiento y comida o el transporte, y baja en finanzas, en el sector público, la educación y la salud o en los servicios públicos. Permite ver dónde se concentra el problema y si mejora o empeora en cada sector.",
            "leer": "Eje horizontal de 0% a 100%: proporción de los ocupados de cada rama que son informales, total nacional. Las barras naranjas son el dato del último trimestre móvil, ordenadas de menor a mayor; la raya vertical negra sobre cada barra es el dato del mismo trimestre móvil un año antes. El recuadro flotante muestra la tasa, su cambio en pp frente a un año antes y cuántos informales y ocupados hay en la rama, en millones de personas.",
            "importa": "La informalidad sectorial explica por qué el crecimiento de ciertas ramas genera más o menos empleo formal, cotizaciones y recaudo. Para un inversionista ayuda a dimensionar los costos laborales, la exposición regulatoria y el tamaño del mercado formal en cada actividad, y a entender qué sectores pesan en el promedio nacional.",
            "interpretar": [
                "Una barra a la izquierda de su raya indica que la informalidad del sector bajó frente a un año antes; a la derecha, que subió.",
                "Una rama con tasa alta pero pocos ocupados pesa poco en el total; mire el número de personas en el recuadro flotante.",
                "El promedio nacional también cambia si el empleo se desplaza entre sectores, aunque la tasa de cada uno no varíe (efecto composición).",
                "Las ramas pequeñas tienen más error de muestreo; diferencias de 1–2 pp en un año pueden no ser significativas."
            ],
            "formulas": [
                ["Informalidad por rama", "INF<sub>r</sub> = I<sub>r</sub> ÷ O<sub>r</sub> × 100", "I = informales; O = ocupados de la rama r; trimestre móvil, total nacional"],
                ["Cambio frente a un año antes", "ΔINF<sub>r</sub> = INF<sub>r,t</sub> − INF<sub>r,t−12</sub>", "en pp (recuadro flotante)"]
            ]
        },
        "en": {
            "que": "This chart compares informality across the 13 sectors into which the GEIH groups employment, for the latest rolling quarter. It shows that informality is uneven: it is almost universal in farming, trade, accommodation and food, or transport, and low in finance, government, education and health, or utilities. It reveals where the problem is concentrated and whether it is improving or worsening in each sector.",
            "leer": "Horizontal axis from 0% to 100%: share of each sector's employed people who are informal, national total. Orange bars are the latest rolling quarter, sorted from lowest to highest; the black vertical tick on each bar is the same rolling quarter a year earlier. The hover box shows the rate, its change in pp versus a year earlier and how many informal and employed people the sector has, in millions.",
            "importa": "Sectoral informality explains why growth in some sectors generates more or less formal employment, social security contributions and tax revenue. For an investor it helps size labour costs, regulatory exposure and the formal market in each activity, and shows which sectors drive the national average.",
            "interpretar": [
                "A bar ending left of its tick means the sector's informality fell versus a year earlier; to the right, it rose.",
                "A sector with a high rate but few workers weighs little in the total; check the number of people in the hover box.",
                "The national average also moves when employment shifts between sectors, even if each sector's rate is unchanged (composition effect).",
                "Small sectors carry more sampling error; differences of 1–2 pp over a year may not be significant."
            ],
            "formulas": [
                ["Informality by sector", "INF<sub>s</sub> = I<sub>s</sub> ÷ E<sub>s</sub> × 100", "I = informal workers; E = employed in sector s; rolling quarter, national total"],
                ["Change versus a year earlier", "ΔINF<sub>s</sub> = INF<sub>s,t</sub> − INF<sub>s,t−12</sub>", "in pp (hover box)"]
            ]
        },
    },
    "g-emp-ramas": {
        "es": {
            "que": "Muestra cuántos empleos ganó o perdió cada rama de actividad en el último año, en miles de personas. Responde a la pregunta de dónde se está creando el empleo: qué sectores explican el aumento (o la caída) del número total de ocupados. Usa las 13 agrupaciones de ramas de la GEIH (clasificación CIIU Rev. 4 adaptada para Colombia).",
            "leer": "Cada barra horizontal es una rama, ordenada del mayor aumento (arriba) a la mayor caída (abajo). El eje está en miles de personas y la línea vertical marca el cero. Barras azules: la rama tiene más ocupados que un año antes; naranjas: tiene menos. La cifra junto a cada barra es el cambio redondeado. Se compara el promedio de los últimos 3 meses con el de los mismos 3 meses del año anterior, en datos sin desestacionalizar.",
            "importa": "El empleo sectorial conecta el crecimiento del PIB con los hogares: un sector puede crecer en producción sin contratar, o contratar mucho con poca producción. Para un inversionista indica qué actividades sostienen el ingreso laboral y el consumo, y cuáles están ajustando su planta de personal, una señal temprana sobre su demanda y sus márgenes.",
            "interpretar": [
                "La suma de las barras aproxima el cambio anual del total de ocupados; si unas pocas ramas explican casi todo el aumento, el empleo depende de pocos motores.",
                "Comparar los mismos meses del año anterior evita la estacionalidad (cosechas, temporada de fin de año) sin modelos estadísticos.",
                "Cambios de pocas decenas de miles en ramas pequeñas pueden estar dentro del error de muestreo de la encuesta.",
                "La GEIH agrupa la minería con los servicios públicos (electricidad, gas y agua); compárelo con el crecimiento del PIB por sectores y con la informalidad por rama."
            ],
            "formulas": [
                ["Promedio de 3 meses", "Ō<sub>r,t</sub> = (O<sub>r,t</sub> + O<sub>r,t−1</sub> + O<sub>r,t−2</sub>) ÷ 3", "O = ocupados de la rama r en el mes t (miles)"],
                ["Empleos creados o perdidos", "ΔO<sub>r</sub> = Ō<sub>r,t</sub> − Ō<sub>r,t−12</sub>", "en miles de personas"]
            ]
        },
        "en": {
            "que": "This chart shows how many jobs each sector gained or lost over the last year, in thousands of people. It answers where employment is being created: which sectors explain the increase (or drop) in the total number of employed. It uses the 13 sector groups of the GEIH (ISIC Rev. 4 adapted for Colombia).",
            "leer": "Each horizontal bar is a sector, sorted from the largest gain (top) to the largest loss (bottom). The axis is in thousands of people and the vertical line marks zero. Blue bars: the sector employs more people than a year earlier; orange: fewer. The figure next to each bar is the rounded change. The average of the last 3 months is compared with the same 3 months a year earlier, using non-seasonally adjusted data.",
            "importa": "Sectoral employment links GDP growth to households: a sector can grow output without hiring, or hire heavily with little output. For an investor it shows which activities are sustaining labour income and consumption, and which are trimming headcount, an early signal about their demand and margins.",
            "interpretar": [
                "The bars add up to roughly the annual change in total employment; if a few sectors explain almost all the gain, job growth relies on few engines.",
                "Comparing the same months a year earlier removes seasonality (harvests, year-end season) without statistical models.",
                "Changes of a few tens of thousands in small sectors may be within the survey's sampling error.",
                "The GEIH groups mining with utilities (electricity, gas and water); compare with GDP growth by sector and with informality by sector."
            ],
            "formulas": [
                ["3-month average", "Ē<sub>s,t</sub> = (E<sub>s,t</sub> + E<sub>s,t−1</sub> + E<sub>s,t−2</sub>) ÷ 3", "E = employed in sector s in month t (thousands)"],
                ["Jobs created or lost", "ΔE<sub>s</sub> = Ē<sub>s,t</sub> − Ē<sub>s,t−12</sub>", "in thousands of people"]
            ]
        },
    },
    "g-emp-ramas-2019": {
        "es": {
            "que": "Compara el empleo actual de cada rama con el de 2019, el último año completo antes de la pandemia. Muestra qué sectores ya superan su nivel de empleo prepandemia y cuáles siguen por debajo, es decir, cómo cambió la estructura del empleo después del choque de 2020. Es una mirada de mediano plazo que complementa el cambio de un año.",
            "leer": "Cada barra horizontal es una rama de la GEIH, ordenada de mayor a menor variación. El eje muestra la variación porcentual del promedio de ocupados de los últimos 12 meses frente al promedio de los 12 meses de 2019. Barras verdes: la rama emplea más personas que en 2019; naranjas: menos. La línea vertical marca el 0% (mismo nivel que en 2019).",
            "importa": "Revela cambios estructurales que el dato de un año no muestra: sectores que crecieron de forma sostenida y otros que perdieron peso de manera duradera. Para un inversionista ayuda a separar recuperaciones cíclicas de transformaciones de largo plazo en la demanda de trabajo, la productividad y los hábitos de consumo.",
            "interpretar": [
                "Una barra verde amplia indica un sector cuyo empleo creció por encima del nivel prepandemia; una naranja, que no ha recuperado los puestos de 2019 o que se encoge por razones estructurales (automatización, cambio de demanda).",
                "Promediar 12 meses elimina la estacionalidad y reduce el ruido de la encuesta.",
                "Una caída del empleo no implica una caída de la producción: puede reflejar ganancias de productividad; compárelo con el PIB por sectores.",
                "La comparación depende del año base: si 2019 fue un año atípico para una rama, la variación lo arrastra."
            ],
            "formulas": [
                ["Variación frente a 2019", "V<sub>r</sub> = (Ō<sup>12</sup><sub>r,t</sub> ÷ Ō<sub>r,2019</sub> − 1) × 100", "Ō<sup>12</sup> = promedio de ocupados de los últimos 12 meses; Ō<sub>2019</sub> = promedio de los 12 meses de 2019; r = rama"]
            ]
        },
        "en": {
            "que": "This chart compares current employment in each sector with 2019, the last full year before the pandemic. It shows which sectors already exceed their pre-pandemic employment and which remain below it, that is, how the structure of employment changed after the 2020 shock. It is a medium-term view that complements the one-year change.",
            "leer": "Each horizontal bar is a GEIH sector, sorted from the largest to the smallest change. The axis shows the percentage change in average employment over the last 12 months versus the average for the 12 months of 2019. Green bars: the sector employs more people than in 2019; orange: fewer. The vertical line marks 0% (same level as 2019).",
            "importa": "It reveals structural shifts that the one-year change hides: sectors that have grown steadily and others that have lost weight for good. For an investor it helps separate cyclical recoveries from long-term changes in labour demand, productivity and consumer habits.",
            "interpretar": [
                "A long green bar marks a sector whose employment has grown beyond its pre-pandemic level; an orange bar, one that has not regained its 2019 jobs or is shrinking for structural reasons (automation, shifting demand).",
                "Averaging 12 months removes seasonality and reduces survey noise.",
                "Lower employment does not imply lower output: it may reflect productivity gains; compare with GDP by sector.",
                "The comparison depends on the base year: if 2019 was atypical for a sector, the change carries that over."
            ],
            "formulas": [
                ["Change versus 2019", "V<sub>s</sub> = (Ē<sup>12</sup><sub>s,t</sub> ÷ Ē<sub>s,2019</sub> − 1) × 100", "Ē<sup>12</sup> = average employment over the last 12 months; Ē<sub>2019</sub> = average of the 12 months of 2019; s = sector"]
            ]
        },
    },
    "g-emp-posicion": {
        "es": {
            "que": "Muestra cómo se reparte el empleo según la posición ocupacional, es decir, la relación de cada persona con su trabajo según la clasificación internacional CISE-93 de la OIT: asalariados del sector privado, trabajadores por cuenta propia, empleados del Gobierno, empleo doméstico, empleadores, jornaleros y familiares sin pago. Revela la calidad del empleo: cuánto descansa en contratos asalariados y cuánto en el trabajo independiente.",
            "leer": "Áreas apiladas que suman el 100% de los ocupados (eje de 0% a 100%), desde 2011. De abajo hacia arriba: azul = asalariado privado; naranja = cuenta propia; verde = asalariado del Gobierno; morado = empleo doméstico; ámbar = empleador; azul verdoso = jornalero o peón; café = familiar sin pago. Cada participación usa promedios móviles de 12 meses de los ocupados, lo que elimina la estacionalidad. Se omite la categoría «otro» (menos de 0,1%).",
            "importa": "En Colombia cerca de la mitad de los ocupados trabaja por cuenta propia o en posiciones sin contrato, lo que se asocia con informalidad, ingresos inestables y baja productividad. Un aumento del peso de los asalariados suele acompañar la formalización y la expansión de las empresas. Para un inversionista es una señal de la profundidad del mercado laboral formal, la estabilidad del ingreso de los hogares y la base de cotizantes.",
            "interpretar": [
                "Si la franja azul se ensancha a costa de la naranja, el empleo se está volviendo más asalariado; lo contrario indica más trabajo independiente.",
                "Los asalariados privados son en su mayoría formales, pero no todos; para la informalidad exacta use el gráfico de informalidad.",
                "En las recesiones el trabajo por cuenta propia tiende a absorber a quienes pierden un empleo asalariado; obsérvelo alrededor de 2020.",
                "Por ser un promedio de 12 meses, los cambios aparecen de forma gradual y con rezago; el gráfico de cambio en un año por posición muestra el movimiento reciente."
            ],
            "formulas": [
                ["Promedio de 12 meses", "Ō<sub>p,t</sub> = (1 ÷ 12) × Σ<sub>k=0..11</sub> O<sub>p,t−k</sub>", "O = ocupados en la posición p en el mes t"],
                ["Participación", "S<sub>p,t</sub> = Ō<sub>p,t</sub> ÷ Σ<sub>j</sub> Ō<sub>j,t</sub> × 100", "j recorre las siete posiciones graficadas"]
            ]
        },
        "en": {
            "que": "This chart shows how employment is split by status in employment, that is, each person's relationship to their job under the ILO's ICSE-93 classification: private wage employees, own-account workers, government employees, domestic workers, employers, day labourers and unpaid family workers. It reveals job quality: how much rests on wage contracts and how much on self-employment.",
            "leer": "Stacked areas adding up to 100% of the employed (axis from 0% to 100%), since 2011. From bottom to top: blue = private wage employee; orange = own-account worker; green = government employee; purple = domestic worker; amber = employer; teal = day labourer; brown = unpaid family worker. Each share uses 12-month moving averages of employment, which removes seasonality. The ‘other’ category (under 0.1%) is omitted.",
            "importa": "In Colombia close to half of workers are self-employed or in positions without a contract, which is associated with informality, unstable incomes and low productivity. A rising share of wage employees usually accompanies formalisation and firm expansion. For an investor it signals the depth of the formal labour market, household income stability and the contributor base.",
            "interpretar": [
                "If the blue band widens at the expense of the orange one, employment is becoming more wage-based; the opposite signals more self-employment.",
                "Private wage employees are mostly formal, but not all; for the exact informality figure use the informality chart.",
                "In recessions own-account work tends to absorb those who lose wage jobs; look around 2020.",
                "As a 12-month average, changes appear gradually and with a lag; the one-year change by status chart shows recent moves."
            ],
            "formulas": [
                ["12-month average", "Ē<sub>p,t</sub> = (1 ÷ 12) × Σ<sub>k=0..11</sub> E<sub>p,t−k</sub>", "E = employed in status p in month t"],
                ["Share", "S<sub>p,t</sub> = Ē<sub>p,t</sub> ÷ Σ<sub>j</sub> Ē<sub>j,t</sub> × 100", "j runs over the seven statuses plotted"]
            ]
        },
    },
    "g-emp-posicion-cambio": {
        "es": {
            "que": "Muestra cuántos ocupados ganó o perdió cada posición ocupacional (CISE-93 de la OIT) en el último año, en miles de personas. Indica qué tipo de empleo se está creando: si el aumento del número de ocupados viene de puestos asalariados, en su mayoría con contrato, o del trabajo por cuenta propia y otras formas más expuestas a la informalidad.",
            "leer": "Cada barra horizontal es una posición ocupacional, ordenada del mayor aumento (arriba) a la mayor caída (abajo); el eje está en miles de personas y la línea vertical marca el cero. Barras azules: más ocupados que un año antes; naranjas: menos. La cifra al lado es el cambio redondeado. Se compara el promedio de los últimos 3 meses con el de los mismos meses del año anterior, sin desestacionalizar.",
            "importa": "No todo empleo nuevo tiene el mismo valor económico: un puesto asalariado privado suele traer contrato, cotización a la seguridad social e ingreso estable, mientras que el trabajo por cuenta propia suele ser informal y de menor productividad. Para un inversionista, la mezcla del empleo creado es un indicador de la calidad del ingreso laboral que respalda el consumo y la capacidad de pago de los hogares.",
            "interpretar": [
                "Si la barra de asalariado privado supera a la de cuenta propia, el empleo crece por la vía de los contratos; si ocurre lo contrario, crece sobre todo por trabajo independiente.",
                "La suma de las barras aproxima el cambio anual del total de ocupados.",
                "Las posiciones pequeñas (empleador, jornalero, familiar sin pago) tienen más error de muestreo; cambios de pocas decenas de miles pueden no ser significativos.",
                "Léalo junto con la composición del empleo (tendencia de 12 meses) y con la proporción de informalidad."
            ],
            "formulas": [
                ["Promedio de 3 meses", "Ō<sub>p,t</sub> = (O<sub>p,t</sub> + O<sub>p,t−1</sub> + O<sub>p,t−2</sub>) ÷ 3", "O = ocupados en la posición p en el mes t (miles)"],
                ["Cambio en un año", "ΔO<sub>p</sub> = Ō<sub>p,t</sub> − Ō<sub>p,t−12</sub>", "en miles de personas"]
            ]
        },
        "en": {
            "que": "This chart shows how many workers each status in employment (ILO ICSE-93) gained or lost over the last year, in thousands of people. It shows what kind of jobs are being created: whether the increase in employment comes from wage positions, mostly with a contract, or from own-account work and other forms more exposed to informality.",
            "leer": "Each horizontal bar is a status in employment, sorted from the largest gain (top) to the largest loss (bottom); the axis is in thousands of people and the vertical line marks zero. Blue bars: more workers than a year earlier; orange: fewer. The figure alongside is the rounded change. The average of the last 3 months is compared with the same months a year earlier, not seasonally adjusted.",
            "importa": "Not every new job has the same economic value: a private wage job usually brings a contract, social security contributions and a stable income, whereas own-account work tends to be informal and less productive. For an investor, the mix of jobs created indicates the quality of the labour income that underpins consumption and households' ability to repay debt.",
            "interpretar": [
                "If the private wage employee bar exceeds the own-account bar, employment is growing through contracts; if the reverse, mainly through self-employment.",
                "The bars add up to roughly the annual change in total employment.",
                "Small categories (employer, day labourer, unpaid family worker) carry more sampling error; changes of a few tens of thousands may not be significant.",
                "Read it together with the composition of employment (12-month trend) and with the informality share."
            ],
            "formulas": [
                ["3-month average", "Ē<sub>p,t</sub> = (E<sub>p,t</sub> + E<sub>p,t−1</sub> + E<sub>p,t−2</sub>) ÷ 3", "E = employed in status p in month t (thousands)"],
                ["One-year change", "ΔE<sub>p</sub> = Ē<sub>p,t</sub> − Ē<sub>p,t−12</sub>", "in thousands of people"]
            ]
        },
    },
    "g-emp-genero-td": {
        "es": {
            "que": "Compara la tasa de desempleo de las mujeres y la de los hombres en el total nacional. Muestra una de las brechas más persistentes del mercado laboral colombiano: el desempleo femenino ha estado de forma sistemática por encima del masculino. Permite ver si esa brecha se cierra o se amplía con el tiempo y cómo reaccionó cada grupo a los choques, como la pandemia de 2020.",
            "leer": "Eje vertical en porcentaje, desde cero; eje horizontal desde 2011. Línea naranja = mujeres; línea azul = hombres. Cada punto es el promedio de las tasas mensuales de los últimos 12 meses, sin desestacionalizar: promediar un año completo elimina la estacionalidad sin usar modelos estadísticos. La distancia vertical entre las dos líneas es la brecha de desempleo en puntos porcentuales.",
            "importa": "La brecha de género en el desempleo refleja barreras de acceso al empleo, la carga de cuidado no remunerado y la segmentación por sectores. Cerrarla amplía la oferta de trabajo efectiva, el ingreso de los hogares y el crecimiento potencial. Para un inversionista indica cuánto talento queda sin aprovechar y la profundidad del mercado de consumo.",
            "interpretar": [
                "Si las dos líneas se acercan, la brecha se reduce; si se separan, se amplía.",
                "Una caída del desempleo femenino puede deberse a que más mujeres consiguen trabajo o a que dejan de buscarlo; léalo con la participación laboral por sexo.",
                "El promedio de 12 meses reacciona con rezago: un cambio brusco tarda varios meses en verse completo.",
                "Al no estar desestacionalizada, la serie no es directamente comparable con la tasa de desempleo nacional desestacionalizada del primer gráfico."
            ],
            "formulas": [
                ["Tasa de desempleo por sexo", "TD<sub>s,t</sub> = D<sub>s,t</sub> ÷ FT<sub>s,t</sub> × 100", "D = desocupados; FT = fuerza de trabajo; s = mujeres u hombres"],
                ["Promedio de 12 meses", "TD12<sub>s,t</sub> = (1 ÷ 12) × Σ<sub>k=0..11</sub> TD<sub>s,t−k</sub>", "promedio simple de las tasas mensuales"],
                ["Brecha", "B<sub>t</sub> = TD12<sub>mujeres,t</sub> − TD12<sub>hombres,t</sub>", "en puntos porcentuales"]
            ]
        },
        "en": {
            "que": "This chart compares the unemployment rate of women and men nationwide. It shows one of the most persistent gaps in Colombia's labour market: female unemployment has been systematically above male unemployment. It lets you see whether the gap is narrowing or widening and how each group reacted to shocks such as the 2020 pandemic.",
            "leer": "Vertical axis in percent, starting at zero; horizontal axis from 2011. Orange line = women; blue line = men. Each point is the average of the monthly rates over the last 12 months, not seasonally adjusted: averaging a full year removes seasonality without statistical models. The vertical distance between the two lines is the unemployment gap in percentage points.",
            "importa": "The gender unemployment gap reflects barriers to accessing jobs, the burden of unpaid care work and sectoral segmentation. Narrowing it expands effective labour supply, household income and potential growth. For an investor it shows how much talent is left untapped and how deep the consumer market is.",
            "interpretar": [
                "If the two lines converge, the gap is narrowing; if they diverge, it is widening.",
                "Lower female unemployment can mean more women find jobs or that they stop looking; read it with participation by sex.",
                "The 12-month average reacts with a lag: an abrupt change takes several months to show fully.",
                "Because it is not seasonally adjusted, the series is not directly comparable with the seasonally adjusted national rate in the first chart."
            ],
            "formulas": [
                ["Unemployment rate by sex", "UR<sub>s,t</sub> = U<sub>s,t</sub> ÷ LF<sub>s,t</sub> × 100", "U = unemployed; LF = labour force; s = women or men"],
                ["12-month average", "UR12<sub>s,t</sub> = (1 ÷ 12) × Σ<sub>k=0..11</sub> UR<sub>s,t−k</sub>", "simple average of monthly rates"],
                ["Gap", "G<sub>t</sub> = UR12<sub>women,t</sub> − UR12<sub>men,t</sub>", "in percentage points"]
            ]
        },
    },
    "g-emp-genero-tgp": {
        "es": {
            "que": "Compara la tasa global de participación (TGP) de mujeres y hombres: el porcentaje de las personas en edad de trabajar (15 años y más) que trabajan o buscan trabajo. Muestra que una proporción mucho menor de mujeres participa en el mercado laboral, en buena medida por el trabajo de cuidado y del hogar no remunerado, y si esa distancia cambia con el tiempo.",
            "leer": "Eje vertical en porcentaje, de 40% a 90% (no empieza en cero, para ver mejor los cambios); eje horizontal desde 2011. Línea naranja = mujeres; línea azul = hombres. Cada punto es el promedio de las tasas mensuales de los últimos 12 meses, sin desestacionalizar. La distancia vertical entre ambas líneas es la brecha de participación en puntos porcentuales.",
            "importa": "La participación laboral determina cuánta mano de obra está disponible para producir. La baja participación femenina es una de las principales fuentes de crecimiento potencial no aprovechado en Colombia: cada punto adicional amplía la fuerza de trabajo y el ingreso de los hogares. Para un inversionista ayuda a entender la oferta laboral, el consumo y la dinámica demográfica del país.",
            "interpretar": [
                "Una TGP femenina en aumento con desempleo estable indica que más mujeres consiguen empleo; si sube junto con el desempleo, entran más de las que el mercado absorbe.",
                "La caída de 2020 refleja salidas masivas de la fuerza de trabajo, mayores entre las mujeres, que no aparecen como desempleo.",
                "Una participación más baja puede deberse a más años de estudio (positivo) o a más oficios del hogar; el gráfico de población fuera de la fuerza de trabajo muestra la razón.",
                "El eje recortado amplía visualmente las diferencias; lea siempre los valores del eje."
            ],
            "formulas": [
                ["Tasa global de participación", "TGP<sub>s,t</sub> = FT<sub>s,t</sub> ÷ PET<sub>s,t</sub> × 100", "FT = fuerza de trabajo (ocupados + desocupados); PET = población en edad de trabajar (15 años y más); s = sexo"],
                ["Promedio de 12 meses", "TGP12<sub>s,t</sub> = (1 ÷ 12) × Σ<sub>k=0..11</sub> TGP<sub>s,t−k</sub>", "promedio simple de las tasas mensuales"]
            ]
        },
        "en": {
            "que": "This chart compares the labour force participation rate of women and men: the share of working-age people (15 and over) who work or look for work. It shows that a much smaller share of women take part in the labour market, largely because of unpaid care and household work, and whether that distance is changing over time.",
            "leer": "Vertical axis in percent, from 40% to 90% (it does not start at zero, to make changes visible); horizontal axis from 2011. Orange line = women; blue line = men. Each point is the average of the monthly rates over the last 12 months, not seasonally adjusted. The vertical distance between the lines is the participation gap in percentage points.",
            "importa": "Participation determines how much labour is available for production. Low female participation is one of the main sources of untapped potential growth in Colombia: each additional point enlarges the labour force and household income. For an investor it helps understand labour supply, consumption and the country's demographic dynamics.",
            "interpretar": [
                "Rising female participation with stable unemployment means more women are finding jobs; if it rises with unemployment, more are entering than the market absorbs.",
                "The 2020 drop reflects mass exits from the labour force, larger among women, which do not show up as unemployment.",
                "Lower participation may reflect more years of schooling (positive) or more household work; the chart on people outside the labour force shows why.",
                "The truncated axis visually magnifies differences; always read the axis values."
            ],
            "formulas": [
                ["Participation rate", "PR<sub>s,t</sub> = LF<sub>s,t</sub> ÷ WAP<sub>s,t</sub> × 100", "LF = labour force (employed + unemployed); WAP = working-age population (15 and over); s = sex"],
                ["12-month average", "PR12<sub>s,t</sub> = (1 ÷ 12) × Σ<sub>k=0..11</sub> PR<sub>s,t−k</sub>", "simple average of monthly rates"]
            ]
        },
    },
    "g-emp-jovenes": {
        "es": {
            "que": "Muestra la tasa de desempleo de los jóvenes de 15 a 28 años (rango definido por la Ley 1622 de 2013, Estatuto de Ciudadanía Juvenil), en total y por sexo, frente al desempleo de toda la población. Revela que los jóvenes enfrentan tasas de desempleo muy superiores al promedio y que las mujeres jóvenes son el grupo más afectado.",
            "leer": "Eje vertical en porcentaje, desde cero; eje horizontal desde 2011. Línea azul gruesa = todos los jóvenes; naranja = mujeres jóvenes; verde = hombres jóvenes. Las series juveniles son trimestres móviles (tres meses que terminan en el mes indicado), sin desestacionalizar, del boletín de juventud de la GEIH. La línea gris punteada es la tasa de desempleo nacional mensual desestacionalizada, como referencia.",
            "importa": "El desempleo juvenil prolongado deja cicatrices duraderas: menor experiencia, salarios más bajos a lo largo de la vida y mayor probabilidad de informalidad. Afecta la acumulación de capital humano y la cohesión social. Para un inversionista es un indicador de la presión social y del aprovechamiento del bono demográfico del país.",
            "interpretar": [
                "La distancia entre la línea azul y la gris mide cuánto peor les va a los jóvenes; una relación cercana a dos veces el promedio nacional es habitual en muchos países.",
                "La separación entre la línea naranja y la verde es la brecha de género entre jóvenes, en general mayor que entre adultos.",
                "Las series juveniles no están desestacionalizadas y la referencia sí: compare cada serie juvenil con el mismo trimestre de años anteriores, no mes a mes.",
                "Los jóvenes que estudian y no buscan trabajo no cuentan como desempleados; complemente con el gráfico de jóvenes que ni estudian ni están ocupados."
            ],
            "formulas": [
                ["Tasa de desempleo juvenil", "TD<sup>J</sup><sub>t</sub> = D<sup>J</sup><sub>t</sub> ÷ FT<sup>J</sup><sub>t</sub> × 100", "D<sup>J</sup> = desocupados de 15 a 28 años; FT<sup>J</sup> = fuerza de trabajo de 15 a 28 años; trimestre móvil terminado en t"]
            ]
        },
        "en": {
            "que": "This chart shows the unemployment rate of young people aged 15 to 28 (the range set by Law 1622 of 2013, the Youth Citizenship Statute), overall and by sex, against unemployment for the whole population. It reveals that young people face unemployment rates well above average and that young women are the most affected group.",
            "leer": "Vertical axis in percent, starting at zero; horizontal axis from 2011. Thick blue line = all young people; orange = young women; green = young men. The youth series are rolling quarters (three months ending in the month shown), not seasonally adjusted, from the GEIH youth bulletin. The dotted grey line is the monthly seasonally adjusted national unemployment rate, for reference.",
            "importa": "Prolonged youth unemployment leaves lasting scars: less experience, lower lifetime wages and a higher likelihood of informality. It affects human capital accumulation and social cohesion. For an investor it is an indicator of social pressure and of how well the country is using its demographic dividend.",
            "interpretar": [
                "The distance between the blue and grey lines measures how much worse young people fare; a ratio of about twice the national rate is common in many countries.",
                "The gap between the orange and green lines is the gender gap among young people, usually wider than among adults.",
                "The youth series are not seasonally adjusted while the reference is: compare each youth series with the same quarter in earlier years, not month to month.",
                "Young people studying and not looking for work are not counted as unemployed; complement with the chart on youth neither studying nor employed."
            ],
            "formulas": [
                ["Youth unemployment rate", "UR<sup>Y</sup><sub>t</sub> = U<sup>Y</sup><sub>t</sub> ÷ LF<sup>Y</sup><sub>t</sub> × 100", "U<sup>Y</sup> = unemployed aged 15–28; LF<sup>Y</sup> = labour force aged 15–28; rolling quarter ending in t"]
            ]
        },
    },
    "g-emp-nini": {
        "es": {
            "que": "Muestra el porcentaje de jóvenes de 15 a 28 años que ni estudian ni están ocupados (conocidos como «ninis»), y cuánto de ese total corresponde a mujeres y cuánto a hombres. Es una medida más amplia de exclusión juvenil que el desempleo, porque incluye también a quienes no buscan trabajo, por ejemplo por dedicarse a oficios del hogar o por desaliento.",
            "leer": "Áreas apiladas en porcentaje del total de jóvenes de 15 a 28 años, desde 2011: la franja naranja (abajo) son las mujeres que ni estudian ni están ocupadas y la azul (arriba) los hombres; el borde superior es el total. Ambas franjas están expresadas sobre el total de jóvenes (no sobre los jóvenes de cada sexo), por eso se suman. Datos en trimestre móvil, sin desestacionalizar.",
            "importa": "Los jóvenes que no acumulan educación ni experiencia laboral pierden capital humano en la etapa de la vida en que más rinde, con efectos sobre su ingreso futuro y sobre la productividad del país. Una proporción alta también se asocia a mayor vulnerabilidad social. Para un inversionista, es un indicador del aprovechamiento del bono demográfico y de la calidad de la futura fuerza de trabajo.",
            "interpretar": [
                "Si el área total se reduce, una mayor parte de los jóvenes estudia o trabaja.",
                "La franja naranja suele ser bastante más ancha: muchas jóvenes están fuera del estudio y del empleo por labores de cuidado y del hogar.",
                "Como es trimestre móvil sin desestacionalizar, compare con el mismo periodo de años anteriores (los ciclos académicos influyen).",
                "Complemente con el desempleo juvenil y con la población fuera de la fuerza de trabajo."
            ],
            "formulas": [
                ["Proporción de ninis", "N<sub>t</sub> = J<sup>NEO</sup><sub>t</sub> ÷ J<sub>t</sub> × 100", "J<sup>NEO</sup> = jóvenes de 15 a 28 años que no estudian ni están ocupados; J = total de jóvenes de 15 a 28 años"],
                ["Descomposición por sexo", "N<sub>t</sub> = J<sup>NEO</sup><sub>mujeres,t</sub> ÷ J<sub>t</sub> × 100 + J<sup>NEO</sup><sub>hombres,t</sub> ÷ J<sub>t</sub> × 100", "cada franja se calcula sobre el total de jóvenes"]
            ]
        },
        "en": {
            "que": "This chart shows the share of young people aged 15 to 28 who are neither studying nor employed (often called NEET), and how much of that total is women and how much men. It is a broader measure of youth exclusion than unemployment, because it also covers those not looking for work, for instance because of household duties or discouragement.",
            "leer": "Stacked areas as a percentage of all 15–28 year-olds, since 2011: the orange band (bottom) is women neither studying nor employed and the blue band (top) men; the upper edge is the total. Both bands are expressed over all young people (not over each sex), which is why they add up. Rolling-quarter data, not seasonally adjusted.",
            "importa": "Young people who build neither education nor work experience lose human capital at the stage of life when it pays off most, affecting their future income and the country's productivity. A high share is also linked to greater social vulnerability. For an investor it indicates how well the demographic dividend is being used and the quality of the future workforce.",
            "interpretar": [
                "If the total area shrinks, a larger share of young people are studying or working.",
                "The orange band is usually much wider: many young women are out of school and work because of care and household duties.",
                "As a non-seasonally adjusted rolling quarter, compare with the same period in earlier years (school calendars matter).",
                "Complement with youth unemployment and with the population outside the labour force."
            ],
            "formulas": [
                ["NEET share", "N<sub>t</sub> = Y<sup>NEET</sup><sub>t</sub> ÷ Y<sub>t</sub> × 100", "Y<sup>NEET</sup> = 15–28 year-olds neither studying nor employed; Y = all 15–28 year-olds"],
                ["Split by sex", "N<sub>t</sub> = Y<sup>NEET</sup><sub>women,t</sub> ÷ Y<sub>t</sub> × 100 + Y<sup>NEET</sup><sub>men,t</sub> ÷ Y<sub>t</sub> × 100", "each band is computed over all young people"]
            ]
        },
    },
    "g-emp-area": {
        "es": {
            "que": "Compara la tasa de desempleo en las cabeceras municipales (los cascos urbanos) con la de los centros poblados y el rural disperso (el campo). Muestra que el desempleo urbano es de forma persistente mayor que el rural, lo que no significa mejores condiciones en el campo: allí predominan el trabajo por cuenta propia, el agro y la informalidad.",
            "leer": "Eje vertical en porcentaje, desde cero; eje horizontal desde 2011. Línea azul = cabeceras; línea verde = campo (centros poblados y rural disperso). Cada punto es un trimestre móvil (tres meses que terminan en el mes indicado), sin desestacionalizar. La distancia vertical entre ambas líneas es la diferencia de desempleo entre ciudad y campo, en pp.",
            "importa": "La geografía del desempleo muestra dónde se concentra la holgura laboral y ayuda a entender el impacto regional del ciclo económico, de la construcción y de la industria (más urbanas) frente al agro (rural). Para un inversionista ayuda a dimensionar mercados de consumo urbanos y el riesgo social en las ciudades.",
            "interpretar": [
                "Un desempleo rural bajo suele reflejar que en el campo casi todos trabajan en algo, aunque sea en actividades informales o de baja productividad; compárelo con la informalidad por sector.",
                "El desempleo rural tiene estacionalidad marcada por las cosechas; compare con el mismo trimestre de años anteriores.",
                "Las cabeceras concentran la mayor parte de la fuerza de trabajo, por lo que dominan el promedio nacional.",
                "La muestra rural es más pequeña y su estimación es más volátil."
            ],
            "formulas": [
                ["Tasa de desempleo por zona", "TD<sub>z,t</sub> = D<sub>z,t</sub> ÷ FT<sub>z,t</sub> × 100", "D = desocupados; FT = fuerza de trabajo; z = cabeceras o centros poblados y rural disperso; trimestre móvil terminado en t"],
                ["Diferencia ciudad−campo", "Δ<sub>t</sub> = TD<sub>cabeceras,t</sub> − TD<sub>campo,t</sub>", "en puntos porcentuales"]
            ]
        },
        "en": {
            "que": "This chart compares the unemployment rate in municipal town centres (urban areas) with that in villages and dispersed rural areas (the countryside). It shows that urban unemployment is persistently higher than rural unemployment, which does not mean better conditions in the countryside: self-employment, farming and informality dominate there.",
            "leer": "Vertical axis in percent, starting at zero; horizontal axis from 2011. Blue line = urban; green line = rural (villages and dispersed rural areas). Each point is a rolling quarter (three months ending in the month shown), not seasonally adjusted. The vertical distance between the lines is the urban–rural unemployment gap, in pp.",
            "importa": "The geography of unemployment shows where labour slack is concentrated and helps explain the regional impact of the business cycle, of construction and manufacturing (more urban) versus farming (rural). For an investor it helps size urban consumer markets and social risk in cities.",
            "interpretar": [
                "Low rural unemployment usually reflects that almost everyone in the countryside works at something, even in informal or low-productivity activities; compare with informality by sector.",
                "Rural unemployment has marked seasonality linked to harvests; compare with the same quarter in earlier years.",
                "Urban areas hold most of the labour force, so they dominate the national average.",
                "The rural sample is smaller and its estimate more volatile."
            ],
            "formulas": [
                ["Unemployment rate by area", "UR<sub>a,t</sub> = U<sub>a,t</sub> ÷ LF<sub>a,t</sub> × 100", "U = unemployed; LF = labour force; a = urban or rural; rolling quarter ending in t"],
                ["Urban−rural gap", "Δ<sub>t</sub> = UR<sub>urban,t</sub> − UR<sub>rural,t</sub>", "in percentage points"]
            ]
        },
    },
    "g-emp-fuera": {
        "es": {
            "que": "Muestra cuántas personas en edad de trabajar no trabajan ni buscan trabajo, es decir, la población fuera de la fuerza de trabajo, y por qué: porque estudian, porque se dedican a oficios del hogar o por otras razones (pensionados, rentistas, personas con incapacidad permanente para trabajar). Ayuda a entender la otra cara de la tasa de participación.",
            "leer": "Áreas apiladas en millones de personas, total nacional, desde 2011. De abajo hacia arriba: naranja = oficios del hogar; azul = estudiando; morado = otros (pensionados, rentistas, incapacitados). El borde superior es el total de personas fuera de la fuerza de trabajo. Cada punto es el promedio de los últimos 12 meses de los datos mensuales, lo que elimina la estacionalidad.",
            "importa": "Una población inactiva grande reduce la oferta de trabajo disponible y la base de ingresos de la economía. Su composición importa: estudiar es una inversión en capital humano, mientras que una franja de oficios del hogar muy amplia, mayoritariamente femenina, indica barreras para incorporarse al empleo remunerado. Para un inversionista es clave para entender el potencial de crecimiento de la fuerza laboral.",
            "interpretar": [
                "Si el total crece más rápido que la población en edad de trabajar, la participación laboral está cayendo.",
                "Un aumento de la franja «estudiando» suele ser favorable; uno de «oficios del hogar» suele asociarse a labores de cuidado no remuneradas.",
                "El envejecimiento de la población tiende a ampliar la franja de «otros» por el mayor número de pensionados.",
                "El salto de 2020 refleja personas que dejaron de buscar trabajo durante la pandemia; compare con la participación por sexo."
            ],
            "formulas": [
                ["Población fuera de la fuerza de trabajo", "PFFT<sub>t</sub> = PET<sub>t</sub> − FT<sub>t</sub> = Est<sub>t</sub> + Hog<sub>t</sub> + Otr<sub>t</sub>", "PET = población en edad de trabajar; FT = fuerza de trabajo; Est, Hog, Otr = según actividad principal"],
                ["Promedio de 12 meses", "X̄<sub>t</sub> = (1 ÷ 12) × Σ<sub>k=0..11</sub> X<sub>t−k</sub> ÷ 1.000", "X = personas en cada categoría (miles); el resultado queda en millones"]
            ]
        },
        "en": {
            "que": "This chart shows how many working-age people neither work nor look for work, that is, the population outside the labour force, and why: because they study, because they do household work or for other reasons (retirees, rentiers, people permanently unable to work). It helps understand the other side of the participation rate.",
            "leer": "Stacked areas in millions of people, national total, since 2011. From bottom to top: orange = household work; blue = studying; purple = other (retired, rentiers, disabled). The upper edge is the total population outside the labour force. Each point is the average of the last 12 months of monthly data, which removes seasonality.",
            "importa": "A large inactive population reduces available labour supply and the economy's income base. Its composition matters: studying is an investment in human capital, whereas a very large household-work band, mostly women, signals barriers to entering paid work. For an investor it is key to understanding the growth potential of the labour force.",
            "interpretar": [
                "If the total grows faster than the working-age population, participation is falling.",
                "A wider ‘studying’ band is usually favourable; a wider ‘household work’ band is usually linked to unpaid care.",
                "Population ageing tends to widen the ‘other’ band through a larger number of retirees.",
                "The 2020 jump reflects people who stopped looking for work during the pandemic; compare with participation by sex."
            ],
            "formulas": [
                ["Population outside the labour force", "OLF<sub>t</sub> = WAP<sub>t</sub> − LF<sub>t</sub> = Stu<sub>t</sub> + Hh<sub>t</sub> + Oth<sub>t</sub>", "WAP = working-age population; LF = labour force; Stu, Hh, Oth = by main activity"],
                ["12-month average", "X̄<sub>t</sub> = (1 ÷ 12) × Σ<sub>k=0..11</sub> X<sub>t−k</sub> ÷ 1,000", "X = people in each category (thousands); the result is in millions"]
            ]
        },
    },
    "g-cap-ciudades": {
        "es": {
            "que": "Compara la tasa de desempleo de las 32 ciudades capitales de departamento (13 de ellas con su área metropolitana) en el último año móvil, frente al año móvil terminado doce meses antes. Muestra la gran dispersión regional del desempleo en Colombia y en qué ciudades mejoró o empeoró en el último año.",
            "leer": "Cada fila es una ciudad, ordenada por su tasa más reciente (la más alta arriba); el eje horizontal está en porcentaje y empieza en cero. El punto gris es la tasa del año móvil terminado un año antes y el punto de color la del año móvil más reciente; la línea que los une muestra la magnitud del cambio. Punto verde: el desempleo bajó o no cambió; naranja: subió. Año móvil = promedio de los 12 meses que terminan en el último mes publicado.",
            "importa": "El desempleo urbano difiere mucho entre regiones según su estructura productiva, su grado de informalidad y su exposición a choques como la migración, el comercio fronterizo o los precios de las materias primas. Para un inversionista ayuda a identificar mercados laborales más holgados o más estrechos al decidir dónde ubicar operaciones, contratar o vender.",
            "interpretar": [
                "Una línea larga entre el punto gris y el de color indica un cambio grande en el año; una línea corta, estabilidad.",
                "Una tasa baja no siempre indica un mercado laboral sano: puede coincidir con alta informalidad o baja participación.",
                "El año móvil elimina la estacionalidad y reduce el error de muestreo, pero reacciona con rezago a los cambios recientes.",
                "Las ciudades pequeñas tienen muestras menores en la GEIH y cifras más volátiles; diferencias de 1 pp entre ellas pueden no ser significativas."
            ],
            "formulas": [
                ["Tasa de desempleo de la ciudad (año móvil)", "TD<sub>c,t</sub> = D<sub>c</sub> ÷ FT<sub>c</sub> × 100", "D = desocupados; FT = fuerza de trabajo de la ciudad c en los 12 meses que terminan en t (cálculo del DANE)"],
                ["Cambio en un año", "ΔTD<sub>c</sub> = TD<sub>c,t</sub> − TD<sub>c,t−12</sub>", "en pp; verde si ΔTD ≤ 0, naranja si ΔTD > 0"]
            ]
        },
        "en": {
            "que": "This chart compares the unemployment rate of Colombia's 32 departmental capital cities (13 of them with their metropolitan area) over the latest rolling year, against the rolling year ending twelve months earlier. It shows the wide regional dispersion of unemployment in Colombia and where it improved or worsened over the last year.",
            "leer": "Each row is a city, sorted by its latest rate (highest at the top); the horizontal axis is in percent and starts at zero. The grey dot is the rate for the rolling year ending a year earlier and the coloured dot the latest rolling year; the line between them shows the size of the change. Green dot: unemployment fell or was unchanged; orange: it rose. Rolling year = average of the 12 months ending in the latest published month.",
            "importa": "Urban unemployment varies widely across regions according to their productive structure, degree of informality and exposure to shocks such as migration, border trade or commodity prices. For an investor it helps identify slacker or tighter labour markets when deciding where to locate operations, hire or sell.",
            "interpretar": [
                "A long line between the grey and coloured dots signals a large change over the year; a short line, stability.",
                "A low rate does not always mean a healthy labour market: it can coincide with high informality or low participation.",
                "The rolling year removes seasonality and reduces sampling error, but reacts with a lag to recent changes.",
                "Smaller cities have smaller GEIH samples and more volatile figures; 1 pp differences between them may not be significant."
            ],
            "formulas": [
                ["City unemployment rate (rolling year)", "UR<sub>c,t</sub> = U<sub>c</sub> ÷ LF<sub>c</sub> × 100", "U = unemployed; LF = labour force of city c over the 12 months ending in t (DANE calculation)"],
                ["One-year change", "ΔUR<sub>c</sub> = UR<sub>c,t</sub> − UR<sub>c,t−12</sub>", "in pp; green if ΔUR ≤ 0, orange if ΔUR > 0"]
            ]
        },
    },
    # =========================================================================================== TASAS
    "g-politica": {
        "es": {
            "que": "Compara la tasa de política monetaria (TPM), la tasa de interés de intervención que fija la Junta Directiva del Banco de la República, con la inflación anual medida por el índice de precios al consumidor (IPC) del DANE. Resume la estrategia del Banco: sube la tasa cuando la inflación se aleja de la meta y la baja cuando cede. La distancia entre ambas líneas da una idea de cuán restrictiva es la política.",
            "leer": "Panel superior, en % anual: la línea azul en escalones es la TPM (último dato de cada semana; cada escalón es una decisión de la Junta); la línea naranja es la inflación anual del IPC, mensual; la línea verde punteada marca la meta de inflación del 3%. Si hay una decisión ya anunciada que aún no rige, aparece como una estrella azul en la fecha en que entra en vigor. Panel inferior: cambio de la TPM frente a un año antes, en pp (azul = subió, naranja = bajó). Vista inicial de diez años.",
            "importa": "La TPM es el ancla de todas las tasas de interés en pesos: del mercado interbancario, de los CDT, del crédito y de los TES. Determina el costo de financiación de empresas, hogares y Gobierno, y afecta el atractivo de los activos en pesos frente a los de otros países. Para un inversionista es la variable que más mueve la curva de rendimientos y el tipo de cambio en el corto plazo.",
            "interpretar": [
                "Una TPM muy por encima de la inflación indica una política restrictiva (el dinero es caro en términos reales); por debajo, una política expansiva.",
                "La política monetaria actúa con rezago: sus efectos sobre la inflación suelen tardar entre 12 y 24 meses, por lo que la Junta reacciona a la inflación esperada más que a la observada.",
                "Una comparación más precisa es con la inflación esperada (gráfico de tasa real frente a la tasa neutral), porque la inflación observada mira hacia atrás.",
                "Barras azules seguidas en el panel inferior marcan ciclos de subidas; naranjas, ciclos de bajadas (véase el gráfico de ciclos)."
            ],
            "formulas": [
                ["Inflación anual", "π<sub>t</sub> = (IPC<sub>t</sub> ÷ IPC<sub>t−12</sub> − 1) × 100", "IPC = índice de precios al consumidor del mes t"],
                ["Cambio anual de la TPM (panel inferior)", "ΔTPM<sub>t</sub> = TPM<sub>t</sub> − TPM<sub>t−1 año</sub>", "en puntos porcentuales; TPM semanal (último dato de la semana)"]
            ]
        },
        "en": {
            "que": "This chart compares the monetary policy rate (TPM), the intervention rate set by the Board of the Banco de la República, with annual inflation measured by DANE's consumer price index (CPI). It sums up the Bank's strategy: raise the rate when inflation drifts away from target and cut it when inflation eases. The distance between the lines gives a sense of how restrictive policy is.",
            "leer": "Top panel, in % a year: the stepped blue line is the policy rate (last value each week; each step is a Board decision); the orange line is annual CPI inflation, monthly; the dotted green line marks the 3% inflation target. If a decision has been announced but is not yet in force, it appears as a blue star on its effective date. Bottom panel: change in the policy rate versus a year earlier, in pp (blue = up, orange = down). Initial view of ten years.",
            "importa": "The policy rate anchors every peso interest rate: interbank, CDs, lending and TES government bonds. It sets the funding cost of firms, households and government, and affects the appeal of peso assets relative to other countries. For an investor it is the variable that moves the yield curve and the exchange rate most in the short run.",
            "interpretar": [
                "A policy rate well above inflation signals restrictive policy (money is expensive in real terms); below it, expansionary policy.",
                "Monetary policy works with a lag: its effects on inflation usually take 12 to 24 months, so the Board reacts to expected rather than observed inflation.",
                "A sharper comparison is against expected inflation (real rate versus neutral rate chart), since observed inflation looks backward.",
                "Runs of blue bars in the bottom panel mark hiking cycles; orange ones, easing cycles (see the cycles chart)."
            ],
            "formulas": [
                ["Annual inflation", "π<sub>t</sub> = (CPI<sub>t</sub> ÷ CPI<sub>t−12</sub> − 1) × 100", "CPI = consumer price index in month t"],
                ["Annual change in the policy rate (bottom panel)", "ΔTPM<sub>t</sub> = TPM<sub>t</sub> − TPM<sub>t−1 year</sub>", "in percentage points; weekly policy rate (last value of the week)"]
            ]
        },
    },
    "g-real": {
        "es": {
            "que": "Muestra la tasa de interés real ex ante: la tasa del Banco de la República descontada la inflación que el mercado espera para los próximos 12 meses. Es lo que de verdad cuesta endeudarse en términos de poder de compra. Se compara con la tasa real neutral, el nivel que ni estimula ni frena la economía, para medir la postura de la política monetaria.",
            "leer": "Panel superior, en % anual: la línea azul es la tasa real ex ante (dato semanal); la franja gris es el rango de tasa neutral estimado por el equipo técnico del Banco (2,7%–3,0%); la línea horizontal oscura marca el cero. La inflación esperada a un año es la inflación implícita (breakeven) en los TES (títulos de deuda pública): la diferencia entre el rendimiento a un año de los TES en pesos y el de los TES en UVR (unidad indexada a la inflación). Panel inferior: cambio frente a un año antes, en pp.",
            "importa": "La tasa nominal por sí sola no dice si la política es restrictiva: un 9% con inflación esperada del 8% es laxo, y con 3% es muy restrictivo. La distancia frente a la neutral es la medida estándar de cuánto está frenando o estimulando el Banco la demanda. Para un inversionista determina el rendimiento real de los activos en pesos y ayuda a leer la fase del ciclo monetario.",
            "interpretar": [
                "Por encima de la franja gris, la política frena la economía (restrictiva); dentro, es neutral; por debajo, la estimula (expansiva).",
                "Una tasa real negativa (bajo la línea de cero) significa que endeudarse cuesta menos que la inflación esperada.",
                "La tasa real puede subir sin que el Banco mueva su tasa, si cae la inflación esperada.",
                "La inflación implícita incluye primas de riesgo y de liquidez, y la tasa neutral no es observable sino estimada con incertidumbre: lea la franja como una zona, no como un valor exacto."
            ],
            "formulas": [
                ["Tasa real ex ante (Fisher)", "r<sub>t</sub> = [(1 + i<sub>t</sub> ÷ 100) ÷ (1 + π<sup>e</sup><sub>t</sub> ÷ 100) − 1] × 100", "i = tasa de política; π<sup>e</sup> = inflación esperada a 1 año"],
                ["Inflación implícita a 1 año", "π<sup>e</sup><sub>t</sub> = [(1 + y<sup>pesos</sup><sub>1a</sub> ÷ 100) ÷ (1 + y<sup>UVR</sup><sub>1a</sub> ÷ 100) − 1] × 100", "y = rendimiento de los TES a 1 año en pesos y en UVR"],
                ["Cambio anual (panel inferior)", "Δr<sub>t</sub> = r<sub>t</sub> − r<sub>t−1 año</sub>", "en puntos porcentuales"]
            ]
        },
        "en": {
            "que": "This chart shows the ex-ante real interest rate: the Banco de la República policy rate net of the inflation the market expects over the next 12 months. It is what borrowing really costs in terms of purchasing power. It is compared with the neutral real rate, the level that neither stimulates nor restrains the economy, to gauge the monetary policy stance.",
            "leer": "Top panel, in % a year: the blue line is the ex-ante real rate (weekly data); the grey band is the neutral-rate range estimated by the Bank's technical staff (2.7%–3.0%); the dark horizontal line marks zero. One-year expected inflation is the breakeven inflation in TES (government bonds): the gap between the one-year yield on peso TES and on UVR TES (a unit indexed to inflation). Bottom panel: change versus a year earlier, in pp.",
            "importa": "The nominal rate alone does not say whether policy is tight: 9% with 8% expected inflation is loose, and with 3% it is very tight. The distance from neutral is the standard measure of how much the Bank is restraining or stimulating demand. For an investor it sets the real return on peso assets and helps read the phase of the monetary cycle.",
            "interpretar": [
                "Above the grey band, policy restrains the economy (restrictive); inside it, neutral; below it, stimulative (expansionary).",
                "A negative real rate (below the zero line) means borrowing costs less than expected inflation.",
                "The real rate can rise without any move by the Bank if expected inflation falls.",
                "Breakeven inflation contains risk and liquidity premia, and the neutral rate is not observed but estimated with uncertainty: read the band as a zone, not an exact value."
            ],
            "formulas": [
                ["Ex-ante real rate (Fisher)", "r<sub>t</sub> = [(1 + i<sub>t</sub> ÷ 100) ÷ (1 + π<sup>e</sup><sub>t</sub> ÷ 100) − 1] × 100", "i = policy rate; π<sup>e</sup> = one-year expected inflation"],
                ["One-year breakeven inflation", "π<sup>e</sup><sub>t</sub> = [(1 + y<sup>peso</sup><sub>1y</sub> ÷ 100) ÷ (1 + y<sup>UVR</sup><sub>1y</sub> ÷ 100) − 1] × 100", "y = one-year TES yield in pesos and in UVR"],
                ["Annual change (bottom panel)", "Δr<sub>t</sub> = r<sub>t</sub> − r<sub>t−1 year</sub>", "in percentage points"]
            ]
        },
    },
    "g-ts-ciclos": {
        "es": {
            "que": "Muestra la trayectoria de la tasa de política monetaria (TPM) del Banco de la República desde 2000 y marca sus ciclos: periodos de subidas consecutivas para contener la inflación y periodos de bajadas consecutivas para apoyar la actividad. Permite comparar la duración y la intensidad de cada ciclo con los anteriores.",
            "leer": "Eje vertical en % anual. La línea azul en escalones es la TPM (último dato de cada semana); cada escalón es una decisión de la Junta Directiva. Las franjas naranjas sombrean los ciclos de subidas y las azules los de bajadas, desde la primera hasta la última decisión en la misma dirección. Un ciclo termina cuando una decisión va en sentido contrario; las pausas (decisiones sin cambio) no lo cortan. La tabla inferior detalla cada ciclo: fechas, número de decisiones, tasa inicial y final, cambio acumulado y duración.",
            "importa": "Los ciclos monetarios marcan el ritmo de las tasas de interés, del crédito, de los TES y de la valoración de los activos en pesos. Conocer la amplitud y la duración de los ciclos pasados da contexto para dimensionar el actual sin asumir que se repetirá. Para un inversionista es la referencia histórica básica de la política monetaria colombiana.",
            "interpretar": [
                "Franjas largas con escalones pequeños indican ajustes graduales; franjas cortas con escalones grandes, reacciones fuertes a choques (por ejemplo, la crisis financiera de 2008 o la pandemia de 2020).",
                "Los espacios sin franja son periodos de tasa estable o con decisiones aisladas entre ciclos.",
                "La amplitud de un ciclo depende del nivel de la inflación y de su distancia a la meta en cada época; los ciclos de comienzos de los 2000 ocurrieron con metas de inflación más altas.",
                "El último ciclo aparece como «en curso» en la tabla hasta que una decisión vaya en sentido contrario."
            ],
            "formulas": [
                ["Decisión", "m<sub>j</sub> = TPM<sub>d<sub>j</sub></sub> − TPM<sub>d<sub>j</sub>−1</sub> ≠ 0", "d<sub>j</sub> = fecha de la decisión j que cambia la tasa"],
                ["Cambio acumulado del ciclo", "C = Σ<sub>j∈ciclo</sub> m<sub>j</sub>", "suma de las decisiones consecutivas del mismo signo"]
            ]
        },
        "en": {
            "que": "This chart shows the path of the Banco de la República monetary policy rate since 2000 and marks its cycles: stretches of consecutive hikes to contain inflation and stretches of consecutive cuts to support activity. It lets you compare the length and intensity of each cycle with earlier ones.",
            "leer": "Vertical axis in % a year. The stepped blue line is the policy rate (last value each week); each step is a Board decision. Orange bands shade hiking cycles and blue bands easing cycles, from the first to the last decision in the same direction. A cycle ends when a decision goes the other way; pauses (no-change decisions) do not break it. The table below details each cycle: dates, number of decisions, starting and ending rate, cumulative change and length.",
            "importa": "Monetary cycles set the pace of interest rates, credit, TES bonds and the valuation of peso assets. Knowing the size and duration of past cycles gives context to gauge the current one without assuming it will repeat. For an investor it is the basic historical reference for Colombian monetary policy.",
            "interpretar": [
                "Long bands with small steps indicate gradual adjustment; short bands with large steps, strong reactions to shocks (for example, the 2008 financial crisis or the 2020 pandemic).",
                "Gaps without bands are periods of a stable rate or isolated decisions between cycles.",
                "A cycle's size depends on the level of inflation and its distance from target at the time; the early-2000s cycles took place under higher inflation targets.",
                "The latest cycle appears as ‘ongoing’ in the table until a decision goes the other way."
            ],
            "formulas": [
                ["Decision", "m<sub>j</sub> = TPM<sub>d<sub>j</sub></sub> − TPM<sub>d<sub>j</sub>−1</sub> ≠ 0", "d<sub>j</sub> = date of decision j that changes the rate"],
                ["Cumulative change in the cycle", "C = Σ<sub>j∈cycle</sub> m<sub>j</sub>", "sum of consecutive decisions with the same sign"]
            ]
        },
    },
    "g-ts-transmision": {
        "es": {
            "que": "Muestra cómo se transmite la tasa del Banco de la República a las demás tasas de la economía: el IBR a 3 meses (Indicador Bancario de Referencia, la tasa a la que los bancos se prestan pesos entre sí), los CDT a 90 días (certificados de depósito a término, lo que pagan los bancos por el ahorro) y las tasas del crédito nuevo. Permite ver si las tasas del mercado siguen a la de política, con qué rezago y con qué margen.",
            "leer": "Eje vertical en tasa efectiva anual, desde 2008, en promedios mensuales. Línea azul = tasa del Banco; morada = IBR a 3 meses; verde = CDT a 90 días; naranja continua = crédito nuevo total (tasa de colocación, promedio ponderado por monto desembolsado); naranja punteada = crédito de consumo. Las tasas diarias (tasa del Banco, IBR, CDT) y semanales (colocación) se promedian por mes.",
            "importa": "La política monetaria solo funciona si sus cambios llegan a las tasas que pagan y cobran hogares y empresas; ese es el canal de transmisión de las tasas de interés. Para un inversionista indica el costo de financiación efectivo de la economía, el rendimiento del ahorro en pesos y la rapidez con que una decisión del Banco cambia las condiciones del crédito.",
            "interpretar": [
                "El IBR a 3 meses sigue a la tasa del Banco casi de inmediato y suele anticipar sus movimientos, porque incorpora las decisiones que el mercado descuenta para los próximos meses.",
                "El CDT y el crédito reaccionan con rezago y de forma incompleta; la distancia entre crédito y CDT es el margen de los bancos (gráfico de margen).",
                "El crédito de consumo está muy por encima del promedio por su mayor riesgo y costo; el crédito nuevo total incluye operaciones de tesorería de muy corto plazo y bajo riesgo, que lo acercan a las tasas de mercado.",
                "Las tasas son nominales: compárelas con la inflación para ver su nivel real (gráfico de crédito por modalidad)."
            ],
            "formulas": [
                ["Promedio mensual", "R̄<sub>m</sub> = (1 ÷ n<sub>m</sub>) × Σ<sub>d∈m</sub> R<sub>d</sub>", "R = tasa diaria o semanal; n<sub>m</sub> = número de datos del mes m"]
            ]
        },
        "en": {
            "que": "This chart shows how the Banco de la República rate passes through to other rates in the economy: the 3-month IBR (Bank Reference Indicator, the rate at which banks lend pesos to each other), 90-day CDs (term deposit certificates, what banks pay on savings) and new-lending rates. It shows whether market rates follow the policy rate, with what lag and with what spread.",
            "leer": "Vertical axis in effective annual rate, since 2008, as monthly averages. Blue line = policy rate; purple = 3-month IBR; green = 90-day CD; solid orange = total new lending (lending rate, weighted by amount disbursed); dotted orange = consumer credit. Daily rates (policy rate, IBR, CD) and weekly ones (lending) are averaged by month.",
            "importa": "Monetary policy only works if its changes reach the rates households and firms pay and earn; that is the interest-rate transmission channel. For an investor it shows the economy's effective funding cost, the return on peso savings and how quickly a Bank decision changes credit conditions.",
            "interpretar": [
                "The 3-month IBR follows the policy rate almost immediately and often moves ahead of it, because it embeds the decisions the market prices for the coming months.",
                "CDs and lending react with a lag and incompletely; the distance between lending and CDs is the banks' spread (spread chart).",
                "Consumer credit sits well above the average because of its higher risk and cost; total new lending includes very short-term, low-risk treasury loans, which pull it toward market rates.",
                "Rates are nominal: compare them with inflation for their real level (lending by type chart)."
            ],
            "formulas": [
                ["Monthly average", "R̄<sub>m</sub> = (1 ÷ n<sub>m</sub>) × Σ<sub>d∈m</sub> R<sub>d</sub>", "R = daily or weekly rate; n<sub>m</sub> = number of observations in month m"]
            ]
        },
    },
    "g-ts-traspaso": {
        "es": {
            "que": "Mide el traspaso de cada ciclo de la tasa del Banco a nueve tasas del mercado: qué porcentaje del cambio acumulado de la tasa de política llegó a cada una. Compara los últimos ciclos desde 2008 y muestra que la transmisión es heterogénea: rápida y casi completa en el mercado interbancario, más lenta o parcial en el ahorro y en algunas modalidades de crédito.",
            "leer": "Mapa de calor: cada fila es un ciclo (fechas de la primera y la última decisión y, entre paréntesis, el cambio total de la tasa del Banco en pp); cada columna es una tasa: IBR a un día y a 3 meses, CDT a 90 días, DTF (promedio de captación a 90 días), crédito nuevo total, comercial ordinario, preferencial (corporativo), consumo y vivienda. El número de cada celda es el traspaso en %; el color va de claro (0% o menos) a azul (cerca de 100%) y morado (150% o más). «—» = la serie no existía al inicio del ciclo; * = ciclo en curso.",
            "importa": "El traspaso indica cuánto de una decisión del Banco termina en el costo del crédito y en el rendimiento del ahorro, y por tanto la potencia de la política monetaria. Para un inversionista ayuda a entender cuánto se mueven el costo de financiación, los márgenes bancarios y las tasas de los depósitos ante un ciclo de política.",
            "interpretar": [
                "100% = la tasa se movió lo mismo que la del Banco; menos de 100% = traspaso parcial; más de 100% = se movió más (por ejemplo, por cambios en las primas de riesgo).",
                "Un traspaso bajo en el CDT con uno alto en el crédito amplía el margen de los bancos, y al revés.",
                "La ventana va desde el día antes de la primera decisión hasta tres meses después de la última; en el ciclo en curso se mide hasta el último dato, por lo que el traspaso puede estar incompleto.",
                "El traspaso no aísla la política monetaria: en la misma ventana influyen el riesgo de crédito, la liquidez y otros choques. Valores negativos aparecen con el color más claro."
            ],
            "formulas": [
                ["Traspaso", "P<sub>k</sub> = (R<sub>k,t1</sub> − R<sub>k,t0</sub>) ÷ (TPM<sub>t1</sub> − TPM<sub>t0</sub>) × 100", "R<sub>k</sub> = tasa k; t0 = día anterior a la primera decisión del ciclo; t1 = tres meses después de la última decisión (o último dato)"]
            ]
        },
        "en": {
            "que": "This chart measures the pass-through of each policy-rate cycle to nine market rates: what percentage of the cumulative change in the policy rate reached each one. It compares the latest cycles since 2008 and shows that transmission is uneven: fast and nearly complete in the interbank market, slower or partial in savings and some loan types.",
            "leer": "Heat map: each row is a cycle (dates of the first and last decision and, in brackets, the total change in the policy rate in pp); each column is a rate: overnight and 3-month IBR, 90-day CD, DTF (average 90-day deposit rate), total new lending, ordinary commercial, preferential (corporate), consumer and housing. The number in each cell is the pass-through in %; colour runs from light (0% or less) to blue (around 100%) and purple (150% or more). ‘—’ = the series did not exist at the start of the cycle; * = ongoing cycle.",
            "importa": "Pass-through shows how much of a Bank decision ends up in the cost of credit and the return on savings, and therefore how powerful monetary policy is. For an investor it helps gauge how much funding costs, bank margins and deposit rates move during a policy cycle.",
            "interpretar": [
                "100% = the rate moved as much as the policy rate; below 100% = partial pass-through; above 100% = it moved more (for instance because of changing risk premia).",
                "Low pass-through to CDs combined with high pass-through to lending widens bank spreads, and vice versa.",
                "The window runs from the day before the first decision to three months after the last; for the ongoing cycle it runs to the latest data, so pass-through may be incomplete.",
                "Pass-through does not isolate monetary policy: credit risk, liquidity and other shocks act in the same window. Negative values show in the lightest colour."
            ],
            "formulas": [
                ["Pass-through", "P<sub>k</sub> = (R<sub>k,t1</sub> − R<sub>k,t0</sub>) ÷ (TPM<sub>t1</sub> − TPM<sub>t0</sub>) × 100", "R<sub>k</sub> = rate k; t0 = day before the cycle's first decision; t1 = three months after the last decision (or latest data)"]
            ]
        },
    },
    "g-ts-modalidades": {
        "es": {
            "que": "Compara cuánto cuesta hoy el crédito nuevo en pesos según su modalidad: consumo, comercial ordinario, vivienda (no VIS y VIS, la vivienda de interés social), preferencial o corporativo, tesorería y el promedio total. Muestra cada tasa en términos nominales y reales, y frente a la tasa del Banco de la República.",
            "leer": "Eje vertical en tasa efectiva anual. Para cada modalidad hay dos barras: la de color sólido es la tasa nominal del último dato semanal (azul; el promedio total en naranja) y la ámbar clara es la tasa real, descontada la inflación anual del IPC más reciente. La línea horizontal punteada es la tasa del Banco vigente. Las tasas son promedios ponderados por monto desembolsado, informados por los bancos a la Superintendencia Financiera (formato 088).",
            "importa": "El costo del crédito determina la inversión de las empresas, la compra de vivienda y el consumo financiado de los hogares. La diferencia entre modalidades refleja el riesgo, el plazo, las garantías y el costo de originar cada tipo de préstamo. Para un inversionista indica las condiciones financieras que enfrentan los distintos sectores y la rentabilidad potencial de cada segmento de la banca.",
            "interpretar": [
                "La distancia entre cada barra nominal y la línea punteada es la prima que cobran los bancos sobre la tasa del Banco en esa modalidad.",
                "Una tasa real alta indica condiciones financieras restrictivas para ese segmento; una cercana a cero o negativa, condiciones holgadas.",
                "Tesorería y preferencial son préstamos a grandes empresas, de corto plazo y bajo riesgo, por eso quedan cerca de la tasa del Banco; consumo es el más caro.",
                "La tasa real usa la inflación pasada (ex post), no la esperada, y los datos semanales son volátiles: un solo dato puede verse afectado por desembolsos puntuales."
            ],
            "formulas": [
                ["Tasa real de cada modalidad", "r<sub>k</sub> = [(1 + i<sub>k</sub> ÷ 100) ÷ (1 + π ÷ 100) − 1] × 100", "i<sub>k</sub> = tasa nominal efectiva anual de la modalidad k (último dato semanal); π = inflación anual del IPC más reciente"]
            ]
        },
        "en": {
            "que": "This chart compares what new peso lending costs today by type: consumer, ordinary commercial, housing (non-social and VIS social housing), preferential or corporate, treasury and the overall average. It shows each rate in nominal and real terms, and against the Banco de la República policy rate.",
            "leer": "Vertical axis in effective annual rate. Each loan type has two bars: the solid one is the nominal rate from the latest weekly data (blue; the overall average in orange) and the light amber one is the real rate, net of the latest annual CPI inflation. The dotted horizontal line is the policy rate in force. Rates are averages weighted by amount disbursed, reported by banks to the Financial Superintendence (Form 088).",
            "importa": "The cost of credit drives business investment, home purchases and households' financed consumption. Differences across loan types reflect the risk, term, collateral and origination cost of each kind of loan. For an investor it shows the financial conditions faced by different sectors and the potential profitability of each banking segment.",
            "interpretar": [
                "The distance between each nominal bar and the dotted line is the premium banks charge over the policy rate for that loan type.",
                "A high real rate signals tight financial conditions for that segment; one near zero or negative, loose conditions.",
                "Treasury and preferential loans go to large firms, are short-term and low-risk, so they sit close to the policy rate; consumer credit is the most expensive.",
                "The real rate uses past (ex-post) inflation, not expected inflation, and weekly data are volatile: a single print can be affected by one-off disbursements."
            ],
            "formulas": [
                ["Real rate by type", "r<sub>k</sub> = [(1 + i<sub>k</sub> ÷ 100) ÷ (1 + π ÷ 100) − 1] × 100", "i<sub>k</sub> = effective annual nominal rate of type k (latest weekly data); π = latest annual CPI inflation"]
            ]
        },
    },
    "g-ts-margen": {
        "es": {
            "que": "Muestra dos diferencias de tasas que resumen el negocio de los bancos y la prima de riesgo de los hogares: el margen de intermediación (tasa del crédito nuevo total menos la de los CDT a 90 días, es decir, lo que cobran los bancos por prestar frente a lo que pagan por captar) y la prima del consumo (tasa del crédito de consumo menos la tasa del Banco de la República).",
            "leer": "Eje vertical en puntos porcentuales (pp), desde 2008, con promedios mensuales. Línea azul = crédito nuevo total − CDT a 90 días. Línea naranja = crédito de consumo − tasa del Banco. Cada línea se calcula restando los promedios mensuales de las tasas diarias o semanales correspondientes.",
            "importa": "El margen de intermediación refleja el costo, el riesgo y el grado de competencia del sistema bancario, y determina cuánto del ahorro llega como crédito a un costo razonable. La prima del consumo mide cuánto más pagan los hogares que la tasa de referencia, en función del riesgo percibido. Para un inversionista son indicadores de la rentabilidad bancaria y de la percepción de riesgo de crédito.",
            "interpretar": [
                "Un margen que se amplía puede reflejar mayor riesgo percibido, costos más altos o un traspaso más lento hacia el ahorro que hacia el crédito; uno que se estrecha, lo contrario.",
                "La prima del consumo suele subir cuando aumenta la morosidad de los hogares y bajar cuando la competencia por clientes se intensifica.",
                "Durante los ciclos de la tasa del Banco ambas líneas se mueven temporalmente porque las tasas no se ajustan al mismo ritmo (véase el gráfico de traspaso).",
                "El crédito nuevo total mezcla modalidades; un cambio en la composición de los desembolsos puede mover el margen sin que cambie ninguna tasa."
            ],
            "formulas": [
                ["Margen de intermediación", "M<sub>m</sub> = R̄<sup>crédito</sup><sub>m</sub> − R̄<sup>CDT90</sup><sub>m</sub>", "R̄ = promedio mensual de la tasa; en pp"],
                ["Prima del consumo", "P<sub>m</sub> = R̄<sup>consumo</sup><sub>m</sub> − R̄<sup>TPM</sup><sub>m</sub>", "TPM = tasa de política monetaria; en pp"]
            ]
        },
        "en": {
            "que": "This chart shows two rate spreads that sum up the banking business and households' risk premium: the intermediation spread (total new-lending rate minus the 90-day CD rate, i.e., what banks charge to lend versus what they pay to fund) and the consumer premium (consumer-credit rate minus the Banco de la República policy rate).",
            "leer": "Vertical axis in percentage points (pp), since 2008, as monthly averages. Blue line = total new lending − 90-day CD. Orange line = consumer credit − policy rate. Each line subtracts the monthly averages of the corresponding daily or weekly rates.",
            "importa": "The intermediation spread reflects the cost, risk and degree of competition in the banking system, and determines how much savings reach borrowers at a reasonable cost. The consumer premium measures how much more households pay than the reference rate, depending on perceived risk. For an investor they are indicators of bank profitability and of perceived credit risk.",
            "interpretar": [
                "A widening spread can reflect higher perceived risk, higher costs or slower pass-through to savings than to lending; a narrowing one, the opposite.",
                "The consumer premium tends to rise when household delinquencies increase and to fall when competition for clients intensifies.",
                "During policy-rate cycles both lines move temporarily because rates do not adjust at the same pace (see the pass-through chart).",
                "Total new lending mixes loan types; a shift in the composition of disbursements can move the spread without any rate changing."
            ],
            "formulas": [
                ["Intermediation spread", "M<sub>m</sub> = R̄<sup>lending</sup><sub>m</sub> − R̄<sup>CD90</sup><sub>m</sub>", "R̄ = monthly average rate; in pp"],
                ["Consumer premium", "P<sub>m</sub> = R̄<sup>consumer</sup><sub>m</sub> − R̄<sup>TPM</sup><sub>m</sub>", "TPM = monetary policy rate; in pp"]
            ]
        },
    },
    "g-ts-ibr": {
        "es": {
            "que": "Muestra la curva del IBR (Indicador Bancario de Referencia): las tasas a las que los bancos están dispuestos a prestarse pesos a un día, 1, 3, 6 y 12 meses. Compara la curva de hoy con la de hace 3 meses y la de hace un año, junto a la tasa del Banco de la República en cada fecha. Su forma resume cómo valora el mercado el costo del dinero en los próximos meses.",
            "leer": "Eje horizontal: plazo (un día, 1 mes, 3 meses, 6 meses, 12 meses). Eje vertical: IBR en tasa efectiva anual. Línea azul = hoy; morada = hace 3 meses; ámbar = hace un año (la fecha exacta aparece en la leyenda; se usa el último dato disponible en o antes de cada fecha). La raya horizontal discontinua del mismo color es la tasa del Banco vigente en esa fecha.",
            "importa": "El IBR es la referencia de muchos créditos a tasa variable, de los swaps de tasa de interés y de la valoración de deuda de corto plazo. La pendiente de la curva incorpora la trayectoria de la tasa del Banco que el mercado descuenta, por lo que es un termómetro diario de las condiciones del mercado monetario. Para un inversionista sirve para valorar instrumentos en pesos y medir el costo de cubrir riesgo de tasa.",
            "interpretar": [
                "Si los plazos largos están por encima del de un día, el mercado cobra más por prestar a más tiempo, lo que es coherente con subidas de la tasa del Banco incorporadas en los precios; si están por debajo, con bajadas incorporadas.",
                "El IBR a un día debe quedar pegado a la raya de la tasa del Banco; una distancia grande indicaría problemas de liquidez (véase el gráfico de tasas a un día).",
                "Un desplazamiento de toda la curva entre fechas refleja decisiones ya tomadas; un cambio de pendiente, un cambio en lo que el mercado descuenta.",
                "Las tasas a plazo también contienen primas por plazo y liquidez: no son una medida pura de expectativas."
            ],
            "formulas": [
                ["Diferencia frente a la tasa del Banco", "S<sub>h</sub> = IBR<sub>h</sub> − TPM", "h = plazo; distancia vertical entre cada punto y la raya del mismo color"]
            ]
        },
        "en": {
            "que": "This chart shows the IBR curve (Bank Reference Indicator): the rates at which banks are willing to lend pesos to each other overnight and at 1, 3, 6 and 12 months. It compares today's curve with those of 3 months and a year ago, alongside the Banco de la República policy rate on each date. Its shape sums up how the market values the cost of money over the coming months.",
            "leer": "Horizontal axis: tenor (overnight, 1 month, 3 months, 6 months, 12 months). Vertical axis: IBR as an effective annual rate. Blue line = today; purple = 3 months ago; amber = a year ago (the exact date appears in the legend; the last value on or before each date is used). The dashed horizontal line in the same colour is the policy rate in force on that date.",
            "importa": "The IBR is the benchmark for many floating-rate loans, interest-rate swaps and short-term debt valuation. The slope of the curve embeds the policy-rate path the market prices, making it a daily gauge of money-market conditions. For an investor it is used to value peso instruments and to measure the cost of hedging interest-rate risk.",
            "interpretar": [
                "If longer tenors sit above overnight, the market charges more to lend for longer, consistent with policy hikes being priced in; if below, with cuts priced in.",
                "Overnight IBR should hug the policy-rate dash; a large gap would signal liquidity strains (see the overnight rates chart).",
                "A parallel shift of the whole curve between dates reflects decisions already taken; a change in slope, a change in what the market prices.",
                "Term rates also contain term and liquidity premia: they are not a pure measure of expectations."
            ],
            "formulas": [
                ["Spread over the policy rate", "S<sub>h</sub> = IBR<sub>h</sub> − TPM", "h = tenor; vertical distance between each point and the same-coloured dash"]
            ]
        },
    },
    "g-ts-overnight": {
        "es": {
            "que": "Mide qué tan bien controla el Banco de la República el costo del dinero a un día. Compara dos tasas de muy corto plazo con la tasa de política: el IBR a un día y la TIB (tasa interbancaria, préstamos entre bancos sin garantía a un día). Si ambas se mantienen cerca de la tasa del Banco, la decisión de la Junta se cumple efectivamente en el mercado.",
            "leer": "Eje vertical en puntos básicos (pb; 100 pb = 1 pp) por encima o por debajo de la tasa del Banco, desde 2008. Línea azul = IBR a un día − tasa del Banco; línea naranja = TIB − tasa del Banco. Cada punto es el promedio semanal de las diferencias diarias. La línea horizontal oscura marca el cero (tasa igual a la del Banco).",
            "importa": "El primer eslabón de la transmisión monetaria es el mercado interbancario a un día: si allí la tasa se aparta de la de política, la señal del Banco se diluye antes de llegar al resto de tasas. Para un inversionista, desviaciones grandes o persistentes son señales de tensiones de liquidez en el sistema financiero.",
            "interpretar": [
                "Valores cercanos a cero indican un control efectivo; desvíos de unos pocos puntos básicos son normales.",
                "Picos positivos suelen coincidir con estrechez de liquidez (pagos de impuestos, cierres de mes o de año); valores negativos, con exceso de pesos en el sistema.",
                "La TIB es más volátil que el IBR porque refleja operaciones efectivas entre pocos participantes, mientras el IBR se construye con cotizaciones de varios bancos.",
                "Compárelo con el gráfico de liquidez: las subastas de expansión y la ventanilla de contracción son los instrumentos con que el Banco cierra estas brechas."
            ],
            "formulas": [
                ["Diferencia diaria", "s<sub>d</sub> = (R<sub>d</sub> − TPM<sub>d</sub>) × 100", "R = IBR a un día o TIB del día d (en %); resultado en puntos básicos"],
                ["Promedio semanal", "S<sub>w</sub> = (1 ÷ n<sub>w</sub>) × Σ<sub>d∈w</sub> s<sub>d</sub>", "n<sub>w</sub> = número de días con dato en la semana w"]
            ]
        },
        "en": {
            "que": "This chart measures how well the Banco de la República steers the overnight cost of money. It compares two very short-term rates with the policy rate: the overnight IBR and the TIB (interbank rate, unsecured overnight loans between banks). If both stay close to the policy rate, the Board's decision effectively holds in the market.",
            "leer": "Vertical axis in basis points (bp; 100 bp = 1 pp) above or below the policy rate, since 2008. Blue line = overnight IBR − policy rate; orange line = TIB − policy rate. Each point is the weekly average of daily differences. The dark horizontal line marks zero (rate equal to the policy rate).",
            "importa": "The first link in monetary transmission is the overnight interbank market: if the rate there drifts from the policy rate, the Bank's signal is diluted before reaching other rates. For an investor, large or persistent deviations signal liquidity strains in the financial system.",
            "interpretar": [
                "Values near zero indicate effective control; deviations of a few basis points are normal.",
                "Positive spikes tend to coincide with tight liquidity (tax payments, month-end or year-end); negative values, with excess pesos in the system.",
                "The TIB is more volatile than the IBR because it reflects actual trades among a few participants, while the IBR is built from quotes by several banks.",
                "Compare with the liquidity chart: expansion auctions and the contraction window are the tools the Bank uses to close these gaps."
            ],
            "formulas": [
                ["Daily spread", "s<sub>d</sub> = (R<sub>d</sub> − TPM<sub>d</sub>) × 100", "R = overnight IBR or TIB on day d (in %); result in basis points"],
                ["Weekly average", "S<sub>w</sub> = (1 ÷ n<sub>w</sub>) × Σ<sub>d∈w</sub> s<sub>d</sub>", "n<sub>w</sub> = number of days with data in week w"]
            ]
        },
    },
    "g-ts-cartera": {
        "es": {
            "que": "Muestra a qué ritmo crece el saldo de crédito en pesos (la cartera de los establecimientos de crédito) una vez descontada la inflación, en total y por modalidad: comercial (empresas), consumo (hogares), vivienda y microcrédito. Indica si el sistema financiero está expandiendo o contrayendo en términos reales el financiamiento a la economía.",
            "leer": "Eje vertical: variación anual real, en %, desde 2008; la línea horizontal oscura marca el cero. Línea azul gruesa = cartera total; morada = comercial; naranja = consumo; verde = vivienda; ámbar = microcrédito. Cada punto compara el saldo de fin de mes con el del mismo mes un año antes y descuenta la inflación anual del IPC de ese mes. La cartera total es la cartera bruta sin ajuste por titularización y la de vivienda es la hipotecaria ajustada por titularizaciones.",
            "importa": "El crédito financia la inversión de las empresas y el consumo de los hogares, por lo que su crecimiento real acompaña al ciclo económico y es un canal clave de la política monetaria. Para un inversionista indica la fase del ciclo crediticio, el dinamismo de la demanda interna y las perspectivas de ingreso de los bancos.",
            "interpretar": [
                "Por encima de cero, el crédito crece más que los precios (expansión real); por debajo, se contrae en términos reales.",
                "El crédito suele reaccionar con rezago a la tasa del Banco: tasas reales altas tienden a moderar su crecimiento después de varios trimestres.",
                "El consumo suele ser la modalidad más cíclica; la vivienda, la más estable por sus plazos largos.",
                "Desde 2015 la contabilidad bancaria usa NIIF, un cambio metodológico; además, las titularizaciones y castigos de cartera pueden alterar el saldo sin que cambien los desembolsos."
            ],
            "formulas": [
                ["Crecimiento nominal anual", "g<sub>t</sub> = C<sub>t</sub> ÷ C<sub>t−12</sub> − 1", "C = saldo de cartera en pesos a fin del mes t"],
                ["Crecimiento real anual", "g<sup>r</sup><sub>t</sub> = [(1 + g<sub>t</sub>) ÷ (1 + π<sub>t</sub> ÷ 100) − 1] × 100", "π = inflación anual del IPC del mes t (%)"]
            ]
        },
        "en": {
            "que": "This chart shows how fast the outstanding peso loan book of credit institutions grows once inflation is netted out, overall and by type: commercial (firms), consumer (households), housing and microcredit. It shows whether the financial system is expanding or contracting real financing to the economy.",
            "leer": "Vertical axis: real annual change, in %, since 2008; the dark horizontal line marks zero. Thick blue line = total loan book; purple = commercial; orange = consumer; green = housing; amber = microcredit. Each point compares the end-of-month balance with the same month a year earlier and deflates it by that month's annual CPI inflation. The total is the gross loan book without securitisation adjustment, and housing is the mortgage book adjusted for securitisations.",
            "importa": "Credit finances business investment and household consumption, so its real growth tracks the business cycle and is a key channel of monetary policy. For an investor it signals the phase of the credit cycle, the strength of domestic demand and banks' income outlook.",
            "interpretar": [
                "Above zero, credit grows faster than prices (real expansion); below zero, it shrinks in real terms.",
                "Credit usually reacts to the policy rate with a lag: high real rates tend to slow its growth after several quarters.",
                "Consumer credit is usually the most cyclical type; housing the most stable given its long terms.",
                "Since 2015 bank accounting uses IFRS, a methodological change; securitisations and write-offs can also alter balances without any change in disbursements."
            ],
            "formulas": [
                ["Annual nominal growth", "g<sub>t</sub> = C<sub>t</sub> ÷ C<sub>t−12</sub> − 1", "C = outstanding peso loans at the end of month t"],
                ["Annual real growth", "g<sup>r</sup><sub>t</sub> = [(1 + g<sub>t</sub>) ÷ (1 + π<sub>t</sub> ÷ 100) − 1] × 100", "π = annual CPI inflation in month t (%)"]
            ]
        },
    },
    "g-ts-composicion": {
        "es": {
            "que": "Muestra cómo se reparte el saldo de crédito en pesos entre las cuatro modalidades: comercial (empresas), consumo (hogares, para gastos distintos de vivienda), vivienda y microcrédito (pequeños negocios). Revela hacia dónde se dirige el financiamiento bancario y cómo ha cambiado el peso relativo de empresas y hogares en el balance de los bancos.",
            "leer": "Áreas apiladas que suman 100% (eje de 0% a 100%), desde 2008, con datos mensuales. De abajo hacia arriba: morado = comercial; naranja = consumo; verde = vivienda (cartera hipotecaria ajustada por titularizaciones); ámbar = microcrédito. El denominador es la suma de las cuatro modalidades en moneda legal, no la cartera bruta total.",
            "importa": "La composición del crédito influye en la sensibilidad del sistema financiero al ciclo y en el canal por el que actúa la política monetaria. Más peso del consumo hace la cartera más rentable pero también más expuesta al deterioro del empleo y del ingreso de los hogares; más peso comercial la liga a la inversión y al desempeño de las empresas. Para un inversionista es un indicador del perfil de riesgo de la banca.",
            "interpretar": [
                "Una franja de consumo que se ensancha indica que el crédito a los hogares crece más rápido que el resto.",
                "Los cambios de composición son lentos; movimientos de un punto en un año ya son relevantes.",
                "Una participación puede caer porque esa cartera crece menos que las demás, no necesariamente porque se contraiga; compárelo con el crecimiento real por modalidad.",
                "Titularizaciones, castigos y reclasificaciones entre modalidades pueden alterar la composición sin cambios en la actividad."
            ],
            "formulas": [
                ["Participación de cada modalidad", "S<sub>k,t</sub> = C<sub>k,t</sub> ÷ (C<sub>com,t</sub> + C<sub>cons,t</sub> + C<sub>viv,t</sub> + C<sub>mic,t</sub>) × 100", "C = saldo en pesos de cada modalidad a fin del mes t"]
            ]
        },
        "en": {
            "que": "This chart shows how the outstanding peso loan book is split across the four types: commercial (firms), consumer (households, for spending other than housing), housing and microcredit (small businesses). It reveals where bank financing goes and how the relative weight of firms and households on bank balance sheets has changed.",
            "leer": "Stacked areas adding up to 100% (axis from 0% to 100%), since 2008, with monthly data. From bottom to top: purple = commercial; orange = consumer; green = housing (mortgage book adjusted for securitisations); amber = microcredit. The denominator is the sum of the four types in local currency, not the total gross loan book.",
            "importa": "The composition of credit shapes how sensitive the financial system is to the cycle and the channel through which monetary policy acts. A larger consumer share makes the book more profitable but also more exposed to weaker household jobs and incomes; a larger commercial share ties it to investment and corporate performance. For an investor it is an indicator of the banking sector's risk profile.",
            "interpretar": [
                "A widening consumer band means household credit is growing faster than the rest.",
                "Composition changes slowly; a one-point move in a year is already meaningful.",
                "A share can fall because that book grows more slowly than others, not necessarily because it shrinks; compare with real growth by type.",
                "Securitisations, write-offs and reclassifications between types can alter the composition without changes in activity."
            ],
            "formulas": [
                ["Share of each type", "S<sub>k,t</sub> = C<sub>k,t</sub> ÷ (C<sub>com,t</sub> + C<sub>cons,t</sub> + C<sub>hous,t</sub> + C<sub>mic,t</sub>) × 100", "C = outstanding peso balance of each type at the end of month t"]
            ]
        },
    },
    "g-ts-liquidez": {
        "es": {
            "que": "Muestra cómo el Banco de la República ajusta la cantidad de pesos en el sistema financiero para que la tasa a un día se mantenga cerca de la tasa de política. Arriba, los repos de expansión: préstamos de corto plazo del Banco a las entidades financieras con garantía de títulos. Abajo, la ventanilla de contracción: depósitos remunerados que las entidades hacen en el Banco con sus excedentes de liquidez.",
            "leer": "Barras mensuales en billones de pesos, desde 2012. Hacia arriba (valores positivos): azul = repos de expansión a un día; morado = repos a plazos mayores de un día. Hacia abajo (valores negativos): ámbar = saldo en la ventanilla de contracción. Cada barra es el promedio del mes de los saldos diarios (los días sin operación cuentan como cero). La línea horizontal marca el cero.",
            "importa": "Es la cara operativa de la política monetaria: la Junta fija la tasa y el Banco provee o retira liquidez para que se cumpla en el mercado. Un uso alto de los repos indica que los bancos necesitan pesos (por ejemplo, por pagos de impuestos, menor ahorro o crecimiento del crédito); depósitos de contracción altos, que les sobran. Para un inversionista es una señal de las condiciones de liquidez del mercado de dinero y de los TES de corto plazo.",
            "interpretar": [
                "Barras azules y moradas crecientes indican una mayor necesidad de liquidez del sistema; barras ámbar más profundas, excedentes que el Banco absorbe.",
                "Los saldos tienen estacionalidad: suben en fechas de pago de impuestos y en fin de año; compare con los mismos meses de años anteriores.",
                "Las compras o ventas de TES y de divisas por parte del Banco también cambian la liquidez y no aparecen en este gráfico.",
                "Léalo con el gráfico de tasas a un día: si la liquidez se ajusta bien, el IBR y la TIB permanecen cerca de la tasa del Banco."
            ],
            "formulas": [
                ["Promedio mensual de saldos", "L̄<sub>k,m</sub> = (1 ÷ n<sub>m</sub>) × Σ<sub>d∈m</sub> L<sub>k,d</sub> ÷ 1.000", "L = saldo diario del instrumento k (miles de millones de pesos; 0 si no hubo operación); n<sub>m</sub> = días del mes con registro; resultado en billones"],
                ["Posición neta (lectura)", "N<sub>m</sub> = L̄<sub>repo 1 día,m</sub> + L̄<sub>repo plazo,m</sub> − L̄<sub>contracción,m</sub>", "positivo = el Banco presta en neto al sistema"]
            ]
        },
        "en": {
            "que": "This chart shows how the Banco de la República adjusts the amount of pesos in the financial system so the overnight rate stays close to the policy rate. Above, expansion repos: short-term loans from the Bank to financial institutions against securities. Below, the contraction window: interest-bearing deposits institutions place at the Bank with their surplus liquidity.",
            "leer": "Monthly bars in COP trillion, since 2012. Upward (positive values): blue = overnight expansion repos; purple = repos for terms longer than one day. Downward (negative values): amber = balance in the contraction window. Each bar is the monthly average of daily balances (days without operations count as zero). The horizontal line marks zero.",
            "importa": "This is the operational side of monetary policy: the Board sets the rate and the Bank supplies or withdraws liquidity so it holds in the market. Heavy repo use means banks need pesos (for instance due to tax payments, weaker deposits or credit growth); large contraction deposits mean they have surplus funds. For an investor it signals liquidity conditions in the money market and in short-term TES.",
            "interpretar": [
                "Growing blue and purple bars signal a greater liquidity need in the system; deeper amber bars, surpluses the Bank absorbs.",
                "Balances are seasonal: they rise around tax-payment dates and at year-end; compare with the same months in earlier years.",
                "The Bank's purchases or sales of TES and foreign currency also change liquidity and are not shown here.",
                "Read it with the overnight rates chart: if liquidity is well managed, the IBR and TIB stay close to the policy rate."
            ],
            "formulas": [
                ["Monthly average balance", "L̄<sub>k,m</sub> = (1 ÷ n<sub>m</sub>) × Σ<sub>d∈m</sub> L<sub>k,d</sub> ÷ 1,000", "L = daily balance of instrument k (COP billion; 0 if no operation); n<sub>m</sub> = recorded days in the month; result in COP trillion"],
                ["Net position (reading aid)", "N<sub>m</sub> = L̄<sub>overnight repo,m</sub> + L̄<sub>term repo,m</sub> − L̄<sub>contraction,m</sub>", "positive = the Bank is a net lender to the system"]
            ]
        },
    },
}
