import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Conectar a la base de datos
db_path = 'bibliometria.db'
conn = sqlite3.connect(db_path)

# Consultar la cantidad de artículos por journal
query = """
SELECT journal, COUNT(*) as cantidad
FROM publicaciones
GROUP BY journal
ORDER BY cantidad DESC;
"""
data = conn.execute(query).fetchall()

# Cerrar conexión
conn.close()

# Imprimir los datos en la consola
print("Cantidad de artículos por journal:")
for row in data:
    print(f"Journal: {row[0]}, Cantidad de artículos: {row[1]}")

# Preparar los datos para el gráfico
df = pd.DataFrame(data, columns=['journal', 'cantidad'])
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='cantidad', y='journal', palette='viridis')
plt.title("Cantidad de Artículos por Journal")
plt.xlabel("Cantidad de Artículos")
plt.ylabel("Journal")
plt.tight_layout()
plt.show()
