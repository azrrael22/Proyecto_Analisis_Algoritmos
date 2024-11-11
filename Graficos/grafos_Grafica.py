import matplotlib.pyplot as plt
import networkx as nx
import sqlite3



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
        G.add_node(journal, type='journal')
        journal_articles = [article for article in articles if article['journal'] == journal]
        top_articles = sorted(journal_articles, key=lambda x: x['citations'], reverse=True)[:15]
        
        for article in top_articles:
            G.add_node(article['title'], type='article', country=article['first_author_country'])
            G.add_edge(journal, article['title'])
            
            country = article['first_author_country']
            if country not in G:
                G.add_node(country, type='country')
            G.add_edge(article['title'], country)
    
    return G

def draw_graph(G):
    pos = nx.spring_layout(G)
    journal_nodes = [node for node, attr in G.nodes(data=True) if attr['type'] == 'journal']
    article_nodes = [node for node, attr in G.nodes(data=True) if attr['type'] == 'article']
    country_nodes = [node for node, attr in G.nodes(data=True) if attr['type'] == 'country']
    
    nx.draw_networkx_nodes(G, pos, nodelist=journal_nodes, node_color='blue', node_size=500, label='Journals')
    nx.draw_networkx_nodes(G, pos, nodelist=article_nodes, node_color='green', node_size=300, label='Articles')
    nx.draw_networkx_nodes(G, pos, nodelist=country_nodes, node_color='red', node_size=200, label='Countries')
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    
    plt.legend(scatterpoints=1)
    plt.show()

top_journals = identify_top_journals(articles)
G = create_graph(articles, top_journals)
draw_graph(G)
