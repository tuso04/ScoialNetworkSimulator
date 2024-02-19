import json

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, dcc, html, Output, State, Input
from dash import dash_table
from sklearn.linear_model import LinearRegression
import numpy as np

import network_simulator

# Beispiel Daten Tabelle
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Beispiel-Daten für das Balkendiagramm
x = np.arange(1, 100)
y = np.random.randint(1, 100, size=100)

# Für inneren Balken
inner_y = np.random.randint(1, 50, size=100)  # Zufällige Werte für die Höhe des inneren Balkens
inner_y2 = np.random.randint(1, 50, size=100)  # Zufällige Werte für die Höhe des inneren Balkens der zweiten Gruppe

# Generiere zufällige Daten für die unabhängige und abhängige Variable
np.random.seed(0)
Xr = np.random.rand(100, 1) * 10  # Unabhängige Variable
yr = 2 * Xr + np.random.randn(100, 1) * 2  # Abhängige Variable (mit Rauschen)

# Führe die lineare Regression durch
model = LinearRegression()
model.fit(Xr, yr)

# Vorhersagen mit dem trainierten Modell
yr_pred = model.predict(Xr)

# Extrahieren der Daten aus den ersten beiden Zeilen des DataFrame
first_two_rows = df.head(2).to_dict('records')

# Hinzufügen der Spaltenüberschriften als erste Zeile
rows = [{'Index': 'Nachricht', **first_two_rows[0]},
        {'Index': 'Gegennachricht', **first_two_rows[1]}]

app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH])
app.title = "Networksimulation"

# Erstellen der Optionen für das Dropdown-Menü
options = [{'label': str(i), 'value': i} for i in range(0, 101)]

card_left = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Höchste Kaufwahrscheinlichkeit", className="card-title", style={'textAlign': 'center'}, ),
                html.H3(
                    "500",
                    className="card-text", style={'text-align': 'center'},
                ),
            ]
        ),

    ],
    color="primary",  # https://bootswatch.com/default/ for more card colors
    inverse=True,  # change color of text (black or white)
    outline=False,  # True = remove the block colors from the background and header
)

card_leftmid = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Geringste Kaufwahrscheinlichkeit", className="card-title", style={'textAlign': 'center'}, ),
                html.H3(
                    "500",
                    className="card-text", style={'text-align': 'center'},
                ),
            ]
        ),

    ],
    color="primary",  # https://bootswatch.com/default/ for more card colors
    inverse=True,  # change color of text (black or white)
    outline=False,  # True = remove the block colors from the background and header
)

card_mid = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Höchste Anzahl an Nachbarn", className="card-title", style={'textAlign': 'center'}, ),
                html.H3(
                    "500",
                    className="card-text", style={'text-align': 'center'},
                ),
            ]
        ),

    ],
    color="primary",  # https://bootswatch.com/default/ for more card colors
    inverse=True,  # change color of text (black or white)
    outline=False,  # True = remove the block colors from the background and header
)

card_rightmid = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Höchste Glaubwürdigkeit", className="card-title", style={'textAlign': 'center'}, ),
                html.H3(
                    "500",
                    className="card-text", style={'text-align': 'center'},
                ),
            ]
        ),

    ],
    color="primary",  # https://bootswatch.com/default/ for more card colors
    inverse=True,  # change color of text (black or white)
    outline=False,  # True = remove the block colors from the background and header
)

card_right = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Geringste Glaubwürdigkeit", className="card-title", style={'textAlign': 'center'}, ),
                html.H3(
                    "500",
                    className="card-text", style={'text-align': 'center'},
                ),
            ]
        ),

    ],
    color="primary",  # https://bootswatch.com/default/ for more card colors
    inverse=True,  # change color of text (black or white)
    outline=False,  # True = remove the block colors from the background and header
)

##############################################Layout####################################################################
app.layout = html.Div([

    # Cache
    dcc.Store(id="network_cache"),

    # Download
    dcc.Download(id="download_simulation_csv"),

    html.Br(),
    html.H1('Network Simulation', style={'textAlign': 'center'}),
    html.Hr(),

    dcc.Tabs([

        #############################################Tab 1 Input########################################################
        dcc.Tab(label='Parameter input', children=[
            html.Br(),
            dbc.Card(
                [
                    dbc.CardHeader(html.H4('Netzwerkparameter', style={'textAlign': 'center'})),
                    dbc.CardBody(
                        [
                            dbc.Row(className='mx-auto', style={'width': 'fit-content'},
                                    children=[
                                        dbc.Col([
                                            html.Label('Netzwerkart'),
                                            dcc.Dropdown(options=[{'label': 'SWN', 'value': 'SWN'},
                                                                  {'label': 'SFN', 'value': 'SFN'},
                                                                  {'label': 'random', 'value': 'random'}],
                                                         value='SWN', id='net_shape',
                                                         style={'width': '300px', 'height': '40px',
                                                                'margin-bottom': '30px'},
                                                         ),
                                        ], width=3),

                                        dbc.Col([
                                            html.Label('Netzwerkteilnehmer'),
                                            html.Br(),
                                            dcc.Input(id='network_participant_parameter', type='number',
                                                      value=10,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '30px'}),
                                        ], width=3),

                                        dbc.Col([
                                            html.Label('Anzahl initialer Kanten'),
                                            html.Br(),
                                            dcc.Input(id='n_init_edges', type='number', value=2, min=0, step=1,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '30px'}
                                                      ),
                                        ], width=3),

                                        dbc.Col([
                                            html.Label('Seperationswahrscheinlichkeit'),
                                            html.Br(),
                                            dcc.Input(id='sep_prob', type='number', value=0.1, min=0, max=1, step=0.01,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '30px'}),
                                        ], width=3),
                                    ]
                                    ),

                            dbc.Row(className='mx-auto', style={'width': 'fit-content'},
                                    children=[
                                        dbc.Col([
                                            html.Label('Turbulenz-Faktor des Netzwerks'),
                                            html.Br(),
                                            dcc.Input(id='turbulence_factor', type='number', value=0.5, min=0, max=1,
                                                      step=0.01,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '30px'}),
                                        ], width=4),

                                        dbc.Col([
                                            html.Label('Bots'),
                                            html.Br(),
                                            dcc.Input(id='bots_parameter', type='number', value=2, min=0, step=1,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '30px'}
                                                      ),
                                        ], width=4),

                                        dbc.Col([
                                            html.Label('Influencer'),
                                            html.Br(),
                                            dcc.Input(id='influencer_parameter', type='number', value=2, min=0, step=1,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '30px'}
                                                      ),
                                        ], width=4),
                                    ],
                                    ),
                        ]
                    ),
                ],
                style={'max-width': '1600px', 'margin': 'auto', 'background-color': '#f0f0f0'}
            ),

            html.Br(),

            dbc.Card(
                [
                    dbc.CardHeader(html.H4('Teilnehmerparameter', style={'textAlign': 'center'})),
                    dbc.CardBody(
                        [
                            dbc.Row(className='mx-auto', style={'width': 'fit-content'},
                                    children=[
                                        dbc.Col([
                                            html.Label('Schwellenwert Glaubwürdigkeit'),
                                            html.Br(),
                                            dcc.Input(id='cred_parameter', type='number', value=0.5, min=0, max=1,
                                                      step=0.01,
                                                      style={'width': '350px', 'height': '40px',
                                                             'margin-bottom': '30px', 'margin-left': 'auto',
                                                             'margin-right': 'auto'}),
                                        ], width=4),

                                        dbc.Col([
                                            html.Label('Indifferenz'),
                                            html.Br(),
                                            dcc.Input(id='indefference', type='number', value=2, min=0, step=1,
                                                      style={'width': '350px', 'height': '40px',
                                                             'margin-bottom': '30px', 'margin-left': 'auto',
                                                             'margin-right': 'auto'}
                                                      ),
                                        ], width=4),

                                        dbc.Col([
                                            html.Label('ISI Parameter'),
                                            html.Br(),
                                            dcc.Input(id='isi_parameter', type='number', value=2, min=0, step=1,
                                                      style={'width': '350px', 'height': '40px',
                                                             'margin-bottom': '30px', 'margin-left': 'auto',
                                                             'margin-right': 'auto'}
                                                      ),
                                        ], width=4),
                                    ],
                                    ),

                            dbc.Row(className='mx-auto', style={'width': 'fit-content'},
                                    children=[
                                        dbc.Col([
                                            html.Label('FI Parameter'),
                                            html.Br(),
                                            dcc.Input(id='fi_parameter', type='number', value=0.5, min=0, max=1,
                                                      step=0.01,
                                                      style={'width': '350px', 'height': '40px',
                                                             'margin-bottom': '30px', 'margin-left': 'auto',
                                                             'margin-right': 'auto'}),
                                        ], width=4),

                                        dbc.Col([
                                            html.Label('Initiale Kaufwahrscheinlichkeit'),
                                            html.Br(),
                                            dcc.Input(id='purchase_init_prob_parameter', type='number', value=2, min=0,
                                                      step=1,
                                                      style={'width': '350px', 'height': '40px',
                                                             'margin-bottom': '30px', 'margin-left': 'auto',
                                                             'margin-right': 'auto'}
                                                      ),
                                        ], width=4),

                                        dbc.Col([
                                            html.Label('Maximale Kaufwahrscheinlichkeit'),
                                            html.Br(),
                                            dcc.Input(id='purchase_prob_max_parameter', type='number', value=2, min=0,
                                                      step=1,
                                                      style={'width': '350px', 'height': '40px',
                                                             'margin-bottom': '30px', 'margin-left': 'auto',
                                                             'margin-right': 'auto'}
                                                      ),
                                        ], width=4),
                                    ],
                                    ),
                            dbc.Row(className='mx-auto', style={'width': 'fit-content'},
                                    children=[
                                        dbc.Col([
                                            html.Label('Minimale Kaufwahrscheinlichkeit'),
                                            html.Br(),
                                            dcc.Input(id='purchase_prob_min_parameter', type='number', value=0.5, min=0,
                                                      max=1,
                                                      step=0.01,
                                                      style={'width': '350px', 'height': '40px',
                                                             'margin-bottom': '30px', 'margin-left': 'auto',
                                                             'margin-right': 'auto'}),
                                        ], width=4),

                                        dbc.Col([
                                            html.Label('Positive expotenzielle Kaufwahrscheinlichkeit'),
                                            html.Br(),
                                            dcc.Input(id='purchase_expo_param_positive_parameter', type='number',
                                                      value=2, min=0, step=1,
                                                      style={'width': '350px', 'height': '40px',
                                                             'margin-bottom': '30px', 'margin-left': 'auto',
                                                             'margin-right': 'auto'}
                                                      ),
                                        ], width=4),

                                        dbc.Col([
                                            html.Label('Negative expotenzielle Kaufwahrscheinlichkeit'),
                                            html.Br(),
                                            dcc.Input(id='purchase_expo_param_negative_parameter', type='number',
                                                      value=2, min=0, step=1,
                                                      style={'width': '350px', 'height': '40px',
                                                             'margin-bottom': '30px', 'margin-left': 'auto',
                                                             'margin-right': 'auto'}
                                                      ),
                                        ], width=4),
                                    ],
                                    ),
                        ]
                    ),
                ],
                style={'max-width': '1600px', 'margin': 'auto', 'background-color': '#f0f0f0'}
            ),

            html.Br(),
            dbc.Card(
                [
                    dbc.CardHeader(html.H4('Nachrichtenparameter', style={'textAlign': 'center'})),
                    dbc.CardBody(
                        [
                            dbc.Row(className='mx-auto', align='center', style={'width': 'fit-content'},
                                    children=[
                                        dbc.Col([
                                            html.Label('Qualität der Nachricht'),
                                            dcc.Input(id='quality_parameter', type='number',
                                                      value=0.5,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '15px'}),
                                        ], width=3),

                                        dbc.Col([
                                            html.Label('Emotionalität der Nachricht'),
                                            html.Br(),
                                            dcc.Input(id='emotional_parameter', type='number',
                                                      value=0.5,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '15px'}),
                                        ], width=3),

                                        dbc.Col([
                                            html.Label('Zeitpunkt Auftritt Nachricht'),
                                            html.Br(),
                                            dcc.Input(id='time_message_parameter', type='number', value=0, min=0,
                                                      step=1,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '15px'}),
                                        ], width=3),

                                        dbc.Col([
                                            html.Label('Lebenszeit der Nachricht'),
                                            html.Br(),
                                            dcc.Input(id='lifetime_parameter', type='number', value=5,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '15px'}),
                                        ], width=3),
                                    ]
                                    ),
                            dbc.Row(className='mx-auto', align='center', style={'width': 'fit-content'},
                                    children=[
                                        dbc.Col([
                                            html.Label('Qualität Gegennachricht'),
                                            dcc.Input(id='quality_counter_parameter', type='number',
                                                      value=0.5,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '15px'}),
                                        ], width=3),

                                        dbc.Col([
                                            html.Label('Emotionalität Gegennachricht'),
                                            html.Br(),
                                            dcc.Input(id='emotional_counter_parameter', type='number',
                                                      value=0.5,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '15px'}),
                                        ], width=3),

                                        dbc.Col([
                                            html.Label('Zeitpunkt Auftritt Gegennachricht'),
                                            html.Br(),
                                            dcc.Input(id='time_counter_parameter', type='number', value=2, min=0,
                                                      step=1,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '15px'}),
                                        ], width=3),

                                        dbc.Col([
                                            html.Label('Lebenszeit Gegennachricht'),
                                            html.Br(),
                                            dcc.Input(id='lifetime_counter_parameter', type='number', value=0.1, min=0,
                                                      max=1, step=0.01,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '15px'}),
                                        ], width=3),
                                    ]
                                    ),
                        ]
                    ),
                ],
                style={'max-width': '1600px', 'margin': 'auto', 'background-color': '#f0f0f0', 'margin-left': 'auto',
                       'margin-right': 'auto'}
            ),

            html.Br(),
            dbc.Card(
                [
                    dbc.CardHeader(html.H4('Simulationsparameter', style={'textAlign': 'center'})),
                    dbc.CardBody(
                        [
                            dbc.Row(className='mx-auto text-center', style={'width': 'fit-content'},
                                    children=[
                                        dbc.Col([
                                            html.Label('Anzahl der Durchläufe'),
                                            dcc.Input(id='run_parameter', type='number',
                                                      value=3,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '15px'}),
                                        ], width=6, className="mb-3"),

                                        dbc.Col([
                                            html.Label('Schritte pro Durchlauf'),
                                            html.Br(),
                                            dcc.Input(id='steps_per_run_parameter', type='number',
                                                      value=3,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '15px'}),
                                        ], width=6, className="mb-3"),
                                    ]
                                    ),

                            dbc.Row(className='mx-auto text-center', style={'width': 'fit-content'},
                                    children=[
                                        dbc.Col([
                                            html.H5('Möchten Sie für jeden Durchlauf eine CSV Datei erstellen?'),
                                            dcc.RadioItems(
                                                id='run_csv_parameter',
                                                options=[
                                                    {'label': 'Ja', 'value': 'ja'},
                                                    {'label': 'Nein', 'value': 'nein'}
                                                ],
                                                value='nein',
                                                inline=True,
                                                labelStyle={'margin-right': '20px', 'font-size': '20px'},
                                                inputStyle={'margin-right': '5px'}
                                            )
                                        ], width=12),
                                    ]
                                    ),
                        ]
                    ),
                ],
                style={'max-width': '800px', 'margin': 'auto', 'background-color': '#f0f0f0'}
            ),

            html.Br(),
            html.H5('Alternative: Put in your own Network File', style={'textAlign': 'center'}),
            html.Br(),
            html.Div(
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    style={
                        'width': '400px',
                        'height': '65px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px',
                        'position': 'absolute',
                        'left': '50%',
                        'top': '50%',
                        'transform': 'translate(-50%, -50%)'
                    },
                    multiple=True
                ),
                style={'position': 'relative'}
            ),
            html.Br(),
            html.Div(
                style={'textAlign': 'center', 'marginTop': '30px'},
                children=[
                    html.Button('Starte Simulation', id='generate_Network', n_clicks=0,
                                style={'width': '200px', 'height': '50px'}),
                ],
            ),
            html.Div(children=[
                dcc.Interval(id='interval_net_graph', interval=9999999, n_intervals=0),
                dcc.Graph(
                    id='network_graph',
                    config={'displayModeBar': False},
                    # style={'height': 400}
                ),
            ]),
            html.Div(
                style={'textAlign': 'center', 'marginTop': '10px'},
                children=[
                    html.Button('Show Network', id='show_Network', n_clicks=0,
                                style={'width': '200px', 'height': '50px'}),
                ],
            ),
            html.Div(
                style={'textAlign': 'center', 'marginTop': '10px'},
                children=[
                    html.Button("Download CSV", id="btn_csv", style={'width': '200px', 'height': '50px'}),
                    dcc.Download(id="download_csv"),
                ]
            )

        ]),

        #############################################Tab 2 Auswertung##################################################
        dcc.Tab(label='Auswertung', children=[
            html.Br(),
            html.H4('Die ersten 100 Knoten eines Netzwerkes', style={'textAlign': 'center'}),
            html.Label('Durchlauf:', style={'margin-left': '6px', 'font-size': '20px'}),
            dcc.Dropdown(
                id='step-number-dropdown',
                options=options,
                value=0,
                style={'width': '200px', 'height': '30px', 'margin-left': '2px'},
            ),
            # Tabelle mit den ersten 100 ID eines Durchlaufs
            dash_table.DataTable(
                id='Table100',
                columns=[
                    {'name': 'ID', 'id': 'ID'},
                    {'name': 'Turbulenzfaktor', 'id': 'Turbulenzfaktor'},
                    {'name': 'Kaufwahrscheinlichkeit', 'id': 'Kaufwahrscheinlichkeit'},
                    {'name': 'ID', 'id': 'ID'},
                    {'name': 'Turbulenzfaktor', 'id': 'Turbulenzfaktor'},
                    {'name': 'Kaufwahrscheinlichkeit', 'id': 'Kaufwahrscheinlichkeit'},
                    {'name': 'Gleichgültigkeit', 'id': 'Gleichgültigkeit'},
                ],
                data=df.to_dict('records'), page_size=10, sort_action='native', style_table={'overflowX': 'auto'}),

            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5('Gesamtkaufwahrscheinlichkeit aller Durchläufe:',
                                    style={'margin-left': '3px', 'margin-bottom': '7px'}),
                            dcc.Input(id='id-input', type='number', placeholder='Durchlauf',
                                      style={'margin-left': '3px', 'margin-bottom': '7px'}),
                            html.Button('Search', id='search-button', n_clicks=0),
                            html.Div(
                                style={'textAlign': 'center', 'marginTop': '1px'},
                                children=[
                                    dcc.Graph(
                                        id='node_data_bar_chart',
                                        config={'displayModeBar': False},
                                        figure={
                                            'data': [{'x': x, 'y': y, 'type': 'bar'}],
                                            'layout': {
                                                'title': 'Gesamtkaufwahrscheinlichkeit aller Durchläufe',
                                                'xaxis': {'title': 'Durchlauf'},
                                                'yaxis': {'title': 'Kaufwahrscheinlichkeit'},
                                                'plot_bgcolor': '#f2f2f2',
                                                'paper_bgcolor': '#f2f2f2',
                                            }
                                        }
                                    ),
                                ],
                            )
                        ],
                        md=6
                    ),

                    dbc.Col(
                        [
                            html.H5('Vergleich zwischen Durchläufen'),
                            dcc.RangeSlider(
                                id='range-slider',
                                min=0,
                                max=100,
                                value=[10, 30],
                                tooltip={'always_visible': True, 'placement': 'bottom'}
                            ),
                            html.Div(
                                style={'textAlign': 'center', 'marginTop': '1px'},
                                children=[
                                    dcc.Graph(
                                        id='node_data_bar_chart',
                                        config={'displayModeBar': False},
                                        figure={
                                            'data': [
                                                {'x': x, 'y': y, 'type': 'bar', 'name': 'Anzahl potenzieller Käufer'},
                                                {'x': x, 'y': inner_y, 'type': 'bar', 'name': 'Käufer wegen Nachricht'},
                                            ],
                                            'layout': {
                                                'title': 'Wie viele würden Produkt kaufen',
                                                'xaxis': {'title': 'Anzahl Teilnehmer'},
                                                'yaxis': {'title': 'Durchlauf'},
                                                'barmode': 'overlay',  # Überlagerungsmodus für die Balken
                                                'plot_bgcolor': '#f2f2f2',
                                                'paper_bgcolor': '#f2f2f2',
                                            }
                                        }
                                    ),
                                ],
                            )
                        ],
                        md=6
                    )

                ]
            ),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Br(),
                            html.H5('Wie viele glauben die Nachricht:',
                                    style={'margin-left': '3px', 'margin-bottom': '18px'}),
                            html.Div(
                                style={'textAlign': 'center', 'marginTop': '1px'},
                                children=[
                                    dcc.Graph(
                                        id='glaube_insgesamt',
                                        config={'displayModeBar': False},
                                        figure={
                                            'data': [{'x': x, 'y': y, 'type': 'bar'}],
                                            'layout': {
                                                'title': 'Glaubwürdigkeit insgesamt',
                                                'xaxis': {'title': 'Durchlauf'},
                                                'yaxis': {'title': 'Anzahl Netzwerkteilnehmer'},
                                                'plot_bgcolor': '#f2f2f2',
                                                'paper_bgcolor': '#f2f2f2',
                                            }
                                        }
                                    ),
                                ],
                            )
                        ],
                        md=6
                    ),
                    dbc.Col(
                        [
                            html.H5('Vergleich zwischen Durchläufen'),
                            dcc.RangeSlider(
                                id='range-slider',
                                min=0,
                                max=100,
                                value=[10, 30],
                                tooltip={'always_visible': True, 'placement': 'bottom'}
                            ),
                            html.Div(
                                style={'textAlign': 'center', 'marginTop': '1px'},
                                children=[
                                    dcc.Graph(
                                        id='erreichte_Teilnehmer',
                                        config={'displayModeBar': False},
                                        figure={
                                            'data': [{'y': x, 'x': y, 'type': 'bar', 'orientation': 'h'}],
                                            'layout': {
                                                'title': 'Erreichte Teilnehmer',
                                                'xaxis': {'title': 'Teilnehmer'},
                                                'yaxis': {'title': 'Durchlauf'},
                                                'plot_bgcolor': '#f2f2f2',
                                                'paper_bgcolor': '#f2f2f2',
                                            }
                                        }
                                    ),
                                ],
                            )
                        ],
                        md=6
                    )
                ]
            ),
            html.Br(),
            html.Br(),
            html.H5('Wie viele haben die Nachricht weitergeleitet', style={'textAlign': 'center'}),
            html.Div(
                style={'textAlign': 'center', 'marginTop': '1px'},
                children=[
                    dcc.Graph(
                        id='weiterleitung',
                        config={'displayModeBar': False},
                        figure={
                            'data': [
                                {'x': x, 'y': y, 'type': 'bar', 'name': 'Weiterleitungen insgesamt'},
                                {'x': x, 'y': inner_y, 'type': 'bar', 'name': 'Anteil Knoten die weitergeleitet haben'},
                            ],
                            'layout': {
                                'title': 'Weiterleitung Nachricht',
                                'xaxis': {'title': 'Durchlauf'},
                                'yaxis': {'title': 'Anzahl Weiterleitung'},
                                'barmode': 'overlay',  # Überlagerungsmodus für die Balken
                                'plot_bgcolor': '#f2f2f2',
                                'paper_bgcolor': '#f2f2f2',
                            }
                        }
                    ),
                ],
            )

            # Regressionsgrad einfügen für alle läufe
            # Top10 Durchläufe Kaufwahrscheinlichekeit als Balkendiagramm
            # Die größten und niedrigsten Beeinflusser in einem
        ]),

        #############################################Tab 3 Werte########################################################
        dcc.Tab(label='Werte pro Teilnehmer', children=[
            html.Br(),
            dbc.Row(
                [
                    # Karten in Tab 3 zu sehen → können mittels Callback befüllt werden
                    dbc.Col(dbc.Card(card_left, color="primary", inverse=True), md=2),
                    dbc.Col(dbc.Card(card_leftmid, color="secondary", inverse=True), md=2),
                    dbc.Col(dbc.Card(card_mid, color="info", inverse=True), md=2),
                    dbc.Col(dbc.Card(card_rightmid, color="info", inverse=True), md=2),
                    dbc.Col(dbc.Card(card_right, color="info", inverse=True), md=2)

                ], justify='center',
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Br(),
                            html.Br(),
                            html.H4('Werte pro Teilnehmer', style={'textAlign': 'center'}),
                            "Durchlauf ",
                            dcc.Input(id="per_Participant_run", value=10, type="number", step=1),
                            " Teilnehmer-ID ",
                            dcc.Input(
                                id="per_Particpant_id",
                                value=100,
                                type="number",
                            ),
                            # Tabelle mit den ersten 100 ID eines Durchlaufs
                            dash_table.DataTable(
                                id='Table_per_Participant',
                                columns=[
                                    {'name': 'ID', 'id': 'id_per_Particpant'},
                                    {'name': 'Wie oft Nachricht erhalten', 'id': 'erhalten_per_Participant'},
                                    {'name': 'Wie oft weitergeleitet', 'id': 'weitergeleitet_per_Participant'},
                                    {'name': 'Anteil erhalten und weitergeleitet',
                                     'id': 'erhalten_weitergeleitet_per_Participant'},
                                    {'name': 'Grad Zentralität', 'id': 'zentralitaet_per_Participant'},
                                    {'name': 'Verflechtung der Zentralität', 'id': 'verflechtung_per_Participant'},
                                ],
                                data=df.to_dict('records'), page_size=10, sort_action='native',
                                style_table={'overflowX': 'auto'}),

                        ],
                        md=12
                    )
                ]
            ),

            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5('Regressionsanalyse'),
                            html.Div(
                                style={'textAlign': 'center', 'marginTop': '1px'},
                                children=[
                                    dcc.Graph(
                                        id='regression_plot',
                                        config={'displayModeBar': False},
                                        figure={
                                            'data': [
                                                {'x': Xr.squeeze(), 'y': yr.squeeze(), 'mode': 'markers',
                                                 'name': 'Datenpunkte'},
                                                {'x': Xr.squeeze(), 'y': yr_pred.squeeze(), 'mode': 'lines',
                                                 'name': 'Regressionslinie'}
                                            ],
                                            'layout': {
                                                'title': {'text': 'Einfache lineare Regression', 'x': 0.5},
                                                'xaxis': {'title': 'Unabhängige Variable'},
                                                'yaxis': {'title': 'Abhängige Variable'},
                                                'plot_bgcolor': '#f2f2f2',
                                                'paper_bgcolor': '#f2f2f2',
                                            }
                                        }
                                    ),
                                ],
                            )
                        ],
                        md=6
                    ),

                    dbc.Col(
                        [
                            html.H5('Anzahl Nachbarn: ', style={'display': 'inline'}),
                            dcc.Input(id='id_input_Follower', type='number', placeholder='Durchlauf',
                                      style={'margin-left': '3px', 'margin-bottom': '7px'}),
                            html.Button('Search', id='search-Follower', n_clicks=0),
                            html.Div(
                                style={'textAlign': 'center'},
                                children=[
                                    dcc.Graph(
                                        id='participant_per_run',
                                        config={'displayModeBar': False},
                                        figure={
                                            'data': [{'x': x, 'y': y, 'type': 'bar'}],
                                            'layout': {
                                                'title': 'Nachbarn pro Durchlauf',
                                                'xaxis': {'title': 'Teilnehmer'},
                                                'yaxis': {'title': 'Anzahl Nachbarn'},
                                                'plot_bgcolor': '#f2f2f2',
                                                'paper_bgcolor': '#f2f2f2',
                                            }
                                        }
                                    ),
                                ],
                            )
                        ],
                        md=6
                    ),
                ]
            )

            # Gesamtkaufwahrscheinlichkeit als Rad
            # Teilnehmer mit meisten Followern
            # Top5 Beeinflusser in einem Durchlauf
            # höchster Influencer wert und wer es ist
        ]),
        dcc.Tab(label='Werte pro Teilnehmer', children=[
            html.Br(),
            dbc.Row(

                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(html.H4('Verbreitung', style={'textAlign': 'center'})),
                                    dbc.CardBody(
                                        dash_table.DataTable(
                                            id='verbreitung1',
                                            columns=[
                                                {'name': 'Weiterleitung', 'id': 'weitergeleitet_per_Participant'},
                                                {'name': 'Minimum', 'id': 'id_per_Particpant'},
                                                {'name': 'Average', 'id': 'erhalten_per_Participant'},
                                                {'name': 'Maximum', 'id': 'weitergeleitet_per_Participant'},
                                            ],
                                            data=df.to_dict('records'), page_size=3,
                                            style_table={'overflowX': 'auto', 'margin': '10px',
                                                         'backgroundColor': '#f2f2f2'},
                                            style_header={'textAlign': 'left'},
                                        )
                                    ),
                                ],
                                style={'background-color': '#f0f0f0'}
                            ),
                        ],
                        md=6
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(html.H4('Glaubwürdigkeit', style={'textAlign': 'center'})),
                                    dbc.CardBody(
                                        dash_table.DataTable(
                                            id='verbreitung2',
                                            columns=[
                                                {'name': 'Glaubwürdigkeit', 'id': 'weitergeleitet_per_Participant',
                                                 'editable': False},
                                                {'name': 'Minimum', 'id': 'id_per_Particpant'},
                                                {'name': 'Average', 'id': 'erhalten_per_Participant'},
                                                {'name': 'Maximum', 'id': 'weitergeleitet_per_Participant'},
                                            ],
                                            data=df.to_dict('records'), page_size=3,
                                            style_table={'overflowX': 'auto', 'margin': '10px',
                                                         'backgroundColor': '#f2f2f2'},
                                            style_header={'textAlign': 'left'},
                                        )
                                    ),
                                ],
                                style={'background-color': '#f0f0f0'}
                            ),
                        ],
                        md=6
                    )
                ],
                justify='around',  # Gleichmäßige Verteilung der Spalten

            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(html.H4('Kaufwahrscheinlichtkeit', style={'textAlign': 'center'})),
                                    dbc.CardBody(
                                        dash_table.DataTable(
                                            id='verbreitung3',
                                            columns=[
                                                {'name': 'Kaufwahrscheinlichkeit',
                                                 'id': 'weitergeleitet_per_Participant'},
                                                {'name': 'Minimum', 'id': 'id_per_Particpant'},
                                                {'name': 'Average', 'id': 'erhalten_per_Participant'},
                                                {'name': 'Maximum', 'id': 'weitergeleitet_per_Participant'},
                                            ],
                                            data=df.to_dict('records'), page_size=3,
                                            style_table={'overflowX': 'auto', 'margin': '10px',
                                                         'backgroundColor': '#f2f2f2'},
                                            style_header={'textAlign': 'left'},
                                        )
                                    ),
                                ],
                                style={'background-color': '#f0f0f0'}
                            ),
                        ],
                        md=6
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(html.H4('Weiterleitung', style={'textAlign': 'center'})),
                                    dbc.CardBody(
                                        dash_table.DataTable(
                                            id='verbreitung4',
                                            columns=[
                                                {'name': 'Weiterleitung', 'id': 'weitergeleitet_per_Participant',
                                                 'editable': False},
                                                {'name': 'Minimum', 'id': 'id_per_Particpant'},
                                                {'name': 'Average', 'id': 'erhalten_per_Participant'},
                                                {'name': 'Maximum', 'id': 'weitergeleitet_per_Participant'},
                                            ],
                                            data=df.to_dict('records'), page_size=3,
                                            style_table={'overflowX': 'auto', 'margin': '10px',
                                                         'backgroundColor': '#f2f2f2'},
                                            style_header={'textAlign': 'left'},
                                        )
                                    ),
                                ],
                                style={'background-color': '#f0f0f0'}
                            ),
                        ],
                        md=6
                    )
                ],
                justify='around'  # Gleichmäßige Verteilung der Spalten
            ),
        ]),

    ])
])


@app.callback(
    Output('network_cache', 'data'),
    Input('generate_Network', 'n_clicks'),
    State('net_shape', 'value'),
    State('network_participant_parameter', 'value'),
    State('n_init_edges', 'value'),
    State('sep_prob', 'value'),
    State('turbulence_factor', 'value'),
    State('bots_parameter', 'value'),
    State('influencer_parameter', 'value'),
    State('cred_parameter', 'value'),
    State('indefference', 'value'),
    State('isi_parameter', 'value'),
    State('fi_parameter', 'value'),
    State('purchase_init_prob_parameter', 'value'),
    State('purchase_prob_max_parameter', 'value'),
    State('purchase_prob_min_parameter', 'value'),
    State('purchase_expo_param_positive_parameter', 'value'),
    State('purchase_expo_param_negative_parameter', 'value'),
    State('time_message_parameter', 'value'),
    State('lifetime_parameter', 'value'),
    State('quality_parameter', 'value'),
    State('emotional_parameter', 'value'),
    State('time_counter_parameter', 'value'),
    State('lifetime_counter_parameter', 'value'),
    State('quality_counter_parameter', 'value'),
    State('emotional_counter_parameter', 'value'),
    State('run_parameter', 'value'),
    State('steps_per_run_parameter', 'value'),
    State('run_csv_parameter', 'value')
)
def button_start_simulation(n_clicks,
                            shape,
                            n_network_participants,
                            init_edges,
                            split_prob,
                            turbulence_factor,
                            n_bots,
                            n_influencer,
                            threshold_believe,
                            indifference,
                            isi_parameter,
                            fi_parameter,
                            purchase_init_prob,
                            purchase_prob_max,
                            purchase_prob_min,
                            purchase_expo_param_positive,
                            purchase_expo_param_negative,
                            message_start_time,
                            message_life_time,
                            message_quality,
                            message_emotionality,
                            counter_message_start_time,
                            counter_message_life_time,
                            counter_message_quality,
                            counter_message_emotionality,
                            runs,
                            run_steps,
                            run_csv
                            ):
    # Initialisierung der Parameter-Dictionary
    network_parameters = {}
    participant_parameters = {}
    message_parameters = {}
    counter_message_parameters = {}
    simulation_parameters = {}

    network_parameters["shape"] = shape
    network_parameters["n_nodes"] = n_network_participants
    network_parameters["init_edges"] = init_edges
    network_parameters["split_prob"] = split_prob
    network_parameters["turbulence_factor"] = turbulence_factor
    network_parameters["n_bots"] = n_bots
    network_parameters["n_influencer"] = n_influencer

    participant_parameters["threshold_belive"] = threshold_believe
    participant_parameters["indifference"] = indifference
    participant_parameters["isi_parameter"] = isi_parameter
    participant_parameters["fi_parameter"] = fi_parameter
    participant_parameters["purchase_init_prob"] = purchase_init_prob
    participant_parameters["purchase_prob_max"] = purchase_prob_max
    participant_parameters["purchase_prob_min"] = purchase_prob_min
    participant_parameters["purchase_expo_param_positive"] = purchase_expo_param_positive
    participant_parameters["purchase_expo_param_negative"] = purchase_expo_param_negative

    message_parameters["start_time"] = message_start_time
    message_parameters["life_time"] = message_life_time
    message_parameters["quality"] = message_quality
    message_parameters["emotionality"] = message_emotionality

    counter_message_parameters["start_time"] = counter_message_start_time
    counter_message_parameters["life_time"] = counter_message_life_time
    counter_message_parameters["quality"] = counter_message_quality
    counter_message_parameters["emotionality"] = counter_message_emotionality

    simulation_parameters["runs"] = runs
    simulation_parameters["run_steps"] = run_steps
    simulation_parameters["run_csv"] = run_csv

    if n_clicks > 0:
        ns = network_simulator.Network_Simulation(simulation_parameters,
                                                  network_parameters,
                                                  participant_parameters,
                                                  message_parameters,
                                                  counter_message_parameters)

        simulation_csv = ns.compute_simulation()

        return simulation_csv.to_json()


@app.callback(Output('download_simulation_csv', 'data'),
              Input('btn_csv', 'n_clicks'),
              State('network_cache', 'data'))
def download_csv(n_clicks, csv_data):
    if csv_data:
        return dcc.send_data_frame(pd.read_json(csv_data).to_csv, "Simulation.csv")

"""
@app.callback(
    Output('Table100nodes', 'data'),
    Output('Table100message', 'data'),
    Output('Table100conter_message', 'data'),
    State("network_cache", "data"),
    State("network_cache", "data")
)
def generate_table_100(network_data):
    if not network_data:
        network_data = {'directed': False, 'multigraph': False, 'graph': [], 'nodes': [], 'adjacency': []}

    net = network_converter.network_form_json(network_data)
    G = net.graph

    df_node_data = pd.DataFrame(columns=["ID",
                                         "Grad der Zentralität",
                                         "Betweenes Zentralität",
                                         "Initiale Kaufwahrscheinlichkeit",
                                         "Aktuelle Kaufwahrscheinlichkeit"
                                         ])

    df_node_message_data = pd.DataFrame(columns=["Häufigkeit Erhalt",
                                                 "Glaubwürdigkeit",
                                                 "Glaube",
                                                 "Weiterleitungswahrscheinlichkeit"
                                                 "Häufigkeit Weiterleitung",
                                                 ])

    df_node_conter_message_data = pd.DataFrame(columns=["Häufigkeit Erhalt",
                                                        "Glaubwürdigkeit",
                                                        "Glaube",
                                                        "Weiterleitungswahrscheinlichkeit"
                                                        "Häufigkeit Weiterleitung",
                                                        ])"""

if __name__ == '__main__':
    app.run_server(debug=True)