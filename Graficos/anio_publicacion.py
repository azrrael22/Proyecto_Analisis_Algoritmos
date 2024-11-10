import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Conectar a la base de datos
db_path = 'bibliometria.db'
conn = sqlite3.connect(db_path)

# Consultar la cantidad de artículos por año de publicación
query = """
SELECT anio_publicacion, COUNT(*) as cantidad
FROM publicaciones
GROUP BY anio_publicacion
ORDER BY anio_publicacion;
"""
data = conn.execute(query).fetchall()

# Cerrar conexión
conn.close()

# Convertir los datos obtenidos a un DataFrame de pandas
df = pd.DataFrame(data, columns=['anio_publicacion', 'cantidad'])

# Agrupar los años en intervalos de 5 años
df['rango_anio'] = pd.cut(df['anio_publicacion'], bins=range(min(df['anio_publicacion']), max(df['anio_publicacion']) + 5, 5), right=False, labels=[f'{x}-{x+4}' for x in range(min(df['anio_publicacion']), max(df['anio_publicacion']), 5)])

# Agrupar por los rangos de años
df_rango = df.groupby('rango_anio')['cantidad'].sum().reset_index()

# Imprimir los datos en la consola
print("Cantidad de artículos por rango de años:")
print(df_rango)

# Preparar el gráfico
plt.figure(figsize=(12, 6))
ax = sns.barplot(data=df_rango, x='rango_anio', y='cantidad', palette='viridis')

# Añadir los valores encima de las barras con fuente más pequeña
for p in ax.patches:
    # Obtener la altura de la barra
    height = p.get_height()
    # Colocar el valor justo encima de la barra
    ax.annotate(f'{int(height)}', 
                (p.get_x() + p.get_width() / 2., height), 
                ha='center', va='bottom',  # Coloca el texto encima de la barra
                fontsize=10, color='black',  # Fuente más pequeña
                xytext=(0, 5), textcoords='offset points')

# Configuración del gráfico
plt.title("Cantidad de Artículos por Rango de Años de Publicación")
plt.xlabel("Rango de Años de Publicación")
plt.ylabel("Cantidad de Artículos")
plt.xticks(rotation=45)  # Rotar las etiquetas del eje X para mejorar la legibilidad
plt.tight_layout()
plt.show()
