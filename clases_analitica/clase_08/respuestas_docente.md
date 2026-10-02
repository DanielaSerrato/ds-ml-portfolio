# Clase 8 — Respuestas Docente

## Proyecto final — Dashboard integrador multi-fuente

### Datasets disponibles
| Dataset | Archivo | Clave de unión |
|---------|---------|----------------|
| Población | DANE_poblacion_departamentos_LIMPIO.csv | departamento, ano |
| Pobreza | DANE_pobreza_monetaria_departamento.csv | departamento, ano |
| Educación | MinEducacion_matriculas_desercion.csv | departamento, ano |
| Empleo | DANE_mercado_laboral_GEIH.csv | departamento, ano |
| Seguridad | PoliciaNacional_delitos_municipio.csv | departamento (agregar por depto), ano |

### Modelo estrella esperado
```
         dim_Departamento
              |
   ┌──────────┼──────────┐
   |          |          |
fact_Educacion  fact_Empleo  fact_Seguridad
   |          |          |
   └──────────┼──────────┘
              |
         dim_Fecha
              |
        fact_Pobreza
```

**dim_Departamento:** departamento (PK), capital, region, poblacion_2024
**dim_Fecha:** ano (PK), es_covid (2020-2021)
**Relaciones:** todas por departamento + ano

### Trampa común en el modelo
- Crear relaciones muchos-a-muchos → Power BI las permite pero dan resultados incorrectos
- Solución: agregar delitos por departamento/año antes de relacionar (o usar tabla puente)
- No relacionar TODAS las tablas entre sí → modelo estrella, no modelo espagueti

## Páginas sugeridas del dashboard

### Página 1 — Panorama Departamental
**Visuals:**
- Mapa de Colombia con KPI seleccionable (pobreza, desempleo, deserción)
- 4 tarjetas KPI: Pobreza promedio, Desempleo promedio, Deserción promedio, Tasa delitos
- Slicer de departamento y año

**DAX útil:**
```dax
Pobreza Promedio = AVERAGE(pobreza[incidencia_pobreza])
Cambio vs 2019 = 
VAR Actual = [Pobreza Promedio]
VAR Base = CALCULATE([Pobreza Promedio], FILTER(ALL(dim_Fecha), dim_Fecha[ano] = 2019))
RETURN Actual - Base
```

### Página 2 — Educación y Empleo
**Historia:** ¿Los departamentos con más deserción tienen más desempleo?
- Scatter: deserción (X) vs desempleo (Y), burbujas = población
- Línea dual: deserción y desempleo por año (mismo gráfico, dos ejes)
- Tabla: ranking de departamentos por deserción con indicador de desempleo

**Hallazgo esperado:** Correlación positiva moderada. Chocó y La Guajira en el cuadrante alto-alto.

### Página 3 — Seguridad y Pobreza
**Historia:** ¿Los departamentos más pobres son más inseguros?
- Scatter: pobreza (X) vs tasa de delitos por 100K (Y)
- Barras: top 5 departamentos por hurto y por homicidio
- Filtro: tipo de delito

**Hallazgo esperado:** Relación compleja. Algunos departamentos pobres tienen baja criminalidad registrada (posible sub-reporte). Ciudades grandes tienen alta tasa de hurto pero baja pobreza relativa.

**Punto docente:** "La correlación entre pobreza y criminalidad NO es tan simple como se piensa. Factores como urbanización, presencia institucional y reporte afectan los datos."

### Página 4 (opcional) — Evolución temporal
- Líneas: todos los indicadores normalizados (índice base 100 = 2019) por año
- Muestra cómo COVID afectó TODO simultáneamente
- Bookmarks: "Pre-COVID" vs "Post-COVID" vs "Recuperación"

## Rúbrica de evaluación sugerida

| Criterio | Peso | Excelente | Bueno | Por mejorar |
|----------|------|-----------|-------|-------------|
| Modelo de datos | 20% | Star schema correcto, relaciones limpias | Funcional con algunos errores | Relaciones incorrectas o faltantes |
| Visuales | 25% | Gráficos apropiados, bien formateados, interactivos | Funcionales pero con mejoras posibles | Gráficos incorrectos o sin formato |
| DAX | 20% | Medidas calculadas correctas, tasas normalizadas | Medidas básicas correctas | Solo usa drag & drop sin medidas |
| Narrativa | 20% | Historia clara con inicio-nudo-desenlace, recomendaciones | Hallazgos identificados sin narrativa clara | Solo describe lo que se ve |
| Presentación | 15% | Clara, convincente, dentro del tiempo | Completa pero sin impacto | Incompleta o desorganizada |

## Tips para la presentación de 5 minutos
1. **Minuto 1:** Contexto — qué datos usaste, para quién es este dashboard
2. **Minuto 2:** Hallazgo principal — la historia más importante
3. **Minuto 3:** Evidencia — mostrar los visuals que soportan el hallazgo
4. **Minuto 4:** Hallazgo secundario o dato sorprendente
5. **Minuto 5:** Recomendación — "Con base en estos datos, recomiendo..."

## Cierre del curso
**Mensaje clave:** "En 8 clases pasaron de abrir un CSV a construir un dashboard que integra 5 fuentes de datos del Estado. Esa es la habilidad: convertir datos en decisiones."
