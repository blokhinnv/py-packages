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

def create_table(df):
    header = html.Thead(
        html.Tr([html.Th(col) for col in df.columns])
    )
    body = html.Tbody([
        html.Tr([
            html.Td(df.iloc[i][col]) for col in df.columns
        ]) for i in range(len(df))
    ])
    return html.Table([header, body])

markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''

app = Dash(__name__)
app.layout = html.Div(
    children=[
        html.H1(
            children='Красивая табличка',
        ),
        create_table(df),
        # dash поддерживает работу с языком Markdown
        dcc.Markdown(markdown_text)
])
if __name__ == '__main__':
    app.run_server(debug=True)
