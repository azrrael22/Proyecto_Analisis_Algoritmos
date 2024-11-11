from flask import Flask, render_template, make_response
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sqlite3
import io
import base64
import plotly.express as px
from pyvis.network import Network
import networkx as nx
from wordcloud import WordCloud

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Welcome to the Bibliometric Analysis Dashboard</h1>
    <ul>
        <li><a href="/año_publicacion">Cantidad de Artículos por Año de Publicación</a></li>
        <li><a href="/autores_citados">15 Autores Más Citados</a></li>
        <li><a href="/bases_datos">Cantidad de Publicaciones por Base de Datos</a></li>
        <li><a href="/grafos_grafica">Grafos de Artículos y Países</a></li>
        <li><a href="/journal">Cantidad de Artículos por Journal</a></li>
        <li><a href="/tipo_producto">Cantidad Total de Artículos por Tipo de Producto</a></li>
        <li><a href="/consulta_frecuencias">Frecuencia de Variables por Categoría</a></li>
        <li><a href="/nube_palabras">Nube de Palabras</a></li>
    </ul>
    '''

@app.route('/año_publicacion')
def año_publicacion():
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

    # Preparar el gráfico
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(data=df_rango, x='rango_anio', y='cantidad', palette='viridis')

    # Añadir los valores encima de las barras con fuente más pequeña
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{int(height)}', 
                    (p.get_x() + p.get_width() / 2., height), 
                    ha='center', va='bottom',  
                    fontsize=10, color='black',  
                    xytext=(0, 5), textcoords='offset points')

    # Configuración del gráfico
    plt.title("Cantidad de Artículos por Rango de Años de Publicación")
    plt.xlabel("Rango de Años de Publicación")
    plt.ylabel("Cantidad de Artículos")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save it to a temporary buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img = base64.b64encode(buf.getvalue()).decode('utf8')
    buf.close()

    return render_template('año_publicacion.html', img_data=img)

@app.route('/autores_citados')
def autores_citados():
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

    # Preparar los datos para el gráfico
    df = pd.DataFrame(data, columns=['primer_autor', 'cantidad'])
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='cantidad', y='primer_autor', palette='viridis')
    plt.title("15 Autores Más Citados (por Cantidad de Artículos)")
    plt.xlabel("Cantidad de Artículos")
    plt.ylabel("Primer Autor")
    plt.tight_layout()

    # Save it to a temporary buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img = base64.b64encode(buf.getvalue()).decode('utf8')
    buf.close()

    return render_template('autores_citados.html', img_data=img)

@app.route('/bases_datos')
def bases_datos():
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

    # Preparar y graficar los datos
    df = pd.DataFrame(data, columns=['base_datos', 'cantidad'])
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=df, x='cantidad', y='base_datos', palette='magma')

    # Añadir los valores encima de las barras con fuente más pequeña
    for p in ax.patches:
        height = p.get_width()
        ax.annotate(f'{int(height)}', 
                    (p.get_width() + 2, p.get_y() + p.get_height() / 2),  
                    ha='left', va='center',  
                    fontsize=10, color='black')

    # Configuración del gráfico
    plt.title("Cantidad de Publicaciones por Base de Datos")
    plt.xlabel("Cantidad")
    plt.ylabel("Base de Datos")
    plt.tight_layout()

    # Save it to a temporary buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img = base64.b64encode(buf.getvalue()).decode('utf8')
    buf.close()

    return render_template('bases_datos.html', img_data=img)

@app.route('/grafos_grafica')
def grafos_grafica():
    # Connect to the database
    conn = sqlite3.connect('bibliometria copy.db')
    cursor = conn.cursor()

    # Extract the values from the table
    cursor.execute("SELECT titulo, journal, citaciones, pais_primer_autor FROM publicaciones")
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Convert the rows to a list of dictionaries
    articles = [
        {'title': row[0], 'journal': row[1], 'citations': row[2], 'first_author_country': row[3]}
        for row in rows
    ]

    def identify_top_journals(articles):
        # Identify the top 10 journals with the most published articles
        journal_counts = {}
        for article in articles:
            journal = article['journal']
            if journal in journal_counts:
                journal_counts[journal] += 1
            else:
                journal_counts[journal] = 1
        top_journals = sorted(journal_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        return [journal for journal, count in top_journals]

    def create_graph(articles, top_journals):
        G = nx.Graph()
        
        for journal in top_journals:
            G.add_node(journal, nodetype='blue', type='journal')
            journal_articles = [article for article in articles if article['journal'] == journal]
            top_articles = sorted(journal_articles, key=lambda x: x['citations'], reverse=True)[:15]
            
            for article in top_articles:
                G.add_node(article['title'], nodetype='red', type='article', country=article['first_author_country'])
                G.add_edge(journal, article['title'])
                
                country = article['first_author_country']
                if country not in G:
                    G.add_node(country, nodetype='green', type='country')
                G.add_edge(article['title'], country)
        
        return G

    top_journals = identify_top_journals(articles)
    G = create_graph(articles, top_journals)

    # Create a Pyvis network
    net = Network(notebook=False)
    net.from_nx(G)
    

    # Generate the HTML content
    html_content = net.generate_html()

    return render_template('grafos_grafica.html', graph_html=html_content)

@app.route('/journal')
def journal():
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

    # Preparar los datos para el gráfico
    df = pd.DataFrame(data, columns=['journal', 'cantidad'])
    fig = px.bar(df, x='journal', y='cantidad', orientation='v', title='Cantidad de Artículos por Journal', labels={'cantidad': 'Cantidad de Artículos', 'journal': 'Journal'})
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, yaxis_range=[0, df['cantidad'].max() + 5])

    # Convertir el gráfico a HTML
    graph_html = fig.to_html(full_html=False)

    return render_template('journal.html', graph_html=graph_html)


@app.route('/tipo_producto')
def tipo_producto():
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

    # Preparar los datos para el gráfico
    df = pd.DataFrame(data, columns=['tipo_producto', 'cantidad'])
    fig = px.bar(df, x='cantidad', y='tipo_producto', orientation='h', title='Cantidad Total de Artículos por Tipo de Producto', labels={'cantidad': 'Cantidad de Artículos', 'tipo_producto': 'Tipo de Producto'})

    # Convertir el gráfico a HTML
    graph_html = fig.to_html(full_html=False)

    return render_template('tipo_producto.html', graph_html=graph_html)

@app.route('/consulta_frecuencias')
def consulta_frecuencias():
    # Conectar a la base de datos
    db_path = 'bibliometria.db'
    conn = sqlite3.connect(db_path)

    # Consultar la frecuencia de cada variable junto con su categoría
    query = '''
    SELECT categoria, variable, SUM(frecuencia) AS total_frecuencia
    FROM analisis_frecuencias
    GROUP BY categoria, variable
    ORDER BY categoria, total_frecuencia DESC;
    '''
    df_frecuencia = pd.read_sql_query(query, conn)

    # Cerrar conexión
    conn.close()

    # Preparar los datos para el gráfico
    fig = px.bar(df_frecuencia, x='variable', y='total_frecuencia', color='categoria', title='Frecuencia de Variables por Categoría', labels={'total_frecuencia': 'Frecuencia Total', 'variable': 'Variable'})

    # Convertir el gráfico a HTML
    graph_html = fig.to_html(full_html=False)

    return render_template('consulta_frecuencias.html', graph_html=graph_html)


@app.route('/nube_palabras')
def nube_palabras():
    # Conectar a la base de datos
    db_path = 'bibliometria.db'
    conn = sqlite3.connect(db_path)

    # Consultar los datos para la nube de palabras
    query = """
    SELECT categoria, variable, SUM(frecuencia) AS total_frecuencia
    FROM analisis_frecuencias
    GROUP BY categoria, variable
    ORDER BY categoria, total_frecuencia DESC;
    """
    data = conn.execute(query).fetchall()

    # Cerrar conexión
    conn.close()

    # Convertir los datos a un diccionario
    word_freq = {row[1]: row[2] for row in data}

    # Generar la nube de palabras
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

    # Guardar la nube de palabras en un buffer
    buf = io.BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_data = base64.b64encode(buf.getvalue()).decode('utf8')
    buf.close()

    return render_template('nube_palabras.html', img_data=img_data)

if __name__ == '__main__':
    app.run(debug=True)