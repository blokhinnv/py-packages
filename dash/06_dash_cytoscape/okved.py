from dash import Dash, html, dcc, Input, Output, State
import dash_cytoscape as cyto

import pandas as pd
import networkx as nx

def get_okved_graph(fname='06_dash_cytoscape/okved_2014.csv'):
    okved_data = pd.read_csv(
        fname,
        dtype={
            'code': str,
            'code_okved': str,
            'parent_code': str,
            'native_code': str
        }
    )
    okved_data['label'] = okved_data['native_code']
    digit_code_to_okved = (okved_data.loc[:, ['code', 'native_code']]
                                        .set_index('code')
                                        .loc[:, 'native_code']
                                        .to_dict())
    # add extra root node which is not real OKVED
    digit_code_to_okved['000000'] = 'root'

    classifier_edges = okved_data[['code', 'parent_code']].copy()
    classifier_edges['source'] = classifier_edges['code'].map(digit_code_to_okved)
    classifier_edges['target'] = classifier_edges['parent_code'].map(digit_code_to_okved)
    classifier_edges['label'] = classifier_edges['source'] + '->' + classifier_edges['target']
    
    nodes = (okved_data.loc[:, ['native_code', 'name', 'comment', "label"]]
                       .rename(columns={"native_code": "id"})
                       .to_dict(orient="records"))
    edges = classifier_edges[["source", "target", "label"]].to_dict(orient="records")
    elements = [{"data": node} for node in nodes]
    elements.extend({"data": edge} for edge in edges)
    elements.append({"data": {"id": "root", "label": "root"}})
    G = nx.Graph()
    G.add_edges_from((e["data"]["source"], e["data"]["target"]) for e in elements if "source" in e["data"])
    return elements, G

all_elements, G = get_okved_graph()
start_elements = [e for e in all_elements if e["data"].get("id")=="root"]

app = Dash(
    __name__,
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
)

app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="okved_graph",
            layout={
                "name": "breadthfirst",
                "spacingFactor": 5
            },
            elements=start_elements,
            style={
                "width": "100%",
                "height": "500px"
            },
            autoRefreshLayout=True
        ),
    ],
)

@app.callback(
    Output("okved_graph", "elements"),
    Input("okved_graph", "tapNodeData"),
    State("okved_graph", "elements")
)
def _(node, elements):
    if not node:
        return start_elements
    nid = node["id"] 
    ns = list(G[nid])
    new_nodes = set()
    new_edges_els = []
    for n in list(ns):
        for e in all_elements:
            dt = e["data"]
            if "source" in dt:
                s, t = dt["source"], dt["target"]
                if n == s and t == nid:
                    new_edges_els.append(e)
                    new_nodes.add(s)
                elif n == t and s == nid:
                    new_edges_els.append(e)
                    new_nodes.add(t)

    new_nodes_els = [e for n in new_nodes for e in all_elements if e["data"].get("id")==n]

    return elements + new_nodes_els + new_edges_els

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
