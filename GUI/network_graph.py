import pandas as pd
import plotly.graph_objs as go
import networkx as nx
from dash import html, dcc, Dash, Input, Output, callback, callback_context, State
from dash.exceptions import PreventUpdate


import network_converter


# Layout der Dash-Anwendung
network_layout = html.Div([
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
])

# Callback-Funktion zum Aktualisieren des Diagramms basierend auf Benutzereingaben

########## Anderen Trigger finden
@callback(
    Output('network_graph', 'figure'),
    Input('interval_net_graph', 'n_intervals'),
    State("network_cache", "data")
)
def update_layout(n_intervals,network_data):

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
