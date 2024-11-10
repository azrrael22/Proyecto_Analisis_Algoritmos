import sqlite3
import pandas as pd
import re

# Conectar a la base de datos
conexion = sqlite3.connect('bibliometria.db')
cursor = conexion.cursor()

# Crear la tabla para almacenar los resultados si no existe con una restricción de unicidad
cursor.execute('''
CREATE TABLE IF NOT EXISTS analisis_frecuencias (
    categoria TEXT,
    variable TEXT,
    frecuencia INTEGER,
    UNIQUE(categoria, variable)
);
''')
conexion.commit()

# Cargar la tabla que contiene los abstracts
query = "SELECT resumen FROM publicaciones"
df = pd.read_sql_query(query, conexion)

# Diccionario de categorías con variables y sinónimos
categorias_sinonimos = {
    "Habilidades": {
        "Abstraction": ["abstraction"],
        "Algorithm": ["algorithm"],
        "Algorithmic thinking": ["algorithmic thinking"],
        "Coding": ["coding"],
        "Collaboration": ["collaboration"],
        "Cooperation": ["cooperation"],
        "Creativity": ["creativity"],
        "Critical thinking": ["critical thinking"],
        "Debug": ["debug"],
        "Decomposition": ["decomposition"],
        "Evaluation": ["evaluation"],
        "Generalization": ["generalization"],
        "Logic": ["logic"],
        "Logical thinking": ["logical thinking"],
        "Modularity": ["modularity"],
        "Pattern recognition": ["pattern recognition"],
        "Problem solving": ["problem solving"],
        "Programming": ["programming"],
        "Representation": ["representation"],
        "Reuse": ["reuse"],
        "Simulation": ["simulation"]
    },
    "Conceptos Computacionales": {
        "Conditionals": ["conditionals"],
        "Control structures": ["control structures"],
        "Directions": ["directions"],
        "Events": ["events"],
        "Functions": ["functions"],
        "Loops": ["loops"],
        "Modular structure": ["modular structure"],
        "Parallelism": ["parallelism"],
        "Sequences": ["sequences"],
        "Software/hardware": ["software/hardware"],
        "Variables": ["variables"]
    },
    "Actitudes":{
        "Emotional":["emotional"],
        "Engagement":["engagement"],
        "Motivation":["motivation"],
        "Perceptions":["perceptions"],
        "Persistence":["persistence"],
        "Self-efficacy":["self-efficacy"],
        "Self-perceived":["self-perceived"]
    },
    "Propiedades psicométricas":{
        "Classical Test Theory":["classical test theory","ctt"],
        "Confirmatory Factor Analysis":["confirmatory factor analysis","cfa"],
        "Exploratory Factor Analysis":["exploratory factor analysis","efa"],
        "Item Response Theory (IRT)":["item response theory","irt"],
        "Reliability":["reliability"],
        "Structural Equation Model":["structural equation model","sem"],
        "Validity":["validity"]
    },
    "Herramienta de evaluación":{
        "Beginners Computational Thinking test":["Beginners Computational Thinking test","BCTt"],
        "Coding Attitudes Survey":["Coding Attitudes Survey","ESCAS"],
        "Collaborative Computing Observation Instrument":["Collaborative Computing Observation Instrument"],
        "Competent Computational Thinking test":["Competent Computational Thinking test","cCTt"],
        "Computational thinking skills test":["Computational thinking skills test","CTST"],
        "Computational concepts":["Computational concepts"],
        "Computational Thinking Assessment for Chinese Elementary Students":["Computational Thinking Assessment for Chinese Elementary Students","CTA-CES"],
        "Computational Thinking Challenge":["Computational Thinking Challenge","CTC"],
        "Computational Thinking Levels Scale":["Computational Thinking Levels Scale","CTLS"],
        "Computational Thinking Scale":["Computational Thinking Scale","CTS"],
        "Computational Thinking Skill Levels Scale":["Computational Thinking Skill Levels Scale","CTS"],#No sé si el acronimo este bien
        "Computational Thinking Test":["Computational Thinking Test","CTt"],
        "Computational Thinking Test for Elementary School Students":["Computational Thinking Test for Elementary School Students","CTT-ES"],
        "Computational Thinking Test for Lower Primary":["Computational Thinking Test for Lower Primary","CTtLP"],
        "Computational thinking-skill tasks on numbers and arithmetic":["Computational thinking-skill tasks on numbers and arithmetic"],
        "Computerized Adaptive Programming Concepts Test":["Computerized Adaptive Programming Concepts Test","CAPCT"],
        "CT Scale":["CT Scale","CTS"],
        "Elementary Student Coding Attitudes Survey":["Elementary Student Coding Attitudes Survey","ESCAS"],
        "General self-efficacy scale":["General self-efficacy scale"],
        "ICT competency test":["ICT competency test"],
        "Instrument of computational identity":["Instrument of computational identity"],
        "KBIT fluid intelligence subtest":["KBIT fluid intelligence subtest"],
        "Mastery of computational concepts Test and an Algorithmic Test":["Mastery of computational concepts Test and an Algorithmic Test"],
        "Multidimensional 21st Century Skills Scale":["Multidimensional 21st Century Skills Scale"],
        "Self-efficacy scale":["Self-efficacy scale"],
        "STEM learning attitude scale":["STEM learning attitude scale","STEM-LAS"],
        "The computational thinking scale":["The computational thinking scale"]
    },
    "Diseño de investigación":{
        "No experimental":["No experimental"],
        "Experimental":["Experimental"],
        "Longitudinal research":["Longitudinal research"],
        "Mixed methods":["Mixed methods"],
        "Post-test":["Post-test"],
        "Pre-test":["Pre-test"],
        "Quasi-experiments":["Quasi-experiments"]
    },
    "Nivel de escolaridad":{
        "Upper elementary education":["Upper elementary education","Upper elementary school"],
        "Primary school":["Primary school","Primary education","Elementary school"],
        "Early childhood education":["Early childhood education","Kindergarten","Preschool"],
        "Secondary school":["Secondary school","Secondary education"],
        "high school":["high school","higher education"],
        "University":["University","College"]
    },
    "Medio":{
        "Block programming":["Block programming"],
        "Mobile application":["Mobile application"],
        "Pair programming":["Pair programming"],
        "Plugged activities":["Plugged activities"],
        "Programming":["Programming"],
        "Robotics":["Robotics"],
        "Spreadsheet":["Spreadsheet"],
        "STEM":["STEM"],
        "Unplugged activities":["Unplugged activities"]
    },
    "Estrategia":{
        "Construct-by-self mind mapping":["Construct-by-self mind mapping","CBS-MM"],
        "Construct-on-scaffold mind mapping":["Construct-on-scaffold mind mapping","COS-MM"],
        "Design-based learning":["Design-based learning","DBL"],
        "Evidence-centred design approach":["Evidence-centred design approach"],
        "Gamification":["Gamification"],
        "Reverse engineering pedagogy":["Reverse engineering pedagogy","REP"],
        "Technology-enhanced learning":["Technology-enhanced learning"],
        "Collaborative learning":["Collaborative learning"],
        "Cooperative learning":["Cooperative learning"],
        "Flipped classroom":["Flipped classroom"],
        "Game-based learning":["Game-based learning"],
        "Inquiry-based learning":["Inquiry-based learning"],
        "Personalized learning":["Personalized learning"],
        "Problem-based learning":["Problem-based learning"],
        "Project-based learning":["Project-based learning"],
        "Universal design for learning":["Universal design for learning"]
    },
    "Herramienta":{
        "Alice":["Alice"],
        "Arduino":["Arduino"],
        "Scratch":["Scratch"],
        "ScratchJr":["ScratchJr"],
        "Blockly Games":["Blockly Games"],
        "Code.org":["Code.org"],
        "Codecombat":["Codecombat"],
        "CSUnplugged":["CSUnplugged"],
        "Robot Turtles":["Robot Turtles"],
        "Hello Ruby":["Hello Ruby"],
        "Kodable":["Kodable"],
        "LightbotJr":["LightbotJr"],
        "KIBO robots":["KIBO robots"],
        "BEE BOT":["BEE BOT"],
        "CUBETTO":["CUBETTO"],
        "Minecraft":["Minecraft"],
        "Agent Sheets":["Agent Sheets"],
        "Mimo":["Mimo"],
        "Py– Learn":["Py– Learn"],
        "SpaceChem":["SpaceChem"]
    }
}

# Inicializar una lista para almacenar las frecuencias con categoría
frecuencias = []

# Contar la frecuencia de aparición de cada variable en los abstracts
for abstract in df['resumen'].dropna():  # Eliminar valores nulos para evitar errores
    for categoria, variables in categorias_sinonimos.items():
        for variable, sinonimos in variables.items():
            # Crear una expresión regular que busque cualquiera de los sinónimos de la variable
            patron = r'\b(' + '|'.join(sinonimos) + r')\b'  # Búsqueda exacta de palabras
            frecuencia = len(re.findall(patron, abstract, flags=re.IGNORECASE))  # Ignorar mayúsculas/minúsculas
            if frecuencia > 0:
                frecuencias.append({"Variable": variable, "Frecuencia": frecuencia, "Categoría": categoria})

# Convertir la lista de frecuencias a un DataFrame
df_frecuencias = pd.DataFrame(frecuencias)

# Agrupar por variable y categoría para sumar las frecuencias en todos los abstracts
df_frecuencias = df_frecuencias.groupby(["Categoría", "Variable"]).sum().reset_index()

# Insertar los resultados en la tabla `analisis_frecuencias` con manejo de duplicados
for _, row in df_frecuencias.iterrows():
    try:
        cursor.execute('''
        INSERT INTO analisis_frecuencias (categoria, variable, frecuencia)
        VALUES (?, ?, ?)
        ''', (row['Categoría'], row['Variable'], row['Frecuencia']))
    except sqlite3.IntegrityError:
        print(f"Registro duplicado para {row['Categoría']} - {row['Variable']}, no se insertará.")

# Confirmar los cambios y cerrar la conexión
conexion.commit()
conexion.close()