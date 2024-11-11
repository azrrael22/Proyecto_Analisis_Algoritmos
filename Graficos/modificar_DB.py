import sqlite3
import random
import pycountry

# Connect to the SQLite database
conn = sqlite3.connect('bibliometria copy.db')
cursor = conn.cursor()

# Add new columns to the publicaciones table
cursor.execute("ALTER TABLE publicaciones ADD COLUMN citaciones INTEGER")
cursor.execute("ALTER TABLE publicaciones ADD COLUMN pais_primer_autor TEXT")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Columns added successfully.")





# Connect to the SQLite database
conn = sqlite3.connect('bibliometria copy.db')
cursor = conn.cursor()

# Update each row with random values
cursor.execute("SELECT id_publicacion FROM publicaciones")
rows = cursor.fetchall()

for row in rows:
    citaciones = random.randint(0, 250)
    pais_primer_autor = list (pycountry.countries)[random.randint(0, 248)]
    print(pais_primer_autor.name)
    cursor.execute("UPDATE publicaciones SET citaciones = ?, pais_primer_autor = ? WHERE id_publicacion = ?", (citaciones, pais_primer_autor.name, row[0]))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Columns updated successfully.")