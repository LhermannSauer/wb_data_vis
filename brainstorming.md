# TP Final – Visualizacion de Datos con World Bank Data360

## API Data360 – Resumen

**Base URL:** `https://data360api.worldbank.org`

### Endpoints

| Endpoint | Metodo | Descripcion |
|---|---|---|
| `/data360/data` | GET | Obtener datos filtrados por base, indicador, pais, periodo, sexo, edad, etc. Paginado (max 1000 por request, usar `skip`). |
| `/data360/indicators` | GET | Listar IDs de indicadores de una base de datos (`?datasetId=WB_WDI`). |
| `/data360/searchv2` | POST | Busqueda por texto libre con filtros OData por topic, tipo, base. Soporta facets y paginacion. |
| `/data360/metadata` | POST | Metadatos detallados de indicadores (descripcion, fuente, metodologia). |
| `/data360/disaggregation` | GET | Desagregaciones disponibles para un indicador (sexo, edad, urbanizacion, etc.). |

### Estructura de cada observacion

| Campo | Descripcion | Ejemplo |
|---|---|---|
| `DATABASE_ID` | Base de datos fuente | `WB_WDI` |
| `INDICATOR` | Codigo del indicador | `WB_WDI_IT_NET_USER_ZS` |
| `REF_AREA` | Pais/region (ISO) | `ARG`, `BRA`, `LAC` |
| `TIME_PERIOD` | Anio | `2020` |
| `OBS_VALUE` | Valor numerico | `87.12` |
| `SEX` | Sexo (`M`, `F`, `_T`=total) | `_T` |
| `AGE` | Grupo etario | `_T` |
| `URBANISATION` | Urbano/rural | `_T` |
| `UNIT_MEASURE` | Unidad (`PT`=%, `USD`, etc.) | `PT` |
| `COMMENT_TS` | Nombre legible del indicador | `Individuals using the Internet (% of population)` |

### Bases de datos disponibles (50 total, ~12,800 indicadores)

Las mas relevantes:

| ID | Nombre | Indicadores |
|---|---|---|
| `WB_WDI` | World Development Indicators | 1,526 |
| `IMF_BOP` | IMF Balance of Payments | 1,147 |
| `WB_EDSTATS` | Education Statistics | 1,073 |
| `IMF_FSI` | Financial Soundness Indicators | 594 |
| `WB_ES` | Enterprise Surveys | 583 |
| `IMF_IFS` | International Financial Statistics | 496 |
| `WB_GS` | Gender Statistics | 364 |
| `WB_FINDEX` | Global Findex (Inclusion Financiera) | 281 |
| `WB_HNP` | Health, Nutrition & Population | 193 |
| `OWID_CB` | Our World in Data – Carbon Budget | 77 |
| `WB_CCKP` | Climate Change Knowledge Portal | 41 |
| `ITU_DH` | ITU Digital/Telecom | 39 |

### Temas principales

Prosperity (7,707) · Economic Policy (3,657) · Finance (1,625) · Trade (1,168) · People (954) · Institutions (938) · Planet (750) · Gender (457) · Poverty (423) · Climate Change (271) · Digital (234) · Health (133) · Agriculture (132)

---

## Propuestas de Visualizacion

### Idea A: "La Brecha Digital en America Latina"

**Angulo:** Evolucion del acceso a internet y telecomunicaciones en LATAM comparado con el mundo. Quien avanza y quien se queda atras.

**Indicadores:**
- `WB_WDI_IT_NET_USER_ZS` – Individuos usando internet (% poblacion)
- `ITU_DH_HH_INT` – Hogares con acceso a internet (%)
- `ITU_DH_INT_BAND_PER_CAP` – Ancho de banda internacional per capita
- `WB_WDI_IT_CEL_SETS_P2` – Suscripciones a celulares por 100 hab.

**Paises:** ARG, BRA, CHL, COL, MEX, PER, URY + promedios regionales (LAC, EAS, ECS)

**3 visualizaciones:**
1. **Line chart interactivo** – Evolucion 2000-2023 del % internet por pais, con slider temporal
2. **Mapa coropletico de LATAM** – Ultimo dato de penetracion, click para ver serie temporal
3. **Bump chart** – Ranking de paises en conectividad a lo largo del tiempo

**Alineacion:** Directa con el desafio MediaParty "Global Digital Challenge 360".

---

### Idea B: "Clima y Emisiones: America Latina frente al mundo"

**Angulo:** LATAM emite poco CO2 pero sufre desproporcionadamente los efectos del cambio climatico. La asimetria global.

**Indicadores:**
- `WB_WDI_EN_GHG_CO2_MT_CE_AR5` – Emisiones CO2 totales (Mt CO2e)
- `OWID_CB_CUMULATIVE_CO2_INCLUDING_LUC` – CO2 acumulado historico
- `WB_WDI_EN_ATM_CO2E_PC` – CO2 per capita
- `WB_CCKP_HD35` – Dias calurosos (Tmax>35C)
- `WB_WDI_EG_USE_PCAP_KG_OE` – Uso de energia per capita

**Paises:** Top emisores globales (CHN, USA, IND, RUS, JPN) vs LATAM (ARG, BRA, MEX, COL, CHL)

**3 visualizaciones:**
1. **Stacked area chart** – Emisiones globales por region/pais (1970-2023)
2. **Scatter plot animado** – CO2 per capita vs PIB per capita, burbujas por poblacion (estilo Gapminder)
3. **Heatmap** – Dias calurosos por pais y anio, tendencia de calentamiento

---

### Idea C: "Desigualdad y Genero: El mapa de las brechas"

**Angulo:** Donde naciste define tu futuro. Brechas de genero en educacion, empleo y participacion economica.

**Indicadores:**
- `WB_GS_SL_UEM_ZS` – Desempleo por sexo (%)
- `WB_GS_SE_PRM_GINT_ZS` – Tasa bruta de ingreso escolar
- `WB_GS_SG_VAW_1549_ZS` – Violencia contra la mujer (%)
- `WB_WDI_SI_POV_GINI` – Indice de Gini
- `WB_GS_SP_HOU_FEMA_ZS` – Hogares con jefatura femenina (%)

**Paises:** Foco LATAM o seleccion global representativa

**3 visualizaciones:**
1. **Dumbbell chart** – Brecha hombre vs mujer en desempleo/educacion por pais
2. **Radar chart interactivo** – Perfil multidimensional de igualdad de genero por pais
3. **Mapa + small multiples** – Gini mundial + evolucion temporal de paises seleccionados

---

## Stack Tecnico Recomendado

### Google Colab + Python
```
requests        -> consumir la API
pandas          -> manipulacion de datos
plotly          -> visualizaciones interactivas (mapas, scatter, line)
altair          -> graficos declarativos
ipywidgets      -> controles interactivos en Colab
```

### Alternativa: Observable
```
Plot / D3.js    -> visualizaciones custom
fetch()         -> consumir la API
Vega-Lite       -> graficos declarativos
```

---

## Codigo base para consumir la API

```python
import requests
import pandas as pd

BASE = "https://data360api.worldbank.org"

def search_indicators(topic, keyword="*", top=20):
    """Buscar indicadores por tema."""
    resp = requests.post(f"{BASE}/data360/searchv2", json={
        "count": True,
        "filter": f"series_description/topics/any(t: t/name eq '{topic}') and type eq 'indicator'",
        "select": "series_description/idno, series_description/name, series_description/database_id",
        "search": keyword,
        "top": top
    })
    return resp.json()

def get_data(database_id, indicator, countries=None, time_from=None, time_to=None):
    """Obtener datos con paginacion automatica."""
    params = {"DATABASE_ID": database_id, "INDICATOR": indicator}
    if countries:
        params["REF_AREA"] = countries
    if time_from:
        params["timePeriodFrom"] = time_from
    if time_to:
        params["timePeriodTo"] = time_to

    all_data = []
    skip = 0
    while True:
        params["skip"] = skip
        resp = requests.get(f"{BASE}/data360/data", params=params)
        values = resp.json().get("value", [])
        all_data.extend(values)
        if len(values) < 1000:
            break
        skip += 1000

    return pd.DataFrame(all_data)
```

---

## Recomendacion

La **Idea A (Brecha Digital)** es la mejor opcion si participan del desafio MediaParty: datos abundantes, visualizaciones variadas, angulo periodistico claro. Si no, la **Idea B (Clima)** tiene mayor impacto visual y narrativo.

## Proximos pasos

1. Elegir idea final
2. Verificar disponibilidad de datos para los indicadores elegidos
3. Crear notebook en Colab
4. Implementar las 3 visualizaciones interactivas
5. Agregar narrativa contextual
6. Entregar antes del 02/04/2026 23:59
