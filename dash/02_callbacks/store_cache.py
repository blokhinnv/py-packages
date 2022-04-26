from dash import Dash, dcc, html, Input, Output, State
import json
import numpy as np
import time
import plotly.express as px
import pandas as pd
from flask_caching import Cache

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
# нужна дополнительная библиотека flask_caching
# создаем специальный объект для кэширования на диске
server = app.server
CACHE_CONFIG = {
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': '02_callbacks/.'
}
cache = Cache()
cache.init_app(app.server, config=CACHE_CONFIG)

app.layout = html.Div(
    [
        dcc.Dropdown(id='dropdown', options=["Normal", "Uniform"], value="Normal"),
        dcc.Graph(id='graph'),
        html.Table(id='table'),
        # dcc.Store для хранения промежуточных значений
        dcc.Store(id='intermediate-value')
    ]
)

# делаем препроцессинг и сохраняем результат в кэш
# который доступен всем процессам в любое время
@cache.memoize()
def global_store(value):
    print(f"Computing {value}...")
    time.sleep(3)
    if value == "Normal":
        data = np.random.random(size=(100, 2)).tolist()
    else:
        data = np.random.uniform(10, 20, size=(100, 2)).tolist()
    return pd.DataFrame(data, columns=['x', 'y'])

# тригерим вычисления и сохранение в кэш
# подаем сигнал, когда расчеты закончены
@app.callback(
    Output('intermediate-value', 'data'),
    Input('dropdown', 'value')
)
def preprocessing(value):
    global_store(value)
    return value

# после этого тригерятся остальные вызовы
# данные для визуализаций уже готовы после вызова preprocessing
# и лежат в global_store
@app.callback(
    Output('graph', 'figure'),
    Input('intermediate-value', 'data')
)
def update_graph(value):
    data_df = global_store(value)
    return px.scatter(data_df, x="x", y="y")

@app.callback(
    Output('table', 'children'),
    Input('intermediate-value', 'data')
)
def update_table(value):
    data_df = global_store(value)
    return create_table(data_df)

if __name__ == '__main__':
    app.run_server(debug=True)    
