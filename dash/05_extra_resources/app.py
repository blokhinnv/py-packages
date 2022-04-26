import plotly.express as px
from dash import Dash, dcc, Input, Output, html
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
app = Dash(
    __name__, 
    # external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'],
    assets_folder="assets"
)
app.layout = html.Div(
    [
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            df['year'].min(),
            df['year'].max(),
            step=None,
            value=df['year'].min(),
            marks={str(year): str(year) for year in df['year'].unique()},
            id='year-slider'
        ),
        html.H2('Горизонтальная ось:'),
        dcc.RadioItems(
            ['Linear', 'Log'],
            value='Log',
            id='xaxis-type'
        )
    ]
)

# callback может принимать несколько входных параметров
@app.callback(
    # модифицируем фигуру на основе
    Output('graph-with-slider', 'figure'),
    # значения слайдера и селектора
    Input('year-slider', 'value'),
    Input('xaxis-type', 'value')
)
def _(selected_year, xaxis_type):
    # функция обратного вызова не должна модифицировать глобальные переменные
    filtered_df = df[df.year == selected_year]
    fig = px.scatter(
        filtered_df, 
        x="gdpPercap", 
        y="lifeExp",
        size="pop", 
        color="continent", 
        hover_name="country",
        log_x=(xaxis_type=='Log'), 
        size_max=55
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
