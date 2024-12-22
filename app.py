import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from utils import get_weather_data_sheet
import re

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Погода в городах"),
    html.Div([
        html.Label("Введите координаты городов (например, (52, 64), (34, 77))...:"),
        dcc.Input(id='coords-input', type='text', value='(52, 64), (34, 77)', style={'width': '50%'}),
        html.Button('Получить данные', id='submit-button'),
    ]),
    html.Div([
        html.Label("Выберите параметр:"),
        dcc.Dropdown(id='param-dropdown',
                     options=[{'label': i, 'value': i} for i in
                              ['temperature', 'wind_speed', 'precip_prob', 'humidities']],
                     value='temperature'),
    ]),
    html.Div([
        html.Label("Выберите количество дней:"),
        dcc.Slider(id='days-slider', min=1, max=5, step=1, value=5, marks={i: str(i) for i in range(1, 6)}),
    ]),
    dcc.Graph(id='weather-graph'),
])


@app.callback(
    Output('weather-graph', 'figure'),
    Input('submit-button', 'n_clicks'),
    Input('coords-input', 'value'),
    Input('param-dropdown', 'value'),
    Input('days-slider', 'value')
)
def update_graph(n_clicks, coords_str, param, num_days):
    if n_clicks is None:
        return {}

    try:
        cords_list = [(int(x), int(y)) for x, y in re.findall(r'\((\d+), (\d+)\)', coords_str)]
        if not isinstance(cords_list, tuple) and not all(isinstance(coord, tuple) for coord in cords_list):

            raise ValueError("Неверный формат координат")

    except (ValueError, SyntaxError, NameError):
        return {'data': [{'type': 'scatter', 'x': [], 'y': []}], 'layout': {'title': 'Ошибка ввода координат'}}

    combined_df = get_weather_data_sheet(cords_list, num_days)

    fig = px.line(combined_df, x="date", y=param, color="coordinates", title=f"Погода: {param}")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
