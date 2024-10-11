import pandas as pd
import sqlite3
import re

# Rutas de los archivos CSV
rutaIEEE = 'Archivos_CSV/archivo_combinado.csv'
rutaScience = 'Archivos_CSV/archivo_combinadoScienceD.csv'
rutaScopus = 'Archivos_CSV/scopus solo me dejo 20000.csv'

# Leer los CSV
df1 = pd.read_csv(rutaIEEE) 
df2 = pd.read_csv(rutaScience) 
df3 = pd.read_csv(rutaScopus) 

# Asociar cada DataFrame con su base de datos correspondiente
dfList = [
    (df1, 'IEEE'),
    (df2, 'ScienceDirect'),
    (df3, 'Scopus')
]

# Conectar a la base de datos (se creará si no existe)
conexion = sqlite3.connect('bibliometria.db')
cursor = conexion.cursor()

# Crear la tabla 'publicaciones' si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS publicaciones (
    id_publicacion INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL UNIQUE,
    primer_autor TEXT,
    afiliacion_primer_autor TEXT,
    anio_publicacion INTEGER,
    tipo_producto TEXT,
    journal TEXT,
    publisher TEXT,
    base_datos TEXT,
    cantidad_citaciones INTEGER DEFAULT 0,
    resumen TEXT,
    palabras_clave TEXT,
    doi TEXT
);
''')
conexion.commit()

# Expresión regular para separadores de autores
separadores = r';|\s+and\s+'

# Recorrer los DataFrames e insertar registros
for df, nombre_base in dfList:
    for index, row in df.iterrows():
        titulo = row.get('Document Title') or row.get('title') or row.get('Title')
        autores = row.get('Authors') or row.get('author')
        afiliaciones = row.get('Author Affiliations') or row.get('Affiliations')
        anio_publicacion = row.get('Publication Year') or row.get('year') or row.get('Year')
        tipo_producto = row.get('Document Identifier') or row.get('Document Type')
        journal = row.get('Publication Title') or row.get('journal') or row.get('Source title')
        publisher = row.get('Publisher')
        base_datos = nombre_base  # Asignar el nombre de la base de datos
        cantidad_citaciones = row.get('Article Citation Count') or row.get('Cited by') or 0
        resumen = row.get('Abstract') or row.get('abstract')
        palabras_clave = row.get('Author Keywords') or row.get('keywords')
        doi = row.get('DOI') or row.get('doi')

        # Asegurarse de que los campos numéricos sean del tipo correcto
        cantidad_citaciones = int(cantidad_citaciones) if pd.notnull(cantidad_citaciones) else 0
        anio_publicacion = int(anio_publicacion) if pd.notnull(anio_publicacion) else None

        # Extraer el primer autor
        if pd.notnull(autores):
            lista_autores = [autor.strip() for autor in re.split(separadores, autores, flags=re.IGNORECASE)]
            primer_autor = lista_autores[0] if lista_autores else None
        else:
            primer_autor = None

        # Extraer la afiliación del primer autor
        if pd.notnull(afiliaciones):
            lista_afiliaciones = [afiliacion.strip() for afiliacion in re.split(';', afiliaciones, flags=re.IGNORECASE)]
            afiliacion_primer_autor = lista_afiliaciones[0] if lista_afiliaciones else None
        else:
            afiliacion_primer_autor = None

        # Limpiar el campo 'tipo_producto' para eliminar 'IEEE' si está presente
        if pd.notnull(tipo_producto) and isinstance(tipo_producto, str):
            tipo_producto = tipo_producto.replace('IEEE', '').strip()

        # Verificar que los campos obligatorios no sean None
        if pd.notnull(titulo) :
            try:
                cursor.execute('''
                INSERT INTO publicaciones (
                    titulo, primer_autor, afiliacion_primer_autor, anio_publicacion,
                    tipo_producto, journal, publisher, base_datos,
                    cantidad_citaciones, resumen, palabras_clave, doi
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    titulo,
                    primer_autor,
                    afiliacion_primer_autor,
                    anio_publicacion,
                    tipo_producto,
                    journal,
                    publisher,
                    base_datos,
                    cantidad_citaciones,
                    resumen,
                    palabras_clave,
                    doi
                ))
            except sqlite3.IntegrityError:
               print(f"El registro con título '{titulo}' ya existe en la base de datos.")
             
        else:
            print(f"Registro en la fila {index} {nombre_base} omitido por falta de datos obligatorios.")

# Confirmar los cambios
conexion.commit()

# Cerrar la conexión
conexion.close()
