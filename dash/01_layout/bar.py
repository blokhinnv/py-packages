from dash import (Dash, 
                  html, # компоненты для HTML тэгов
                  dcc) # высокоуровневые интерактивные компоненты с применением CSS и JS
import plotly.express as px
import pandas as pd

# пример для работы
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app = Dash(__name__)
# макет страницы
app.layout = html.Div(
    # children - всегда первый атрибут тэга
    children=[
        # классы для тэгов HTML имеют
        # именованные аргументы для всех свойств тэгов
        # например, style
        html.H1(
            children='Hello Dash!!',
            # style можно передавать в виде словаря, а не строки (как в HTML)
            style={
                'textAlign': 'center', # названия свойств в стиле camelCase, это отличается от css
                'color': colors['text']
            }
        ),
        html.Div(
            children='''Dash: A web application framework for your data.''',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        # dcc.Graph - это компонент для отрисовки фигур plotly
        dcc.Graph(
            id='example-graph',
            figure=fig
        )
])
if __name__ == '__main__':
    # по умолчанию Dash автоматически обновит браузер,
    # когда код будет изменен.
    # это поведение можно изменить, вызвав app.run_server(dev_tools_hot_reload=False)
    app.run_server(debug=True)
