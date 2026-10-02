# Clase 5 — Respuestas Docente

## Dataset: MinEducacion_matriculas_desercion.csv
- 744 registros (31 departamentos × 6 años × 4 niveles)
- Columnas: departamento, ano, nivel_educativo, matriculados, desertores, tasa_desercion, cobertura_neta

## Preguntas y respuestas esperadas

### P1: ¿Dónde es mayor la deserción?
**Respuesta:** Chocó, Vaupés, Vichada, La Guajira, Amazonas — todos departamentos rurales/periféricos
- Tasa deserción Básica Secundaria en Chocó: ~6.7% vs Bogotá: ~2.7%
- **Por qué importa:** La brecha rural-urbana es el hallazgo más fuerte del dataset

### P2: ¿Ha mejorado la cobertura desde 2019?
**Respuesta:** Caída fuerte en 2020 (COVID), recuperación gradual 2021-2024. Media no ha vuelto completamente a niveles 2019.
- **Dato clave:** En 2020, la matrícula cayó ~8% a nivel nacional
- **Trampa común:** "Mejoró desde 2021" — sí, pero comparar contra 2019, no contra 2020

### P3: ¿Qué nivel educativo pierde más estudiantes?
**Respuesta:** Básica Secundaria (tasa ~4.5% promedio nacional) seguida de Media (~3.8%)
- Preescolar y Primaria tienen tasas menores (~3% y ~2.8%)
- **Interpretación:** La transición de primaria a secundaria es donde más se pierde
- **Por qué importa:** Focalizar intervenciones en grado 6° (entrada a secundaria)

### P4: ¿Cómo afectó el COVID la matrícula?
**Respuesta:**
- 2020: caída del 8% en matrículas, aumento del 40% en tasa de deserción
- 2021: recuperación parcial, deserción aún 25% arriba de 2019
- 2022: casi normalizado
- **Hallazgo:** El efecto COVID fue más fuerte en Básica Secundaria y Media

### P5: ¿Hay relación entre pobreza y deserción?
**Cruce con datos de Clase 4:**
- Departamentos con alta pobreza (Chocó 60.8%, La Guajira 59.5%) tienen alta deserción
- Departamentos con baja pobreza (Cundinamarca 24.9%, Bogotá 26.5%) tienen baja deserción
- Correlación positiva clara, pero: **correlación ≠ causalidad**
- **Trampa común:** "La pobreza causa deserción" — puede ser, pero también la deserción causa pobreza (ciclo). Y hay terceras variables (acceso geográfico, conflicto armado, migración).

## Introducción a Power BI — Puntos clave

### Por qué moverse de Excel a Power BI
| Aspecto | Excel | Power BI |
|---------|-------|----------|
| Filas | ~1M máximo | Millones |
| Actualización | Manual | Automática (scheduled refresh) |
| Compartir | Enviar archivo | Publicar link/app |
| Interactividad | Limitada | Filtros cruzados en tiempo real |
| Relaciones | Difícil (BUSCARV) | Modelo de datos nativo |

### Primer ejercicio en Power BI
1. Abrir Power BI Desktop
2. Obtener datos → Desde archivo → CSV
3. Seleccionar MinEducacion_matriculas_desercion.csv
4. Verificar tipos en preview → Cargar
5. En el panel de visualizaciones → clic en "Gráfico de barras agrupadas"
6. Arrastrar departamento al Eje, matriculados a Valores
7. "¡Eso es todo!" — primer visual interactivo

**Trampa común:** Intentar "hacer todo" en el primer intento. Clase 6 profundiza. Aquí solo necesitan el "wow moment" de ver los datos interactivos.

## Entregable esperado
Documento con:
1. 5 preguntas formuladas
2. 3-5 gráficos/tablas que responden las preguntas
3. 1 hallazgo del cruce pobreza + educación
4. 1 recomendación de política pública basada en los hallazgos
