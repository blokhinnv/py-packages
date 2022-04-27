from dash import Dash, html, dcc, Input, Output
from dash_canvas import DashCanvas
import networkx as nx
import matplotlib.pyplot as plt
from dash_canvas.utils import array_to_data_url

G = nx.karate_club_graph()
nx.draw(G, pos=nx.spring_layout(G, seed=42))
plt.savefig("03_dash_opensource/karate.jpg", dpi=300, bbox_inches='tight')
img = plt.imread("03_dash_opensource/karate.jpg")
image_content=array_to_data_url(img)

app = Dash(
    __name__,
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
)
app.layout = html.Div(
    [
        html.Div(
            children=[
                html.H3('На этом изображении можно рисовать!'),
                DashCanvas(
                    id="my-canvas",
                    tool='pencil', # line
                    width=1000,
                    lineColor="blue",
                    image_content=image_content
                ),
                dcc.Slider(
                    id='bg-width-slider',
                    min=2,
                    max=40,
                    step=1,
                    value=5
                ),
            ],
            className="six columns"
        ),
    ]
)

@app.callback(
    Output('my-canvas', 'lineWidth'),
    Input('bg-width-slider', 'value')
)
def _(value):
    return value

if __name__ == '__main__':
    app.run_server(debug=True)
