import networkx as nx
from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objs as go

import network_converter
import network_generator

app = Dash(__name__)
app.title = "Networksimulation"

app.layout = html.Div([
    # dcc.Store fürs caching
    dcc.Store(id="network_cache"),

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
        ],
    ),
    html.Button('Show Network', id='show_Network', n_clicks=0,
                style={'width': '200px', 'height': '50px'}),
    html.Div(children=[
        dcc.Interval(id='interval_net_graph', interval=9999999, n_intervals=0),
        dcc.Graph(
            id='network_graph',
            config={'displayModeBar': False},
        ),

    ])
])


@app.callback(
    Output('network_graph', 'figure'),
    Input('show_Network', 'n_clicks'),
    State("network_cache", "data")
)
def update_layout(n_clicks, network_data):

    if not network_data:
        network_data = {'directed': False, 'multigraph': False, 'graph': [], 'nodes': [], 'adjacency': []}

    # Generiere aus JSON Daten ein Netzwerk-Objekt
    net = network_converter.network_form_json(network_data)

    # Erstellen eines zufälligen Netzwerks mit der angegebenen Anzahl von Knoten
    G = net.graph_json

    # Positionen der Knoten festlegen (spring_layout ist nur ein Beispiel, Sie können andere Layouts verwenden)
    pos = nx.spring_layout(G)

    # Daten für Plotly-Diagramm erstellen
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            )
        )
    )

    # Erstellen des Plotly-Figure-Objekts
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    return fig


@app.callback(
    Output('network_cache', 'data'),
    Input('generate_Network', 'n_clicks'),
    State('input_Network-participant', 'value'),
    State('anteil_Bots', 'value'),
    State('turbulence_factor', 'value')
)
def button_generate_network(n_clicks, n_networkparticipants, n_bots, turbulence_factor):
    network_graph = network_generator.generate_new_network("", n_nodes=int(n_networkparticipants))
    return network_graph


if __name__ == '__main__':
    app.run_server(debug=True)
