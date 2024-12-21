import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd


data = {
    'location': ['Место A', 'Место B', 'Место C'],
    'time': ['2024-10-27 12:00', '2024-10-27 12:00', '2024-10-27 12:00'],
    'temperature': [20, 25, 18],
    'wind_speed': [10, 5, 15],
    'precipitation': [0.1, 0, 0.5]
}
df = pd.DataFrame(data)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Прогноз погоды"),
    dcc.Dropdown(
        id='location-dropdown',
        options=[{'label': loc, 'value': loc} for loc in df['location'].unique()],
        value=df['location'].iloc[0]
    ),
    dcc.Graph(id='weather-graph'),
])

@app.callback(
    dash.Output('weather-graph', 'figure'),
    dash.Input('location-dropdown', 'value')
)
def update_graph(selected_location):
    filtered_df = df[df['location'] == selected_location]
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=filtered_df['time'], y=filtered_df['temperature'], name='Температура', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=filtered_df['time'], y=filtered_df['wind_speed'], name='Скорость ветра', mode='lines+markers'))
    fig.add_trace(go.Bar(x=filtered_df['time'], y=filtered_df['precipitation'], name='Осадки'))

    fig.update_layout(title=f'Прогноз погоды для {selected_location}', xaxis_title='Время', yaxis_title='Значение')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
