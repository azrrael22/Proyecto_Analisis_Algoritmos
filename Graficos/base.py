import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Conectar a la base de datos
db_path = 'bibliometria.db'
conn = sqlite3.connect(db_path)

# Consulta para cantidad de publicaciones por base de datos
query = """
SELECT base_datos, COUNT(*) as cantidad
FROM publicaciones
GROUP BY base_datos
ORDER BY cantidad DESC;
"""
data = conn.execute(query).fetchall()
conn.close()

# Imprimir datos
print("Cantidad de publicaciones por base de datos:")
for row in data:
    print(f"Base de Datos: {row[0]}, Cantidad: {row[1]}")

# Preparar y graficar los datos
df = pd.DataFrame(data, columns=['base_datos', 'cantidad'])
plt.figure(figsize=(10, 6))
ax = sns.barplot(data=df, x='cantidad', y='base_datos', palette='magma')

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
plt.title("Cantidad de Publicaciones por Base de Datos")
plt.xlabel("Cantidad")
plt.ylabel("Base de Datos")
plt.tight_layout()
plt.show()
