from dash import Dash, dcc, html, Input, Output, State
import json
import numpy as np
import time
import plotly.express as px
import pandas as pd
def create_table(df):
    header = html.Thead(
        html.Tr([html.Th(col) for col in df.columns])
    )
    body = html.Tbody([
        html.Tr([
            html.Td(df.iloc[i][col]) for col in df.columns
        ]) for i in range(len(df))
    ])
    return header, body

app = Dash(
    __name__,
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
)

app.layout = html.Div(
    [
        dcc.Dropdown(id='dropdown', options=["Normal", "Uniform"]),
        dcc.Graph(id='graph'),
        html.Table(id='table'),

        # dcc.Store для хранения промежуточных значений
        dcc.Store(id='intermediate-value')
    ]
)

@app.callback(
    Output('intermediate-value', 'data'),
    Input('dropdown', 'value')
)
def preprocessing(value):
    print("Sleeping...")
    time.sleep(3)
    if value == "Normal":
        data = np.random.random(size=(100, 2)).tolist()
    else:
        data = np.random.uniform(10, 20, size=(100, 2)).tolist()
    return json.dumps(data)

@app.callback(
    Output('graph', 'figure'),
    Input('intermediate-value', 'data')
)
def update_graph(data):
    data_df = pd.DataFrame(json.loads(data), columns=['x', 'y'])
    return px.scatter(data_df, x="x", y="y")

@app.callback(
    Output('table', 'children'),
    Input('intermediate-value', 'data')
)
def update_table(data):
    data_df = pd.DataFrame(json.loads(data), columns=['x', 'y'])
    return create_table(data_df)

if __name__ == '__main__':
    app.run_server(debug=True)    
