import pandas as pd
import sqlite3
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Conectar a la base de datos
conexion = sqlite3.connect('bibliometria.db')

# Cargar la tabla de frecuencias
query = '''
SELECT categoria, variable, SUM(frecuencia) AS total_frecuencia
FROM analisis_frecuencias
GROUP BY categoria, variable
ORDER BY categoria, total_frecuencia DESC;
'''
df_frecuencia = pd.read_sql_query(query, conexion)

# Cerrar la conexión
conexion.close()

# Crear un diccionario de palabras y frecuencias
frecuencias_dict = dict(zip(df_frecuencia['variable'], df_frecuencia['total_frecuencia']))

# Generar la nube de palabras
wordcloud = WordCloud(
    width=1920, 
    height=1080, 
    background_color='black', 
    colormap='Set3',
    scale=2,
    max_words=120,       
    ).generate_from_frequencies(frecuencias_dict)

# Mostrar la nube de palabras
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # Quitar ejes
plt.show()
