"""Lupas (explicaciones de cada gráfico) del grupo g6: comercio exterior de bienes (página Comercio: flujos, balanza,
canasta exportadora, importaciones por uso, socios, precio y volumen, apertura y diversificación) y cuentas externas y
fiscales (página Externo: cuenta corriente, financiación, IED, remesas, deuda externa, PII y cuentas del Gobierno).
Español e inglés."""

LUPAS = {
    # =========================================================================================== COMERCIO
    "g-comercio-flujos": {
        "es": {
            "que": "Muestra cuánto vende Colombia al resto del mundo (exportaciones de bienes) y cuánto le compra (importaciones), sumando siempre los últimos 12 meses. La distancia entre las dos líneas es la balanza comercial de bienes. La historia que cuenta es la del ciclo de las materias primas: las exportaciones suben y bajan con el precio del petróleo y del carbón, mientras las importaciones siguen más de cerca a la demanda interna y a la inversión. Se ven, por ejemplo, el desplome de ambas en 2020 y el rebote posterior.",
            "leer": "Eje vertical en miles de millones de dólares corrientes, desde cero. Línea azul: exportaciones FOB (valor de la mercancía en el puerto colombiano, sin fletes ni seguros); línea naranja: importaciones CIF (incluyen costo, seguro y flete hasta Colombia). Cada punto es la suma de los 12 meses que terminan en ese mes. Las exportaciones arrancan en los años noventa; las importaciones, cuando empieza la serie mensual del DANE disponible en el sitio. Cuando la naranja va por encima de la azul hay déficit comercial.",
            "importa": "El comercio de bienes es la principal fuente de dólares de la economía y el componente más grande de la cuenta corriente. Un déficit comercial amplio debe cubrirse con inversión extranjera, endeudamiento externo o remesas, y su tamaño influye en la tasa de cambio. Para un inversionista, las exportaciones indican el ingreso externo del país y de los sectores minero-energéticos; las importaciones reflejan el pulso del consumo de bienes durables y de la compra de maquinaria.",
            "interpretar": [
                "Si la brecha entre la línea naranja y la azul se amplía, el déficit comercial crece y el país necesita más financiación externa; si se cierra, depende menos de ella.",
                "Las exportaciones pueden caer solo por menores precios internacionales, sin que se venda menos cantidad: compárelo con el gráfico de valor, precio y volumen.",
                "La suma de 12 meses elimina la estacionalidad sin modelos, pero reacciona con rezago: un cambio fuerte de un mes tarda en verse completo.",
                "Las cifras son en dólares corrientes, sin ajuste por inflación externa; los últimos meses son provisionales y el DANE los revisa.",
                "Esta balanza (FOB menos CIF) es algo más negativa que la de bienes de la balanza de pagos de la página Externo, que valora ambas en FOB."
            ],
            "formulas": [
                ["Suma de 12 meses", "X12<sub>t</sub> = Σ<sub>j=0..11</sub> X<sub>t−j</sub>", "X = exportaciones (o importaciones) del mes; t = mes; resultado en miles de millones de dólares"],
                ["Balanza comercial de 12 meses", "B12<sub>t</sub> = X12<sub>t</sub> − M12<sub>t</sub>", "X12 = exportaciones FOB; M12 = importaciones CIF, ambas sumas de 12 meses"]
            ]
        },
        "en": {
            "que": "This chart shows how much Colombia sells to the rest of the world (goods exports) and how much it buys (imports), always adding up the last 12 months. The gap between the two lines is the goods trade balance. The story it tells is that of the commodity cycle: exports rise and fall with oil and coal prices, while imports track domestic demand and investment more closely. The 2020 collapse in both flows and the rebound that followed are clearly visible.",
            "leer": "Vertical axis in billions of current US dollars, starting at zero. Blue line: FOB exports (value of goods at the Colombian port, without freight or insurance); orange line: CIF imports (including cost, insurance and freight to Colombia). Each point is the sum of the 12 months ending in that month. Exports start in the 1990s; imports start where DANE's monthly series available on the site begins. When the orange line is above the blue one there is a trade deficit.",
            "importa": "Goods trade is the economy's main source of dollars and the largest item in the current account. A wide trade deficit must be covered by foreign investment, external borrowing or remittances, and its size bears on the exchange rate. For an investor, exports show the country's external income and the health of the mining and energy sectors; imports reflect the pulse of durable-goods consumption and machinery purchases.",
            "interpretar": [
                "If the gap between the orange and blue lines widens, the trade deficit grows and the country needs more external financing; if it narrows, it relies less on it.",
                "Exports can fall purely because of lower international prices, without lower quantities: compare with the value, price and volume chart.",
                "The 12-month sum removes seasonality without any model, but it lags: a sharp move in one month takes time to show fully.",
                "Figures are in current dollars, with no adjustment for foreign inflation; the latest months are provisional and revised by DANE.",
                "This balance (FOB minus CIF) is somewhat more negative than the goods balance in the balance of payments on the External page, which values both sides FOB."
            ],
            "formulas": [
                ["12-month sum", "X12<sub>t</sub> = Σ<sub>j=0..11</sub> X<sub>t−j</sub>", "X = monthly exports (or imports); t = month; result in billions of dollars"],
                ["12-month trade balance", "B12<sub>t</sub> = X12<sub>t</sub> − M12<sub>t</sub>", "X12 = FOB exports; M12 = CIF imports, both 12-month sums"]
            ]
        },
    },
    "g-balanza": {
        "es": {
            "que": "Resume, año por año, si Colombia vendió al exterior más bienes de los que compró (superávit) o menos (déficit). Permite ver de un vistazo los periodos en que la bonanza de precios de las materias primas dejó saldos cercanos a cero o positivos y el cambio de régimen tras la caída del precio del petróleo de mediados de la década pasada, desde la cual el saldo ha sido persistentemente negativo.",
            "leer": "Cada barra es un año calendario, en miles de millones de dólares: exportaciones FOB menos importaciones CIF, sumando los meses del año. Barras verdes: superávit; barras naranjas: déficit. La línea horizontal marca el cero. La serie empieza con el primer año en que hay datos mensuales de importaciones en el sitio. El último año aparece con la etiqueta «ene–mes» cuando está incompleto: suma solo de enero al último mes publicado y no es comparable con un año completo.",
            "importa": "El saldo comercial anual es la referencia más usada para describir la posición externa del país en bienes. Un déficit persistente implica una necesidad estructural de dólares que se cubre con capitales externos, y hace a la economía más sensible a los cambios en el apetito internacional por riesgo. Para un inversionista ayuda a dimensionar la presión sobre el peso y la dependencia del financiamiento externo.",
            "interpretar": [
                "Una barra naranja más larga que la del año anterior indica que el déficit se amplió; puede deberse a menores exportaciones, a mayores importaciones o a ambas: revise el gráfico de flujos de 12 meses.",
                "La barra parcial del año en curso debe compararse con el acumulado del mismo periodo del año anterior, no con el total anual.",
                "Como las importaciones incluyen flete y seguro (CIF), este saldo es algo más negativo que el de bienes de la balanza de pagos del Banco de la República, que usa FOB en ambos lados.",
                "Las cifras de los meses recientes son provisionales y pueden revisarse."
            ],
            "formulas": [
                ["Balanza anual", "B<sub>a</sub> = Σ<sub>m∈a</sub> X<sub>m</sub> − Σ<sub>m∈a</sub> M<sub>m</sub>", "X = exportaciones FOB; M = importaciones CIF; m = meses del año a (en el año en curso, solo los publicados)"]
            ]
        },
        "en": {
            "que": "This chart summarises, year by year, whether Colombia sold more goods abroad than it bought (surplus) or fewer (deficit). It shows at a glance the periods when the commodity price boom left balances close to zero or positive, and the regime change after the oil price fall of the middle of the last decade, since when the balance has been persistently negative.",
            "leer": "Each bar is a calendar year, in billions of dollars: FOB exports minus CIF imports, adding up the months of the year. Green bars: surplus; orange bars: deficit. The horizontal line marks zero. The series starts with the first year for which monthly import data are available on the site. The latest year is labelled 'Jan–month' when incomplete: it only adds January to the latest month published and is not comparable with a full year.",
            "importa": "The annual trade balance is the most widely used benchmark of the country's external position in goods. A persistent deficit implies a structural need for dollars that is met by foreign capital, and makes the economy more sensitive to shifts in global risk appetite. For an investor it helps size the pressure on the peso and the reliance on external financing.",
            "interpretar": [
                "An orange bar longer than the previous year's means the deficit widened; this may reflect lower exports, higher imports or both: check the 12-month flows chart.",
                "The partial bar for the current year should be compared with the same period of the previous year, not with the full-year total.",
                "Because imports include freight and insurance (CIF), this balance is somewhat more negative than the goods balance in Banco de la República's balance of payments, which uses FOB on both sides.",
                "Figures for recent months are provisional and may be revised."
            ],
            "formulas": [
                ["Annual balance", "B<sub>a</sub> = Σ<sub>m∈a</sub> X<sub>m</sub> − Σ<sub>m∈a</sub> M<sub>m</sub>", "X = FOB exports; M = CIF imports; m = months of year a (for the current year, only those published)"]
            ]
        },
    },
    "g-expo-productos": {
        "es": {
            "que": "Muestra qué vende Colombia al exterior en los últimos 12 meses, según los cinco grupos con que el DANE clasifica las exportaciones: los cuatro productos tradicionales (petróleo y derivados, carbón, café y ferroníquel) y los no tradicionales, que agrupan todo lo demás (manufacturas, agroindustria, flores, banano, químicos, entre otros). Revela el grado de concentración de la canasta exportadora en unos pocos bienes básicos.",
            "leer": "Barras horizontales ordenadas de mayor a menor. El largo de cada barra es el valor exportado en 12 meses, en miles de millones de dólares FOB; el número al final es su participación en el total. Colores: azul para petróleo y derivados, café oscuro para carbón y verde para los demás grupos. Al pasar el cursor aparece la variación frente a los 12 meses anteriores, en dólares.",
            "importa": "La composición de las exportaciones determina qué tan expuestos están los ingresos externos, el recaudo y la tasa de cambio a los precios internacionales de unos pocos bienes. Una canasta dominada por petróleo y carbón transmite con fuerza los choques de precios a la economía; un peso mayor de los no tradicionales suele asociarse a ingresos externos más estables y a más empresas y regiones vinculadas al comercio.",
            "interpretar": [
                "Una variación anual fuerte en petróleo o carbón suele reflejar sobre todo precios internacionales; en café influyen además el clima y la cosecha.",
                "Si la participación de los no tradicionales sube, la canasta se diversifica; el gráfico de peso del petróleo y el carbón muestra esa evolución en el tiempo.",
                "Los no tradicionales son un grupo muy heterogéneo: su total no permite saber qué producto concreto creció.",
                "Las variaciones están en dólares corrientes, así que mezclan cambios de precio y de cantidad; las cifras recientes son provisionales."
            ],
            "formulas": [
                ["Valor de 12 meses del grupo k", "X12<sub>k,t</sub> = Σ<sub>j=0..11</sub> X<sub>k,t−j</sub>", "X<sub>k</sub> = exportaciones FOB del grupo k en el mes"],
                ["Participación", "s<sub>k</sub> = X12<sub>k,t</sub> ÷ X12<sub>t</sub> × 100", "X12<sub>t</sub> = exportaciones totales de 12 meses"],
                ["Variación anual (al pasar el cursor)", "g<sub>k</sub> = (X12<sub>k,t</sub> ÷ X12<sub>k,t−12</sub> − 1) × 100", "compara con los 12 meses que terminan un año antes"]
            ]
        },
        "en": {
            "que": "This chart shows what Colombia sold abroad over the last 12 months, using DANE's five export groups: the four traditional products (oil and derivatives, coal, coffee and ferronickel) and non-traditional exports, which cover everything else (manufactures, agribusiness, flowers, bananas, chemicals and more). It reveals how concentrated the export basket is in a handful of commodities.",
            "leer": "Horizontal bars sorted from largest to smallest. Bar length is the value exported over 12 months, in billions of FOB dollars; the number at the end is its share of the total. Colours: blue for oil and derivatives, dark brown for coal and green for the other groups. Hovering shows the change versus the previous 12 months, in dollars.",
            "importa": "Export composition determines how exposed external income, tax revenue and the exchange rate are to the world prices of a few goods. A basket dominated by oil and coal transmits price shocks strongly to the economy; a larger weight of non-traditional exports tends to go with steadier external income and more firms and regions linked to trade.",
            "interpretar": [
                "A large annual change in oil or coal mostly reflects world prices; for coffee, weather and the harvest also matter.",
                "If the share of non-traditional exports rises, the basket is diversifying; the oil-and-coal weight chart shows that evolution over time.",
                "Non-traditional exports are a very mixed group: their total does not reveal which specific product grew.",
                "Changes are in current dollars, so they mix price and quantity effects; recent figures are provisional."
            ],
            "formulas": [
                ["12-month value of group k", "X12<sub>k,t</sub> = Σ<sub>j=0..11</sub> X<sub>k,t−j</sub>", "X<sub>k</sub> = monthly FOB exports of group k"],
                ["Share", "s<sub>k</sub> = X12<sub>k,t</sub> ÷ X12<sub>t</sub> × 100", "X12<sub>t</sub> = total 12-month exports"],
                ["Annual change (on hover)", "g<sub>k</sub> = (X12<sub>k,t</sub> ÷ X12<sub>k,t−12</sub> − 1) × 100", "compared with the 12 months ending a year earlier"]
            ]
        },
    },
    "g-expo-minero": {
        "es": {
            "que": "Muestra qué parte de todo lo que Colombia exporta corresponde a petróleo y sus derivados más carbón, los dos productos minero-energéticos que han dominado la canasta. Es una medida directa de la dependencia del país de estos bienes: se dispara en los auges de precios de las materias primas, como la bonanza de inicios de la década de 2010, y cae cuando esos precios se desploman o cuando crecen otras ventas.",
            "leer": "Una sola línea azul, en porcentaje de las exportaciones totales, con eje fijo de 0% a 80%. Cada punto divide la suma de 12 meses de las exportaciones de petróleo y derivados más carbón entre la suma de 12 meses de las exportaciones totales, ambas en dólares FOB. La serie empieza a mediados de los años noventa. Una línea descendente indica menor peso minero-energético.",
            "importa": "Cuanto mayor es esta participación, más dependen de los precios internacionales de la energía la entrada de dólares, la tasa de cambio, las regalías y los ingresos del Gobierno. Para un inversionista indica la sensibilidad de la economía colombiana al ciclo petrolero y la vulnerabilidad de las cuentas externas y fiscales ante una caída de precios.",
            "interpretar": [
                "Una caída puede deberse a que la minería se vende más barata (efecto precio) o a que crecen más los demás productos; no siempre implica una diversificación genuina.",
                "Saltos bruscos coinciden con choques de precios del petróleo; compárelo con el gráfico de valor, precio y volumen de las exportaciones.",
                "No incluye otros minerales como oro o ferroníquel, que el DANE clasifica de forma distinta.",
                "Como usa sumas de 12 meses, el indicador se mueve gradualmente y no capta la estacionalidad de un mes aislado."
            ],
            "formulas": [
                ["Peso minero-energético", "S<sub>t</sub> = (P12<sub>t</sub> + C12<sub>t</sub>) ÷ X12<sub>t</sub> × 100", "P12 = petróleo y derivados; C12 = carbón; X12 = exportaciones totales; todas sumas de 12 meses en dólares FOB"]
            ]
        },
        "en": {
            "que": "This chart shows what share of everything Colombia exports is oil and its derivatives plus coal, the two mining and energy products that have dominated the basket. It is a direct measure of the country's dependence on these goods: it surges during commodity price booms, such as the bonanza of the early 2010s, and falls when those prices collapse or when other sales grow.",
            "leer": "A single blue line, as a percentage of total exports, on a fixed 0% to 80% axis. Each point divides the 12-month sum of oil-and-derivatives plus coal exports by the 12-month sum of total exports, both in FOB dollars. The series starts in the mid-1990s. A falling line means a smaller mining-and-energy weight.",
            "importa": "The higher this share, the more the inflow of dollars, the exchange rate, royalties and government revenue depend on world energy prices. For an investor it gauges the Colombian economy's sensitivity to the oil cycle and the vulnerability of the external and fiscal accounts to a price fall.",
            "interpretar": [
                "A decline may happen because mining output sells at lower prices (price effect) or because other products grow faster; it does not always mean genuine diversification.",
                "Sharp jumps coincide with oil price shocks; compare with the export value, price and volume chart.",
                "It excludes other minerals such as gold or ferronickel, which DANE classifies separately.",
                "Because it uses 12-month sums, the indicator moves gradually and does not capture the seasonality of a single month."
            ],
            "formulas": [
                ["Mining-and-energy weight", "S<sub>t</sub> = (P12<sub>t</sub> + C12<sub>t</sub>) ÷ X12<sub>t</sub> × 100", "P12 = oil and derivatives; C12 = coal; X12 = total exports; all 12-month sums in FOB dollars"]
            ]
        },
    },
    "g-impo-uso": {
        "es": {
            "que": "Muestra para qué compra bienes Colombia en el exterior y cuáles de esas compras crecen o caen en lo corrido del año frente al mismo periodo del año anterior. Usa la clasificación CUODE (Clasificación según Uso o Destino Económico), que separa las importaciones en bienes de consumo, materias primas e insumos, combustibles y bienes de capital. Así distingue si el movimiento de las importaciones viene del consumo de los hogares, de la producción o de la inversión.",
            "leer": "Barras horizontales, una por cada uno de los nueve subgrupos CUODE, ordenadas por su variación. El eje horizontal es la variación porcentual del valor CIF en dólares del periodo enero–último mes publicado frente al mismo periodo del año anterior; la línea vertical marca el cero. Verde: el grupo crece; naranja: cae. El número entre paréntesis junto al nombre es la participación del grupo en las importaciones totales del periodo, para ponderar su importancia.",
            "importa": "Las importaciones por uso son un termómetro adelantado de la demanda interna. Las compras de bienes de capital anticipan inversión en maquinaria y equipo; las materias primas para la industria acompañan la producción manufacturera; los bienes de consumo duradero (vehículos, electrodomésticos) reflejan la confianza y el crédito de los hogares. Para un inversionista permiten leer qué componente de la demanda empuja la economía.",
            "interpretar": [
                "Una variación alta en un grupo con participación pequeña pesa poco en el total: combine siempre el signo y el tamaño de la barra con el número entre paréntesis.",
                "El crecimiento de bienes de capital y equipo de transporte suele acompañar ciclos de inversión; el de consumo duradero, ciclos de crédito y confianza de los hogares.",
                "Las variaciones están en dólares corrientes: una devaluación o una subida de precios internacionales cambia el valor sin que cambie la cantidad comprada.",
                "Al ser año corrido, al comienzo del año pocos meses determinan el resultado; compare con la composición anual del gráfico vecino."
            ],
            "formulas": [
                ["Variación año corrido", "g<sub>k</sub> = (M<sub>k,a</sub> ÷ M<sub>k,a−1</sub> − 1) × 100", "M<sub>k,a</sub> = importaciones CIF del grupo k de enero al último mes del año a; a−1 = mismo periodo del año anterior"],
                ["Participación (entre paréntesis)", "s<sub>k</sub> = M<sub>k,a</sub> ÷ M<sub>a</sub> × 100", "M<sub>a</sub> = importaciones totales del periodo"]
            ]
        },
        "en": {
            "que": "This chart shows what Colombia imports goods for, and which of those purchases are rising or falling so far this year versus the same period of the previous year. It uses the CUODE classification (by economic use or destination), which splits imports into consumer goods, raw materials and intermediate inputs, fuels and capital goods. That way it shows whether import moves come from household consumption, production or investment.",
            "leer": "Horizontal bars, one for each of the nine CUODE subgroups, sorted by their change. The horizontal axis is the percentage change in CIF dollar value for January to the latest month published versus the same period a year earlier; the vertical line marks zero. Green: the group is growing; orange: falling. The number in brackets next to the name is the group's share of total imports in the period, to weigh its importance.",
            "importa": "Imports by use are a leading gauge of domestic demand. Capital goods purchases anticipate investment in machinery and equipment; raw materials for industry accompany manufacturing output; durable consumer goods (vehicles, appliances) reflect household confidence and credit. For an investor they reveal which component of demand is driving the economy.",
            "interpretar": [
                "A large change in a group with a small share carries little weight in the total: always combine the sign and size of the bar with the number in brackets.",
                "Growth in capital goods and transport equipment tends to accompany investment cycles; durable consumer goods, household credit and confidence cycles.",
                "Changes are in current dollars: a depreciation or higher world prices change the value without changing the quantity bought.",
                "Because it is year to date, early in the year a few months drive the result; compare with the annual composition in the neighbouring chart."
            ],
            "formulas": [
                ["Year-to-date change", "g<sub>k</sub> = (M<sub>k,a</sub> ÷ M<sub>k,a−1</sub> − 1) × 100", "M<sub>k,a</sub> = CIF imports of group k from January to the latest month of year a; a−1 = same period a year earlier"],
                ["Share (in brackets)", "s<sub>k</sub> = M<sub>k,a</sub> ÷ M<sub>a</sub> × 100", "M<sub>a</sub> = total imports in the period"]
            ]
        },
    },
    "g-impo-estructura": {
        "es": {
            "que": "Muestra cómo se reparten, año por año, las importaciones de Colombia entre los tres grandes grupos de la clasificación CUODE (uso o destino económico): bienes de consumo, materias primas e insumos, y bienes de capital y materiales de construcción. Permite ver si el país importa cada vez más para consumir, para producir o para invertir, y cómo cambia esa mezcla en recesiones y auges.",
            "leer": "Cada barra es un año y suma 100%. Azul (abajo): bienes de consumo; verde: materias primas y productos intermedios, que incluyen combustibles; naranja (arriba): bienes de capital y materiales de construcción. Se excluyen las partidas «no clasificadas», de modo que las participaciones se calculan sobre la suma de los tres grupos. La serie empieza en 2005. El último año, marcado con asterisco (*), es el acumulado a la fecha y no un año completo.",
            "importa": "La estructura de las importaciones informa sobre el modelo de crecimiento: una mayor parte de bienes de capital se asocia a fases de inversión y ampliación de la capacidad productiva; una mayor parte de bienes de consumo, a fases impulsadas por el gasto de los hogares. Para un inversionista ayuda a evaluar la calidad del déficit comercial: no es lo mismo financiar maquinaria que bienes de consumo.",
            "interpretar": [
                "Si la franja naranja se ensancha, el país dedica una mayor parte de sus compras externas a maquinaria, equipo y construcción.",
                "Las participaciones dependen también de los precios: un encarecimiento del petróleo y de los insumos agranda la franja verde sin que cambie la cantidad importada.",
                "El año parcial puede verse afectado por estacionalidad (compras concentradas en ciertos meses).",
                "Para el detalle por subgrupo y su variación reciente, use el gráfico «¿Para qué importa?»."
            ],
            "formulas": [
                ["Participación del grupo g en el año a", "s<sub>g,a</sub> = M<sub>g,a</sub> ÷ (M<sub>C,a</sub> + M<sub>MP,a</sub> + M<sub>K,a</sub>) × 100", "M = importaciones CIF anuales; C = consumo; MP = materias primas; K = capital y construcción (sin «no clasificados»)"]
            ]
        },
        "en": {
            "que": "This chart shows how Colombia's imports are split, year by year, among the three main groups of the CUODE classification (by economic use): consumer goods, raw materials and inputs, and capital goods and construction materials. It shows whether the country increasingly imports to consume, to produce or to invest, and how that mix changes in recessions and booms.",
            "leer": "Each bar is one year and adds up to 100%. Blue (bottom): consumer goods; green: raw materials and intermediate goods, including fuels; orange (top): capital goods and construction materials. 'Unclassified' items are excluded, so shares are computed over the sum of the three groups. The series starts in 2005. The latest year, marked with an asterisk (*), is year to date, not a full year.",
            "importa": "The structure of imports says something about the growth model: a larger share of capital goods goes with investment phases and expansion of productive capacity; a larger share of consumer goods, with phases driven by household spending. For an investor it helps assess the quality of the trade deficit: financing machinery is not the same as financing consumer goods.",
            "interpretar": [
                "If the orange band widens, the country is devoting a larger share of its foreign purchases to machinery, equipment and construction.",
                "Shares also depend on prices: more expensive oil and inputs enlarge the green band with no change in the quantity imported.",
                "The partial year may be affected by seasonality (purchases concentrated in certain months).",
                "For subgroup detail and recent changes, use the 'What are imports for?' chart."
            ],
            "formulas": [
                ["Share of group g in year a", "s<sub>g,a</sub> = M<sub>g,a</sub> ÷ (M<sub>C,a</sub> + M<sub>MP,a</sub> + M<sub>K,a</sub>) × 100", "M = annual CIF imports; C = consumer goods; MP = raw materials; K = capital and construction (excluding 'unclassified')"]
            ]
        },
    },
    "g-destinos": {
        "es": {
            "que": "Muestra a quién le vende Colombia: qué parte de las exportaciones de los últimos 12 meses va a cada destino principal. Destaca el peso de Estados Unidos como primer comprador y el papel de la Unión Europea, Panamá, China y los vecinos latinoamericanos. Retrata la exposición del ingreso exportador a la demanda de cada socio y a sus políticas comerciales.",
            "leer": "Barras horizontales azules con los nueve destinos de mayor participación, ordenados de mayor a menor, y una barra gris al final, «Resto», que agrupa a todos los demás países (incluidos los destinos del anexo del DANE que no entran entre los nueve primeros). El eje horizontal y el número al final de cada barra son el porcentaje de las exportaciones FOB de los últimos 12 meses. La Unión Europea aparece como un solo destino, tal como la publica el DANE.",
            "importa": "La concentración de las ventas en pocos mercados expone al país a los ciclos económicos, las monedas y las decisiones arancelarias de esos socios. Un comprador dominante amplifica cualquier choque en su economía. Para un inversionista permite identificar qué economías extranjeras influyen más sobre los ingresos de los exportadores colombianos.",
            "interpretar": [
                "Si sube la participación de un destino, ese mercado gana peso en la demanda externa del país; puede deberse a más ventas allí o a menos ventas en los demás.",
                "La composición depende de los productos: los destinos del petróleo y el carbón cambian con los precios de esos bienes, lo que mueve las participaciones sin cambios de fondo en las relaciones comerciales.",
                "Panamá incluye en parte mercancías en tránsito o reexportadas desde allí, por lo que no es necesariamente el destino final.",
                "Para la evolución de la concentración en el tiempo, vea el gráfico de diversificación de destinos y productos."
            ],
            "formulas": [
                ["Participación del destino d", "s<sub>d</sub> = X12<sub>d,t</sub> ÷ X12<sub>t</sub> × 100", "X12<sub>d</sub> = exportaciones FOB al destino d en 12 meses; X12 = exportaciones totales en 12 meses"],
                ["Resto", "s<sub>Resto</sub> = 100 − Σ<sub>d∈top 9</sub> s<sub>d</sub>", "agrupa todos los destinos fuera de los nueve principales"]
            ]
        },
        "en": {
            "que": "This chart shows who buys from Colombia: what share of the last 12 months' exports goes to each main destination. It highlights the weight of the United States as the top buyer and the role of the European Union, Panama, China and Latin American neighbours. It portrays how exposed export income is to each partner's demand and trade policy.",
            "leer": "Blue horizontal bars for the nine destinations with the largest shares, sorted from largest to smallest, and a grey bar at the end, 'Rest', grouping all other countries (including annex destinations outside the top nine). The horizontal axis and the number at the end of each bar are the percentage of FOB exports over the last 12 months. The European Union appears as a single destination, as published by DANE.",
            "importa": "Concentrating sales in a few markets exposes the country to those partners' business cycles, currencies and tariff decisions. A dominant buyer amplifies any shock in its economy. For an investor it identifies which foreign economies have the greatest bearing on Colombian exporters' revenue.",
            "interpretar": [
                "If a destination's share rises, that market gains weight in the country's external demand; this may come from more sales there or fewer sales elsewhere.",
                "The mix depends on products: destinations for oil and coal shift with those goods' prices, moving shares without deep changes in trade relationships.",
                "Panama partly includes goods in transit or re-exported from there, so it is not necessarily the final destination.",
                "For how concentration has evolved over time, see the diversification of destinations and products chart."
            ],
            "formulas": [
                ["Share of destination d", "s<sub>d</sub> = X12<sub>d,t</sub> ÷ X12<sub>t</sub> × 100", "X12<sub>d</sub> = FOB exports to destination d over 12 months; X12 = total exports over 12 months"],
                ["Rest", "s<sub>Rest</sub> = 100 − Σ<sub>d∈top 9</sub> s<sub>d</sub>", "groups all destinations outside the top nine"]
            ]
        },
    },
    "g-origenes": {
        "es": {
            "que": "Muestra a quién le compra Colombia: qué parte de las importaciones de los últimos 12 meses proviene de cada uno de los diez países con mayor participación. Pone en evidencia que dos proveedores, Estados Unidos y China, concentran una parte muy grande de las compras externas, seguidos de socios regionales y europeos.",
            "leer": "Barras horizontales naranjas, ordenadas de mayor a menor, con los diez principales países de origen. El eje horizontal y el número al final de cada barra son el porcentaje de las importaciones CIF de los últimos 12 meses. El denominador son las importaciones totales publicadas por el DANE en esos 12 meses (sin las operaciones de zonas francas), de modo que los diez países no suman 100%: la diferencia corresponde a los demás orígenes.",
            "importa": "El origen de las importaciones indica de qué economías depende el abastecimiento de bienes de consumo, insumos y maquinaria. Una alta dependencia de un proveedor expone los costos de las empresas y los precios al consumidor a su tasa de cambio, a sus cadenas de suministro y a cambios de política comercial. Para un inversionista ayuda a evaluar riesgos de abastecimiento y de costos importados.",
            "interpretar": [
                "Un aumento de la participación de un país puede reflejar mayor competitividad de sus productos o cambios en lo que Colombia compra (por ejemplo, más combustibles o más electrónicos).",
                "La evolución en el tiempo de las dos principales fuentes se ve en el gráfico de China, Estados Unidos y el resto.",
                "El país de origen es donde se produjo la mercancía, no necesariamente desde donde se despachó.",
                "Las cifras son en dólares CIF corrientes y las de los meses recientes son provisionales."
            ],
            "formulas": [
                ["Participación del país p", "s<sub>p</sub> = M12<sub>p,t</sub> ÷ M12<sup>pub</sup><sub>t</sub> × 100", "M12<sub>p</sub> = importaciones CIF desde p en 12 meses; M12<sup>pub</sup> = importaciones totales publicadas por el DANE en los mismos 12 meses"]
            ]
        },
        "en": {
            "que": "This chart shows who Colombia buys from: what share of the last 12 months' imports comes from each of the ten countries with the largest shares. It makes clear that two suppliers, the United States and China, account for a very large part of foreign purchases, followed by regional and European partners.",
            "leer": "Orange horizontal bars, sorted from largest to smallest, for the ten main countries of origin. The horizontal axis and the number at the end of each bar are the percentage of CIF imports over the last 12 months. The denominator is total imports published by DANE over those 12 months (excluding free-trade-zone operations), so the ten countries do not add up to 100%: the remainder corresponds to other origins.",
            "importa": "The origin of imports shows which economies Colombia relies on for consumer goods, inputs and machinery. Heavy dependence on one supplier exposes firms' costs and consumer prices to its exchange rate, its supply chains and changes in trade policy. For an investor it helps assess supply and imported-cost risks.",
            "interpretar": [
                "A rising share for a country may reflect more competitive products or changes in what Colombia buys (for instance, more fuels or more electronics).",
                "How the two main sources have evolved over time is shown in the China, United States and the rest chart.",
                "The country of origin is where the goods were produced, not necessarily where they were shipped from.",
                "Figures are in current CIF dollars and those for recent months are provisional."
            ],
            "formulas": [
                ["Share of country p", "s<sub>p</sub> = M12<sub>p,t</sub> ÷ M12<sup>pub</sup><sub>t</sub> × 100", "M12<sub>p</sub> = CIF imports from p over 12 months; M12<sup>pub</sup> = total imports published by DANE over the same 12 months"]
            ]
        },
    },
    "g-com-pq-expo": {
        "es": {
            "que": "Descompone el crecimiento del valor de las exportaciones en dos partes: cuánto se debe a que los bienes se vendieron más caros o más baratos en dólares (precio) y cuánto a que se vendió más o menos cantidad (volumen). Responde a la pregunta de si Colombia exporta más o solo cobra más: en los auges y caídas del petróleo, casi todo el movimiento del valor suele venir del precio.",
            "leer": "Eje vertical en variación anual (%), con una línea horizontal en cero. Línea azul gruesa: valor, variación anual de la suma de 12 meses de las exportaciones FOB del DANE. Línea amarilla punteada: precio, variación anual del promedio de 12 meses del índice de precios de exportación en dólares del Banco de la República. Línea verde: volumen implícito, lo que queda del valor después de descontar el precio. La serie empieza en 2005.",
            "importa": "Distinguir precio de volumen es clave para leer el comercio: una subida del valor por precios mejora el ingreso nacional y las cuentas fiscales, pero no indica que el aparato exportador produzca más; un aumento del volumen sí refleja más producción, empleo y capacidad. Para un inversionista ayuda a separar el efecto del ciclo de las materias primas del desempeño real de los sectores exportadores.",
            "interpretar": [
                "Si la línea azul sube y la amarilla también mientras la verde está cerca de cero, el valor exportado crece por precios y no por cantidades.",
                "Una línea verde positiva con precios en caída indica que se vende más cantidad aunque cada unidad valga menos.",
                "El volumen implícito es un residuo: acumula cualquier diferencia de cobertura o de ponderación entre las cifras del DANE y el índice de precios, por lo que no es una medida directa de cantidades.",
                "La relación entre este índice de precios y el de importaciones son los términos de intercambio, que aparecen en la tarjeta de medidas de la página."
            ],
            "formulas": [
                ["Valor", "v<sub>t</sub> = (X12<sub>t</sub> ÷ X12<sub>t−12</sub> − 1) × 100", "X12 = suma de 12 meses de las exportaciones FOB"],
                ["Precio", "p<sub>t</sub> = (P̄12<sub>t</sub> ÷ P̄12<sub>t−12</sub> − 1) × 100", "P̄12 = promedio de 12 meses del índice de precios de exportación en dólares"],
                ["Volumen implícito", "q<sub>t</sub> = [(1 + v<sub>t</sub>/100) ÷ (1 + p<sub>t</sub>/100) − 1] × 100", "v y p en porcentaje; se cumple (1 + v) = (1 + p)(1 + q)"]
            ]
        },
        "en": {
            "que": "This chart breaks down the growth in export value into two parts: how much is due to goods selling at higher or lower dollar prices (price) and how much to selling a larger or smaller quantity (volume). It answers whether Colombia is exporting more or merely charging more: during oil booms and busts, almost all of the change in value usually comes from price.",
            "leer": "Vertical axis in annual change (%), with a horizontal line at zero. Thick blue line: value, the annual change in the 12-month sum of DANE's FOB exports. Dotted yellow line: price, the annual change in the 12-month average of Banco de la República's dollar export price index. Green line: implied volume, what is left of value after removing price. The series starts in 2005.",
            "importa": "Separating price from volume is key to reading trade: a value increase driven by prices improves national income and the fiscal accounts but does not mean the export sector is producing more; a volume increase does reflect more output, jobs and capacity. For an investor it helps separate the commodity cycle from the real performance of export sectors.",
            "interpretar": [
                "If the blue and yellow lines rise while the green line stays near zero, export value is growing through prices, not quantities.",
                "A positive green line while prices fall means more quantity is being sold even though each unit is worth less.",
                "Implied volume is a residual: it absorbs any coverage or weighting differences between DANE figures and the price index, so it is not a direct measure of quantities.",
                "The ratio of this price index to the import price index is the terms of trade, shown in the page's measures card."
            ],
            "formulas": [
                ["Value", "v<sub>t</sub> = (X12<sub>t</sub> ÷ X12<sub>t−12</sub> − 1) × 100", "X12 = 12-month sum of FOB exports"],
                ["Price", "p<sub>t</sub> = (P̄12<sub>t</sub> ÷ P̄12<sub>t−12</sub> − 1) × 100", "P̄12 = 12-month average of the dollar export price index"],
                ["Implied volume", "q<sub>t</sub> = [(1 + v<sub>t</sub>/100) ÷ (1 + p<sub>t</sub>/100) − 1] × 100", "v and p in percent; (1 + v) = (1 + p)(1 + q) holds"]
            ]
        },
    },
    "g-com-pq-impo": {
        "es": {
            "que": "Aplica a las importaciones la misma descomposición que el gráfico de exportaciones: separa el crecimiento del valor importado en la parte que viene de precios en dólares y la que viene de la cantidad comprada. Permite saber si Colombia compra más bienes al exterior porque la demanda interna se expande o porque los bienes importados, como combustibles, insumos y maquinaria, se encarecieron.",
            "leer": "Eje vertical en variación anual (%), con una línea horizontal en cero. Línea azul gruesa: valor, variación anual de la suma de 12 meses de las importaciones CIF totales del DANE. Línea amarilla punteada: precio, variación anual del promedio de 12 meses del índice de precios de importación en dólares del Banco de la República. Línea verde: volumen implícito, el residuo después de descontar el precio. La serie empieza en 2005.",
            "importa": "El volumen importado es un indicador cercano del gasto interno en bienes: crece con el consumo y la inversión y cae en las recesiones, a menudo con más fuerza que el PIB. El precio de las importaciones, por su parte, es un canal de la inflación externa hacia los costos de las empresas. Para un inversionista ayuda a leer el ciclo de la demanda interna y las presiones de costos importados.",
            "interpretar": [
                "Una línea verde positiva y creciente indica que se están comprando más bienes al exterior, señal de demanda interna en expansión; una caída fuerte suele acompañar a las recesiones, como en 2020.",
                "Si el valor sube sobre todo por la línea amarilla, el encarecimiento de lo importado explica el mayor gasto en dólares, no un mayor volumen.",
                "Las importaciones están en dólares: el efecto de la tasa de cambio sobre la demanda se ve en el volumen con rezago, no en el precio en dólares.",
                "Como en exportaciones, el volumen implícito es un residuo y no una medida directa de cantidades."
            ],
            "formulas": [
                ["Valor", "v<sub>t</sub> = (M12<sub>t</sub> ÷ M12<sub>t−12</sub> − 1) × 100", "M12 = suma de 12 meses de las importaciones CIF totales"],
                ["Precio", "p<sub>t</sub> = (P̄12<sub>t</sub> ÷ P̄12<sub>t−12</sub> − 1) × 100", "P̄12 = promedio de 12 meses del índice de precios de importación en dólares"],
                ["Volumen implícito", "q<sub>t</sub> = [(1 + v<sub>t</sub>/100) ÷ (1 + p<sub>t</sub>/100) − 1] × 100", "v y p en porcentaje"]
            ]
        },
        "en": {
            "que": "This chart applies to imports the same breakdown as the exports chart: it splits growth in import value into the part coming from dollar prices and the part coming from the quantity bought. It shows whether Colombia is buying more goods abroad because domestic demand is expanding or because imported goods such as fuels, inputs and machinery have become more expensive.",
            "leer": "Vertical axis in annual change (%), with a horizontal line at zero. Thick blue line: value, the annual change in the 12-month sum of DANE's total CIF imports. Dotted yellow line: price, the annual change in the 12-month average of Banco de la República's dollar import price index. Green line: implied volume, the residual after removing price. The series starts in 2005.",
            "importa": "Import volume is a close proxy for domestic spending on goods: it grows with consumption and investment and falls in recessions, often more sharply than GDP. Import prices, in turn, are a channel through which foreign inflation reaches firms' costs. For an investor it helps read the domestic demand cycle and imported cost pressures.",
            "interpretar": [
                "A positive and rising green line means more goods are being bought abroad, a sign of expanding domestic demand; a sharp fall usually accompanies recessions, as in 2020.",
                "If value rises mainly because of the yellow line, more expensive imports explain the higher dollar spending, not higher volume.",
                "Imports are in dollars: the exchange rate's effect on demand shows up in volume with a lag, not in the dollar price.",
                "As with exports, implied volume is a residual, not a direct measure of quantities."
            ],
            "formulas": [
                ["Value", "v<sub>t</sub> = (M12<sub>t</sub> ÷ M12<sub>t−12</sub> − 1) × 100", "M12 = 12-month sum of total CIF imports"],
                ["Price", "p<sub>t</sub> = (P̄12<sub>t</sub> ÷ P̄12<sub>t−12</sub> − 1) × 100", "P̄12 = 12-month average of the dollar import price index"],
                ["Implied volume", "q<sub>t</sub> = [(1 + v<sub>t</sub>/100) ÷ (1 + p<sub>t</sub>/100) − 1] × 100", "v and p in percent"]
            ]
        },
    },
    "g-com-canasta": {
        "es": {
            "que": "Muestra cómo ha cambiado en el tiempo lo que vende Colombia al exterior, separando las exportaciones en los cinco grupos del DANE. Cuenta la historia de la canasta exportadora: el auge del petróleo y el carbón durante la bonanza de las materias primas, su caída posterior y el crecimiento gradual de los productos no tradicionales, que con el tiempo se volvieron el grupo más grande.",
            "leer": "Áreas apiladas en miles de millones de dólares FOB; cada punto es la suma de los 12 meses que terminan en ese mes, desde mediados de los años noventa. De abajo hacia arriba: petróleo y derivados (amarillo), carbón (morado), café (naranja), ferroníquel (azul) y no tradicionales (verde). El grosor de cada franja es lo exportado por ese grupo y la altura total es el total exportado. Al pasar el cursor se ve el valor de cada grupo.",
            "importa": "La evolución de la canasta muestra si el país reduce su dependencia de los bienes minero-energéticos y si las exportaciones con mayor valor agregado ganan espacio. Esto incide en la estabilidad de los ingresos externos, en la sensibilidad de la tasa de cambio al petróleo y en el potencial de crecimiento de largo plazo. Para un inversionista ofrece una perspectiva histórica de la exposición a materias primas.",
            "interpretar": [
                "Si la franja verde crece mientras las de petróleo y carbón se estrechan, la canasta se diversifica en valor.",
                "Las franjas de petróleo y carbón cambian mucho con los precios internacionales: su encogimiento no siempre indica menor producción.",
                "Compare con el gráfico de peso del petróleo y el carbón, que expresa la misma información como porcentaje del total.",
                "Las cifras son en dólares corrientes: parte del crecimiento de largo plazo refleja inflación en dólares, no solo mayor volumen."
            ],
            "formulas": [
                ["Suma de 12 meses del grupo k", "X12<sub>k,t</sub> = Σ<sub>j=0..11</sub> X<sub>k,t−j</sub>", "k ∈ {petróleo, carbón, café, ferroníquel, no tradicionales}; dólares FOB"],
                ["Altura total", "X12<sub>t</sub> = Σ<sub>k</sub> X12<sub>k,t</sub>", "exportaciones totales de 12 meses"]
            ]
        },
        "en": {
            "que": "This chart shows how what Colombia sells abroad has changed over time, splitting exports into DANE's five groups. It tells the story of the export basket: the oil and coal surge during the commodity boom, their later decline and the gradual growth of non-traditional products, which over time became the largest group.",
            "leer": "Stacked areas in billions of FOB dollars; each point is the sum of the 12 months ending in that month, from the mid-1990s. From bottom to top: oil and derivatives (yellow), coal (purple), coffee (orange), ferronickel (blue) and non-traditional (green). The thickness of each band is what that group exported and the total height is total exports. Hovering shows each group's value.",
            "importa": "The evolution of the basket shows whether the country is reducing its dependence on mining and energy goods and whether higher value-added exports are gaining ground. This bears on the stability of external income, the exchange rate's sensitivity to oil and long-run growth potential. For an investor it offers a historical view of commodity exposure.",
            "interpretar": [
                "If the green band grows while the oil and coal bands narrow, the basket is diversifying in value.",
                "The oil and coal bands move a lot with world prices: their shrinking does not always mean lower output.",
                "Compare with the oil-and-coal weight chart, which expresses the same information as a share of the total.",
                "Figures are in current dollars: part of long-run growth reflects dollar inflation, not just higher volume."
            ],
            "formulas": [
                ["12-month sum of group k", "X12<sub>k,t</sub> = Σ<sub>j=0..11</sub> X<sub>k,t−j</sub>", "k ∈ {oil, coal, coffee, ferronickel, non-traditional}; FOB dollars"],
                ["Total height", "X12<sub>t</sub> = Σ<sub>k</sub> X12<sub>k,t</sub>", "total 12-month exports"]
            ]
        },
    },
    "g-com-bilateral": {
        "es": {
            "que": "Muestra con qué socios comerciales Colombia tiene superávit (les vende más de lo que les compra) y con cuáles tiene déficit, en los últimos 12 meses. Suele revelar un déficit grande con China, donde Colombia compra mucho y vende poco, y saldos más equilibrados o positivos con algunos vecinos latinoamericanos. Ayuda a entender de dónde viene el déficit comercial total.",
            "leer": "Barras horizontales en miles de millones de dólares, ordenadas del mayor déficit al mayor superávit. Cada barra es exportaciones FOB al país en 12 meses menos importaciones CIF desde ese país en los mismos 12 meses. Verde: superávit; naranja: déficit; la línea vertical marca el cero. El número junto a cada barra es el saldo con signo. Solo incluye socios individuales que aparecen a la vez en el anexo de destinos y en el de orígenes del DANE; la Unión Europea no está porque se publica como bloque.",
            "importa": "El saldo bilateral indica qué relaciones comerciales aportan dólares y cuáles los demandan, y qué tan expuesto está el país a la política comercial de cada socio. Para un inversionista ayuda a dimensionar el efecto de cambios arancelarios, de acuerdos comerciales o de choques en economías específicas sobre las cuentas externas de Colombia.",
            "interpretar": [
                "Un déficit con un país no es por sí mismo un problema: puede reflejar que de allí vienen insumos y maquinaria que Colombia no produce.",
                "Como las importaciones se valoran CIF (con flete y seguro) y las exportaciones FOB, todos los saldos aparecen algo más negativos que en la balanza de pagos.",
                "El destino registrado de las exportaciones puede no ser el final (por ejemplo, ventas a través de Panamá), lo que afecta los saldos con algunos países.",
                "La evolución de la participación de China y Estados Unidos en las compras se ve en el gráfico vecino."
            ],
            "formulas": [
                ["Saldo con el socio p", "B<sub>p</sub> = Σ<sub>j=0..11</sub> X<sub>p,t−j</sub> − Σ<sub>j=0..11</sub> M<sub>p,t−j</sub>", "X<sub>p</sub> = exportaciones FOB al país p; M<sub>p</sub> = importaciones CIF desde p; en miles de millones de dólares"]
            ]
        },
        "en": {
            "que": "This chart shows which trading partners Colombia runs a surplus with (selling them more than it buys) and which it runs a deficit with, over the last 12 months. It usually reveals a large deficit with China, from which Colombia buys a lot and to which it sells little, and more balanced or positive balances with some Latin American neighbours. It helps explain where the overall trade deficit comes from.",
            "leer": "Horizontal bars in billions of dollars, sorted from the largest deficit to the largest surplus. Each bar is FOB exports to the country over 12 months minus CIF imports from that country over the same 12 months. Green: surplus; orange: deficit; the vertical line marks zero. The number next to each bar is the signed balance. It only includes individual partners that appear in both DANE's destinations annex and its origins annex; the European Union is absent because it is published as a bloc.",
            "importa": "The bilateral balance shows which trade relationships bring in dollars and which demand them, and how exposed the country is to each partner's trade policy. For an investor it helps size the impact of tariff changes, trade agreements or shocks in specific economies on Colombia's external accounts.",
            "interpretar": [
                "A deficit with a country is not a problem in itself: it may reflect that inputs and machinery Colombia does not produce come from there.",
                "Because imports are valued CIF (with freight and insurance) and exports FOB, all balances appear somewhat more negative than in the balance of payments.",
                "The recorded destination of exports may not be the final one (for example, sales through Panama), which affects balances with some countries.",
                "How China's and the United States' shares of purchases have evolved is shown in the neighbouring chart."
            ],
            "formulas": [
                ["Balance with partner p", "B<sub>p</sub> = Σ<sub>j=0..11</sub> X<sub>p,t−j</sub> − Σ<sub>j=0..11</sub> M<sub>p,t−j</sub>", "X<sub>p</sub> = FOB exports to country p; M<sub>p</sub> = CIF imports from p; in billions of dollars"]
            ]
        },
    },
    "g-com-china": {
        "es": {
            "que": "Muestra cómo ha cambiado el peso de los dos principales proveedores de Colombia: China y Estados Unidos. Cuenta una de las transformaciones más grandes del comercio colombiano en lo que va del siglo: el ascenso de China como fuente de importaciones de manufacturas, electrónicos, maquinaria y textiles, hasta disputarle el primer lugar a Estados Unidos, que históricamente fue el proveedor dominante.",
            "leer": "Dos líneas en porcentaje de las importaciones: naranja para China y azul para Estados Unidos. Cada punto divide las importaciones CIF desde ese país en los últimos 12 meses entre las importaciones totales publicadas por el DANE en los mismos 12 meses (sin zonas francas). La serie empieza cuando hay doce meses completos del anexo de países de origen del DANE. La diferencia hasta 100% corresponde a todos los demás proveedores.",
            "importa": "La dependencia de pocos proveedores determina la exposición de los costos de las empresas y de los precios al consumidor a la tasa de cambio, la política industrial y las cadenas de suministro de esos países. El cruce entre China y Estados Unidos también tiene implicaciones para la política comercial y para los sectores colombianos que compiten con importaciones. Para un inversionista ayuda a evaluar riesgos geopolíticos y de abastecimiento.",
            "interpretar": [
                "Si la línea naranja sube y la azul baja, China gana terreno como proveedor a costa de Estados Unidos; si ambas suben, las compras se concentran en esos dos países.",
                "Las importaciones desde Estados Unidos incluyen muchos combustibles, cuyo peso cambia con el precio del petróleo, lo que mueve la línea azul sin cambios en las relaciones comerciales.",
                "La participación es en valor: un abaratamiento de los bienes chinos puede reducir su línea aunque la cantidad comprada crezca.",
                "Para el saldo comercial con cada uno de estos países, vea el gráfico de balanza con cada socio."
            ],
            "formulas": [
                ["Participación del país p", "s<sub>p,t</sub> = M12<sub>p,t</sub> ÷ M12<sup>pub</sup><sub>t</sub> × 100", "M12<sub>p</sub> = importaciones CIF desde p (China o Estados Unidos) en 12 meses; M12<sup>pub</sup> = importaciones totales publicadas en los mismos 12 meses"]
            ]
        },
        "en": {
            "que": "This chart shows how the weight of Colombia's two main suppliers, China and the United States, has changed. It tells one of the biggest transformations in Colombian trade this century: China's rise as a source of imported manufactures, electronics, machinery and textiles, to the point of contesting first place with the United States, historically the dominant supplier.",
            "leer": "Two lines as a percentage of imports: orange for China and blue for the United States. Each point divides CIF imports from that country over the last 12 months by total imports published by DANE over the same 12 months (excluding free trade zones). The series starts once there are twelve full months in DANE's country-of-origin annex. The gap to 100% corresponds to all other suppliers.",
            "importa": "Dependence on a few suppliers determines how exposed firms' costs and consumer prices are to those countries' exchange rates, industrial policy and supply chains. The China–United States crossover also matters for trade policy and for Colombian sectors that compete with imports. For an investor it helps assess geopolitical and supply risks.",
            "interpretar": [
                "If the orange line rises and the blue falls, China is gaining ground as a supplier at the expense of the United States; if both rise, purchases are concentrating in those two countries.",
                "Imports from the United States include a lot of fuel, whose weight shifts with oil prices, moving the blue line without changes in trade relationships.",
                "The share is in value: cheaper Chinese goods can lower its line even if the quantity bought grows.",
                "For the trade balance with each of these countries, see the balance-with-each-partner chart."
            ],
            "formulas": [
                ["Share of country p", "s<sub>p,t</sub> = M12<sub>p,t</sub> ÷ M12<sup>pub</sup><sub>t</sub> × 100", "M12<sub>p</sub> = CIF imports from p (China or the United States) over 12 months; M12<sup>pub</sup> = total published imports over the same 12 months"]
            ]
        },
    },
    "g-com-apertura": {
        "es": {
            "que": "Mide qué tan abierta está la economía colombiana al comercio de bienes: cuánto suman las exportaciones y las importaciones en relación con el tamaño de la economía (el PIB). Colombia es una economía relativamente cerrada frente a otros países de tamaño similar; el indicador muestra si esa apertura aumenta o disminuye con el tiempo y cómo responde a los ciclos de precios de las materias primas y a la tasa de cambio.",
            "leer": "Áreas apiladas en porcentaje del PIB, trimestrales, desde 2005. Azul (abajo): exportaciones FOB de bienes; naranja (arriba): importaciones CIF. Ambas suman los últimos cuatro trimestres completos y se dividen por el PIB nominal de esos mismos cuatro trimestres, convertido a dólares con la TRM (tasa representativa del mercado, el tipo de cambio oficial peso-dólar) promedio de cada trimestre. La altura total es la apertura comercial de bienes.",
            "importa": "La apertura indica cuánto dependen la producción y el consumo del comercio exterior y, por tanto, qué tan expuesta está la economía a choques externos y a la tasa de cambio. Una mayor integración suele asociarse a más competencia, transferencia de tecnología y acceso a insumos. Para un inversionista ayuda a dimensionar el peso de los sectores transables y la sensibilidad de la economía al comercio mundial.",
            "interpretar": [
                "Una subida puede venir de más comercio en dólares o de un PIB en dólares más pequeño: una fuerte devaluación del peso reduce el PIB en dólares y eleva la razón aunque el comercio no crezca.",
                "Los auges de precios de las materias primas inflan las exportaciones en valor y, con ellas, la apertura.",
                "Solo incluye bienes: no cuenta el comercio de servicios (turismo, transporte, servicios empresariales).",
                "Las importaciones incluyen fletes y seguros (CIF), lo que eleva un poco la franja naranja frente a una medición FOB."
            ],
            "formulas": [
                ["PIB en dólares de 4 trimestres", "Y$<sub>t</sub> = Σ<sub>j=0..3</sub> (PIB<sub>t−j</sub> ÷ TRM<sub>t−j</sub>)", "PIB = PIB nominal trimestral en pesos; TRM = promedio trimestral del tipo de cambio"],
                ["Apertura", "A<sub>t</sub> = (X4<sub>t</sub> + M4<sub>t</sub>) ÷ Y$<sub>t</sub> × 100", "X4 y M4 = exportaciones FOB e importaciones CIF de los últimos 4 trimestres completos, en dólares"]
            ]
        },
        "en": {
            "que": "This chart measures how open the Colombian economy is to goods trade: exports plus imports relative to the size of the economy (GDP). Colombia is a relatively closed economy compared with countries of similar size; the indicator shows whether that openness is rising or falling over time and how it responds to commodity price cycles and the exchange rate.",
            "leer": "Stacked areas as a percentage of GDP, quarterly, since 2005. Blue (bottom): FOB goods exports; orange (top): CIF imports. Both add up the last four complete quarters and are divided by nominal GDP for those same four quarters, converted to dollars with the average TRM (the official peso–dollar market exchange rate) of each quarter. The total height is goods trade openness.",
            "importa": "Openness shows how much production and consumption depend on foreign trade and, therefore, how exposed the economy is to external shocks and to the exchange rate. Greater integration tends to go with more competition, technology transfer and access to inputs. For an investor it helps size the weight of tradable sectors and the economy's sensitivity to world trade.",
            "interpretar": [
                "A rise may come from more trade in dollars or from smaller dollar GDP: a sharp peso depreciation shrinks dollar GDP and lifts the ratio even if trade does not grow.",
                "Commodity price booms inflate export values and, with them, openness.",
                "It covers goods only: trade in services (tourism, transport, business services) is not counted.",
                "Imports include freight and insurance (CIF), which slightly raises the orange band compared with an FOB measure."
            ],
            "formulas": [
                ["4-quarter dollar GDP", "Y$<sub>t</sub> = Σ<sub>j=0..3</sub> (GDP<sub>t−j</sub> ÷ TRM<sub>t−j</sub>)", "GDP = quarterly nominal GDP in pesos; TRM = quarterly average exchange rate"],
                ["Openness", "A<sub>t</sub> = (X4<sub>t</sub> + M4<sub>t</sub>) ÷ Y$<sub>t</sub> × 100", "X4 and M4 = FOB exports and CIF imports over the last 4 complete quarters, in dollars"]
            ]
        },
    },
    "g-com-diversificacion": {
        "es": {
            "que": "Mide qué tan repartidas están las exportaciones colombianas entre destinos y entre productos, con una medida muy usada en economía: el «número equivalente», que traduce la concentración a un número intuitivo de socios o productos de igual tamaño. Si Colombia vendiera lo mismo a cuatro destinos, el número sería 4; si vendiera todo a uno solo, sería 1. Muestra si la canasta y los mercados se diversifican o se concentran con el tiempo.",
            "leer": "Dos líneas desde 2005, con el eje en número equivalente. Línea azul: destinos, calculada sobre los 17 grupos del anexo de destinos del DANE (países individuales, la Unión Europea como bloque y «Resto»). Línea verde: productos, calculada sobre los cinco grupos del DANE (petróleo, carbón, café, ferroníquel y no tradicionales), por lo que su máximo posible es 5. Ambas usan participaciones de las sumas de 12 meses en dólares FOB.",
            "importa": "Una canasta y unos mercados diversificados hacen que los ingresos externos sean menos vulnerables a la caída de precios de un producto o a una recesión en un socio. La literatura sobre comercio y desarrollo asocia la diversificación con mayor estabilidad y con capacidades productivas más amplias. Para un inversionista, una mayor diversificación reduce la exposición de la economía a choques concentrados.",
            "interpretar": [
                "Una línea que sube indica exportaciones más repartidas; una que baja, más concentración en pocos destinos o productos.",
                "Durante auges del petróleo y el carbón, la línea de productos tiende a caer porque esos dos grupos dominan la canasta.",
                "Como la Unión Europea y «Resto» se cuentan como un solo destino cada uno, el número de destinos subestima la diversificación real por países.",
                "Con solo cinco grupos de productos, la medida es gruesa: no capta la diversificación dentro de los no tradicionales."
            ],
            "formulas": [
                ["Índice de Herfindahl", "H<sub>t</sub> = Σ<sub>i</sub> s<sub>i,t</sub><sup>2</sup>", "s<sub>i</sub> = participación (entre 0 y 1) del destino o producto i en las exportaciones de 12 meses"],
                ["Número equivalente", "N<sub>t</sub> = 1 ÷ H<sub>t</sub>", "número de destinos o productos de igual tamaño que daría la misma concentración"]
            ]
        },
        "en": {
            "que": "This chart measures how evenly Colombia's exports are spread across destinations and products, using a common economic measure: the 'equivalent number', which translates concentration into an intuitive number of equal-sized partners or products. If Colombia sold the same amount to four destinations, the number would be 4; if it sold everything to one, it would be 1. It shows whether the basket and markets are diversifying or concentrating over time.",
            "leer": "Two lines since 2005, with the axis in equivalent number. Blue line: destinations, computed over the 17 groups in DANE's destinations annex (individual countries, the European Union as a bloc and 'Rest'). Green line: products, computed over DANE's five groups (oil, coal, coffee, ferronickel and non-traditional), so its maximum possible value is 5. Both use shares of 12-month sums in FOB dollars.",
            "importa": "A diversified basket and set of markets make external income less vulnerable to a price fall in one product or a recession in one partner. The trade and development literature links diversification with greater stability and broader productive capabilities. For an investor, greater diversification reduces the economy's exposure to concentrated shocks.",
            "interpretar": [
                "A rising line means more evenly spread exports; a falling line, more concentration in a few destinations or products.",
                "During oil and coal booms the products line tends to fall because those two groups dominate the basket.",
                "Because the European Union and 'Rest' each count as a single destination, the destinations number understates true diversification across countries.",
                "With only five product groups the measure is coarse: it does not capture diversification within non-traditional exports."
            ],
            "formulas": [
                ["Herfindahl index", "H<sub>t</sub> = Σ<sub>i</sub> s<sub>i,t</sub><sup>2</sup>", "s<sub>i</sub> = share (between 0 and 1) of destination or product i in 12-month exports"],
                ["Equivalent number", "N<sub>t</sub> = 1 ÷ H<sub>t</sub>", "number of equal-sized destinations or products that would give the same concentration"]
            ]
        },
    },
    # =========================================================================================== EXTERNO
    "g-cc": {
        "es": {
            "que": "Muestra el saldo de la cuenta corriente de la balanza de pagos como porcentaje del PIB, trimestre a trimestre. La cuenta corriente registra todo lo que el país recibe y paga al exterior por bienes, servicios, rentas (utilidades e intereses) y transferencias (como remesas). Colombia ha tenido déficit casi de forma permanente: gasta e invierte más de lo que ahorra y cubre la diferencia con recursos del resto del mundo.",
            "leer": "Barras azules trimestrales en porcentaje del PIB, con una línea horizontal en cero. Una barra negativa es un déficit: el país usó más recursos externos de los que generó. La vista inicial cubre los últimos diez años y se puede ampliar hacia atrás. Al pasar el cursor se ve el trimestre y el cambio frente al mismo trimestre del año anterior, en puntos porcentuales (pp). Es el dato de un solo trimestre, por lo que es más volátil que la suma de cuatro trimestres del gráfico por componentes.",
            "importa": "La cuenta corriente es la medida central de la posición externa de una economía. Un déficit grande y persistente significa dependencia del financiamiento externo, lo que expone al país a cambios en el apetito global por riesgo, a salidas de capital y a presiones sobre la tasa de cambio. Las calificadoras y los inversionistas en deuda colombiana lo siguen de cerca; un déficit que se cierra reduce esas vulnerabilidades.",
            "interpretar": [
                "Barras menos negativas indican que el déficit se reduce; suele ocurrir cuando la demanda interna se enfría o cuando suben los precios de exportación.",
                "Un déficit financiado con inversión extranjera directa es más estable que uno financiado con flujos de cartera o deuda de corto plazo: vea el gráfico de entradas netas de capital.",
                "El dato trimestral tiene estacionalidad (por ejemplo, el giro de utilidades y dividendos se concentra en ciertos trimestres); compare siempre con el mismo trimestre del año anterior.",
                "El Banco de la República revisa las cifras de balanza de pagos, en especial las de los trimestres recientes."
            ],
            "formulas": [
                ["Cuenta corriente (% del PIB)", "CC%<sub>q</sub> = CC<sub>q</sub> ÷ PIB<sub>q</sub> × 100", "CC = bienes + servicios + ingreso primario + ingreso secundario del trimestre q; PIB del mismo trimestre (dato del Banco de la República)"],
                ["Cambio anual (al pasar el cursor)", "ΔCC%<sub>q</sub> = CC%<sub>q</sub> − CC%<sub>q−4</sub>", "en puntos porcentuales"]
            ]
        },
        "en": {
            "que": "This chart shows the current-account balance of the balance of payments as a percentage of GDP, quarter by quarter. The current account records everything the country receives from and pays to the rest of the world for goods, services, income (profits and interest) and transfers (such as remittances). Colombia has run a deficit almost continuously: it spends and invests more than it saves and covers the difference with resources from abroad.",
            "leer": "Blue quarterly bars as a percentage of GDP, with a horizontal line at zero. A negative bar is a deficit: the country used more external resources than it generated. The initial view covers the last ten years and can be zoomed back. Hovering shows the quarter and the change versus the same quarter a year earlier, in percentage points (pp). It is the figure for a single quarter, so it is more volatile than the four-quarter sum in the by-component chart.",
            "importa": "The current account is the central measure of an economy's external position. A large, persistent deficit means dependence on external financing, exposing the country to shifts in global risk appetite, capital outflows and exchange-rate pressure. Rating agencies and investors in Colombian debt watch it closely; a narrowing deficit reduces those vulnerabilities.",
            "interpretar": [
                "Less negative bars mean the deficit is shrinking; this usually happens when domestic demand cools or export prices rise.",
                "A deficit financed by foreign direct investment is more stable than one financed by portfolio flows or short-term debt: see the net capital inflows chart.",
                "The quarterly figure is seasonal (for example, profit and dividend remittances cluster in certain quarters); always compare with the same quarter a year earlier.",
                "Banco de la República revises balance-of-payments figures, especially for recent quarters."
            ],
            "formulas": [
                ["Current account (% of GDP)", "CA%<sub>q</sub> = CA<sub>q</sub> ÷ GDP<sub>q</sub> × 100", "CA = goods + services + primary income + secondary income in quarter q; GDP of the same quarter (Banco de la República figure)"],
                ["Annual change (on hover)", "ΔCA%<sub>q</sub> = CA%<sub>q</sub> − CA%<sub>q−4</sub>", "in percentage points"]
            ]
        },
    },
    "g-deuda": {
        "es": {
            "que": "Muestra la deuda bruta del Gobierno Nacional Central (GNC) como porcentaje del PIB al cierre de cada año. El GNC es el Gobierno central (ministerios y entidades que dependen del presupuesto nacional), sin gobiernos regionales ni empresas públicas. La serie permite ver los grandes episodios fiscales: la crisis de finales de los noventa, la reducción de la deuda durante la bonanza de materias primas y el salto de 2020 por la pandemia.",
            "leer": "Barras moradas anuales, en porcentaje del PIB, con una línea horizontal en cero. Cada barra es el saldo de la deuda bruta al 31 de diciembre de ese año, incluyendo deuda interna (principalmente TES, los bonos del Tesoro en pesos) y externa. Se muestra la historia completa desde mediados de los años noventa. Al pasar el cursor se ve el cambio frente al año anterior, en puntos porcentuales (pp).",
            "importa": "La deuda pública es el principal indicador de sostenibilidad fiscal. Un nivel alto o creciente aumenta el pago de intereses, reduce el margen del Gobierno para responder a crisis, puede elevar las tasas de interés de toda la economía y presiona la calificación crediticia del país. Para los inversionistas en TES y en bonos externos es la referencia básica del riesgo soberano.",
            "interpretar": [
                "La razón sube si la deuda crece más rápido que el PIB nominal: por déficit fiscales, por devaluación (que encarece en pesos la deuda en dólares) o por un crecimiento económico débil.",
                "Es deuda bruta: no descuenta los activos financieros ni los depósitos del Gobierno.",
                "La regla fiscal colombiana (Ley 2155 de 2021) toma como referencia la deuda neta del GNC, una medida distinta de la bruta que aquí se muestra.",
                "El mismo dato, con los años por encima de 60% del PIB resaltados, aparece en la sección de cuentas del Gobierno."
            ],
            "formulas": [
                ["Deuda bruta como % del PIB", "D%<sub>a</sub> = D<sub>a</sub> ÷ PIB<sub>a</sub> × 100", "D = saldo de la deuda bruta del GNC al cierre del año a (interna + externa, en pesos); PIB = PIB nominal del año"],
                ["Cambio anual (al pasar el cursor)", "ΔD%<sub>a</sub> = D%<sub>a</sub> − D%<sub>a−1</sub>", "en puntos porcentuales"]
            ]
        },
        "en": {
            "que": "This chart shows the gross debt of the Central National Government (GNC) as a percentage of GDP at the end of each year. The GNC is the central government (ministries and entities funded by the national budget), excluding regional governments and public companies. The series shows the major fiscal episodes: the late-1990s crisis, the debt reduction during the commodity boom and the 2020 jump caused by the pandemic.",
            "leer": "Annual purple bars, as a percentage of GDP, with a horizontal line at zero. Each bar is gross debt outstanding at 31 December of that year, including domestic debt (mainly TES, the peso-denominated Treasury bonds) and external debt. The full history since the mid-1990s is shown. Hovering shows the change versus the previous year, in percentage points (pp).",
            "importa": "Public debt is the main indicator of fiscal sustainability. A high or rising level increases interest payments, narrows the government's room to respond to crises, can raise interest rates across the economy and pressures the country's credit rating. For investors in TES and external bonds it is the basic benchmark of sovereign risk.",
            "interpretar": [
                "The ratio rises if debt grows faster than nominal GDP: because of fiscal deficits, depreciation (which raises the peso value of dollar debt) or weak growth.",
                "It is gross debt: it does not net out the government's financial assets or deposits.",
                "Colombia's fiscal rule (Law 2155 of 2021) targets the GNC's net debt, a different measure from the gross debt shown here.",
                "The same figure, with years above 60% of GDP highlighted, appears in the government accounts section."
            ],
            "formulas": [
                ["Gross debt as % of GDP", "D%<sub>a</sub> = D<sub>a</sub> ÷ GDP<sub>a</sub> × 100", "D = GNC gross debt outstanding at the end of year a (domestic + external, in pesos); GDP = nominal GDP for the year"],
                ["Annual change (on hover)", "ΔD%<sub>a</sub> = D%<sub>a</sub> − D%<sub>a−1</sub>", "in percentage points"]
            ]
        },
    },
    "g-ext-cc": {
        "es": {
            "que": "Descompone la cuenta corriente de la balanza de pagos en sus cuatro partes para mostrar de dónde viene el déficit externo de Colombia. Suele revelar que el mayor drenaje no está solo en el comercio de bienes, sino en el ingreso primario: las utilidades que las empresas extranjeras ganan en Colombia y los intereses de la deuda externa. Las remesas de los colombianos en el exterior, en cambio, compensan parte del déficit.",
            "leer": "Eje en miles de millones de dólares; cada punto suma los últimos cuatro trimestres, desde 2005. Barras apiladas: bienes (azul), servicios (morado), ingreso primario, es decir utilidades e intereses (naranja), e ingreso secundario, principalmente remesas (verde). Las barras por encima de cero aportan dólares y las de abajo los restan. La línea amarilla es la cuenta corriente total, igual a la suma de las cuatro barras. La línea horizontal marca el cero.",
            "importa": "Saber qué componente explica el déficit permite juzgar su naturaleza: un déficit de ingreso primario refleja el pago a la inversión extranjera acumulada, que tiende a moverse con la rentabilidad de las empresas (en especial petroleras y mineras); uno de bienes refleja la brecha entre gasto interno y producción. Para un inversionista ayuda a entender la demanda estructural de dólares y la sensibilidad del saldo externo al petróleo.",
            "interpretar": [
                "Si la barra naranja (ingreso primario) se agranda cuando suben los precios de las materias primas, es porque las empresas extranjeras del sector ganan y giran más utilidades.",
                "Un aumento de la barra verde (remesas) suaviza el déficit sin necesidad de financiación; vea el gráfico de remesas.",
                "La línea amarilla por debajo de cero es el déficit que debe financiarse con la cuenta financiera: compárela con el gráfico de entradas netas de capital.",
                "La balanza de pagos valora los bienes FOB en ambos lados, por lo que el saldo de bienes difiere del de la página de comercio (FOB − CIF)."
            ],
            "formulas": [
                ["Suma de 4 trimestres", "Z4<sub>q</sub> = Σ<sub>j=0..3</sub> Z<sub>q−j</sub>", "Z = cada componente (millones de dólares por trimestre); se grafica en miles de millones"],
                ["Identidad de la cuenta corriente", "CC4 = B4 + S4 + IP4 + IS4", "B = bienes; S = servicios; IP = ingreso primario; IS = ingreso secundario"]
            ]
        },
        "en": {
            "que": "This chart breaks the current account of the balance of payments into its four parts to show where Colombia's external deficit comes from. It usually reveals that the biggest drain is not only goods trade but primary income: the profits foreign companies earn in Colombia and interest on external debt. Remittances from Colombians abroad, by contrast, offset part of the deficit.",
            "leer": "Axis in billions of dollars; each point adds up the last four quarters, since 2005. Stacked bars: goods (blue), services (purple), primary income, i.e. profits and interest (orange), and secondary income, mainly remittances (green). Bars above zero bring in dollars and those below take them out. The yellow line is the total current account, equal to the sum of the four bars. The horizontal line marks zero.",
            "importa": "Knowing which component explains the deficit helps judge its nature: a primary-income deficit reflects payments on accumulated foreign investment, which tends to move with company profitability (especially oil and mining); a goods deficit reflects the gap between domestic spending and output. For an investor it clarifies the structural demand for dollars and the external balance's sensitivity to oil.",
            "interpretar": [
                "If the orange bar (primary income) grows when commodity prices rise, it is because foreign companies in the sector earn and remit more profits.",
                "A larger green bar (remittances) eases the deficit without requiring financing; see the remittances chart.",
                "The yellow line below zero is the deficit that must be financed through the financial account: compare with the net capital inflows chart.",
                "The balance of payments values goods FOB on both sides, so the goods balance differs from the one on the trade page (FOB − CIF)."
            ],
            "formulas": [
                ["4-quarter sum", "Z4<sub>q</sub> = Σ<sub>j=0..3</sub> Z<sub>q−j</sub>", "Z = each component (millions of dollars per quarter); plotted in billions"],
                ["Current-account identity", "CA4 = G4 + S4 + PI4 + SI4", "G = goods; S = services; PI = primary income; SI = secondary income"]
            ]
        },
    },
    "g-ext-xm": {
        "es": {
            "que": "Muestra las exportaciones y las importaciones de bienes de Colombia según la balanza de pagos del Banco de la República, sumando cuatro trimestres. Es la misma historia del comercio que cuenta la página de comercio, pero con la metodología de la balanza de pagos, que valora ambos flujos en FOB y es la que se usa para la cuenta corriente. La distancia entre las dos líneas es el saldo de bienes.",
            "leer": "Eje en miles de millones de dólares, desde 2005. Línea verde: exportaciones de bienes (crédito de la balanza de pagos); línea naranja: importaciones de bienes (débito). Cada punto es la suma de los cuatro trimestres que terminan en ese trimestre. Cuando la naranja está por encima de la verde, el país tiene déficit en bienes; la distancia vertical entre ambas es el tamaño de ese déficit, que corresponde a la barra azul del gráfico de componentes.",
            "importa": "El saldo de bienes es uno de los motores principales de la cuenta corriente y, por tanto, de la necesidad de financiamiento externo. Las exportaciones dependen sobre todo de los precios del petróleo y del carbón; las importaciones, del ciclo de la demanda interna y de la inversión. Para un inversionista, esta comparación explica buena parte de los movimientos del déficit externo y de la tasa de cambio.",
            "interpretar": [
                "Si las líneas se separan con la naranja arriba, el déficit en bienes se amplía; si se juntan, se reduce.",
                "Estas cifras difieren de las del DANE porque la balanza de pagos valora las importaciones FOB (sin fletes ni seguros) y ajusta por cobertura y cambio de propiedad de las mercancías.",
                "Las caídas simultáneas de ambas líneas, como en 2020, reflejan contracciones de la economía y del comercio mundial.",
                "Los datos trimestrales recientes son provisionales y se revisan."
            ],
            "formulas": [
                ["Suma de 4 trimestres", "X4<sub>q</sub> = Σ<sub>j=0..3</sub> X<sub>q−j</sub>; M4<sub>q</sub> = Σ<sub>j=0..3</sub> M<sub>q−j</sub>", "X = exportaciones de bienes; M = importaciones de bienes (balanza de pagos, FOB)"],
                ["Saldo de bienes", "B4<sub>q</sub> = X4<sub>q</sub> − M4<sub>q</sub>", "distancia vertical entre las líneas"]
            ]
        },
        "en": {
            "que": "This chart shows Colombia's goods exports and imports according to Banco de la República's balance of payments, adding up four quarters. It is the same trade story told on the trade page, but using balance-of-payments methodology, which values both flows FOB and is the basis for the current account. The gap between the two lines is the goods balance.",
            "leer": "Axis in billions of dollars, since 2005. Green line: goods exports (balance-of-payments credit); orange line: goods imports (debit). Each point is the sum of the four quarters ending in that quarter. When the orange line is above the green one, the country has a goods deficit; the vertical distance between them is the size of that deficit, which corresponds to the blue bar in the components chart.",
            "importa": "The goods balance is one of the main drivers of the current account and, therefore, of the need for external financing. Exports depend mostly on oil and coal prices; imports on the domestic demand and investment cycle. For an investor, this comparison explains much of the movement in the external deficit and the exchange rate.",
            "interpretar": [
                "If the lines move apart with orange on top, the goods deficit widens; if they converge, it narrows.",
                "These figures differ from DANE's because the balance of payments values imports FOB (without freight or insurance) and adjusts for coverage and change of ownership of goods.",
                "Simultaneous falls in both lines, as in 2020, reflect contractions in the economy and in world trade.",
                "Recent quarterly data are provisional and revised."
            ],
            "formulas": [
                ["4-quarter sum", "X4<sub>q</sub> = Σ<sub>j=0..3</sub> X<sub>q−j</sub>; M4<sub>q</sub> = Σ<sub>j=0..3</sub> M<sub>q−j</sub>", "X = goods exports; M = goods imports (balance of payments, FOB)"],
                ["Goods balance", "B4<sub>q</sub> = X4<sub>q</sub> − M4<sub>q</sub>", "vertical distance between the lines"]
            ]
        },
    },
    "g-ext-financiacion": {
        "es": {
            "que": "Muestra cómo se financia el déficit externo de Colombia: qué tipo de capital entra al país para cubrir lo que la cuenta corriente no alcanza a pagar. La historia habitual es que la inversión extranjera directa, la más estable, es la principal fuente, complementada por inversión de cartera (compras de TES y acciones por extranjeros) y préstamos, mientras el Banco de la República acumula o usa reservas internacionales.",
            "leer": "Barras apiladas en miles de millones de dólares, suma de cuatro trimestres, desde 2005. Cada barra es un tipo de flujo de la cuenta financiera con el signo invertido, de modo que positivo = entrada neta de financiación: inversión directa (azul), inversión de cartera (morado), otra inversión, sobre todo préstamos y depósitos (verde), derivados (amarillo) y reservas (naranja), donde un valor negativo indica acumulación de reservas. La línea gris punteada es el déficit corriente que hay que financiar.",
            "importa": "La calidad del financiamiento importa tanto como su monto: la inversión directa es de largo plazo y difícil de retirar, mientras que la de cartera y los préstamos de corto plazo pueden revertirse con rapidez ante cambios en el apetito por riesgo. Para un inversionista, una dependencia creciente de flujos volátiles aumenta la vulnerabilidad del peso y de los activos colombianos a choques globales.",
            "interpretar": [
                "Si la suma de barras positivas supera la línea punteada, entra más capital del necesario y la diferencia suele terminar en acumulación de reservas (barra naranja negativa).",
                "Una barra azul grande y estable es una señal de financiamiento de mejor calidad que una dependencia de cartera u otra inversión.",
                "Las barras no cuadran exactamente con la línea: faltan la cuenta de capital (pequeña) y los errores y omisiones de la balanza de pagos.",
                "Una inversión de cartera negativa indica que los extranjeros redujeron sus tenencias netas de bonos y acciones colombianos o que los residentes invirtieron más afuera."
            ],
            "formulas": [
                ["Entrada neta por tipo", "F<sub>i,q</sub> = −CF<sub>i,q</sub>", "CF<sub>i</sub> = cuenta financiera del tipo i con signo MBP6 (activos netos − pasivos netos); con signo invertido, positivo = entrada neta"],
                ["Suma de 4 trimestres", "F4<sub>i,q</sub> = Σ<sub>j=0..3</sub> F<sub>i,q−j</sub>", "i ∈ {directa, cartera, otra, derivados, reservas}"],
                ["Déficit a financiar (línea punteada)", "DEF4<sub>q</sub> = −CC4<sub>q</sub>", "CC4 = cuenta corriente de 4 trimestres"]
            ]
        },
        "en": {
            "que": "This chart shows how Colombia's external deficit is financed: what kind of capital comes into the country to cover what the current account cannot pay for. The usual story is that foreign direct investment, the most stable source, is the main one, complemented by portfolio investment (foreign purchases of TES and equities) and loans, while Banco de la República accumulates or draws down international reserves.",
            "leer": "Stacked bars in billions of dollars, four-quarter sum, since 2005. Each bar is a type of financial-account flow with its sign inverted, so positive = net inflow of financing: direct investment (blue), portfolio investment (purple), other investment, mainly loans and deposits (green), derivatives (yellow) and reserves (orange), where a negative value means reserve accumulation. The dotted grey line is the current-account deficit that must be financed.",
            "importa": "The quality of financing matters as much as its size: direct investment is long term and hard to withdraw, while portfolio flows and short-term loans can reverse quickly when risk appetite shifts. For an investor, growing reliance on volatile flows increases the vulnerability of the peso and Colombian assets to global shocks.",
            "interpretar": [
                "If the positive bars add up to more than the dotted line, more capital comes in than needed and the difference usually ends up as reserve accumulation (negative orange bar).",
                "A large, stable blue bar signals better-quality financing than reliance on portfolio or other investment.",
                "The bars do not match the line exactly: the (small) capital account and balance-of-payments errors and omissions are not shown.",
                "Negative portfolio investment means foreigners reduced their net holdings of Colombian bonds and equities or residents invested more abroad."
            ],
            "formulas": [
                ["Net inflow by type", "F<sub>i,q</sub> = −FA<sub>i,q</sub>", "FA<sub>i</sub> = financial account for type i with BPM6 sign (net assets − net liabilities); with sign inverted, positive = net inflow"],
                ["4-quarter sum", "F4<sub>i,q</sub> = Σ<sub>j=0..3</sub> F<sub>i,q−j</sub>", "i ∈ {direct, portfolio, other, derivatives, reserves}"],
                ["Deficit to finance (dotted line)", "DEF4<sub>q</sub> = −CA4<sub>q</sub>", "CA4 = 4-quarter current account"]
            ]
        },
    },
    "g-ext-ied-sectores": {
        "es": {
            "que": "Muestra en qué sectores de la economía colombiana invierten las empresas extranjeras: la inversión extranjera directa (IED, capital que entra para crear, comprar o ampliar empresas con control o influencia duradera) de los últimos cuatro trimestres frente a los cuatro anteriores. Suele resaltar el peso del petróleo, la minería y los servicios financieros y empresariales, y permite ver qué sectores ganan o pierden atractivo.",
            "leer": "Barras horizontales agrupadas, una pareja por sector, en millones de dólares. Barra azul: IED de los últimos cuatro trimestres; barra amarilla: IED de los cuatro trimestres anteriores. Los sectores se ordenan según el valor de los últimos cuatro trimestres, con el mayor arriba. Son flujos netos: una barra negativa indica que las desinversiones o los pagos de préstamos entre empresas relacionadas superaron a las nuevas entradas en ese sector.",
            "importa": "La IED es la fuente más estable de financiamiento externo y además trae tecnología, empleo y capacidad productiva. Su composición sectorial indica si el capital extranjero se concentra en actividades extractivas, sensibles a los precios de las materias primas, o se diversifica hacia servicios, industria y energía. Para un inversionista revela en qué sectores ven oportunidades las empresas multinacionales.",
            "interpretar": [
                "Si la barra azul supera a la amarilla, la IED en ese sector aumentó frente al año anterior; si es menor, se redujo.",
                "La IED en petróleo y minería suele moverse con los precios internacionales y con la reinversión de utilidades de las empresas del sector.",
                "Incluye la reinversión de utilidades: parte de la IED no es dinero nuevo que entra, sino ganancias que las filiales no giran al exterior.",
                "El total de la IED y su papel en la financiación del déficit se ven en el gráfico de entradas netas de capital."
            ],
            "formulas": [
                ["IED de los últimos 4 trimestres", "IED4<sub>s,q</sub> = Σ<sub>j=0..3</sub> IED<sub>s,q−j</sub>", "s = sector; q = último trimestre publicado; millones de dólares"],
                ["IED de los 4 trimestres anteriores", "IED4<sub>s,q−4</sub> = Σ<sub>j=4..7</sub> IED<sub>s,q−j</sub>", "mismo cálculo, desplazado un año"]
            ]
        },
        "en": {
            "que": "This chart shows which sectors of the Colombian economy foreign companies invest in: foreign direct investment (FDI, capital that comes in to create, buy or expand companies with lasting control or influence) over the last four quarters versus the previous four. It usually highlights the weight of oil, mining and financial and business services, and shows which sectors are gaining or losing appeal.",
            "leer": "Grouped horizontal bars, one pair per sector, in millions of dollars. Blue bar: FDI over the last four quarters; yellow bar: FDI over the previous four quarters. Sectors are sorted by the latest four-quarter value, with the largest at the top. These are net flows: a negative bar means divestments or repayments of intercompany loans exceeded new inflows in that sector.",
            "importa": "FDI is the most stable source of external financing and also brings technology, jobs and productive capacity. Its sector mix shows whether foreign capital is concentrated in extractive activities, sensitive to commodity prices, or is diversifying into services, manufacturing and energy. For an investor it reveals where multinational companies see opportunities.",
            "interpretar": [
                "If the blue bar exceeds the yellow one, FDI in that sector rose compared with the previous year; if smaller, it fell.",
                "FDI in oil and mining tends to move with world prices and with the sector's reinvested earnings.",
                "It includes reinvested earnings: part of FDI is not new money coming in but profits that subsidiaries do not send abroad.",
                "Total FDI and its role in financing the deficit appear in the net capital inflows chart."
            ],
            "formulas": [
                ["FDI over the last 4 quarters", "FDI4<sub>s,q</sub> = Σ<sub>j=0..3</sub> FDI<sub>s,q−j</sub>", "s = sector; q = latest quarter published; millions of dollars"],
                ["FDI over the previous 4 quarters", "FDI4<sub>s,q−4</sub> = Σ<sub>j=4..7</sub> FDI<sub>s,q−j</sub>", "same calculation, shifted one year"]
            ]
        },
    },
    "g-ext-remesas": {
        "es": {
            "que": "Muestra cuántos dólares envían a Colombia los colombianos que trabajan en el exterior (remesas de trabajadores) y qué tan importantes son frente al tamaño de la economía. Las remesas se han convertido en una de las principales fuentes de divisas del país, comparable con algunas de las mayores exportaciones, y sostienen el ingreso de muchos hogares, en especial en ciertas regiones.",
            "leer": "Línea verde (eje izquierdo): suma de los ingresos de remesas de los últimos 12 meses, en miles de millones de dólares. Línea morada punteada (eje derecho): esa misma suma como porcentaje del PIB en dólares, calculado con el PIB nominal de los últimos cuatro trimestres disponibles convertido con la TRM (tasa de cambio oficial) promedio de cada trimestre; mientras no se publica un trimestre nuevo de PIB, se usa el último disponible. La serie empieza en 2005.",
            "importa": "Las remesas son un flujo de dólares estable que no genera deuda ni obligaciones futuras, por lo que ayudan a cerrar el déficit de cuenta corriente y a sostener el consumo de los hogares receptores. Dependen sobre todo del mercado laboral de Estados Unidos y España, donde vive la mayoría de los emigrantes. Para un inversionista son un soporte del peso y del consumo interno.",
            "interpretar": [
                "Si la línea morada sube, las remesas pesan más en la economía; puede deberse a más envíos o a un PIB en dólares menor (por ejemplo, tras una devaluación).",
                "Un crecimiento sostenido suele reflejar más emigración o mejores condiciones laborales en los países de destino.",
                "Las remesas forman la mayor parte del ingreso secundario (barra verde) del gráfico de cuenta corriente por componentes.",
                "Los datos mensuales recientes son provisionales y el Banco de la República los revisa."
            ],
            "formulas": [
                ["Remesas de 12 meses", "R12<sub>t</sub> = Σ<sub>j=0..11</sub> R<sub>t−j</sub>", "R = ingresos mensuales de remesas de trabajadores, en dólares"],
                ["Remesas como % del PIB", "R%<sub>t</sub> = R12<sub>t</sub> ÷ Y$4 × 100", "Y$4 = PIB nominal de los últimos 4 trimestres disponibles, en dólares (Σ PIB<sub>q</sub> ÷ TRM<sub>q</sub>)"]
            ]
        },
        "en": {
            "que": "This chart shows how many dollars Colombians working abroad send home (workers' remittances) and how important they are relative to the size of the economy. Remittances have become one of the country's main sources of foreign currency, comparable to some of its largest exports, and support the income of many households, especially in certain regions.",
            "leer": "Green line (left axis): the sum of remittance inflows over the last 12 months, in billions of dollars. Dotted purple line (right axis): that same sum as a percentage of dollar GDP, computed with nominal GDP over the latest four available quarters converted at each quarter's average TRM (official exchange rate); until a new GDP quarter is published, the latest available one is used. The series starts in 2005.",
            "importa": "Remittances are a stable flow of dollars that creates no debt or future obligations, so they help close the current-account deficit and support consumption by receiving households. They depend mainly on labour markets in the United States and Spain, where most emigrants live. For an investor they underpin the peso and domestic consumption.",
            "interpretar": [
                "If the purple line rises, remittances weigh more in the economy; this may reflect larger transfers or smaller dollar GDP (for example, after a depreciation).",
                "Sustained growth usually reflects more emigration or better labour conditions in destination countries.",
                "Remittances make up most of secondary income (green bar) in the current account by component chart.",
                "Recent monthly data are provisional and revised by Banco de la República."
            ],
            "formulas": [
                ["12-month remittances", "R12<sub>t</sub> = Σ<sub>j=0..11</sub> R<sub>t−j</sub>", "R = monthly workers' remittance inflows, in dollars"],
                ["Remittances as % of GDP", "R%<sub>t</sub> = R12<sub>t</sub> ÷ Y$4 × 100", "Y$4 = nominal GDP over the latest 4 available quarters, in dollars (Σ GDP<sub>q</sub> ÷ TRM<sub>q</sub>)"]
            ]
        },
    },
    "g-ext-deuda": {
        "es": {
            "que": "Muestra cuánto debe Colombia al resto del mundo (deuda externa) y quién la debe: el sector público (Gobierno, entidades territoriales y empresas públicas) o el sector privado (empresas y bancos). También muestra el total en relación con el tamaño de la economía. Permite ver el aumento de la deuda externa en la última década y los cambios en su composición entre público y privado.",
            "leer": "Áreas apiladas (eje izquierdo) en miles de millones de dólares: azul, deuda externa pública; morado, deuda externa privada; la altura total es la deuda externa del país. Línea naranja (eje derecho, desde cero): deuda externa total como porcentaje del PIB, tal como la publica el Banco de la República. Son saldos mensuales desde 2005. Incluye préstamos y bonos emitidos en el exterior, de corto y largo plazo.",
            "importa": "La deuda externa debe pagarse en divisas, por lo que expone a los deudores a la tasa de cambio: una devaluación encarece su servicio en pesos. Un nivel alto como porcentaje del PIB aumenta la vulnerabilidad del país ante cierres de los mercados internacionales. Para un inversionista, la evolución de la deuda pública y privada indica el riesgo de refinanciación y la exposición cambiaria de la economía.",
            "interpretar": [
                "La línea naranja puede subir sin que aumente la deuda en dólares: basta con que el PIB medido en dólares caiga por una devaluación del peso.",
                "Si el área morada crece más rápido, el endeudamiento externo lo están impulsando las empresas y los bancos; si crece la azul, el sector público.",
                "Es deuda bruta: no descuenta los activos externos del país (como las reservas internacionales); el balance completo está en la posición de inversión internacional.",
                "Los saldos recientes son provisionales y pueden revisarse."
            ],
            "formulas": [
                ["Deuda externa total", "D<sub>t</sub> = D<sup>pública</sup><sub>t</sub> + D<sup>privada</sup><sub>t</sub>", "saldos al cierre del mes t, en dólares"],
                ["Deuda externa como % del PIB", "D%<sub>t</sub> = D<sub>t</sub> ÷ PIB$<sub>t</sub> × 100", "PIB$ = PIB en dólares; razón calculada y publicada por el Banco de la República"]
            ]
        },
        "en": {
            "que": "This chart shows how much Colombia owes the rest of the world (external debt) and who owes it: the public sector (government, territorial entities and public companies) or the private sector (firms and banks). It also shows the total relative to the size of the economy. It reveals the rise in external debt over the last decade and the shifts in its public–private mix.",
            "leer": "Stacked areas (left axis) in billions of dollars: blue, public external debt; purple, private external debt; the total height is the country's external debt. Orange line (right axis, from zero): total external debt as a percentage of GDP, as published by Banco de la República. These are monthly balances since 2005. It includes loans and bonds issued abroad, short and long term.",
            "importa": "External debt must be repaid in foreign currency, so it exposes debtors to the exchange rate: a depreciation makes servicing it more expensive in pesos. A high ratio to GDP increases the country's vulnerability if international markets close. For an investor, the path of public and private debt shows the refinancing risk and the economy's currency exposure.",
            "interpretar": [
                "The orange line can rise without any increase in dollar debt: a peso depreciation that lowers GDP measured in dollars is enough.",
                "If the purple area grows faster, firms and banks are driving external borrowing; if the blue grows, the public sector is.",
                "It is gross debt: it does not net out the country's external assets (such as international reserves); the full balance sheet is in the international investment position.",
                "Recent balances are provisional and may be revised."
            ],
            "formulas": [
                ["Total external debt", "D<sub>t</sub> = D<sup>public</sup><sub>t</sub> + D<sup>private</sup><sub>t</sub>", "balances at the end of month t, in dollars"],
                ["External debt as % of GDP", "D%<sub>t</sub> = D<sub>t</sub> ÷ GDP$<sub>t</sub> × 100", "GDP$ = GDP in dollars; ratio computed and published by Banco de la República"]
            ]
        },
    },
    "g-ext-pii": {
        "es": {
            "que": "Muestra el balance financiero de Colombia con el resto del mundo: la posición de inversión internacional (PII), que compara lo que los residentes colombianos poseen en el exterior (activos) con lo que los extranjeros poseen en Colombia o les presta (pasivos). Colombia es deudora neta: sus pasivos superan a sus activos, fruto de décadas de déficit en cuenta corriente financiados con inversión extranjera y deuda.",
            "leer": "Eje izquierdo en miles de millones de dólares: línea verde, activos externos (incluye reservas internacionales, inversiones de residentes y depósitos en el exterior); línea naranja, pasivos externos (inversión extranjera directa y de cartera en Colombia, préstamos y deuda). Eje derecho: línea morada punteada con la posición neta (activos menos pasivos) como porcentaje del PIB en dólares de los últimos cuatro trimestres. Saldos al cierre de cada trimestre desde 2005.",
            "importa": "La PII neta resume la deuda acumulada del país con el exterior en todas sus formas. Un saldo muy negativo implica pagos recurrentes de utilidades e intereses (el ingreso primario de la cuenta corriente) y mayor exposición a la confianza de los inversionistas extranjeros. Para un inversionista ayuda a evaluar la vulnerabilidad externa más allá de la deuda: buena parte de los pasivos colombianos es inversión directa, que no es deuda.",
            "interpretar": [
                "Si la distancia entre la línea naranja y la verde se amplía, el país se vuelve más deudor neto; la línea morada se hace más negativa.",
                "La posición cambia no solo por los flujos, sino por cambios de valoración: variaciones de la tasa de cambio y de los precios de acciones y bonos alteran activos y pasivos sin que haya transacciones.",
                "Una devaluación del peso reduce el valor en dólares de los pasivos en pesos (TES y acciones en manos de extranjeros), lo que puede mejorar la posición neta.",
                "Las reservas internacionales en meses de importaciones aparecen en la tarjeta de medidas de la página."
            ],
            "formulas": [
                ["Posición neta", "PII<sub>q</sub> = A<sub>q</sub> − P<sub>q</sub>", "A = activos financieros externos; P = pasivos financieros externos, al cierre del trimestre q"],
                ["Posición neta como % del PIB", "PII%<sub>q</sub> = PII<sub>q</sub> ÷ Y$4<sub>q</sub> × 100", "Y$4 = PIB nominal de 4 trimestres en dólares (Σ PIB ÷ TRM promedio de cada trimestre)"]
            ]
        },
        "en": {
            "que": "This chart shows Colombia's financial balance sheet with the rest of the world: the international investment position (IIP), which compares what Colombian residents own abroad (assets) with what foreigners own in Colombia or lend to it (liabilities). Colombia is a net debtor: its liabilities exceed its assets, the result of decades of current-account deficits financed with foreign investment and debt.",
            "leer": "Left axis in billions of dollars: green line, external assets (including international reserves, residents' investments and deposits abroad); orange line, external liabilities (foreign direct and portfolio investment in Colombia, loans and debt). Right axis: dotted purple line with the net position (assets minus liabilities) as a percentage of four-quarter dollar GDP. End-of-quarter balances since 2005.",
            "importa": "The net IIP sums up the country's accumulated obligations to the rest of the world in all forms. A very negative position implies recurring profit and interest payments (the current account's primary income) and greater exposure to foreign investor confidence. For an investor it helps assess external vulnerability beyond debt: a large part of Colombia's liabilities is direct investment, which is not debt.",
            "interpretar": [
                "If the gap between the orange and green lines widens, the country becomes more of a net debtor; the purple line becomes more negative.",
                "The position changes not only with flows but with valuation effects: moves in the exchange rate and in equity and bond prices change assets and liabilities without any transaction.",
                "A peso depreciation lowers the dollar value of peso liabilities (TES and equities held by foreigners), which can improve the net position.",
                "International reserves in months of imports appear in the page's measures card."
            ],
            "formulas": [
                ["Net position", "IIP<sub>q</sub> = A<sub>q</sub> − L<sub>q</sub>", "A = external financial assets; L = external financial liabilities, at the end of quarter q"],
                ["Net position as % of GDP", "IIP%<sub>q</sub> = IIP<sub>q</sub> ÷ Y$4<sub>q</sub> × 100", "Y$4 = 4-quarter nominal GDP in dollars (Σ GDP ÷ each quarter's average TRM)"]
            ]
        },
    },
    "g-fi-gobierno": {
        "es": {
            "que": "Muestra cuánto recauda, cuánto gasta y cuánto paga en intereses el Gobierno Nacional Central (GNC), en relación con el tamaño de la economía. La distancia entre gastos e ingresos es el déficit fiscal. Permite ver los grandes episodios fiscales: el aumento del gasto durante la pandemia de 2020, los efectos de las reformas tributarias sobre los ingresos y el peso creciente o decreciente de los intereses de la deuda.",
            "leer": "Tres líneas en porcentaje del PIB, desde 2005: ingresos (verde), gastos totales (naranja) e intereses de la deuda (morado), estos últimos incluidos dentro de los gastos. Las cifras son de caja (cuando el dinero efectivamente entra o sale). Para cada trimestre completo se suman los últimos cuatro trimestres de cada concepto y se dividen por el PIB nominal de esos mismos cuatro trimestres. Así se obtiene una cifra comparable a la anual en cada trimestre.",
            "importa": "La relación entre ingresos y gastos determina el déficit y, con él, la evolución de la deuda pública. Un gasto persistentemente superior a los ingresos obliga a endeudarse; un peso creciente de los intereses resta espacio a la inversión y al gasto social. Para un inversionista en TES y en bonos soberanos, estas cifras son la base para evaluar la sostenibilidad fiscal y el cumplimiento de la regla fiscal.",
            "interpretar": [
                "Si la brecha entre la línea naranja y la verde se amplía, el déficit fiscal crece; si se cierra, el Gobierno necesita menos financiamiento.",
                "Una línea morada en ascenso indica que la deuda o las tasas de interés pesan más en el presupuesto.",
                "Las cifras de caja pueden diferir de las de causación que publica el Ministerio de Hacienda por diferencias en el momento de registro de pagos e ingresos.",
                "Los ingresos tienen componentes extraordinarios (dividendos de Ecopetrol, ingresos petroleros, medidas temporales) que pueden moverlos sin cambios estructurales."
            ],
            "formulas": [
                ["Suma de 4 trimestres completos", "Z4<sub>q</sub> = Σ<sub>j=0..3</sub> Z<sub>q−j</sub>", "Z<sub>q</sub> = suma de los tres meses del trimestre q (solo trimestres completos); Z = ingresos, gastos o intereses"],
                ["Razón al PIB", "Z%<sub>q</sub> = Z4<sub>q</sub> ÷ PIB4<sub>q</sub> × 100", "PIB4 = PIB nominal de los mismos 4 trimestres, en pesos"]
            ]
        },
        "en": {
            "que": "This chart shows how much the Central National Government (GNC) collects, how much it spends and how much it pays in interest, relative to the size of the economy. The gap between spending and revenue is the fiscal deficit. It shows the major fiscal episodes: the spending surge during the 2020 pandemic, the effect of tax reforms on revenue and the rising or falling weight of debt interest.",
            "leer": "Three lines as a percentage of GDP, since 2005: revenue (green), total spending (orange) and debt interest (purple), the latter included within spending. Figures are on a cash basis (when money actually comes in or goes out). For each complete quarter, the last four quarters of each item are added up and divided by nominal GDP for those same four quarters. This yields a figure comparable to the annual one at every quarter.",
            "importa": "The relationship between revenue and spending determines the deficit and, with it, the path of public debt. Spending persistently above revenue forces borrowing; a rising interest burden squeezes investment and social spending. For investors in TES and sovereign bonds, these figures are the basis for assessing fiscal sustainability and compliance with the fiscal rule.",
            "interpretar": [
                "If the gap between the orange and green lines widens, the fiscal deficit is growing; if it narrows, the government needs less financing.",
                "A rising purple line means debt or interest rates weigh more on the budget.",
                "Cash figures may differ from the accrual figures published by the Ministry of Finance because of differences in when payments and revenue are recorded.",
                "Revenue has extraordinary components (Ecopetrol dividends, oil revenue, temporary measures) that can move it without structural change."
            ],
            "formulas": [
                ["Sum of 4 complete quarters", "Z4<sub>q</sub> = Σ<sub>j=0..3</sub> Z<sub>q−j</sub>", "Z<sub>q</sub> = sum of the three months of quarter q (complete quarters only); Z = revenue, spending or interest"],
                ["Ratio to GDP", "Z%<sub>q</sub> = Z4<sub>q</sub> ÷ GDP4<sub>q</sub> × 100", "GDP4 = nominal GDP for the same 4 quarters, in pesos"]
            ]
        },
    },
    "g-fi-balance": {
        "es": {
            "que": "Muestra el resultado fiscal del Gobierno Nacional Central: el balance total (ingresos menos gastos) y el balance primario (el mismo resultado sin contar los intereses de la deuda). El balance primario indica si el Gobierno cubre con sus ingresos el gasto corriente y de inversión antes de pagar la deuda; el total incluye el costo de la deuda acumulada. Permite ver episodios como el gran déficit de 2020 y los esfuerzos posteriores de ajuste.",
            "leer": "Dos líneas en porcentaje del PIB, desde 2005, con una línea horizontal en cero. Línea naranja: balance total. Línea azul: balance primario, igual al balance total más los intereses. Valores negativos son déficit y positivos superávit. Cifras de caja, sumando los últimos cuatro trimestres completos y dividiendo por el PIB nominal de esos mismos trimestres. La distancia entre las dos líneas es el pago de intereses.",
            "importa": "El balance primario es la variable clave de la sostenibilidad de la deuda: si es positivo y suficiente frente a la diferencia entre la tasa de interés y el crecimiento de la economía, la deuda como porcentaje del PIB tiende a estabilizarse o bajar. La regla fiscal colombiana (Ley 2155 de 2021) fija su meta sobre el balance primario neto estructural, una medida relacionada pero ajustada por el ciclo y los ingresos petroleros. Para un inversionista en deuda soberana es la medida más directa del esfuerzo fiscal del Gobierno.",
            "interpretar": [
                "Un balance primario positivo significa que el Gobierno genera recursos para pagar parte de los intereses; uno negativo, que se endeuda incluso para gastos distintos de la deuda.",
                "Si la distancia entre las líneas crece, los intereses pesan más en el déficit total.",
                "La deuda como porcentaje del PIB se estabiliza aproximadamente cuando el balance primario iguala (r − g) × deuda ÷ (1 + g), donde r es la tasa de interés implícita y g el crecimiento nominal.",
                "En cifras de caja, los intereses pueden mostrar meses con valores atípicos o negativos (por ejemplo, primas en colocaciones de bonos), lo que también afecta al balance primario."
            ],
            "formulas": [
                ["Balance total", "BT<sub>q</sub> = (I4<sub>q</sub> − G4<sub>q</sub>) ÷ PIB4<sub>q</sub> × 100", "I = ingresos; G = gastos totales (incluyen intereses); sumas de 4 trimestres"],
                ["Balance primario", "BP<sub>q</sub> = BT<sub>q</sub> + INT4<sub>q</sub> ÷ PIB4<sub>q</sub> × 100", "INT = intereses de la deuda en 4 trimestres"]
            ]
        },
        "en": {
            "que": "This chart shows the fiscal result of the Central National Government: the total balance (revenue minus spending) and the primary balance (the same result excluding debt interest). The primary balance shows whether the government covers current and investment spending with its revenue before paying its debt; the total balance includes the cost of accumulated debt. It shows episodes such as the large 2020 deficit and later consolidation efforts.",
            "leer": "Two lines as a percentage of GDP, since 2005, with a horizontal line at zero. Orange line: total balance. Blue line: primary balance, equal to the total balance plus interest. Negative values are deficits and positive values surpluses. Cash figures, adding up the last four complete quarters and dividing by nominal GDP for the same quarters. The gap between the two lines is interest payments.",
            "importa": "The primary balance is the key variable for debt sustainability: if it is positive and large enough relative to the gap between the interest rate and economic growth, debt as a share of GDP tends to stabilise or fall. Colombia's fiscal rule (Law 2155 of 2021) sets its target on the structural net primary balance, a related measure adjusted for the cycle and oil revenue. For a sovereign-debt investor it is the most direct measure of the government's fiscal effort.",
            "interpretar": [
                "A positive primary balance means the government generates resources to pay part of its interest; a negative one means it borrows even for non-debt spending.",
                "If the gap between the lines widens, interest weighs more on the total deficit.",
                "Debt as a share of GDP roughly stabilises when the primary balance equals (r − g) × debt ÷ (1 + g), where r is the implicit interest rate and g nominal growth.",
                "On a cash basis, interest can show unusual or negative months (for example, premiums on bond placements), which also affects the primary balance."
            ],
            "formulas": [
                ["Total balance", "TB<sub>q</sub> = (R4<sub>q</sub> − G4<sub>q</sub>) ÷ GDP4<sub>q</sub> × 100", "R = revenue; G = total spending (including interest); 4-quarter sums"],
                ["Primary balance", "PB<sub>q</sub> = TB<sub>q</sub> + INT4<sub>q</sub> ÷ GDP4<sub>q</sub> × 100", "INT = debt interest over 4 quarters"]
            ]
        },
    },
    "g-fi-deuda": {
        "es": {
            "que": "Muestra la deuda bruta del Gobierno Nacional Central (GNC) como porcentaje del PIB al cierre de cada año, resaltando los años en que superó el 60% del PIB. Resume la historia fiscal de tres décadas: el aumento de la deuda tras la crisis de finales de los noventa, su reducción en los años de bonanza, el nuevo ascenso tras la caída del petróleo y el salto de 2020 por la pandemia.",
            "leer": "Barras anuales en porcentaje del PIB, desde mediados de los años noventa. Barras azules: años con deuda igual o inferior al 60% del PIB; barras naranjas: años por encima de ese nivel. Cada barra es el saldo al 31 de diciembre de la deuda interna (principalmente TES, los bonos del Tesoro en pesos) y externa del GNC. Al pasar el cursor se ve el valor exacto de cada año.",
            "importa": "El nivel de deuda condiciona el costo de financiamiento del Gobierno, la calificación crediticia del país y el margen para responder a choques. El umbral de 60% del PIB es una referencia internacional habitual de deuda elevada para economías emergentes, usada aquí solo como guía visual. Para un inversionista en TES y bonos externos, la trayectoria de la deuda es el punto de partida del análisis de riesgo soberano.",
            "interpretar": [
                "Barras naranjas indican niveles de deuda que tradicionalmente se asocian a mayor riesgo para economías emergentes; el umbral es una referencia, no un límite legal.",
                "La deuda puede subir por déficit fiscales, por devaluación del peso (la deuda externa vale más en pesos) o por un crecimiento nominal débil.",
                "La regla fiscal colombiana fija su ancla sobre la deuda neta, no sobre la bruta; las dos medidas difieren por los activos financieros del Gobierno.",
                "El balance fiscal que explica los cambios de la deuda se ve en los gráficos de ingresos, gastos y balance."
            ],
            "formulas": [
                ["Deuda bruta como % del PIB", "D%<sub>a</sub> = D<sub>a</sub> ÷ PIB<sub>a</sub> × 100", "D = saldo de la deuda bruta del GNC al cierre del año a; PIB = PIB nominal del año"],
                ["Color de la barra", "naranja si D%<sub>a</sub> > 60; azul en otro caso", "umbral de referencia de 60% del PIB"]
            ]
        },
        "en": {
            "que": "This chart shows Central National Government (GNC) gross debt as a percentage of GDP at the end of each year, highlighting years in which it exceeded 60% of GDP. It summarises three decades of fiscal history: the debt build-up after the late-1990s crisis, its reduction during the boom years, the renewed rise after the oil price fall and the 2020 pandemic jump.",
            "leer": "Annual bars as a percentage of GDP, since the mid-1990s. Blue bars: years with debt at or below 60% of GDP; orange bars: years above that level. Each bar is the 31 December balance of the GNC's domestic debt (mainly TES, the peso-denominated Treasury bonds) and external debt. Hovering shows each year's exact value.",
            "importa": "The debt level shapes the government's funding cost, the country's credit rating and its room to respond to shocks. The 60%-of-GDP threshold is a common international benchmark for high debt in emerging economies, used here only as a visual guide. For investors in TES and external bonds, the debt path is the starting point of sovereign-risk analysis.",
            "interpretar": [
                "Orange bars indicate debt levels traditionally associated with higher risk for emerging economies; the threshold is a benchmark, not a legal limit.",
                "Debt can rise through fiscal deficits, peso depreciation (external debt is worth more in pesos) or weak nominal growth.",
                "Colombia's fiscal rule anchors on net debt, not gross debt; the two measures differ by the government's financial assets.",
                "The fiscal balance behind changes in debt is shown in the revenue, spending and balance charts."
            ],
            "formulas": [
                ["Gross debt as % of GDP", "D%<sub>a</sub> = D<sub>a</sub> ÷ GDP<sub>a</sub> × 100", "D = GNC gross debt outstanding at the end of year a; GDP = nominal GDP for the year"],
                ["Bar colour", "orange if D%<sub>a</sub> > 60; blue otherwise", "60%-of-GDP benchmark threshold"]
            ]
        },
    },
    "g-fi-financiamiento": {
        "es": {
            "que": "Muestra cómo cubre el Gobierno Nacional Central su déficit (con recursos internos o externos) y cuánto de sus ingresos se le va en pagar intereses de la deuda. El financiamiento interno proviene sobre todo de la colocación de TES (bonos del Tesoro en pesos) en el mercado local; el externo, de bonos en el exterior y créditos de organismos multilaterales. La línea de intereses mide la carga de la deuda sobre el presupuesto.",
            "leer": "Barras apiladas (eje izquierdo) en porcentaje del PIB, suma de cuatro trimestres completos sobre el PIB nominal de esos trimestres, desde 2005: financiamiento interno (azul) y externo (amarillo). Un valor negativo indica que en neto se pagó más deuda de esa fuente de la que se tomó. Por construcción, la suma de las dos barras equivale al déficit de caja. Línea naranja (eje derecho, desde cero): intereses pagados por cada $100 de ingresos del Gobierno en esos mismos cuatro trimestres.",
            "importa": "La mezcla entre financiamiento interno y externo determina la exposición del Gobierno a la tasa de cambio y su dependencia del mercado local de TES, donde también participan bancos, fondos de pensiones e inversionistas extranjeros. La carga de intereses sobre ingresos es un indicador directo de cuánta capacidad fiscal absorbe la deuda: cuanto mayor, menos espacio queda para otros gastos. Es una referencia básica para inversionistas en deuda pública.",
            "interpretar": [
                "Una línea naranja en ascenso indica que una parte creciente del recaudo se destina a intereses, por mayor deuda, tasas más altas o ingresos más débiles.",
                "Más financiamiento interno implica más oferta de TES en el mercado local, lo que puede presionar sus tasas; más financiamiento externo eleva la exposición a la tasa de cambio.",
                "Una barra externa negativa puede reflejar amortizaciones de deuda externa o su sustitución por deuda interna.",
                "Los intereses de caja tienen meses atípicos o negativos (por ejemplo, primas en colocaciones), por lo que este indicador puede quedar por debajo del costo de la deuda en causación que reporta el Ministerio de Hacienda."
            ],
            "formulas": [
                ["Financiamiento como % del PIB", "F%<sub>q</sub> = F4<sub>q</sub> ÷ PIB4<sub>q</sub> × 100", "F4 = financiamiento interno o externo de 4 trimestres completos; PIB4 = PIB nominal de los mismos trimestres"],
                ["Identidad de financiamiento", "F<sup>int</sup> + F<sup>ext</sup> = −BT", "BT = balance total de caja (negativo si hay déficit)"],
                ["Intereses por cada $100 de ingresos", "II<sub>q</sub> = INT4<sub>q</sub> ÷ I4<sub>q</sub> × 100", "INT4 = intereses; I4 = ingresos; ambos sumas de 4 trimestres"]
            ]
        },
        "en": {
            "que": "This chart shows how the Central National Government covers its deficit (with domestic or external resources) and how much of its revenue goes to paying debt interest. Domestic financing comes mostly from placing TES (peso Treasury bonds) in the local market; external financing from bonds issued abroad and loans from multilateral institutions. The interest line measures the debt burden on the budget.",
            "leer": "Stacked bars (left axis) as a percentage of GDP, sum of four complete quarters over nominal GDP for those quarters, since 2005: domestic financing (blue) and external financing (yellow). A negative value means more debt from that source was repaid than taken on, in net terms. By construction, the two bars add up to the cash deficit. Orange line (right axis, from zero): interest paid per $100 of government revenue over the same four quarters.",
            "importa": "The mix of domestic and external financing determines the government's exposure to the exchange rate and its reliance on the local TES market, where banks, pension funds and foreign investors also participate. The interest-to-revenue burden is a direct measure of how much fiscal capacity debt absorbs: the higher it is, the less room remains for other spending. It is a basic benchmark for public-debt investors.",
            "interpretar": [
                "A rising orange line means a growing share of revenue goes to interest, because of higher debt, higher rates or weaker revenue.",
                "More domestic financing means more TES supply in the local market, which can push up their yields; more external financing raises exposure to the exchange rate.",
                "A negative external bar may reflect repayment of external debt or its replacement with domestic debt.",
                "Cash interest has unusual or negative months (for example, premiums on placements), so this indicator may be below the accrual-basis debt cost reported by the Ministry of Finance."
            ],
            "formulas": [
                ["Financing as % of GDP", "F%<sub>q</sub> = F4<sub>q</sub> ÷ GDP4<sub>q</sub> × 100", "F4 = domestic or external financing over 4 complete quarters; GDP4 = nominal GDP for the same quarters"],
                ["Financing identity", "F<sup>dom</sup> + F<sup>ext</sup> = −TB", "TB = total cash balance (negative in deficit)"],
                ["Interest per $100 of revenue", "II<sub>q</sub> = INT4<sub>q</sub> ÷ R4<sub>q</sub> × 100", "INT4 = interest; R4 = revenue; both 4-quarter sums"]
            ]
        },
    },
}
