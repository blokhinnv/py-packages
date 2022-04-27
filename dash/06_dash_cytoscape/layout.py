from dash import Dash, html, dcc
import dash_cytoscape as cyto
import networkx as nx
import math

def city_graph():
    nodes = [
        {
            'data': {'id': short, 'label': label},
            'position': {'x': 20 * lat, 'y': -20 * long}
        }
        for short, label, long, lat in (
            ('la', 'Los Angeles', 34.03, -118.25),
            ('nyc', 'New York', 40.71, -74),
            ('to', 'Toronto', 43.65, -79.38),
            ('mtl', 'Montreal', 45.50, -73.57),
            ('van', 'Vancouver', 49.28, -123.12),
            ('chi', 'Chicago', 41.88, -87.63),
            ('bos', 'Boston', 42.36, -71.06),
            ('hou', 'Houston', 29.76, -95.37)
        )
    ]

    edges = [
        {'data': {'source': source, 'target': target}}
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
            ('nyc', 'bos')
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
                    'cytoscape-grid',
                    cyto.Cytoscape(
                        id='cytoscape-grid',
                        elements=elements,
                        style={'width': '100%', 'height': '350px'},
                        layout={
                            'name': 'grid',
                            'rows': 3
                        }
                    )
                ], className="four columns"),
                html.Div([
                    'cytoscape-circle',
                    cyto.Cytoscape(
                        id='cytoscape-circle',
                        elements=elements,
                        style={'width': '100%', 'height': '350px'},
                        layout={
                            'name': 'circle',
                            'radius': 250,
                            'startAngle': math.pi * 1 / 6,
                            'sweep': math.pi * 2 / 3
                        }
                    )
                ], className="four columns"),
                html.Div([
                    'cytoscape-breadthfirst1',
                    cyto.Cytoscape(
                        id='cytoscape-breadthfirst1',
                        elements=elements,
                        style={'width': '100%', 'height': '350px'},
                        layout={
                            'name': 'breadthfirst',
                            'roots': '[id = "nyc"]' # специальный синтаксис для указания ID узлов 
                        }
                    )
                ], className="four columns"),
            ],
            className='Row'
        ),
        html.Div(
            [
                html.Div([
                    'cytoscape-breadthfirst2',
                    cyto.Cytoscape(
                        id='cytoscape-breadthfirst2',
                        elements=elements,
                        style={'width': '100%', 'height': '350px'},
                        layout={
                            'name': 'breadthfirst',
                            'roots': '#van, #mtl' # специальный синтаксис для указания ID узлов 
                        }
                    )
                ], className="four columns"),
                html.Div([
                    'cytoscape-cose',
                    cyto.Cytoscape(
                        id='cytoscape-cose',
                        elements=elements,
                        style={'width': '100%', 'height': '350px'},
                        layout={
                            'name': 'cose'
                        }
                    )
                ], className="four columns"),
            ],
            className="Row"
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
