import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, dcc, html
from dash import dash_table
from sklearn.linear_model import LinearRegression
import plotly.express as px
import numpy as np

#Beispiel Daten Tabelle
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

app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH])
app.title = "Networksimulation"

# Erstellen der Optionen für das Dropdown-Menü
options = [{'label': str(i), 'value': i} for i in range(0, 101)]

card_left = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Höchste Kaufwahrscheinlichkeit", className="card-title", style={'textAlign': 'center'},),
                html.H3(
                    "500",
                    className="card-text", style={'text-align': 'center'},
                ),
            ]
        ),

    ],
    color="primary",   # https://bootswatch.com/default/ for more card colors
    inverse=True,   # change color of text (black or white)
    outline=False,  # True = remove the block colors from the background and header
)

card_leftmid = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Geringste Kaufwahrscheinlichkeit", className="card-title", style={'textAlign': 'center'},),
                html.H3(
                    "500",
                    className="card-text", style={'text-align': 'center'},
                ),
            ]
        ),

    ],
    color="primary",   # https://bootswatch.com/default/ for more card colors
    inverse=True,   # change color of text (black or white)
    outline=False,  # True = remove the block colors from the background and header
)

card_mid = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Höchste Anzahl an Nachbarn", className="card-title", style={'textAlign': 'center'},),
                html.H3(
                    "500",
                    className="card-text", style={'text-align': 'center'},
                ),
            ]
        ),

    ],
    color="primary",   # https://bootswatch.com/default/ for more card colors
    inverse=True,   # change color of text (black or white)
    outline=False,  # True = remove the block colors from the background and header
)

card_rightmid = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Höchste Glaubwürdigkeit", className="card-title", style={'textAlign': 'center'},),
                html.H3(
                    "500",
                    className="card-text", style={'text-align': 'center'},
                ),
            ]
        ),

    ],
    color="primary",   # https://bootswatch.com/default/ for more card colors
    inverse=True,   # change color of text (black or white)
    outline=False,  # True = remove the block colors from the background and header
)

card_right = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Geringste Glaubwürdigkeit", className="card-title", style={'textAlign': 'center'},),
                html.H3(
                    "500",
                    className="card-text", style={'text-align': 'center'},
                ),
            ]
        ),

    ],
    color="primary",   # https://bootswatch.com/default/ for more card colors
    inverse=True,   # change color of text (black or white)
    outline=False,  # True = remove the block colors from the background and header
)

app.layout = html.Div([
    html.Br(),
    html.H1('Network Simulation', style={'textAlign': 'center'}),
    html.Hr(),

    dcc.Tabs([
        dcc.Tab(label='Parameter input', children=[
            html.Br(),
            dbc.Row(className='mx-auto', style={'width': 'fit-content'},
                    children=[
                        dbc.Col([
                            html.H6('Network Participants'),
                            dcc.Input(id='input_Network-participant', value=10, type='number',
                                      style={'width': '300px', 'height': '30px', 'margin-bottom': '15px'},
                                      placeholder='Enter the number of Network Participants'),
                        ], width=4),

                        dbc.Col([
                            html.H6('Bots'),
                            dcc.Input(id='anteil_Bots', type='number',
                                      style={'width': '300px', 'height': '30px', 'margin-bottom': '15px'},
                                      placeholder='Enter the number of Bots'),
                        ], width=4),

                        dbc.Col([
                            html.H6('Seperationswahrscheinlichkeit'),
                            dcc.Input(id='sep_prob', type='number', value=0.1, min=0, max=1, step=0.01,
                                      style={'textAlign': 'center', 'width': '300px', 'height': '30px',
                                             'margin-bottom': '15px'}),
                        ], width=4),
                    ]
                    ),

            dbc.Row(className='mx-auto', style={'width': 'fit-content'},
                    children=[
                        dbc.Col([
                            html.H6('Turbulenz-Faktor des Netzwerks'),
                            dcc.Input(id='turbulence_factor', type='number', value=0.5, min=0, max=1, step=0.01,
                                      style={'width': '300px', 'height': '30px', 'margin-bottom': '15px'},
                                      placeholder='Turbulenz Faktor'),
                        ], width=4),

                        dbc.Col([
                            html.H6('Anzahl initialer Kanten'),
                            dcc.Input(id='n_init_edges', type='number', value=2, min=0, step=1,
                                      style={'width': '300px', 'height': '30px', 'margin-bottom': '15px'}
                                      ),
                        ], width=4),

                        dbc.Col([
                            html.H6('Netzwerkart'),
                            dcc.Dropdown(options=[{'label': 'SWN', 'value': 'SWN'},
                                                  {'label': 'SFN', 'value': 'SFN'},
                                                  {'label': 'random', 'value': 'random'}],
                                         value='SWN', id='net_shape',
                                         style={'width': '300px', 'height': '30px', 'margin-bottom': '15px'},
                                         ),
                        ], width=4),
                    ]
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
                style={'textAlign': 'center', 'marginTop': '50px'},
                children=html.Div([
                    html.H5('Möchten Sie für jeden Durchlauf eine CSV Datei erstellen?'),
                    dcc.RadioItems(
                        options=[
                            {'label': 'Ja', 'value': 'ja'},
                            {'label': 'Nein', 'value': 'nein'}
                        ],
                        value='nein',
                        inline=True,
                        labelStyle={'margin-right': '20px', 'font-size': '20px'},
                        inputStyle={'margin-right': '5px'}
                    )
                ])
            ),
            html.Div(
                style={'textAlign': 'center', 'marginTop': '30px'},
                children=[
                    html.Button('Generate Network', id='generate_Network', n_clicks=0,
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
        ]),

        dcc.Tab(label='Auswertung', children=[
            html.Br(),
            html.H4('Die ersten 100 Knoten eines Netzwerkes', style={'textAlign': 'center'}),
            html.Label('Durchlauf:', style={'margin-left': '6px', 'font-size': '20px'}),
            dcc.Dropdown(
                id='number-dropdown',
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
                            html.H5('Gesamtkaufwahrscheinlichkeit aller Durchläufe:', style={'margin-left': '3px', 'margin-bottom': '7px'}),
                            dcc.Input(id='id-input', type='number', placeholder='Durchlauf', style={'margin-left': '3px', 'margin-bottom': '7px'}),
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
                            html.H5('Wie viele glauben die Nachricht:', style={'margin-left': '3px', 'margin-bottom': '18px'}),
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

            #Regressionsgrad einfügen für alle läufe
            #Top10 Durchläufe Kaufwahrscheinlichekeit als Balkendiagramm
            #Die größten und nidrigsten Beeinflusser in einem
        ]),

        dcc.Tab(label='Werte pro Teilnehmer', children=[
            html.Br(),
            dbc.Row(
                [
                    #Karten in Tab 3 zu sehen -> können mittels Callback befüllt werden
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
                                    {'name': 'Anteil erhalten und weitergeleitet', 'id': 'erhalten_weitergeleitet_per_Participant'},
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

                            ),
                        ],
                        md=6
                    ),

                    dbc.Col(
                        [
                            html.H5('Anzahl Nachbarn: ', style={'display': 'inline'}),
                            dcc.Input(id='id_input_Follower', type='number', placeholder='Durchlauf', style={'margin-left': '3px', 'margin-bottom': '7px'}),
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

                            ),
                    ],
                    md=6
                ),
                ]
            )

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
                                                {'name': 'Kaufwahrscheinlichkeit', 'id': 'weitergeleitet_per_Participant'},
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

if __name__ == '__main__':
    app.run_server(debug=True)
