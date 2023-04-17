import dash
from dash.dependencies import Input, Output, State
from dash import dcc, ctx
from dash import html

import plotly.express as px

def serve_layout():
        
    return html.Div([
        html.Header([
            html.H1('Radio Interferometry 101'),
            html.Img(src='logo.png', alt='logo', width='100', height='100')
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
                    ]),
                    html.Div([
                        html.P('antennas configuration'),
                        dcc.Dropdown(
                            id='antennas_configuration',
                            options=[
                                {'label': 'VLA', 'value': 'vla'},
                                {'label': 'MeerKat', 'value': 'meerkat'},
                                {'label': 'WSRT', 'value': 'wsrt'},
                                {'label': 'Kat-7', 'value': 'kat-7'},
                            ],
                            value='kat-7'
                        ),
                        dcc.Dropdown(
                            id='sky_model',
                            options=[
                                {'label': 'Gaussian source', 'value': 'gaussian_source'},
                                {'label': 'Gaussian ellipspoids', 'value': 'ellipsoids'},
                                {'label': 'Point source', 'value': 'point_source'},
                                {'label': 'M31 radiogalaxy', 'value': 'm31'}
                            ],
                            value='gaussian_source'
                        ),
                        html.P('synthesis time'),
                        dcc.Input(
                            type='number',
                            name='synthesis_time',
                            id='synthesis_time',
                            min=0,
                            max=12,
                            value=1
                        ),
                        html.P('integration time'),
                        dcc.Input(
                            type='number',
                            name='integration_time',
                            id='integration_time',
                            min=0,
                            max=36000,
                            value=60
                        ),
                        html.P('observation wavelength'),
                        dcc.Input(
                            type='number',
                            name='wavelength',
                            id='wavelength',
                            min=0,
                            max=10,
                            value=0.1
                        ),
                        html.P('pointing direction (declination)'),
                        dcc.Input(
                            type='number',
                            name='pointing_direction',
                            id='pointing_direction',
                            min=0,
                            max=100,
                            value=35
                        ),
                        html.P('right ascension of the source direction is considered to be in the zenith at middle of the observation')
                    ]),
                    html.Div([
                        html.P('description'),
                        html.Button('Compute UV', id='btn'),
                    ])
                ])
            ])
        ])
    ])
