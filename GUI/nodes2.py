from dash import html, dcc, callback, Input, Output, dash_table, Dash
import plotly.express as px
import pandas as pd

class Nodes:
    # Beispiel-Daten für die Tabelle
    data = {
        'ID': [1, 2, 3, 4, 5],
        'Turbulenzfaktor': [0.8, 0.6, 0.7, 0.5, 0.9],
        'Kaufwahrscheinlichkeit': [0.75, 0.85, 0.6, 0.9, 0.7],
        'Gleichgültigkeit': [0.2, 0.1, 0.3, 0.5, 0.4],
    }

    df = pd.DataFrame(data)

    nodes_layout = html.Div([
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

    @callback(
        Output('table', 'data'),
        [Input('search-button', 'n_clicks')],
        [Input('id-input', 'value')]
    )
    def update_table(n_clicks, id_value):
        if n_clicks > 0 and id_value is not None:
            filtered_df = Nodes.df[Nodes.df['ID'] == int(id_value)]
            return filtered_df.to_dict('records')
        else:
            return Nodes.df.to_dict('records')