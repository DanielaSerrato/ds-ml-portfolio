"""
Genera un CSV con datos "sucios" de población por departamento
simulando los problemas típicos de los archivos del DANE.
El estudiante debe limpiarlo en clase.
"""
import csv
import random

departamentos = [
    ("Amazonas", "Leticia", [79610, 80213, 80845, 81499, 82177]),
    ("Antioquia", "Medellín", [6977984, 7010812, 7044013, 7077587, 7111532]),
    ("Arauca", "Arauca", [283642, 285178, 286733, 288306, 289897]),
    ("Atlántico", "Barranquilla", [2685908, 2703946, 2722128, 2740453, 2758919]),
    ("Bolívar", "Cartagena", [2199072, 2217474, 2236073, 2254868, 2273859]),
    ("Boyacá", "Tunja", [1264263, 1266914, 1269581, 1272263, 1274962]),
    ("Caldas", "Manizales", [1003475, 1005681, 1007896, 1010119, 1012351]),
    ("Caquetá", "Florencia", [510042, 514239, 518476, 522752, 527068]),
    ("Casanare", "Yopal", [439093, 443929, 448813, 453745, 458726]),
    ("Cauca", "Popayán", [1491508, 1498835, 1506202, 1513608, 1521053]),
    ("Cesar", "Valledupar", [1243975, 1254247, 1264612, 1275069, 1285618]),
    ("Chocó", "Quibdó", [544764, 549010, 553294, 557615, 561974]),
    ("Córdoba", "Montería", [1879265, 1894102, 1909071, 1924171, 1939401]),
    ("Cundinamarca", "Bogotá", [3190224, 3216396, 3242999, 3270034, 3297502]),
    ("Guainía", "Inírida", [50834, 51642, 52466, 53305, 54160]),
    ("Guaviare", "San José", [87844, 88716, 89601, 90498, 91408]),
    ("Huila", "Neiva", [1211163, 1218608, 1226096, 1233627, 1241201]),
    ("La Guajira", "Riohacha", [1067063, 1085284, 1103729, 1122397, 1141289]),
    ("Magdalena", "Santa Marta", [1398882, 1411847, 1424937, 1438150, 1451487]),
    ("Meta", "Villavicencio", [1063454, 1076393, 1089466, 1102672, 1116012]),
    ("Nariño", "Pasto", [1866347, 1876194, 1886097, 1896055, 1906068]),
    ("Norte de Santander", "Cúcuta", [1491689, 1503977, 1516381, 1528900, 1541533]),
    ("Putumayo", "Mocoa", [371425, 375414, 379441, 383506, 387610]),
    ("Quindío", "Armenia", [579411, 581668, 583935, 586212, 588500]),
    ("Risaralda", "Pereira", [994532, 998990, 1003466, 1007960, 1012472]),
    ("San Andrés", "San Andrés", [83403, 83804, 84208, 84614, 85023]),
    ("Santander", "Bucaramanga", [2218023, 2227148, 2236327, 2245560, 2254847]),
    ("Sucre", "Sincelejo", [921868, 929591, 937393, 945274, 953233]),
    ("Tolima", "Ibagué", [1412710, 1413905, 1415107, 1416317, 1417535]),
    ("Valle del Cauca", "Cali", [4832005, 4852663, 4873548, 4894660, 4915999]),
    ("Vaupés", "Mitú", [46381, 47143, 47919, 48708, 49511]),
    ("Vichada", "Puerto Carreño", [112958, 115618, 118341, 121128, 123980]),
]

anos = [2022, 2023, 2024, 2025, 2026]

rows = []

# Problem 1: Multiple header rows (typical DANE)
rows.append(["DEPARTAMENTO ADMINISTRATIVO NACIONAL DE ESTADÍSTICA - DANE", "", "", "", "", "", ""])
rows.append(["Proyecciones de población por departamento", "", "", "", "", "", ""])
rows.append(["Fuente: Censo Nacional de Población y Vivienda 2018", "", "", "", "", "", ""])
rows.append(["", "", "", "", "", "", ""])

# Problem 2: Merged-style headers
rows.append(["Departamento", "Capital", "2022", "2023", "2024", "2025", "2026"])

for i, (depto, capital, pobs) in enumerate(departamentos):
    row = [depto, capital] + [str(p) for p in pobs]

    # Problem 3: Random inconsistencies
    if i == 3:  # Atlántico without accent
        row[0] = "ATLANTICO"
    if i == 7:  # Caquetá all caps
        row[0] = "CAQUETA"
    if i == 13:  # Cundinamarca with extra space
        row[0] = "Cundinamarca "
    if i == 17:  # La Guajira different format
        row[0] = "LA GUAJIRA"
    if i == 21:  # Norte de Santander abbreviated
        row[0] = "Nte. de Santander"

    # Problem 4: Missing values
    if i == 10:  # Cesar missing 2024
        row[4] = ""
    if i == 15:  # Guaviare missing capital
        row[1] = ""
    if i == 25:  # San Andrés missing 2025-2026
        row[5] = ""
        row[6] = ""

    # Problem 5: Number format inconsistencies
    if i == 1:  # Antioquia with dots as thousand separator
        row[2] = "6.977.984"
        row[3] = "7.010.812"
    if i == 29:  # Valle del Cauca with spaces
        row[2] = "4 832 005"
        row[3] = "4 852 663"

    # Problem 6: Extra text in numeric cells
    if i == 20:  # Nariño
        row[4] = "1886097*"
    if i == 27:  # Sucre
        row[3] = "929591 (p)"

    rows.append(row)

    # Problem 7: Random empty rows
    if i in [9, 19]:
        rows.append(["", "", "", "", "", "", ""])

# Problem 8: Footer/notes at bottom
rows.append(["", "", "", "", "", "", ""])
rows.append(["* Dato preliminar", "", "", "", "", "", ""])
rows.append(["(p) Dato proyectado", "", "", "", "", "", ""])
rows.append(["Nota: Las proyecciones se basan en el CNPV 2018", "", "", "", "", "", ""])

output_path = r"C:\Users\Dani Serrato\Documents\DS_ML_Portfolio\clases_analitica\clase_02\DANE_poblacion_departamentos_SUCIO.csv"

with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f, delimiter=';')
    for row in rows:
        writer.writerow(row)

print(f"Archivo generado: {output_path}")
print(f"Total filas (incluyendo problemas): {len(rows)}")

# Also generate the CLEAN version (answer key for teacher)
clean_rows = []
clean_rows.append(["departamento", "capital", "ano", "poblacion"])

for depto, capital, pobs in departamentos:
    for j, ano in enumerate(anos):
        clean_rows.append([depto, capital, ano, pobs[j]])

clean_path = r"C:\Users\Dani Serrato\Documents\DS_ML_Portfolio\clases_analitica\clase_02\DANE_poblacion_departamentos_LIMPIO.csv"

with open(clean_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    for row in clean_rows:
        writer.writerow(row)

print(f"Archivo limpio generado: {clean_path}")
print(f"Total filas datos: {len(clean_rows) - 1}")
