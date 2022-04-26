from dash import Dash, dcc, html, Input, Output, State

app = Dash(
    __name__,
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
)

app.layout = html.Div(
    [
        dcc.Input(id='input-1-state', type='text', placeholder="Введите что-нибудь"),
        html.Br(),
        dcc.Input(id='input-2-state', type='text', placeholder="Введите что-нибудь"),
        html.Br(),
        html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
        html.Br(),
        html.Div(id='output-state'),
        insta_div := html.Div()
    ]
)

@app.callback(
    Output(insta_div, 'children'),
    Input('input-1-state', 'value'), # изменение текста в этом поле триггерит обратный вызов
    Input('input-2-state', 'value') # изменение текста в этом поле триггерит обратный вызов
)
def _(input_1, input_2):
    return f'''
    Меняется моментально: 
    Значение поля 1: {input_1}.\n
    Значение поля 2: {input_2}.\n
    '''

@app.callback(
    Output('output-state', 'children'),
    Input('submit-button-state', 'n_clicks'), # свойство у объектов HTML
    State('input-1-state', 'value'), # изменение текста в этом поле не триггер обратный вызов
    State('input-2-state', 'value') # изменение текста в этом поле не триггер обратный вызов
)
def _(n_clicks, input_1, input_2):
    return f'''
    Меняется после нажатия 
    Кнопка была нажата {n_clicks} раз.\n
    Значение поля 1: {input_1}.\n
    Значение поля 2: {input_2}.\n
    '''

if __name__ == '__main__':
    app.run_server(debug=True)
