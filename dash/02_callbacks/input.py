from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

# создаем простой макет
app.layout = html.Div([
    html.H2("Измените значение в текстовом поле, чтобы увидеть обратные вызовы в действии!"),
    html.Div([
        dcc.Input(id='my-input', value='Начальное значение', type='text')
    ]),
    html.Br(),
    html.Div(id='my-output'),

])

# описываем функцию обратного вызова
# входные и выходные параметры функции описываются при помощи декоратора
# когда значение входного параметра меняется, задекорированная функция вызовется автоматически
# при запуске приложения все функции обратного вызова будут вызваны по одному разу
@app.callback(
    # изменяем значение children у компонента с ID my-output ...
    Output(component_id='my-output', component_property='children'),
    # ... на основе значения value у компонента c ID my-input
    Input(component_id='my-input', component_property='value') 
)
def update_output_div(input_value):
    return f'Output: {input_value}'

if __name__ == '__main__':
    app.run_server(debug=True)
