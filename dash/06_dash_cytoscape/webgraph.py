from dash import Dash, html, dcc, Input, Output, State
import dash_cytoscape as cyto
import networkx as nx
import json

import pandas as pd
import networkx as nx

def fb_graph():
    nodes_df = pd.read_csv('06_dash_cytoscape/musae_facebook_target.csv')
    edges_df = pd.read_csv('06_dash_cytoscape/musae_facebook_edges.csv')
    G = nx.Graph()
    G.add_edges_from(edges_df.values.tolist())
    layout = nx.circular_layout(G)

    edges = []
    for u, v in edges_df.values:
        edges.append({'data': {'source': u, 'target': v}})
    nodes = []
    for node in nodes_df.to_dict(orient='records'):
        id_ = node['id']
        nodes.append({
            'data': node, 
            # 'position': {
            #     'x': layout[id_][0], 
            #     'y': layout[id_][1]
            # },
            # 'locked': True,
            # 'selectable': False,
            # 'draggable': False
        })    

    return nodes, edges

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

def web_graph():
    node_ids = set()
    nodes = []
    edges = []
    with open("06_dash_cytoscape/web-webbase-2001.mtx") as fp:
        fp.readline()
        fp.readline()
        for line in fp:
            source, target = tuple(map(int, line.split()))
            node_ids.update((source, target))
            edges.append({'data': {'source': source, 'target': target}})
    for node_id in node_ids:
        nodes.append({'data': {'id': node_id}})
    return nodes, edges

app = Dash(
    __name__,
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
)
nodes, edges = fb_graph()
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
            'width': "3px",
            'height': "3px",
            "border-color": "black",
            "border-width": 1,
        },

    },
    {
        'selector': 'edge',
        'style': {
            'line-color': 'gray',
            'width': "1px",
            'height': "1px",
        }
    }
]

app.layout = html.Div(
    [
        html.P(
            f"Граф facebook: {len(nodes)} узлов, {len(edges)} связей", 
            style={"text-align": "center"}
        ),
        cyto.Cytoscape(
            id="cyto",
            elements=elements,
            stylesheet=default_stylesheet,
            style={
                "width": "100%",
                "height": "1000px"
            },
            layout={
                "name": "concentric",
            },
            responsive=False
        )
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)
