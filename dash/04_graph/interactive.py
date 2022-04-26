
import networkx as nx
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


app = Dash(
    __name__, 
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
)

import numpy as np
def to_scatter(G, pos):
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_x.append(None)
        edge_y.append(None)
    edges_lines = np.c_[edge_x, edge_y]
    
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y) 
    nodes_markers = np.c_[node_x, node_y]

    node_text = np.array([f'Узел {n}' for n in G])
    
    fig = go.Figure(
        data = [
            go.Scatter(
                x=edges_lines[:, 0],
                y=edges_lines[:, 1],
                mode="lines",
                line_width=0.5,
                line_color="black",
                name="Связи"
            ),
            go.Scatter(
                x=nodes_markers[:, 0],
                y=nodes_markers[:, 1],
                mode="markers",
                marker_size=20,
                marker_color="blue",
                name="Узлы",
                text=node_text,
                customdata = list(G),
                hoverinfo='text',
            ),
        ],
    )
    fig.update_layout(clickmode='event+select')
    return fig
 

G = nx.karate_club_graph()
pos = nx.spring_layout(G, seed=42)
fig1 = to_scatter(G, pos)
fig2 = to_scatter(nx.ego_graph(G, 0), pos)

app.layout = html.Div(
    [
        html.Div([dcc.Graph(id="full-graph", figure=fig1)], className="six columns"),
        html.Div([dcc.Graph(id="ego-graph", figure=fig2)], className="six columns")
    ],
    className='Row'
)

@app.callback(
    Output('ego-graph', 'figure'),
    Input('full-graph', 'clickData'))
# срабатывает при клике на точку
def display_ego(clickData):
    print(clickData)
    if clickData is None:
        return to_scatter(G, pos)
    sG = nx.compose_all([nx.ego_graph(G, point["customdata"]) for point in clickData["points"]] )

    return to_scatter(sG, pos)

    

if __name__ == '__main__':
    app.run_server(debug=True)
