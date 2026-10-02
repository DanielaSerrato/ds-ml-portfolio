"""
Genera dataset de delitos por municipio simulando datos de Policía Nacional
para ejercicios de DAX y relaciones en Power BI.
"""
import csv
import random

random.seed(55)

# Major municipalities with their departments
municipios = [
    ("Bogotá D.C.", "Bogotá D.C."),
    ("Medellín", "Antioquia"), ("Bello", "Antioquia"), ("Envigado", "Antioquia"), ("Itagüí", "Antioquia"),
    ("Cali", "Valle del Cauca"), ("Buenaventura", "Valle del Cauca"), ("Palmira", "Valle del Cauca"),
    ("Barranquilla", "Atlántico"), ("Soledad", "Atlántico"),
    ("Cartagena", "Bolívar"),
    ("Cúcuta", "Norte de Santander"),
    ("Bucaramanga", "Santander"), ("Floridablanca", "Santander"),
    ("Pereira", "Risaralda"),
    ("Santa Marta", "Magdalena"),
    ("Ibagué", "Tolima"),
    ("Manizales", "Caldas"),
    ("Villavicencio", "Meta"),
    ("Pasto", "Nariño"),
    ("Neiva", "Huila"),
    ("Armenia", "Quindío"),
    ("Popayán", "Cauca"),
    ("Valledupar", "Cesar"),
    ("Montería", "Córdoba"),
    ("Sincelejo", "Sucre"),
    ("Tunja", "Boyacá"),
    ("Riohacha", "La Guajira"),
    ("Quibdó", "Chocó"),
    ("Florencia", "Caquetá"),
]

poblacion_municipio = {
    "Bogotá D.C.": 7901653, "Medellín": 2569007, "Cali": 2252616,
    "Barranquilla": 1274250, "Cartagena": 1057767, "Cúcuta": 711715,
    "Bucaramanga": 581130, "Pereira": 488839, "Santa Marta": 538718,
    "Ibagué": 583315, "Manizales": 434403, "Villavicencio": 531275,
    "Pasto": 471518, "Neiva": 357392, "Armenia": 308236,
    "Popayán": 325125, "Valledupar": 521132, "Montería": 505334,
    "Sincelejo": 297618, "Bello": 533268, "Envigado": 232926,
    "Itagüí": 304425, "Buenaventura": 311727, "Palmira": 315238,
    "Soledad": 692534, "Floridablanca": 271728, "Tunja": 215311,
    "Riohacha": 298927, "Quibdó": 130337, "Florencia": 185972,
}

tipos_delito = ["Hurto a personas", "Hurto a comercio", "Hurto de vehículos",
                "Lesiones personales", "Homicidio", "Violencia intrafamiliar",
                "Hurto a residencias", "Extorsión"]

# Base rates per 100K by crime type
tasa_base = {
    "Hurto a personas": 450, "Hurto a comercio": 120, "Hurto de vehículos": 85,
    "Lesiones personales": 280, "Homicidio": 24, "Violencia intrafamiliar": 180,
    "Hurto a residencias": 95, "Extorsión": 15,
}

# City-specific multipliers
ciudad_factor = {
    "Bogotá D.C.": 1.3, "Medellín": 1.1, "Cali": 1.4,
    "Barranquilla": 1.0, "Cartagena": 1.1, "Cúcuta": 1.3,
    "Bucaramanga": 0.8, "Pereira": 0.9, "Santa Marta": 1.0,
    "Ibagué": 0.85, "Manizales": 0.75, "Villavicencio": 1.1,
    "Pasto": 0.7, "Neiva": 0.85, "Armenia": 0.9,
    "Popayán": 0.8, "Valledupar": 1.05, "Montería": 0.95,
    "Sincelejo": 0.9, "Bello": 1.0, "Envigado": 0.6,
    "Itagüí": 0.85, "Buenaventura": 1.5, "Palmira": 1.1,
    "Soledad": 1.15, "Floridablanca": 0.65, "Tunja": 0.5,
    "Riohacha": 1.1, "Quibdó": 1.3, "Florencia": 1.0,
}

anos = [2020, 2021, 2022, 2023, 2024]
meses = list(range(1, 13))

rows = []
for muni, depto in municipios:
    pob = poblacion_municipio[muni]
    c_factor = ciudad_factor[muni]

    for ano in anos:
        # Yearly trend (general decrease)
        year_trend = 1.0 + (2022 - ano) * 0.03

        for mes in meses:
            for tipo in tipos_delito:
                base = tasa_base[tipo]
                # Monthly rate per 100K, then scale to population
                seasonal = 1 + 0.1 * random.uniform(-1, 1)
                if mes == 12:
                    seasonal = 1.15  # December spike
                if mes in [1, 6]:
                    seasonal = 1.08  # Vacation months

                rate = base * c_factor * year_trend * seasonal * random.uniform(0.8, 1.2) / 12
                cantidad = max(0, int(pob * rate / 100000))

                if cantidad > 0:
                    rows.append([depto, muni, ano, mes, tipo, cantidad])

output_path = r"C:\Users\Dani Serrato\Documents\DS_ML_Portfolio\clases_analitica\clase_07\PoliciaNacional_delitos_municipio.csv"

with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(["departamento", "municipio", "ano", "mes", "tipo_delito", "cantidad"])
    for row in rows:
        writer.writerow(row)

print(f"Archivo generado: {output_path}")
print(f"Total registros: {len(rows)}")
print(f"Municipios: {len(municipios)}")
print(f"Tipos de delito: {len(tipos_delito)}")
