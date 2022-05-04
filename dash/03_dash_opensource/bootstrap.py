import dash
# компоненты bootstrap
import dash_bootstrap_components as dbc

app = dash.Dash(
    # подключение стилей bootstrap
    external_stylesheets=[dbc.themes.BOOTSTRAP], # стили хранятся в CDN
    # альтернативно можно подключить по ссылке
    # external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"]
    # добавить тэг meta можно вот так:
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)

styles = {
    "Row": {
        "background-color": "olive",
        "border": "1px solid black",
        "height": "100px"
    },
    "Col": {
        "background-color": "pink",
        "border": "1px solid black"
    }
}

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col('Col 1/3'), # .col
                dbc.Col('Col 2/3', width=6), # .col-6
                dbc.Col('Col 3/3'), # .col
            ],
            style=styles['Row']
        ),
        dbc.Row(
            [
                dbc.Col(
                    'Col 1/3', 
                    width={
                        "size": 3,
                        "offset": 1
                    }
                ), # .col-3 .offset-1
                dbc.Col('Col 2/3', width=6), # .col-6
                dbc.Col('Col 3/3'), # .col
            ],
            align="center",
            style=styles['Row']
        ),
        dbc.Row(
            [
                # если меньше md - каждая по 50%, если md+, то каждая по четверти экрана
                dbc.Col(
                    'Col 1/4', 
                    width=6, 
                    md=3, 
                    style=styles["Col"],
                    align="stretch"
                ), # .col-6 .col-md-3
                dbc.Col('Col 2/4', width=6, md=3, style=styles["Col"]), # .col-6 .col-md-3
                dbc.Col('Col 3/4', width=6, md=3, style=styles["Col"]), # .col-6 .col-md-3
                dbc.Col(
                    'Col 3/4', 
                    width=6, 
                    md=3, 
                    style=styles["Col"],
                    align="end"
                ), # .col-6 .col-md-3
            ],
            align="center",
            style=styles['Row']
        ),
        # fluid=True,
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
