import bibtexparser
import csv
import os

# Función para convertir el archivo .bib a .csv automáticamente detectando los campos
def bib_to_csv_auto(bib_file, csv_file):
    # Leer el archivo .bib
    with open(bib_file, encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    # Obtener todos los campos presentes en las entradas
    all_fields = set()
    for entry in bib_database.entries:
        all_fields.update(entry.keys())

    # Convertir el conjunto de campos a una lista y ordenarla (opcional)
    all_fields = sorted(list(all_fields))

    # Abrir el archivo .csv para escribir
    with open(csv_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=all_fields)

        # Escribir los encabezados
        writer.writeheader()

        # Escribir los datos de cada entrada
        for entry in bib_database.entries:
            # Escribir cada entrada en el archivo CSV, rellenando con valores vacíos donde no existan campos
            writer.writerow({field: entry.get(field, '') for field in all_fields})

    print(f"Archivo CSV creado exitosamente: {csv_file}")

# Función para recorrer una carpeta y procesar los archivos .bib
def process_bib_folder(bib_folder, output_folder):
    # Verificar si la carpeta de salida existe, si no, crearla
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Recorrer todos los archivos en la carpeta de archivos .bib
    for filename in os.listdir(bib_folder):
        if filename.endswith('.bib'):
            # Crear las rutas completas para el archivo .bib y el archivo .csv
            bib_file = os.path.join(bib_folder, filename)
            csv_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.csv")

            # Convertir el archivo .bib a .csv
            bib_to_csv_auto(bib_file, csv_file)

# Uso de la función
bib_folder = 'Archivos/TF/ArchivoTF_2024-10-24'  # Cambia esto por la carpeta donde están los archivos .bib
output_folder = 'Archivos/TF/ArchivosTF2_CSV'  # Cambia esto por la carpeta donde quieres guardar los archivos .csv

# Procesar todos los archivos .bib en la carpeta
process_bib_folder(bib_folder, output_folder)
