# Reporte del Proyecto — Tres Pilares del Desarrollo

**Materia:** Visualizacion de la Informacion — ECD 2025  
**Datos:** World Bank Data360 API  
**Tecnologia:** D3.js v7, TopoJSON, Python (pandas, pyarrow, duckdb)

---

## 1. Extraccion de Datos

Se utilizo la API REST del World Bank Data360 (`data360api.worldbank.org`) para extraer indicadores de multiples bases de datos. Los datos fueron almacenados en formato Parquet en `data/raw/`, organizados por tema:

- **trade/** — Exportaciones, importaciones, comercio % PIB, restricciones comerciales
- **commerce/** — Logistica, negocios registrados, comercio digital
- **fdi/** — Inversion extranjera directa (entrante y saliente), barreras a la IED
- **wealth/** — Riqueza nacional integral, capital humano, capital producido
- **development/** — IDH, asistencia oficial al desarrollo, I+D
- **internet/** — Penetracion de internet, banda ancha, gobierno electronico
- **freedom/** — Puntaje Freedom House, libertades civiles, derechos politicos
- **governance/** — Estado de derecho, control de corrupcion, estabilidad politica

El script de extraccion (`notebooks/data_extraction.ipynb`) realiza paginacion automatica (max 1000 registros por request) y almacena cada indicador como un archivo Parquet individual.

### Estructura de cada observacion

| Campo | Descripcion |
|---|---|
| `OBS_VALUE` | Valor numerico del indicador |
| `REF_AREA` | Codigo ISO3 del pais |
| `TIME_PERIOD` | Ano |
| `INDICATOR` | Codigo del indicador |
| `DATABASE_ID` | Base de datos fuente |
| `UNIT_MEASURE` | Unidad (%, USD, indice, etc.) |

---

## 2. Exploracion de Datos

En `notebooks/data_exploration.ipynb` se realizo:

- Inventario de todos los archivos Parquet extraidos (18 carpetas tematicas)
- Analisis de cobertura por pais y ano para cada indicador
- Identificacion de los indicadores con mayor cobertura global (~160-250 paises)
- Seleccion de variables clave para las visualizaciones

---

## 3. Preparacion de Datos para D3

Se crearon scripts de preparacion (`viz/prepare_data.py`) que:

1. Leen los archivos Parquet relevantes con pandas
2. Seleccionan el ultimo valor disponible por pais para cada indicador
3. Cruzan indicadores por codigo ISO3 de pais
4. Agregan coordenadas geograficas (lat/lon) y asignacion de region del Banco Mundial
5. Exportan a JSON para consumo directo en D3.js

Para el cartograma, se construyo un mapeo de codigos ISO3 a codigos ISO numericos (usados por el TopoJSON de Natural Earth) para hacer join con los datos geograficos.

---

## 4. Visualizaciones

### 4.1. Coordenadas Paralelas — Tres Pilares (`three_pillars_parallel.html`)

**Tipo:** Grafico de coordenadas paralelas  
**Interactividad:** Busqueda y seleccion de paises, hover para detalle, agregar/quitar paises  
**Datos:** 23 paises con datos manuales curados para 7 indicadores  

Siete ejes representan indicadores de los tres pilares:
- **Apertura economica:** Comercio % PIB, IED Entrante
- **Instituciones:** Libertades civiles, Estado de derecho, Control de corrupcion
- **Conectividad:** Internet %, Indice de E-Gobierno

El color de cada linea codifica el IDH usando una rampa azul monocromatica.

### 4.2. Cartograma No Contiguo (`cartogram.html`)

**Tipo:** Cartograma no contiguo (non-contiguous cartogram)  
**Interactividad:** 8 botones para cambiar variable de tamano, hover para detalle  
**Datos:** 162 paises con datos del World Bank Data360  

Inspirado en el ejemplo de Mike Bostock (Observable). Cada pais conserva su forma geografica real pero se escala alrededor de su centroide proporcionalmente a la variable seleccionada. Siluetas grises muestran las fronteras originales como referencia.

La tecnica clave es la transformacion SVG:
```
translate(cx, cy) scale(factor) translate(-cx, -cy)
```

### 4.3. Scatter Plot Animado — Brecha Digital (`pilar3_digital_development.html`)

**Tipo:** Scatter plot animado (estilo Gapminder)  
**Interactividad:** Slider temporal (2000-2022), boton de animacion, filtro por region  
**Datos:** 5,008 observaciones, 182 paises, 23 anos  

Muestra la relacion entre penetracion de internet (eje X) e IDH (eje Y) a lo largo del tiempo. El tamano de cada burbuja codifica el indice de gobierno electronico. El color codifica la region del Banco Mundial.

---

## 5. Diseno Visual

Se adopto un sistema de diseno consistente para las tres visualizaciones:

- **Tipografia:** DM Sans (cuerpo) + DM Mono (etiquetas, ejes, monoespaciado)
- **Paleta:** Fondo beige calido (#f7f5f0), superficie blanca, tinta oscura
- **Colores de pilares:** Dorado (#c9a96e), Verde (#6e9e8a), Azul (#7a8bbf)
- **Tooltip:** Fondo blanco con sombra sutil, datos organizados en filas
- **Layout:** Header con titulo y leyenda, barra de controles, area de grafico, footer con fuentes

---

## 6. Pagina Principal (index.html)

Se creo una pagina de indice en la raiz del repositorio para uso como GitHub Pages que incluye:

- Titulo y descripcion del proyecto
- Las 5 preguntas de investigacion
- Links a las 3 visualizaciones interactivas
- Tabla de definicion de todas las variables utilizadas con sus fuentes

---

## 7. Estructura del Repositorio

```
tp_final/
├── index.html                          # Pagina principal (GitHub Pages)
├── REPORT.md                           # Este reporte
├── pyproject.toml                      # Dependencias Python
├── brainstorming.md                    # Ideas iniciales del proyecto
├── data/
│   └── raw/                            # Datos crudos del World Bank (Parquet)
│       ├── trade/                      # 21 indicadores de comercio
│       ├── commerce/                   # 14 indicadores de negocios
│       ├── fdi/                        # 17 indicadores de IED
│       ├── wealth/                     # 6 indicadores de riqueza
│       ├── development/                # 18 indicadores de desarrollo
│       ├── internet/                   # 16 indicadores de conectividad
│       ├── freedom/                    # 20 indicadores de libertad
│       ├── governance/                 # 20 indicadores de gobernanza
│       └── ...                         # Otras carpetas tematicas
├── html/
│   ├── three_pillars_parallel.html     # Vis 1: Coordenadas paralelas
│   ├── cartogram.html                  # Vis 2: Cartograma no contiguo
│   └── pilar3_digital_development.html # Vis 3: Scatter animado
├── notebooks/
│   ├── data_extraction.ipynb           # Extraccion de datos de la API
│   ├── data_exploration.ipynb          # Exploracion y analisis
│   └── pilar3_digital_development.ipynb # Preparacion de datos para scatter
└── viz/
    ├── prepare_data.py                 # Script de preparacion de datos
    └── data.json                       # Datos procesados para D3
```

---

## 8. Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| Python 3.12 | Extraccion y procesamiento de datos |
| pandas / pyarrow | Lectura de Parquet, manipulacion de datos |
| duckdb | Consultas analiticas sobre Parquet |
| D3.js v7 | Visualizaciones interactivas |
| TopoJSON | Datos geograficos (Natural Earth 110m) |
| DM Sans / DM Mono | Tipografia del sistema de diseno |
