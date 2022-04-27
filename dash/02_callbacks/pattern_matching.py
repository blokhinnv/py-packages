from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL

app = Dash(
    __name__, 
    suppress_callback_exceptions=True
)

app.layout = html.Div([
    html.Button("Add Filter", id="add-filter", n_clicks=0),
    html.Div(id='dropdown-container', children=[]),
    html.Hr(),
    html.Details(
        [html.Div(id='dropdown-container-output')]
    )
    
])

@app.callback(
    # дополняем контейнер
    Output('dropdown-container', 'children'),
    # триггер - нажатие на кнопку
    Input('add-filter', 'n_clicks'),
    # используем State для доступа к имеющимся эл-там в контейнере
    State('dropdown-container', 'children')
)
def display_dropdowns(n_clicks, children):
    new_dropdown = dcc.Dropdown(
        ['NYC', 'MTL', 'LA', 'TOKYO'],
        # в новых версиях ID компонента может быть словарем
        id={
            'type': 'filter-dropdown',
            'index': n_clicks
        }
    )
    new_div = html.Div(
        id={
            "type": "dynamic-filter-output",
            "index": n_clicks
        }
    )
    new_element = html.Div([new_dropdown, new_div])
    children.append(new_element)
    return children

@app.callback(
    Output('dropdown-container-output', 'children'),
    # любой компонент, у которого ID имеет тип filter-dropdown и любое значение index
    # в функцию передадутся все такие компоненты
    # важно: таким образом можно матчить только ID
    Input({'type': 'filter-dropdown', 'index': ALL}, 'value')
)
def display_output_all(values):
    return html.Div([
        html.Div('Dropdown {} = {}'.format(i + 1, value))
        for (i, value) in enumerate(values)
    ])

@app.callback(
    # 3.Обновить компонент с id type = filter-dropdown
    # а index совпадается с index компонента из п.1.
    Output({'type': 'dynamic-filter-output', 'index': MATCH}, 'children'),
    # 1. вызвать функцию, когда значение любого компонента 
    # с id type = filter-dropdown меняется
    # в функцию передастся только один компонент
    Input({'type': 'filter-dropdown', 'index': MATCH}, 'value'),
    # 2. Найти ID компонента, у которого id type = filter-dropdown и
    # index совпадается с index компонента из п.1.
    State({'type': 'filter-dropdown', 'index': MATCH}, 'id'),
)
def display_output_match(value, id):
    return html.Div('Dropdown {} = {}'.format(id['index'], value))

if __name__ == '__main__':
    app.run_server(debug=True)
