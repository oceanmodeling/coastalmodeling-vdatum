#!/usr/bin/env python3
from typing import Union
import logging
import warnings

import pyproj
import numpy as np
# pyproj.network.set_network_enabled(active=True)

from coastalmodeling_vdatum import geoid_tr
from coastalmodeling_vdatum import path

_logger = logging.getLogger(__name__)

def build_pipe(lat, lon ,z ,h_g , g_g, g_h, online, epoch=None):
    """
    Basic pipeline that is common to all transfomations.
    h_g: height - geoid
    g_g: geiod to geiod
    g_h: geoid - height
    """

    pipeline=f"""+proj=pipeline
  +step +proj=axisswap +order=2,1
  +step +proj=unitconvert +xy_in=deg +z_in=m +xy_out=rad +z_out=m
  +step +proj=vgridshift +grids={h_g} +multiplier=1
  {g_g}
  +step +proj=vgridshift +grids={g_h} +multiplier=-1
  +step +proj=unitconvert +xy_in=rad +z_in=m +xy_out=deg +z_out=m
  +step +proj=axisswap +order=2,1
    """

    if online is True:
        pyproj.network.set_network_enabled(active=True)

    tr = pyproj.Transformer.from_pipeline(pipeline).transform
    if epoch is not None:
        t=[epoch for l in lat]
        out = tr(lat,lon,z,t)
    else:
        out = tr(lat,lon,z)

    return out


def inputs(vd_from,vd_to):
    """
    Calls the respective (height - geoid), (geoid to geoid), and (geoid - height)
    transformations given the vertical datum of origin and target vertical datum
    """
    if vd_from == "xgeoid20b" and vd_to == "mllw":
        h_g = path.xGEOID20B
        g_g = geoid_tr.ITRF2014_to_ITRF2020
        g_h = path.MLLW_ITRF2020_2020
    elif vd_from == "mllw" and vd_to == "xgeoid20b":
        h_g = path.MLLW_ITRF2020_2020
        g_g = geoid_tr.ITRF2020_to_ITRF2014
        g_h = path.xGEOID20B

    elif vd_from == "xgeoid20b" and vd_to == "lmsl":
        h_g = path.xGEOID20B
        g_g = geoid_tr.ITRF2014_to_ITRF2020
        g_h = path.LMSL_ITRF2020_2020
    elif vd_from == "lmsl" and vd_to == "xgeoid20b":
        h_g = path.LMSL_ITRF2020_2020
        g_g = geoid_tr.ITRF2020_to_ITRF2014
        g_h = path.xGEOID20B

    elif vd_from == "navd88" and vd_to == "mllw":
        h_g = "us_noaa_g2018u0.tif"
        g_g = geoid_tr.NAD832011_2010_to_ITRF2020_2020
        g_h = path.MLLW_ITRF2020_2020
    elif vd_from == "mllw" and vd_to == "navd88":
        h_g = path.MLLW_ITRF2020_2020
        g_g = geoid_tr.ITRF2020_2020_to_NAD832011_2010
        g_h = "us_noaa_g2018u0.tif"

    elif vd_from == "navd88" and vd_to == "lmsl":
        h_g = "us_noaa_g2018u0.tif"
        g_g = geoid_tr.NAD832011_2010_to_ITRF2020_2020
        g_h = path.LMSL_ITRF2020_2020
    elif vd_from == "lmsl" and vd_to == "navd88":
        h_g = path.LMSL_ITRF2020_2020
        g_g = geoid_tr.ITRF2020_2020_to_NAD832011_2010
        g_h = "us_noaa_g2018u0.tif"

    elif vd_from == "mllw" and vd_to == "lmsl":
        h_g = path.MLLW_ITRF2020_2020
        g_g = None
        g_h = path.LMSL_ITRF2020_2020
    elif vd_from == "lmsl" and vd_to == "mllw":
        h_g = path.LMSL_ITRF2020_2020
        g_g = None
        g_h = path.MLLW_ITRF2020_2020

    elif vd_from == "navd88" and vd_to == "xgeoid20b":
        h_g = "us_noaa_g2018u0.tif"
        g_g = geoid_tr.NAD832011_to_ITRF2014
        g_h = path.xGEOID20B
    elif vd_from == "xgeoid20b" and vd_to == "navd88":
        h_g = path.xGEOID20B
        g_g = geoid_tr.ITRF2014_to_NAD832011
        g_h = "us_noaa_g2018u0.tif"

    else:
        warnings.warn(f"Vertical datum donversion not found. \
Datums available:'xgeoid20b','navd88','mllw','lmsl', \
datum conversion requested: from {vd_from} to {vd_to}")

    return h_g,g_g,g_h


def convert(vd_from: str,
            vd_to: str,
            lat: Union[int, float, list, np.array],
            lon: Union[int, float, list, np.array],
            z: Union[int, float, list, np.array],
            epoch: int=None,
            online = True) -> Union[list, np.array]:
    """Converts vertical datum (main function)

    Given the vertical datum of origin, the target vertical datum, 
    xyz and epoch (optional), output the xyz for the targer vertical datum.

    Parameters
    ----------
    vd_from : str
        The name of the vertical datum you want to go from, any of these:
        "xgeoid20b","navd88","mllw","lmsl"
    vd_to : str
        The name of the vertical datum you want to go to, any of these:
        "xgeoid20b","navd88","mllw","lmsl"
    lat : int or float or list or np.array
        Latitudes, e.g. [30,26,27.5] or 28.8
    lon : int or float or list or np.array
        Longitudes, e.g. [-80,-75,-77.5] or 78.8
    z : int or float or list or np.array
        Longitudes, e.g. [0,0,.1] or 10
    epoch : int [Optional]
        Default is set to None
    online : True(default) or False [Optional]
        Needs to be set to True is geotiff files (path.py) are retrieve from the web
        Can be set to False if geotiff files are stored locally (ideal for HPC compute node)

    Returns
    -------
    Lists
        Returns 3 lists (lat, lon, and z)

    Notes
    -----
    - The conversions are based on predefined geotiff files - see path.py
    - Geoid transformations use predefined proj pipelines - see geoid_tr.py
    - The size of lat, lon, and z must match.
    - Points outside the vertical datum conversion domain will be output as inf
    """

    h_g,g_g,g_h=inputs(vd_from,vd_to)
    clat,clon,cz=build_pipe(lat, lon ,z ,h_g , g_g, g_h, online, epoch=epoch)

    return clat,clon,cz


if __name__ == '__main__':

    convert(vd_from, vd_to, lat, lon ,z, epoch=None)
