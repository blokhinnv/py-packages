from dash import Dash, html, dcc
import dash_cytoscape as cyto
import networkx as nx
import math

def city_graph():
    nodes = [
        {
            'data': {'id': short, 'label': label, 'pop': pop},
            'position': {'x': 20 * lat, 'y': -20 * long}
        }
        for short, label, long, lat, pop in (
            ('la', 'Los Angeles', 34.03, -118.25, 1000),
            ('nyc', 'New York', 40.71, -74, 2000),
            ('to', 'Toronto', 43.65, -79.38, 1000),
            ('mtl', 'Montreal', 45.50, -73.57, 3000),
            ('van', 'Vancouver', 49.28, -123.12, 6000),
            ('chi', 'Chicago', 41.88, -87.63, 3000),
            ('bos', 'Boston', 42.36, -71.06, 5000),
            ('hou', 'Houston', 29.76, -95.37, 1000)
        )
    ]

    edges = [
        {'data': {'id':f'{source}2{target}', 'source': source, 'target': target}}
        for source, target in (
            ('van', 'la'),
            ('la', 'chi'),
            ('hou', 'chi'),
            ('to', 'mtl'),
            ('mtl', 'bos'),
            ('nyc', 'bos'),
            ('to', 'hou'),
            ('to', 'nyc'),
            ('la', 'nyc'),
            ('bos', 'nyc')
        )
    ]
    elements = nodes + edges
    return elements


app = Dash(
    __name__,
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
)
elements = city_graph()

app.layout = html.Div([
        html.Div(
            [
                html.Div([
                    'Красные узлы содержат пробел в названии',
                    cyto.Cytoscape(
                        id='cytoscape-grid',
                        elements=elements,
                        style={'width': '100%', 'height': '350px'},
                        layout={
                            'name': 'grid',
                            'rows': 3
                        },
                        stylesheet=[
                            {
                                "selector": "[label *= ' ']",
                                "style": {
                                    "background-color": "#FF4136",
                                }
                            }
                        ]
                    )
                ], className="four columns"),
                html.Div([
                    'Зеленые узлы имеют степень больше 2 + кривые ребра для параллельных связей',
                    cyto.Cytoscape(
                        id='cytoscape-circle',
                        elements=elements,
                        style={'width': '100%', 'height': '350px'},
                        layout={
                            'name': 'circle',
                            'radius': 250,
                            'startAngle': math.pi * 1 / 6,
                            'sweep': math.pi * 2 / 3
                        },
                        stylesheet=[
                            {
                                "selector": "node",
                                'style': {
                                    'label': 'data(label)'
                                }
                            },
                            {
                                "selector": "[[degree > 2]]", # двойные скобки для метаинформации
                                "style": {
                                    "background-color": "green"
                                }
                            },
                            {
                                "selector": '#nyc2bos, #bos2nyc', # способ выбрать ребра
                                "style": {
                                    'curve-style': 'bezier',
                                    'label': 'bezier',
                                }
                            }
                        ]
                    )
                ], className="four columns"),
                html.Div([
                    'Треугольные узлы имеют большое население; Хьюстон раскрашен в зеленый',
                    cyto.Cytoscape(
                        id='cytoscape-breadthfirst1',
                        elements=elements,
                        style={'width': '100%', 'height': '350px'},
                        layout={
                            'name': 'breadthfirst',
                            'roots': '[id = "nyc"]' # специальный синтаксис для указания ID узлов 
                        },
                        stylesheet=[
                            {
                                'selector': 'node',
                                'style': {
                                    'label': 'data(label)'
                                }
                            },
                            {
                                "selector": "[pop >= 3000]",
                                "style": {
                                    "shape": "triangle"
                                }
                            },
                            {
                                "selector": "[label = 'Houston']",
                                "style": {
                                    "shape": "rectangle"
                                }
                            },
                            {
                                "selector": "#nyc2bos, #bos2nyc",
                                "style": {
                                    "curve-style": "bezier"
                                }
                            },
                            {
                                "selector": "#nyc2la, #la2nyc",
                                "style": {
                                    "curve-style": "segments"
                                }
                            },
                            {
                                "selector": "#to2nyc",
                                "style": {
                                    'target-arrow-shape': 'triangle',
                                    'target-arrow-color': 'blue',
                                    'target-arrow-shape': 'vee',
                                    "curve-style": "bezier",
                                    'line-color': 'red',
                                }
                            },
                        ]
                    )
                ], className="four columns"),
            ],
            className='Row'
        ),
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
