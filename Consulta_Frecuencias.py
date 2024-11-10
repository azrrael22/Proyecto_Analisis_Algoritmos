import sqlite3
import pandas as pd

# Conectar a la base de datos
conexion = sqlite3.connect('bibliometria.db')

# Consultar la frecuencia de cada variable junto con su categoría
query = '''
SELECT categoria, variable, SUM(frecuencia) AS total_frecuencia
FROM analisis_frecuencias
GROUP BY categoria, variable
ORDER BY categoria, total_frecuencia DESC;
'''
df_frecuencia = pd.read_sql_query(query, conexion)

# Cerrar la conexión
conexion.close()

# Configurar para mostrar todas las filas
pd.set_option('display.max_rows', None)

# Mostrar los resultados
print(df_frecuencia)
