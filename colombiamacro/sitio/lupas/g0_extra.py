"""Lupas escritas a mano para graficos que no estaban en el inventario inicial."""

LUPAS = {
    "g-informal-ciudades": {
        "es": {
            "que": "Ordena las 23 ciudades y áreas metropolitanas (A.M.) que mide la GEIH según la proporción de sus ocupados que trabajan en la informalidad. Muestra que el problema tiene una geografía marcada: las ciudades más grandes e industriales tienden a tener menos informalidad que las ciudades intermedias y de la región Caribe, y permite ver si cada ciudad mejora o empeora frente a un año antes.",
            "leer": "Cada barra horizontal es una ciudad, ordenada de menor a mayor informalidad; el eje va de 0% a 80% de los ocupados. Las barras azules son las 13 ciudades y áreas metropolitanas principales; las grises, las otras 10 capitales. La raya vertical negra sobre cada barra marca el dato del mismo trimestre móvil un año antes. Al pasar el cursor se ven la tasa, el dato de hace un año y el cambio en pp.",
            "importa": "La informalidad local indica qué tan formal es el mercado laboral en cada plaza: afecta la capacidad de los hogares de acceder a crédito, la base de cotización a la seguridad social y el recaudo de impuestos locales. Para un inversionista ayuda a dimensionar el mercado formal de consumo y la disponibilidad de trabajadores formales en cada ciudad.",
            "interpretar": [
                "Una barra que termina a la izquierda de su raya indica que la informalidad de esa ciudad bajó frente a un año antes; a la derecha, que subió.",
                "Las diferencias entre ciudades reflejan su estructura productiva (industria y servicios modernos frente a comercio y servicios personales) más que cambios de corto plazo.",
                "Las ciudades pequeñas tienen muestras más pequeñas en la GEIH: cambios de 1–2 pp en un año pueden estar dentro del error de muestreo.",
                "Compárelo con la informalidad por rama: una ciudad con mucho comercio y transporte tiende a tener tasas más altas."
            ],
            "formulas": [
                ["Informalidad de la ciudad", "INF<sub>c</sub> = I<sub>c</sub> ÷ O<sub>c</sub> × 100", "I = ocupados informales; O = ocupados de la ciudad c; trimestre móvil"],
                ["Cambio en un año", "ΔINF<sub>c</sub> = INF<sub>c,t</sub> − INF<sub>c,t−12</sub>", "en puntos porcentuales (pp)"]
            ]
        },
        "en": {
            "que": "This chart ranks the 23 cities and metropolitan areas measured by the GEIH by the share of their employed people who work informally. It shows that informality has a clear geography: the larger, more industrial cities tend to have less informality than mid-sized cities and those in the Caribbean region, and it shows whether each city is improving or worsening versus a year earlier.",
            "leer": "Each horizontal bar is a city, sorted from lowest to highest informality; the axis runs from 0% to 80% of employed people. Blue bars are the 13 main cities and metropolitan areas; grey bars are the other 10 capitals. The black vertical tick on each bar is the same rolling quarter a year earlier. Hovering shows the rate, the year-earlier figure and the change in pp.",
            "importa": "Local informality shows how formal each city's labour market is: it affects households' access to credit, the social security contribution base and local tax revenue. For an investor it helps size the formal consumer market and the availability of formal workers in each city.",
            "interpretar": [
                "A bar ending left of its tick means the city's informality fell versus a year earlier; to the right, it rose.",
                "Differences between cities mostly reflect their economic structure (industry and modern services versus retail and personal services) rather than short-term changes.",
                "Smaller cities have smaller GEIH samples: changes of 1–2 pp over a year may be within sampling error.",
                "Compare with informality by sector: a city with a lot of retail and transport tends to have higher rates."
            ],
            "formulas": [
                ["City informality", "INF<sub>c</sub> = I<sub>c</sub> ÷ E<sub>c</sub> × 100", "I = informal workers; E = employed in city c; rolling quarter"],
                ["Change over a year", "ΔINF<sub>c</sub> = INF<sub>c,t</sub> − INF<sub>c,t−12</sub>", "in percentage points (pp)"]
            ]
        },
    },
}
