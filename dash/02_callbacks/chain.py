import plotly.express as px
from dash import Dash, dcc, Input, Output, html
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
app = Dash(__name__, external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = html.Div(
    [
        dcc.Graph(id='graph-with-slider'),
        html.H2("Континент:"),
        dcc.RadioItems(
            df['continent'].unique().tolist(),
            'Asia',
            id='continent-radio',
        ),
        html.H2("Страна:"),
        dcc.RadioItems(
            df[df['continent']=='Asia']['country'].unique().tolist(),
            value='Afghanistan',
            id='country-radio',
        ),
    ]
)


@app.callback(
    Output('country-radio', 'options'),
    Output('country-radio', 'value'),
    Input('continent-radio', 'value')
)
def update_country_radio(continent_value):
    options = df[df['continent']==continent_value]['country'].unique()
    option = options[0]
    return options, option

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('continent-radio', 'value'),
    Input('country-radio', 'value')
)
def update_fig(continent, country):
    filtered_df = df[(df['continent']==continent) & (df['country']==country)]
    fig = px.scatter(
        filtered_df, 
        x="year", 
        y="lifeExp",
        size="pop", 
        size_max=55
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
