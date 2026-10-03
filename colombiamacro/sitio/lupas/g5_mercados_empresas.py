"""Lupas (explicaciones ampliadas) del grupo g5: la bolsa (COLCAP, equiponderado, 7 Magníficas, pesos, acciones y
sectores del índice), las 10.000 empresas más grandes (tamaño, rentabilidad, sectores, regiones, concentración),
financiación y registro mercantil (página Empresas), y el peso colombiano: TRM, tasa de cambio real, pares,
otras monedas, petróleo, balanza cambiaria, reservas y volatilidad (página Mercados). Español e inglés."""

LUPAS = {
    # =========================================================================================== BOLSA
    "g-bolsa": {
        "es": {
            "que": "Muestra la evolución del COLCAP, el índice de referencia de la Bolsa de Valores de Colombia (BVC), que resume el precio de las acciones más negociadas del país ponderadas por su valor de mercado. Es un termómetro del apetito de los inversionistas por las empresas colombianas listadas y de cómo el mercado valora sus utilidades presentes y futuras. Al no incluir dividendos, mide solo la ganancia o pérdida de precio.",
            "leer": "Panel superior: el nivel del COLCAP en puntos, con el último cierre de cada semana; el índice arrancó en enero de 2008 alrededor de 1.000 puntos. Panel inferior: barras con la variación porcentual frente a la misma semana un año antes, azules cuando el índice sube y naranjas cuando baja. La vista inicial abarca diez años y el selector de horizonte (3, 5, 10 años o todo) cambia la ventana; el recuadro flotante muestra el último dato y sus cambios.",
            "importa": "La bolsa refleja en tiempo casi real la confianza en las grandes empresas del país, buena parte de ellas bancos, petroleras y empresas de energía. Su desempeño influye en el costo del capital, en la riqueza de fondos de pensiones e inversionistas y en la percepción externa del riesgo Colombia. Para un inversionista extranjero, el rendimiento en dólares depende además de la tasa de cambio.",
            "interpretar": [
                "Una variación anual positiva indica que el índice vale más que hace un año en pesos; comparar con la inflación muestra si hubo ganancia real.",
                "El COLCAP no incluye dividendos: el rendimiento total para el accionista es mayor que el que muestra la línea, sobre todo en empresas que reparten mucho.",
                "Como pondera por capitalización, unas pocas empresas grandes dominan su movimiento; el gráfico equiponderado y el de pesos de esta página muestran cuánto.",
                "Para un inversionista en dólares, combine este gráfico con el de la TRM: si el peso se debilita, el rendimiento en dólares es menor que el que se ve en pesos.",
                "Caídas generales del mercado, como el desplome de 2020 por la pandemia, se ven como barras naranjas profundas y simultáneas en muchas bolsas emergentes."
            ],
            "formulas": [
                ["Variación anual", "g<sub>t</sub> = (P<sub>t</sub> ÷ P<sub>t−52</sub> − 1) × 100", "P<sub>t</sub> = último cierre del COLCAP en la semana t; t−52 = misma semana un año antes"],
                ["Índice de capitalización (esquema)", "I<sub>t</sub> = Σ<sub>i</sub> p<sub>i,t</sub> × q<sub>i</sub> ÷ D<sub>t</sub>", "p = precio de la acción i; q = acciones en circulación ajustadas; D = divisor que mantiene la continuidad del índice"]
            ],
        },
        "en": {
            "que": "Shows the COLCAP, the benchmark index of the Colombian Stock Exchange (BVC), which summarises the prices of the country's most traded shares weighted by their market value. It gauges investors' appetite for Colombia's listed companies and how the market values their current and future earnings. Because it excludes dividends, it measures price gains or losses only.",
            "leer": "Top panel: the COLCAP level in points, using the last close of each week; the index started in January 2008 at about 1,000 points. Bottom panel: bars with the percentage change against the same week a year earlier, blue when the index rises and orange when it falls. The initial view covers ten years and the horizon selector (3, 5, 10 years or all) changes the window; the floating box shows the latest value and its changes.",
            "importa": "The stock market reflects, almost in real time, confidence in the country's large companies, many of them banks, oil producers and utilities. Its performance affects the cost of capital, the wealth of pension funds and investors, and the external perception of Colombian risk. For a foreign investor, the dollar return also depends on the exchange rate.",
            "interpretar": [
                "A positive annual change means the index is worth more than a year ago in pesos; comparing it with inflation shows whether there was a real gain.",
                "The COLCAP excludes dividends: shareholders' total return is higher than the line shows, especially for high-payout companies.",
                "Because it is capitalisation-weighted, a few large firms drive its moves; the equal-weighted and weights charts on this page show by how much.",
                "For a dollar-based investor, read this chart together with the TRM: if the peso weakens, the dollar return is lower than the peso return.",
                "Broad market sell-offs, such as the 2020 pandemic collapse, appear as deep orange bars that coincide across many emerging markets."
            ],
            "formulas": [
                ["Annual change", "g<sub>t</sub> = (P<sub>t</sub> ÷ P<sub>t−52</sub> − 1) × 100", "P<sub>t</sub> = last COLCAP close in week t; t−52 = same week a year earlier"],
                ["Capitalisation index (outline)", "I<sub>t</sub> = Σ<sub>i</sub> p<sub>i,t</sub> × q<sub>i</sub> ÷ D<sub>t</sub>", "p = price of share i; q = adjusted shares outstanding; D = divisor that keeps the index continuous"]
            ],
        },
    },
    "g-indices": {
        "es": {
            "que": "Compara tres maneras de medir la bolsa colombiana: el COLCAP oficial, donde las empresas grandes pesan más; un índice equiponderado, donde todas las acciones de la canasta pesan lo mismo; y un índice de las 7 Magníficas, las siete empresas de mayor peso en el COLCAP, también con igual peso. La distancia entre las líneas revela si el mercado lo mueven unas pocas compañías o la mayoría de ellas.",
            "leer": "Panel superior: las tres series en base 100, re-basadas al primer dato visible del horizonte elegido (3, 5, 10 años o todo); azul es el COLCAP oficial, verde el equiponderado y naranja las 7 Magníficas. Una línea en 130 significa que ese índice subió 30% desde el inicio de la ventana. Panel inferior: líneas con la rentabilidad de 12 meses de cada índice, con los mismos colores, y una línea de referencia en cero. Datos semanales.",
            "importa": "Un índice dominado por pocas empresas expone al inversionista a sus riesgos particulares (petróleo, banca, energía) más que a la economía en general. Si el COLCAP sube más que el equiponderado, el avance se concentra en las grandes; si ocurre lo contrario, la mejora es más amplia. Esto ayuda a entender la amplitud del mercado y la diversificación real que ofrece la bolsa local.",
            "interpretar": [
                "COLCAP por encima del equiponderado: las acciones de mayor peso rindieron más que la acción típica; por debajo, rindieron menos.",
                "Las 7 Magníficas se recalculan con cada canasta vigente; su línea muestra cómo habrían rendido las líderes de hoy, no las de cada momento.",
                "El equiponderado se rebalancea cada semana (cada acción vuelve a pesar lo mismo), lo que no equivale a una cartera que se pueda replicar sin costos.",
                "Sesgo de supervivencia: se usa la canasta actual hacia atrás, de modo que se omiten empresas que salieron del índice, a menudo por mal desempeño.",
                "Ninguna de las tres series incluye dividendos; se descartan retornos semanales de más de ±60% por ser errores de precio de la fuente."
            ],
            "formulas": [
                ["Retorno semanal de cada acción", "r<sub>i,t</sub> = P<sub>i,t</sub> ÷ P<sub>i,t−1</sub> − 1", "P<sub>i,t</sub> = cierre de la acción i en la semana t; se descarta si |r| > 0,60"],
                ["Índice equiponderado", "E<sub>t</sub> = E<sub>t−1</sub> × (1 + (1/N<sub>t</sub>) × Σ<sub>i</sub> r<sub>i,t</sub>)", "N<sub>t</sub> = número de acciones con retorno válido en la semana t; para las 7 Magníficas solo se usan sus siete acciones"],
                ["Re-base al horizonte", "B<sub>t</sub> = 100 × X<sub>t</sub> ÷ X<sub>0</sub>", "X<sub>0</sub> = valor del índice en el primer dato visible del horizonte elegido"],
                ["Rentabilidad de 12 meses", "R<sub>t</sub> = (X<sub>t</sub> ÷ X<sub>t−52</sub> − 1) × 100", "X = nivel del índice; t−52 = misma semana un año antes"]
            ],
        },
        "en": {
            "que": "Compares three ways of measuring the Colombian stock market: the official COLCAP, where large companies weigh more; an equal-weighted index, where every share in the basket weighs the same; and a Magnificent 7 index of the seven companies with the largest COLCAP weights, also equally weighted. The distance between the lines shows whether the market is driven by a few companies or by most of them.",
            "leer": "Top panel: the three series indexed to 100, rebased to the first visible observation of the chosen horizon (3, 5, 10 years or all); blue is the official COLCAP, green the equal-weighted index and orange the Magnificent 7. A line at 130 means that index rose 30% since the start of the window. Bottom panel: lines with each index's 12-month return, in the same colours, with a zero reference line. Weekly data.",
            "importa": "An index dominated by a few companies exposes investors to their specific risks (oil, banking, energy) more than to the economy as a whole. If the COLCAP outperforms the equal-weighted index, gains are concentrated in the large names; if the opposite happens, the improvement is broader. This helps gauge market breadth and the real diversification the local exchange offers.",
            "interpretar": [
                "COLCAP above the equal-weighted line: the heaviest shares outperformed the typical share; below it, they underperformed.",
                "The Magnificent 7 are recomputed with each current basket; their line shows how today's leaders would have performed, not the leaders at each point in time.",
                "The equal-weighted index is rebalanced every week (each share returns to the same weight), which is not a portfolio that can be replicated without costs.",
                "Survivorship bias: the current basket is applied backwards, so companies that left the index, often after poor performance, are omitted.",
                "None of the three series includes dividends; weekly returns above ±60% are discarded as source price errors."
            ],
            "formulas": [
                ["Weekly return of each share", "r<sub>i,t</sub> = P<sub>i,t</sub> ÷ P<sub>i,t−1</sub> − 1", "P<sub>i,t</sub> = close of share i in week t; discarded if |r| > 0.60"],
                ["Equal-weighted index", "E<sub>t</sub> = E<sub>t−1</sub> × (1 + (1/N<sub>t</sub>) × Σ<sub>i</sub> r<sub>i,t</sub>)", "N<sub>t</sub> = number of shares with a valid return in week t; the Magnificent 7 index uses only its seven shares"],
                ["Rebasing to the horizon", "B<sub>t</sub> = 100 × X<sub>t</sub> ÷ X<sub>0</sub>", "X<sub>0</sub> = index value at the first visible observation of the chosen horizon"],
                ["12-month return", "R<sub>t</sub> = (X<sub>t</sub> ÷ X<sub>t−52</sub> − 1) × 100", "X = index level; t−52 = same week a year earlier"]
            ],
        },
    },
    "g-pesos": {
        "es": {
            "que": "Muestra cuánto pesa cada una de las 15 acciones más grandes dentro del COLCAP, según la composición diaria del fondo iShares MSCI COLCAP, que replica el índice. Permite ver de un vistazo qué tan concentrada está la bolsa colombiana y qué compañías determinan la mayor parte de su movimiento.",
            "leer": "Barras horizontales ordenadas de mayor a menor, una por acción (identificada por su código bursátil o ticker), con su peso en porcentaje del fondo. Las barras naranjas son las acciones de las 7 Magníficas, las siete empresas de mayor peso (si una empresa tiene acción ordinaria y preferencial, ambas barras aparecen en naranja y sus pesos se suman para elegir a las siete); las grises son las demás. Al pasar el cursor se ven el nombre de la empresa y su sector. La fecha del título es la de la canasta.",
            "importa": "El peso de una acción indica cuánto mueve al índice: si una acción pesa 20%, una caída de 10% en su precio resta cerca de 2% al COLCAP por sí sola. Para quien invierte a través de fondos que replican el índice, estos pesos son su exposición real a cada empresa y sector. Una canasta concentrada reduce la diversificación.",
            "interpretar": [
                "La suma de las barras naranjas muestra qué parte del índice depende de siete empresas; una cifra alta indica un mercado estrecho.",
                "Los pesos cambian todos los días con los precios: una acción que sube gana peso aunque no cambie la metodología.",
                "Son los pesos del fondo (solo acciones, sin el efectivo), que aproximan pero no son idénticos a los oficiales de la BVC; por eso pueden no sumar exactamente 100%.",
                "Compare con el gráfico de sectores del COLCAP: la concentración por empresa suele traducirse en concentración en servicios financieros y energía."
            ],
            "formulas": [
                ["Peso de una acción", "w<sub>i</sub> = V<sub>i</sub> ÷ Σ<sub>j</sub> V<sub>j</sub> × 100", "V<sub>i</sub> = valor de mercado de la posición del fondo en la acción i; Σ sobre todo el fondo"],
                ["Peso de una empresa (para elegir las 7)", "W<sub>e</sub> = Σ<sub>i ∈ e</sub> w<sub>i</sub>", "suma de los pesos de las clases de acción (ordinaria y preferencial) de la empresa e"],
                ["Aporte aproximado al índice", "ΔI ≈ w<sub>i</sub> × r<sub>i</sub>", "r<sub>i</sub> = variación del precio de la acción i; ΔI = efecto sobre el índice"]
            ],
        },
        "en": {
            "que": "Shows the weight of each of the 15 largest shares in the COLCAP, based on the daily holdings of the iShares MSCI COLCAP fund, which tracks the index. It shows at a glance how concentrated the Colombian stock market is and which companies drive most of its moves.",
            "leer": "Horizontal bars sorted from largest to smallest, one per share (identified by its ticker), with its weight as a percentage of the fund. Orange bars are the shares of the Magnificent 7, the seven companies with the largest weights (if a company has ordinary and preferred shares, both bars are orange and their weights are added to pick the seven); grey bars are the rest. Hovering shows the company name and sector. The date in the title is the basket date.",
            "importa": "A share's weight tells how much it moves the index: if a share weighs 20%, a 10% fall in its price alone takes about 2% off the COLCAP. For anyone investing through index-tracking funds, these weights are their actual exposure to each company and sector. A concentrated basket reduces diversification.",
            "interpretar": [
                "The sum of the orange bars shows how much of the index depends on seven companies; a high figure signals a narrow market.",
                "Weights change every day with prices: a share that rises gains weight even if the methodology does not change.",
                "These are the fund's weights (equities only, excluding cash), which approximate but are not identical to the official BVC weights, so they may not add up to exactly 100%.",
                "Compare with the COLCAP sector chart: concentration by company usually translates into concentration in financial services and energy."
            ],
            "formulas": [
                ["Weight of a share", "w<sub>i</sub> = V<sub>i</sub> ÷ Σ<sub>j</sub> V<sub>j</sub> × 100", "V<sub>i</sub> = market value of the fund's holding in share i; Σ over the whole fund"],
                ["Weight of a company (to pick the 7)", "W<sub>e</sub> = Σ<sub>i ∈ e</sub> w<sub>i</sub>", "sum of the weights of company e's share classes (ordinary and preferred)"],
                ["Approximate contribution to the index", "ΔI ≈ w<sub>i</sub> × r<sub>i</sub>", "r<sub>i</sub> = price change of share i; ΔI = effect on the index"]
            ],
        },
    },
    "g-em-acciones": {
        "es": {
            "que": "Muestra cuánto cambió en el último año el precio de cada empresa que forma parte del COLCAP. Mientras el índice resume el promedio ponderado, este gráfico revela la dispersión que hay debajo: cuántas empresas subieron, cuántas bajaron y cuáles explican el resultado del mercado.",
            "leer": "Una barra horizontal por empresa, ordenadas de la que más cayó a la que más subió, con la variación porcentual de su precio de cierre frente al de 52 semanas antes. Verde: el precio subió; naranja: bajó. La línea vertical marca el cero. Para empresas con varias clases de acción se usa la de mayor peso en el índice. Al pasar el cursor se ve el sector de la empresa.",
            "importa": "Un mercado donde suben casi todas las acciones refleja una mejora amplia de expectativas; uno donde el índice sube gracias a pocas empresas es más frágil y depende de factores específicos. Para el inversionista, la dispersión muestra el riesgo y la oportunidad de elegir acciones individuales frente a comprar el índice completo.",
            "interpretar": [
                "Cuente las barras verdes frente a las naranjas: es una medida simple de la amplitud del mercado.",
                "Una empresa con gran variación pero poco peso mueve poco el COLCAP; cruce este gráfico con el de pesos para saber cuáles importan para el índice.",
                "Son variaciones de precio sin dividendos: en empresas con dividendos altos, el rendimiento total para el accionista es mayor.",
                "La canasta es la vigente; una empresa recién incluida puede mostrar una variación de un periodo en que aún no estaba en el índice."
            ],
            "formulas": [
                ["Variación en 12 meses", "v<sub>i</sub> = (P<sub>i,t</sub> ÷ P<sub>i,t−52</sub> − 1) × 100", "P<sub>i,t</sub> = último cierre semanal de la acción principal de la empresa i; P<sub>i,t−52</sub> = último cierre disponible 364 días o más antes"]
            ],
        },
        "en": {
            "que": "Shows how much the share price of each company in the COLCAP changed over the past year. While the index summarises the weighted average, this chart reveals the dispersion beneath it: how many companies rose, how many fell and which ones explain the market's result.",
            "leer": "One horizontal bar per company, sorted from the largest fall to the largest gain, with the percentage change in its closing price against 52 weeks earlier. Green: the price rose; orange: it fell. The vertical line marks zero. For companies with several share classes, the class with the largest index weight is used. Hovering shows the company's sector.",
            "importa": "A market where almost every share rises reflects a broad improvement in expectations; one where the index rises thanks to a few companies is more fragile and depends on specific factors. For investors, the dispersion shows the risk and opportunity of picking individual shares versus buying the whole index.",
            "interpretar": [
                "Count green versus orange bars: it is a simple measure of market breadth.",
                "A company with a large change but a small weight barely moves the COLCAP; cross-check with the weights chart to see which ones matter for the index.",
                "These are price changes excluding dividends: for high-dividend companies, shareholders' total return is higher.",
                "The basket is the current one; a recently added company may show a change over a period when it was not yet in the index."
            ],
            "formulas": [
                ["12-month change", "v<sub>i</sub> = (P<sub>i,t</sub> ÷ P<sub>i,t−52</sub> − 1) × 100", "P<sub>i,t</sub> = latest weekly close of company i's main share; P<sub>i,t−52</sub> = latest close available 364 days or more earlier"]
            ],
        },
    },
    "g-em-colcap-sectores": {
        "es": {
            "que": "Muestra cómo se reparte el COLCAP entre sectores económicos, sumando los pesos de las acciones de cada sector en la canasta vigente. Deja ver que la bolsa colombiana no es una muestra representativa de la economía: está concentrada en pocos sectores, con un peso grande de servicios financieros y energía.",
            "leer": "Barras horizontales moradas, una por sector, ordenadas de menor a mayor, con el porcentaje del índice que representan sus acciones. Los sectores siguen la clasificación del proveedor del fondo iShares MSCI COLCAP (servicios financieros, energía, servicios públicos, materiales, inmobiliario y consumo, entre otros). Es una fotografía de la canasta actual, no una serie de tiempo.",
            "importa": "La composición sectorial determina a qué riesgos responde el índice: con mucho peso financiero y energético, el COLCAP es sensible a las tasas de interés, al crédito, al precio del petróleo y a la regulación. Para un inversionista, comprar el índice no equivale a comprar la economía colombiana, donde comercio, servicios e industria tienen un peso mucho mayor.",
            "interpretar": [
                "Un sector con más de un tercio del índice hace que su ciclo domine el desempeño del COLCAP.",
                "Compare con el gráfico de ingresos por sector de las 10.000 empresas: la bolsa sobrerrepresenta algunos sectores y casi no tiene comercio ni manufactura.",
                "Los pesos se mueven con los precios: si las acciones de un sector suben más que el resto, su participación aumenta sin que cambie la canasta.",
                "La clasificación sectorial es la del proveedor del fondo y puede diferir de la de la BVC o de la de Supersociedades."
            ],
            "formulas": [
                ["Peso de un sector", "S<sub>k</sub> = Σ<sub>i ∈ k</sub> w<sub>i</sub>", "w<sub>i</sub> = peso (%) de la acción i en el fondo; k = sector"]
            ],
        },
        "en": {
            "que": "Shows how the COLCAP is split across economic sectors, adding up the weights of each sector's shares in the current basket. It reveals that the Colombian stock market is not a representative sample of the economy: it is concentrated in a few sectors, with a large weight of financial services and energy.",
            "leer": "Purple horizontal bars, one per sector, sorted from smallest to largest, with the percentage of the index their shares represent. Sectors follow the classification of the iShares MSCI COLCAP fund provider (financial services, energy, utilities, materials, real estate and consumer, among others). It is a snapshot of the current basket, not a time series.",
            "importa": "Sector composition determines which risks the index responds to: with a heavy financial and energy weight, the COLCAP is sensitive to interest rates, credit, oil prices and regulation. For investors, buying the index is not the same as buying the Colombian economy, where commerce, services and manufacturing weigh much more.",
            "interpretar": [
                "A sector with more than a third of the index makes its cycle dominate COLCAP performance.",
                "Compare with the revenue-by-sector chart of the 10,000 companies: the exchange overrepresents some sectors and has almost no commerce or manufacturing.",
                "Weights move with prices: if a sector's shares outperform, its share rises without any change in the basket.",
                "The sector classification is the fund provider's and may differ from that of the BVC or the Superintendence of Companies."
            ],
            "formulas": [
                ["Sector weight", "S<sub>k</sub> = Σ<sub>i ∈ k</sub> w<sub>i</sub>", "w<sub>i</sub> = weight (%) of share i in the fund; k = sector"]
            ],
        },
    },
    # =========================================================================================== 10.000 EMPRESAS
    "g-em-tamano": {
        "es": {
            "que": "Muestra el tamaño agregado de las 10.000 empresas con más ingresos del país según la Superintendencia de Sociedades: cuánto venden (ingresos operacionales) y cuánto ganan (utilidad neta) cada año. Es la mejor aproximación disponible al pulso financiero del sector empresarial formal grande de Colombia.",
            "leer": "Eje horizontal: años de corte de los estados financieros (31 de diciembre). Barras azules: ingresos operacionales, en billones de pesos corrientes, eje izquierdo. Línea naranja con puntos: ganancia o pérdida neta agregada, en billones de pesos, eje derecho (que parte de cero y tiene otra escala). Las etiquetas muestran el valor de cada año.",
            "importa": "Los ingresos de estas empresas equivalen a una parte muy grande del PIB, de modo que su evolución refleja la demanda, los precios y la actividad del país. Las utilidades determinan la capacidad de invertir, pagar impuestos y dividendos y atender deudas. Para un inversionista, separar el crecimiento de las ventas del de las ganancias muestra si los márgenes se amplían o se estrechan.",
            "interpretar": [
                "Son pesos corrientes: parte del crecimiento de los ingresos es inflación; restando la inflación del año se obtiene el crecimiento real.",
                "La lista cambia cada año (entran y salen empresas), así que la comparación es entre las 10.000 más grandes de cada año, no entre las mismas empresas.",
                "Si las utilidades crecen menos que los ingresos, el margen neto cae; el gráfico de rentabilidad lo muestra directamente.",
                "Los precios del petróleo y de otras materias primas influyen mucho en el agregado por el peso de las grandes empresas mineras y energéticas.",
                "Excluye bancos y aseguradoras y a las empresas que no reportan a una superintendencia."
            ],
            "formulas": [
                ["Ingresos agregados", "I<sub>a</sub> = Σ<sub>j=1</sub><sup>10.000</sup> ingresos operacionales<sub>j,a</sub>", "j = empresa de la lista del año a"],
                ["Utilidades agregadas", "G<sub>a</sub> = Σ<sub>j</sub> ganancia (pérdida)<sub>j,a</sub>", "incluye las pérdidas de las empresas con resultado negativo"],
                ["Crecimiento real de los ingresos", "c<sup>real</sup> = (1 + c) ÷ (1 + π) − 1", "c = variación nominal anual de I; π = inflación promedio del año"]
            ],
        },
        "en": {
            "que": "Shows the aggregate size of the 10,000 companies with the most revenue in the country according to the Superintendence of Companies: how much they sell (operating revenue) and how much they earn (net profit) each year. It is the best available approximation to the financial pulse of Colombia's large formal business sector.",
            "leer": "Horizontal axis: financial-statement cut-off years (31 December). Blue bars: operating revenue, in trillions of current pesos, left axis. Orange line with markers: aggregate net profit or loss, in trillions of pesos, right axis (starting at zero, on a different scale). Labels show each year's value.",
            "importa": "These companies' revenue equals a very large share of GDP, so its evolution reflects demand, prices and activity in the country. Profits determine the capacity to invest, pay taxes and dividends and service debt. For investors, separating sales growth from profit growth shows whether margins are widening or narrowing.",
            "interpretar": [
                "Figures are in current pesos: part of revenue growth is inflation; netting out the year's inflation gives real growth.",
                "The list changes every year (companies enter and leave), so the comparison is between each year's 10,000 largest, not the same companies.",
                "If profits grow less than revenue, the net margin falls; the profitability chart shows it directly.",
                "Oil and other commodity prices strongly influence the aggregate because of the weight of large mining and energy companies.",
                "Banks and insurers, and firms that do not report to a superintendence, are excluded."
            ],
            "formulas": [
                ["Aggregate revenue", "I<sub>a</sub> = Σ<sub>j=1</sub><sup>10,000</sup> operating revenue<sub>j,a</sub>", "j = company in year a's list"],
                ["Aggregate profits", "G<sub>a</sub> = Σ<sub>j</sub> profit (loss)<sub>j,a</sub>", "includes losses of companies with a negative result"],
                ["Real revenue growth", "c<sup>real</sup> = (1 + c) ÷ (1 + π) − 1", "c = annual nominal change in I; π = average inflation of the year"]
            ],
        },
    },
    "g-em-razones": {
        "es": {
            "que": "Resume la salud financiera de las 10.000 empresas más grandes con tres razones calculadas sobre el agregado: el margen neto (cuánto queda de utilidad por cada peso vendido), la rentabilidad del patrimonio (lo que gana cada peso aportado por los dueños) y el endeudamiento (qué parte de los activos está financiada con deudas).",
            "leer": "Eje horizontal: años de corte. Eje vertical: porcentaje. Línea azul: margen neto; verde: rentabilidad del patrimonio (ROE, por su sigla en inglés); morada: endeudamiento. Cada punto lleva su valor. Las tres razones se calculan con las sumas del conjunto de empresas de cada año, no como promedio de las razones de cada empresa.",
            "importa": "Márgenes y rentabilidad altos indican capacidad para invertir y resistir choques; un endeudamiento creciente con rentabilidad decreciente es una combinación que eleva la fragilidad financiera, tema central en el seguimiento del Banco de la República. Para el inversionista, estas razones permiten comparar la rentabilidad empresarial con el costo del crédito y con el rendimiento de otros activos.",
            "interpretar": [
                "Un margen neto de 7% significa que de cada $100 vendidos quedan $7 de utilidad después de costos, intereses e impuestos.",
                "Si la rentabilidad del patrimonio está por debajo de las tasas de interés de los bonos públicos (TES), los accionistas obtienen menos que con un activo de bajo riesgo.",
                "Un endeudamiento de 60% indica que 60 de cada 100 pesos de activos se financian con pasivos; cambios de pocos puntos son relevantes porque la razón es muy estable.",
                "Al ser razones del agregado, las empresas más grandes pesan mucho; un sector con resultados extraordinarios puede mover todo el indicador.",
                "La lista cambia cada año, por lo que parte de la variación se debe a qué empresas entran y salen."
            ],
            "formulas": [
                ["Margen neto", "M = Σ ganancia ÷ Σ ingresos × 100", "sumas de las 10.000 empresas del año"],
                ["Rentabilidad del patrimonio", "ROE = Σ ganancia ÷ Σ patrimonio × 100", "patrimonio = activos − pasivos, al cierre del año"],
                ["Endeudamiento", "E = Σ pasivos ÷ Σ activos × 100", "proporción de los activos financiada con deudas"]
            ],
        },
        "en": {
            "que": "Summarises the financial health of the 10,000 largest companies with three ratios computed on the aggregate: the net margin (how much profit remains per peso sold), return on equity (what each peso contributed by owners earns) and leverage (which share of assets is financed with debt).",
            "leer": "Horizontal axis: cut-off years. Vertical axis: percent. Blue line: net margin; green: return on equity (ROE); purple: leverage. Each point carries its value. The three ratios are computed from the sums of each year's set of companies, not as an average of each company's ratios.",
            "importa": "High margins and returns signal the capacity to invest and withstand shocks; rising leverage with falling profitability is a combination that increases financial fragility, a key topic in Banco de la República's monitoring. For investors, these ratios allow comparing corporate profitability with the cost of credit and the return on other assets.",
            "interpretar": [
                "A 7% net margin means that out of every $100 sold, $7 of profit remains after costs, interest and taxes.",
                "If return on equity is below the yields on government bonds (TES), shareholders earn less than on a low-risk asset.",
                "Leverage of 60% means 60 of every 100 pesos of assets are financed with liabilities; changes of a few points matter because the ratio is very stable.",
                "Being aggregate ratios, the largest companies weigh heavily; one sector with extraordinary results can move the whole indicator.",
                "The list changes every year, so part of the change is due to which companies enter and leave."
            ],
            "formulas": [
                ["Net margin", "M = Σ profit ÷ Σ revenue × 100", "sums over the year's 10,000 companies"],
                ["Return on equity", "ROE = Σ profit ÷ Σ equity × 100", "equity = assets − liabilities, at year-end"],
                ["Leverage", "E = Σ liabilities ÷ Σ assets × 100", "share of assets financed with debt"]
            ],
        },
    },
    "g-em-sectores": {
        "es": {
            "que": "Muestra cómo se reparten los ingresos de las 10.000 empresas más grandes entre los seis macrosectores que define la Superintendencia de Sociedades: comercio, servicios, manufactura, minero e hidrocarburos, construcción y agropecuario. Indica qué actividades concentran el grueso de las ventas del sector empresarial formal grande en el último año disponible.",
            "leer": "Barras horizontales azules, una por macrosector, ordenadas de menor a mayor, con su participación en el total de ingresos operacionales del año (el año aparece en el título). Las participaciones suman 100%. Al pasar el cursor se ven los ingresos del sector en billones de pesos y su variación nominal frente al año anterior.",
            "importa": "La estructura sectorial de los ingresos muestra de qué depende el desempeño agregado de las empresas: un peso alto del sector minero e hidrocarburos liga los resultados a los precios internacionales, mientras que comercio y servicios dependen más de la demanda interna. Para un inversionista, permite dimensionar sectores y contrastar la economía real con la composición de la bolsa.",
            "interpretar": [
                "La participación es de ingresos, no de valor agregado: un sector con márgenes bajos y mucho volumen, como el comercio, pesa más aquí que en el PIB.",
                "La variación anual del cursor es nominal e incluye el efecto de qué empresas entran y salen de la lista.",
                "Compárelo con el gráfico de rentabilidad por sector: vender mucho no implica ganar mucho.",
                "La clasificación es la de Supersociedades (macrosector) y no coincide exactamente con las ramas del PIB del DANE."
            ],
            "formulas": [
                ["Participación en los ingresos", "p<sub>k</sub> = I<sub>k</sub> ÷ Σ<sub>k</sub> I<sub>k</sub> × 100", "I<sub>k</sub> = ingresos operacionales de las empresas del macrosector k en el año"],
                ["Variación anual (cursor)", "c<sub>k</sub> = (I<sub>k,a</sub> ÷ I<sub>k,a−1</sub> − 1) × 100", "a = último año; a−1 = año anterior"]
            ],
        },
        "en": {
            "que": "Shows how the revenue of the 10,000 largest companies is split across the six macro-sectors defined by the Superintendence of Companies: commerce, services, manufacturing, mining and oil, construction and agriculture. It indicates which activities account for the bulk of large formal-sector sales in the latest available year.",
            "leer": "Blue horizontal bars, one per macro-sector, sorted from smallest to largest, with its share of the year's total operating revenue (the year is in the title). Shares add up to 100%. Hovering shows the sector's revenue in COP trillion and its nominal change against the previous year.",
            "importa": "The sector structure of revenue shows what aggregate corporate performance depends on: a large mining and oil share ties results to international prices, while commerce and services depend more on domestic demand. For investors, it helps size sectors and contrast the real economy with the composition of the stock market.",
            "interpretar": [
                "The share is of revenue, not value added: a high-volume, low-margin sector such as commerce weighs more here than in GDP.",
                "The annual change shown on hover is nominal and includes the effect of companies entering and leaving the list.",
                "Compare with the profitability-by-sector chart: selling a lot does not mean earning a lot.",
                "The classification is the Superintendence's (macro-sector) and does not match DANE's GDP branches exactly."
            ],
            "formulas": [
                ["Revenue share", "p<sub>k</sub> = I<sub>k</sub> ÷ Σ<sub>k</sub> I<sub>k</sub> × 100", "I<sub>k</sub> = operating revenue of companies in macro-sector k in the year"],
                ["Annual change (hover)", "c<sub>k</sub> = (I<sub>k,a</sub> ÷ I<sub>k,a−1</sub> − 1) × 100", "a = latest year; a−1 = previous year"]
            ],
        },
    },
    "g-em-sectores-rentabilidad": {
        "es": {
            "que": "Compara la rentabilidad de los seis macrosectores de Supersociedades en el último año disponible con dos medidas: el margen neto (utilidad sobre ingresos) y la rentabilidad del patrimonio (utilidad sobre patrimonio). Muestra qué actividades convierten mejor sus ventas y su capital en ganancias.",
            "leer": "Para cada macrosector hay dos barras horizontales: azul para el margen neto y verde para la rentabilidad del patrimonio, en porcentaje. Los sectores están ordenados por margen neto, de menor a mayor. La línea vertical marca el cero; una barra a la izquierda indica pérdidas agregadas en ese sector. El año aparece en el título.",
            "importa": "Las diferencias de rentabilidad entre sectores orientan la asignación de capital: los sectores más rentables atraen inversión y crédito, y los menos rentables enfrentan presión para ajustarse. Sectores como el minero suelen tener márgenes altos y volátiles, ligados a los precios internacionales, mientras que el comercio opera con márgenes estrechos y alta rotación.",
            "interpretar": [
                "Margen bajo con rentabilidad del patrimonio alta es típico de negocios de mucho volumen y poco capital (comercio); margen alto con rentabilidad moderada, de negocios intensivos en capital.",
                "Una rentabilidad del patrimonio por encima del margen indica que las ventas superan al patrimonio (alta rotación o mayor apalancamiento).",
                "Son razones del agregado de cada sector: una o dos empresas muy grandes pueden determinar el resultado del sector minero o de construcción.",
                "Es un solo año; la rentabilidad de sectores ligados a materias primas cambia mucho de un año a otro."
            ],
            "formulas": [
                ["Margen neto del sector", "M<sub>k</sub> = Σ<sub>j ∈ k</sub> ganancia<sub>j</sub> ÷ Σ<sub>j ∈ k</sub> ingresos<sub>j</sub> × 100", "k = macrosector; j = empresa"],
                ["Rentabilidad del patrimonio del sector", "ROE<sub>k</sub> = Σ<sub>j ∈ k</sub> ganancia<sub>j</sub> ÷ Σ<sub>j ∈ k</sub> patrimonio<sub>j</sub> × 100", "patrimonio al cierre del año"],
                ["Relación entre ambas", "ROE = M × (ingresos ÷ patrimonio)", "la rotación del patrimonio explica la diferencia entre las dos barras"]
            ],
        },
        "en": {
            "que": "Compares the profitability of the Superintendence's six macro-sectors in the latest available year using two measures: net margin (profit over revenue) and return on equity (profit over equity). It shows which activities best turn their sales and capital into profits.",
            "leer": "Each macro-sector has two horizontal bars: blue for net margin and green for return on equity, in percent. Sectors are sorted by net margin, from lowest to highest. The vertical line marks zero; a bar to the left indicates aggregate losses in that sector. The year is in the title.",
            "importa": "Profitability gaps between sectors guide capital allocation: the most profitable sectors attract investment and credit, and the least profitable face pressure to adjust. Sectors such as mining tend to have high and volatile margins tied to international prices, while commerce operates with thin margins and high turnover.",
            "interpretar": [
                "A low margin with high return on equity is typical of high-volume, low-capital businesses (commerce); a high margin with moderate ROE, of capital-intensive ones.",
                "Return on equity above the margin indicates that sales exceed equity (high turnover or more leverage).",
                "These are aggregate ratios per sector: one or two very large companies can determine the result of mining or construction.",
                "It is a single year; the profitability of commodity-linked sectors changes a lot from year to year."
            ],
            "formulas": [
                ["Sector net margin", "M<sub>k</sub> = Σ<sub>j ∈ k</sub> profit<sub>j</sub> ÷ Σ<sub>j ∈ k</sub> revenue<sub>j</sub> × 100", "k = macro-sector; j = company"],
                ["Sector return on equity", "ROE<sub>k</sub> = Σ<sub>j ∈ k</sub> profit<sub>j</sub> ÷ Σ<sub>j ∈ k</sub> equity<sub>j</sub> × 100", "equity at year-end"],
                ["Link between both", "ROE = M × (revenue ÷ equity)", "equity turnover explains the gap between the two bars"]
            ],
        },
    },
    "g-em-regiones": {
        "es": {
            "que": "Muestra cómo se distribuyen las 10.000 empresas más grandes entre las regiones del país, tanto por sus ingresos como por el número de empresas, según el domicilio que registran ante Supersociedades. Hace visible la fuerte concentración geográfica de la actividad empresarial grande en Bogotá y Cundinamarca y en Antioquia.",
            "leer": "Para cada región hay dos barras horizontales: azul con su participación en los ingresos totales y amarilla con su participación en el número de empresas, ambas en porcentaje del total. Las regiones (Bogotá-Cundinamarca, Antioquia, Costa Atlántica, Región Caribe, Costa Pacífica, Eje Cafetero, Centro-Oriente, Centro-Sur, Llanos y otras) son las que define Supersociedades y están ordenadas por ingresos. El año aparece en el título.",
            "importa": "La concentración regional determina dónde se generan empleo formal, recaudo e inversión empresarial, y explica parte de las brechas de desarrollo entre regiones. Que una región tenga más participación en ingresos que en número de empresas indica que allí se ubican las compañías de mayor tamaño.",
            "interpretar": [
                "Barra azul más larga que la amarilla: las empresas de esa región son, en promedio, más grandes que las del resto.",
                "Las cifras se asignan al domicilio de la empresa, no a donde produce: una petrolera con sede en Bogotá suma sus ingresos a Bogotá aunque extraiga en los Llanos.",
                "Por ese sesgo de sede, la concentración en la capital es mayor que la que mostraría el PIB departamental del DANE.",
                "Es una sola fotografía anual; la clasificación regional es la de Supersociedades."
            ],
            "formulas": [
                ["Participación en ingresos", "p<sup>I</sup><sub>r</sub> = I<sub>r</sub> ÷ Σ<sub>r</sub> I<sub>r</sub> × 100", "I<sub>r</sub> = ingresos de las empresas domiciliadas en la región r"],
                ["Participación en número de empresas", "p<sup>N</sup><sub>r</sub> = N<sub>r</sub> ÷ 10.000 × 100", "N<sub>r</sub> = número de empresas de la región r en la lista"],
                ["Tamaño relativo", "T<sub>r</sub> = p<sup>I</sup><sub>r</sub> ÷ p<sup>N</sup><sub>r</sub>", "mayor que 1 = empresas más grandes que el promedio"]
            ],
        },
        "en": {
            "que": "Shows how the 10,000 largest companies are distributed across the country's regions, both by revenue and by number of companies, according to the registered address they report to the Superintendence of Companies. It makes visible the strong geographic concentration of large business activity in Bogotá-Cundinamarca and Antioquia.",
            "leer": "Each region has two horizontal bars: blue with its share of total revenue and yellow with its share of the number of companies, both as a percentage of the total. Regions (Bogotá-Cundinamarca, Antioquia, Atlantic coast, Caribbean region, Pacific coast, Coffee axis, Centre-East, Centre-South, Llanos and other) are those defined by the Superintendence and are sorted by revenue. The year is in the title.",
            "importa": "Regional concentration determines where formal employment, tax revenue and corporate investment are generated, and explains part of the development gaps between regions. A region with a larger share of revenue than of companies hosts the biggest firms.",
            "interpretar": [
                "Blue bar longer than the yellow one: companies in that region are, on average, larger than elsewhere.",
                "Figures are assigned to the company's registered address, not where it produces: an oil company headquartered in Bogotá adds its revenue to Bogotá even if it extracts in the Llanos.",
                "Because of this headquarters bias, concentration in the capital is higher than DANE's departmental GDP would show.",
                "It is a single annual snapshot; the regional classification is the Superintendence's."
            ],
            "formulas": [
                ["Revenue share", "p<sup>I</sup><sub>r</sub> = I<sub>r</sub> ÷ Σ<sub>r</sub> I<sub>r</sub> × 100", "I<sub>r</sub> = revenue of companies registered in region r"],
                ["Share of companies", "p<sup>N</sup><sub>r</sub> = N<sub>r</sub> ÷ 10,000 × 100", "N<sub>r</sub> = number of companies of region r in the list"],
                ["Relative size", "T<sub>r</sub> = p<sup>I</sup><sub>r</sub> ÷ p<sup>N</sup><sub>r</sub>", "above 1 = companies larger than average"]
            ],
        },
    },
    "g-em-concentracion": {
        "es": {
            "que": "Es una curva de concentración: muestra qué porcentaje de los ingresos de las 10.000 empresas más grandes generan las N mayores, desde las 10 primeras hasta las 10.000. Compara el primer y el último año disponibles para ver si la actividad empresarial se ha concentrado más o menos en pocas compañías.",
            "leer": "Eje horizontal: número de empresas más grandes (N = 10, 50, 100, 500, 1.000, 2.500, 5.000 y 10.000), en escala logarítmica para que se vean bien tanto las primeras como las últimas. Eje vertical: porcentaje acumulado de los ingresos, de 0 a 100%. Línea azul gruesa: último año; línea amarilla delgada: primer año de la serie. Por construcción, ambas terminan en 100% con N = 10.000.",
            "importa": "Una economía donde pocas empresas generan buena parte de las ventas es más sensible a los choques de esas compañías: lo que les pase se transmite al empleo, al recaudo y al crecimiento agregado (los llamados orígenes granulares de las fluctuaciones). La concentración también se relaciona con el poder de mercado y la competencia.",
            "interpretar": [
                "Una curva más alta indica más concentración: las N mayores se quedan con una parte más grande de los ingresos.",
                "Si la línea azul está por encima de la amarilla, la concentración aumentó entre el primer y el último año; si está por debajo, disminuyó.",
                "Los precios del petróleo afectan esta medida: cuando suben, la mayor empresa del país gana participación y la curva sube en su tramo inicial.",
                "Mide concentración dentro de las 10.000, no en toda la economía, ni por mercado o producto."
            ],
            "formulas": [
                ["Participación acumulada", "C<sub>N</sub> = Σ<sub>j=1</sub><sup>N</sup> I<sub>(j)</sub> ÷ Σ<sub>j=1</sub><sup>10.000</sup> I<sub>(j)</sub> × 100", "I<sub>(j)</sub> = ingresos de la empresa que ocupa el puesto j, ordenadas de mayor a menor"]
            ],
        },
        "en": {
            "que": "A concentration curve: it shows what percentage of the revenue of the 10,000 largest companies is generated by the N largest, from the top 10 up to all 10,000. It compares the first and the latest available years to see whether business activity has become more or less concentrated in a few companies.",
            "leer": "Horizontal axis: number of largest companies (N = 10, 50, 100, 500, 1,000, 2,500, 5,000 and 10,000), on a log scale so both the first and the last are visible. Vertical axis: cumulative share of revenue, from 0 to 100%. Thick blue line: latest year; thin yellow line: first year in the series. By construction, both end at 100% at N = 10,000.",
            "importa": "An economy where a few companies generate much of sales is more sensitive to shocks to those firms: what happens to them passes through to employment, tax revenue and aggregate growth (the so-called granular origins of fluctuations). Concentration is also related to market power and competition.",
            "interpretar": [
                "A higher curve means more concentration: the top N take a larger share of revenue.",
                "If the blue line is above the yellow one, concentration rose between the first and latest year; if below, it fell.",
                "Oil prices affect this measure: when they rise, the country's largest company gains share and the start of the curve rises.",
                "It measures concentration within the 10,000, not in the whole economy, nor by market or product."
            ],
            "formulas": [
                ["Cumulative share", "C<sub>N</sub> = Σ<sub>j=1</sub><sup>N</sup> I<sub>(j)</sub> ÷ Σ<sub>j=1</sub><sup>10,000</sup> I<sub>(j)</sub> × 100", "I<sub>(j)</sub> = revenue of the company ranked j, sorted from largest to smallest"]
            ],
        },
    },
    # =========================================================================================== FINANCIACION Y REGISTRO
    "g-em-credito": {
        "es": {
            "que": "Muestra cuánto crece el crédito bancario a las empresas descontada la inflación y cuánto cuesta. Compara la cartera comercial (préstamos en pesos a empresas) con la cartera total del sistema y las tasas de interés de los créditos preferencial (a grandes empresas de bajo riesgo) y ordinario. Es un indicador de cómo se transmite la política monetaria a la financiación empresarial.",
            "leer": "Eje izquierdo, líneas sólidas: crecimiento real anual del saldo de la cartera comercial (azul, gruesa) y de la cartera total (morada), en porcentaje; la línea horizontal marca el cero. Eje derecho, líneas punteadas: tasa del crédito preferencial o corporativo (naranja) y del ordinario (amarilla), en porcentaje efectivo anual, promedio mensual de los datos semanales. Datos mensuales desde 2008.",
            "importa": "El crédito financia capital de trabajo e inversión: cuando su crecimiento real cae por debajo de cero, las empresas en conjunto están reduciendo su deuda bancaria real, lo que suele acompañar fases de menor inversión. Las tasas muestran el costo de esa financiación y responden, con rezago, a la tasa de política monetaria (TPM) del Banco de la República.",
            "interpretar": [
                "Crecimiento real negativo significa que el saldo de crédito crece menos que la inflación, aunque en pesos corrientes siga aumentando.",
                "Tasas en alza con crédito desacelerándose son típicas de una política monetaria restrictiva; la combinación inversa, de una política expansiva.",
                "La tasa preferencial es menor que la ordinaria porque se otorga a clientes de menor riesgo; la brecha entre ambas refleja la percepción de riesgo.",
                "Compare con el gráfico de la TPM en la página de tasas: las tasas de colocación siguen a la de política con meses de rezago.",
                "La cartera es en moneda legal (pesos): no incluye préstamos en dólares, bonos corporativos ni crédito de proveedores."
            ],
            "formulas": [
                ["Crecimiento real anual del saldo", "g<sup>real</sup><sub>t</sub> = [(1 + g<sub>t</sub>) ÷ (1 + π<sub>t</sub>) − 1] × 100", "g<sub>t</sub> = S<sub>t</sub> ÷ S<sub>t−12</sub> − 1, con S = saldo de cartera del mes t; π<sub>t</sub> = inflación anual del IPC del mes t"],
                ["Tasa mensual", "i<sub>m</sub> = (1/n) × Σ<sub>s</sub> i<sub>s</sub>", "i<sub>s</sub> = tasa efectiva anual de la semana s del mes; n = semanas con dato"]
            ],
        },
        "en": {
            "que": "Shows how fast bank credit to companies grows after inflation and how much it costs. It compares commercial loans (peso lending to companies) with total system loans and with the interest rates on preferential (to large, low-risk companies) and ordinary loans. It indicates how monetary policy passes through to corporate financing.",
            "leer": "Left axis, solid lines: annual real growth of the commercial loan stock (thick blue) and total loans (purple), in percent; the horizontal line marks zero. Right axis, dotted lines: preferential or corporate lending rate (orange) and ordinary rate (yellow), in effective annual percent, monthly average of weekly data. Monthly data since 2008.",
            "importa": "Credit finances working capital and investment: when its real growth falls below zero, companies as a whole are reducing their real bank debt, which usually accompanies phases of weaker investment. Rates show the cost of that financing and respond, with a lag, to Banco de la República's policy rate (TPM).",
            "interpretar": [
                "Negative real growth means the loan stock grows less than inflation, even if it still rises in current pesos.",
                "Rising rates with slowing credit are typical of tight monetary policy; the opposite combination, of easy policy.",
                "The preferential rate is lower than the ordinary rate because it goes to lower-risk clients; the gap between them reflects perceived risk.",
                "Compare with the TPM chart on the rates page: lending rates follow the policy rate with a lag of months.",
                "Loans are in local currency (pesos): dollar loans, corporate bonds and supplier credit are not included."
            ],
            "formulas": [
                ["Annual real growth of the stock", "g<sup>real</sup><sub>t</sub> = [(1 + g<sub>t</sub>) ÷ (1 + π<sub>t</sub>) − 1] × 100", "g<sub>t</sub> = S<sub>t</sub> ÷ S<sub>t−12</sub> − 1, with S = loan stock in month t; π<sub>t</sub> = annual CPI inflation in month t"],
                ["Monthly rate", "i<sub>m</sub> = (1/n) × Σ<sub>s</sub> i<sub>s</sub>", "i<sub>s</sub> = effective annual rate in week s of the month; n = weeks with data"]
            ],
        },
    },
    "g-em-posicion": {
        "es": {
            "que": "Muestra la posición financiera neta de cada sector institucional de la economía según las cuentas financieras del Banco de la República: lo que cada sector tiene en activos financieros (depósitos, bonos, acciones, préstamos otorgados) menos lo que debe. Indica qué sectores financian a los demás y cuáles se financian con el ahorro ajeno.",
            "leer": "Líneas trimestrales en porcentaje del PIB, desde 2015: sociedades no financieras (azul, gruesa), hogares (verde), gobierno general (naranja) y sociedades financieras (morada). La línea horizontal marca el cero: por encima, el sector es acreedor neto; por debajo, deudor neto. Los saldos de los sectores internos no suman cero, porque la diferencia corresponde a la posición frente al resto del mundo.",
            "importa": "Las empresas no financieras suelen ser deudoras netas porque invierten más de lo que ahorran y emiten acciones y deuda; los hogares suelen ser acreedores netos. Una posición deudora creciente de empresas o gobierno indica mayor dependencia del financiamiento de otros sectores o del exterior, lo que eleva la sensibilidad a las tasas de interés y a la tasa de cambio.",
            "interpretar": [
                "Negativo = el sector se financia con los demás; positivo = financia a otros sectores.",
                "Los pasivos de las sociedades incluyen las acciones y participaciones de capital: una posición negativa no es solo deuda.",
                "Los saldos se valoran a precios de mercado, así que cambian con la tasa de cambio y con los precios de las acciones y los bonos, no solo con nuevos flujos.",
                "La suma de los cuatro sectores aproxima la posición de inversión internacional (PII) del país, con signo contrario a la del resto del mundo.",
                "Las cuentas financieras se publican con rezago y se revisan."
            ],
            "formulas": [
                ["Posición financiera neta", "PFN<sub>s,t</sub> = (A<sub>s,t</sub> − P<sub>s,t</sub>) ÷ PIB<sub>t</sub> × 100", "A = activos financieros; P = pasivos (incluidas acciones emitidas) del sector s al final del trimestre t; PIB = PIB nominal de referencia que usa el Banco de la República"],
                ["Identidad agregada", "Σ<sub>s</sub> PFN<sub>s</sub> = − PFN<sub>resto del mundo</sub>", "los sectores internos en conjunto son acreedores o deudores del exterior"]
            ],
        },
        "en": {
            "que": "Shows the net financial position of each institutional sector of the economy according to Banco de la República's financial accounts: what each sector holds in financial assets (deposits, bonds, shares, loans granted) minus what it owes. It indicates which sectors finance the others and which rely on others' savings.",
            "leer": "Quarterly lines in percent of GDP, since 2015: non-financial corporations (thick blue), households (green), general government (orange) and financial corporations (purple). The horizontal line marks zero: above it the sector is a net creditor; below, a net debtor. The domestic sectors do not add up to zero, because the difference is the position against the rest of the world.",
            "importa": "Non-financial corporations are usually net debtors because they invest more than they save and issue shares and debt; households are usually net creditors. A growing debtor position of companies or government signals greater reliance on financing from other sectors or from abroad, which raises sensitivity to interest rates and the exchange rate.",
            "interpretar": [
                "Negative = the sector is financed by the others; positive = it finances other sectors.",
                "Corporations' liabilities include shares and equity: a negative position is not only debt.",
                "Stocks are valued at market prices, so they change with the exchange rate and with share and bond prices, not only with new flows.",
                "The sum of the four sectors approximates the country's international investment position (IIP), with the opposite sign to the rest of the world's.",
                "Financial accounts are published with a lag and are revised."
            ],
            "formulas": [
                ["Net financial position", "NFP<sub>s,t</sub> = (A<sub>s,t</sub> − L<sub>s,t</sub>) ÷ GDP<sub>t</sub> × 100", "A = financial assets; L = liabilities (including shares issued) of sector s at the end of quarter t; GDP = the nominal GDP reference used by Banco de la República"],
                ["Aggregate identity", "Σ<sub>s</sub> NFP<sub>s</sub> = − NFP<sub>rest of world</sub>", "domestic sectors together are creditors or debtors of the rest of the world"]
            ],
        },
    },
    "g-em-registro": {
        "es": {
            "que": "Muestra cuántas empresas se crean y cuántas cierran en Colombia, a partir de las matrículas y cancelaciones en el registro mercantil que llevan las cámaras de comercio (RUES, Registro Único Empresarial y Social, administrado por Confecámaras). Distingue las sociedades de las personas naturales con negocio propio, y es una señal temprana del dinamismo empresarial.",
            "leer": "Cuatro líneas mensuales, cada una con la suma de los últimos 12 meses en miles, desde 2012. Azul: sociedades (personas jurídicas principales y entidades sin ánimo de lucro); amarillo: personas naturales. Línea sólida: matrículas (nacimientos); punteada: cancelaciones (cierres). Se descarta el último mes si aún está incompleto. El selector de horizonte cambia la ventana.",
            "importa": "La creación de empresas refleja la confianza para emprender y la demanda esperada; las cancelaciones, el cierre de negocios. La diferencia entre ambas aproxima la creación neta de unidades productivas formales, ligada al empleo formal. Para un inversionista, es una medida del dinamismo del tejido empresarial, especialmente de las pequeñas empresas que no aparecen en la bolsa ni en las 10.000 más grandes.",
            "interpretar": [
                "Matrículas por encima de cancelaciones: el número de unidades registradas aumenta; la brecha entre la línea sólida y la punteada de un mismo color es la creación neta.",
                "La suma de 12 meses suaviza la estacionalidad del calendario de registro pero hace que los cambios aparezcan de forma gradual.",
                "Las cancelaciones incluyen depuraciones masivas del registro ordenadas por norma, que generan saltos que no son cierres económicos de ese momento.",
                "Una matrícula no equivale a una empresa en operación ni a empleo creado; es un conteo administrativo.",
                "Compare con el gráfico de crédito: periodos de crédito real débil suelen coincidir con menor creación de sociedades."
            ],
            "formulas": [
                ["Suma móvil de 12 meses", "S<sub>t</sub> = Σ<sub>k=0</sub><sup>11</sup> x<sub>t−k</sub> ÷ 1.000", "x = matrículas o cancelaciones del mes, por fecha de matrícula o de cancelación"],
                ["Creación neta", "N<sub>t</sub> = S<sup>matrículas</sup><sub>t</sub> − S<sup>cancelaciones</sup><sub>t</sub>", "para sociedades o para personas naturales"],
                ["Mes incompleto", "se descarta el mes t si x<sub>t</sub> < 0,5 × mediana(x<sub>t−12</sub>, …, x<sub>t−1</sub>)", "x = matrículas totales del mes"]
            ],
        },
        "en": {
            "que": "Shows how many businesses are created and closed in Colombia, based on registrations and cancellations in the business register kept by the chambers of commerce (RUES, the Single Business and Social Register run by Confecámaras). It separates companies from self-employed individuals with their own business, and is an early signal of business dynamism.",
            "leer": "Four monthly lines, each the sum of the last 12 months in thousands, since 2012. Blue: companies (principal legal entities and non-profits); yellow: self-employed individuals. Solid line: registrations (births); dotted: cancellations (closures). The last month is dropped if still incomplete. The horizon selector changes the window.",
            "importa": "Business creation reflects confidence to start ventures and expected demand; cancellations, business closures. The gap between both approximates the net creation of formal productive units, linked to formal employment. For investors, it measures the dynamism of the business fabric, especially of small firms that are neither listed nor among the 10,000 largest.",
            "interpretar": [
                "Registrations above cancellations: the number of registered units grows; the gap between the solid and dotted line of the same colour is net creation.",
                "The 12-month sum smooths out the seasonality of the registration calendar but makes changes appear gradually.",
                "Cancellations include mass registry clean-ups mandated by law, which produce jumps that are not economic closures at that time.",
                "A registration is not the same as an operating business or a job created; it is an administrative count.",
                "Compare with the credit chart: periods of weak real credit often coincide with lower company creation."
            ],
            "formulas": [
                ["12-month rolling sum", "S<sub>t</sub> = Σ<sub>k=0</sub><sup>11</sup> x<sub>t−k</sub> ÷ 1,000", "x = registrations or cancellations in the month, by registration or cancellation date"],
                ["Net creation", "N<sub>t</sub> = S<sup>registrations</sup><sub>t</sub> − S<sup>cancellations</sup><sub>t</sub>", "for companies or for self-employed individuals"],
                ["Incomplete month", "month t is dropped if x<sub>t</sub> < 0.5 × median(x<sub>t−12</sub>, …, x<sub>t−1</sub>)", "x = total registrations in the month"]
            ],
        },
    },

    # =========================================================================================== PESO Y TASA DE CAMBIO
    "g-dolar": {
        "es": {
            "que": "Muestra cuántos pesos cuesta un dólar según la Tasa Representativa del Mercado (TRM), el precio de referencia del dólar en Colombia que calcula y certifica la Superintendencia Financiera con las operaciones del mercado cambiario. Colombia tiene un régimen de tasa de cambio flexible: el precio lo determinan la oferta y la demanda de dólares, no una autoridad.",
            "leer": "Panel superior: pesos por dólar, con el último dato de cada semana; si la línea sube, el peso se debilita (se necesitan más pesos por dólar) y si baja, se fortalece. Panel inferior: barras con la variación porcentual frente a la misma semana un año antes, azules cuando la TRM sube (peso más débil) y naranjas cuando baja (peso más fuerte). Vista inicial de diez años, ajustable con el selector de horizonte.",
            "importa": "La tasa de cambio afecta los precios de los bienes importados y, por tanto, la inflación; el valor en pesos de la deuda externa de empresas y gobierno; los ingresos de exportadores y receptores de remesas; y el rendimiento en dólares de cualquier inversión en activos colombianos. Es uno de los precios más vigilados por inversionistas extranjeros y por el Banco de la República.",
            "interpretar": [
                "Una variación anual de +10% significa que el dólar cuesta 10% más en pesos que hace un año: el peso se depreció.",
                "Para saber si el movimiento es propio de Colombia o global, compare con el dólar global y con las monedas vecinas en los gráficos de esta página.",
                "El precio del petróleo, el apetito global por riesgo y el diferencial de tasas de interés con Estados Unidos son factores que suelen acompañar los grandes movimientos de la TRM.",
                "Una depreciación encarece los bienes importados con rezago; la transmisión a la inflación suele ser parcial.",
                "La TRM calculada con las operaciones de un día rige al día hábil siguiente; cada punto del gráfico es el último valor vigente de la semana."
            ],
            "formulas": [
                ["Variación anual", "g<sub>t</sub> = (TRM<sub>t</sub> ÷ TRM<sub>t−52</sub> − 1) × 100", "TRM<sub>t</sub> = último valor de la semana t; t−52 = misma semana un año antes"],
                ["TRM (cálculo de la Superfinanciera)", "TRM = Σ<sub>k</sub> (p<sub>k</sub> × m<sub>k</sub>) ÷ Σ<sub>k</sub> m<sub>k</sub>", "p<sub>k</sub> = tasa de la operación de contado k entre pesos y dólares; m<sub>k</sub> = su monto en dólares"]
            ],
        },
        "en": {
            "que": "Shows how many pesos one dollar costs according to the Representative Market Rate (TRM), Colombia's reference dollar price, computed and certified by the Financial Superintendence from foreign-exchange market trades. Colombia has a flexible exchange-rate regime: the price is set by the supply and demand of dollars, not by an authority.",
            "leer": "Top panel: pesos per dollar, using the last value of each week; if the line rises the peso weakens (more pesos per dollar) and if it falls the peso strengthens. Bottom panel: bars with the percentage change against the same week a year earlier, blue when the TRM rises (weaker peso) and orange when it falls (stronger peso). The initial view covers ten years and can be changed with the horizon selector.",
            "importa": "The exchange rate affects the prices of imported goods and hence inflation; the peso value of companies' and government's external debt; the income of exporters and remittance recipients; and the dollar return on any investment in Colombian assets. It is one of the prices most closely watched by foreign investors and by Banco de la República.",
            "interpretar": [
                "An annual change of +10% means the dollar costs 10% more in pesos than a year ago: the peso depreciated.",
                "To tell whether a move is Colombian or global, compare with the global dollar and peer currencies in this page's charts.",
                "Oil prices, global risk appetite and the interest-rate differential with the United States usually accompany large TRM moves.",
                "A depreciation makes imported goods dearer with a lag; pass-through to inflation is usually partial.",
                "The TRM computed from one day's trades applies on the next business day; each point in the chart is the week's last applicable value."
            ],
            "formulas": [
                ["Annual change", "g<sub>t</sub> = (TRM<sub>t</sub> ÷ TRM<sub>t−52</sub> − 1) × 100", "TRM<sub>t</sub> = last value in week t; t−52 = same week a year earlier"],
                ["TRM (Superintendence computation)", "TRM = Σ<sub>k</sub> (p<sub>k</sub> × m<sub>k</sub>) ÷ Σ<sub>k</sub> m<sub>k</sub>", "p<sub>k</sub> = rate of spot peso-dollar trade k; m<sub>k</sub> = its amount in dollars"]
            ],
        },
    },
    "g-itcr": {
        "es": {
            "que": "Muestra el Índice de la Tasa de Cambio Real (ITCR) que calcula el Banco de la República: la tasa de cambio del peso frente a las monedas de sus principales socios comerciales, ajustada por la diferencia de inflación (medida con el IPC). Indica si los bienes colombianos son caros o baratos frente a los de otros países, algo que la TRM sola no muestra.",
            "leer": "Panel superior: el índice mensual con base 2010 = 100; la línea horizontal marca 100. Por encima de 100, el peso está más barato en términos reales que en 2010; por debajo, más caro. Panel inferior: barras con la variación porcentual frente al mismo mes del año anterior, azules cuando el índice sube (el peso se abarata en términos reales) y naranjas cuando baja. Vista inicial de diez años.",
            "importa": "Un peso real barato mejora la competitividad de exportadores y de quienes compiten con importaciones, y encarece lo importado; uno caro abarata importaciones y viajes, pero resta competitividad. La tasa de cambio real es una variable central para entender el ajuste de la balanza de pagos y la rentabilidad relativa de producir en Colombia.",
            "interpretar": [
                "Sube = depreciación real (el peso se abarata frente a sus socios después de corregir por inflación); baja = apreciación real.",
                "El año base 2010 es solo una fecha de comparación, no un nivel de equilibrio: estar por encima o por debajo de 100 no indica por sí solo desalineación.",
                "Si la TRM sube pero la inflación colombiana es mayor que la de los socios, el ITCR puede subir menos que la TRM o incluso bajar.",
                "Para la comparación con el promedio histórico y con la competitividad en Estados Unidos, vea los gráficos de tasa de cambio real de esta página.",
                "Los datos se revisan cuando se actualizan los índices de precios y las ponderaciones de los socios."
            ],
            "formulas": [
                ["Tasa de cambio real (esquema)", "ITCR<sub>t</sub> = Π<sub>j</sub> (E<sub>j,t</sub> × P<sup>*</sup><sub>j,t</sub> ÷ P<sub>t</sub>)<sup>w<sub>j</sub></sup>, base 2010 = 100", "E<sub>j</sub> = pesos por unidad de la moneda del socio j; P<sup>*</sup><sub>j</sub> = IPC del socio j; P = IPC de Colombia; w<sub>j</sub> = peso del socio en el comercio"],
                ["Variación anual", "g<sub>t</sub> = (ITCR<sub>t</sub> ÷ ITCR<sub>t−12</sub> − 1) × 100", "t = mes"]
            ],
        },
        "en": {
            "que": "Shows Banco de la República's Real Exchange Rate Index (ITCR): the peso's exchange rate against its main trading partners' currencies, adjusted for the inflation differential (measured with the CPI). It indicates whether Colombian goods are expensive or cheap relative to other countries, something the TRM alone does not show.",
            "leer": "Top panel: the monthly index with base 2010 = 100; the horizontal line marks 100. Above 100 the peso is cheaper in real terms than in 2010; below, more expensive. Bottom panel: bars with the percentage change against the same month a year earlier, blue when the index rises (the peso becomes cheaper in real terms) and orange when it falls. The initial view covers ten years.",
            "importa": "A cheap real peso improves the competitiveness of exporters and import-competing producers and makes imports dearer; an expensive one makes imports and travel cheaper but erodes competitiveness. The real exchange rate is central to understanding balance-of-payments adjustment and the relative profitability of producing in Colombia.",
            "interpretar": [
                "Up = real depreciation (the peso becomes cheaper against its partners after correcting for inflation); down = real appreciation.",
                "The 2010 base year is only a comparison date, not an equilibrium level: being above or below 100 does not by itself indicate misalignment.",
                "If the TRM rises but Colombian inflation exceeds partners' inflation, the ITCR may rise less than the TRM or even fall.",
                "For the comparison with the historical average and with competitiveness in the US market, see the real exchange rate charts on this page.",
                "Data are revised when price indices and partner weights are updated."
            ],
            "formulas": [
                ["Real exchange rate (outline)", "ITCR<sub>t</sub> = Π<sub>j</sub> (E<sub>j,t</sub> × P<sup>*</sup><sub>j,t</sub> ÷ P<sub>t</sub>)<sup>w<sub>j</sub></sup>, base 2010 = 100", "E<sub>j</sub> = pesos per unit of partner j's currency; P<sup>*</sup><sub>j</sub> = partner j's CPI; P = Colombia's CPI; w<sub>j</sub> = partner's trade weight"],
                ["Annual change", "g<sub>t</sub> = (ITCR<sub>t</sub> ÷ ITCR<sub>t−12</sub> − 1) × 100", "t = month"]
            ],
        },
    },
    "g-tc-pares": {
        "es": {
            "que": "Compara cuánto cambió en los últimos 12 meses el valor del dólar en pesos colombianos con lo que cambió frente al real brasileño, el peso mexicano y el sol peruano, y con el índice amplio del dólar de la Reserva Federal. Sirve para separar lo que es propio de Colombia de lo que es un movimiento general del dólar o de las monedas de la región.",
            "leer": "Una barra por moneda con la variación porcentual de las unidades de esa moneda por dólar entre el último dato y el último disponible 12 meses antes. Positivo = la moneda se debilita frente al dólar; negativo = se fortalece. Naranja: peso colombiano; azul: monedas vecinas; morado: «dólar global», el índice amplio nominal de la Reserva Federal frente a 26 monedas, que se lee al revés (positivo = el dólar se fortalece en el mundo).",
            "importa": "Si el peso se mueve como sus vecinos y como el dólar global, el origen del movimiento es externo (tasas de interés en Estados Unidos, apetito global por riesgo, precios de materias primas). Si se separa, pesan más factores locales: política fiscal y monetaria, flujos de inversión o percepción de riesgo del país. Esta distinción es clave para interpretar el riesgo cambiario de una inversión en Colombia.",
            "interpretar": [
                "Barra naranja mayor que las azules: el peso se debilitó más (o se fortaleció menos) que sus vecinos.",
                "Dólar global positivo y peso negativo: el peso se fortaleció pese a un dólar fuerte, señal de factores propios favorables.",
                "Son variaciones nominales: no corrigen por inflación, que difiere entre países.",
                "Las series del Banco de la República y de la Reserva Federal tienen fechas de corte distintas (la segunda llega con unos días de rezago), así que los 12 meses no terminan exactamente el mismo día."
            ],
            "formulas": [
                ["Variación en 12 meses", "v = (X<sub>t</sub> ÷ X<sub>t−12m</sub> − 1) × 100", "X<sub>t</sub> = último dato de unidades de la moneda por dólar (o del índice amplio); X<sub>t−12m</sub> = último dato disponible 12 meses antes"],
                ["Diferencia frente a los vecinos", "d = v<sub>COP</sub> − (v<sub>BRL</sub> + v<sub>MXN</sub> + v<sub>PEN</sub>) ÷ 3", "en puntos porcentuales; positivo = el peso se debilitó más que el promedio de sus vecinos"]
            ],
        },
        "en": {
            "que": "Compares how much the dollar's value in Colombian pesos changed over the last 12 months with its change against the Brazilian real, the Mexican peso and the Peruvian sol, and with the Federal Reserve's broad dollar index. It separates what is specific to Colombia from a general move of the dollar or of the region's currencies.",
            "leer": "One bar per currency with the percentage change in units of that currency per dollar between the latest observation and the latest available 12 months earlier. Positive = the currency weakens against the dollar; negative = it strengthens. Orange: Colombian peso; blue: peer currencies; purple: 'global dollar', the Federal Reserve's nominal broad index against 26 currencies, which reads the other way round (positive = the dollar strengthens worldwide).",
            "importa": "If the peso moves like its peers and the global dollar, the cause is external (US interest rates, global risk appetite, commodity prices). If it diverges, local factors weigh more: fiscal and monetary policy, investment flows or country risk perception. This distinction is key to interpreting the currency risk of an investment in Colombia.",
            "interpretar": [
                "Orange bar larger than the blue ones: the peso weakened more (or strengthened less) than its peers.",
                "Global dollar positive and peso negative: the peso strengthened despite a strong dollar, a sign of favourable local factors.",
                "These are nominal changes: they do not correct for inflation, which differs across countries.",
                "Banco de la República and Federal Reserve series have different cut-off dates (the latter arrives a few days later), so the 12 months do not end on exactly the same day."
            ],
            "formulas": [
                ["12-month change", "v = (X<sub>t</sub> ÷ X<sub>t−12m</sub> − 1) × 100", "X<sub>t</sub> = latest units of the currency per dollar (or broad index); X<sub>t−12m</sub> = latest value available 12 months earlier"],
                ["Gap against peers", "d = v<sub>COP</sub> − (v<sub>BRL</sub> + v<sub>MXN</sub> + v<sub>PEN</sub>) ÷ 3", "in percentage points; positive = the peso weakened more than its peers' average"]
            ],
        },
    },
    "g-tc-dolar-global": {
        "es": {
            "que": "Compara a lo largo del tiempo la variación anual de la TRM con la del índice amplio del dólar de la Reserva Federal, que mide el valor del dólar frente a las monedas de 26 socios comerciales de Estados Unidos. Muestra cuándo el peso ha seguido el ciclo global del dólar y cuándo se ha separado de él por razones propias.",
            "leer": "Dos líneas con la variación en 52 semanas, en porcentaje, usando el último dato de cada semana: naranja para la TRM (pesos por dólar) y morada para el dólar global. En ambas, positivo significa un dólar más fuerte: frente al peso en el primer caso y frente al mundo en el segundo. La línea horizontal marca el cero. El selector de horizonte cambia la ventana.",
            "importa": "Una buena parte de los movimientos del peso responde al ciclo financiero global, que se resume en la fortaleza del dólar. Cuando la TRM se mueve más que el dólar global, el peso amplifica los choques externos o reacciona a factores locales; separar ambos componentes ayuda a evaluar el riesgo cambiario específico de Colombia.",
            "interpretar": [
                "Líneas juntas: el peso sigue al dólar mundial. Naranja muy por encima de la morada: el peso se debilita más de lo que explica el dólar global.",
                "La TRM suele moverse con más amplitud que el índice amplio, porque este promedia monedas de economías avanzadas, menos volátiles.",
                "Episodios de aversión global al riesgo tienden a llevar ambas líneas hacia arriba al mismo tiempo.",
                "La correlación entre ambas cambia en el tiempo; el gráfico de correlación móvil de esta página la mide semana a semana."
            ],
            "formulas": [
                ["Variación de 52 semanas", "g<sub>t</sub> = (X<sub>t</sub> ÷ X<sub>t−52</sub> − 1) × 100", "X<sub>t</sub> = TRM o índice amplio del dólar, último dato de la semana t (viernes)"],
                ["Brecha", "b<sub>t</sub> = g<sup>TRM</sup><sub>t</sub> − g<sup>dólar global</sup><sub>t</sub>", "en puntos porcentuales; positiva = el peso se debilita más que lo que se fortalece el dólar en el mundo"]
            ],
        },
        "en": {
            "que": "Compares over time the annual change in the TRM with that of the Federal Reserve's broad dollar index, which measures the dollar against the currencies of 26 US trading partners. It shows when the peso has followed the global dollar cycle and when it has diverged for domestic reasons.",
            "leer": "Two lines with the 52-week change, in percent, using the last value of each week: orange for the TRM (pesos per dollar) and purple for the global dollar. In both, positive means a stronger dollar: against the peso in the first case and against the world in the second. The horizontal line marks zero. The horizon selector changes the window.",
            "importa": "A large share of the peso's moves responds to the global financial cycle, summarised by the dollar's strength. When the TRM moves more than the global dollar, the peso is amplifying external shocks or reacting to local factors; separating both components helps assess Colombia-specific currency risk.",
            "interpretar": [
                "Lines together: the peso follows the world dollar. Orange well above purple: the peso weakens more than the global dollar explains.",
                "The TRM usually swings more than the broad index, because the index averages less volatile advanced-economy currencies.",
                "Episodes of global risk aversion tend to push both lines up at the same time.",
                "The correlation between both changes over time; this page's rolling correlation chart measures it week by week."
            ],
            "formulas": [
                ["52-week change", "g<sub>t</sub> = (X<sub>t</sub> ÷ X<sub>t−52</sub> − 1) × 100", "X<sub>t</sub> = TRM or broad dollar index, last value of week t (Friday)"],
                ["Gap", "b<sub>t</sub> = g<sup>TRM</sup><sub>t</sub> − g<sup>global dollar</sup><sub>t</sub>", "in percentage points; positive = the peso weakens more than the dollar strengthens worldwide"]
            ],
        },
    },
    "g-tc-monedas": {
        "es": {
            "que": "Muestra cuántos pesos cuesta cada una de cinco monedas relevantes para Colombia (dólar, euro, yuan, real brasileño y peso mexicano), expresado como índice. Permite ver que el peso puede fortalecerse frente a una moneda y debilitarse frente a otra al mismo tiempo, según el comercio y los socios de que se trate.",
            "leer": "Una línea por moneda, con datos semanales (último dato de cada semana) desde 2009, re-basadas a 100 en el primer dato visible del horizonte elegido (3, 5, 10 años o todo). Naranja: dólar (TRM); azul: euro; amarilla: yuan; verde: real brasileño; morada: peso mexicano. Si una línea sube, se necesitan más pesos para comprar esa moneda: el peso se debilita frente a ella. Una línea en 120 indica 20% más pesos por unidad que al inicio de la ventana.",
            "importa": "Colombia comercia con Estados Unidos, la zona euro, China y la región; el costo de las importaciones y la competitividad de las exportaciones dependen de la tasa de cambio frente a cada socio, no solo frente al dólar. Para un inversionista que mide resultados en euros u otra moneda, estas líneas muestran el efecto cambiario relevante.",
            "interpretar": [
                "Líneas que suben juntas: el peso se debilita frente a todas, señal de un factor propio de Colombia.",
                "Si la del dólar sube y las del real y el peso mexicano no, el movimiento refleja sobre todo fortaleza del dólar frente a todas las monedas de la región.",
                "Los índices dependen del punto de partida: cambiar el horizonte cambia el nivel de las líneas, no su forma.",
                "Real y peso mexicano se obtienen como tasas cruzadas con la TRM, por lo que heredan diferencias de fechas de corte entre fuentes."
            ],
            "formulas": [
                ["Tasa cruzada", "COP/X = TRM ÷ (X por USD)", "X = real o peso mexicano; X por USD = unidades de esa moneda por dólar"],
                ["Índice re-basado", "I<sub>t</sub> = 100 × S<sub>t</sub> ÷ S<sub>0</sub>", "S<sub>t</sub> = pesos por unidad de la moneda en la semana t; S<sub>0</sub> = valor al inicio del horizonte elegido"]
            ],
        },
        "en": {
            "que": "Shows how many pesos each of five currencies relevant to Colombia (dollar, euro, yuan, Brazilian real and Mexican peso) costs, expressed as an index. It shows that the peso can strengthen against one currency and weaken against another at the same time, depending on the trade and partners involved.",
            "leer": "One line per currency, weekly data (last value of each week) since 2009, rebased to 100 at the first visible observation of the chosen horizon (3, 5, 10 years or all). Orange: dollar (TRM); blue: euro; yellow: yuan; green: Brazilian real; purple: Mexican peso. If a line rises, more pesos are needed to buy that currency: the peso weakens against it. A line at 120 means 20% more pesos per unit than at the start of the window.",
            "importa": "Colombia trades with the United States, the euro area, China and the region; the cost of imports and export competitiveness depend on the exchange rate against each partner, not only against the dollar. For an investor measuring results in euros or another currency, these lines show the relevant currency effect.",
            "interpretar": [
                "Lines rising together: the peso weakens against all of them, a sign of a Colombia-specific factor.",
                "If the dollar line rises and the real and Mexican peso lines do not, the move mainly reflects dollar strength against all the region's currencies.",
                "Indices depend on the starting point: changing the horizon changes the level of the lines, not their shape.",
                "The real and the Mexican peso are cross rates with the TRM, so they inherit cut-off date differences between sources."
            ],
            "formulas": [
                ["Cross rate", "COP/X = TRM ÷ (X per USD)", "X = real or Mexican peso; X per USD = units of that currency per dollar"],
                ["Rebased index", "I<sub>t</sub> = 100 × S<sub>t</sub> ÷ S<sub>0</sub>", "S<sub>t</sub> = pesos per unit of the currency in week t; S<sub>0</sub> = value at the start of the chosen horizon"]
            ],
        },
    },
    "g-tc-cruces": {
        "es": {
            "que": "Resume en una sola vista cuánto cambió en los últimos 12 meses el precio en pesos de ocho monedas: dólar, euro, libra esterlina, yen, yuan, real brasileño, peso mexicano y sol peruano. Muestra frente a cuáles el peso colombiano ganó o perdió valor.",
            "leer": "Una barra horizontal por moneda, ordenadas de la mayor caída a la mayor subida, con la variación porcentual de los pesos necesarios para comprar una unidad de esa moneda. Negativo (verde) = se necesitan menos pesos: el peso se fortaleció frente a esa moneda. Positivo (naranja) = el peso se debilitó. La línea vertical marca el cero.",
            "importa": "El efecto de la tasa de cambio sobre precios, exportaciones y balances depende de la moneda en que se hace cada transacción. Un peso que se fortalece frente al dólar pero se debilita frente al euro tiene efectos distintos sobre importadores de Europa y de Estados Unidos. Para inversionistas de distintas regiones, la barra de su moneda indica el efecto cambiario de los últimos 12 meses.",
            "interpretar": [
                "Mayoría de barras verdes: el peso se fortaleció de forma generalizada; mayoría naranja, se debilitó de forma generalizada.",
                "Si el peso se fortalece frente al dólar pero no frente al euro o la libra, buena parte del movimiento es debilidad global del dólar.",
                "Euro, libra, yen y yuan son tasas medias que publica el Banco de la República; real, peso mexicano y sol son cruces con la TRM.",
                "Son cambios nominales y de punta a punta: no recogen la volatilidad intermedia ni las diferencias de inflación."
            ],
            "formulas": [
                ["Variación en 12 meses", "v<sub>X</sub> = (S<sub>X,t</sub> ÷ S<sub>X,t−12m</sub> − 1) × 100", "S<sub>X</sub> = pesos por unidad de la moneda X; t−12m = último dato disponible 12 meses antes"],
                ["Cruce con la TRM", "S<sub>X</sub> = TRM ÷ (X por USD)", "para real, peso mexicano y sol"]
            ],
        },
        "en": {
            "que": "Summarises in a single view how much the peso price of eight currencies changed over the last 12 months: dollar, euro, pound sterling, yen, yuan, Brazilian real, Mexican peso and Peruvian sol. It shows against which ones the Colombian peso gained or lost value.",
            "leer": "One horizontal bar per currency, sorted from the largest fall to the largest rise, with the percentage change in pesos needed to buy one unit of that currency. Negative (green) = fewer pesos are needed: the peso strengthened against that currency. Positive (orange) = the peso weakened. The vertical line marks zero.",
            "importa": "The impact of the exchange rate on prices, exports and balance sheets depends on the currency of each transaction. A peso that strengthens against the dollar but weakens against the euro has different effects on importers from Europe and from the United States. For investors from different regions, the bar for their currency shows the currency effect over the last 12 months.",
            "interpretar": [
                "Mostly green bars: the peso strengthened across the board; mostly orange, it weakened across the board.",
                "If the peso strengthens against the dollar but not against the euro or the pound, much of the move is global dollar weakness.",
                "Euro, pound, yen and yuan are average rates published by Banco de la República; real, Mexican peso and sol are crosses with the TRM.",
                "These are nominal, point-to-point changes: they do not capture interim volatility or inflation differences."
            ],
            "formulas": [
                ["12-month change", "v<sub>X</sub> = (S<sub>X,t</sub> ÷ S<sub>X,t−12m</sub> − 1) × 100", "S<sub>X</sub> = pesos per unit of currency X; t−12m = latest value available 12 months earlier"],
                ["Cross with the TRM", "S<sub>X</sub> = TRM ÷ (X per USD)", "for the real, Mexican peso and sol"]
            ],
        },
    },
    "g-tc-itcr": {
        "es": {
            "que": "Muestra dos medidas de la tasa de cambio real multilateral que publica el Banco de la República: el ITCR deflactado con IPC y ponderado por el comercio total con los 22 principales socios, y el ITCR-C, que mide la competitividad de Colombia frente a otros países que venden en el mercado de Estados Unidos. Ambas indican si el peso está caro o barato en términos reales.",
            "leer": "Líneas mensuales desde 2000, en índice con base 2010 = 100: azul para el ITCR (IPC, comercio total) y amarilla para el ITCR-C. La línea horizontal continua marca 100 y la punteada azul, el promedio del ITCR desde 2000. Cuando las líneas suben, el peso se abarata en términos reales; cuando bajan, se encarece. El selector de horizonte cambia la ventana.",
            "importa": "Un peso real persistentemente caro resta competitividad a exportadores e industrias que compiten con importaciones; uno barato la favorece, pero encarece insumos y bienes importados. Comparar el nivel actual con su promedio de largo plazo es una forma sencilla de ubicar la tasa de cambio real en su historia, y el ITCR-C añade la perspectiva de los exportadores que compiten en Estados Unidos.",
            "interpretar": [
                "ITCR por encima de la línea punteada: el peso está más barato en términos reales que su promedio desde 2000; por debajo, más caro.",
                "Si el ITCR-C sube más que el ITCR, Colombia gana competitividad frente a otros proveedores de Estados Unidos más de lo que gana frente al conjunto de socios.",
                "El promedio histórico no es un nivel de equilibrio: cambios estructurales (por ejemplo, en los términos de intercambio) pueden desplazar el nivel de referencia.",
                "Las ponderaciones son móviles de 12 meses y los índices se revisan con nuevos datos de precios y comercio."
            ],
            "formulas": [
                ["ITCR (esquema)", "ITCR<sub>t</sub> = Π<sub>j</sub> (E<sub>j,t</sub> × P<sup>*</sup><sub>j,t</sub> ÷ P<sub>t</sub>)<sup>w<sub>j</sub></sup>, base 2010 = 100", "E<sub>j</sub> = pesos por moneda del socio j; P<sup>*</sup><sub>j</sub> = IPC del socio; P = IPC de Colombia; w<sub>j</sub> = peso en el comercio total"],
                ["Promedio de referencia", "Ī = (1/T) × Σ<sub>t</sub> ITCR<sub>t</sub>", "promedio de los meses desde enero de 2000 hasta el último dato"],
                ["Distancia al promedio", "d<sub>t</sub> = (ITCR<sub>t</sub> ÷ Ī − 1) × 100", "positiva = peso más barato que su promedio"]
            ],
        },
        "en": {
            "que": "Shows two multilateral real exchange rate measures published by Banco de la República: the ITCR deflated with CPI and weighted by total trade with the 22 main partners, and the ITCR-C, which measures Colombia's competitiveness against other countries selling in the US market. Both indicate whether the peso is expensive or cheap in real terms.",
            "leer": "Monthly lines since 2000, as an index with base 2010 = 100: blue for the ITCR (CPI, total trade) and yellow for the ITCR-C. The solid horizontal line marks 100 and the dotted blue line, the ITCR average since 2000. When the lines rise, the peso becomes cheaper in real terms; when they fall, dearer. The horizon selector changes the window.",
            "importa": "A persistently expensive real peso erodes the competitiveness of exporters and import-competing industries; a cheap one helps them but makes imported inputs and goods dearer. Comparing the current level with its long-run average is a simple way to place the real exchange rate in its history, and the ITCR-C adds the perspective of exporters competing in the United States.",
            "interpretar": [
                "ITCR above the dotted line: the peso is cheaper in real terms than its average since 2000; below it, dearer.",
                "If the ITCR-C rises more than the ITCR, Colombia gains competitiveness against other US suppliers more than against its partners as a whole.",
                "The historical average is not an equilibrium level: structural changes (for example in the terms of trade) can shift the reference level.",
                "Weights are 12-month rolling and the indices are revised with new price and trade data."
            ],
            "formulas": [
                ["ITCR (outline)", "ITCR<sub>t</sub> = Π<sub>j</sub> (E<sub>j,t</sub> × P<sup>*</sup><sub>j,t</sub> ÷ P<sub>t</sub>)<sup>w<sub>j</sub></sup>, base 2010 = 100", "E<sub>j</sub> = pesos per partner j currency; P<sup>*</sup><sub>j</sub> = partner CPI; P = Colombia's CPI; w<sub>j</sub> = total trade weight"],
                ["Reference average", "Ī = (1/T) × Σ<sub>t</sub> ITCR<sub>t</sub>", "average of the months from January 2000 to the latest observation"],
                ["Distance from the average", "d<sub>t</sub> = (ITCR<sub>t</sub> ÷ Ī − 1) × 100", "positive = peso cheaper than its average"]
            ],
        },
    },
    "g-tc-bilateral": {
        "es": {
            "que": "Muestra, para cuatro socios clave (Estados Unidos, China, Brasil y México), qué tan lejos está hoy la tasa de cambio real bilateral del peso de su promedio desde 2000. Complementa el índice multilateral al mostrar que el peso puede estar caro frente a un país y barato frente a otro.",
            "leer": "Una barra horizontal por país con la diferencia porcentual entre el último dato mensual del ITCR bilateral y su promedio desde 2000. Negativo (naranja) = el peso está más caro, en términos reales, que su promedio frente a ese país; positivo (azul) = más barato. La línea vertical marca el cero. Es una fotografía del último mes disponible.",
            "importa": "La competitividad de las exportaciones y la presión de las importaciones dependen del país: frente a Estados Unidos importa para el petróleo, el café y las flores; frente a China, para la competencia de las importaciones manufactureras; frente a Brasil y México, para el comercio regional. Un peso caro frente a un socio favorece las compras a ese país y dificulta venderle.",
            "interpretar": [
                "Una barra de −15% significa que el peso está 15% más caro en términos reales que su promedio frente a ese país.",
                "Diferencias grandes entre países suelen reflejar movimientos de la moneda del socio (por ejemplo, una depreciación fuerte del real) más que del peso.",
                "El promedio desde 2000 es una referencia estadística, no un nivel de equilibrio.",
                "Según la nota metodológica del gráfico, estos índices bilaterales se deflactan con índices de precios al productor (IPP), que reflejan mejor los precios de bienes transables."
            ],
            "formulas": [
                ["Distancia al promedio", "d<sub>j</sub> = (ITCR<sub>j,t</sub> ÷ Ī<sub>j</sub> − 1) × 100", "ITCR<sub>j,t</sub> = índice bilateral con el país j en el último mes; Ī<sub>j</sub> = su promedio mensual desde enero de 2000"],
                ["ITCR bilateral (esquema)", "ITCR<sub>j,t</sub> = E<sub>j,t</sub> × P<sup>*</sup><sub>j,t</sub> ÷ P<sub>t</sub>", "E<sub>j</sub> = pesos por unidad de la moneda de j; P<sup>*</sup><sub>j</sub>, P = índices de precios de j y de Colombia"]
            ],
        },
        "en": {
            "que": "Shows, for four key partners (United States, China, Brazil and Mexico), how far the peso's bilateral real exchange rate is today from its average since 2000. It complements the multilateral index by showing that the peso can be expensive against one country and cheap against another.",
            "leer": "One horizontal bar per country with the percentage gap between the latest monthly bilateral ITCR and its average since 2000. Negative (orange) = the peso is dearer, in real terms, than its average against that country; positive (blue) = cheaper. The vertical line marks zero. It is a snapshot of the latest available month.",
            "importa": "Export competitiveness and import pressure depend on the country: against the United States it matters for oil, coffee and flowers; against China, for competition from manufactured imports; against Brazil and Mexico, for regional trade. A dear peso against a partner favours buying from that country and makes selling to it harder.",
            "interpretar": [
                "A bar of −15% means the peso is 15% dearer in real terms than its average against that country.",
                "Large differences between countries often reflect moves in the partner's currency (for example, a sharp real depreciation) rather than in the peso.",
                "The average since 2000 is a statistical reference, not an equilibrium level.",
                "According to the chart's methodology note, these bilateral indices are deflated with producer price indices (PPI), which better reflect tradable-goods prices."
            ],
            "formulas": [
                ["Distance from the average", "d<sub>j</sub> = (ITCR<sub>j,t</sub> ÷ Ī<sub>j</sub> − 1) × 100", "ITCR<sub>j,t</sub> = bilateral index with country j in the latest month; Ī<sub>j</sub> = its monthly average since January 2000"],
                ["Bilateral ITCR (outline)", "ITCR<sub>j,t</sub> = E<sub>j,t</sub> × P<sup>*</sup><sub>j,t</sub> ÷ P<sub>t</sub>", "E<sub>j</sub> = pesos per unit of j's currency; P<sup>*</sup><sub>j</sub>, P = price indices of j and Colombia"]
            ],
        },
    },
    "g-tc-brent": {
        "es": {
            "que": "Relaciona, mes a mes, el cambio anual del precio del petróleo Brent con el cambio anual de la TRM. Como el petróleo ha sido la principal exportación de Colombia, un alza del crudo suele traer más dólares y fortalecer el peso; el gráfico muestra qué tan fuerte ha sido ese vínculo y si ha cambiado con el tiempo.",
            "leer": "Cada punto es un mes desde 2008. Eje horizontal: variación del Brent frente al mismo mes del año anterior; eje vertical: variación de la TRM en el mismo lapso, ambos con promedios mensuales. Azul: 2008–2019; naranja: 2020 en adelante. Cada línea es el ajuste por mínimos cuadrados de su periodo, y el punto amarillo grande, con su fecha, es el dato más reciente. Puntos abajo a la derecha = el petróleo subió y el peso se fortaleció.",
            "importa": "El vínculo entre petróleo y peso determina cuánto se transmiten los choques del mercado petrolero a la tasa de cambio, a la inflación y a las finanzas públicas. Un vínculo más débil indica que otros factores (flujos financieros, riesgo local, política) han ganado peso en la formación de la tasa de cambio.",
            "interpretar": [
                "Línea con pendiente negativa: en promedio, un alza del Brent coincidió con una baja de la TRM (peso más fuerte); a mayor inclinación, más fuerte la asociación.",
                "Una pendiente de −0,3 significa que un alza de 10% del Brent en un año coincidió en promedio con una TRM 3% más baja.",
                "Puntos muy dispersos alrededor de la línea indican que el petróleo explica solo una parte de los movimientos del peso.",
                "Las líneas describen la asociación observada en cada periodo; no son una relación causal ni una regla que se cumpla mes a mes.",
                "Los cambios anuales de meses consecutivos se superponen en 11 meses, de modo que los puntos no son observaciones independientes."
            ],
            "formulas": [
                ["Cambios anuales", "x<sub>m</sub> = (B<sub>m</sub> ÷ B<sub>m−12</sub> − 1) × 100;  y<sub>m</sub> = (T<sub>m</sub> ÷ T<sub>m−12</sub> − 1) × 100", "B = promedio mensual del Brent; T = promedio mensual de la TRM"],
                ["Recta de mínimos cuadrados", "ŷ = a + b × x,  b = Σ(x − x̄)(y − ȳ) ÷ Σ(x − x̄)<sup>2</sup>", "estimada por separado para 2008–2019 y para 2020 en adelante"],
                ["Correlación", "r = Σ(x − x̄)(y − ȳ) ÷ √[Σ(x − x̄)<sup>2</sup> × Σ(y − ȳ)<sup>2</sup>]", "va de −1 a 1; mide qué tan cerca de la recta están los puntos"]
            ],
        },
        "en": {
            "que": "Relates, month by month, the annual change in the Brent oil price to the annual change in the TRM. Since oil has been Colombia's main export, a rise in crude usually brings more dollars and strengthens the peso; the chart shows how strong that link has been and whether it has changed over time.",
            "leer": "Each dot is a month since 2008. Horizontal axis: change in Brent against the same month a year earlier; vertical axis: change in the TRM over the same period, both using monthly averages. Blue: 2008–2019; orange: 2020 onwards. Each line is the least-squares fit for its period, and the large yellow dot, labelled with its date, is the latest observation. Dots at the bottom right = oil rose and the peso strengthened.",
            "importa": "The oil-peso link determines how much oil-market shocks pass through to the exchange rate, inflation and public finances. A weaker link indicates that other factors (financial flows, local risk, policy) have gained weight in setting the exchange rate.",
            "interpretar": [
                "Line with a negative slope: on average, a rise in Brent coincided with a lower TRM (stronger peso); the steeper the line, the stronger the association.",
                "A slope of −0.3 means a 10% annual rise in Brent coincided on average with a TRM 3% lower.",
                "Dots widely scattered around the line indicate that oil explains only part of the peso's moves.",
                "The lines describe the association observed in each period; they are neither a causal relationship nor a rule that holds month by month.",
                "Annual changes of consecutive months overlap by 11 months, so the dots are not independent observations."
            ],
            "formulas": [
                ["Annual changes", "x<sub>m</sub> = (B<sub>m</sub> ÷ B<sub>m−12</sub> − 1) × 100;  y<sub>m</sub> = (T<sub>m</sub> ÷ T<sub>m−12</sub> − 1) × 100", "B = monthly average Brent; T = monthly average TRM"],
                ["Least-squares line", "ŷ = a + b × x,  b = Σ(x − x̄)(y − ȳ) ÷ Σ(x − x̄)<sup>2</sup>", "estimated separately for 2008–2019 and for 2020 onwards"],
                ["Correlation", "r = Σ(x − x̄)(y − ȳ) ÷ √[Σ(x − x̄)<sup>2</sup> × Σ(y − ȳ)<sup>2</sup>]", "ranges from −1 to 1; measures how close the dots are to the line"]
            ],
        },
    },
    "g-tc-correlacion": {
        "es": {
            "que": "Muestra cómo ha cambiado en el tiempo la relación de corto plazo entre el peso y dos de sus determinantes externos: el precio del petróleo Brent y el dólar global. Para cada semana calcula la correlación de los últimos 12 meses entre los cambios semanales de la TRM y los de cada una de esas variables.",
            "leer": "Dos líneas semanales en una escala de −1 a 1: amarilla para la correlación TRM–Brent y morada para TRM–dólar global; la línea horizontal marca el cero. La franja azul clara (de −1 a −0,5) y la morada clara (de 0,5 a 1) señalan relaciones fuertes. Una correlación TRM–Brent cercana a −1 indica que, semana a semana, cuando el petróleo sube el peso casi siempre se fortalece; una TRM–dólar global positiva, que el peso se debilita cuando el dólar se fortalece en el mundo.",
            "importa": "Saber qué factor externo domina en cada momento ayuda a entender la fuente del riesgo cambiario: en unos periodos el peso responde sobre todo al petróleo, en otros al ciclo global del dólar y del apetito por riesgo. La estabilidad o inestabilidad de estas relaciones es relevante para coberturas y para evaluar la exposición de una cartera a choques externos.",
            "interpretar": [
                "La correlación TRM–Brent suele ser negativa (petróleo arriba, peso más fuerte); cuando se acerca a cero, el petróleo pierde peso como explicación de corto plazo.",
                "Una correlación TRM–dólar global dentro de la franja morada indica que el peso se mueve sobre todo con el dólar mundial.",
                "Correlación no es causalidad ni magnitud: una correlación alta puede darse con movimientos pequeños; el gráfico de dispersión muestra la magnitud.",
                "Con ventanas de 52 semanas, un episodio extremo puede dominar la correlación durante un año completo; se exige al menos 80% de las semanas con dato."
            ],
            "formulas": [
                ["Cambio semanal", "x<sub>t</sub> = X<sub>t</sub> ÷ X<sub>t−1</sub> − 1", "X = TRM, Brent o índice amplio del dólar, último dato de cada semana"],
                ["Correlación móvil de Pearson", "r<sub>t</sub> = Σ(x − x̄)(y − ȳ) ÷ √[Σ(x − x̄)<sup>2</sup> × Σ(y − ȳ)<sup>2</sup>]", "sumas sobre las 52 semanas que terminan en t; x = cambio de la TRM; y = cambio del Brent o del dólar global"]
            ],
        },
        "en": {
            "que": "Shows how the short-run relationship between the peso and two of its external drivers, Brent oil and the global dollar, has changed over time. For each week it computes the correlation over the past 12 months between weekly changes in the TRM and in each of those variables.",
            "leer": "Two weekly lines on a scale from −1 to 1: yellow for the TRM–Brent correlation and purple for TRM–global dollar; the horizontal line marks zero. The light blue band (−1 to −0.5) and the light purple band (0.5 to 1) mark strong relationships. A TRM–Brent correlation close to −1 means that, week by week, when oil rises the peso almost always strengthens; a positive TRM–global dollar correlation, that the peso weakens when the dollar strengthens worldwide.",
            "importa": "Knowing which external factor dominates at each moment helps identify the source of currency risk: in some periods the peso responds mainly to oil, in others to the global dollar and risk-appetite cycle. The stability or instability of these relationships matters for hedging and for assessing a portfolio's exposure to external shocks.",
            "interpretar": [
                "The TRM–Brent correlation is usually negative (oil up, stronger peso); when it nears zero, oil loses weight as a short-run explanation.",
                "A TRM–global dollar correlation inside the purple band indicates that the peso moves mainly with the world dollar.",
                "Correlation is neither causation nor magnitude: a high correlation can occur with small moves; the scatter chart shows magnitude.",
                "With 52-week windows, one extreme episode can dominate the correlation for a whole year; at least 80% of weeks must have data."
            ],
            "formulas": [
                ["Weekly change", "x<sub>t</sub> = X<sub>t</sub> ÷ X<sub>t−1</sub> − 1", "X = TRM, Brent or broad dollar index, last value of each week"],
                ["Rolling Pearson correlation", "r<sub>t</sub> = Σ(x − x̄)(y − ȳ) ÷ √[Σ(x − x̄)<sup>2</sup> × Σ(y − ȳ)<sup>2</sup>]", "sums over the 52 weeks ending in t; x = TRM change; y = Brent or global dollar change"]
            ],
        },
    },
    "g-tc-petroleo-exportaciones": {
        "es": {
            "que": "Muestra qué parte del valor de las exportaciones de bienes de Colombia corresponde al petróleo y sus derivados y al carbón, junto con los términos de intercambio, que comparan los precios de lo que el país vende con los de lo que compra. Explica por qué los precios de la energía pesan tanto en la oferta de dólares y en la tasa de cambio.",
            "leer": "Eje izquierdo: participación en el total exportado, en porcentaje, calculada con valores FOB en dólares sumados en 12 meses (línea amarilla, petróleo y derivados; morada, carbón). Eje derecho, línea azul punteada: índice mensual de términos de intercambio del Banco de la República. Datos desde 2000. FOB (free on board) significa valor de la mercancía puesta en el puerto de embarque, sin fletes ni seguros internacionales.",
            "importa": "Entre más depende el país de unas pocas materias primas, más expuestos quedan la tasa de cambio, el ingreso nacional y las finanzas públicas a sus precios internacionales. Unos términos de intercambio favorables significan que con las mismas exportaciones se pueden comprar más importaciones, lo que eleva el ingreso real del país.",
            "interpretar": [
                "Una participación que cae puede reflejar menores precios del crudo, menor producción o un crecimiento mayor de otras exportaciones; compárela con el Brent para distinguir el efecto precio.",
                "Términos de intercambio en alza indican que los precios de exportación suben más que los de importación; suelen acompañar periodos de peso más fuerte.",
                "La suma de 12 meses elimina la estacionalidad y suaviza los cambios, que aparecen de forma gradual.",
                "Las cifras de comercio del DANE-DIAN son provisionales en los meses más recientes y se revisan."
            ],
            "formulas": [
                ["Participación en las exportaciones", "s<sub>t</sub> = Σ<sub>k=0</sub><sup>11</sup> X<sup>p</sup><sub>t−k</sub> ÷ Σ<sub>k=0</sub><sup>11</sup> X<sub>t−k</sub> × 100", "X<sup>p</sup> = exportaciones FOB del producto (petróleo y derivados, o carbón) en el mes; X = exportaciones totales FOB"],
                ["Términos de intercambio", "TI<sub>t</sub> = IPX<sub>t</sub> ÷ IPM<sub>t</sub> × 100", "IPX = índice de precios de exportación; IPM = índice de precios de importación"]
            ],
        },
        "en": {
            "que": "Shows what share of the value of Colombia's goods exports comes from oil and its derivatives and from coal, together with the terms of trade, which compare the prices of what the country sells with those of what it buys. It explains why energy prices weigh so much on the supply of dollars and the exchange rate.",
            "leer": "Left axis: share of total exports, in percent, computed with FOB dollar values summed over 12 months (yellow line, oil and derivatives; purple, coal). Right axis, dotted blue line: Banco de la República's monthly terms-of-trade index. Data since 2000. FOB (free on board) means the value of the goods at the port of shipment, excluding international freight and insurance.",
            "importa": "The more the country depends on a few commodities, the more exposed the exchange rate, national income and public finances are to their international prices. Favourable terms of trade mean the same exports buy more imports, which raises the country's real income.",
            "interpretar": [
                "A falling share may reflect lower crude prices, lower output or faster growth of other exports; compare with Brent to isolate the price effect.",
                "Rising terms of trade mean export prices rise faster than import prices; they usually accompany periods of a stronger peso.",
                "The 12-month sum removes seasonality and smooths changes, which appear gradually.",
                "DANE-DIAN trade figures are provisional for the latest months and are revised."
            ],
            "formulas": [
                ["Share of exports", "s<sub>t</sub> = Σ<sub>k=0</sub><sup>11</sup> X<sup>p</sup><sub>t−k</sub> ÷ Σ<sub>k=0</sub><sup>11</sup> X<sub>t−k</sub> × 100", "X<sup>p</sup> = FOB exports of the product (oil and derivatives, or coal) in the month; X = total FOB exports"],
                ["Terms of trade", "ToT<sub>t</sub> = PX<sub>t</sub> ÷ PM<sub>t</sub> × 100", "PX = export price index; PM = import price index"]
            ],
        },
    },
    "g-tc-balanza": {
        "es": {
            "que": "Muestra cuántos dólares entraron o salieron de Colombia a través del mercado cambiario en los últimos 12 meses, según la balanza cambiaria del Banco de la República. Separa los flujos de comercio y transferencias (cuenta corriente) de los de inversión y financiamiento (movimientos de capital), y muestra cómo cambiaron las reservas brutas.",
            "leer": "Tres líneas mensuales, cada una con la suma móvil de 12 meses en miles de millones de dólares: azul para la cuenta corriente (exportaciones, importaciones, servicios y transferencias como las remesas canalizadas), naranja para los movimientos netos de capital (inversión extranjera, deuda y otros) y verde para la variación de las reservas internacionales brutas. Positivo = entran dólares; negativo = salen. La línea horizontal marca el cero.",
            "importa": "La oferta y la demanda de dólares del mercado cambiario son las que determinan la TRM. Un saldo de capital positivo grande puede compensar un déficit corriente; si ese financiamiento se reduce, la presión recae sobre la tasa de cambio o las reservas. Es una medida de alta frecuencia de la dependencia del país del financiamiento externo.",
            "interpretar": [
                "Cuenta corriente negativa y capital positivo es el patrón habitual: el país compra más de lo que vende y lo financia con inversión y deuda del exterior.",
                "La variación de reservas resume el balance de los flujos canalizados: positiva cuando el Banco de la República compra o acumula dólares.",
                "Solo incluye operaciones canalizadas por el mercado cambiario: no es la balanza de pagos completa, que también registra operaciones que no pasan por él (por ejemplo, cuentas de compensación y reinversión de utilidades).",
                "Compare con el gráfico de cuenta corriente de la página externa, que usa la balanza de pagos en porcentaje del PIB."
            ],
            "formulas": [
                ["Suma móvil de 12 meses", "S<sub>t</sub> = Σ<sub>k=0</sub><sup>11</sup> f<sub>t−k</sub> ÷ 1.000", "f = flujo mensual en millones de dólares (cuenta corriente, capital o variación de reservas)"],
                ["Identidad aproximada", "ΔReservas ≈ Cuenta corriente + Capital", "en la balanza cambiaria; las diferencias provienen de otros rubros y ajustes"]
            ],
        },
        "en": {
            "que": "Shows how many dollars came into or left Colombia through the foreign-exchange market over the last 12 months, according to Banco de la República's foreign-exchange balance. It separates trade and transfer flows (current account) from investment and financing flows (capital movements), and shows how gross reserves changed.",
            "leer": "Three monthly lines, each a 12-month rolling sum in billions of dollars: blue for the current account (exports, imports, services and transfers such as channelled remittances), orange for net capital movements (foreign investment, debt and others) and green for the change in gross international reserves. Positive = dollars come in; negative = they go out. The horizontal line marks zero.",
            "importa": "The supply and demand of dollars in the FX market set the TRM. A large positive capital balance can offset a current deficit; if that financing shrinks, pressure falls on the exchange rate or on reserves. It is a high-frequency measure of the country's reliance on external financing.",
            "interpretar": [
                "Negative current account and positive capital is the usual pattern: the country buys more than it sells and finances it with foreign investment and debt.",
                "The change in reserves summarises the balance of channelled flows: positive when Banco de la República buys or accumulates dollars.",
                "It only includes transactions channelled through the FX market: it is not the full balance of payments, which also records transactions outside it (for example, compensation accounts and reinvested earnings).",
                "Compare with the current-account chart on the external page, which uses the balance of payments as a percentage of GDP."
            ],
            "formulas": [
                ["12-month rolling sum", "S<sub>t</sub> = Σ<sub>k=0</sub><sup>11</sup> f<sub>t−k</sub> ÷ 1,000", "f = monthly flow in millions of dollars (current account, capital or change in reserves)"],
                ["Approximate identity", "ΔReserves ≈ Current account + Capital", "in the FX balance; differences come from other items and adjustments"]
            ],
        },
    },
    "g-tc-reservas": {
        "es": {
            "que": "Muestra el saldo de reservas internacionales netas del Banco de la República y los montos de opciones PUT subastadas cada año para acumularlas. Las reservas son los activos externos líquidos del banco central; las opciones PUT de acumulación son el mecanismo con el que el Banco compra dólares en el mercado de forma gradual y preanunciada.",
            "leer": "Línea azul: reservas internacionales netas a fin de mes, en miles de millones de dólares, desde 2000. Barras amarillas: monto aprobado en las subastas de opciones PUT para acumulación de reservas, sumado por año calendario y ubicado al final de cada año, en miles de millones de dólares. Los años sin barra son años sin subastas de acumulación.",
            "importa": "Las reservas son el colchón del país frente a choques externos: respaldan la capacidad de pagar importaciones y deuda en moneda extranjera y son seguidas de cerca por agencias calificadoras e inversionistas. Las compras de reservas también aumentan la demanda de dólares en el mercado, por lo que tienden a acompañar periodos en que el Banco busca fortalecer ese colchón sin fijar la tasa de cambio.",
            "interpretar": [
                "Las reservas cambian por compras y ventas del Banco, pero también por rendimientos y por la valoración de sus inversiones y de otras monedas frente al dólar.",
                "Una opción PUT da a los agentes el derecho a vender dólares al Banco; solo se ejerce si se cumplen sus condiciones, así que el monto aprobado es un tope, no la compra efectiva.",
                "Para dimensionar el nivel, se suele comparar con las importaciones, la deuda externa de corto plazo o las métricas de suficiencia del FMI.",
                "Compare con la línea verde del gráfico de balanza cambiaria, que muestra la variación de las reservas brutas por flujos del mercado cambiario."
            ],
            "formulas": [
                ["Compras anuales por opciones PUT", "P<sub>a</sub> = Σ<sub>s ∈ a</sub> monto aprobado<sub>s</sub> ÷ 10<sup>9</sup>", "s = subasta de acumulación realizada en el año a; resultado en miles de millones de dólares"],
                ["Reservas netas", "RIN = reservas brutas − pasivos externos de corto plazo del Banco", "saldo a fin de mes, en miles de millones de dólares"]
            ],
        },
        "en": {
            "que": "Shows Banco de la República's net international reserves and the amounts of PUT options auctioned each year to accumulate them. Reserves are the central bank's liquid foreign assets; accumulation PUT options are the mechanism through which the Bank buys dollars in the market gradually and with prior announcement.",
            "leer": "Blue line: net international reserves at month-end, in billions of dollars, since 2000. Yellow bars: amount approved in PUT option auctions for reserve accumulation, summed by calendar year and placed at the end of each year, in billions of dollars. Years without a bar are years without accumulation auctions.",
            "importa": "Reserves are the country's buffer against external shocks: they back the capacity to pay for imports and foreign-currency debt and are closely watched by rating agencies and investors. Reserve purchases also add to dollar demand in the market, so they tend to accompany periods when the Bank seeks to strengthen that buffer without fixing the exchange rate.",
            "interpretar": [
                "Reserves change with the Bank's purchases and sales, but also with returns and the valuation of its investments and of other currencies against the dollar.",
                "A PUT option gives agents the right to sell dollars to the Bank; it is exercised only if its conditions are met, so the approved amount is a ceiling, not the actual purchase.",
                "To gauge the level, it is usually compared with imports, short-term external debt or IMF adequacy metrics.",
                "Compare with the green line of the FX balance chart, which shows the change in gross reserves from FX-market flows."
            ],
            "formulas": [
                ["Annual PUT purchases", "P<sub>a</sub> = Σ<sub>s ∈ a</sub> approved amount<sub>s</sub> ÷ 10<sup>9</sup>", "s = accumulation auction held in year a; result in billions of dollars"],
                ["Net reserves", "NIR = gross reserves − the Bank's short-term external liabilities", "month-end stock, in billions of dollars"]
            ],
        },
    },
    "g-tc-volatilidad": {
        "es": {
            "que": "Mide qué tan bruscos son los movimientos diarios del peso colombiano y los compara con los del real brasileño y el peso mexicano. La volatilidad es la desviación estándar de los cambios diarios, expresada en términos anuales; es la medida estándar del riesgo cambiario de corto plazo.",
            "leer": "Tres líneas desde 2008, en porcentaje anualizado, con el último dato de cada semana: naranja para el peso colombiano, verde para el real y morada para el peso mexicano. Cada punto es la desviación estándar de los cambios logarítmicos diarios en una ventana móvil de 60 observaciones, multiplicada por √252. Una volatilidad de 15% indica que, con movimientos de esa magnitud, en un año típico la tasa varía alrededor de ±15% en una desviación estándar.",
            "importa": "La volatilidad cambiaria encarece las coberturas, complica la planeación de importadores, exportadores y deudores en dólares, y forma parte del riesgo que exigen los inversionistas extranjeros para entrar en activos en pesos. Compararla con la de monedas similares indica si la incertidumbre es regional o propia de Colombia.",
            "interpretar": [
                "Picos simultáneos en las tres monedas (como en la crisis financiera global o en la pandemia de 2020) indican choques globales; un pico solo en el peso colombiano, factores locales.",
                "La volatilidad mide la magnitud de los movimientos, no su dirección: puede subir tanto en depreciaciones como en apreciaciones rápidas.",
                "La TRM y la tasa del real se publican todos los días del calendario, repitiendo el valor en fines de semana y festivos, mientras que el peso mexicano de la Reserva Federal solo tiene días hábiles; por eso la ventana de 60 datos abarca periodos distintos y los niveles no son estrictamente comparables entre monedas.",
                "Una ventana de 60 datos reacciona rápido a los episodios de estrés pero también es ruidosa."
            ],
            "formulas": [
                ["Cambio logarítmico diario", "r<sub>d</sub> = ln(S<sub>d</sub> ÷ S<sub>d−1</sub>)", "S = unidades de moneda local por dólar en la observación d"],
                ["Volatilidad anualizada", "σ<sub>t</sub> = √[(1/(n−1)) × Σ<sub>d</sub> (r<sub>d</sub> − r̄)<sup>2</sup>] × √252 × 100", "suma sobre las últimas n = 60 observaciones (se exige al menos 48)"]
            ],
        },
        "en": {
            "que": "Measures how abrupt the Colombian peso's daily moves are and compares them with those of the Brazilian real and the Mexican peso. Volatility is the standard deviation of daily changes, expressed in annual terms; it is the standard measure of short-run currency risk.",
            "leer": "Three lines since 2008, in annualised percent, using the last value of each week: orange for the Colombian peso, green for the real and purple for the Mexican peso. Each point is the standard deviation of daily log changes over a rolling window of 60 observations, multiplied by √252. A 15% volatility means that, with moves of that size, the rate typically varies by about ±15% over a year within one standard deviation.",
            "importa": "Currency volatility makes hedging more expensive, complicates planning for importers, exporters and dollar debtors, and is part of the risk premium foreign investors demand to hold peso assets. Comparing it with similar currencies shows whether uncertainty is regional or specific to Colombia.",
            "interpretar": [
                "Simultaneous spikes in all three currencies (as in the global financial crisis or the 2020 pandemic) signal global shocks; a spike only in the Colombian peso, local factors.",
                "Volatility measures the size of moves, not their direction: it can rise in fast depreciations as well as fast appreciations.",
                "The TRM and the real rate are published for every calendar day, repeating the value on weekends and holidays, while the Federal Reserve's Mexican peso series has business days only; the 60-observation window therefore spans different periods and levels are not strictly comparable across currencies.",
                "A 60-observation window reacts quickly to stress episodes but is also noisy."
            ],
            "formulas": [
                ["Daily log change", "r<sub>d</sub> = ln(S<sub>d</sub> ÷ S<sub>d−1</sub>)", "S = units of local currency per dollar at observation d"],
                ["Annualised volatility", "σ<sub>t</sub> = √[(1/(n−1)) × Σ<sub>d</sub> (r<sub>d</sub> − r̄)<sup>2</sup>] × √252 × 100", "sum over the last n = 60 observations (at least 48 required)"]
            ],
        },
    },
}
