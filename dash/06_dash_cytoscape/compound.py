from dash import Dash, html, dcc
import dash_cytoscape as cyto
import networkx as nx
G = nx.karate_club_graph()
pos = nx.spring_layout(G, seed=42)

app = Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-two-nodes',
        layout={'name': 'preset'}, # располагает в соответствии с координатами узлов
        style={'width': '100%', 'height': '800px'},
        stylesheet=[ # описание всех используемых классов
            {
                'selector': 'node',
                'style': {
                    'content': 'data(label)'
                },
            },
            {
                'selector': '.countries',
                'style': {
                    'width': 5
                }
            },
            {
                'selector': '.cities',
                'style': {
                    'line-style': 'dashed'
                }
            },
        ], 
        elements=[
            # родительские узлы
            {"data": {"id": "rus", "label": "Россия"}},
            {"data": {"id": "br", "label": "Беларусь"}},
            # дочерние узлы
            {"data": {"id": "mos", "label": "Москва", "parent": "rus"}, "position": {"x": 100, "y": 100}},
            {"data": {"id": "dg", "label": "Долгопрудный", "parent": "rus"}, "position": {"x": 100, "y": 200}},
            {"data": {"id": "min", "label": "Минск", "parent": "br"}, "position": {"x": 400, "y": 200}},
            # связи
            {"data": {"source": "rus", "target": "br"}, "classes": "countries"},
            {"data": {"source": "dg", "target": "mos"}, "classes": "cities"},
            {"data": {"source": "min", "target": "mos"}, "classes": "cities"},
            
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
