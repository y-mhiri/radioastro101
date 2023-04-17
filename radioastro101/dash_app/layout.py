import dash
from dash.dependencies import Input, Output, State
from dash import dcc, ctx
from dash import html

import plotly.express as px

def entry_layout(description, component):
    return html.Div([ 
        html.P(description),
        component
       ], className='entry')

def serve_layout():
        
    return html.Div([
        html.Header([
            html.H1('Radio Interferometry 101'),
            html.Img(src='/opt/radioastro101/data/misc/logo.svg', alt='logo', width='100', height='100')
        ]),

        # html.Nav([
        #     html.Ul([
        #         html.Li(html.A('Home', href='main.html')),
        #         html.Li(html.A('About', href='about.html')),
        #         html.Li(html.A('Contact', href='contact.html'))
        #     ])
        # ]),

        html.Main([
            html.P('Radio interferometry is a technique used in radio astronomy to create images of celestial objects by combining signals from multiple antennas.'),

            html.Div([
                html.H2('Array configuration'),

                html.Div([
                    html.Div([
                        dcc.Graph(id='array_configuration', figure=px.scatter())
                    ], id='figure'),
                    html.Div([
                        html.Div([html.P('Array configuration'),
                        dcc.Dropdown(
                            id='antennas_configuration',
                            options=[
                                {'label': 'VLA', 'value': 'vla'},
                                {'label': 'MeerKat', 'value': 'meerkat'},
                                {'label': 'WSRT', 'value': 'wsrt'},
                                {'label': 'Kat-7', 'value': 'kat-7'},
                            ],
                            value='kat-7'
                        )], className='entry'),
                        
                        entry_layout("Sky model : ",
                        dcc.Dropdown(
                            id='sky_model',
                            options=[
                                {'label': 'Gaussian source', 'value': 'gaussian_source'},
                                {'label': 'Gaussian ellipspoids', 'value': 'ellipsoids'},
                                {'label': 'Point source', 'value': 'point_source'},
                                {'label': 'M31 radiogalaxy', 'value': 'm31'}
                            ],
                            value='gaussian_source'
                        )
                        )
                        ,
                        entry_layout('Synthesis time',
                        dcc.Input(
                            type='number',
                            name='synthesis_time',
                            id='synthesis_time',
                            min=0,
                            max=12,
                            value=1
                            # className="input"
                        )),
                        entry_layout('Integration time',
                        dcc.Input(
                            type='number',
                            name='integration_time',
                            id='integration_time',
                            min=0,
                            max=36000,
                            value=60
                        )),
                        entry_layout('Observation wavelength',
                        dcc.Input(
                            type='number',
                            name='wavelength',
                            id='wavelength',
                            min=0,
                            max=10,
                            value=0.1
                        )),
                        entry_layout('Pointing direction (declination)',
                        dcc.Input(
                            type='number',
                            name='pointing_direction',
                            id='pointing_direction',
                            min=0,
                            max=100,
                            value=35
                        )),
                    ]),
                    html.Div([
                        html.P('description'),
                        html.Button('Run', id='btn'),
                    ])
                ])
            ])
        ])
    ])
