from dash import html, dcc, Dash, callback, callback_context, Input, Output, State

import network
import network_generator

from network_graph import Network_graph


# Grafische Oberfläche
parameter_layout = [
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
    Output('confirm_output', 'children'),
    Input('generate_Network', 'n_clicks'),
    State('input_Network-participant', 'value'),
    State('anteil_Bots', 'value'),
    State('turbulence_factor', 'value')
)
def button_generate_network(n_clicks, n_networkparticipants, n_bots, turbulence_factor):
    net = network.Network(turbulence_factor=turbulence_factor)
    network_generator.generate_new_network(net, "", n_nodes=int(n_networkparticipants))

    Network_graph.network_layout()

    return f"Netzwerk wurde erstellt"
