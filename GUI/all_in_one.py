from dash import html, dcc, Dash, Input, Output, callback, callback_context, State

import network
import network_generator

import plotly.graph_objs as go
import networkx as nx


import network_converter

# Callback-Funktion zum Aktualisieren des Diagramms basierend auf Benutzereingaben

# Grafische Oberfläche
parameter_layout = [
    html.Div(children=[
                          dcc.Interval(id='interval_net_graph', interval=9999999, n_intervals=0),
                          dcc.Input(
                                id='node_input',
                                type='number',
                                value=10,
                                min=1,
                                max=100,
                                step=1,
                            ),
                          html.Button('Update Network', id='update_button', n_clicks=0),
                        dcc.Graph(
                            id='network_graph',
                            config={'displayModeBar': False},
                        ),
    html.H1('Parameter input', style={'textAlign': 'center'}),
    html.Hr(),
    html.Div('Network Participants'),
    dcc.Input(id='input_Network-participant', value=0, type='number',
              style={'width': '300px', 'height': '30px', 'margin-bottom': '15px'},
              placeholder='Enter the number of Network Participants'),
    html.Br(),
    html.Div('Bots'),
    dcc.Input(id='anteil_Bots', type='number', value=0,
              style={'width': '300px', 'height': '30px', 'margin-bottom': '15px'},
              placeholder='Enter the number of Bots'),
    html.Br(),
    html.Div('Influencer'),
    dcc.Input(id='anteil_Influencer', value=0, type='number',
              style={'width': '300px', 'height': '30px', 'margin-bottom': '15px'},
              placeholder='Enter the number of Influencers'),
    html.Div('Turbulenz-Faktor des Netzwerks'),
    dcc.Input(id='turbulence_factor', type='number', value=0.5, min=0, max=1, step=0.01,
              style={'width': '300px', 'height': '30px', 'margin-bottom': '15px'},
              placeholder='Turbulenz Faktor'),
    html.Br(),
    html.H5('Alternative: Put in your own Network File'),

    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(
        style={'textAlign': 'center', 'marginTop': '50px'},
        children=[
            html.Button('Generate Network', id='generate_Network', n_clicks=0,
                        style={'width': '200px', 'height': '50px'}),
            html.Div(id="confirm_output", children=" ")
        ],
    ),
]

# Logische Verarbeitung
@callback(
    Output('network_cache', 'data'),
    Input('generate_Network', 'n_clicks'),
    State('input_Network-participant', 'value'),
    State('anteil_Bots', 'value'),
    State('turbulence_factor', 'value')
)
def button_generate_network(n_clicks, n_networkparticipants, n_bots, turbulence_factor):
    network_graph = network_generator.generate_new_network("", n_nodes=int(n_networkparticipants))
    return network_graph

########## Anderen Trigger finden



