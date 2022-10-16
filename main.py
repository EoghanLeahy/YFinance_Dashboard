# Import libraries and dependencies
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import plotly.express as px
import yfinance as yf

# Instantiate our App and incorporate BOOTSTRAP theme stylesheet
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])

# Build the layout to define what will be displayed on the page
app.layout = dbc.Container([
    dbc.Row([
       dbc.Col([
           html.H1("Stock Info")
       ], width=8)
    ], justify="center"),

    dbc.Row([
        dbc.Col([
            html.Label('Ticker to fetch:'),
            dcc.Input(id="my-ticker", value='.ixn', type="text", debounce=True),

        ], width=6),
    ]),


    dbc.Row([
        dbc.Col([
            dcc.Graph(id='graph-output',figure={})
        ], width=12)
    ]),
])

# callback is used to create app interactivity
@app.callback(
    dash.Output(component_id="graph-output", component_property="figure"),
    dash.Input(component_id="my-ticker", component_property="value"),
    prevent_initial_call=True)

def update_figure(ticker):
    # Stock data
    stock = yf.Ticker(ticker)
    # Set the timeframe you are interested in viewing.
    stock_historical = stock.history(start="2020-01-2", end="2022-10-15", interval="1d")
    # Create a new DataFrame called signals, keeping only the 'Date' & 'Close' columns.
    stock_df = stock_historical.drop(columns=['Dividends', 'Stock Splits'])
    stock_df = stock_df.reset_index()
    # Build the scatter plot
    fig = px.scatter(data_frame=stock_df, x="Date", y="Close", size="Volume")
    return fig

# Run the App
if __name__ == '__main__':
    app.run_server(port=8001)
