import numpy as np

from astropy.coordinates import EarthLocation,SkyCoord
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import AltAz

from .linalg import Rz, Ry
from PIL import Image

from ducc0.wgridder import ms2dirty
from scipy.constants import speed_of_light

def rotate_antenna_positions(antenna_positions, telescope_location):
    """ 
    Rotate the antenna positions to align X with the meridian

    Parameters
    ----------
    antenna_positions : array   
        Antenna positions (in meters)
    telescope_location : tuple
        longitude, latitude of the telescope (in degrees, degrees)
        
    Returns
    -------
    antenna_positions : array
        Rotated antenna positions (in meters)
    """

    # Compute the Right Ascension at the Meridian (RAM) of the observatory
    lon  = telescope_location[0]

    # Rotate the antenna positions
    R = np.array([[np.cos(lon), np.sin(lon), 0],
                  [-np.sin(lon), np.cos(lon), 0],
                  [0, 0, 1]])
    antenna_positions = np.dot(R, antenna_positions.T).T

    return antenna_positions

def compute_baselines(antenna_positions):
    """
    Compute the baselines between antennas.
    Antenna positions are assumed to be in the ITRF frame rotated such that X
    is aligned with the local meridian.

    Parameters
    ----------
    antenna_positions : array
        Antenna positions (in meters)
    
    Returns
    -------
    uvw : array
        Baselines (in meters)

    """

    nant = antenna_positions.shape[0]
    
    nbaselines = nant * (nant - 1) // 2
    uvw = np.zeros((nbaselines, 3))
    ant_index = np.zeros((nbaselines, 2), dtype=int)
    for k, (i,j) in enumerate(zip(*np.triu_indices(nant, k=1))):
        uvw[k,:] = antenna_positions[i, :] - antenna_positions[j, :]
        ant_index[k, :] = [i, j]
        
    return uvw, ant_index

def project_baselines(baselines, H0, dec0):
    """
    Compute the projection matrix for the uv plane
    """

    # Compute the rotation matrix
    R = np.array([[np.sin(H0), np.cos(H0), 0],
                     [-np.sin(dec0) * np.cos(H0), np.sin(H0) * np.sin(dec0), np.cos(dec0)],
                     [np.cos(H0) * np.cos(dec0), -np.cos(dec0) * np.sin(H0), np.sin(dec0)]])
    
    return np.dot(R, baselines.T).T



def compute_uvw_synthesis(synthesis_time, integration_time, dec,
                           antenna_positions, telescope_location, snapshot=False, zenith=False):
    """
    Compute the uvw coordinates for a synthesis observation

    Parameters
    ----------
    synthesis_time : float
        Total synthesis time (in hours)
    integration_time : float
        Integration time (in seconds)
    dec : float
        Declination of the source (in degrees)
    antenna_positions : array
        Antenna positions (in meters)  
    telescope_location : tuple
        longitude, latitude of the telescope (in degrees, degrees)
        
    Returns
    -------
    uvw : array
        uvw coordinates (in meters)
    """

    # Compute the number of integrations
    
    antenna_positions = rotate_antenna_positions(antenna_positions, telescope_location)
    baselines, ant_index_baselines = compute_baselines(antenna_positions)

    # Compute the uvw coordinates for each integration
    if zenith:
        dec = telescope_location[1]
    else:
        dec = dec * np.pi/180

    if snapshot:
        uvw = np.zeros((1, baselines.shape[0], 3))
        return project_baselines(baselines, 0, dec), ant_index_baselines
    
    n_integrations = int(synthesis_time*3600/integration_time)
    uvw = np.zeros((n_integrations, baselines.shape[0], 3))
    ant_index = np.zeros((n_integrations, baselines.shape[0], 2), dtype=int)
    H = np.linspace(-synthesis_time/2, synthesis_time/2, n_integrations)

    for k, H0 in enumerate(H):
        # Compute the hour angle at the middle of the integration
        H0_rad = H0*360/24 * np.pi/180
        uvw[k,:,:] = project_baselines(baselines, H0_rad, dec)
        ant_index[k,:,:] = ant_index_baselines
    
    return uvw.reshape(-1, 3), ant_index.reshape(-1, 2)



def load_sky_model(path):
    img =  np.array(Image.open(path).convert('L')).squeeze()
    # check if sky image dimension are even and if not, remove the last row and column
    if img.shape[0] % 2 != 0:
        img = img[:-1, :]
    if img.shape[1] % 2 != 0:
        img = img[:, :-1]
    return img



def compute_dirty_beam(uvw, wavelength, npix_x=512, npix_y=512, cellsize=None):
    """
    Compute the dirty beam using the w-projection algorithm from ducc0

    Parameters
    ----------
    uvw : array
        Baselines (in meters)
    wavelength : float
        Wavelength (in meters)
    npix_x : int
        Number of pixels in the x direction
    npix_y : int
        Number of pixels in the y direction
    cellsize : float
        Cell size (in meters)
    
    """

    if cellsize is None:
        cellsize = 1 / (2*np.max(uvw))
    
    freq = np.array([speed_of_light / wavelength])
    print('Cell size: {:.7f} rad'.format(cellsize))
    print('Frequency: {:.2f} GHz'.format(freq[0]/1e9))
          
    # Compute the dirty beam
    dirty_beam = ms2dirty(
                    uvw = uvw,
                    freq = freq,
                    ms = np.ones((len(uvw), 1)).astype(np.complex64),
                    npix_x = npix_x,
                    npix_y = npix_y,
                    pixsize_x = cellsize,
                    pixsize_y = cellsize,
                    epsilon=1.0e-5).real
        

    return dirty_beam


def compute_dirty_image(dirty_beam, sky_image):
    """
    Compute the dirty image by convolving the dirty beam with the sky image using FFTs

    Parameters
    ----------
    dirty_beam : array
        Dirty beam
    sky_image : array
        Sky image

    Returns
    -------
    dirty_image : array
        Dirty image

    """

    # Compute the dirty image
    dirty_image = np.fft.fftshift(np.fft.ifft2(np.fft.fft2(sky_image) * np.fft.fft2(dirty_beam))).real

    return dirty_image
