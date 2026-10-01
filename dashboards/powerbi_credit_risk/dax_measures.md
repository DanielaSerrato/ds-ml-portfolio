# DAX Measures — Credit Risk Portfolio Monitor

Todas las medidas listas para copiar y pegar en Power BI.
Crear una tabla de medidas: **Modeling > New Table** → `_Medidas = {BLANK()}`
y luego agregar cada medida ahí.

---

## 1. Medidas Base

### Total Balance

```dax
Total Balance =
SUM( portfolio_monthly[balance] )
```

### Total Accounts

```dax
Total Accounts =
SUM( portfolio_monthly[accounts] )
```

### Total Balance KPI

```dax
Total Balance KPI =
SUM( kpi_summary[total_balance] )
```

---

## 2. Tasas de Morosidad

### NCL Rate (Net Credit Loss)

```dax
NCL Rate =
VAR _WriteOff =
    CALCULATE(
        SUM( portfolio_monthly[balance] ),
        portfolio_monthly[delinquency_band] = "Write-off"
    )
VAR _Total = [Total Balance]
RETURN
    DIVIDE( _WriteOff, _Total, 0 )
```

### Over 30 Rate

```dax
Over 30 Rate =
VAR _Over30 =
    CALCULATE(
        SUM( portfolio_monthly[balance] ),
        portfolio_monthly[delinquency_band] IN
            { "30-59", "60-89", "90-119", "120+", "Write-off" }
    )
VAR _Total = [Total Balance]
RETURN
    DIVIDE( _Over30, _Total, 0 )
```

### Over 90 Rate

```dax
Over 90 Rate =
VAR _Over90 =
    CALCULATE(
        SUM( portfolio_monthly[balance] ),
        portfolio_monthly[delinquency_band] IN
            { "90-119", "120+", "Write-off" }
    )
VAR _Total = [Total Balance]
RETURN
    DIVIDE( _Over90, _Total, 0 )
```

---

## 3. Crecimiento Mes a Mes

### MoM Balance Growth %

```dax
MoM Balance Growth % =
VAR _Current = [Total Balance]
VAR _Previous =
    CALCULATE(
        [Total Balance],
        DATEADD( DimFecha[Date], -1, MONTH )
    )
RETURN
    DIVIDE( _Current - _Previous, _Previous, 0 )
```

### MoM Accounts Growth %

```dax
MoM Accounts Growth % =
VAR _Current = [Total Accounts]
VAR _Previous =
    CALCULATE(
        [Total Accounts],
        DATEADD( DimFecha[Date], -1, MONTH )
    )
RETURN
    DIVIDE( _Current - _Previous, _Previous, 0 )
```

---

## 4. Roll Rates

### Roll Rate Forward (promedio de roll forward en el mes seleccionado)

```dax
Roll Rate Forward =
AVERAGEX(
    FILTER(
        roll_rates,
        roll_rates[to_band] > roll_rates[from_band]
    ),
    roll_rates[roll_rate]
)
```

### Roll Rate Cure (promedio de cura: se mueve a un band menor)

```dax
Roll Rate Cure =
AVERAGEX(
    FILTER(
        roll_rates,
        roll_rates[to_band] < roll_rates[from_band]
    ),
    roll_rates[roll_rate]
)
```

### Roll Rate Specific (para la matriz — usar con from_band y to_band en filas/columnas)

```dax
Roll Rate Value =
AVERAGE( roll_rates[roll_rate] )
```

---

## 5. Vintage Analysis

### Vintage Default Rate

```dax
Vintage Default Rate =
AVERAGE( vintage_curves[cumulative_default_rate] )
```

### Vintage Max Default Rate (tasa terminal por cohorte)

```dax
Vintage Max Default =
MAXX(
    vintage_curves,
    vintage_curves[cumulative_default_rate]
)
```

---

## 6. Weighted Avg Credit Limit

```dax
Weighted Avg Credit Limit =
DIVIDE(
    SUMX(
        kpi_summary,
        kpi_summary[avg_credit_limit] * kpi_summary[total_accounts]
    ),
    SUM( kpi_summary[total_accounts] ),
    0
)
```

---

## 7. YTD Metrics

### YTD NCL Rate

```dax
YTD NCL Rate =
CALCULATE(
    [NCL Rate],
    DATESYTD( DimFecha[Date] )
)
```

### YTD Over 30 Rate

```dax
YTD Over 30 Rate =
CALCULATE(
    [Over 30 Rate],
    DATESYTD( DimFecha[Date] )
)
```

---

## 8. Formato Condicional (Traffic Lights)

### NCL Traffic Light

```dax
NCL Traffic Light =
VAR _Rate = [NCL Rate]
RETURN
    SWITCH(
        TRUE(),
        _Rate <= 0.02, 1,   -- Verde: <= 2%
        _Rate <= 0.04, 2,   -- Amarillo: 2-4%
        3                    -- Rojo: > 4%
    )
```

### Over 30 Traffic Light

```dax
Over 30 Traffic Light =
VAR _Rate = [Over 30 Rate]
RETURN
    SWITCH(
        TRUE(),
        _Rate <= 0.10, 1,   -- Verde: <= 10%
        _Rate <= 0.18, 2,   -- Amarillo: 10-18%
        3                    -- Rojo: > 18%
    )
```

### Over 90 Traffic Light

```dax
Over 90 Traffic Light =
VAR _Rate = [Over 90 Rate]
RETURN
    SWITCH(
        TRUE(),
        _Rate <= 0.04, 1,   -- Verde: <= 4%
        _Rate <= 0.08, 2,   -- Amarillo: 4-8%
        3                    -- Rojo: > 8%
    )
```

### Roll Rate Heatmap Color

```dax
Roll Rate Color =
VAR _Val = [Roll Rate Value]
RETURN
    SWITCH(
        TRUE(),
        _Val >= 40, "#D32F2F",    -- Rojo fuerte
        _Val >= 20, "#FF9800",    -- Naranja
        _Val >= 10, "#FFC107",    -- Amarillo
        _Val >= 5,  "#8BC34A",    -- Verde claro
        "#4CAF50"                  -- Verde
    )
```

---

## 9. Approval Rate

```dax
Approval Rate =
AVERAGE( kpi_summary[approval_rate] )
```

---

## Notas

- **DimFecha** es la tabla de fechas que se crea en Power BI (ver README).
- Las medidas de traffic light devuelven 1/2/3 para usarse en formato condicional
  con reglas: 1=Verde, 2=Amarillo, 3=Rojo.
- Para la matriz de roll rates, usa `from_band` en filas, `to_band` en columnas,
  y `Roll Rate Value` como valor. Aplica formato condicional por color de fondo
  usando la medida `Roll Rate Color`.
