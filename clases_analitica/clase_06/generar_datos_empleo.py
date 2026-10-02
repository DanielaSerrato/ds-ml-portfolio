"""
Genera dataset de mercado laboral (GEIH) por departamento y trimestre
simulando datos del DANE para Power BI.
"""
import csv
import random

random.seed(99)

departamentos = [
    "Amazonas", "Antioquia", "Arauca", "Atlántico", "Bogotá D.C.",
    "Bolívar", "Boyacá", "Caldas", "Caquetá", "Casanare",
    "Cauca", "Cesar", "Chocó", "Córdoba", "Cundinamarca",
    "Huila", "La Guajira", "Magdalena", "Meta", "Nariño",
    "Norte de Santander", "Putumayo", "Quindío", "Risaralda",
    "Santander", "Sucre", "Tolima", "Valle del Cauca"
]

trimestres = ["I", "II", "III", "IV"]
anos = [2020, 2021, 2022, 2023, 2024]

# Base unemployment rates
desempleo_base = {
    "Bogotá D.C.": 11.2, "Antioquia": 10.8, "Valle del Cauca": 12.5,
    "Atlántico": 9.8, "Santander": 8.5, "Bolívar": 8.2,
    "Cundinamarca": 9.1, "Boyacá": 7.8, "Nariño": 9.5,
    "Córdoba": 11.5, "Tolima": 12.1, "Cauca": 13.2,
    "Norte de Santander": 14.5, "Cesar": 10.2, "Magdalena": 9.8,
    "Huila": 11.8, "La Guajira": 12.8, "Risaralda": 10.5,
    "Meta": 11.2, "Caldas": 10.8, "Sucre": 9.5,
    "Quindío": 15.2, "Chocó": 16.5, "Caquetá": 11.5,
    "Casanare": 9.8, "Arauca": 13.5, "Putumayo": 12.2,
    "Amazonas": 10.5,
}

# Informality rates
informalidad_base = {
    "Bogotá D.C.": 38.5, "Antioquia": 42.1, "Valle del Cauca": 44.8,
    "Atlántico": 55.2, "Santander": 48.5, "Bolívar": 58.1,
    "Cundinamarca": 45.2, "Boyacá": 62.5, "Nariño": 68.2,
    "Córdoba": 65.8, "Tolima": 58.5, "Cauca": 70.1,
    "Norte de Santander": 62.8, "Cesar": 60.5, "Magdalena": 63.2,
    "Huila": 57.8, "La Guajira": 72.5, "Risaralda": 44.2,
    "Meta": 52.1, "Caldas": 46.8, "Sucre": 66.5,
    "Quindío": 50.8, "Chocó": 78.2, "Caquetá": 64.5,
    "Casanare": 55.2, "Arauca": 60.1, "Putumayo": 63.8,
    "Amazonas": 58.5,
}

rows = []
for depto in departamentos:
    base_d = desempleo_base[depto]
    base_i = informalidad_base[depto]

    for ano in anos:
        for i, trim in enumerate(trimestres):
            # COVID effect
            if ano == 2020:
                if trim == "I":
                    covid_factor = 1.1
                elif trim == "II":
                    covid_factor = 1.8  # Peak COVID
                elif trim == "III":
                    covid_factor = 1.5
                else:
                    covid_factor = 1.3
            elif ano == 2021:
                covid_factor = 1.15 - (i * 0.03)
            elif ano == 2022:
                covid_factor = 1.0
            else:
                covid_factor = max(0.92, 1.0 - (ano - 2022) * 0.02)

            # Seasonal variation
            seasonal = [1.02, 0.98, 0.96, 1.04][i]

            tasa_desempleo = round(base_d * covid_factor * seasonal * random.uniform(0.95, 1.05), 1)
            tasa_ocupacion = round(100 - tasa_desempleo - random.uniform(35, 45), 1)
            tasa_informalidad = round(base_i * (1 + (covid_factor - 1) * 0.3) * random.uniform(0.96, 1.04), 1)

            fecha = f"{ano}-{str((i*3)+1).zfill(2)}-01"

            rows.append([depto, ano, trim, fecha, tasa_desempleo, tasa_ocupacion, tasa_informalidad])

output_path = r"C:\Users\Dani Serrato\Documents\DS_ML_Portfolio\clases_analitica\clase_06\DANE_mercado_laboral_GEIH.csv"

with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(["departamento", "ano", "trimestre", "fecha", "tasa_desempleo",
                      "tasa_ocupacion", "tasa_informalidad"])
    for row in rows:
        writer.writerow(row)

print(f"Archivo generado: {output_path}")
print(f"Total registros: {len(rows)}")
