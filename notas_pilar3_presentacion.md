# Pilar 3: Conectividad Digital y Desarrollo Humano
## Notas de presentación — TP InfoVis ECD 2025 A

---

## 1. ¿Qué muestra esta visualización?

Un scatter plot interactivo D3.js que responde la pregunta: **¿existe una relación entre la penetración de internet y el desarrollo humano de un país?**

Cada burbuja es un país. Se codifican 5 dimensiones simultáneamente:

| Canal visual | Variable | Fuente |
|---|---|---|
| Posición X | % de población que usa internet | WDI — IT.NET.USER.ZS |
| Posición Y | Índice de Desarrollo Humano (HDI) | UNDP vía Data360 |
| Tamaño | E-Government Development Index | UN EGDI vía Data360 |
| Color | Región del mundo | World Bank country metadata |
| Interactividad temporal | Año (slider 1990–2022) | TIME_PERIOD en los datos |

---

## 2. Datos utilizados

- **5008 registros** totales
- **182 países** con datos de internet + HDI
- **33 años** de cobertura (1990–2022)
- Variables adicionales en tooltip: broadband por 100 hab, brecha de género digital

### Archivos parquet utilizados (de la carpeta `raw/`):

**Carpeta `internet/`:**
- `individuals_using_internet_(%_population).parquet`
- `individuals_using_internet,_female_(%_female_population).parquet`
- `individuals_using_internet,_male_(%_male_population).parquet`
- `broadband_internet_subscribers_per_100_pop.parquet`

**Carpeta `development/`:**
- `human_development_index_(hdi)_[highest_=_1].parquet`
- `e-gov_development_index_(un_egdi)_-_overall_score.parquet`

### Estructura de los parquets:
Todos los archivos comparten la misma estructura proveniente de la API Data360:

- `REF_AREA`: código ISO3 del país (ej: ARG, USA, NGA)
- `TIME_PERIOD`: año
- `OBS_VALUE`: valor numérico del indicador
- `INDICATOR`: código del indicador en Data360
- `DATABASE_ID`: dataset de origen (ej: WB_WDI, VDEM_CORE)
- `SEX`, `AGE`, `URBANISATION`: dimensiones de desagregación
- `FREQ`: frecuencia (anual)

### Procesamiento:
1. Limpieza: filtrado de valores nulos, conversión numérica, eliminación de agregados regionales
2. Merge por `REF_AREA` + `year` de los 6 indicadores
3. Cálculo de brecha de género: `internet_male - internet_female`
4. Enriquecimiento con metadata de región e income group via API v2 del World Bank
5. Exportación a JSON para consumo de D3.js

---

## 3. Decisiones de diseño

### ¿Por qué un scatter plot?
- Es el gráfico más efectivo para mostrar **correlación entre dos variables continuas**
- Los canales adicionales (tamaño, color) permiten codificar 4-5 dimensiones sin sobrecargar
- Con animación temporal se agrega una dimensión más (tiempo)

### ¿Por qué D3.js?
- Permite interactividad real (hover, click, animación temporal)
- Control total sobre la estética y los elementos SVG
- El slider temporal es esencial para la narrativa: muestra la "revolución digital" en movimiento

### Paleta de colores:
Se usó una paleta categórica de 7 colores para las regiones del World Bank, con suficiente contraste para diferenciarse sobre fondo oscuro. Dark theme para consistencia con las visualizaciones del Pilar 1 del equipo.

### Tamaño de burbuja:
Se usó escala `sqrt` (raíz cuadrada) para que el área sea proporcional al valor, evitando la distorsión perceptual de la escala lineal en radio.

---

## 4. Hallazgos clave (lo que dirías al presentar)

### Hallazgo 1: Correlación fuerte pero no lineal
Hay una relación positiva clara entre internet y HDI. Pero no es lineal: existe un **"codo" alrededor del 40-60% de penetración** donde el HDI se acelera. Esto sugiere que hay un umbral mínimo de conectividad necesario para impulsar el desarrollo.

### Hallazgo 2: Clusters regionales revelan desigualdad estructural
- **Europa + Norteamérica**: cuadrante superior derecho (alta conectividad + alto HDI)
- **África Subsahariana**: cuadrante inferior izquierdo (baja conectividad + bajo HDI)
- **LATAM y Asia**: la mayor dispersión — sugiere que otros factores (instituciones del Pilar 2, inversión del Pilar 1) moderan la relación
- **Medio Oriente**: casos interesantes como UAE y Qatar con 100% internet pero HDI no tan alto como Europa nórdica

### Hallazgo 3: La animación temporal revela la "revolución digital"
Animando desde 1990 hasta 2022:
- En 1990-2000: la mayoría de los países están en el extremo izquierdo (<10% internet)
- En 2005-2015: "explosión" hacia la derecha — muchos países saltan de <20% a >50%
- El HDI (eje Y) se mueve mucho más lento — **la conectividad digital avanza más rápido que el desarrollo humano integral**
- Esto sugiere que internet es condición necesaria pero no suficiente para el desarrollo

### Hallazgo 4: Brecha de género digital (visible en tooltips)
En países con baja penetración (<30%), la brecha de género (diferencia internet masculino vs femenino) es significativamente mayor (hasta 15-20 puntos porcentuales). A medida que un país se digitaliza más, la brecha tiende a cerrarse. Esto tiene implicancias para políticas de inclusión digital.

### Hallazgo 5: E-Government como proxy de digitalización estatal
Los países con burbujas más grandes (alto EGDI) tienden a estar más arriba y a la derecha. Esto sugiere que la digitalización del gobierno acompaña (o impulsa) tanto la conectividad como el desarrollo humano.

---

## 5. Conexión con la tesis general del trabajo

**Tesis: "Apertura económica, instituciones y conectividad: los tres pilares del desarrollo"**

El Pilar 3 demuestra que la conectividad digital está fuertemente asociada al desarrollo humano, pero con matices importantes:

- No es una relación determinista: hay países con alta conectividad pero HDI moderado (petro-estados del Golfo) y países con HDI relativamente alto pero conectividad moderada (algunos de LATAM)
- La dispersión en LATAM y Asia sugiere que los **Pilares 1 y 2 (comercio e instituciones) actúan como moderadores**: países con buenas instituciones y apertura comercial logran "convertir" mejor su conectividad en desarrollo real
- El Pilar 3 es el que más rápido se mueve temporalmente, lo que lo convierte en el vector más dinámico de los tres

---

## 6. Aspectos técnicos para preguntas del profesor

### Sobre la API Data360:
- Los datos se obtuvieron de `data360api.worldbank.org`
- Los parquets fueron generados consultando el endpoint `/data360/data` con los indicadores del dataset WB_WDI y otros
- La estructura SDMX incluye dimensiones como SEX, AGE, URBANISATION para desagregación

### Sobre D3.js:
- Se usa D3 v7 cargado desde CDN
- Escalas: `scaleLinear` para X e Y, `scaleSqrt` para radio
- Transiciones de 400ms para las burbujas al cambiar de año
- Patrón enter/update/exit para data binding eficiente
- El HTML se genera desde Python (Colab) inyectando el JSON de datos directamente en el script

### Sobre las limitaciones:
- HDI y datos de internet no están disponibles para todos los países en todos los años
- La cobertura de E-Government Index es bienal (solo años pares), por lo que en años impares las burbujas no tienen tamaño variable
- La brecha de género solo tiene buena cobertura desde ~2007 en adelante
- Correlación no implica causalidad: internet no necesariamente "causa" mayor HDI ni viceversa

---

## 7. Datos extremos para mencionar en la presentación

**Top 5 internet 2022:**
1. UAE — 100% internet, HDI 0.866
2. Bahrain — 100% internet, HDI 0.838
3. Saudi Arabia — 100% internet, HDI 0.857
4. Iceland — 99.8% internet, HDI 0.938
5. Kuwait — 99.7% internet, HDI 0.808

**Bottom 5 internet 2022:**
1. Burundi — 11.0% internet, HDI 0.423
2. Uganda — 11.1% internet, HDI 0.528
3. Chad — 12.5% internet, HDI 0.401
4. Burkina Faso — 14.6% internet, HDI 0.434
5. Malawi — 17.0% internet, HDI 0.485

**Caso interesante — Argentina (2022):**
Buscar ARG en el tooltip para tener el dato exacto y comparar con la región.

---
