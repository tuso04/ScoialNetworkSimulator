from dash import html, dcc, Dash

layout = [
    html.H1('Paremeter input', style={'textAlign': 'center'}),
    html.Hr(),
    html.Div('Network Participants'),
    dcc.Input(id='anteil_Networkparticipant', value="", type='number', style={'width': '300px', 'height': '30px', 'margin-bottom': '15px'}, placeholder='Enter the number of Network Participants'),
    html.Br(),
    html.Div('Bots'),
    dcc.Input(id= 'anteil_Bots', type='number', value="", style={'width': '300px', 'height': '30px', 'margin-bottom': '15px'}, placeholder='Enter the number of Bots'),
    html.Br(),
    html.Div('Influencer'),
    dcc.Input(id= 'anteil_Influencer', value="", type='number', style={'width': '300px', 'height': '30px', 'margin-bottom': '15px'}, placeholder='Enter the number of Influencers'),
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
]
