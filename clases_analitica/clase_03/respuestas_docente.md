# Clase 3 — Respuestas Docente

## Dataset: MinSalud_vacunacion_COVID_departamento.csv
- 3,957 registros
- Columnas: departamento, grupo_etario, tipo_dosis, vacuna, dosis_aplicadas

## Respuestas esperadas

### Ejercicio 1 — Medidas básicas por departamento

**Top 5 departamentos por primera dosis (total):**
1. Bogotá D.C.: ~5,064,486
2. Antioquia: ~4,359,217
3. Valle del Cauca: ~2,981,321
4. Cundinamarca: ~1,891,957
5. Atlántico: ~1,562,299

- **Trampa común:** Bogotá siempre "gana" en totales porque tiene más población. No significa que vacunó mejor.
- **Por qué importa:** Introducir el concepto de TASA. Totales no son comparables sin normalizar por población.

**Para calcular correctamente:**
- Total dosis: =SUMAR.SI(rango_depto, "Bogotá D.C.", rango_dosis)
- Promedio por grupo: =PROMEDIO.SI(...)
- Mediana: requiere MEDIANA sobre rango filtrado (más complejo en Excel)

### Media vs Mediana — Ejemplo clave

Salarios mensuales de un equipo: $1.2M, $1.5M, $1.8M, $2.0M, $2.2M, $2.5M, $15.0M (el director)
- **Media:** $3.74M (distorsionada por el outlier)
- **Mediana:** $2.0M (refleja mejor la realidad del grupo)
- **Respuesta esperada:** "La mediana es mejor cuando hay valores extremos"
- **Trampa común:** "El promedio es siempre la mejor medida" — NO, depende de la distribución

### Ejercicio 2 — Tabla resumen con funciones condicionales

**Funciones a usar:**
```
=SUMAR.SI($A:$A, "Antioquia", $E:$E)
=CONTAR.SI($A:$A, "Antioquia")
=PROMEDIO.SI($A:$A, "Antioquia", $E:$E)
```

**Trampa común:**
- Olvidar anclar rangos con $ → al copiar la fórmula se desplaza
- Confundir SUMAR.SI (suma valores) con CONTAR.SI (cuenta ocurrencias)

### Tasas por 1,000 habitantes

**Fórmula:** (Total dosis primera / Población) × 1,000

**Resultados interesantes cuando se normaliza:**
- Bogotá baja de #1 en total a nivel medio en tasa
- Departamentos pequeños con buena cobertura suben (ej: San Andrés, Quindío)
- Chocó, Vaupés, Guainía tienen las tasas más bajas → brecha rural/urbana

**Por qué importa:** "Si solo reportamos totales, parecemos eficientes en las ciudades grandes. La tasa muestra dónde realmente falta cobertura."

### Tablas dinámicas

**Configuración sugerida:**
- Filas: departamento
- Columnas: tipo_dosis
- Valores: SUMA de dosis_aplicadas

**Lo que deben observar:**
- Caída drástica entre primera dosis → segunda dosis → refuerzo
- Algunos departamentos tienen casi igual primera y segunda (buena adherencia)
- El refuerzo es mucho menor en todos → fatiga de vacunación

### Interpretación esperada (ejemplo)

> "Bogotá D.C. aplicó la mayor cantidad de primeras dosis en total (~5M), pero al normalizar por población, su tasa de cobertura (~641 por 1,000 hab.) es similar a la de otros departamentos urbanos. Los departamentos con menor cobertura relativa son Guainía, Vaupés y Chocó, todos con alta ruralidad y difícil acceso geográfico. Esto sugiere que la estrategia de vacunación fue más efectiva en zonas urbanas."

### Punto de cierre
- "Los números sin contexto engañan. El promedio sin la mediana engaña. El total sin la tasa engaña."
- Preguntar: "¿En su trabajo, reportan totales o tasas? ¿Qué cambia si usan tasas?"
