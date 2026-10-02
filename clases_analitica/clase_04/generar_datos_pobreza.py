"""
Genera dataset de pobreza monetaria por departamento
simulando datos del DANE para ejercicios de visualización.
"""
import csv
import random

random.seed(123)

departamentos_pobreza = {
    "Bogotá D.C.":      {"2019": 27.2, "2020": 35.8, "2021": 33.5, "2022": 30.2, "2023": 28.1, "2024": 26.5},
    "Antioquia":         {"2019": 33.1, "2020": 40.2, "2021": 37.8, "2022": 35.1, "2023": 33.4, "2024": 31.8},
    "Valle del Cauca":   {"2019": 30.8, "2020": 39.5, "2021": 36.2, "2022": 33.7, "2023": 31.5, "2024": 29.9},
    "Atlántico":         {"2019": 38.5, "2020": 46.1, "2021": 43.8, "2022": 41.2, "2023": 39.0, "2024": 37.4},
    "Santander":         {"2019": 28.4, "2020": 35.6, "2021": 33.1, "2022": 30.8, "2023": 29.2, "2024": 27.6},
    "Bolívar":           {"2019": 48.2, "2020": 55.8, "2021": 53.1, "2022": 50.4, "2023": 48.0, "2024": 46.1},
    "Cundinamarca":      {"2019": 25.6, "2020": 33.4, "2021": 30.8, "2022": 28.2, "2023": 26.5, "2024": 24.9},
    "Boyacá":            {"2019": 38.2, "2020": 44.1, "2021": 41.5, "2022": 39.0, "2023": 37.1, "2024": 35.5},
    "Nariño":            {"2019": 50.1, "2020": 57.3, "2021": 55.2, "2022": 52.8, "2023": 50.5, "2024": 48.7},
    "Córdoba":           {"2019": 53.8, "2020": 60.2, "2021": 58.1, "2022": 55.5, "2023": 53.2, "2024": 51.4},
    "Tolima":            {"2019": 36.5, "2020": 43.8, "2021": 41.2, "2022": 38.6, "2023": 36.4, "2024": 34.8},
    "Cauca":             {"2019": 54.6, "2020": 61.5, "2021": 59.2, "2022": 56.8, "2023": 54.5, "2024": 52.7},
    "Norte de Santander":{"2019": 43.1, "2020": 50.4, "2021": 48.2, "2022": 45.6, "2023": 43.3, "2024": 41.5},
    "Cesar":             {"2019": 49.5, "2020": 56.8, "2021": 54.1, "2022": 51.5, "2023": 49.2, "2024": 47.3},
    "Magdalena":         {"2019": 52.3, "2020": 59.1, "2021": 57.0, "2022": 54.2, "2023": 52.0, "2024": 50.1},
    "Huila":             {"2019": 42.8, "2020": 49.5, "2021": 47.1, "2022": 44.6, "2023": 42.3, "2024": 40.5},
    "La Guajira":        {"2019": 61.8, "2020": 67.4, "2021": 65.8, "2022": 63.5, "2023": 61.2, "2024": 59.5},
    "Risaralda":         {"2019": 28.1, "2020": 35.2, "2021": 32.8, "2022": 30.5, "2023": 28.8, "2024": 27.2},
    "Meta":              {"2019": 31.2, "2020": 38.5, "2021": 36.1, "2022": 33.8, "2023": 31.5, "2024": 29.8},
    "Caldas":            {"2019": 29.5, "2020": 36.8, "2021": 34.2, "2022": 31.8, "2023": 30.1, "2024": 28.5},
    "Sucre":             {"2019": 52.1, "2020": 58.4, "2021": 56.5, "2022": 54.0, "2023": 51.8, "2024": 50.0},
    "Quindío":           {"2019": 30.2, "2020": 37.5, "2021": 35.1, "2022": 32.8, "2023": 31.0, "2024": 29.4},
    "Chocó":             {"2019": 63.4, "2020": 68.2, "2021": 66.8, "2022": 64.5, "2023": 62.3, "2024": 60.8},
    "Caquetá":           {"2019": 44.2, "2020": 51.5, "2021": 49.1, "2022": 46.8, "2023": 44.5, "2024": 42.8},
}

# Pobreza extrema (roughly 40-50% of monetary poverty)
# Gini (0.45-0.55 range for Colombia)
rows = []
for depto, pobreza_by_year in departamentos_pobreza.items():
    for ano, pobreza in pobreza_by_year.items():
        pobreza_extrema = round(pobreza * random.uniform(0.38, 0.48), 1)
        gini = round(random.uniform(0.44, 0.56), 3)
        rows.append([depto, ano, pobreza, pobreza_extrema, gini])

output_path = r"C:\Users\Dani Serrato\Documents\DS_ML_Portfolio\clases_analitica\clase_04\DANE_pobreza_monetaria_departamento.csv"

with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(["departamento", "ano", "incidencia_pobreza", "incidencia_pobreza_extrema", "coeficiente_gini"])
    for row in rows:
        writer.writerow(row)

print(f"Archivo generado: {output_path}")
print(f"Total registros: {len(rows)}")
print(f"Departamentos: {len(departamentos_pobreza)}")

# Show extremes for teacher
print("\n--- Departamentos más pobres (2024) ---")
for depto, data in sorted(departamentos_pobreza.items(), key=lambda x: x[1]["2024"], reverse=True)[:5]:
    print(f"  {depto}: {data['2024']}%")

print("\n--- Departamentos menos pobres (2024) ---")
for depto, data in sorted(departamentos_pobreza.items(), key=lambda x: x[1]["2024"])[:5]:
    print(f"  {depto}: {data['2024']}%")
