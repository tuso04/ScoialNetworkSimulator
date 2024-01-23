import networkx as nx
from dash import Dash, dcc, html, Input, Output, State, dash_table
import plotly.graph_objs as go
import network_converter
import network_generator
import random
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(__name__)
app.title = "Networksimulation"


# Funktion zur Extraktion der IDs
def get_node_ids(network_data):
    if not network_data:
        network_data = {'directed': False, 'multigraph': False, 'graph': [], 'nodes': [], 'adjacency': []}

    net = network_converter.network_form_json(network_data)
    G = net.graph
    return list(G.nodes)


# Funktion zur Erstellung von Beispieldaten für die Knoten
def generate_node_data(node_ids):
    node_data = {}
    for node_id in node_ids:
        # Beispielwerte - Sie können dies entsprechend Ihren Anforderungen anpassen
        node_data[node_id] = random.uniform(0, 1)
    return node_data


# Beispiel-Daten für die Tabelle
data = {
    'ID': [1, 2, 3, 4, 5],
    'Turbulenzfaktor': [0.8, 0.6, 0.7, 0.5, 0.9],
    'Kaufwahrscheinlichkeit': [0.75, 0.85, 0.6, 0.9, 0.7],
    'Gleichgültigkeit': [0.2, 0.1, 0.3, 0.5, 0.4],
}

df = pd.DataFrame(data)

app.layout = html.Div([
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
    html.Div(children=[
        dcc.Interval(id='interval_net_graph', interval=9999999, n_intervals=0),
        dcc.Graph(
            id='network_graph',
            config={'displayModeBar': False},
            #style={'height': 400}
        ),
    ]),
    html.Div(
        style={'textAlign': 'center', 'marginTop': '10px'},
        children=[
            html.Button('Show Network', id='show_Network', n_clicks=0,
                        style={'width': '200px', 'height': '50px'}),
        ],
    ),
    html.Br(),
    html.Br(),

    html.Div('Node stats:'),
    dcc.Input(id='search_id', type='number'),

    html.Button('Show Node ID', id='show_Node_ID', n_clicks=0),
    html.Div(id='node_id_output'),

    html.Br(),
    html.Div(
        style={'textAlign': 'center', 'marginTop': '10px'},
        children=[
            html.Div('Node Data:'),
            dcc.Graph(id='node_data_bar_chart'),
        ],
    ),
    dcc.Input(id='id-input', type='number', placeholder='Enter ID'),
    html.Button('Search', id='search-button', n_clicks=0),
    dash_table.DataTable(
        id='table',
        columns=[
            {'name': 'ID', 'id': 'ID'},
            {'name': 'Turbulenzfaktor', 'id': 'Turbulenzfaktor'},
            {'name': 'Kaufwahrscheinlichkeit', 'id': 'Kaufwahrscheinlichkeit'},
            {'name': 'Gleichgültigkeit', 'id': 'Gleichgültigkeit'},
        ],
        data=df.to_dict('records'),
    ),
])


# Callback zum Generieren des Netzwerks
@app.callback(
    Output('network_cache', 'data'),
    Input('generate_Network', 'n_clicks'),
    State('input_Network-participant', 'value'),
    State('anteil_Bots', 'value'),
    State('turbulence_factor', 'value')
)
def button_generate_network(n_clicks, n_networkparticipants, n_bots, turbulence_factor):
    network_graph = network_generator.generate_new_network("SFN", n_nodes=int(n_networkparticipants), init_edges=4, split_prob=0.9)
    return network_graph


# Callback zum Anzeigen des Netzwerks
@app.callback(
    Output('network_graph', 'figure'),
    Input('show_Network', 'n_clicks'),
    State("network_cache", "data")
)
def update_layout(n_clicks, network_data):
    if not network_data:
        network_data = {'directed': False, 'multigraph': False, 'graph': [], 'nodes': [], 'adjacency': []}

    net = network_converter.network_form_json(network_data)
    G = net.graph

    pos = nx.spring_layout(G)

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


    nodes = G.nodes()
    node_x = []
    node_y = []
    node_id = []
    node_purchase_prob = []

    for node in nodes:
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)


    for i in range(len(nodes)):
        node_id.append(nodes[i]["np_id"])
        if nodes[i]["purchase_prob"] < 0.5:
            node_purchase_prob.append("red")
        else:
            node_purchase_prob.append("green")



    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_id,
        marker=dict(
            color=node_purchase_prob
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        height=800,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    return fig


# Neue Callback-Funktion zum Ausgeben der ausgewählten ID
@app.callback(
    Output('node_id_output', 'children'),
    Input('show_Node_ID', 'n_clicks'),
    State("network_cache", "data"),
    State('search_id', 'value')
)
def show_node_id(n_clicks, network_data, search_id):
    if n_clicks > 0 and search_id is not None:
        node_ids = get_node_ids(network_data)
        if search_id in node_ids:
            return f"Selected Node ID: {search_id}"

    return ""


# Neue Callback-Funktion zum Anzeigen der Bar-Daten
@app.callback(
    Output('node_data_bar_chart', 'figure'),
    Input('show_Node_ID', 'n_clicks'),
    State("network_cache", "data"),
    State('search_id', 'value')
)
def show_node_data_bar_chart(n_clicks, network_data, search_id):
    if n_clicks > 0 and search_id is not None:
        node_ids = get_node_ids(network_data)
        if search_id in node_ids:
            node_data = generate_node_data(node_ids)

            values = [node_data[node_id] for node_id in node_ids]
            labels = ['Kaufwahrscheinlichkeit', 'Glaubwürdigkeit', 'Weiterleitungsabsicht', 'Test']

            return {
                'data': [go.Bar(y=labels, x=values, orientation='h')],
                'layout': {
                    'title': f'Node Data for ID {search_id}',
                    'yaxis': {'title': 'Node Data'},
                    'xaxis': {'title': 'Value'},
                    'margin': {'l': 150}  # Adjust left margin to accommodate long labels
                }
            }

    return {'data': [], 'layout': {}}

    # Callback zum Aktualisieren der DataTable mit Suchfilter
    # Callback zum Aktualisieren der DataTable mit Suchfilter
    # Callback zum Aktualisieren der DataTable mit Suchfilter


@app.callback(
    Output('table', 'data'),
    Input('search-button', 'n_clicks'),
    State('id-input', 'value'),
    prevent_initial_call=True
)
def update_table(n_clicks, search_id):
    if n_clicks > 0 and search_id is not None:
        # Beispiel: Wenn die Daten in einem DataFrame namens df gespeichert sind
        filtered_df = df[df['ID'] == int(search_id)]
        return filtered_df.to_dict('records')
    else:
        # Beispiel: Wenn die Daten in einem DataFrame namens df gespeichert sind
        return df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
