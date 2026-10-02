"""
Genera dataset de matrículas y deserción escolar por departamento
simulando datos de MinEducación para análisis exploratorio.
"""
import csv
import random

random.seed(77)

departamentos = [
    "Amazonas", "Antioquia", "Arauca", "Atlántico", "Bogotá D.C.",
    "Bolívar", "Boyacá", "Caldas", "Caquetá", "Casanare",
    "Cauca", "Cesar", "Chocó", "Córdoba", "Cundinamarca",
    "Huila", "La Guajira", "Magdalena", "Meta", "Nariño",
    "Norte de Santander", "Putumayo", "Quindío", "Risaralda",
    "San Andrés", "Santander", "Sucre", "Tolima",
    "Valle del Cauca", "Vaupés", "Vichada"
]

niveles = ["Preescolar", "Básica Primaria", "Básica Secundaria", "Media"]
anos = [2019, 2020, 2021, 2022, 2023, 2024]

# Base matriculation rates by department (proportion of population)
mat_base = {
    "Bogotá D.C.": 0.15, "Antioquia": 0.16, "Valle del Cauca": 0.15,
    "Atlántico": 0.17, "Santander": 0.14, "Bolívar": 0.18,
    "Cundinamarca": 0.14, "Boyacá": 0.13, "Nariño": 0.16,
    "Córdoba": 0.18, "Tolima": 0.14, "Cauca": 0.17,
    "Norte de Santander": 0.15, "Cesar": 0.17, "Magdalena": 0.17,
    "Huila": 0.15, "La Guajira": 0.19, "Risaralda": 0.13,
    "Meta": 0.14, "Caldas": 0.13, "Sucre": 0.18,
    "Quindío": 0.12, "Chocó": 0.19, "Caquetá": 0.16,
    "Casanare": 0.14, "Arauca": 0.15, "Putumayo": 0.16,
    "San Andrés": 0.12, "Amazonas": 0.15, "Vaupés": 0.16,
    "Vichada": 0.17,
}

# Desertion rates by level (higher in secondary/media)
desercion_base = {
    "Preescolar": 0.035,
    "Básica Primaria": 0.028,
    "Básica Secundaria": 0.045,
    "Media": 0.038,
}

# Department factor for desertion (rural/poor = higher)
desercion_factor = {
    "Bogotá D.C.": 0.6, "Antioquia": 0.85, "Valle del Cauca": 0.8,
    "Atlántico": 0.9, "Santander": 0.75, "Bolívar": 1.1,
    "Cundinamarca": 0.7, "Boyacá": 0.8, "Nariño": 1.15,
    "Córdoba": 1.2, "Tolima": 0.95, "Cauca": 1.25,
    "Norte de Santander": 1.1, "Cesar": 1.15, "Magdalena": 1.2,
    "Huila": 1.0, "La Guajira": 1.4, "Risaralda": 0.75,
    "Meta": 0.9, "Caldas": 0.78, "Sucre": 1.2,
    "Quindío": 0.72, "Chocó": 1.5, "Caquetá": 1.3,
    "Casanare": 0.95, "Arauca": 1.1, "Putumayo": 1.25,
    "San Andrés": 0.65, "Amazonas": 1.35, "Vaupés": 1.5,
    "Vichada": 1.45,
}

poblaciones = {
    "Amazonas": 80845, "Antioquia": 7044013, "Arauca": 286733,
    "Atlántico": 2722128, "Bogotá D.C.": 7901653,
    "Bolívar": 2236073, "Boyacá": 1269581, "Caldas": 1007896,
    "Caquetá": 518476, "Casanare": 448813, "Cauca": 1506202,
    "Cesar": 1264612, "Chocó": 553294, "Córdoba": 1909071,
    "Cundinamarca": 3242999, "Huila": 1226096, "La Guajira": 1103729,
    "Magdalena": 1424937, "Meta": 1089466, "Nariño": 1886097,
    "Norte de Santander": 1516381, "Putumayo": 379441,
    "Quindío": 583935, "Risaralda": 1003466, "San Andrés": 84208,
    "Santander": 2236327, "Sucre": 937393, "Tolima": 1415107,
    "Valle del Cauca": 4873548, "Vaupés": 47919, "Vichada": 118341,
}

# Level distribution of students
nivel_pct = {
    "Preescolar": 0.10,
    "Básica Primaria": 0.45,
    "Básica Secundaria": 0.30,
    "Media": 0.15,
}

rows = []
for depto in departamentos:
    pob = poblaciones[depto]
    base_mat = mat_base[depto]
    d_factor = desercion_factor[depto]

    for ano in anos:
        # COVID effect on 2020-2021
        if ano == 2020:
            year_factor = 0.92
            desert_mult = 1.4
        elif ano == 2021:
            year_factor = 0.95
            desert_mult = 1.25
        elif ano == 2022:
            year_factor = 0.98
            desert_mult = 1.1
        else:
            year_factor = 1.0 + (ano - 2019) * 0.005
            desert_mult = 1.0

        for nivel in niveles:
            n_pct = nivel_pct[nivel]
            matriculados = int(pob * base_mat * n_pct * year_factor * random.uniform(0.95, 1.05))

            tasa_desercion = desercion_base[nivel] * d_factor * desert_mult * random.uniform(0.85, 1.15)
            tasa_desercion = round(min(tasa_desercion, 0.15), 4)
            desertores = int(matriculados * tasa_desercion)

            cobertura = round(random.uniform(0.75, 0.99) if nivel != "Media"
                             else random.uniform(0.55, 0.85), 2)

            rows.append([depto, ano, nivel, matriculados, desertores, tasa_desercion, cobertura])

output_path = r"C:\Users\Dani Serrato\Documents\DS_ML_Portfolio\clases_analitica\clase_05\MinEducacion_matriculas_desercion.csv"

with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(["departamento", "ano", "nivel_educativo", "matriculados", "desertores",
                      "tasa_desercion", "cobertura_neta"])
    for row in rows:
        writer.writerow(row)

print(f"Archivo generado: {output_path}")
print(f"Total registros: {len(rows)}")
