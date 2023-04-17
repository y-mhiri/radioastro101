import dash
from dash.dependencies import Input, Output, State
from dash import dcc, ctx
from dash import html
import datetime
import pandas as pd
import time
import uuid
import os

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import zarr
import numpy as np

from ducc0.wgridder import ms2dirty
from scipy.constants import speed_of_light

from radioastro101.utility.synthesis import compute_uvw_synthesis, load_sky_model, compute_dirty_beam, compute_dirty_image

from radioastro101.utility.mstozarr import load_telescope_from_itrf
from radioastro101 import ROOT_DIR



from layout import serve_layout

app = dash.Dash()
# cache = Cache(app.server, config={
#     'CACHE_TYPE': 'filesystem',
#     'CACHE_DIR': 'cache-directory',
#     'CACHE_THRESHOLD': 50  # should be equal to maximum number of active users
# })





    
    

app.layout = serve_layout




@app.callback(
    Output('array_configuration', 'figure'),
    [State('antennas_configuration', 'value'),
    State('synthesis_time', 'value'),
    State('integration_time', 'value'),
    State('pointing_direction', 'value'),
    State('wavelength', 'value'),
    State('sky_model', 'value'),
    Input('btn', 'n_clicks')]
)
def generate_antenna_plot(antennas_configuration, synthesis_time, integration_time, pointing_direction, wavelength, sky_model, n_clicks):
    antenna_positions, telescope_location_lon_lat = load_telescope_from_itrf(f'/opt/radioastro101/data/telescopes/{antennas_configuration}.itrf')

    uvw_snapshot, _ = compute_uvw_synthesis(antenna_positions=
    antenna_positions,
                                telescope_location=telescope_location_lon_lat,
                                dec=pointing_direction,
                                synthesis_time=synthesis_time,
                                integration_time=integration_time,
                                snapshot=True)
    
    uvw, _ = compute_uvw_synthesis(antenna_positions=
    antenna_positions,
                                telescope_location=telescope_location_lon_lat,
                                dec=pointing_direction,
                                synthesis_time=synthesis_time,
                                integration_time=integration_time,
                                snapshot=False)


    # add conjugate points
    uvw = np.concatenate((uvw, -uvw), axis=0)
    uvw_snapshot = np.concatenate((uvw_snapshot, -uvw_snapshot), axis=0)

    
    sky_image =  load_sky_model(f'/opt/radioastro101/data/sky_models/{sky_model}.png')


    dirty_beam = compute_dirty_beam(uvw, wavelength, npix_x=sky_image.shape[0], npix_y=sky_image.shape[1])
    dirty_image = compute_dirty_image(dirty_beam, sky_image)

    uvw = uvw / wavelength 
    uvw_snapshot = uvw_snapshot / wavelength 

    fig = make_subplots(rows=2, cols=3)

   # use a colormap relevant to astronomy 
    fig.add_trace(go.Heatmap(z=dirty_image, colorscale='viridis', showscale=False), row=1, col=1)
    fig.add_trace(go.Heatmap(z=dirty_beam, colorscale='viridis', showscale=False), row=1, col=2)
    fig.add_trace(go.Heatmap(z=sky_image, colorscale='viridis', showscale=False), row=1, col=3)


    fig.add_trace(go.Scatter(x=antenna_positions[:, 0], y=antenna_positions[:, 1], mode='markers', name='antenna positions'), row=2, col=1)
    fig.add_trace(go.Scatter(x=uvw[:, 0], y=uvw[:, 1], mode='markers', name='uvw'), row=2, col=2)
    fig.add_trace(go.Scatter(x=uvw_snapshot[:, 0], y=uvw_snapshot[:, 1], mode='markers', name='uvw snapshot'), row=2, col=3)

    # remove the grid lines
    fig.update_xaxes(showgrid=False, row=2, col=1)
    fig.update_yaxes(showgrid=False, row=2, col=1)
    fig.update_xaxes(showgrid=False, row=2, col=2)
    fig.update_yaxes(showgrid=False, row=2, col=2)
    fig.update_xaxes(showgrid=False, row=2, col=3)
    fig.update_yaxes(showgrid=False, row=2, col=3)

    # remove ticks for antenna positions
    fig.update_xaxes(showticklabels=False, row=2, col=1)
    fig.update_yaxes(showticklabels=False, row=2, col=1)
    fig.update_xaxes(showticklabels=False, row=2, col=2)
    fig.update_yaxes(showticklabels=False, row=2, col=2)
    fig.update_xaxes(showticklabels=False, row=2, col=3)
    fig.update_yaxes(showticklabels=False, row=2, col=3)


    # # have only extreme values for the ticks 
    # fig.update_xaxes(tickvals=[np.min(uvw[:, 0]), np.max(uvw[:, 0])], row=1, col=2)
    # fig.update_yaxes(tickvals=[np.min(uvw[:, 1]), np.max(uvw[:, 1])], row=1, col=2)
    # fig.update_xaxes(tickvals=[np.min(uvw_snapshot[:, 0]), np.max(uvw_snapshot[:, 0])], row=1, col=3)
    # fig.update_yaxes(tickvals=[np.min(uvw_snapshot[:, 1]), np.max(uvw_snapshot[:, 1])], row=1, col=3)


    

 
    fig.update_xaxes(showticklabels=False, row=1, col=1)
    fig.update_yaxes(showticklabels=False, row=1, col=1)
    fig.update_xaxes(showticklabels=False, row=1, col=2)
    fig.update_yaxes(showticklabels=False, row=1, col=2)
    fig.update_xaxes(showticklabels=False, row=1, col=3)
    fig.update_yaxes(showticklabels=False, row=1, col=3)


    fig.update_xaxes(title_text="x [m]", row=2, col=1)
    fig.update_yaxes(title_text="y [m]", row=2, col=1)
    fig.update_xaxes(title_text="u [m]", row=2, col=2)
    fig.update_yaxes(title_text="v [m]", row=2, col=2)
    fig.update_xaxes(title_text="u [m]", row=2, col=3)
    fig.update_yaxes(title_text="v [m]", row=2, col=3)

    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", showlegend=False)


        



    fig.update_layout()
    print("here")

    return fig



# @app.callback(
#     Output('skymodel', 'figure'),
#     [Input('btn', 'n_clicks'),
#     State('wavelength', 'value'),
#     State('synthesis-time', 'value'),
#     State('integration-time', 'value'),
#     State('declination', 'value')]
# )
# def generate_skymodel(n_clicks, wavelength, synthesis_time, integration_time, declination):
#     if n_clicks is None:
#         n_clicks = 0

#     # convert to float
#     wavelength = float(wavelength)
#     synthesis_time = float(synthesis_time)
#     integration_time = float(integration_time)
#     declination = float(declination)
    

#     print(declination)
#     simObj = ViSim( freq=speed_of_light/wavelength,
#                     synthesis_time=synthesis_time,
#                     integration_time=integration_time,
#                     dec=declination,
#                     npixel=512,
#                     do_sim=False)
#     sky_model = simObj.simulate_sky_image()

#     vis = simObj.simulate_noise_free_visibilities(sky_model)
#     dirty_image = simObj.compute_dirty_image(vis=vis)

#     antenna_positions = simObj.antenna_positions
#     uvw = simObj.uvw
#     uvw = np.concatenate((uvw,-uvw), axis=0)
#     freq = simObj.freq


#     # show image and dirty image in the same figure
#     fig = make_subplots(rows=2, cols=2)
#     # use appropriate colormap for astronomical images
#     fig.add_trace(go.Heatmap(z=sky_model, colorscale='gray'), row=1, col=1)
#     fig.add_trace(go.Heatmap(z=dirty_image, colorscale='gray'), row=1, col=2)
#     fig.add_trace(go.Scatter(x=uvw[:,0], y=uvw[:,1], mode='markers'), row=2, col=1)
#     fig.add_trace(go.Scatter(x=antenna_positions[:,0], y=antenna_positions[:,2], mode='markers'), row=2, col=2)
#     fig.update_layout(height=800, width=800, title_text="Sky model")
#     fig.update_xaxes(title_text="u (m)", row=2, col=1)
#     fig.update_yaxes(title_text="v (m)", row=2, col=1)
#     fig.update_xaxes(title_text="x (m)", row=2, col=2)
#     fig.update_yaxes(title_text="y (m)", row=2, col=2)
#     return fig

if __name__ == '__main__':
    app.run_server(port=8050, debug=True)
    
    
    