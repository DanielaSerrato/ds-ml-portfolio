# Clase 4 — Respuestas Docente

## Dataset: DANE_pobreza_monetaria_departamento.csv
- 144 registros (24 departamentos × 6 años)
- Columnas: departamento, ano, incidencia_pobreza, incidencia_pobreza_extrema, coeficiente_gini

## Hallazgos clave que los estudiantes deberían encontrar

### Departamentos más pobres (2024)
1. Chocó: 60.8%
2. La Guajira: 59.5%
3. Cauca: 52.7%
4. Córdoba: 51.4%
5. Magdalena: 50.1%

### Departamentos menos pobres (2024)
1. Cundinamarca: 24.9%
2. Bogotá D.C.: 26.5%
3. Risaralda: 27.2%
4. Santander: 27.6%
5. Caldas: 28.5%

### Impacto COVID (2019 → 2020)
- Todos los departamentos suben entre 6-8 puntos porcentuales
- Respuesta esperada: "El COVID aumentó la pobreza en todo el país, pero el impacto fue relativamente uniforme en términos de puntos porcentuales"
- **Trampa común:** Pensar que el impacto fue mayor en los más pobres. En puntos porcentuales fue similar; en porcentaje de cambio también.

### Gráfico de barras — Pobreza por departamento (2024)
- **Título correcto:** "Chocó y La Guajira lideran pobreza con más del 59%" (hallazgo)
- **Título incorrecto:** "Gráfico de pobreza por departamento" (descripción)
- **Por qué importa:** Título como hallazgo → el lector entiende el mensaje sin leer el gráfico

### Gráfico de líneas — Tendencia temporal
- Patrón claro: subida en 2020, descenso gradual 2021-2024
- Ningún departamento ha vuelto al nivel pre-COVID (2019) exacto
- **Título sugerido:** "La pobreza aún no regresa a niveles pre-pandemia en ningún departamento"

### Errores clásicos de visualización

| Error | Por qué es malo | Cómo se arregla |
|-------|-----------------|-----------------|
| Pie chart con 24 departamentos | Imposible leer, todas las tajadas se ven iguales | Usar barras horizontales ordenadas |
| Gráfico 3D | Distorsiona proporciones, los departamentos del "fondo" se ven más pequeños | Usar 2D siempre |
| Eje Y cortado (empieza en 40%) | Exagera diferencias entre departamentos | Empezar en 0% (en este caso) |
| Colores aleatorios | No comunican nada | Usar gradiente: verde (baja pobreza) → rojo (alta pobreza) |
| Sin título | No se sabe qué mirar | Título = hallazgo principal |

### Cuándo NO empezar en cero
- Respuesta: cuando la variación es lo importante y el rango es estrecho
- Ejemplo: si todos los departamentos están entre 25% y 65%, empezar en 0% desperdicia la mitad del gráfico en espacio vacío
- **Regla práctica:** ¿El gráfico comunica mejor empezando en 0? Sí → empezar en 0. ¿Aplasta las diferencias importantes? → Considerar un corte, pero SIEMPRE indicarlo visualmente

### Entregable esperado

3 gráficos con estas características:
1. **Barras horizontales:** Pobreza por departamento 2024, ordenado de mayor a menor. Título-hallazgo.
2. **Líneas:** Tendencia 2019-2024 de top 5 departamentos más pobres. Título-hallazgo.
3. **Scatter o barras pareadas:** Pobreza vs pobreza extrema o Pobreza vs Gini. Título-hallazgo.

Cada uno con una oración de interpretación. Ejemplo:
> "Entre 2019 y 2024, la pobreza en Chocó pasó de 63.4% a 60.8%, una reducción de solo 2.6 puntos en 5 años, la más lenta del país."
