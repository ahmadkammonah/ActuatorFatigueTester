import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output, callback
import mainTester

fileName = mainTester.fileName  # gui.rawDataFileName
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

    # Create a figure with two subplots
    fig = make_subplots(rows=2, cols=1)

    # Add Angle trace to the first subplot
    fig.add_trace(
        go.Scatter(x=time_column, y=angle_column, mode='lines', name='Angle'),
        row=1, col=1
    )

    # Add Voltage trace to the second subplot
    fig.add_trace(
        go.Scatter(x=time_column, y=voltage_column, mode='lines', name='Voltage'),
        row=2, col=1
    )

    # Add x-axis and y-axis titles to the first subplot
    fig.update_xaxes(title_text="Time", row=1, col=1)
    fig.update_yaxes(title_text="Angle", row=1, col=1)

    # Add x-axis and y-axis titles to the second subplot
    fig.update_xaxes(title_text="Time", row=2, col=1)
    fig.update_yaxes(title_text="Voltage", row=2, col=1)

    # Update layout with title
    fig.update_layout(title='Actuator Test: ' + fileName)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
