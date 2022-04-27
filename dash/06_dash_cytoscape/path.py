from dash import Dash, html, dcc
import dash_cytoscape as cyto
import networkx as nx
G = nx.karate_club_graph()
pos = nx.spring_layout(G, seed=42)

my_stylesheet = [
    # Стиль для узлов
    {
        'selector': 'node',
        'style': {
            'content': 'data(label)'
        }
    },
    # Стиль для классов
    {
        'selector': '.red',
        'style': {
            'background-color': 'red',
            'line-color': 'red'
        }
    },
    {
        'selector': '.triangle',
        'style': {
            'shape': 'triangle'
        }
    }
]


app = Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-two-nodes',
        layout={'name': 'preset'}, # располагает в соответствии с координатами узлов
        style={'width': '100%', 'height': '800px'},
        stylesheet=my_stylesheet, # описание всех используемых классов
        elements=[
            {"data": {"id": 0, "label": "0 (locked)"}, "position": {"x": 0, "y": 0}, "locked": True, "classes": "red"},
            {"data": {"id": 1, "label": "1 (selected)"}, "position": {"x": 150, "y": 0}, "selected": True, "classes": "triangle"},
            {"data": {"id": 2, "label": "2 (!selectable)"}, "position": {"x": 250, "y": 0}, "selectable": False, "classes": "triangle"},
            {"data": {"id": 3, "label": "3 (!grabbable)"}, "position": {"x": 350, "y": 0}, "grabbable": False, "classes": "red"},
            {"data": {"source": 0, "target": 1}},
            {"data": {"source": 1, "target": 2}},
            {"data": {"source": 2, "target": 3}},
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
