import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output, callback

fileName = "Unit0012_21Jan2024"  # gui.rawDataFileName
file_path = f"./Data/{fileName}.csv"  # gui.rawDataFile_path

app = Dash(__name__)

# Layout
app.layout = html.Div([
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1 * 5000,  # in milliseconds
        n_intervals=0
    )
])


# Callback for live updating
@callback(Output('live-update-graph', 'figure'),
          [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    df = pd.read_csv(file_path)
    df = df.tail(390000)

    time_column = df['Time']
    angle_column = df['Angle']
    voltage_column = df['Voltage']

    # Create the graph
    fig = go.Figure(data=[
        go.Scatter(x=time_column, y=angle_column, mode='lines', name='Angle'),
        go.Scatter(x=time_column, y=voltage_column, mode='lines', name='Voltage')
    ])

    fig.update_layout(title='Actuator Test: ' + fileName)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
