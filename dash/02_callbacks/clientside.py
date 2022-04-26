from dash import Dash, dcc, html, Input, Output
import pandas as pd
import json
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

app = Dash(
    __name__, 
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
)
app.layout = html.Div(
    [
        dcc.Graph(id='clientside-graph'),
        # используем store для хранения данных для графиков
        dcc.Store(
            id='clientside-figure-store',
            data=[
                {
                    "x": df[df['country'] == 'Canada']['year'],
                    "y": df[df['country'] == 'Canada']['pop'],
                }
            ]
        ),
        "Индикатор",
        dcc.Dropdown(
            {
                'pop' : 'Population', 
                'lifeExp': 'Life Expectancy', 
                'gdpPercap': 'GDP per Capita'
            },
            'pop',
            id='clientside-graph-indicator'
        ),
        "Страна", 
        dcc.Dropdown(df["country"].unique(), 'Canada', id='clientside-graph-country'),
        "Масштаб осей",
        dcc.RadioItems(
            ['linear', 'log'],
            'linear',
            id='clientside-graph-scale'
        ),
        html.Hr(),
        html.Details(
            [
                html.Summary('Contents of figure storage'),
                dcc.Markdown(
                    id='clientside-figure-json'
                )
            ]
        )
    ]
)

# два обычных обратных вызова - для заполнения store ...
@app.callback(
    Output('clientside-figure-store', 'data'),
    Input('clientside-graph-indicator', 'value'),
    Input('clientside-graph-country', 'value')
)
def update_store_data(indicator, country):
    dff = df[df['country'] == country]
    return [{
        'x': dff['year'],
        'y': dff[indicator],
        'mode': 'markers'
    }]

# ... и для обновления тэга details
@app.callback(
    Output('clientside-figure-json', 'children'),
    Input('clientside-figure-store', 'data')
)
def generated_figure_json(data):
    return '```\n'+json.dumps(data, indent=2)+'\n```'

# функция обратного вызова на клиенской стороне
app.clientside_callback(
    # сама функция на JS в виде строки
    """
    function(data, scale) {
        return {
            'data': data,
            'layout': {
                 'yaxis': {'type': scale}
             }
        }
    }
    """,
    # обычные Input и Output
    Output('clientside-graph', 'figure'),
    Input('clientside-figure-store', 'data'),
    Input('clientside-graph-scale', 'value')
)

if __name__ == '__main__':
    app.run_server(debug=True)
