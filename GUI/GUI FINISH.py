from io import StringIO
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, dcc, html, Output, State, Input
from dash import dash_table
import numpy as np
import network_simulator

# Beispiel Daten Tabelle
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df = pd.DataFrame(0, index=range(3), columns=["Verbreitung", "Minimum", "Durchschnitt", "Maximum"])


app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH])
app.title = "Netzwerksimulation"

##############################################Layout####################################################################
app.layout = html.Div([

    # Cache
    dcc.Store(id="network_cache"),

    # Download
    dcc.Download(id="download_simulation_csv"),

    # Interval in dem aktaulisiert wird
    dcc.Interval(id='refresh_interval', interval=5 * 1000, n_intervals=0),  # im Millisekunden

    html.Br(),
    html.H1('Netzwerk Simulation', style={'textAlign': 'center'}),
    html.Hr(),

    dcc.Tabs([

        #############################################Tab 1 Input########################################################
        dcc.Tab(label='Eingabe', children=[
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
                                                      value=1000,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '30px'}),
                                        ], width=3),

                                        dbc.Col([
                                            html.Label('Anzahl initialer Kanten'),
                                            html.Br(),
                                            dcc.Input(id='n_init_edges', type='number', value=6, min=0, step=1,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '30px'}
                                                      ),
                                        ], width=3),

                                        dbc.Col([
                                            html.Label('Seperationswahrscheinlichkeit'),
                                            html.Br(),
                                            dcc.Input(id='sep_prob', type='number', value=0.1, min=0, max=1,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '30px'}),
                                        ], width=3),
                                    ]
                                    ),

                            dbc.Row(className='mx-auto', style={'width': 'fit-content'},
                                    children=[
                                        dbc.Col([
                                            html.Label('Turbulenz-Faktor des Marktes'),
                                            html.Br(),
                                            dcc.Input(id='turbulence_factor', type='number', value=0.5, min=0, max=1,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '30px'}),
                                        ], width=4),

                                        dbc.Col([
                                            html.Label('Bots'),
                                            html.Br(),
                                            dcc.Input(id='bots_parameter', type='number', value=0, min=0, step=1,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '30px'}
                                                      ),
                                        ], width=4),

                                        dbc.Col([
                                            html.Label('Influencer'),
                                            html.Br(),
                                            dcc.Input(id='influencer_parameter', type='number', value=0, min=0, step=1,
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
                                                      style={'width': '350px', 'height': '40px',
                                                             'margin-bottom': '30px', 'margin-left': 'auto',
                                                             'margin-right': 'auto'}),
                                        ], width=4),

                                        dbc.Col([
                                            html.Label('Indifferenz'),
                                            html.Br(),
                                            dcc.Input(id='indefference', type='number', value=0.1, min=0, max=1,
                                                      style={'width': '350px', 'height': '40px',
                                                             'margin-bottom': '30px', 'margin-left': 'auto',
                                                             'margin-right': 'auto'}
                                                      ),
                                        ], width=4),

                                        dbc.Col([
                                            html.Label('ISI Parameter'),
                                            html.Br(),
                                            dcc.Input(id='isi_parameter', type='number', value=0.5, min=0, max=1,
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
                                                      style={'width': '350px', 'height': '40px',
                                                             'margin-bottom': '30px', 'margin-left': 'auto',
                                                             'margin-right': 'auto'}),
                                        ], width=4),

                                        dbc.Col([
                                            html.Label('Initiale Kaufwahrscheinlichkeit'),
                                            html.Br(),
                                            dcc.Input(id='purchase_init_prob_parameter', type='number', value=0.1, min=0, max=1,
                                                      style={'width': '350px', 'height': '40px',
                                                             'margin-bottom': '30px', 'margin-left': 'auto',
                                                             'margin-right': 'auto'}
                                                      ),
                                        ], width=4),

                                        dbc.Col([
                                            html.Label('Maximale Kaufwahrscheinlichkeit'),
                                            html.Br(),
                                            dcc.Input(id='purchase_prob_max_parameter', type='number', value=0.125, min=0,max=1,
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
                                            dcc.Input(id='purchase_prob_min_parameter', type='number', value=0.05, min=0,max=1,
                                                      step=0.01,
                                                      style={'width': '350px', 'height': '40px',
                                                             'margin-bottom': '30px', 'margin-left': 'auto',
                                                             'margin-right': 'auto'}),
                                        ], width=4),

                                        dbc.Col([
                                            html.Label('Positive expotenzielle Kaufwahrscheinlichkeit'),
                                            html.Br(),
                                            dcc.Input(id='purchase_expo_param_positive_parameter', type='number',
                                                      value=5, min=0,
                                                      style={'width': '350px', 'height': '40px',
                                                             'margin-bottom': '30px', 'margin-left': 'auto',
                                                             'margin-right': 'auto'}
                                                      ),
                                        ], width=4),

                                        dbc.Col([
                                            html.Label('Negative expotenzielle Kaufwahrscheinlichkeit'),
                                            html.Br(),
                                            dcc.Input(id='purchase_expo_param_negative_parameter', type='number',
                                                      value=2.5, min=0,
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
                                            dcc.Checklist(
                                                id='checkbox_nachricht',
                                                options=[
                                                    {'label': ' Nachricht simulieren', 'value': 'check_value'}
                                                ],
                                                value=[],  # Standardmäßig nicht ausgewählt
                                            ),
                                        ]
                                        ),
                                    ]
                                    ),
                            dbc.Row(className='mx-auto', align='center', style={'width': 'fit-content'},
                                    children=[
                                        dbc.Col([
                                            html.Label('Qualität der Nachricht'),
                                            dcc.Input(id='quality_parameter', type='number', min=0, max=1,value=0.5,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '15px'}),
                                        ], width=3),

                                        dbc.Col([
                                            html.Label('emotionale Aussagekraft'),
                                            html.Br(),
                                            dcc.Input(id='emotional_parameter', type='number',min=0, max=1,value=0.5,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '15px'}),
                                        ], width=3),

                                        dbc.Col([
                                            html.Label('Zeitpunkt Auftritt Nachricht'),
                                            html.Br(),
                                            dcc.Input(id='time_message_parameter', type='number', value=0, min=0,step=1,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '15px'}),
                                        ], width=3),

                                        dbc.Col([
                                            html.Label('Lebenszeit der Nachricht'),
                                            html.Br(),
                                            dcc.Input(id='lifetime_parameter', type='number', value=20,min=0,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '15px'}),
                                        ], width=3),
                                    ]
                                    ),
                            dbc.Row(className='mx-auto', align='center', style={'width': 'fit-content'},
                                    children=[
                                        dbc.Col([
                                            dcc.Checklist(
                                                id='checkbox_gegennachricht',
                                                options=[
                                                    {'label': ' Gegennachricht simulieren', 'value': 'check_value'}
                                                ],
                                                value=[],  # Standardmäßig nicht ausgewählt
                                            ),
                                        ]
                                        ),
                                    ]
                                    ),
                            dbc.Row(className='mx-auto', align='center', style={'width': 'fit-content'},
                                    children=[
                                        dbc.Col([
                                            html.Label('Qualität Gegennachricht'),
                                            dcc.Input(id='quality_counter_parameter', type='number',min=0, max=1,value=0.5,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '15px'}),
                                        ], width=3),

                                        dbc.Col([
                                            html.Label('emotionale Aussagekraft'),
                                            html.Br(),
                                            dcc.Input(id='emotional_counter_parameter', type='number',min=0, max=1,value=0.5,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '15px'}),
                                        ], width=3),

                                        dbc.Col([
                                            html.Label('Zeitpunkt Auftritt Gegennachricht'),
                                            html.Br(),
                                            dcc.Input(id='time_counter_parameter', type='number', value=0, min=0,step=1,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '15px'}),
                                        ], width=3),

                                        dbc.Col([
                                            html.Label('Lebenszeit Gegennachricht'),
                                            html.Br(),
                                            dcc.Input(id='lifetime_counter_parameter', type='number', value=20, min=0,
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
                                            dcc.Input(id='run_parameter', type='number',value=1,
                                                      style={'width': '300px', 'height': '40px',
                                                             'margin-bottom': '15px'}),
                                        ], width=6, className="mb-3"),

                                        dbc.Col([
                                            html.Label('Schritte pro Durchlauf'),
                                            html.Br(),
                                            dcc.Input(id='steps_per_run_parameter', type='number',value=1000,
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
                                style={'width': '200px', 'height': '50px', 'margin-bottom': '2rem'}),
                ],
            ),
        ]),

        dcc.Tab(label='Auswertung', children=[
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
                                            id='verbreitung',
                                            style_header={'textAlign': 'left'}
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
                                            id='glauben',
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
                                    dbc.CardHeader(html.H4('Kaufwahrscheinlichkeit', style={'textAlign': 'center'})),
                                    dbc.CardBody(
                                        dash_table.DataTable(
                                            id='kaufen',
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
                                            id='weiterleitung',
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
            html.Br(),
            html.Div(
                style={'textAlign': 'center', 'marginTop': '10px'},
                children=[
                    html.Button("Download CSV", id="btn_csv",
                                style={'width': '300px', 'height': '50px', 'font-size': '20px'}),
                    dcc.Download(id="download_csv"),
                ]
            )

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
    State('checkbox_nachricht', 'value'),
    State('time_message_parameter', 'value'),
    State('lifetime_parameter', 'value'),
    State('quality_parameter', 'value'),
    State('emotional_parameter', 'value'),
    State('checkbox_gegennachricht', 'value'),
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
                            check_message,
                            message_start_time,
                            message_life_time,
                            message_quality,
                            message_emotionality,
                            check_counter_message,
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

    participant_parameters["threshold_believe"] = threshold_believe
    participant_parameters["indifference"] = indifference
    participant_parameters["isi_parameter"] = isi_parameter
    participant_parameters["fi_parameter"] = fi_parameter
    participant_parameters["purchase_init_prob"] = purchase_init_prob
    participant_parameters["purchase_prob_max"] = purchase_prob_max
    participant_parameters["purchase_prob_min"] = purchase_prob_min
    participant_parameters["purchase_expo_param_positive"] = purchase_expo_param_positive
    participant_parameters["purchase_expo_param_negative"] = purchase_expo_param_negative

    message_parameters["check"] = check_message
    message_parameters["start_time"] = message_start_time
    message_parameters["life_time"] = message_life_time
    message_parameters["quality"] = message_quality
    message_parameters["emotionality"] = message_emotionality

    counter_message_parameters["check"] = check_counter_message
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


@app.callback(Output('verbreitung', 'data'),
              Input('refresh_interval', 'n_intervals'),
              State('network_cache', 'data')
              )
def fill_table_spreading(refresh_interval, simulation_data_message):
    if refresh_interval > 0 and simulation_data_message:
        simulation_data_message = pd.read_json(StringIO(simulation_data_message))

        output_spreading = pd.DataFrame(columns=["Verbreitung", "Minimum", "Durchschnitt", "Maximum"])

        # Verbreitung
        output_spreading.loc[1] = ["Nachricht", round(simulation_data_message["prob_spreading"].min(), 2),
                                   round(simulation_data_message["prob_spreading"].mean(), 2),
                                   round(simulation_data_message["prob_spreading"].max(), 2)]
        output_spreading.loc[2] = ["Gegennachricht", round(simulation_data_message["prob_counter_spreading"].min(), 2),
                                   round(simulation_data_message["prob_counter_spreading"].mean(), 2),
                                   round(simulation_data_message["prob_counter_spreading"].max(), 2)]

        return output_spreading.to_dict('records')


@app.callback(Output('glauben', 'data'),
              Input('refresh_interval', 'n_intervals'),
              State('network_cache', 'data')
              )
def fill_table_believe(refresh_interval, simulation_data_message):
    if refresh_interval > 0 and simulation_data_message:
        simulation_data_message = pd.read_json(StringIO(simulation_data_message))

        # Glauben
        output_believe = pd.DataFrame(columns=["Glauben", "Minimum", "Durchschnitt", "Maximum"])

        output_believe.loc[1] = ["Glaubwürdigkeit Nachricht",
                                 round(simulation_data_message["avg_credibility"].min(), 2),
                                 round(simulation_data_message["avg_credibility"].mean(), 2),
                                 round(simulation_data_message["avg_credibility"].max(), 2)]
        output_believe.loc[2] = ["Glauben Nachricht", round(simulation_data_message["prob_believe"].min(), 2),
                                 round(simulation_data_message["prob_believe"].mean(), 2),
                                 round(simulation_data_message["prob_believe"].max(), 2)]

        return output_believe.to_dict('records')


@app.callback(Output('weiterleitung', 'data'),
              Input('refresh_interval', 'n_intervals'),
              State('network_cache', 'data')
              )
def fill_table_forward(refresh_interval, simulation_data_message):
    if refresh_interval > 0 and simulation_data_message:
        simulation_data_message = pd.read_json(StringIO(simulation_data_message))

        # Weiterleitung
        output_forward = pd.DataFrame(columns=["Weiterleitung", "Minimum", "Durchschnitt", "Maximum"])

        output_forward.loc[1] = ["Weiterleitung Nachricht", round(simulation_data_message["prob_forward"].min(), 2),
                                 round(simulation_data_message["prob_forward"].mean(), 2),
                                 round(simulation_data_message["prob_forward"].max(), 2)]
        output_forward.loc[2] = ["Weiterleitung Gegennachricht",
                                 round(simulation_data_message["prob_counter_forward"].min(), 2),
                                 round(simulation_data_message["prob_counter_forward"].mean(), 2),
                                 round(simulation_data_message["prob_counter_forward"].max(), 2)]

        return output_forward.to_dict('records')


@app.callback(Output('kaufen', 'data'),
              Input('refresh_interval', 'n_intervals'),
              State('network_cache', 'data')
              )
def fill_table_purchase(refresh_interval, simulation_data_message):
    if refresh_interval > 0 and simulation_data_message:
        simulation_data_message = pd.read_json(StringIO(simulation_data_message))

        # Kaufen
        output_purchase = pd.DataFrame(columns=["Kaufen", "Minimum", "Durchschnitt", "Maximum"])

        output_purchase.loc[1] = ["Kaufwahrscheinlichkeit", round(simulation_data_message["avg_purchase"].min(), 2),
                                  round(simulation_data_message["avg_purchase"].mean(), 2),
                                  round(simulation_data_message["avg_purchase"].max(), 2)]
        output_purchase.loc[2] = ["Kaufentscheidung", round(simulation_data_message["prob_purchase"].min(), 2),
                                  round(simulation_data_message["prob_purchase"].mean(), 2),
                                  round(simulation_data_message["prob_purchase"].max(), 2)]

        return output_purchase.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
