from dash import Dash, html, dcc
import dash_cytoscape as cyto
import networkx as nx
G = nx.karate_club_graph()
pos = nx.spring_layout(G, seed=42)


app = Dash(__name__)

def get_cyto_elements(G, pos, scale=200):
    # elements - это список словарей
    # каждый элемент имеет ключ data - характеристики узла в виде словаря
    # у узлов - доп ключ position
    # у ребер - в data есть ключи source и target
    elements = []
    for node, data in G.nodes(data=True):
        # у каждого узла должен быть ID
        data["id"] = node
        data["label"] = f"Узел {node}"
        x, y = pos[node] * scale
        position = {"x": x, "y": y}
        elements.append({
            "data": data, 
            "position": position
        })
    for u, v in G.edges:
        elements.append({
            "data": {"source": u, "target": v} 
        })
    return elements


cyto_elements = get_cyto_elements(G, pos)
app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-two-nodes',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '800px'},
        elements=cyto_elements
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
