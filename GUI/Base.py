from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from parameter_input import Parameter_input
from network_graph import Network_graph
from nodes import Nodes

class Base:

    app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True)
    app.title = "Networksimulation"


    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
    }

    CONTENT_STYLE = {
        "margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
    }

    sidebar = html.Div(
        [
            html.H1("Menu", className="display-2"),
            html.Hr(),
            html.P(
                "Network Simulation based on Siepermanns Model", className="lead"
            ),
            dbc.Nav(
                [
                    dbc.NavLink("Parameter input", href="/", active="exact"),
                    dbc.NavLink("Network", href="/Network", active="exact"),
                    dbc.NavLink("Nodes", href="/Nodes", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=SIDEBAR_STYLE,
    )

    hidden_div = html.Div(id='hidden-div', style={'display': 'none'})

    content = html.Div(id="page-content", children=[hidden_div], style=CONTENT_STYLE)


    app.layout = html.Div([
        dcc.Location(id="url"),
        sidebar,
        content
    ])

    @app.callback(
        Output("page-content", "children"),
        [Input("url", "pathname")]
    )
    def render_page_content(pathname):
        if pathname == "/":
            return Parameter_input.parameter_layout
        elif pathname == "/Network":
            return Network_graph.network_layout
        elif pathname == "/Nodes":
            return Nodes.nodes_layout

    if __name__ == '__main__':
        app.run_server(debug=True)