import json

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


app = Dash(
    __name__, 
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
)

df = pd.DataFrame({
    "x": [1,2,1,2],
    "y": [1,2,3,4],
    "customdata": [1,2,3,4],
    "fruit": ["apple", "apple", "orange", "orange"]
})
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

fig = px.scatter(df, x="x", y="y", color="fruit", custom_data=["customdata"])
fig.update_layout(clickmode='event+select') # позволяет выделить точки с зажатым shift
fig.update_traces(marker_size=20)

app.layout = html.Div([
    dcc.Graph(
        id='basic-interactions',
        figure=fig
    ),
    html.Div(
        [
            html.Div(html.Pre(id='hover-data', style=styles['pre']), className='three columns'),
            html.Div(html.Pre(id='click-data', style=styles['pre']), className='three columns'),
            html.Div(html.Pre(id='selected-data', style=styles['pre']), className='three columns'),
            html.Div(html.Pre(id='relayout-data', style=styles['pre']), className='three columns'),
        ], 
        className='Row'
    )

])

@app.callback(
    Output('hover-data', 'children'),
    Input('basic-interactions', 'hoverData'))
# срабатывает при наведении курсора на точку
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)

@app.callback(
    Output('click-data', 'children'),
    Input('basic-interactions', 'clickData'))
# срабатывает при клике на точку
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


@app.callback(
    Output('selected-data', 'children'),
    Input('basic-interactions', 'selectedData'))
# срабатывает при выделении множества точек
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)


@app.callback(
    Output('relayout-data', 'children'),
    Input('basic-interactions', 'relayoutData'))
# срабатывает при масштабировании или нажатии на легенду
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)



if __name__ == '__main__':
    app.run_server(debug=True)
