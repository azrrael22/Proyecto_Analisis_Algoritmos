import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Conectar a la base de datos
db_path = 'bibliometria.db'
conn = sqlite3.connect(db_path)

# Consultar los 15 autores más citados por cantidad de artículos
query = """
SELECT primer_autor, COUNT(*) as cantidad
FROM publicaciones
GROUP BY primer_autor
ORDER BY cantidad DESC
LIMIT 15;
"""
data = conn.execute(query).fetchall()

# Cerrar conexión
conn.close()

# Imprimir los datos en la consola
print("15 Autores más citados (por cantidad de artículos):")
for row in data:
    print(f"Autor: {row[0]}, Cantidad de artículos: {row[1]}")

# Preparar los datos para el gráfico
df = pd.DataFrame(data, columns=['primer_autor', 'cantidad'])
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='cantidad', y='primer_autor', palette='viridis')
plt.title("15 Autores Más Citados (por Cantidad de Artículos)")
plt.xlabel("Cantidad de Artículos")
plt.ylabel("Primer Autor")
plt.tight_layout()
plt.show()
