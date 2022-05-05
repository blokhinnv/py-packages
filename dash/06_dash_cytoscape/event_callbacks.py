from dash import Dash, html, dcc, Input, Output, State
import dash_cytoscape as cyto
import networkx as nx
import json


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
    return nodes, edges


app = Dash(
    __name__,
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
)
nodes, edges = city_graph()
elements = nodes + edges

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(label)'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'line-color': '#A3C4BC'
        }
    }
]

app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="cyto",
            elements=elements,
            stylesheet=default_stylesheet,
            style={
                "width": "100%",
                "height": "400px"
            },
            layout={
                "name": "preset"
            }
        ),
        html.Div(
            [
                html.Div(
                    [
                        "Данные об узле при клике",
                        html.Pre(id='tap-node-data-pre', style=styles['pre']),
                    ],
                    className="two columns"
                ),
                html.Div(
                    [
                        "Данные об ребре при клике",
                        html.Pre(id='tap-edge-data-pre', style=styles['pre']),
                    ],
                    className="two columns"
                ),
                html.Div(
                    [
                        "Данные об узле при наведении",
                        html.Pre(id='hover-node-data-pre', style=styles['pre']),
                    ],
                    className="two columns"
                ),
                html.Div(
                    [
                        "Данные об ребре при наведении",
                        html.Pre(id='hover-edge-data-pre', style=styles['pre']),
                    ],
                    className="two columns"
                ),
                html.Div(
                    [
                        "Выбранные узлы",
                        html.Pre(id='selected-node-data-pre', style=styles['pre']),
                    ],
                    className="two columns"
                ),
            ],
            className="Row"
        )
    ]
)

@app.callback(
    Output('tap-node-data-pre', 'children'),
    Input('cyto', 'tapNodeData')
)
def _(data):
    return json.dumps(data, indent=2)

@app.callback(
    Output('tap-edge-data-pre', 'children'),
    Input('cyto', 'tapEdgeData')
)
def _(data):
    return json.dumps(data, indent=2)

@app.callback(
    Output('hover-node-data-pre', 'children'),
    Input('cyto', 'mouseoverNodeData')
)
def _(data):
    return json.dumps(data, indent=2)

@app.callback(
    Output('hover-edge-data-pre', 'children'),
    Input('cyto', 'mouseoverEdgeData')
)
def _(data):
    return json.dumps(data, indent=2)

@app.callback(
    Output('selected-node-data-pre', 'children'),
    Input('cyto', 'selectedNodeData')
)
def _(data):
    return json.dumps(data, indent=2)

@app.callback(
    Output("cyto", "stylesheet"),
    Input("cyto", "tapNode")
)
def _(tap_data):
    if tap_data is None:
        return default_stylesheet

    node_id = tap_data['data']['id']
    additional_styles = [
        {
            "selector": f"#{node_id}",
            "style": {
                "background-color": "green"
            }
        }
    ]
    for edge in tap_data['edgesData']:
        for node_side in ["source", "target"]:
            if edge[node_side] != node_id:
                additional_styles.append(
                    {
                        "selector": f"#{edge[node_side]}",
                        "style": {
                            "background-color": "pink"
                        }
                    }
                )
    return default_stylesheet + additional_styles

if __name__ == '__main__':
    app.run_server(debug=True)
