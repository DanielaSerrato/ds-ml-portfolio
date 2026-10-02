# Clase 6 — Respuestas Docente

## Dataset: DANE_mercado_laboral_GEIH.csv
- 560 registros (28 departamentos × 5 años × 4 trimestres)
- Columnas: departamento, ano, trimestre, fecha, tasa_desempleo, tasa_ocupacion, tasa_informalidad

## Power Query — Limpieza esperada

### Pasos en Power Query
1. **Promover encabezados** (si no se detectan automáticamente)
2. **Renombrar columnas** a nombres más descriptivos si se desea:
   - tasa_desempleo → Tasa de Desempleo (%)
   - tasa_informalidad → Tasa de Informalidad (%)
3. **Cambiar tipos:**
   - fecha → tipo Fecha
   - tasa_desempleo, tasa_ocupacion, tasa_informalidad → Número decimal
   - ano → Número entero
4. **Eliminar errores** si los hubiera

### Trampa común
- No cerrar y aplicar los cambios en Power Query → cambios no se reflejan
- Confundir "Cargar" vs "Transformar datos" al importar

## Tabla DimFecha

### Cómo crear
Opción 1 — Tabla nueva con DAX:
```
DimFecha = 
ADDCOLUMNS(
    CALENDARAUTO(),
    "Año", YEAR([Date]),
    "Trimestre", "T" & FORMAT([Date], "Q"),
    "Mes", FORMAT([Date], "MMMM"),
    "NumMes", MONTH([Date])
)
```

Opción 2 — Más simple para esta clase:
- La tabla ya tiene columna "fecha" (2020-01-01, 2020-04-01, etc.)
- Crear columnas calculadas: Año = YEAR([fecha]), Trimestre = "T" & QUARTER([fecha])

### Por qué necesitamos DimFecha
- **Respuesta:** Para que Power BI entienda el eje temporal y pueda hacer comparaciones entre períodos
- **Trampa común:** "¿No alcanza con la columna ano?" — para esto sí, pero para análisis más avanzados (YoY, QoQ) necesitamos una tabla de fechas completa

## Primer visual — Desempleo por departamento

### Configuración
- Visual: Gráfico de barras horizontales agrupadas
- Eje Y: departamento
- Eje X: tasa_desempleo (promedio)
- Ordenar: de mayor a menor

### Hallazgos que deberían encontrar
1. **Quindío y Chocó** tienen las tasas más altas (~15-16%)
2. **Boyacá y Santander** tienen las más bajas (~7-8%)
3. **Pico COVID (2020-T2):** tasas subieron ~80% respecto a 2019-T4

### Slicer de año
- Al filtrar por 2020: el gráfico cambia drásticamente (todas las barras crecen)
- Al filtrar por 2024: se ve la recuperación
- **Punto docente:** "Miren cómo un solo clic cambia la historia. Eso es interactividad."

## Informalidad — Dato adicional valioso

### Hallazgo clave
- Chocó: 78.2% informalidad (la más alta)
- Bogotá: 38.5% (la más baja)
- **Correlación:** departamentos con alto desempleo NO necesariamente tienen alta informalidad. Algunos tienen bajo desempleo pero alta informalidad (empleo precario).
- **Punto docente:** "Un bajo desempleo no significa buen empleo. La informalidad cuenta la otra parte de la historia."

## Formato profesional

### Principios
1. **Título = hallazgo:** "Quindío lidera desempleo con 15.2% promedio 2020-2024"
2. **Colores:** máximo 3 colores con significado. Ej: rojo para alto desempleo, azul para bajo.
3. **Ejes:** siempre etiquetados con unidades (%)
4. **Menos es más:** quitar líneas de cuadrícula innecesarias, bordes, fondos decorativos

### Trampa común
- Poner TODOS los departamentos en un solo gráfico con colores diferentes → ilegible
- Mejor: top 10 en barras + tabla con el resto

## Entregable esperado
- .pbix con 1 página:
  - 2-3 KPI cards (tasa desempleo nacional, tasa ocupación, informalidad)
  - Barras horizontales: desempleo por departamento
  - Línea: tendencia trimestral de desempleo
  - Slicer: año y/o departamento
