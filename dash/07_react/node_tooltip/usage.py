import example_component
import dash
import dash_cytoscape as cyto
from dash import html, dcc, Input, Output, State
import json
import numpy as np
from dash.exceptions import PreventUpdate
from datetime import datetime

app = dash.Dash(__name__)

positions = {
    'one': (50, 20),
    'two': (200, 250)
}

last_seen = None

app.layout = html.Div([
    cyto.Cytoscape(
        id='cyto',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '400px'},
        elements=[
            # The nodes elements
            {'data': {'id': 'one', 'label': 'Node 1'},
             'position': {'x': positions['one'][0], 'y': positions['one'][1]}},
            {'data': {'id': 'two', 'label': 'Node 2'},
             'position': {'x': positions['two'][0], 'y': positions['two'][1]}},

            # The edge elements
            {'data': {'source': 'one', 'target': 'two', 'label': 'Node 1 to 2'}}
        ]
    ),
    example_component.NodeTooltip(
        children="",
        id="my_tooltip",
        visible=True,
        offsetX=20,
        offsetY=20,
        top=0,
        left=0,
        lastNodeLeft=None,
        lastNodeTop=None,
        maxDistance=30
    ),
    example_component.NodeTooltip(
        children="",
        id="current_cursor_pos",
        visible=True,
        lastNodeLeft=None,
        lastNodeTop=None,
    ),

    html.Span(id="output"),
    html.Span(id="output2"),
    dcc.Store(id='last_seen_pos'),
    dcc.Store(id='last_seen_id', data=None)
])

# @app.callback(
#     Output('my_tooltip', 'children'),
#     Input('my_tooltip', 'top'),
#     Input('my_tooltip', 'left'),
#     State('my_tooltip', 'children'),
# )
# def display_output(top, left, children):
#     if last_seen is None:
#         return children
#     ts, ls = last_seen
#     if ((top - ts)**2 + (left - ls) ** 2) ** (0.5) <= 1:
#         return children
#     else:
#         return ''


@app.callback(
    Output('my_tooltip', 'lastNodeTop'),
    Output('my_tooltip', 'lastNodeLeft'),
    Output('my_tooltip', 'visible'),
    Output('my_tooltip', 'children'),
    Input("cyto", "mouseoverNodeData"),
    State('current_cursor_pos', 'top'),
    State('current_cursor_pos', 'left'),
)
def displayTapNodeData(data, top, left):
    if data:
        print(f'{datetime.now()} updated!')
        text = "You recently hovered over the city: " + data['label']
        return top, left, True, text
    raise PreventUpdate

@app.callback(
    Output("cyto", "mouseoverNodeData"),
    Input('current_cursor_pos', 'top'),
    Input('current_cursor_pos', 'left'),
    State('my_tooltip', 'lastNodeTop'),
    State('my_tooltip', 'lastNodeLeft'),
)
def _(top, left, lastTop, lastLeft):
    print(top, left, lastTop, lastLeft)
    if lastTop is not None:
        d = ((lastTop-top) ** 2  + (lastLeft-left) ** 2) ** 0.5
        if d >= 5:
            return None

    # raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
