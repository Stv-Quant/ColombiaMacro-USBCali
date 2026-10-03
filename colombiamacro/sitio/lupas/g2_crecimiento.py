"""Lupas (explicaciones ampliadas) de los gráficos de la página de crecimiento: PIB, velocidades, precios,
aportes por sector y por demanda, inversión, consumo de los hogares, PIB por persona, productividad y nivel."""

LUPAS = {
    # ------------------------------------------------------------------ PIB trimestral e ISE
    "g-crec": {
        "es": {
            "que": "Muestra a qué ritmo crece la producción de bienes y servicios de Colombia frente al mismo trimestre del año anterior y lo compara con el ritmo habitual de la economía. Junto al PIB trimestral aparece el Indicador de Seguimiento a la Economía (ISE), un índice mensual del DANE que resume la actividad de todos los sectores y llega antes que el PIB. En conjunto cuentan la historia del ciclo: periodos en que la economía corre por encima de su ritmo normal y periodos en que se queda por debajo, como el desplome de 2020 y el rebote que le siguió.",
            "leer": "Panel superior, eje en %: las barras azules son la variación anual del PIB real de cada trimestre (datos originales, sin desestacionalizar); la línea naranja es la variación anual del ISE desestacionalizado, mes a mes; la línea gris punteada es el «ritmo habitual», el crecimiento anual de la tendencia estimada con el filtro de Hodrick-Prescott (HP). La línea horizontal en cero separa crecimiento de contracción. El panel inferior muestra, en puntos porcentuales (pp), cuánto cambió la tasa anual del PIB frente al trimestre anterior: azul si subió, naranja si bajó. La vista inicial cubre los últimos diez años; el resto de la historia se ve ampliando el eje.",
            "importa": "El crecimiento del PIB resume en una cifra la evolución de los ingresos, el empleo y las ventas de las empresas. Compararlo con el ritmo habitual indica si la economía genera presiones de demanda sobre su capacidad o si tiene holgura, una distinción central para leer la inflación y las decisiones de tasas del Banco de la República. Para un inversionista es el punto de partida para evaluar utilidades corporativas, recaudo tributario y calidad del crédito.",
            "interpretar": [
                "Barras por encima de la línea punteada: la economía crece más rápido que su tendencia; por debajo, más despacio. Barras negativas indican que se produce menos que un año antes.",
                "El panel inferior muestra la dirección: varias barras azules seguidas indican aceleración y varias naranjas, desaceleración, aunque el crecimiento siga siendo positivo.",
                "El ISE cubre meses que el PIB trimestral aún no recoge: si la línea naranja se separa de la última barra, la actividad reciente se movió en esa dirección. La brecha frente al ritmo habitual se estudia en la página de capacidad.",
                "Los datos originales incluyen efectos de calendario (Semana Santa, días hábiles) y efectos base: tras una caída fuerte, la tasa anual sube mucho aunque el nivel apenas se recupere, como en 2021.",
                "La tendencia HP se reestima con cada dato nuevo y su tramo final es el menos preciso; los trimestres 2020T2–2021T2 se reemplazan por interpolación al estimarla. El DANE revisa el PIB en cada publicación.",
            ],
            "formulas": [
                ["Variación anual del PIB", "g<sub>t</sub> = (Y<sub>t</sub> ÷ Y<sub>t−4</sub> − 1) × 100", "Y<sub>t</sub> = PIB real del trimestre t (volúmenes encadenados, base 2015, datos originales)"],
                ["Variación anual del ISE", "i<sub>m</sub> = (ISE<sub>m</sub> ÷ ISE<sub>m−12</sub> − 1) × 100", "ISE<sub>m</sub> = índice desestacionalizado del mes m"],
                ["Ritmo habitual (filtro HP)", "τ = argmin Σ(y<sub>t</sub> − τ<sub>t</sub>)<sup>2</sup> + λ Σ(Δ<sup>2</sup>τ<sub>t</sub>)<sup>2</sup><br>g*<sub>t</sub> = (e<sup>(τ<sub>t</sub> − τ<sub>t−4</sub>) ÷ 100</sup> − 1) × 100", "y<sub>t</sub> = 100 × ln(PIB real desestacionalizado); τ<sub>t</sub> = tendencia; λ = 1.600; Δ<sup>2</sup> = segunda diferencia"],
                ["Cambio del panel inferior", "Δg<sub>t</sub> = g<sub>t</sub> − g<sub>t−1</sub>", "en pp; g<sub>t</sub> = variación anual del PIB del trimestre t"],
            ],
        },
        "en": {
            "que": "Shows how fast Colombia's output of goods and services is growing versus the same quarter a year earlier, and compares it with the economy's usual pace. Alongside quarterly GDP sits the Economic Tracking Indicator (ISE), a monthly DANE index that summarises activity across all sectors and arrives before GDP. Together they tell the story of the cycle: stretches when the economy runs above its normal pace and stretches when it falls short, such as the 2020 collapse and the rebound that followed.",
            "leer": "Upper panel, axis in %: blue bars are the annual change in real GDP for each quarter (unadjusted data); the orange line is the annual change in the seasonally adjusted ISE, month by month; the grey dotted line is the \"usual pace\", the annual growth of the trend estimated with the Hodrick-Prescott (HP) filter. The horizontal line at zero separates growth from contraction. The lower panel shows, in percentage points (pp), how much GDP's annual rate changed versus the previous quarter: blue if it rose, orange if it fell. The initial view covers the last ten years; widen the axis to see the full history.",
            "importa": "GDP growth condenses into one number the path of incomes, jobs and company sales. Comparing it with the usual pace tells whether the economy is pressing on its capacity or has slack, a distinction at the heart of reading inflation and the interest-rate decisions of Banco de la República. For an investor it is the starting point for assessing corporate earnings, tax revenue and credit quality.",
            "interpretar": [
                "Bars above the dotted line: the economy is growing faster than its trend; below it, more slowly. Negative bars mean output is lower than a year earlier.",
                "The lower panel shows direction: a run of blue bars signals acceleration and a run of orange ones deceleration, even while growth stays positive.",
                "The ISE covers months that quarterly GDP has not yet captured: if the orange line drifts away from the last bar, recent activity moved that way. The gap versus the usual pace is studied on the capacity page.",
                "Unadjusted data carry calendar effects (Easter, working days) and base effects: after a sharp fall the annual rate jumps even if the level barely recovers, as in 2021.",
                "The HP trend is re-estimated with every new data point and its final stretch is the least precise; quarters 2020Q2–2021Q2 are replaced by interpolation when estimating it. DANE revises GDP with every release.",
            ],
            "formulas": [
                ["Annual GDP growth", "g<sub>t</sub> = (Y<sub>t</sub> ÷ Y<sub>t−4</sub> − 1) × 100", "Y<sub>t</sub> = real GDP in quarter t (chain-linked volumes, 2015 base, unadjusted)"],
                ["Annual ISE growth", "i<sub>m</sub> = (ISE<sub>m</sub> ÷ ISE<sub>m−12</sub> − 1) × 100", "ISE<sub>m</sub> = seasonally adjusted index for month m"],
                ["Usual pace (HP filter)", "τ = argmin Σ(y<sub>t</sub> − τ<sub>t</sub>)<sup>2</sup> + λ Σ(Δ<sup>2</sup>τ<sub>t</sub>)<sup>2</sup><br>g*<sub>t</sub> = (e<sup>(τ<sub>t</sub> − τ<sub>t−4</sub>) ÷ 100</sup> − 1) × 100", "y<sub>t</sub> = 100 × ln(seasonally adjusted real GDP); τ<sub>t</sub> = trend; λ = 1,600; Δ<sup>2</sup> = second difference"],
                ["Lower-panel change", "Δg<sub>t</sub> = g<sub>t</sub> − g<sub>t−1</sub>", "in pp; g<sub>t</sub> = annual GDP growth in quarter t"],
            ],
        },
    },
    # ------------------------------------------------------------------ crecimiento por año
    "g-pib-anual": {
        "es": {
            "que": "Resume el crecimiento real de la economía año por año: cuánto más (o menos) produjo el país frente al año anterior, descontando el efecto de los precios. Al agregar los cuatro trimestres se eliminan la estacionalidad y buena parte del ruido trimestral, lo que deja ver los grandes episodios: el auge de comienzos de la década de 2010, la desaceleración tras la caída del petróleo, la contracción de 2020 y el rebote posterior. El año todavía incompleto se muestra con los últimos 12 meses disponibles.",
            "leer": "Eje vertical: crecimiento real en %. Cada barra es un año calendario completo; azul si la producción creció y naranja si cayó, con el valor escrito encima. La barra clara con borde azul aparece cuando el año en curso no ha terminado: es el crecimiento de los últimos 12 meses frente a los 12 previos, hasta el último trimestre publicado. La línea verde punteada es el ritmo habitual (promedio anual del crecimiento de la tendencia HP) y la línea gris discontinua, el promedio simple de 2010–2019. La vista inicial cubre unos diez años.",
            "importa": "La cifra anual es la que se usa para comparar a Colombia con otros países, para los presupuestos públicos y para las metas fiscales, porque no depende de la estacionalidad ni de un trimestre atípico. Ponerla frente al ritmo habitual y al promedio de la década previa a la pandemia permite juzgar si un año fue excepcional o si la economía se mueve dentro de su rango histórico.",
            "interpretar": [
                "Una barra por encima de la línea verde indica un año de crecimiento superior a la tendencia; por debajo, inferior. La línea gris es una referencia fija para comparar con la década anterior a la pandemia.",
                "La barra clara no es el dato del año: mezcla trimestres del año anterior y del actual, y cambia con cada publicación trimestral hasta que se completa el cuarto trimestre.",
                "Tras años de contracción, el siguiente suele mostrar crecimiento alto por efecto base: la comparación parte de un nivel deprimido, como ocurrió en 2021.",
                "El ritmo habitual se reestima cuando llegan datos nuevos y el DANE revisa los trimestres previos, de modo que barras y línea pueden moverse levemente entre publicaciones.",
            ],
            "formulas": [
                ["Crecimiento real anual", "g<sub>A</sub> = (Σ<sub>q∈A</sub> Y<sub>q</sub> ÷ Σ<sub>q∈A−1</sub> Y<sub>q</sub> − 1) × 100", "Y<sub>q</sub> = PIB real del trimestre q (datos originales); A = año calendario"],
                ["Últimos 12 meses", "g<sub>12m</sub> = (Σ<sub>k=0..3</sub> Y<sub>t−k</sub> ÷ Σ<sub>k=4..7</sub> Y<sub>t−k</sub> − 1) × 100", "t = último trimestre publicado"],
                ["Ritmo habitual anual", "ḡ*<sub>A</sub> = (1 ÷ 4) × Σ<sub>q∈A</sub> g*<sub>q</sub>", "g*<sub>q</sub> = crecimiento anual de la tendencia HP en el trimestre q"],
                ["Referencia 2010–2019", "ḡ = (1 ÷ 10) × Σ<sub>A=2010..2019</sub> g<sub>A</sub>", "promedio simple de las tasas anuales"],
            ],
        },
        "en": {
            "que": "Summarises the economy's real growth year by year: how much more (or less) the country produced than the year before, net of price effects. Adding up the four quarters removes seasonality and much of the quarterly noise, which brings out the big episodes: the boom of the early 2010s, the slowdown after the oil-price fall, the 2020 contraction and the rebound that followed. The year still in progress is shown with the latest available 12 months.",
            "leer": "Vertical axis: real growth in %. Each bar is a full calendar year; blue if output grew and orange if it fell, with the value written on top. The pale bar with a blue outline appears when the current year is not over: it is growth over the last 12 months versus the previous 12, up to the latest published quarter. The green dotted line is the usual pace (annual average of HP-trend growth) and the grey dashed line the simple 2010–2019 average. The initial view spans about ten years.",
            "importa": "The annual figure is the one used to compare Colombia with other countries, for public budgets and for fiscal targets, because it does not depend on seasonality or on one unusual quarter. Setting it against the usual pace and the pre-pandemic decade average shows whether a year was exceptional or within the historical range.",
            "interpretar": [
                "A bar above the green line marks a year of above-trend growth; below it, below-trend. The grey line is a fixed benchmark against the decade before the pandemic.",
                "The pale bar is not the year's figure: it mixes quarters from the previous and current years and changes with every quarterly release until the fourth quarter is in.",
                "After a contraction year the next one usually shows high growth from a base effect, since the comparison starts from a depressed level, as happened in 2021.",
                "The usual pace is re-estimated as new data arrive and DANE revises earlier quarters, so bars and line may shift slightly between releases.",
            ],
            "formulas": [
                ["Annual real growth", "g<sub>A</sub> = (Σ<sub>q∈A</sub> Y<sub>q</sub> ÷ Σ<sub>q∈A−1</sub> Y<sub>q</sub> − 1) × 100", "Y<sub>q</sub> = real GDP in quarter q (unadjusted); A = calendar year"],
                ["Last 12 months", "g<sub>12m</sub> = (Σ<sub>k=0..3</sub> Y<sub>t−k</sub> ÷ Σ<sub>k=4..7</sub> Y<sub>t−k</sub> − 1) × 100", "t = latest published quarter"],
                ["Annual usual pace", "ḡ*<sub>A</sub> = (1 ÷ 4) × Σ<sub>q∈A</sub> g*<sub>q</sub>", "g*<sub>q</sub> = annual growth of the HP trend in quarter q"],
                ["2010–2019 benchmark", "ḡ = (1 ÷ 10) × Σ<sub>A=2010..2019</sub> g<sub>A</sub>", "simple average of annual rates"],
            ],
        },
    },
    # ------------------------------------------------------------------ tres velocidades
    "g-velocidades": {
        "es": {
            "que": "Presenta tres maneras de medir el mismo crecimiento del PIB real, cada una con un horizonte distinto. La variación anual compara con el mismo trimestre del año anterior; la de 12 meses compara el último año completo con el anterior y es la más suave; el trimestre anualizado mide el impulso más reciente, como si el ritmo del último trimestre se mantuviera un año entero. Leídas juntas indican si la economía está acelerando o frenando antes de que lo refleje la cifra anual.",
            "leer": "Eje en %, desde 2012. Línea azul: variación anual del PIB real (datos originales). Línea verde: suma de los últimos cuatro trimestres frente a los cuatro anteriores. Barras azul claro: variación del PIB desestacionalizado frente al trimestre anterior, elevada a ritmo anual. La línea horizontal en cero separa crecimiento de contracción. Para que la escala siga siendo legible, todos los valores se recortan entre −12% y 16%, lo que afecta sobre todo a 2020 y 2021.",
            "importa": "Las tasas anuales reaccionan con retraso: pueden seguir altas cuando la economía ya se frenó, o bajas cuando ya se está recuperando. El trimestre anualizado, convención de la Oficina de Análisis Económico de EE. UU. (BEA), es el que primero muestra los puntos de giro, y la medida de 12 meses es la que se compara con las cifras anuales oficiales. Comparar las tres evita conclusiones apresuradas a partir de un solo dato.",
            "interpretar": [
                "Barras por encima de la línea azul: el ritmo reciente supera al anual, la economía está acelerando; por debajo, está frenando.",
                "La línea verde cambia despacio: si gira, el cambio de tendencia ya acumula varios trimestres.",
                "El trimestre anualizado multiplica por cuatro aproximadamente el ruido trimestral y depende del ajuste estacional, que se reestima con cada publicación; un solo trimestre alto o bajo no define una tendencia.",
                "Los valores fuera del rango −12% a 16% aparecen topados en el borde: en 2020–2021 los datos reales fueron más extremos que lo que muestra el dibujo.",
            ],
            "formulas": [
                ["Variación anual", "g<sub>t</sub> = (Y<sub>t</sub> ÷ Y<sub>t−4</sub> − 1) × 100", "Y = PIB real, datos originales"],
                ["12 meses", "g<sub>12m,t</sub> = (Σ<sub>k=0..3</sub> Y<sub>t−k</sub> ÷ Σ<sub>k=4..7</sub> Y<sub>t−k</sub> − 1) × 100", "sumas móviles de cuatro trimestres"],
                ["Trimestre anualizado", "a<sub>t</sub> = ((S<sub>t</sub> ÷ S<sub>t−1</sub>)<sup>4</sup> − 1) × 100", "S = PIB real desestacionalizado"],
                ["Recorte gráfico", "valor dibujado = min(16; max(−12; x))", "x = cualquiera de las tres medidas"],
            ],
        },
        "en": {
            "que": "Presents three ways of measuring the same real GDP growth, each over a different horizon. Annual growth compares with the same quarter a year earlier; 12-month growth compares the last full year with the previous one and is the smoothest; the annualised quarter measures the most recent momentum, as if the latest quarter's pace held for a whole year. Read together, they show whether the economy is speeding up or slowing down before the annual figure reflects it.",
            "leer": "Axis in %, from 2012. Blue line: annual change in real GDP (unadjusted). Green line: sum of the last four quarters versus the previous four. Light-blue bars: change in seasonally adjusted GDP versus the previous quarter, compounded to an annual rate. The horizontal line at zero separates growth from contraction. To keep the scale readable, all values are capped between −12% and 16%, which mainly affects 2020 and 2021.",
            "importa": "Annual rates react with a lag: they can stay high when the economy has already slowed, or low when it is already recovering. The annualised quarter, the convention of the US Bureau of Economic Analysis (BEA), is the first to show turning points, while the 12-month measure is the one comparable with official annual figures. Comparing all three avoids hasty conclusions from a single number.",
            "interpretar": [
                "Bars above the blue line: recent momentum exceeds the annual rate, so the economy is accelerating; below it, it is slowing.",
                "The green line moves slowly: when it turns, the change in trend has already built up over several quarters.",
                "Annualising roughly quadruples quarterly noise and relies on seasonal adjustment, which is re-estimated with every release; one high or low quarter does not make a trend.",
                "Values outside −12% to 16% are pinned at the edge: in 2020–2021 the actual figures were more extreme than the drawing shows.",
            ],
            "formulas": [
                ["Annual change", "g<sub>t</sub> = (Y<sub>t</sub> ÷ Y<sub>t−4</sub> − 1) × 100", "Y = real GDP, unadjusted"],
                ["12 months", "g<sub>12m,t</sub> = (Σ<sub>k=0..3</sub> Y<sub>t−k</sub> ÷ Σ<sub>k=4..7</sub> Y<sub>t−k</sub> − 1) × 100", "rolling four-quarter sums"],
                ["Annualised quarter", "a<sub>t</sub> = ((S<sub>t</sub> ÷ S<sub>t−1</sub>)<sup>4</sup> − 1) × 100", "S = seasonally adjusted real GDP"],
                ["Display cap", "plotted value = min(16; max(−12; x))", "x = any of the three measures"],
            ],
        },
    },
    # ------------------------------------------------------------------ crecimiento por periodo
    "g-periodos": {
        "es": {
            "que": "Condensa la historia reciente del crecimiento en etapas: el auge petrolero (2010–2014), el ajuste tras la caída del precio del crudo (2015–2019), la pandemia y el rebote (2020–2021) y la pospandemia, a partir de 2022, que se incluye solo cuando sus años están completos. Para cada etapa calcula el crecimiento anual compuesto del PIB real, es decir, la tasa constante que habría llevado la economía del nivel inicial al final. La última barra muestra el año corrido frente al mismo periodo del año anterior.",
            "leer": "Eje vertical en %, con el valor escrito sobre cada barra. Las barras azul oscuro son los periodos completos; la barra azul claro es el año corrido (del primer trimestre al último publicado) y no es comparable en duración con las demás. La línea en cero separa crecimiento de contracción. El eje horizontal no es temporal: cada categoría es un periodo con sus años indicados en la etiqueta.",
            "importa": "Promediar por etapas permite separar la tendencia de largo plazo de los vaivenes de cada trimestre y comparar regímenes económicos distintos: un periodo con petróleo caro, uno de ajuste y uno de choque sanitario. Para un inversionista, el crecimiento compuesto de cada etapa es la referencia de cuánto puede expandirse el mercado interno en condiciones similares.",
            "interpretar": [
                "La tasa compuesta es menor que el promedio simple de las tasas anuales cuando estas son volátiles: por eso el periodo de pandemia muestra un crecimiento moderado aunque incluye una caída fuerte y un rebote fuerte.",
                "La barra del año corrido puede cambiar bastante con cada trimestre nuevo y con las revisiones del DANE; compárela con precaución frente a periodos de cinco años.",
                "Los cortes de los periodos son una convención basada en hitos conocidos; otros cortes darían promedios distintos.",
            ],
            "formulas": [
                ["Tasa anual compuesta", "c = ((Y<sub>A1</sub> ÷ Y<sub>A0−1</sub>)<sup>1 ÷ n</sup> − 1) × 100", "Y<sub>A</sub> = PIB real del año A (suma de 4 trimestres); A0 y A1 = primer y último año del periodo; n = A1 − A0 + 1"],
                ["Año corrido", "c<sub>yc</sub> = (Σ<sub>q≤t, año actual</sub> Y<sub>q</sub> ÷ Σ<sub>mismos trimestres, año anterior</sub> Y<sub>q</sub> − 1) × 100", "t = último trimestre publicado"],
            ],
        },
        "en": {
            "que": "Condenses recent growth history into stages: the oil boom (2010–2014), the adjustment after the crude-price fall (2015–2019), the pandemic and rebound (2020–2021) and the post-pandemic period from 2022, included only once its years are complete. For each stage it computes the compound annual growth rate of real GDP, the constant rate that would have taken the economy from the starting level to the ending one. The last bar shows year-to-date growth versus the same period a year earlier.",
            "leer": "Vertical axis in %, with the value written above each bar. Dark-blue bars are complete periods; the light-blue bar is year to date (from the first quarter to the latest published) and is not comparable in length with the rest. The zero line separates growth from contraction. The horizontal axis is not a timeline: each category is a period whose years appear in its label.",
            "importa": "Averaging by stage separates the long-run trend from quarter-to-quarter swings and compares distinct economic regimes: one with expensive oil, one of adjustment and one of a health shock. For an investor, each stage's compound growth is a benchmark of how fast the domestic market can expand under similar conditions.",
            "interpretar": [
                "The compound rate is lower than the simple average of annual rates when these are volatile, which is why the pandemic period shows moderate growth despite containing a deep fall and a strong rebound.",
                "The year-to-date bar can change markedly with each new quarter and with DANE revisions; compare it cautiously with five-year periods.",
                "Period boundaries are a convention based on well-known milestones; other cut-offs would give different averages.",
            ],
            "formulas": [
                ["Compound annual rate", "c = ((Y<sub>A1</sub> ÷ Y<sub>A0−1</sub>)<sup>1 ÷ n</sup> − 1) × 100", "Y<sub>A</sub> = real GDP in year A (sum of 4 quarters); A0 and A1 = first and last year of the period; n = A1 − A0 + 1"],
                ["Year to date", "c<sub>ytd</sub> = (Σ<sub>q≤t, current year</sub> Y<sub>q</sub> ÷ Σ<sub>same quarters, previous year</sub> Y<sub>q</sub> − 1) × 100", "t = latest published quarter"],
            ],
        },
    },
    # ------------------------------------------------------------------ real frente a nominal
    "g-real-nominal": {
        "es": {
            "que": "Compara el crecimiento del PIB medido en pesos de cada momento (nominal) con el crecimiento del PIB a precios constantes de 2015 (real). El nominal refleja a la vez cuánto más se produce y cuánto más caro se vende; el real aísla las cantidades. La distancia entre las dos líneas es, por tanto, el aumento de los precios de todo lo que produce la economía, conocido como deflactor implícito del PIB.",
            "leer": "Eje en %, variación anual desde 2012. Línea naranja: PIB nominal (billones de pesos corrientes) frente al mismo trimestre del año anterior. Línea azul: PIB real (volúmenes encadenados, base 2015) con la misma comparación. Ambas en datos originales. La línea en cero marca el paso de crecimiento a caída. Los valores se recortan entre −15% y 30% para conservar la escala.",
            "importa": "Los ingresos de las empresas, los salarios, el recaudo de impuestos y la relación deuda/PIB se mueven con el PIB nominal, no con el real. Una economía puede mostrar un crecimiento nominal alto sin que aumente la producción, solo porque suben los precios. Separar ambos componentes evita confundir inflación con dinamismo y explica por qué ciertos indicadores fiscales mejoran o empeoran aunque la actividad real no cambie.",
            "interpretar": [
                "Una distancia amplia entre las líneas indica inflación alta de toda la economía; si se estrecha, los precios crecen menos. La diferencia se analiza en el gráfico del deflactor frente al IPC.",
                "Si la línea naranja cae más que la azul, bajan los precios de lo producido, algo que ocurre cuando caen los precios del petróleo, el carbón u otras exportaciones.",
                "El PIB nominal no se publica desestacionalizado en esta comparación: ambas series usan datos originales para que la diferencia sea coherente.",
            ],
            "formulas": [
                ["Crecimiento nominal", "n<sub>t</sub> = (N<sub>t</sub> ÷ N<sub>t−4</sub> − 1) × 100", "N = PIB a precios corrientes (billones de pesos)"],
                ["Crecimiento real", "g<sub>t</sub> = (Y<sub>t</sub> ÷ Y<sub>t−4</sub> − 1) × 100", "Y = PIB a precios constantes de 2015"],
                ["Relación entre ambos", "(1 + n) = (1 + g) × (1 + π<sub>D</sub>)  ⇒  n ≈ g + π<sub>D</sub>", "π<sub>D</sub> = variación anual del deflactor del PIB (en tasas, no en %)"],
            ],
        },
        "en": {
            "que": "Compares GDP growth measured in pesos of each period (nominal) with GDP growth at constant 2015 prices (real). Nominal growth reflects both how much more is produced and how much more it sells for; real growth isolates quantities. The distance between the two lines is therefore the price increase of everything the economy produces, known as the implicit GDP deflator.",
            "leer": "Axis in %, annual change since 2012. Orange line: nominal GDP (trillions of current pesos) versus the same quarter a year earlier. Blue line: real GDP (chain-linked volumes, 2015 base) on the same comparison. Both use unadjusted data. The zero line marks the switch from growth to decline. Values are capped between −15% and 30% to keep the scale.",
            "importa": "Company revenues, wages, tax collection and the debt-to-GDP ratio move with nominal GDP, not real GDP. An economy can post high nominal growth without producing more, simply because prices rise. Separating the two avoids mistaking inflation for dynamism and explains why some fiscal ratios improve or worsen even when real activity does not change.",
            "interpretar": [
                "A wide gap between the lines signals high economy-wide inflation; a narrowing gap means prices are rising more slowly. The gap is examined in the deflator-versus-CPI chart.",
                "If the orange line falls more than the blue one, prices of what is produced are falling, as happens when oil, coal or other export prices drop.",
                "Both series use unadjusted data in this comparison so that the difference between them is consistent.",
            ],
            "formulas": [
                ["Nominal growth", "n<sub>t</sub> = (N<sub>t</sub> ÷ N<sub>t−4</sub> − 1) × 100", "N = GDP at current prices (trillions of pesos)"],
                ["Real growth", "g<sub>t</sub> = (Y<sub>t</sub> ÷ Y<sub>t−4</sub> − 1) × 100", "Y = GDP at constant 2015 prices"],
                ["Link between them", "(1 + n) = (1 + g) × (1 + π<sub>D</sub>)  ⇒  n ≈ g + π<sub>D</sub>", "π<sub>D</sub> = annual change in the GDP deflator (as rates, not %)"],
            ],
        },
    },
    # ------------------------------------------------------------------ deflactor frente al IPC
    "g-deflactor": {
        "es": {
            "que": "Compara dos medidas de inflación que miran canastas distintas. El deflactor implícito del PIB recoge los precios de todo lo que se produce en Colombia, incluidas las exportaciones (petróleo, carbón, café) y excluidas las importaciones. El Índice de Precios al Consumidor (IPC) recoge los precios de lo que compran los hogares, incluidos bienes importados. Cuando divergen, la razón principal suele ser el cambio en los términos de intercambio: la relación entre los precios de lo que el país vende y lo que compra al exterior.",
            "leer": "Eje en %, desde 2012. Línea morada: variación anual del deflactor implícito del PIB, calculado como PIB nominal sobre PIB real de cada trimestre. Línea naranja: inflación anual del IPC, promediando los tres meses de cada trimestre. La línea en cero marca deflación. Ambas se refieren al mismo trimestre, de modo que la distancia vertical entre ellas se lee directamente en puntos porcentuales.",
            "importa": "El IPC es el objetivo de política monetaria del Banco de la República; el deflactor determina el valor en pesos de la producción y, por tanto, de los ingresos de empresas y del Gobierno. Cuando el deflactor supera al IPC, el país gana poder de compra frente al exterior (mejores términos de intercambio) y suelen mejorar el recaudo y las cuentas externas; cuando va por debajo, ocurre lo contrario aunque la inflación al consumidor no cambie.",
            "interpretar": [
                "Morada por encima de la naranja: suben más los precios de lo que Colombia produce y exporta que los de la canasta de los hogares, típico de periodos de petróleo caro.",
                "Morada por debajo: los precios de los productos exportados caen o suben menos; el ingreso nacional crece menos que lo que sugiere el PIB real.",
                "El deflactor es una medida implícita: se revisa cada vez que el DANE revisa el PIB nominal o real, y en trimestres de choque puede moverse de forma brusca.",
                "La relación con los términos de intercambio se puede contrastar en la página del sector externo.",
            ],
            "formulas": [
                ["Deflactor implícito", "D<sub>t</sub> = N<sub>t</sub> ÷ Y<sub>t</sub>", "N = PIB nominal; Y = PIB real (base 2015), datos originales"],
                ["Inflación del deflactor", "π<sub>D,t</sub> = (D<sub>t</sub> ÷ D<sub>t−4</sub> − 1) × 100", "variación anual del trimestre t"],
                ["IPC trimestral", "π<sub>IPC,t</sub> = (1 ÷ 3) × Σ<sub>m∈t</sub> π<sub>m</sub>", "π<sub>m</sub> = inflación anual del IPC en el mes m"],
            ],
        },
        "en": {
            "que": "Compares two inflation measures that look at different baskets. The implicit GDP deflator captures prices of everything produced in Colombia, including exports (oil, coal, coffee) and excluding imports. The Consumer Price Index (CPI) captures prices of what households buy, including imported goods. When they diverge, the main reason is usually a change in the terms of trade: the ratio between the prices of what the country sells abroad and what it buys.",
            "leer": "Axis in %, from 2012. Purple line: annual change in the implicit GDP deflator, calculated as nominal over real GDP each quarter. Orange line: annual CPI inflation, averaging the three months of each quarter. The zero line marks deflation. Both refer to the same quarter, so the vertical distance between them reads directly in percentage points.",
            "importa": "The CPI is Banco de la República's policy target; the deflator sets the peso value of output and therefore of corporate and government income. When the deflator runs above the CPI, the country gains purchasing power abroad (better terms of trade) and tax revenue and external accounts tend to improve; when it runs below, the opposite happens even if consumer inflation is unchanged.",
            "interpretar": [
                "Purple above orange: prices of what Colombia produces and exports are rising faster than the household basket, typical of high-oil-price periods.",
                "Purple below orange: export prices are falling or rising less; national income grows less than real GDP suggests.",
                "The deflator is an implicit measure: it is revised whenever DANE revises nominal or real GDP, and it can move abruptly in shock quarters.",
                "The link with the terms of trade can be checked on the external-sector page.",
            ],
            "formulas": [
                ["Implicit deflator", "D<sub>t</sub> = N<sub>t</sub> ÷ Y<sub>t</sub>", "N = nominal GDP; Y = real GDP (2015 base), unadjusted"],
                ["Deflator inflation", "π<sub>D,t</sub> = (D<sub>t</sub> ÷ D<sub>t−4</sub> − 1) × 100", "annual change in quarter t"],
                ["Quarterly CPI", "π<sub>CPI,t</sub> = (1 ÷ 3) × Σ<sub>m∈t</sub> π<sub>m</sub>", "π<sub>m</sub> = annual CPI inflation in month m"],
            ],
        },
    },
    # ------------------------------------------------------------------ aportes por grandes grupos
    "g-aportes-grupos": {
        "es": {
            "que": "Descompone el crecimiento anual del valor agregado en cuatro grandes grupos de actividades: sector primario (agro y minería), industria, energía y construcción, servicios de mercado, y Gobierno, educación y salud. Cada bloque indica cuántos puntos del crecimiento total explica ese grupo, combinando su tamaño y su ritmo de crecimiento. Así se ve quién está empujando la economía y quién la está frenando en cada trimestre.",
            "leer": "Eje en puntos porcentuales (pp), últimos cuatro años, un grupo de barras por trimestre. Barras apiladas: azul, servicios de mercado (comercio, transporte, turismo, comunicaciones, finanzas, inmobiliarias, servicios profesionales y entretenimiento); morado, Gobierno, educación y salud; verde, industria, electricidad, gas, agua y construcción; naranja, primario. Los aportes negativos se apilan por debajo de cero. La línea negra con puntos es la suma de todos los aportes, que aproxima el crecimiento anual del valor agregado.",
            "importa": "Un mismo crecimiento puede tener orígenes muy distintos: no es igual que lo impulsen los servicios privados que el gasto público o la minería. La composición informa sobre la sostenibilidad del ciclo, la generación de empleo y los sectores donde se concentran ingresos y utilidades, información útil para evaluar exposición sectorial en carteras y créditos.",
            "interpretar": [
                "Un grupo pequeño que crece mucho puede aportar menos que un grupo grande que crece poco: el aporte pondera el crecimiento por el peso en la economía.",
                "Si la mayor parte de la barra viene del bloque morado, el crecimiento depende del sector público y servicios sociales; el gráfico de la economía con y sin Gobierno lo cuantifica.",
                "La línea mide el valor agregado, no el PIB: falta el aporte de los impuestos netos de subvenciones y, como los volúmenes encadenados no son aditivos, la suma puede diferir unas décimas del crecimiento publicado.",
                "El grupo de Gobierno incluye la educación y la salud privadas: es una aproximación al sector público, no una medida exacta.",
            ],
            "formulas": [
                ["Aporte de un sector", "a<sub>i,t</sub> = (X<sub>i,t</sub> − X<sub>i,t−4</sub>) ÷ VA<sub>t−4</sub> × 100 = g<sub>i,t</sub> × w<sub>i,t−4</sub>", "X<sub>i</sub> = valor agregado real del sector i; VA = valor agregado total; g = variación anual; w = participación en el VA"],
                ["Aporte de un grupo", "A<sub>G,t</sub> = Σ<sub>i∈G</sub> a<sub>i,t</sub>", "G = conjunto de sectores CIIU del grupo"],
                ["Total (línea)", "T<sub>t</sub> = Σ<sub>i=1..12</sub> a<sub>i,t</sub>", "suma de los aportes de las 12 agrupaciones CIIU"],
            ],
        },
        "en": {
            "que": "Breaks annual value-added growth into four broad groups of activities: the primary sector (farming and mining), manufacturing, utilities and construction, market services, and government, education and health. Each block shows how many points of total growth that group explains, combining its size and its growth rate. It reveals who is pushing the economy forward and who is holding it back each quarter.",
            "leer": "Axis in percentage points (pp), last four years, one stack per quarter. Stacked bars: blue, market services (trade, transport, tourism, communications, finance, real estate, professional services and entertainment); purple, government, education and health; green, manufacturing, electricity, gas, water and construction; orange, primary. Negative contributions stack below zero. The black line with dots is the sum of all contributions, which approximates annual value-added growth.",
            "importa": "The same growth rate can have very different sources: it matters whether private services, public spending or mining are driving it. The mix speaks to the sustainability of the cycle, job creation and where income and profits are concentrated, information that helps assess sector exposure in portfolios and loan books.",
            "interpretar": [
                "A small group growing fast can contribute less than a large group growing slowly: the contribution weights growth by size in the economy.",
                "If most of the stack comes from the purple block, growth depends on the public sector and social services; the chart of the economy with and without government quantifies this.",
                "The line measures value added, not GDP: net taxes on products are missing and, since chain-linked volumes are not additive, the sum may differ by a few tenths from published growth.",
                "The government group includes private education and health: it approximates the public sector rather than measuring it exactly.",
            ],
            "formulas": [
                ["Sector contribution", "a<sub>i,t</sub> = (X<sub>i,t</sub> − X<sub>i,t−4</sub>) ÷ VA<sub>t−4</sub> × 100 = g<sub>i,t</sub> × w<sub>i,t−4</sub>", "X<sub>i</sub> = real value added of sector i; VA = total value added; g = annual change; w = share of VA"],
                ["Group contribution", "A<sub>G,t</sub> = Σ<sub>i∈G</sub> a<sub>i,t</sub>", "G = set of ISIC sectors in the group"],
                ["Total (line)", "T<sub>t</sub> = Σ<sub>i=1..12</sub> a<sub>i,t</sub>", "sum of the contributions of the 12 ISIC groupings"],
            ],
        },
    },
    # ------------------------------------------------------------------ con y sin Gobierno
    "g-sin-gobierno": {
        "es": {
            "que": "Muestra cuánto crecería el valor agregado si se excluyera un sector concreto: el de Gobierno, educación y salud (secciones O, P y Q de la Clasificación Industrial Internacional Uniforme, CIIU) o la minería. Sirve para saber si el crecimiento total está sostenido por la actividad privada y diversificada o descansa en el sector público o en los hidrocarburos y el carbón.",
            "leer": "Eje en %, variación anual desde 2012. Línea azul: crecimiento total del valor agregado (suma de los aportes de los 12 sectores). Línea verde: crecimiento del resto de la economía sin Gobierno, educación y salud. Línea gris punteada: crecimiento sin minería. La línea en cero separa crecimiento de contracción. Los valores se recortan entre −12% y 16% para que 2020–2021 no aplasten la escala.",
            "importa": "El sector público crece por decisiones presupuestarias, no por la demanda del mercado, y la minería depende de precios internacionales y de la geología. Si el resto de la economía crece mucho menos que el total, el dinamismo es más estrecho y menos ligado al consumo y la inversión privados, lo que importa para leer el empleo formal, el crédito y las ventas de las empresas.",
            "interpretar": [
                "Verde por debajo de azul: el sector Gobierno, educación y salud crece más que el resto y sostiene el total; verde por encima: el sector privado y los demás servicios van más rápido.",
                "Gris por encima de azul: la minería está restando al crecimiento; por debajo, lo está sumando.",
                "El sector O-P-Q incluye la educación y la salud privadas, por lo que «sin Gobierno» es una aproximación al crecimiento privado.",
                "El cálculo usa aportes aproximados de volúmenes encadenados, que no son exactamente aditivos; diferencias de pocas décimas no son significativas.",
            ],
            "formulas": [
                ["Crecimiento sin el sector X", "g<sub>−X,t</sub> = 100 × (Σ<sub>i</sub> a<sub>i,t</sub> − a<sub>X,t</sub>) ÷ (Σ<sub>i</sub> w<sub>i,t</sub> − w<sub>X,t</sub>)", "a = aporte en pp; w = participación en el valor agregado en %; Σ sobre los 12 sectores"],
                ["Total (línea azul)", "T<sub>t</sub> = Σ<sub>i</sub> a<sub>i,t</sub>", "a<sub>i,t</sub> = (X<sub>i,t</sub> − X<sub>i,t−4</sub>) ÷ VA<sub>t−4</sub> × 100"],
            ],
        },
        "en": {
            "que": "Shows how fast value added would grow if a specific sector were excluded: government, education and health (sections O, P and Q of the International Standard Industrial Classification, ISIC) or mining. It tells whether total growth rests on broad private activity or on the public sector or on oil and coal.",
            "leer": "Axis in %, annual change since 2012. Blue line: total value-added growth (sum of the 12 sector contributions). Green line: growth of the rest of the economy excluding government, education and health. Grey dotted line: growth excluding mining. The zero line separates growth from contraction. Values are capped between −12% and 16% so 2020–2021 do not flatten the scale.",
            "importa": "The public sector grows on budget decisions rather than market demand, and mining depends on world prices and geology. If the rest of the economy grows much more slowly than the total, momentum is narrower and less tied to private consumption and investment, which matters for reading formal employment, credit and company sales.",
            "interpretar": [
                "Green below blue: government, education and health is growing faster than the rest and propping up the total; green above blue: the private sector and other services are moving faster.",
                "Grey above blue: mining is subtracting from growth; below blue, it is adding to it.",
                "The O-P-Q sector includes private education and health, so \"excluding government\" approximates private growth.",
                "The calculation uses approximate contributions from chain-linked volumes, which are not exactly additive; differences of a few tenths are not meaningful.",
            ],
            "formulas": [
                ["Growth excluding sector X", "g<sub>−X,t</sub> = 100 × (Σ<sub>i</sub> a<sub>i,t</sub> − a<sub>X,t</sub>) ÷ (Σ<sub>i</sub> w<sub>i,t</sub> − w<sub>X,t</sub>)", "a = contribution in pp; w = share of value added in %; Σ over the 12 sectors"],
                ["Total (blue line)", "T<sub>t</sub> = Σ<sub>i</sub> a<sub>i,t</sub>", "a<sub>i,t</sub> = (X<sub>i,t</sub> − X<sub>i,t−4</sub>) ÷ VA<sub>t−4</sub> × 100"],
            ],
        },
    },
    # ------------------------------------------------------------------ barras por sector
    "g-sec-barras": {
        "es": {
            "que": "Ordena las 12 grandes ramas de actividad de las cuentas nacionales (agrupaciones de la CIIU Rev. 4) según cuánto creció cada una frente al mismo trimestre del año anterior. Junto a cada barra aparece el dato de un año antes, de modo que se ve no solo quién crece más, sino quién se está acelerando y quién se está frenando. Es la fotografía sectorial del trimestre más reciente, o de cualquier trimestre elegido en el selector.",
            "leer": "Eje horizontal en % de variación anual real; los sectores están ordenados de mayor (arriba) a menor crecimiento. Barra azul: el sector creció; barra naranja: cayó; el valor está escrito al final de cada barra. La raya negra vertical sobre cada fila es la variación anual del mismo sector un año antes. La línea en cero separa crecimiento de caída. Al pasar el cursor se ve el peso del sector en el valor agregado y su aporte en pp. El selector permite ver otro trimestre y el botón vuelve al último; también se puede elegir haciendo clic en el mapa de calor.",
            "importa": "El agregado esconde dispersión: un PIB moderado puede convivir con sectores en auge y otros en recesión. Para un inversionista, conocer qué sectores se aceleran o se contraen orienta el análisis de empresas, crédito y empleo, y permite distinguir si un cambio en el PIB proviene de un sector grande o de muchos sectores a la vez.",
            "interpretar": [
                "Barra más larga que la raya: el sector crece más que hace un año (aceleración); más corta: se frena. Si la barra es naranja y la raya está a la derecha del cero, el sector pasó de crecer a caer.",
                "El crecimiento alto de un sector pequeño pesa poco en el total; el aporte (en el recuadro flotante) combina crecimiento y tamaño.",
                "Los sectores con alta volatilidad, como minería, agro o construcción, pueden mostrar cambios grandes sin que cambie la tendencia de fondo.",
                "Los datos son originales, sin desestacionalizar, y se revisan en cada publicación del DANE; los aportes son aproximados porque los volúmenes encadenados no suman exactamente.",
            ],
            "formulas": [
                ["Variación anual del sector", "g<sub>i,t</sub> = (X<sub>i,t</sub> ÷ X<sub>i,t−4</sub> − 1) × 100", "X<sub>i,t</sub> = valor agregado real del sector i (volúmenes encadenados, base 2015)"],
                ["Peso en la economía", "w<sub>i,t</sub> = X<sub>i,t</sub> ÷ VA<sub>t</sub> × 100", "VA = valor agregado total del mismo trimestre"],
                ["Aporte al crecimiento", "a<sub>i,t</sub> = (X<sub>i,t</sub> − X<sub>i,t−4</sub>) ÷ VA<sub>t−4</sub> × 100", "en pp del valor agregado de hace un año"],
            ],
        },
        "en": {
            "que": "Ranks the 12 broad activity branches of the national accounts (ISIC Rev. 4 groupings) by how much each grew versus the same quarter a year earlier. Next to each bar sits the figure from a year before, so it shows not only who grows most but who is speeding up and who is slowing. It is the sector snapshot of the latest quarter, or of any quarter chosen in the selector.",
            "leer": "Horizontal axis in % real annual change; sectors are sorted from highest (top) to lowest growth. Blue bar: the sector grew; orange bar: it shrank; the value is written at the end of each bar. The black vertical tick on each row is the same sector's annual change a year earlier. The zero line separates growth from decline. Hovering shows the sector's share of value added and its contribution in pp. The selector shows another quarter and the button returns to the latest; you can also pick a quarter by clicking the heat map.",
            "importa": "The aggregate hides dispersion: moderate GDP can coexist with booming sectors and others in recession. For an investor, knowing which sectors are accelerating or contracting guides the analysis of companies, credit and employment, and shows whether a change in GDP comes from one large sector or from many at once.",
            "interpretar": [
                "Bar longer than the tick: the sector is growing faster than a year ago (acceleration); shorter: it is slowing. An orange bar with the tick right of zero means the sector went from growth to decline.",
                "Fast growth in a small sector weighs little in the total; the contribution (in the tooltip) combines growth and size.",
                "Volatile sectors such as mining, farming or construction can show large swings without a change in the underlying trend.",
                "Data are unadjusted and revised with every DANE release; contributions are approximate because chain-linked volumes do not add up exactly.",
            ],
            "formulas": [
                ["Sector annual change", "g<sub>i,t</sub> = (X<sub>i,t</sub> ÷ X<sub>i,t−4</sub> − 1) × 100", "X<sub>i,t</sub> = real value added of sector i (chain-linked volumes, 2015 base)"],
                ["Share of the economy", "w<sub>i,t</sub> = X<sub>i,t</sub> ÷ VA<sub>t</sub> × 100", "VA = total value added in the same quarter"],
                ["Contribution to growth", "a<sub>i,t</sub> = (X<sub>i,t</sub> − X<sub>i,t−4</sub>) ÷ VA<sub>t−4</sub> × 100", "in pp of value added a year earlier"],
            ],
        },
    },
    # ------------------------------------------------------------------ mapa de calor sectorial
    "g-sec-mapa": {
        "es": {
            "que": "Reúne en una sola imagen el crecimiento anual de los 12 sectores en cada trimestre. Permite seguir la historia sectorial completa: qué ramas se hundieron en 2020, cuáles se recuperaron primero, cuáles llevan varios trimestres en terreno negativo y si las caídas o los auges son generalizados o se concentran en pocas actividades.",
            "leer": "Cada fila es un sector, ordenado por su peso en el valor agregado del último trimestre (los más grandes arriba); cada columna es un trimestre. El color indica la variación anual real: blanco cerca de cero, azul cada vez más intenso para crecimientos altos y naranja para caídas. La escala de color se satura en ±12%: valores más extremos se ven con el color del borde, y el recuadro flotante muestra el valor exacto. La vista inicial cubre los últimos cinco años; al hacer clic en una casilla, el gráfico de barras pasa a ese trimestre.",
            "importa": "Un mapa de calor permite ver de un vistazo la persistencia y la amplitud de los movimientos sectoriales, algo difícil de captar con líneas superpuestas. Para un inversionista, señala sectores con debilidad o fortaleza sostenida, que es la información relevante para evaluar ciclos de ingresos y riesgo de crédito por actividad.",
            "interpretar": [
                "Columnas casi todas naranjas indican una contracción generalizada (como en 2020); columnas mixtas, un ciclo con ganadores y perdedores.",
                "Una fila con naranja persistente revela un sector en declive o en ajuste prolongado, aunque el agregado crezca.",
                "El orden por tamaño ayuda a ponderar: un cambio de color en las filas superiores mueve el PIB mucho más que en las inferiores.",
                "Los datos originales pueden mostrar saltos por efectos de calendario o base; el índice de difusión resume cuántas casillas son positivas en cada trimestre.",
            ],
            "formulas": [
                ["Valor de cada casilla", "g<sub>i,t</sub> = (X<sub>i,t</sub> ÷ X<sub>i,t−4</sub> − 1) × 100", "X<sub>i,t</sub> = valor agregado real del sector i en el trimestre t"],
                ["Color", "c = min(12; max(−12; g<sub>i,t</sub>))", "escala divergente centrada en cero"],
            ],
        },
        "en": {
            "que": "Puts the annual growth of all 12 sectors in every quarter into a single picture. It traces the complete sector history: which branches collapsed in 2020, which recovered first, which have spent several quarters in negative territory and whether slumps or booms are widespread or concentrated in a few activities.",
            "leer": "Each row is a sector, ordered by its share of value added in the latest quarter (largest at the top); each column is a quarter. Colour shows real annual change: white near zero, increasingly deep blue for strong growth and orange for declines. The colour scale saturates at ±12%: more extreme values take the edge colour, and the tooltip shows the exact figure. The initial view covers the last five years; clicking a cell switches the bar chart to that quarter.",
            "importa": "A heat map shows at a glance the persistence and breadth of sector movements, which overlapping lines struggle to convey. For an investor it flags sectors with sustained weakness or strength, the relevant input for assessing revenue cycles and credit risk by activity.",
            "interpretar": [
                "Columns that are almost all orange mark a broad contraction (as in 2020); mixed columns mark a cycle with winners and losers.",
                "A row with persistent orange reveals a sector in decline or prolonged adjustment, even if the aggregate grows.",
                "The size ordering helps weighting: a colour change in the top rows moves GDP far more than one in the bottom rows.",
                "Unadjusted data can jump because of calendar or base effects; the diffusion index summarises how many cells are positive each quarter.",
            ],
            "formulas": [
                ["Cell value", "g<sub>i,t</sub> = (X<sub>i,t</sub> ÷ X<sub>i,t−4</sub> − 1) × 100", "X<sub>i,t</sub> = real value added of sector i in quarter t"],
                ["Colour", "c = min(12; max(−12; g<sub>i,t</sub>))", "diverging scale centred on zero"],
            ],
        },
    },
    # ------------------------------------------------------------------ índice de difusión
    "g-sectores-crecen": {
        "es": {
            "que": "Cuenta, trimestre a trimestre, cuántos de los 12 sectores de la economía producen más que un año antes. Es un índice de difusión, en la tradición de Burns y Mitchell (1946): no mide cuánto crece la economía, sino qué tan extendido está el crecimiento. Un PIB que sube con pocos sectores es más frágil que uno que sube con casi todos.",
            "leer": "Eje vertical de 0 a 12 sectores, desde 2010. Cada barra es un trimestre. Barras verdes: 7 o más sectores crecen (crecimiento extendido); barras naranjas: 6 o menos. La línea punteada en 6,5 marca la mitad y separa ambos casos. Un sector cuenta como creciente si su variación anual real es mayor que cero, sin importar su tamaño.",
            "importa": "La amplitud complementa la magnitud: en las expansiones sólidas la mayoría de los sectores crece a la vez, mientras que en las fases de debilidad el crecimiento se concentra. Para un inversionista, una difusión alta reduce la dependencia de un solo motor y suele acompañar mejoras en empleo y crédito; una difusión baja indica que el dato agregado descansa en pocas actividades.",
            "interpretar": [
                "Barras verdes persistentes acompañan expansiones amplias; una racha de barras naranjas, aunque el PIB crezca, señala un crecimiento estrecho.",
                "El índice no pondera por tamaño: un trimestre con 10 sectores creciendo puede tener un PIB bajo si los sectores grandes caen. Compárelo con el gráfico de aportes.",
                "Un sector con crecimiento de 0,1% cuenta igual que uno con 10%; cambios pequeños alrededor de cero pueden mover el conteo sin cambio económico relevante.",
            ],
            "formulas": [
                ["Índice de difusión", "D<sub>t</sub> = Σ<sub>i=1..12</sub> 1[g<sub>i,t</sub> > 0]", "1[·] = 1 si la condición se cumple y 0 si no; g<sub>i,t</sub> = variación anual real del sector i"],
            ],
        },
        "en": {
            "que": "Counts, quarter by quarter, how many of the economy's 12 sectors are producing more than a year earlier. It is a diffusion index in the tradition of Burns and Mitchell (1946): it does not measure how fast the economy grows but how widespread growth is. GDP rising on the back of few sectors is more fragile than GDP rising with almost all of them.",
            "leer": "Vertical axis from 0 to 12 sectors, since 2010. Each bar is a quarter. Green bars: 7 or more sectors growing (broad growth); orange bars: 6 or fewer. The dotted line at 6.5 marks the midpoint and separates the two cases. A sector counts as growing if its real annual change is above zero, regardless of its size.",
            "importa": "Breadth complements magnitude: in solid expansions most sectors grow at once, while in weak phases growth concentrates. For an investor, high diffusion reduces reliance on a single engine and tends to accompany better employment and credit; low diffusion means the headline figure rests on a few activities.",
            "interpretar": [
                "Persistent green bars accompany broad expansions; a run of orange bars, even with GDP growing, signals narrow growth.",
                "The index is not size-weighted: a quarter with 10 sectors growing can show weak GDP if large sectors fall. Compare it with the contributions chart.",
                "A sector growing 0.1% counts the same as one growing 10%; small changes around zero can move the count without meaningful economic change.",
            ],
            "formulas": [
                ["Diffusion index", "D<sub>t</sub> = Σ<sub>i=1..12</sub> 1[g<sub>i,t</sub> > 0]", "1[·] = 1 if the condition holds and 0 otherwise; g<sub>i,t</sub> = real annual change of sector i"],
            ],
        },
    },
    # ------------------------------------------------------------------ sectores frente a su historia
    "g-sector-historia": {
        "es": {
            "que": "Compara el crecimiento reciente de cada sector con su propio desempeño en 2015–2019, un periodo previo a la pandemia sin choques extremos. Responde si cada actividad va hoy más rápido o más lento de lo que era normal para ella, algo que el ranking de crecimiento no muestra porque cada sector tiene su propio ritmo típico.",
            "leer": "Eje horizontal en % de variación anual real. Cada fila es un sector, ordenado de menor (abajo) a mayor (arriba) crecimiento reciente. Punto gris: promedio de la variación anual de 2015T1 a 2019T4. Punto de color: promedio de los últimos cuatro trimestres publicados; verde si supera al promedio histórico y naranja si queda por debajo. La barra gris clara une los dos puntos y su longitud es la distancia entre hoy y la historia. La línea vertical marca el cero.",
            "importa": "Un crecimiento de 2% puede ser bueno para un sector maduro y malo para uno que solía crecer al 6%. Medir contra la propia historia identifica cambios estructurales o cíclicos por actividad, útiles para valorar empresas y para entender qué sectores explican que la economía crezca por encima o por debajo de su ritmo previo.",
            "interpretar": [
                "Muchos puntos verdes indican que la mayoría de sectores supera su ritmo habitual; muchos naranjas, una economía que crece por debajo de su historia en forma extendida.",
                "Una distancia grande hacia la izquierda en un sector importante (por ejemplo, minería o construcción) puede explicar buena parte de la diferencia entre el crecimiento actual y el previo a la pandemia.",
                "El promedio de cuatro trimestres suaviza el ruido, pero incluye trimestres con datos originales y revisiones; el punto de color se mueve con cada publicación.",
                "El periodo 2015–2019 incluye la caída del petróleo: no es un «ideal», solo una referencia reciente sin pandemia.",
            ],
            "formulas": [
                ["Promedio histórico", "h<sub>i</sub> = (1 ÷ 20) × Σ<sub>t=2015T1..2019T4</sub> g<sub>i,t</sub>", "g<sub>i,t</sub> = variación anual real del sector i en el trimestre t"],
                ["Promedio reciente", "u<sub>i</sub> = (1 ÷ 4) × Σ<sub>k=0..3</sub> g<sub>i,T−k</sub>", "T = último trimestre publicado"],
                ["Color", "verde si u<sub>i</sub> ≥ h<sub>i</sub>; naranja en caso contrario", "u<sub>i</sub> = promedio reciente; h<sub>i</sub> = promedio 2015–2019 del sector i"],
            ],
        },
        "en": {
            "que": "Compares each sector's recent growth with its own performance in 2015–2019, a pre-pandemic period without extreme shocks. It answers whether each activity is now growing faster or slower than was normal for it, which the growth ranking cannot show because every sector has its own typical pace.",
            "leer": "Horizontal axis in % real annual change. Each row is a sector, ordered from lowest (bottom) to highest (top) recent growth. Grey dot: average annual change from 2015Q1 to 2019Q4. Coloured dot: average of the last four published quarters; green if above the historical average and orange if below. The light grey bar links the two dots and its length is the distance between today and history. The vertical line marks zero.",
            "importa": "Growth of 2% may be good for a mature sector and poor for one that used to grow 6%. Measuring against each sector's own history identifies structural or cyclical shifts by activity, useful for valuing companies and for understanding which sectors explain the economy growing above or below its earlier pace.",
            "interpretar": [
                "Many green dots mean most sectors exceed their usual pace; many orange ones, an economy growing below its history across the board.",
                "A long gap to the left in a major sector (for instance mining or construction) can explain much of the difference between current and pre-pandemic growth.",
                "The four-quarter average smooths noise but includes unadjusted, revisable data; the coloured dot moves with every release.",
                "The 2015–2019 period includes the oil-price fall: it is not an \"ideal\", only a recent benchmark without the pandemic.",
            ],
            "formulas": [
                ["Historical average", "h<sub>i</sub> = (1 ÷ 20) × Σ<sub>t=2015Q1..2019Q4</sub> g<sub>i,t</sub>", "g<sub>i,t</sub> = real annual change of sector i in quarter t"],
                ["Recent average", "u<sub>i</sub> = (1 ÷ 4) × Σ<sub>k=0..3</sub> g<sub>i,T−k</sub>", "T = latest published quarter"],
                ["Colour", "green if u<sub>i</sub> ≥ h<sub>i</sub>; orange otherwise", "u<sub>i</sub> = recent average; h<sub>i</sub> = 2015–2019 average of sector i"],
            ],
        },
    },
    # ------------------------------------------------------------------ aportes por demanda
    "g-demanda-aportes": {
        "es": {
            "que": "Mira el crecimiento desde el lado del gasto: cuántos puntos del crecimiento anual del PIB explican el consumo de los hogares, el gasto del Gobierno, la inversión fija y el comercio exterior neto. Es la otra cara de los aportes por sector: allí se ve quién produce; aquí, quién compra lo producido y cuánto de la demanda se atiende con importaciones.",
            "leer": "Eje en puntos porcentuales (pp), últimos 16 trimestres. Barras apiladas: azul, consumo de los hogares (incluye las instituciones sin fines de lucro que sirven a los hogares, ISFLH); morado, gasto del Gobierno; verde, inversión fija (formación bruta de capital fijo); naranja, comercio exterior neto (aporte de exportaciones menos aporte de importaciones); gris, existencias y discrepancia, el residuo hasta el PIB. La línea negra con puntos es el crecimiento anual del PIB. Los aportes negativos se apilan por debajo de cero.",
            "importa": "La composición de la demanda indica la calidad del crecimiento: el impulsado por inversión amplía la capacidad productiva, el impulsado por consumo puede apoyarse en crédito, y un comercio neto muy negativo indica que buena parte del gasto se filtra al exterior y presiona la cuenta corriente. Para un inversionista, distinguir estos motores ayuda a leer sectores, importaciones y balanza de pagos.",
            "interpretar": [
                "Un bloque naranja negativo y grande significa que las importaciones crecen más que las exportaciones: la demanda interna avanza más rápido que la producción local.",
                "El bloque gris es un residuo: incluye la variación de inventarios y la no aditividad de los índices encadenados, y puede ser grande y volátil; no debe leerse como un motor económico en sí mismo.",
                "Los aportes usan datos originales frente al mismo trimestre del año anterior; trimestres con calendario atípico pueden distorsionar la composición.",
                "La suma de las barras coincide con la línea del PIB por construcción, gracias al residuo.",
            ],
            "formulas": [
                ["Aporte de un componente", "a<sub>k,t</sub> = (C<sub>k,t</sub> − C<sub>k,t−4</sub>) ÷ PIB<sub>t−4</sub> × 100", "C<sub>k</sub> = volumen encadenado del componente k (datos originales)"],
                ["Comercio exterior neto", "a<sub>net,t</sub> = a<sub>X,t</sub> − a<sub>M,t</sub>", "X = exportaciones; M = importaciones"],
                ["Existencias y discrepancia", "a<sub>res,t</sub> = g<sub>PIB,t</sub> − (a<sub>hog</sub> + a<sub>gob</sub> + a<sub>inv</sub> + a<sub>net</sub>)", "g<sub>PIB,t</sub> = (PIB<sub>t</sub> ÷ PIB<sub>t−4</sub> − 1) × 100"],
            ],
        },
        "en": {
            "que": "Looks at growth from the spending side: how many points of annual GDP growth are explained by household consumption, government spending, fixed investment and net foreign trade. It is the mirror image of the sector contributions: there you see who produces; here, who buys what is produced and how much demand is met by imports.",
            "leer": "Axis in percentage points (pp), last 16 quarters. Stacked bars: blue, household consumption (including non-profit institutions serving households, NPISH); purple, government spending; green, fixed investment (gross fixed capital formation); orange, net foreign trade (export contribution minus import contribution); grey, inventories and discrepancy, the residual up to GDP. The black line with dots is annual GDP growth. Negative contributions stack below zero.",
            "importa": "The mix of demand speaks to the quality of growth: investment-led growth expands productive capacity, consumption-led growth may lean on credit, and strongly negative net trade means much of spending leaks abroad and weighs on the current account. For an investor, separating these engines helps read sectors, imports and the balance of payments.",
            "interpretar": [
                "A large negative orange block means imports are growing faster than exports: domestic demand is outpacing local production.",
                "The grey block is a residual: it includes inventory changes and the non-additivity of chain-linked indices, can be large and volatile, and should not be read as an economic engine in itself.",
                "Contributions use unadjusted data versus the same quarter a year earlier; quarters with unusual calendars can distort the mix.",
                "The bars add up to the GDP line by construction, thanks to the residual.",
            ],
            "formulas": [
                ["Component contribution", "a<sub>k,t</sub> = (C<sub>k,t</sub> − C<sub>k,t−4</sub>) ÷ GDP<sub>t−4</sub> × 100", "C<sub>k</sub> = chain-linked volume of component k (unadjusted)"],
                ["Net foreign trade", "a<sub>net,t</sub> = a<sub>X,t</sub> − a<sub>M,t</sub>", "X = exports; M = imports"],
                ["Inventories and discrepancy", "a<sub>res,t</sub> = g<sub>GDP,t</sub> − (a<sub>hh</sub> + a<sub>gov</sub> + a<sub>inv</sub> + a<sub>net</sub>)", "g<sub>GDP,t</sub> = (GDP<sub>t</sub> ÷ GDP<sub>t−4</sub> − 1) × 100"],
            ],
        },
    },
    # ------------------------------------------------------------------ crecimiento por componente
    "g-demanda-crec": {
        "es": {
            "que": "Muestra cuánto creció en términos reales cada gran componente de la demanda en el último trimestre publicado: PIB, demanda interna, consumo de los hogares, gasto del Gobierno, inversión fija, exportaciones e importaciones. A diferencia del gráfico de aportes, aquí no se pondera por tamaño: se ve el ritmo propio de cada componente.",
            "leer": "Eje horizontal en % de variación anual real frente al mismo trimestre del año anterior (volúmenes encadenados, datos originales). Barras azules: el componente crece; naranjas: cae; el valor está escrito al final de cada barra. El orden es fijo, de arriba abajo: PIB, demanda interna, consumo de los hogares (incluye las ISFLH), gasto del Gobierno, inversión fija, exportaciones e importaciones. La línea vertical marca el cero.",
            "importa": "Comparar la demanda interna con el PIB indica si el gasto de residentes va más rápido que la producción, lo que se cubre con importaciones y se refleja en la cuenta corriente. El ritmo de la inversión anticipa la ampliación de capacidad productiva y el de las exportaciones muestra la conexión con la demanda externa, datos relevantes para la tasa de cambio y las cuentas externas.",
            "interpretar": [
                "Demanda interna por encima del PIB: el país gasta más rápido de lo que produce y la diferencia sale por importaciones; por debajo, ocurre lo contrario.",
                "Las importaciones restan en la identidad del PIB: si crecen, una parte del gasto interno se atiende con producción extranjera.",
                "La inversión fija es el componente más volátil: tasas de dos dígitos, positivas o negativas, son frecuentes y deben leerse junto con su nivel (ver la tasa de inversión).",
                "Un solo trimestre puede estar afectado por calendario, revisiones o efectos base; el gráfico de aportes muestra la evolución en el tiempo.",
            ],
            "formulas": [
                ["Variación anual real", "g<sub>k,t</sub> = (C<sub>k,t</sub> ÷ C<sub>k,t−4</sub> − 1) × 100", "C<sub>k,t</sub> = volumen encadenado del componente k en el último trimestre t"],
                ["Identidad del gasto", "PIB = C<sub>hog</sub> + G + FBKF + ΔE + X − M", "C<sub>hog</sub> = consumo de los hogares; G = Gobierno; FBKF = inversión fija; ΔE = existencias; X − M = comercio neto (a precios corrientes; en volúmenes encadenados la suma no es exacta)"],
            ],
        },
        "en": {
            "que": "Shows how much each major demand component grew in real terms in the latest published quarter: GDP, domestic demand, household consumption, government spending, fixed investment, exports and imports. Unlike the contributions chart, there is no size weighting here: each component's own pace is shown.",
            "leer": "Horizontal axis in % real annual change versus the same quarter a year earlier (chain-linked volumes, unadjusted). Blue bars: growing; orange: falling; the value is written at the end of each bar. The order is fixed, from top to bottom: GDP, domestic demand, household consumption (including NPISH), government spending, fixed investment, exports and imports. The vertical line marks zero.",
            "importa": "Comparing domestic demand with GDP shows whether residents' spending outpaces production, which is met through imports and shows up in the current account. Investment's pace signals expansion of productive capacity and exports' pace the link with external demand, both relevant for the exchange rate and external accounts.",
            "interpretar": [
                "Domestic demand above GDP: the country is spending faster than it produces and the gap is filled by imports; below GDP, the reverse.",
                "Imports subtract in the GDP identity: when they grow, part of domestic spending is met by foreign output.",
                "Fixed investment is the most volatile component: double-digit rates, positive or negative, are common and should be read alongside its level (see the investment rate).",
                "A single quarter can be affected by calendar, revisions or base effects; the contributions chart shows the evolution over time.",
            ],
            "formulas": [
                ["Real annual change", "g<sub>k,t</sub> = (C<sub>k,t</sub> ÷ C<sub>k,t−4</sub> − 1) × 100", "C<sub>k,t</sub> = chain-linked volume of component k in the latest quarter t"],
                ["Expenditure identity", "GDP = C<sub>hh</sub> + G + GFCF + ΔI + X − M", "C<sub>hh</sub> = household consumption; G = government; GFCF = fixed investment; ΔI = inventories; X − M = net trade (exact at current prices; not additive in chain-linked volumes)"],
            ],
        },
    },
    # ------------------------------------------------------------------ tasa de inversión
    "g-tasa-inversion": {
        "es": {
            "que": "Mide qué parte de todo lo que produce el país se destina a inversión fija: construcción de vivienda y obras, maquinaria y equipo, y propiedad intelectual (software, investigación). Es la formación bruta de capital fijo (FBKF) como porcentaje del PIB, ambos en pesos corrientes y sumando los últimos 12 meses. Cuenta la historia del esfuerzo de inversión del país: su ascenso durante el auge de materias primas y su retroceso posterior.",
            "leer": "Eje vertical en % del PIB, una sola línea verde con toda la historia disponible. Cada punto es el cociente entre la inversión fija y el PIB de los cuatro trimestres terminados en ese trimestre, a precios corrientes. La escala vertical se ajusta al rango de la serie, por lo que no empieza en cero: las variaciones se ven amplificadas. No incluye la variación de existencias (inventarios).",
            "importa": "La inversión de hoy es el capital con que se producirá en el futuro: una tasa de inversión baja limita el crecimiento potencial, la productividad y la generación de empleo de calidad. Para un inversionista, es un indicador estructural del atractivo y la confianza empresarial, y se vincula con la demanda de crédito, las importaciones de bienes de capital y la construcción.",
            "interpretar": [
                "Una tasa que sube indica que una parte mayor del ingreso se dedica a ampliar capacidad; si baja de forma sostenida, la economía acumula menos capital.",
                "Al estar en pesos corrientes, la tasa depende también de precios relativos: si los bienes de capital (muchos importados) se encarecen con la devaluación, la tasa puede subir sin más inversión real. El gráfico por tipo de activo muestra los volúmenes reales.",
                "La suma de 12 meses elimina la estacionalidad pero hace que los giros aparezcan con algunos trimestres de rezago.",
                "La tasa de inversión de Colombia se suele comparar con la de otras economías emergentes; las diferencias metodológicas entre países deben considerarse.",
            ],
            "formulas": [
                ["Tasa de inversión", "TI<sub>t</sub> = (Σ<sub>k=0..3</sub> FBKF<sub>t−k</sub> ÷ Σ<sub>k=0..3</sub> PIB<sub>t−k</sub>) × 100", "FBKF y PIB a precios corrientes (billones de pesos)"],
            ],
        },
        "en": {
            "que": "Measures what share of everything the country produces goes to fixed investment: housing and civil works, machinery and equipment, and intellectual property (software, research). It is gross fixed capital formation (GFCF) as a percentage of GDP, both in current pesos and summed over the last 12 months. It tells the story of the country's investment effort: its rise during the commodity boom and its subsequent retreat.",
            "leer": "Vertical axis in % of GDP, a single green line with the full available history. Each point is the ratio of fixed investment to GDP over the four quarters ending in that quarter, at current prices. The vertical scale fits the series' range and does not start at zero, so movements look amplified. Inventory changes are excluded.",
            "importa": "Today's investment is the capital with which output will be produced later: a low investment rate limits potential growth, productivity and quality job creation. For an investor it is a structural gauge of business confidence and attractiveness, linked to credit demand, capital-goods imports and construction.",
            "interpretar": [
                "A rising rate means a larger share of income goes to expanding capacity; a sustained fall means the economy accumulates less capital.",
                "Because it is in current pesos, the rate also reflects relative prices: if capital goods (many imported) become dearer with depreciation, the rate can rise without more real investment. The asset-type chart shows real volumes.",
                "The 12-month sum removes seasonality but makes turning points appear a few quarters late.",
                "Colombia's investment rate is often compared with other emerging economies; methodological differences across countries should be kept in mind.",
            ],
            "formulas": [
                ["Investment rate", "IR<sub>t</sub> = (Σ<sub>k=0..3</sub> GFCF<sub>t−k</sub> ÷ Σ<sub>k=0..3</sub> GDP<sub>t−k</sub>) × 100", "GFCF and GDP at current prices (trillions of pesos)"],
            ],
        },
    },
    # ------------------------------------------------------------------ inversión por activo
    "g-inversion-activos": {
        "es": {
            "que": "Sigue el volumen real de la inversión fija por tipo de activo y lo compara con el nivel de finales de 2019, el último trimestre antes de la pandemia. Separa cuatro destinos: maquinaria y equipo, vivienda, otros edificios y obras civiles (carreteras, infraestructura, edificaciones no residenciales) y propiedad intelectual. Muestra qué tipos de inversión ya recuperaron su nivel previo y cuáles siguen rezagados.",
            "leer": "Eje vertical: índice con 2019T4 = 100, desde 2015. Línea azul: maquinaria y equipo (códigos AN113 + AN114 del Sistema de Cuentas Nacionales); naranja: vivienda (AN111); verde: otros edificios y obras (AN112); morada: propiedad intelectual (AN117). Todas son volúmenes desestacionalizados (cuadro 6 del anexo de gasto del DANE). La línea punteada en 100 es el nivel previo a la pandemia: por encima, el activo ya lo superó; por debajo, aún no.",
            "importa": "No toda la inversión tiene el mismo efecto: la maquinaria y la propiedad intelectual elevan la productividad, la vivienda atiende la demanda de los hogares y las obras civiles dependen en gran parte de la infraestructura pública y las concesiones. Saber cuál se recupera y cuál no ayuda a leer la capacidad productiva futura y el desempeño de sectores como construcción, cemento, importadores de bienes de capital y banca hipotecaria.",
            "interpretar": [
                "Una línea que se mantiene por debajo de 100 indica que ese tipo de inversión aún no recupera el volumen previo a la pandemia; la distancia mide el rezago en %.",
                "La maquinaria y equipo es sensible a la tasa de cambio, porque buena parte se importa; la vivienda, a las tasas hipotecarias y a los subsidios; las obras civiles, a la ejecución pública.",
                "El índice muestra el nivel relativo a una fecha, no el crecimiento anual; una línea que sube indica aumento del volumen, aunque siga por debajo de 100.",
                "Las series desestacionalizadas se reestiman con cada publicación y pueden cambiar trimestres anteriores.",
            ],
            "formulas": [
                ["Índice por activo", "I<sub>j,t</sub> = 100 × K<sub>j,t</sub> ÷ K<sub>j,2019T4</sub>", "K<sub>j,t</sub> = formación bruta de capital fijo real desestacionalizada del activo j en el trimestre t"],
            ],
        },
        "en": {
            "que": "Tracks the real volume of fixed investment by asset type and compares it with the end-2019 level, the last quarter before the pandemic. It separates four destinations: machinery and equipment, housing, other buildings and civil works (roads, infrastructure, non-residential buildings) and intellectual property. It shows which types of investment have regained their earlier level and which are still lagging.",
            "leer": "Vertical axis: index with 2019Q4 = 100, from 2015. Blue line: machinery and equipment (System of National Accounts codes AN113 + AN114); orange: housing (AN111); green: other buildings and works (AN112); purple: intellectual property (AN117). All are seasonally adjusted volumes (table 6 of DANE's expenditure annex). The dotted line at 100 is the pre-pandemic level: above it, the asset has surpassed it; below, not yet.",
            "importa": "Not all investment has the same effect: machinery and intellectual property raise productivity, housing serves household demand and civil works depend largely on public infrastructure and concessions. Knowing which recovers and which does not helps read future productive capacity and the performance of construction, cement, capital-goods importers and mortgage lending.",
            "interpretar": [
                "A line staying below 100 means that investment type has not regained its pre-pandemic volume; the distance measures the shortfall in %.",
                "Machinery and equipment is sensitive to the exchange rate, since much is imported; housing to mortgage rates and subsidies; civil works to public spending execution.",
                "The index shows the level relative to one date, not annual growth; a rising line means volume is increasing even if it remains below 100.",
                "Seasonally adjusted series are re-estimated with each release and can change earlier quarters.",
            ],
            "formulas": [
                ["Asset index", "I<sub>j,t</sub> = 100 × K<sub>j,t</sub> ÷ K<sub>j,2019Q4</sub>", "K<sub>j,t</sub> = seasonally adjusted real gross fixed capital formation in asset j, quarter t"],
            ],
        },
    },
    # ------------------------------------------------------------------ consumo por durabilidad
    "g-consumo-durabilidad": {
        "es": {
            "que": "Divide el consumo de los hogares en cuatro tipos según su durabilidad: bienes durables (vehículos, electrodomésticos, muebles), semidurables (ropa, calzado), no durables (alimentos, combustibles) y servicios. Cada tipo responde de forma distinta al ciclo: los durables son los más sensibles al ingreso, al crédito y a la confianza, mientras que los no durables y los servicios básicos son más estables.",
            "leer": "Eje en %, desde 2015. Cada línea es la variación real de los últimos 12 meses frente a los 12 anteriores (suma de cuatro trimestres, volúmenes en datos originales, cuadro 3 del anexo de gasto del DANE). Azul: servicios; naranja: bienes durables; verde: no durables; morada: semidurables. La línea en cero separa crecimiento de caída. Para conservar la escala, los valores se recortan entre −30% y 40%, lo que afecta sobre todo a 2020–2021.",
            "importa": "El consumo de los hogares es el componente más grande del PIB. Su composición revela la confianza de los hogares y el papel del crédito: un auge de durables suele ir de la mano de crédito de consumo y tasas bajas, y su caída es una de las primeras señales de enfriamiento. Para un inversionista es información directa sobre comercio, vehículos, bienes de consumo y la cartera de consumo de los bancos.",
            "interpretar": [
                "Los durables oscilan mucho más que el resto: caídas de dos dígitos son habituales en desaceleraciones y alzas fuertes en recuperaciones.",
                "Si los servicios crecen mientras los bienes se estancan, el consumo se está desplazando hacia actividades como restaurantes, turismo o entretenimiento.",
                "La medida de 12 meses es suave y reacciona con rezago: un giro reciente tarda varios trimestres en reflejarse por completo.",
                "Las tasas de política del Banco de la República y las de crédito de consumo (página de tasas) ayudan a interpretar el comportamiento de los durables.",
            ],
            "formulas": [
                ["Variación de 12 meses", "g<sub>12m,t</sub> = (Σ<sub>k=0..3</sub> C<sub>t−k</sub> ÷ Σ<sub>k=4..7</sub> C<sub>t−k</sub> − 1) × 100", "C = consumo real de los hogares del grupo de durabilidad (datos originales)"],
                ["Recorte gráfico", "valor dibujado = min(40; max(−30; g<sub>12m</sub>))", "afecta sobre todo a 2020–2021; el valor real puede ser más extremo"],
            ],
        },
        "en": {
            "que": "Splits household consumption into four types by durability: durable goods (vehicles, appliances, furniture), semi-durables (clothing, footwear), non-durables (food, fuel) and services. Each type responds differently to the cycle: durables are the most sensitive to income, credit and confidence, while non-durables and basic services are steadier.",
            "leer": "Axis in %, from 2015. Each line is the real change of the last 12 months versus the previous 12 (sum of four quarters, unadjusted volumes, table 3 of DANE's expenditure annex). Blue: services; orange: durable goods; green: non-durables; purple: semi-durables. The zero line separates growth from decline. To keep the scale, values are capped between −30% and 40%, which mainly affects 2020–2021.",
            "importa": "Household consumption is the largest component of GDP. Its mix reveals household confidence and the role of credit: a durables boom usually goes hand in hand with consumer credit and low rates, and a drop in durables is one of the first signs of cooling. For an investor it is direct information on retail, vehicles, consumer goods and banks' consumer loan books.",
            "interpretar": [
                "Durables swing far more than the rest: double-digit falls are common in slowdowns and sharp rises in recoveries.",
                "If services grow while goods stall, consumption is shifting towards activities such as restaurants, tourism or entertainment.",
                "The 12-month measure is smooth and lags: a recent turn takes several quarters to show fully.",
                "Banco de la República's policy rate and consumer lending rates (rates page) help interpret the behaviour of durables.",
            ],
            "formulas": [
                ["12-month change", "g<sub>12m,t</sub> = (Σ<sub>k=0..3</sub> C<sub>t−k</sub> ÷ Σ<sub>k=4..7</sub> C<sub>t−k</sub> − 1) × 100", "C = real household consumption in the durability group (unadjusted)"],
                ["Display cap", "plotted value = min(40; max(−30; g<sub>12m</sub>))", "mainly affects 2020–2021; the actual value may be more extreme"],
            ],
        },
    },
    # ------------------------------------------------------------------ consumo por finalidad
    "g-consumo-finalidad": {
        "es": {
            "que": "Clasifica el gasto de los hogares según su finalidad, siguiendo la Clasificación del Consumo Individual por Finalidades (COICOP) de Naciones Unidas: alimentos, vivienda y servicios públicos, transporte, salud, educación, restaurantes y hoteles, entre otros, 12 grupos en total. Muestra en qué rubros los hogares están gastando más y en cuáles menos, en términos reales, durante el último año.",
            "leer": "Eje horizontal en %: variación real de los últimos 12 meses frente a los 12 anteriores, con volúmenes en datos originales (cuadro 3 del anexo de gasto del DANE). Las barras están ordenadas de menor (abajo) a mayor (arriba) crecimiento; azul si crece y naranja si cae, con el valor escrito al final. Entre paréntesis, junto al nombre, la participación aproximada de cada grupo en el consumo total de los últimos 12 meses. La línea vertical marca el cero.",
            "importa": "La composición del gasto refleja prioridades y presiones de los hogares: si crecen sobre todo los rubros esenciales mientras caen los discrecionales, el consumo se está ajustando. Para un inversionista, la información orienta sobre sectores como comercio de alimentos, restaurantes, turismo, transporte o comunicaciones, y complementa la lectura de la inflación por grupos de gasto.",
            "interpretar": [
                "Combine crecimiento y participación: un grupo con peso alto, como alimentos o vivienda, mueve mucho más el consumo total que uno pequeño que crece rápido.",
                "Los rubros discrecionales (recreación, restaurantes y hoteles, muebles) suelen ser los primeros en ajustarse cuando el ingreso se debilita.",
                "La participación se calcula con volúmenes encadenados, que no son aditivos: es una aproximación útil para ordenar, no un dato exacto.",
                "Es una variación real: un rubro con precios al alza puede mostrar un gasto en pesos mayor y, aun así, un volumen menor.",
            ],
            "formulas": [
                ["Variación de 12 meses", "g<sub>j</sub> = (Σ<sub>k=0..3</sub> C<sub>j,t−k</sub> ÷ Σ<sub>k=4..7</sub> C<sub>j,t−k</sub> − 1) × 100", "C<sub>j</sub> = consumo real de los hogares en la finalidad COICOP j"],
                ["Participación aproximada", "s<sub>j</sub> = Σ<sub>k=0..3</sub> C<sub>j,t−k</sub> ÷ Σ<sub>i</sub> Σ<sub>k=0..3</sub> C<sub>i,t−k</sub> × 100", "suma de volúmenes encadenados de los 12 grupos en los últimos 4 trimestres"],
            ],
        },
        "en": {
            "que": "Classifies household spending by purpose, following the United Nations Classification of Individual Consumption According to Purpose (COICOP): food, housing and utilities, transport, health, education, restaurants and hotels, among others, 12 groups in all. It shows which items households are spending more on and which less, in real terms, over the past year.",
            "leer": "Horizontal axis in %: real change of the last 12 months versus the previous 12, using unadjusted volumes (table 3 of DANE's expenditure annex). Bars are sorted from lowest (bottom) to highest (top) growth; blue if growing and orange if falling, with the value at the end. In brackets next to the name is each group's approximate share of total consumption over the last 12 months. The vertical line marks zero.",
            "importa": "The spending mix reflects household priorities and pressures: if essentials grow while discretionary items fall, consumption is adjusting. For an investor it points to sectors such as food retail, restaurants, tourism, transport or communications, and complements the reading of inflation by spending group.",
            "interpretar": [
                "Combine growth and share: a heavyweight group such as food or housing moves total consumption much more than a small group growing fast.",
                "Discretionary items (recreation, restaurants and hotels, furnishings) are usually the first to adjust when income weakens.",
                "Shares are computed from chain-linked volumes, which are not additive: a useful approximation for ranking, not an exact figure.",
                "This is a real change: an item with rising prices can show higher peso spending and still a lower volume.",
            ],
            "formulas": [
                ["12-month change", "g<sub>j</sub> = (Σ<sub>k=0..3</sub> C<sub>j,t−k</sub> ÷ Σ<sub>k=4..7</sub> C<sub>j,t−k</sub> − 1) × 100", "C<sub>j</sub> = real household consumption for COICOP purpose j"],
                ["Approximate share", "s<sub>j</sub> = Σ<sub>k=0..3</sub> C<sub>j,t−k</sub> ÷ Σ<sub>i</sub> Σ<sub>k=0..3</sub> C<sub>i,t−k</sub> × 100", "sum of chain-linked volumes of the 12 groups over the last 4 quarters"],
            ],
        },
    },
    # ------------------------------------------------------------------ PIB por persona, real
    "g-pib-persona": {
        "es": {
            "que": "Mide cuánto creció la producción por habitante, descontando la inflación, en cada año calendario completo. Como la población también crece, el PIB por persona avanza menos que el PIB total: la diferencia es aproximadamente el crecimiento demográfico. Es la medida más directa de si el nivel de vida material promedio mejora o se estanca.",
            "leer": "Eje vertical en %: crecimiento del PIB real por persona frente al año anterior. Cada barra es un año completo (solo años con sus cuatro trimestres publicados); azul si creció y naranja si cayó, con el valor encima. Al pasar el cursor se ve el nivel del PIB por persona en millones de pesos constantes de 2015. La línea horizontal marca el cero. La población es la total nacional a mitad de año según las estimaciones oficiales del DANE basadas en el Censo 2018.",
            "importa": "Un PIB que crece al mismo ritmo que la población deja el ingreso promedio estancado. Para comparar el progreso económico entre países o periodos, y para entender el potencial de consumo por habitante, el PIB por persona es más relevante que el total. También ayuda a separar el efecto del crecimiento demográfico, incluido el aporte de la migración, del avance genuino de la producción.",
            "interpretar": [
                "La diferencia entre el crecimiento del PIB total y el del PIB por persona es aproximadamente la tasa de crecimiento de la población.",
                "Cambios en las estimaciones de población del DANE modifican toda la serie por persona aunque el PIB no cambie; la actualización vigente reemplaza las anteriores.",
                "El PIB por persona es un promedio: no informa sobre la distribución del ingreso ni sobre la informalidad.",
                "Antes de 2018 la población es una retroestimación del DANE, consistente con el censo, pero sujeta a mayor incertidumbre.",
            ],
            "formulas": [
                ["PIB real por persona", "y<sub>A</sub> = Σ<sub>q∈A</sub> Y<sub>q</sub> ÷ P<sub>A</sub>", "Y<sub>q</sub> = PIB real del trimestre q (pesos de 2015); P<sub>A</sub> = población total nacional a mitad del año A"],
                ["Crecimiento anual", "g<sub>A</sub> = (y<sub>A</sub> ÷ y<sub>A−1</sub> − 1) × 100", "y<sub>A</sub> = PIB real por persona del año A"],
                ["Descomposición aproximada", "g<sub>y</sub> ≈ g<sub>PIB</sub> − g<sub>P</sub>", "g<sub>P</sub> = crecimiento de la población"],
            ],
        },
        "en": {
            "que": "Measures how much output per inhabitant grew, net of inflation, in each full calendar year. Because the population also grows, GDP per person rises less than total GDP: the difference is roughly population growth. It is the most direct gauge of whether average material living standards are improving or stagnating.",
            "leer": "Vertical axis in %: growth of real GDP per person versus the previous year. Each bar is a full year (only years with all four quarters published); blue if it grew and orange if it fell, with the value on top. Hovering shows the level of GDP per person in millions of constant 2015 pesos. The horizontal line marks zero. Population is the national mid-year total from DANE's official estimates based on the 2018 Census.",
            "importa": "GDP growing at the same pace as population leaves average income flat. To compare economic progress across countries or periods, and to gauge consumption potential per inhabitant, GDP per person matters more than the total. It also separates the effect of population growth, including migration, from genuine output gains.",
            "interpretar": [
                "The difference between total GDP growth and per-person growth is roughly the population growth rate.",
                "Changes in DANE's population estimates alter the whole per-person series even if GDP does not change; the current update replaces earlier ones.",
                "GDP per person is an average: it says nothing about income distribution or informality.",
                "Before 2018 population is a DANE back-estimate, consistent with the census but subject to more uncertainty.",
            ],
            "formulas": [
                ["Real GDP per person", "y<sub>A</sub> = Σ<sub>q∈A</sub> Y<sub>q</sub> ÷ P<sub>A</sub>", "Y<sub>q</sub> = real GDP in quarter q (2015 pesos); P<sub>A</sub> = national population at mid-year A"],
                ["Annual growth", "g<sub>A</sub> = (y<sub>A</sub> ÷ y<sub>A−1</sub> − 1) × 100", "y<sub>A</sub> = real GDP per person in year A"],
                ["Approximate breakdown", "g<sub>y</sub> ≈ g<sub>GDP</sub> − g<sub>P</sub>", "g<sub>P</sub> = population growth"],
            ],
        },
    },
    # ------------------------------------------------------------------ PIB por persona en dólares
    "g-pib-persona-usd": {
        "es": {
            "que": "Expresa el PIB por habitante en dólares corrientes, convirtiendo el PIB nominal en pesos con la tasa de cambio promedio de cada año. Es la cifra que suele usarse en comparaciones internacionales de ingreso. A diferencia del gráfico en pesos constantes, mezcla tres fuerzas: el crecimiento real, la inflación interna y el valor del peso frente al dólar.",
            "leer": "Eje vertical en dólares estadounidenses por persona; cada barra es un año calendario completo y su etiqueta muestra el valor en miles de dólares. El cálculo divide el PIB nominal anual (suma de cuatro trimestres, en pesos corrientes) entre la población a mitad de año y entre el promedio anual de la Tasa Representativa del Mercado (TRM), el tipo de cambio oficial peso-dólar que publica el Banco de la República. No se aplica el método Atlas del Banco Mundial.",
            "importa": "Para un inversionista extranjero, el PIB por persona en dólares aproxima el tamaño del mercado por consumidor en su propia moneda y el poder de compra internacional del país. Sus oscilaciones, sin embargo, dependen mucho de la tasa de cambio: años con devaluación fuerte muestran caídas en dólares aunque la economía crezca en términos reales.",
            "interpretar": [
                "Si el dato en dólares cae mientras el PIB real por persona crece, la causa es la depreciación del peso; si sube más que el real, influyen la inflación y la apreciación.",
                "No ajusta por paridad de poder adquisitivo (PPA): no refleja que en Colombia muchos bienes y servicios son más baratos que en EE. UU.",
                "Como usa la TRM promedio del año, una devaluación concentrada al final del año se refleja solo en parte.",
                "Compárelo con el crecimiento real por persona y con la página de la tasa de cambio para separar las tres fuerzas.",
            ],
            "formulas": [
                ["PIB por persona en dólares", "PIB<sub>USD,A</sub> = Σ<sub>q∈A</sub> N<sub>q</sub> ÷ P<sub>A</sub> ÷ TRM̄<sub>A</sub>", "N = PIB nominal en pesos; P = población a mitad de año; TRM̄ = promedio de la TRM diaria del año calendario"],
                ["Descomposición aproximada", "Δ% PIB<sub>USD</sub> ≈ g<sub>real por persona</sub> + π<sub>deflactor</sub> − Δ% TRM̄", "en tasas anuales; aproximación de primer orden"],
            ],
        },
        "en": {
            "que": "Expresses GDP per inhabitant in current US dollars, converting nominal GDP in pesos at each year's average exchange rate. It is the figure usually used in international income comparisons. Unlike the constant-peso chart, it blends three forces: real growth, domestic inflation and the peso's value against the dollar.",
            "leer": "Vertical axis in US dollars per person; each bar is a full calendar year and its label shows the value in thousands of dollars. The calculation divides annual nominal GDP (sum of four quarters, current pesos) by mid-year population and by the annual average of the Representative Market Rate (TRM), the official peso-dollar exchange rate published by Banco de la República. The World Bank Atlas method is not applied.",
            "importa": "For a foreign investor, GDP per person in dollars approximates market size per consumer in their own currency and the country's international purchasing power. Its swings, however, depend heavily on the exchange rate: years of sharp depreciation show falls in dollars even when the economy grows in real terms.",
            "interpretar": [
                "If the dollar figure falls while real GDP per person grows, the cause is peso depreciation; if it rises faster than real growth, inflation and appreciation play a part.",
                "It does not adjust for purchasing power parity (PPP): it does not reflect that many goods and services are cheaper in Colombia than in the US.",
                "Because it uses the year's average TRM, depreciation concentrated at year-end is only partly reflected.",
                "Compare it with real growth per person and with the exchange-rate page to separate the three forces.",
            ],
            "formulas": [
                ["GDP per person in dollars", "GDP<sub>USD,A</sub> = Σ<sub>q∈A</sub> N<sub>q</sub> ÷ P<sub>A</sub> ÷ TRM̄<sub>A</sub>", "N = nominal GDP in pesos; P = mid-year population; TRM̄ = average of the daily TRM over the calendar year"],
                ["Approximate breakdown", "Δ% GDP<sub>USD</sub> ≈ g<sub>real per person</sub> + π<sub>deflator</sub> − Δ% TRM̄", "annual rates; first-order approximation"],
            ],
        },
    },
    # ------------------------------------------------------------------ productividad laboral
    "g-productividad": {
        "es": {
            "que": "Compara la evolución de la producción y del empleo y, a partir de ambas, la producción por persona ocupada, llamada productividad laboral aparente (OCDE, 2001). Si el PIB crece más que el número de ocupados, cada trabajador produce en promedio más; si el empleo crece más rápido que la producción, la productividad por ocupado cae. Es una lectura directa de la eficiencia con que la economía usa su fuerza laboral.",
            "leer": "Eje vertical: índices con promedio de 2015 = 100, desde 2015. Línea azul: PIB real de los últimos 12 meses (suma de cuatro trimestres). Línea naranja: ocupados, promedio de 12 meses de la Gran Encuesta Integrada de Hogares (GEIH) del DANE, serie desestacionalizada. Línea verde, más gruesa: el cociente entre ambos, PIB por ocupado. La línea punteada en 100 es el nivel promedio de 2015.",
            "importa": "La productividad es el determinante de largo plazo de los salarios reales y del crecimiento potencial: sin ella, el PIB solo crece si crece el empleo. Para un inversionista, una productividad estancada limita el margen para subir salarios sin presionar costos, y una productividad al alza sostiene la rentabilidad y la competitividad externa.",
            "interpretar": [
                "Verde al alza: la producción crece más que el empleo; verde a la baja: el empleo crece más rápido que la producción, algo frecuente cuando se crean puestos en actividades de baja productividad.",
                "Es productividad aparente: no corrige por horas trabajadas, por informalidad ni por el capital disponible, de modo que mezcla eficiencia con composición del empleo.",
                "Los cambios metodológicos o de marco muestral de la GEIH pueden generar saltos en los ocupados que no reflejan cambios económicos.",
                "Compárela con la página de empleo y con el crecimiento por sector para ver qué actividades explican los movimientos.",
            ],
            "formulas": [
                ["Índice del PIB", "I<sup>Y</sup><sub>t</sub> = 100 × Y<sup>4</sup><sub>t</sub> ÷ Ȳ<sup>4</sup><sub>2015</sub>", "Y<sup>4</sup><sub>t</sub> = suma del PIB real de los trimestres t−3 a t; Ȳ<sup>4</sup><sub>2015</sub> = promedio de esa suma en 2015"],
                ["Índice de ocupados", "I<sup>E</sup><sub>t</sub> = 100 × E<sup>12</sup><sub>t</sub> ÷ Ē<sup>12</sup><sub>2015</sub>", "E<sup>12</sup><sub>t</sub> = promedio de ocupados desestacionalizados de los últimos 12 meses"],
                ["PIB por ocupado", "I<sup>P</sup><sub>t</sub> = 100 × I<sup>Y</sup><sub>t</sub> ÷ I<sup>E</sup><sub>t</sub>", "productividad laboral aparente, 2015 = 100"],
            ],
        },
        "en": {
            "que": "Compares the paths of output and employment and, from both, output per employed person, known as apparent labour productivity (OECD, 2001). If GDP grows faster than the number of employed people, each worker produces more on average; if employment grows faster than output, productivity per worker falls. It is a direct reading of how efficiently the economy uses its workforce.",
            "leer": "Vertical axis: indices with 2015 average = 100, from 2015. Blue line: real GDP over the last 12 months (sum of four quarters). Orange line: employed people, 12-month average from DANE's Integrated Household Survey (GEIH), seasonally adjusted. Thicker green line: the ratio of the two, GDP per employed person. The dotted line at 100 is the 2015 average level.",
            "importa": "Productivity is the long-run driver of real wages and potential growth: without it, GDP grows only if employment grows. For an investor, stagnant productivity limits room for wage increases without cost pressure, while rising productivity supports profitability and external competitiveness.",
            "interpretar": [
                "Green rising: output grows faster than employment; green falling: employment grows faster than output, common when jobs are created in low-productivity activities.",
                "This is apparent productivity: it does not adjust for hours worked, informality or available capital, so it mixes efficiency with the composition of employment.",
                "Methodological or sampling-frame changes in the GEIH can create jumps in employment that do not reflect economic change.",
                "Compare it with the employment page and with growth by sector to see which activities explain the movements.",
            ],
            "formulas": [
                ["GDP index", "I<sup>Y</sup><sub>t</sub> = 100 × Y<sup>4</sup><sub>t</sub> ÷ Ȳ<sup>4</sup><sub>2015</sub>", "Y<sup>4</sup><sub>t</sub> = sum of real GDP over quarters t−3 to t; Ȳ<sup>4</sup><sub>2015</sub> = average of that sum in 2015"],
                ["Employment index", "I<sup>E</sup><sub>t</sub> = 100 × E<sup>12</sup><sub>t</sub> ÷ Ē<sup>12</sup><sub>2015</sub>", "E<sup>12</sup><sub>t</sub> = 12-month average of seasonally adjusted employment"],
                ["GDP per employed person", "I<sup>P</sup><sub>t</sub> = 100 × I<sup>Y</sup><sub>t</sub> ÷ I<sup>E</sup><sub>t</sub>", "apparent labour productivity, 2015 = 100"],
            ],
        },
    },
    # ------------------------------------------------------------------ nivel frente al camino previo
    "g-nivel": {
        "es": {
            "que": "Compara el tamaño de la economía con el que habría tenido si hubiera mantenido el ritmo de crecimiento de 2015–2019. No mira tasas sino niveles: aunque la economía haya vuelto a crecer después de 2020, puede seguir por debajo del camino que traía, es decir, con una pérdida permanente de producción. La literatura sobre crisis (Cerra y Saxena, 2008) documenta que estas pérdidas de nivel son frecuentes.",
            "leer": "Eje vertical: índice del PIB real desestacionalizado con 2019T4 = 100, desde 2015. Línea azul: PIB observado. Línea gris punteada: camino de 2015–2019, una tendencia log-lineal ajustada a esos 20 trimestres y extendida con la misma pendiente; es un contrafactual descriptivo, no una estimación de lo que vendrá. La línea horizontal en 100 marca el tamaño de la economía antes de la pandemia.",
            "importa": "Las tasas de crecimiento altas tras una crisis pueden ocultar que la economía no ha recuperado lo perdido. La distancia frente al camino previo resume cuánta producción, ingreso y empleo dejó de generarse, y es relevante para evaluar el tamaño del mercado, la sostenibilidad fiscal y la discusión sobre si la capacidad productiva se redujo de forma duradera (histéresis).",
            "interpretar": [
                "Azul por debajo de la línea punteada: la economía es más pequeña de lo que habría sido con el ritmo previo; la distancia, en %, es la pérdida de nivel. Por encima: ya superó ese camino.",
                "Que la azul esté sobre 100 solo indica que la economía es mayor que a finales de 2019, no que haya recuperado su tendencia.",
                "El camino depende del periodo elegido: 2015–2019 incluye la desaceleración tras la caída del petróleo; con otro periodo, la pendiente y la brecha serían diferentes.",
                "Las revisiones del DANE y del ajuste estacional pueden mover tanto el índice como la pendiente estimada.",
            ],
            "formulas": [
                ["Índice del PIB", "I<sub>t</sub> = 100 × S<sub>t</sub> ÷ S<sub>2019T4</sub>", "S = PIB real desestacionalizado"],
                ["Tendencia 2015–2019", "ln S<sub>t</sub> = b<sub>0</sub> + b<sub>1</sub> × k + ε<sub>t</sub>;  Ŝ<sub>k</sub> = e<sup>b<sub>0</sub> + b<sub>1</sub> × k</sup>", "k = 0, 1, 2… trimestres desde 2015T1; b<sub>0</sub>, b<sub>1</sub> por mínimos cuadrados con 2015T1–2019T4"],
                ["Ritmo anual del camino", "g<sub>tend</sub> = (e<sup>4 × b<sub>1</sub></sup> − 1) × 100", "crecimiento anual implícito en la pendiente trimestral"],
                ["Distancia al camino", "B<sub>t</sub> = (S<sub>t</sub> ÷ Ŝ<sub>t</sub> − 1) × 100", "negativa: nivel por debajo del camino previo"],
            ],
        },
        "en": {
            "que": "Compares the size of the economy with what it would have been had it kept its 2015–2019 growth pace. It looks at levels rather than rates: even if the economy has grown again since 2020, it may remain below its earlier path, meaning a permanent loss of output. The literature on crises (Cerra and Saxena, 2008) documents that such level losses are common.",
            "leer": "Vertical axis: index of seasonally adjusted real GDP with 2019Q4 = 100, from 2015. Blue line: observed GDP. Grey dotted line: the 2015–2019 path, a log-linear trend fitted to those 20 quarters and extended with the same slope; it is a descriptive counterfactual, not a statement about the future. The horizontal line at 100 marks the size of the economy before the pandemic.",
            "importa": "High growth rates after a crisis can hide that the economy has not recovered what it lost. The distance from the earlier path summarises how much output, income and employment went missing, and matters for assessing market size, fiscal sustainability and whether productive capacity has been durably reduced (hysteresis).",
            "interpretar": [
                "Blue below the dotted line: the economy is smaller than it would have been at the earlier pace; the distance, in %, is the level loss. Above it: the path has been surpassed.",
                "Blue above 100 only means the economy is larger than at end-2019, not that it has regained its trend.",
                "The path depends on the chosen period: 2015–2019 includes the slowdown after the oil-price fall; a different window would give a different slope and gap.",
                "DANE revisions and seasonal-adjustment updates can move both the index and the estimated slope.",
            ],
            "formulas": [
                ["GDP index", "I<sub>t</sub> = 100 × S<sub>t</sub> ÷ S<sub>2019Q4</sub>", "S = seasonally adjusted real GDP"],
                ["2015–2019 trend", "ln S<sub>t</sub> = b<sub>0</sub> + b<sub>1</sub> × k + ε<sub>t</sub>;  Ŝ<sub>k</sub> = e<sup>b<sub>0</sub> + b<sub>1</sub> × k</sup>", "k = 0, 1, 2… quarters since 2015Q1; b<sub>0</sub>, b<sub>1</sub> by least squares over 2015Q1–2019Q4"],
                ["Annual pace of the path", "g<sub>trend</sub> = (e<sup>4 × b<sub>1</sub></sup> − 1) × 100", "annual growth implied by the quarterly slope"],
                ["Distance to the path", "B<sub>t</sub> = (S<sub>t</sub> ÷ Ŝ<sub>t</sub> − 1) × 100", "negative: level below the earlier path"],
            ],
        },
    },
}
