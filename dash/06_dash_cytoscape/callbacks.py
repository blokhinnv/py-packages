from dash import Dash, html, dcc, Input, Output, State
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
    return nodes, edges


app = Dash(
    __name__,
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
)
nodes, edges = city_graph()
elements = nodes + edges

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
                "name": "cose"
            }
        ),
        html.Div(
            [
                html.Div(
                    [
                        'Цвет связей',
                        html.Br(),
                        dcc.Input(id="line-color")
                    ],
                    className='two columns'
                ),
                html.Div(
                    [
                        'Цвет узлов',
                        html.Br(),
                        dcc.Input(id="node-color")
                    ],
                    className='two columns'
                ),
                html.Div(
                    [
                        'Стиль расположения узлов',
                        dcc.Dropdown(
                            options=[
                                "cose",
                                "random",
                                "circle",
                                "concentric",
                                "grid"
                            ],
                            value="cose",
                            id="layout-dropdown"
                        )
                    ],
                    className='two columns'
                ),
            ],
            style={
                "display": "flex"
            }
        ),
        html.Br(),
        html.Div(
            [
                html.Div(
                    [
                        html.Button("Добавить узел", id="add_button", n_clicks_timestamp=0)
                    ],
                    className='two columns'
                ),
                html.Div(
                    [
                        html.Button("Удалить узел", id="del_button", n_clicks_timestamp=0)
                    ],
                    className='two columns'
                ),
            ],
            style={
                "display": "flex"
            }
        )
    ]
)

@app.callback(
    Output("cyto", "layout"),
    Input("layout-dropdown", "value")
)
def _(layout):
    return {
        "name": layout,
        'animate': True
    }

@app.callback(
    Output("cyto", "stylesheet"),
    Input("node-color", "value"),
    Input("line-color", "value"),
)
def _(node_color, line_color):
    # если цвет не распознан, функция отработает
    # но ничего не произвойдет
    if line_color is None:
        line_color = ''

    if node_color is None:
        node_color = ''

    new_styles = [
        {
            'selector': 'node',
            'style': {
                'background-color': node_color
            }
        },
        {
            'selector': 'edge',
            'style': {
                'line-color': line_color
            }
        }
    ]
    # не добавляем новые стили непосредственно к стилю по умолчанию, 
    # а вместо этого объединяем default_stylesheet с new_styles. 
    # Это связано с тем, что любое изменение default_stylesheet будет постоянным, 
    # что не очень хорошо, если вы размещаете свое приложение 
    # для многих пользователей 
    # (поскольку default_stylesheet является общим для всех пользовательских сеансов).
    return default_stylesheet + new_styles

@app.callback(
    Output('cyto', 'elements'),
    Input('add_button', 'n_clicks_timestamp'),
    Input('del_button', 'n_clicks_timestamp'),
    State('cyto', 'elements')
)
def _(click_add, click_del, elements):
    def get_current_and_deleted_nodes(elements):
        current_nodes, deleted_nodes = [], []
        current_node_ids = set()
        for elem in elements:
            # у узлов нет ключа source
            if 'source' not in elem['data']:
                current_nodes.append(elem)
                current_node_ids.add(elem['data']['id'])

        # nodes - глобальный список узлов
        for node in nodes:
            if node['data']['id'] not in current_node_ids:
                deleted_nodes.append(node)
        return current_nodes, deleted_nodes

    def get_edges_for_current_nodes(current_nodes):
        # edges - глобальный список ребер
        current_node_ids = {node['data']['id'] for node in current_nodes}
        current_edges = []
        for edge in edges:
            if edge['data']['source'] in current_node_ids and edge['data']['target'] in current_node_ids:
                current_edges.append(edge)
        return current_edges

    add_clicked = int(click_add) > int(click_del) # было больше кликов по кнопке добавить
    del_clicked = int(click_add) < int(click_del)# было больше кликов по кнопке удалить
    current_nodes, deleted_nodes = get_current_and_deleted_nodes(elements)
    if add_clicked and deleted_nodes:
        # берем один удаленный узел 
        current_nodes.append(deleted_nodes.pop())
        return current_nodes + get_edges_for_current_nodes(current_nodes)
    elif del_clicked and current_nodes:
        current_nodes.pop()
        return current_nodes + get_edges_for_current_nodes(current_nodes)
    return elements


if __name__ == '__main__':
    app.run_server(debug=True)
