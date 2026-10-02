"""
Genera dataset de vacunación COVID-19 por departamento
simulando datos de MinSalud para ejercicios de estadística descriptiva.
"""
import csv
import random

random.seed(42)

departamentos = [
    "Amazonas", "Antioquia", "Arauca", "Atlántico", "Bolívar",
    "Boyacá", "Caldas", "Caquetá", "Casanare", "Cauca",
    "Cesar", "Chocó", "Córdoba", "Cundinamarca", "Guainía",
    "Guaviare", "Huila", "La Guajira", "Magdalena", "Meta",
    "Nariño", "Norte de Santander", "Putumayo", "Quindío",
    "Risaralda", "San Andrés", "Santander", "Sucre", "Tolima",
    "Valle del Cauca", "Vaupés", "Vichada", "Bogotá D.C."
]

poblaciones = {
    "Amazonas": 80845, "Antioquia": 7044013, "Arauca": 286733,
    "Atlántico": 2722128, "Bolívar": 2236073, "Boyacá": 1269581,
    "Caldas": 1007896, "Caquetá": 518476, "Casanare": 448813,
    "Cauca": 1506202, "Cesar": 1264612, "Chocó": 553294,
    "Córdoba": 1909071, "Cundinamarca": 3242999, "Guainía": 52466,
    "Guaviare": 89601, "Huila": 1226096, "La Guajira": 1103729,
    "Magdalena": 1424937, "Meta": 1089466, "Nariño": 1886097,
    "Norte de Santander": 1516381, "Putumayo": 379441,
    "Quindío": 583935, "Risaralda": 1003466, "San Andrés": 84208,
    "Santander": 2236327, "Sucre": 937393, "Tolima": 1415107,
    "Valle del Cauca": 4873548, "Vaupés": 47919, "Vichada": 118341,
    "Bogotá D.C.": 7901653
}

vacunas = ["Pfizer", "Sinovac", "AstraZeneca", "Janssen", "Moderna"]
grupos_etarios = ["12-17", "18-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"]
dosis_tipos = ["Primera dosis", "Segunda dosis", "Refuerzo"]

# Coverage rates vary by department (urban = higher coverage)
cobertura_base = {
    "Bogotá D.C.": 0.82, "Antioquia": 0.78, "Valle del Cauca": 0.76,
    "Atlántico": 0.74, "Santander": 0.75, "Cundinamarca": 0.73,
    "Bolívar": 0.68, "Risaralda": 0.72, "Quindío": 0.71,
    "Caldas": 0.70, "Boyacá": 0.69, "Meta": 0.67,
    "Tolima": 0.66, "Huila": 0.65, "Norte de Santander": 0.64,
    "Cesar": 0.62, "Magdalena": 0.60, "Nariño": 0.58,
    "Córdoba": 0.56, "Cauca": 0.55, "Sucre": 0.57,
    "La Guajira": 0.48, "Caquetá": 0.52, "Casanare": 0.63,
    "Arauca": 0.54, "Putumayo": 0.50, "Chocó": 0.42,
    "San Andrés": 0.70, "Amazonas": 0.45, "Guaviare": 0.47,
    "Guainía": 0.38, "Vaupés": 0.35, "Vichada": 0.40,
}

rows = []

for depto in departamentos:
    pob = poblaciones[depto]
    cob = cobertura_base[depto]

    for grupo in grupos_etarios:
        # Proportion of population by age group
        if grupo == "80+":
            pob_grupo = int(pob * 0.03)
        elif grupo == "70-79":
            pob_grupo = int(pob * 0.04)
        elif grupo == "60-69":
            pob_grupo = int(pob * 0.07)
        elif grupo == "50-59":
            pob_grupo = int(pob * 0.10)
        elif grupo == "40-49":
            pob_grupo = int(pob * 0.13)
        elif grupo == "30-39":
            pob_grupo = int(pob * 0.16)
        elif grupo == "18-29":
            pob_grupo = int(pob * 0.20)
        else:  # 12-17
            pob_grupo = int(pob * 0.10)

        # Older groups had higher coverage
        age_factor = {"80+": 1.15, "70-79": 1.12, "60-69": 1.10,
                      "50-59": 1.05, "40-49": 1.0, "30-39": 0.95,
                      "18-29": 0.85, "12-17": 0.70}

        grupo_cob = min(cob * age_factor[grupo], 0.95)

        primera = int(pob_grupo * grupo_cob * random.uniform(0.95, 1.05))
        segunda = int(primera * random.uniform(0.82, 0.92))
        refuerzo = int(segunda * random.uniform(0.45, 0.65))

        # Distribute across vaccines
        for dosis_tipo, total_dosis in [("Primera dosis", primera),
                                         ("Segunda dosis", segunda),
                                         ("Refuerzo", refuerzo)]:
            # Random vaccine distribution
            pfizer_pct = random.uniform(0.30, 0.40)
            sinovac_pct = random.uniform(0.25, 0.35)
            astra_pct = random.uniform(0.10, 0.20)
            janssen_pct = random.uniform(0.05, 0.10)
            moderna_pct = 1 - pfizer_pct - sinovac_pct - astra_pct - janssen_pct

            for vacuna, pct in [("Pfizer", pfizer_pct), ("Sinovac", sinovac_pct),
                                ("AstraZeneca", astra_pct), ("Janssen", janssen_pct),
                                ("Moderna", moderna_pct)]:
                dosis_count = int(total_dosis * pct)
                if dosis_count > 0:
                    rows.append([depto, grupo, dosis_tipo, vacuna, dosis_count])

output_path = r"C:\Users\Dani Serrato\Documents\DS_ML_Portfolio\clases_analitica\clase_03\MinSalud_vacunacion_COVID_departamento.csv"

with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(["departamento", "grupo_etario", "tipo_dosis", "vacuna", "dosis_aplicadas"])
    for row in rows:
        writer.writerow(row)

print(f"Archivo generado: {output_path}")
print(f"Total registros: {len(rows)}")

# Summary for teacher
print("\n--- Resumen por departamento (primera dosis total) ---")
from collections import defaultdict
totales = defaultdict(int)
for row in rows:
    if row[2] == "Primera dosis":
        totales[row[0]] += row[4]

for depto in sorted(totales, key=totales.get, reverse=True)[:10]:
    pob = poblaciones[depto]
    cob = totales[depto] / pob * 100
    print(f"  {depto}: {totales[depto]:,} ({cob:.1f}% de población)")
