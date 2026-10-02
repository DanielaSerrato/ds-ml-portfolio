# Analitica de Datos con Datos del Estado Colombiano
## Plan de 8 Clases — De Excel a Power BI

**Audiencia:** Funcionarios publicos, profesionales no tecnicos, formacion corporativa (ej. MinDefensa)
**Enfoque:** Aprender analitica haciendo, siempre con datos reales del estado colombiano
**Resultado final:** Cada participante construye un dashboard en Power BI con datos publicos

---

## Estructura General

| Clase | Tema | Dataset | Herramienta |
|-------|------|---------|-------------|
| 1 | Que son los datos y por que importan | Datos abiertos Colombia — catalogo | Navegador + Excel |
| 2 | Limpieza y preparacion de datos | DANE — Poblacion por departamento | Excel |
| 3 | Estadistica descriptiva para no estadisticos | MinSalud — Vacunacion COVID por depto | Excel |
| 4 | Visualizacion: contar historias con graficos | DANE — Pobreza monetaria por departamento | Excel + primeros graficos |
| 5 | Analisis exploratorio: hacer preguntas a los datos | MinEducacion — Matriculas y desercion escolar | Excel → Power BI (intro) |
| 6 | Power BI: importar, modelar, primer visual | DANE — Mercado laboral (empleo/desempleo) | Power BI |
| 7 | Power BI intermedio: DAX, relaciones, filtros | Policia Nacional — Delitos por municipio | Power BI |
| 8 | Proyecto final: dashboard completo | Integracion de multiples datasets | Power BI |

---

## Clase 1 — Que son los datos y por que importan

### Objetivo
Entender que es un dato, una base de datos, y por que los datos abiertos del estado son una herramienta de gestion publica.

### Dataset
- **Catalogo de Datos Abiertos Colombia** (datos.gov.co)
- Exploracion guiada: cuantos datasets hay, que entidades publican, que temas cubren

### Actividades
1. Navegar datos.gov.co — encontrar 3 datasets relevantes para su trabajo
2. Descargar un CSV → abrir en Excel → identificar filas, columnas, tipos de dato
3. Discusion: "Que decision tomarian diferente si tuvieran estos datos?"

### Conceptos clave
- Dato vs informacion vs conocimiento
- Tipos de datos: numericos, categoricos, fechas, texto
- Filas = observaciones, columnas = variables
- Datos abiertos como herramienta de transparencia

### Entregable
- Lista de 3 datasets relevantes para su area con descripcion de que contienen

---

## Clase 2 — Limpieza y preparacion de datos

### Objetivo
Aprender que los datos reales vienen "sucios" y como prepararlos para analisis.

### Dataset
- **DANE — Proyecciones de poblacion por departamento y municipio (2018-2035)**
- Fuente: dane.gov.co → Poblacion → Proyecciones de poblacion
- ~1,100 municipios x multiples anos

### Actividades
1. Abrir el archivo crudo — identificar problemas (celdas combinadas, encabezados multiples, valores faltantes)
2. Limpiar: separar encabezados, eliminar filas vacias, corregir tipos
3. Tabular: crear tabla plana (municipio, departamento, ano, poblacion)
4. Filtrar: quedarse con los departamentos de interes

### Conceptos clave
- Datos crudos vs datos limpios
- Celdas combinadas, encabezados multiples (el clasico del DANE)
- Valores nulos, duplicados, inconsistencias
- Formato tabular: cada fila una observacion, cada columna una variable
- Filtros basicos en Excel

### Entregable
- Tabla limpia de poblacion por departamento lista para analisis

---

## Clase 3 — Estadistica descriptiva para no estadisticos

### Objetivo
Calcular e interpretar medidas basicas sin necesidad de formulas complejas.

### Dataset
- **MinSalud — Vacunacion COVID-19 por departamento**
- Fuente: datos.gov.co → buscar "vacunacion COVID"
- Variables: departamento, dosis aplicadas, tipo de vacuna, grupo etario, fecha

### Actividades
1. Calcular: total, promedio, mediana, minimo, maximo por departamento
2. Comparar: que departamentos vacunaron mas? Que grupos etarios?
3. Crear tabla resumen con SUMAR.SI, CONTAR.SI, PROMEDIO.SI
4. Interpretar: "Que significa que la mediana sea diferente al promedio?"

### Conceptos clave
- Media, mediana, moda — cuando usar cada una
- Rango, desviacion estandar (conceptual, no la formula)
- Distribucion: la mayoria vs los extremos
- Proporcion y tasa: "vacunados por cada 1,000 habitantes"
- Tablas dinamicas basicas

### Entregable
- Tabla resumen de vacunacion por departamento con interpretacion escrita

---

## Clase 4 — Visualizacion: contar historias con graficos

### Objetivo
Elegir el grafico correcto para cada pregunta y evitar los errores clasicos.

### Dataset
- **DANE — Pobreza monetaria y multidimensional por departamento**
- Fuente: dane.gov.co → Pobreza → Pobreza monetaria
- Variables: departamento, ano, incidencia pobreza, pobreza extrema, Gini

### Actividades
1. Crear: grafico de barras (pobreza por depto), linea (tendencia temporal), mapa de calor (tabla de colores)
2. Corregir: 5 "graficos malos" con errores clasicos (3D, pie charts con 15 categorias, ejes cortados, colores confusos)
3. Narrar: escribir 3 hallazgos en una oracion cada uno
4. Discusion: "Que historia cuenta este grafico? Que NO cuenta?"

### Conceptos clave
- Barras para comparar, lineas para tendencias, scatter para relaciones
- El mito del pie chart: cuando SI y cuando NO
- Ejes: siempre empezar en cero? No siempre — depende del contexto
- Color con proposito (no decoracion)
- Titulo = hallazgo, no descripcion

### Entregable
- 3 graficos con titulo-hallazgo y una oracion de interpretacion cada uno

---

## Clase 5 — Analisis exploratorio: hacer preguntas a los datos

### Objetivo
Aprender a formular preguntas de negocio/gestion y responderlas con datos.

### Dataset
- **MinEducacion — Matriculas, desercion y cobertura escolar por departamento**
- Fuente: datos.gov.co → buscar "estadisticas educacion" o "matricula"
- Variables: departamento, municipio, nivel educativo, ano, matriculados, desertores

### Actividades
1. Formular 5 preguntas: "Donde es mayor la desercion?", "Ha mejorado la cobertura?", "Que nivel educativo pierde mas estudiantes?"
2. Responder cada pregunta con tablas y graficos
3. Cruzar: desercion vs pobreza (usar datos de clase 4) — primera relacion entre datasets
4. Introduccion a Power BI: importar este mismo Excel → crear primer visual

### Conceptos clave
- Pregunta → dato → analisis → hallazgo → recomendacion
- Correlacion ≠ causalidad (pobreza y desercion correlacionan, pero...)
- Segmentar: por departamento, por nivel, por ano
- El valor de cruzar fuentes de datos
- Primera vista de Power BI (importar, click en visual)

### Entregable
- Documento con 5 preguntas, sus respuestas con graficos, y 1 recomendacion

---

## Clase 6 — Power BI: importar, modelar, primer visual

### Objetivo
Aprender el flujo basico de Power BI: datos → modelo → visual → publicar.

### Dataset
- **DANE — Gran Encuesta Integrada de Hogares (mercado laboral)**
- Tasa de desempleo, ocupacion, informalidad por departamento y trimestre
- Fuente: dane.gov.co → Mercado laboral

### Actividades
1. Importar CSV a Power BI
2. Power Query: limpiar, renombrar columnas, cambiar tipos
3. Crear tabla de fechas (DimFecha)
4. Primer visual: tasa de desempleo por departamento (mapa + barras)
5. Filtros: slicer por ano, por departamento
6. Formato: titulo, colores, ejes legibles

### Conceptos clave
- ETL en Power Query: Extract → Transform → Load
- Modelo estrella simplificado: tabla de hechos + dimension fecha
- Tipos de visuales: tarjeta, barra, linea, mapa, tabla
- Slicers y filtros
- Formato profesional: menos es mas

### Entregable
- .pbix con dashboard de 1 pagina: empleo/desempleo por departamento

---

## Clase 7 — Power BI intermedio: DAX, relaciones, filtros

### Objetivo
Crear medidas calculadas y conectar multiples tablas para analisis mas profundo.

### Dataset
- **Policia Nacional — Delitos por municipio (hurtos, homicidios, lesiones)**
- Fuente: datos.gov.co → buscar "delitos" o "policia nacional"
- Variables: departamento, municipio, tipo delito, ano, mes, cantidad
- PLUS: tabla de poblacion (de clase 2) para calcular tasas

### Actividades
1. Importar 2 tablas: delitos + poblacion
2. Crear relacion: municipio/departamento
3. DAX basico:
   - Total Delitos = SUM(delitos[cantidad])
   - Tasa por 100K = DIVIDE([Total Delitos], [Poblacion]) * 100000
   - Variacion Anual = ([Este Ano] - [Ano Anterior]) / [Ano Anterior]
4. Dashboard de 2 paginas:
   - Pagina 1: panorama nacional (mapa + KPIs + tendencia)
   - Pagina 2: detalle por tipo de delito (barras + tabla drill-down)

### Conceptos clave
- DAX: SUM, DIVIDE, CALCULATE, FILTER, SAMEPERIODLASTYEAR
- Relaciones entre tablas: la clave foranea
- Medidas vs columnas calculadas
- Drill-down y drill-through
- Contexto de filtro (por que CALCULATE existe)

### Entregable
- .pbix con 2 paginas: seguridad nacional + detalle por delito

---

## Clase 8 — Proyecto final: dashboard completo

### Objetivo
Integrar todo lo aprendido en un dashboard ejecutivo con multiples fuentes de datos.

### Datasets (combinados)
- Poblacion (clase 2)
- Pobreza (clase 4)
- Educacion (clase 5)
- Empleo (clase 6)
- Seguridad (clase 7)
- PLUS: Presupuesto de inversion publica (datos.gov.co → "inversion publica" o "SGR")

### Actividades
1. Disenar: que historia quiero contar? Para quien?
2. Construir modelo de datos: 4-5 tablas relacionadas por departamento
3. Dashboard de 3-4 paginas:
   - Pagina 1: Panorama departamental (mapa + KPIs sociales y economicos)
   - Pagina 2: Educacion y empleo (relacion desercion → desempleo)
   - Pagina 3: Seguridad y pobreza (correlaciones por departamento)
   - Pagina 4: Inversion publica vs resultados
4. Presentar: cada grupo expone sus hallazgos y recomendaciones

### Conceptos clave
- Modelo de datos multi-tabla (star schema real)
- Data storytelling: inicio → nudo → desenlace
- Audiencia: no es lo mismo un dashboard para el ministro que para un analista
- De "que paso" a "que deberiamos hacer"

### Entregable
- .pbix con dashboard de 3-4 paginas
- Presentacion de 5 minutos con hallazgos y recomendaciones

---

## Progresion de herramientas

```
Clase 1-4: Excel (zona de confort)
Clase 5: Excel → Power BI (transicion)
Clase 6-7: Power BI (inmersion)
Clase 8: Power BI (proyecto integrador)
```

## Progresion de complejidad

```
Clase 1: Navegar datos         → "que hay?"
Clase 2: Limpiar datos         → "estan listos?"
Clase 3: Describir datos       → "que dicen los numeros?"
Clase 4: Visualizar datos      → "que historia cuentan?"
Clase 5: Explorar datos        → "que preguntas puedo hacer?"
Clase 6: Modelar en Power BI   → "como lo automatizo?"
Clase 7: DAX y relaciones      → "como conecto fuentes?"
Clase 8: Dashboard integrador  → "como lo presento para decidir?"
```

## Datasets del estado usados

| Fuente | Dataset | Clase |
|--------|---------|-------|
| datos.gov.co | Catalogo de datos abiertos | 1 |
| DANE | Poblacion por departamento | 2 |
| MinSalud | Vacunacion COVID | 3 |
| DANE | Pobreza monetaria | 4 |
| MinEducacion | Matriculas y desercion | 5 |
| DANE | Mercado laboral (GEIH) | 6 |
| Policia Nacional | Delitos por municipio | 7 |
| Varios + SGR | Integracion multi-fuente | 8 |

---

## Para el portfolio

Cada clase genera un proyecto mostrable:
- Clases 1-5: ejercicios con datos reales colombianos (Excel + narrativa)
- Clases 6-7: dashboards Power BI con datos del estado
- Clase 8: dashboard integrador multi-fuente

Estos proyectos se agregan al portfolio como seccion **"Analisis de Datos con Datos de Colombia"** — muestra capacidad de formacion corporativa + analisis con datos publicos reales.
