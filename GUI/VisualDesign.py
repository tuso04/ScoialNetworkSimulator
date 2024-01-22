import dash_bootstrap_components as dbc
import networkx as nx
from dash import Dash, dcc, html, Input, Output, State, dash_table
import plotly.graph_objs as go
import network_converter
import network_generator
import random
import pandas as pd

app = Dash(__name__)
app.title = "Networksimulation"

app.layout = dbc.Container([

    html.H1('Parameter input', style={'textAlign': 'center'}),

])



if __name__ == '__main__':
    app.run_server(debug=True)