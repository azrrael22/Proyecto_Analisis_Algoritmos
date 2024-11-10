import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Conectar a la base de datos
db_path = 'bibliometria.db'
conn = sqlite3.connect(db_path)

# Consultar la cantidad total de artículos por tipo de producto
query = """
SELECT tipo_producto, COUNT(*) as cantidad
FROM publicaciones
GROUP BY tipo_producto
ORDER BY cantidad DESC;
"""
data = conn.execute(query).fetchall()

# Cerrar conexión
conn.close()

# Imprimir los datos en la consola
print("Datos obtenidos de la consulta:")
for row in data:
    print(f"Tipo de producto: {row[0]}, Cantidad: {row[1]}")

# Preparar los datos para el gráfico
df = pd.DataFrame(data, columns=['tipo_producto', 'cantidad'])
plt.figure(figsize=(10, 8))
ax = sns.barplot(data=df, x='cantidad', y='tipo_producto', palette='viridis')

# Añadir los valores encima de las barras con fuente más pequeña
for p in ax.patches:
    # Obtener la altura de la barra
    height = p.get_width()  # Cambié get_height() por get_width() para obtener el valor de la barra horizontal
    # Colocar el valor justo encima de la barra
    ax.annotate(f'{int(height)}', 
                (p.get_width() + 2, p.get_y() + p.get_height() / 2),  # Ajuste de la posición
                ha='left', va='center',  # Coloca el texto a la izquierda de la barra
                fontsize=10, color='black')

# Configuración del gráfico
plt.title("Cantidad Total de Artículos por Tipo de Producto")
plt.xlabel("Cantidad de Artículos")
plt.ylabel("Tipo de Producto")
plt.xticks(rotation=0, ha='right')
plt.tight_layout()  # Ajusta automáticamente el layout

plt.show()
