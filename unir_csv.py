import pandas as pd
import os
import csv


def combinar_csvs(ruta_archivos):
    # Crear una lista para almacenar los DataFrames y llevar un registro del número de filas
    lista_dataframes = []
    total_filas = 0

    # Recorrer todos los archivos en la carpeta especificada
    for archivo in os.listdir(ruta_archivos):
        if archivo.endswith('.csv'):
            # Cargar cada archivo CSV usando quotechar para conservar comillas dobles
            archivo_csv = os.path.join(ruta_archivos, archivo)
            df = pd.read_csv(archivo_csv, quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # Mostrar cuántas líneas tiene el archivo (sin contar el encabezado)
            num_filas = len(df)
            print(f"Archivo '{archivo}' tiene {num_filas} líneas de datos (sin encabezado).")

            # Sumar al total de filas
            total_filas += num_filas

            # Agregar el DataFrame a la lista
            lista_dataframes.append(df)

    # Concatenar todos los DataFrames en uno solo
    df_combinado = pd.concat(lista_dataframes, ignore_index=True)

    # Generar el nombre del archivo de salida
    archivo_salida = os.path.join('Archivos', 'archivo_combinadoTF.csv')

    # Guardar el archivo combinado usando quotechar para conservar comillas dobles
    df_combinado.to_csv(archivo_salida, index=False, quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Mostrar el total de líneas en el archivo combinado
    print(f"\nTotal de líneas en el archivo combinado (sin encabezado): {total_filas}")
    print(f"El archivo combinado '{archivo_salida}' debería tener {total_filas + 1} líneas (incluyendo el encabezado).")


if __name__ == "__main__":
    ruta_archivos = 'Archivos/TF/ArchivosTF_CSV'
    combinar_csvs(ruta_archivos)
