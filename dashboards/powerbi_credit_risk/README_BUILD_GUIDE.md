# Credit Risk Portfolio Monitor — Guia de Construccion en Power BI

Dashboard de monitoreo de riesgo crediticio para portafolio de tarjetas/credito.
**Autora:** Daniela Serrato

---

## Paso 0: Generar los datos

Abrir terminal en esta carpeta y ejecutar:

```bash
python generate_data.py
```

Esto genera 4 archivos CSV:
- `portfolio_monthly.csv` — saldos y cuentas por banda de morosidad
- `vintage_curves.csv` — curvas de default por cohorte
- `roll_rates.csv` — tasas de transicion entre bandas
- `kpi_summary.csv` — KPIs agregados mensuales

---

## Paso 1: Importar datos en Power BI

1. Abrir **Power BI Desktop** > **Get Data** > **Text/CSV**
2. Importar cada CSV:
   - `portfolio_monthly.csv`
   - `vintage_curves.csv`
   - `roll_rates.csv`
   - `kpi_summary.csv`
3. En **Power Query Editor**, verificar tipos de datos:
   - `month`, `origination_month`: tipo **Text** (se usara la tabla de fechas)
   - `balance`, `roll_rate`, `cumulative_default_rate`: tipo **Decimal Number**
   - `accounts`, `total_accounts`, `months_on_books`: tipo **Whole Number**
4. Click **Close & Apply**

---

## Paso 2: Crear tabla de fechas (DimFecha)

En **Modeling** > **New Table**, pegar:

```dax
DimFecha =
VAR _MinDate = DATE(2024, 10, 1)
VAR _MaxDate = DATE(2026, 9, 30)
RETURN
ADDCOLUMNS(
    CALENDAR( _MinDate, _MaxDate ),
    "Year", YEAR([Date]),
    "Month", MONTH([Date]),
    "MonthName", FORMAT([Date], "MMM YYYY"),
    "YearMonth", FORMAT([Date], "YYYY-MM"),
    "Quarter", "Q" & FORMAT([Date], "Q YYYY")
)
```

Marcar como **tabla de fechas**: click derecho en `DimFecha` > **Mark as Date Table** > columna `Date`.

---

## Paso 3: Crear relaciones (Star Schema)

Ir a **Model View** y crear estas relaciones:

| Desde | Hacia | Columnas | Cardinalidad |
|-------|-------|----------|--------------|
| `DimFecha[YearMonth]` | `portfolio_monthly[month]` | 1:N |
| `DimFecha[YearMonth]` | `roll_rates[month]` | 1:N |
| `DimFecha[YearMonth]` | `kpi_summary[month]` | 1:N |
| `DimFecha[YearMonth]` | `vintage_curves[origination_month]` | 1:N |

Si Power BI no acepta la relacion directa (tipos distintos), asegurarse de que ambas columnas sean tipo **Text**.

**Tip:** En Model View, organizar las tablas en estrella con `DimFecha` al centro.

---

## Paso 4: Crear tabla de medidas

**Modeling** > **New Table**:

```dax
_Medidas = {BLANK()}
```

Ocultar esta tabla de los reportes (click derecho > **Hide in Report View**).

Luego, seleccionando la tabla `_Medidas`, ir a **New Measure** y agregar cada medida del archivo `dax_measures.md`.

---

## Paso 5: Construir las paginas

### Configuracion general del reporte

- **Tema sugerido:** usar un tema oscuro tipo "Executive" o crear uno custom con:
  - Fondo: `#1A1A2E` o `#0F0F23`
  - Texto: `#E0E0E0`
  - Acentos: `#00D4AA` (verde), `#FF6B6B` (rojo), `#4ECDC4` (teal)
- **Fuente:** Segoe UI o DIN
- **Tamano de pagina:** 16:9 (1280x720)

---

### Pagina 1 — Executive Summary

**Layout:**

```
+----------------------------------------------------+
|  [KPI Card]   [KPI Card]   [KPI Card]  [KPI Card]  |
|  Tot Balance   NCL Rate    Over 30     Over 90      |
+----------------------------------------------------+
|                                                      |
|   [Line Chart — Monthly Balance Trend]               |
|                                                      |
+---------------------------+--------------------------+
|  [Line Chart]             |  [Line Chart]            |
|  NCL Rate trend           |  Approval Rate trend     |
+---------------------------+--------------------------+
```

**Instrucciones detalladas:**

1. **4 KPI Cards** (fila superior):
   - Arrastra un visual **Card** para cada metrica
   - Card 1: `Total Balance KPI` — formato moneda MXN
   - Card 2: `NCL Rate` — formato porcentaje, 2 decimales
   - Card 3: `Over 30 Rate` — formato porcentaje
   - Card 4: `Over 90 Rate` — formato porcentaje
   - Agregar formato condicional usando las medidas Traffic Light

2. **Line Chart grande** (centro):
   - Eje X: `DimFecha[MonthName]`
   - Valores: `Total Balance`
   - Agregar linea secundaria: `Total Accounts`

3. **Line Chart NCL** (inferior izq):
   - Eje X: `DimFecha[MonthName]`
   - Valor: `NCL Rate`
   - Agregar una constant line al 3% como threshold

4. **Line Chart Approval** (inferior der):
   - Eje X: `DimFecha[MonthName]`
   - Valor: `Approval Rate`

**Slicer:** Agregar un slicer con `DimFecha[YearMonth]` como filtro de rango de fechas.

---

### Pagina 2 — Delinquency Analysis

**Layout:**

```
+----------------------------------------------------+
|  [Stacked Bar Chart]                                 |
|  Balance por Banda de Morosidad (mensual)            |
+----------------------------------------------------+
|                                                      |
|  [Matrix — Roll Rate Transition]                     |
|  from_band (rows) x to_band (cols)                   |
|  Valor: Roll Rate Value                              |
+----------------------------------------------------+
```

**Instrucciones:**

1. **100% Stacked Bar Chart**:
   - Eje X: `DimFecha[MonthName]`
   - Eje Y: `Total Balance`
   - Leyenda: `portfolio_monthly[delinquency_band]`
   - Ordenar las bandas: Current, 1-29, 30-59, 60-89, 90-119, 120+, Write-off
   - Colores sugeridos:
     - Current: `#4CAF50` (verde)
     - 1-29: `#8BC34A`
     - 30-59: `#FFC107` (amarillo)
     - 60-89: `#FF9800` (naranja)
     - 90-119: `#FF5722`
     - 120+: `#D32F2F` (rojo)
     - Write-off: `#880E4F` (rojo oscuro)

2. **Matrix visual** (tabla de roll rates):
   - Filas: `roll_rates[from_band]`
   - Columnas: `roll_rates[to_band]`
   - Valores: `Roll Rate Value`
   - Formato: porcentaje con 1 decimal
   - **Formato condicional**: Background color > Based on field value
     - Usar escala de color: verde (bajo) a rojo (alto)
   - Diagonal (mismo band) deberia verse neutra

**Slicer:** `DimFecha[MonthName]` para ver un mes especifico en la matriz.

---

### Pagina 3 — Vintage Analysis

**Layout:**

```
+----------------------------------------------------+
|  [Line Chart — Vintage Curves]                       |
|  Cada cohorte es una linea                           |
|  X = months_on_books                                 |
|  Y = cumulative_default_rate                         |
+----------------------------------------------------+
|  [Heatmap / Matrix]                                  |
|  origination_month (rows) x months_on_books (cols)   |
|  Value: cumulative_default_rate                      |
+----------------------------------------------------+
```

**Instrucciones:**

1. **Line Chart multi-linea**:
   - Eje X: `vintage_curves[months_on_books]`
   - Eje Y: `Vintage Default Rate` (o directo `cumulative_default_rate`)
   - Leyenda: `vintage_curves[origination_month]`
   - Se veran las curvas S de cada cohorte
   - Las cohortes de mediados de 2025 deberian estar mas arriba (efecto estres)

2. **Matrix / Heatmap**:
   - Filas: `vintage_curves[origination_month]`
   - Columnas: `vintage_curves[months_on_books]`
   - Valores: promedio de `cumulative_default_rate`
   - **Formato condicional**: escala de color
     - Bajo (0-2%): verde
     - Medio (2-5%): amarillo
     - Alto (5%+): rojo

---

### Pagina 4 — Partner Comparison

**Layout:**

```
+--------------------------+--------------------------+
|  [Bar Chart]             |  [Bar Chart]             |
|  Balance por Partner     |  NCL Rate por Partner    |
+--------------------------+--------------------------+
|  [Clustered Column]                                  |
|  Over 30 vs Over 90 por Partner                      |
+----------------------------------------------------+
|  [Table]                                             |
|  Detalle por partner: cuentas, balance, NCL, etc.   |
+----------------------------------------------------+
```

**Instrucciones:**

1. **Bar Chart — Balance**:
   - Eje Y: `portfolio_monthly[partner]`
   - Valor: `Total Balance`
   - Ordenar descendente por balance

2. **Bar Chart — NCL**:
   - Eje Y: `portfolio_monthly[partner]`
   - Valor: `NCL Rate`
   - Formato condicional: verde < 2%, amarillo < 4%, rojo > 4%

3. **Clustered Column Chart**:
   - Eje X: `portfolio_monthly[partner]`
   - Valores: `Over 30 Rate` y `Over 90 Rate`
   - Permite comparar ambas metricas lado a lado

4. **Table visual**:
   - Columnas: Partner, Total Accounts, Total Balance, NCL Rate, Over 30 Rate, Over 90 Rate
   - Agregar data bars en la columna de Balance
   - Formato condicional en las columnas de tasas

**Slicer:** `DimFecha[YearMonth]` para ver un periodo especifico.

---

## Paso 6: Toques finales

1. **Bookmarks:** Crear bookmarks para vistas predeterminadas (ej. ultimo mes, periodo de estres)
2. **Tooltips:** En los line charts, agregar tooltips personalizados mostrando MoM Growth %
3. **Titulos:** Cada visual debe tener un titulo descriptivo
4. **Navegacion:** Agregar botones de navegacion entre paginas (Insert > Buttons > Navigator)
5. **Filtros de pagina:** Configurar filtros que apliquen a toda la pagina donde sea necesario
6. **Mobile layout:** Opcionalmente, crear layout mobile para cada pagina

---

## Esquema de relaciones (referencia visual)

```
                    +------------+
                    |  DimFecha  |
                    | YearMonth  |
                    +-----+------+
                          |
           +--------------+--------------+-------------+
           |              |              |             |
     +-----v------+ +----v-----+ +------v----+ +-----v----------+
     | portfolio   | | roll     | | kpi       | | vintage        |
     | _monthly    | | _rates   | | _summary  | | _curves        |
     | month       | | month    | | month     | | origination    |
     | partner     | | from_band| |           | |   _month       |
     | delinq_band | | to_band  | |           | | months_on_books|
     | accounts    | | roll_rate| |           | | cum_default    |
     | balance     | |          | |           | |   _rate        |
     +-------------+ +----------+ +-----------+ +----------------+
```

---

## Recursos adicionales

- **Datos:** Generados con `generate_data.py` (seed=42 para reproducibilidad)
- **Periodo:** Oct 2024 — Sep 2026 (24 meses)
- **Partners:** 8 socios con distintos perfiles de riesgo
- **Evento de estres:** ~Jun-Ago 2025 (simula crisis tipo COVID)
- **Moneda:** MXN (pesos mexicanos)
