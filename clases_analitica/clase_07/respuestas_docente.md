# Clase 7 — Respuestas Docente

## Dataset: PoliciaNacional_delitos_municipio.csv
- 14,399 registros (30 municipios × 5 años × 12 meses × 8 tipos de delito)
- Columnas: departamento, municipio, ano, mes, tipo_delito, cantidad
- Se conecta con tabla de población de Clase 2 para calcular tasas

## DAX — Medidas y respuestas esperadas

### Medida 1: Total Delitos
```dax
Total Delitos = SUM(delitos[cantidad])
```
- **Resultado nacional:** ~varios millones (varía por filtro)
- **Trampa común:** Confundir SUM (agrega) con COUNT (cuenta filas)
- **Por qué SUM y no COUNT:** COUNT daría 14,399 (número de filas). SUM suma la columna cantidad.

### Medida 2: Tasa por 100K
```dax
Tasa por 100K = 
DIVIDE(
    [Total Delitos],
    SUM(poblacion[poblacion])
) * 100000
```
- **Trampa común:** Olvidar multiplicar por 100,000. La tasa sale como 0.004 → "no hay delitos"
- **Por qué DIVIDE y no /:** DIVIDE maneja división por cero (devuelve BLANK en vez de error)
- **Resultado esperado:** Buenaventura y Cali con las tasas más altas; Tunja y Floridablanca con las más bajas

### Medida 3: Variación Anual
```dax
Variacion Anual = 
VAR DelitosAnoActual = [Total Delitos]
VAR DelitosAnoAnterior = 
    CALCULATE(
        [Total Delitos],
        FILTER(
            ALL(delitos[ano]),
            delitos[ano] = MAX(delitos[ano]) - 1
        )
    )
RETURN
    DIVIDE(
        DelitosAnoActual - DelitosAnoAnterior,
        DelitosAnoAnterior
    )
```
- **Alternativa más simple (si tienen tabla de fechas):**
```dax
Variacion Anual = 
DIVIDE(
    [Total Delitos] - CALCULATE([Total Delitos], SAMEPERIODLASTYEAR(DimFecha[Date])),
    CALCULATE([Total Delitos], SAMEPERIODLASTYEAR(DimFecha[Date]))
)
```
- **Trampa común:** SAMEPERIODLASTYEAR requiere una tabla de fechas marcada. Si no la tienen, usar la primera versión con FILTER.

## Contexto de filtro — Explicación simplificada

### ¿Por qué existe CALCULATE?
- **Sin CALCULATE:** las medidas respetan los filtros actuales del visual (departamento seleccionado, año del slicer)
- **Con CALCULATE:** puedes cambiar o ignorar esos filtros
- **Ejemplo práctico:** "Quiero ver el total de delitos de TODA Colombia junto al total del departamento seleccionado"

```dax
Total Nacional = 
CALCULATE(
    [Total Delitos],
    ALL(delitos[departamento])
)
```

### Trampa común
- "CALCULATE cambia los datos" — NO, cambia el contexto de filtro
- "¿Por qué mi variación anual da vacío?" — porque no hay año anterior en el primer año del dataset

## Dashboard de 2 páginas

### Página 1 — Panorama Nacional
- **Mapa:** Burbujas por municipio, tamaño = tasa por 100K
- **KPIs:** Total delitos, Tasa promedio, Variación vs año anterior
- **Línea de tendencia:** Total delitos por mes (toda la serie temporal)
- **Slicer:** Año, tipo de delito

### Página 2 — Detalle por Delito
- **Barras:** Top 10 municipios por tipo de delito seleccionado
- **Tabla con drill-down:** Departamento → Municipio → Mes
- **Líneas:** Tendencia mensual por tipo de delito
- **Slicer:** Departamento

### Drill-down y drill-through
- **Drill-down:** Clic en departamento → ver sus municipios → ver meses
- **Drill-through:** Clic derecho en municipio → ir a página de detalle con contexto
- **Trampa común:** Confundir drill-down (profundizar en la misma página) con drill-through (navegar a otra página)

## Hallazgos clave del dataset

| Tipo de delito | Municipio más afectado | Tasa por 100K más alta |
|---------------|----------------------|----------------------|
| Hurto a personas | Bogotá (total), Buenaventura (tasa) | ~580 |
| Homicidio | Buenaventura, Quibdó | ~35-40 |
| Violencia intrafamiliar | Bogotá (total), varias capitales intermedias (tasa) | ~230 |
| Extorsión | Cali, Bogotá | ~20 |

**Dato para discusión:** "Bogotá tiene más delitos en total, pero Buenaventura tiene la tasa más alta. ¿Cuál es más peligrosa? Depende de la pregunta."
