# Clase 2 — Respuestas Docente

## Dataset: DANE_poblacion_departamentos_SUCIO.csv

### Problemas intencionados en el archivo

| # | Problema | Dónde | Cómo se arregla |
|---|----------|-------|-----------------|
| 1 | Encabezados múltiples (3 filas de título DANE) | Filas 1-3 | Eliminar filas superiores, dejar solo la fila de encabezados |
| 2 | Fila vacía entre encabezados y datos | Fila 4 | Eliminar |
| 3 | Nombres inconsistentes de departamento | ATLANTICO, CAQUETA, LA GUAJIRA, "Cundinamarca " (espacio), "Nte. de Santander" | PROPER() para capitalizar, SUSTITUIR() para abreviaturas, ESPACIOS() para limpiar |
| 4 | Capital faltante | Guaviare — capital vacía | Completar manualmente ("San José del Guaviare") o investigar |
| 5 | Valores numéricos faltantes | Cesar 2024 vacío, San Andrés 2025-2026 vacíos | Investigar fuente o marcar como "Sin dato" |
| 6 | Números con formato inconsistente | Antioquia: "6.977.984" (puntos), Valle: "4 832 005" (espacios) | Buscar y reemplazar "." → "", " " → "", luego convertir a número |
| 7 | Texto en celdas numéricas | Nariño: "1886097*", Sucre: "929591 (p)" | SUSTITUIR para quitar asteriscos y "(p)", luego convertir |
| 8 | Filas vacías intermedias | Después de Cauca y Meta | Seleccionar → Ir a especial → Celdas vacías → Eliminar filas |
| 9 | Notas al pie del archivo | Últimas 4 filas | Eliminar |
| 10 | Delimitador punto y coma | Todo el archivo | Importar con delimitador correcto |

### Proceso de limpieza paso a paso
1. **Importar correctamente:** Datos → Desde CSV → delimitador ";" → UTF-8
2. **Eliminar filas de encabezado DANE** (filas 1-4)
3. **Eliminar filas vacías** intermedias y al final
4. **Eliminar notas al pie** (últimas 4 filas)
5. **Normalizar nombres:** PROPER() + SUSTITUIR("Nte. de Santander", "Norte de Santander") + ESPACIOS()
6. **Limpiar números:** Buscar → Reemplazar "." por nada, " " por nada, "*" por nada, " (p)" por nada
7. **Convertir a tabla plana:** Seleccionar todo → Insertar → Tabla
8. **Verificar tipos:** Números como números, texto como texto

### Trampa común
- Estudiantes intentan limpiar SIN hacer una copia primero → siempre trabajar en copia
- Confundir formato de número (puntos como separador de miles) con decimales
- No verificar que después de limpiar tengan 32 departamentos exactos

### Archivo limpio esperado
- **DANE_poblacion_departamentos_LIMPIO.csv**: 160 filas (32 deptos × 5 años) en formato largo
- Columnas: departamento, capital, ano, poblacion
- Todos los nombres estandarizados
- Todos los números como enteros

### Puntos de discusión
- "¿Cuánto tiempo les tomó limpiar?" → Mostrar que en datos reales, 60-80% del tiempo es limpieza
- "¿Qué errores son más peligrosos?" → Los numéricos que parecen correctos pero no lo son (ej: Antioquia con puntos)
- "¿Cómo automatizan esto si les llega cada mes?" → Adelanto de Power Query (Clase 6)
