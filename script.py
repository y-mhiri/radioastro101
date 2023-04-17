from radioastro101.utility.synthesis import compute_uvw_synthesis, load_sky_model, compute_dirty_beam, compute_dirty_image
from radioastro101.utility.mstozarr import load_telescope_from_itrf

import os
import numpy as np

import pandas as pd

if __name__ == '__main__':

    H = np.linspace(-4,4, 8*3600/10)
    for file in os.listdir("/Users/y/Nextcloud/PRO/Workspace/Perso/WebApps/astro/radioastro101/data/telescope"):
            if 'itrf' in file:
                df = pd.DataFrame(columns=['uvw', 'time_index', 'declination'])
                antenna_positions, telescope_location_lon_lat = load_telescope_from_itrf(file)

                for dec in np.linspace(-90,90, 360):
                    uvw, _ = compute_uvw_synthesis(antenna_positions=
                                             antenna_positions,
                                            telescope_location=telescope_location_lon_lat,
                                            dec=dec,
                                            synthesis_time=8,
                                            integration_time=10,
                                            snapshot=False)

                    