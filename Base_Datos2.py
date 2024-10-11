import pandas as pd
import sqlite3
import re

# Rutas de los archivos CSV
rutaIEEE = 'Archivos/archivo_combinadoIEEE.csv'
rutaScience = 'Archivos/archivo_combinadoScienceDirect.csv'
rutaScopus = 'Archivos/scopus.csv'
rutaSage = 'Archivos/archivo_combinadoSage.csv'
rutaTF = 'Archivos/archivo_combinadoTF.csv'

# Leer los CSV
df1 = pd.read_csv(rutaIEEE) 
df2 = pd.read_csv(rutaScience) 
df3 = pd.read_csv(rutaScopus) 
df4 = pd.read_csv(rutaSage)
df5 = pd.read_csv(rutaTF)

# Asociar cada DataFrame con su base de datos correspondiente
dfList = [
    (df1, 'IEEE'),
    (df2, 'ScienceDirect'),
    (df3, 'Scopus'),
    (df4, 'Sage'),
    (df5, 'Taylor and Francis')
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
    anio_publicacion INTEGER DEFAULT 0,
    tipo_producto TEXT,
    paginas INTEGER,
    journal TEXT,
    volumen INTEGER DEFAULT 0,
    issue INTEGER DEFAULT 0,
    base_datos TEXT,
    resumen TEXT,
    url TEXT,
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
        anio_publicacion = row.get('Publication Year') or row.get('year') or row.get('Year')
        tipo_producto = row.get('Document Identifier') or row.get('Document Type') or row.get('ENTRYTYPE')
        journal = row.get('Publication Title') or row.get('journal') or row.get('Source title')
        base_datos = nombre_base  # Asignar el nombre de la base de datos
        resumen = row.get('Abstract') or row.get('abstract')
        doi = row.get('DOI') or row.get('doi')

        # Asegurarse de que los campos numéricos sean del tipo correcto
        anio_publicacion = int(anio_publicacion) if pd.notnull(anio_publicacion) else None

        # Extraer el primer autor
        if pd.notnull(autores):
            lista_autores = [autor.strip() for autor in re.split(separadores, autores, flags=re.IGNORECASE)]
            primer_autor = lista_autores[0] if lista_autores else None
        else:
            primer_autor = None

        # Limpiar el campo 'tipo_producto' para eliminar 'IEEE' si está presente
        if pd.notnull(tipo_producto) and isinstance(tipo_producto, str):
            tipo_producto = tipo_producto.replace('IEEE', '').strip()

        # Verificar que los campos obligatorios no sean None
        if pd.notnull(titulo) :
            try:
                cursor.execute('''
                INSERT INTO publicaciones (
                    titulo, primer_autor, anio_publicacion,
                    tipo_producto, paginas, journal, volumen, issue, base_datos,
                    resumen, url, doi
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    titulo,
                    primer_autor,
                    anio_publicacion,
                    tipo_producto,
                    paginas,
                    journal,
                    volumen,
                    issue,
                    base_datos,
                    resumen,
                    url,
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
