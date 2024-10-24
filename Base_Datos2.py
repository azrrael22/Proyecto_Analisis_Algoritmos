import pandas as pd
import sqlite3
import re

# Rutas de los archivos CSV
rutaIEEE = 'Archivos/Archivos_Base_Datos/archivo_combinadoIEEE.csv'
rutaScience = 'Archivos/Archivos_Base_Datos/archivo_combinadoScienceDirect.csv'
rutaScopus = 'Archivos/Archivos_Base_Datos/scopus.csv'
rutaSage = 'Archivos/Archivos_Base_Datos/archivo_combinadoSage.csv'
rutaTF = 'Archivos/Archivos_Base_Datos/archivo_combinadoTFV2.csv'

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
    base_datos TEXT,
    titulo TEXT NOT NULL UNIQUE,
    primer_autor TEXT NOT NULL,
    anio_publicacion INTEGER NOT NULL,
    tipo_producto TEXT NOT NULL,
    paginas TEXT,
    journal TEXT NOT NULL,
    volumen TEXT,
    issue TEXT,
    resumen TEXT NOT NULL,
    url TEXT,
    doi TEXT
);
''')
conexion.commit()

# Expresión regular para separadores de autores
separadores = r';|\s+and\s+'

# Función para extraer el año de un valor dado
def extraer_anio(valor):
    match = re.search(r'\d{4}', str(valor))  # Buscar un patrón de 4 dígitos en el valor
    if match:
        return int(match.group(0))  # Devolver el valor como entero
    return None  # Si no hay coincidencia, devolver None

# Recorrer los DataFrames e insertar registros
for df, nombre_base in dfList:
    for index, row in df.iterrows():
        titulo = row.get('Document Title') or row.get('title') or row.get('Title')
        autores = row.get('Authors') or row.get('author')
        anio_publicacion = row.get('Publication Year') or row.get('year') or row.get('Year')
        tipo_producto = row.get('Document Identifier') or row.get('Document Type') or row.get('ENTRYTYPE')
        
        pagInicio = row.get('Start Page')
        pagFin = row.get('End Page')

        # Combinar las páginas en un solo valor si ambas existen
        if pd.notnull(pagInicio) and pd.notnull(pagInicio):
            paginas = f"{pagInicio}-{pagInicio}"
        else:
            # Si no existen las dos páginas, verificar 'pages' o 'Page count'
            paginas = row.get('pages') or row.get('Page count')

        journal = row.get('Publication Title') or row.get('journal') or row.get('Source title')
        volumen = row.get('Volume') or row.get('volume')
        issue = row.get('Issue') or row.get('number')
        base_datos = nombre_base  # Asignar el nombre de la base de datos
        resumen = row.get('Abstract') or row.get('abstract')
        url = row.get('url') or row.get('PDF Link') or row.get('Link')
        doi = row.get('DOI') or row.get('doi')

        # Asegurarse de que los campos numéricos sean del tipo correcto
        anio_publicacion = extraer_anio(anio_publicacion)

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
        if pd.notnull(titulo) and pd.notnull(resumen) and pd.notnull(primer_autor) and pd.notnull(anio_publicacion) and pd.notnull(tipo_producto) and pd.notnull(journal):
            try:
                cursor.execute('''
                INSERT INTO publicaciones (
                    base_datos, titulo, primer_autor, anio_publicacion,
                    tipo_producto, paginas, journal, volumen, issue,
                    resumen, url, doi
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    base_datos,
                    titulo,
                    primer_autor,
                    anio_publicacion,
                    tipo_producto,
                    paginas,
                    journal,
                    volumen,
                    issue,
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
