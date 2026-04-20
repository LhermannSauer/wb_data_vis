# Los Tres Pilares del Desarrollo

**TP Final — Visualización de la Información, ECD 2025**
## https://lhermannsauer.github.io/wb_data_vis/

---

Exploración de la relación entre apertura económica, calidad institucional y conectividad digital con el desarrollo humano, usando datos del World Bank Data360.

### Visualizaciones

| Viz | Descripción | Link a Observable |
|-----|-------------| ----------------- |
| [Coordenadas Paralelas](html/three_pillars_parallel.html) | Cada línea es un país. Siete ejes representan los tres pilares; el color codifica el IDH. Permite buscar y comparar países. | https://observablehq.com/d/9bd7123642e7142d |
| [Cartograma No Contiguo](html/cartogram.html) | Mapa mundial donde cada país se escala al indicador seleccionado. 8 variables con transiciones animadas. | https://observablehq.com/d/ec709763a3e708b5 |
| [Scatter Plot Animado](html/pilar3_digital_development.html) | Internet vs. e-gobierno para 182 países, animado de 2000 a 2022. El tamaño de burbuja codifica el IDH. | https://observablehq.com/@itba26/conectividad-digital-y-apertura-comercial |

### Bases de datos disponibles
Para este trabajo se uso la API Data360, que es el nuevo portal unificado del Banco Mundial. Consolida más de 300 millones de puntos de datos provenientes de múltiples bases de datos institucionales, todas accesibles bajo un mismo prefijo de identificación (DATABASE_ID). Las principales incluyen: WB_WDI (World Development Indicators, el catálogo más grande con miles de series macroeconómicas y sociales), WB_HNP (Health, Nutrition and Population), WB_ED (Education Statistics), WB_GEM (Global Economic Monitor), WB_FINDEX (Global Findex Database sobre inclusión financiera) y WB_DEC (Development Economics), entre otras. La plataforma está organizada además en cinco grandes temáticas transversales —People, Prosperity, Planet, Infrastructure y Digital— que funcionan como etiquetas de clasificación para facilitar la exploración por área de desarrollo.


### Indicadores disponibles y estructura de los datos
Data360 consolida más de 10.000 indicadores desagregados por sexo, edad, empleo, ubicación, nivel de ingresos y nivel educativo, cubriendo más de 200 economías. World Bank Blogs Desde el punto de vista de la API, cada observación está identificada por un conjunto fijo de dimensiones: DATABASE_ID (dataset de origen), INDICATOR (código único del indicador), REF_AREA (código ISO3 del país o región), TIME_PERIOD (año o período) y FREQ (frecuencia: anual, trimestral o mensual). Sobre esa base se añaden dimensiones de desagregación opcionales —SEX, AGE, URBANISATION y hasta tres COMP_BREAKDOWN específicos de cada indicador— que permiten cortes por subpoblación. El valor observado se almacena en OBS_VALUE (string numérico) acompañado de metadatos de calidad como OBS_STATUS (normal / estimado / provisional), LATEST_DATA (si es el dato más reciente disponible), UNIT_MEASURE (unidad: porcentaje, índice, moneda local, etc.) y UNIT_MULT (multiplicador: unidades, miles, millones). La metadata completa de cada indicador —nombre, descripción, fuente, topics, metodología— se accede separadamente vía el endpoint POST /data360/metadata usando consultas OData, lo que permite descubrir el catálogo sin necesidad de conocer los códigos de antemano.

### Metodología
Para explorar la información disponible, comenzamos leyendo la documentación oficial de la API de World Bank Data360, identificando los endpoints disponibles y la lógica de consulta. Quedó en evidencia que el volumen de datos es considerable: la plataforma expone decenas de bases de datos, más de 10.000 indicadores y múltiples dimensiones de desagregación por país, tiempo, sexo, edad y urbanización, lo que hacía inviable una exploración interactiva celda por celda. Por eso optamos por una estrategia de descarga directa: ejecutamos consultas contra la API y persistimos los resultados en archivos Parquet dentro de la carpeta data/raw, un formato columnar eficiente para este tipo de datos tabulares densos. Con los archivos en local, utilizamos la extensión de consulta Parquet dentro de Visual Studio Code para explorar y filtrar el dataset sin necesidad de levantar ningún entorno adicional, seleccionando los indicadores y países de interés. A partir de esa selección final generamos las visualizaciones presentadas en este informe.

Análisis y descarga de datos disponible en los siguientes notebooks:
* notebooks/worldbank_data360_explorer.ipynb
* notebooks/pilar3_digital_development.ipynb
* notebooks/data_extraction.ipynb


