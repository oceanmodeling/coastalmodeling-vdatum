#!/usr/bin/env python3

import pyproj

import geoid_tr
import path

def transform(lat, lon ,z ,h_g , g_g, g_h, epoch=None):
    """
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
    tr = pyproj.Transformer.from_pipeline(pipeline).transform
    if epoch is not None:
        t=[epoch for l in lat]
        out = tr(lat,lon,z,t)
    else:
        out = tr(lat,lon,z)

    return out


def inputs(vd_from,vd_to):
    if vd_from == "xgeoid20b" and vd_to == "mllw":
        h_g = xGEOID20B
        g_g = ITRF2014_to_ITRF2020
        g_h = MLLW_ITRF2020_2020
    if vd_from == "mllw" and vd_to == "xgeoid20b":
        h_g = MLLW_ITRF2020_2020
        g_g = ITRF2020_to_ITRF2014
        g_h = xGEOID20B

    if vd_from == "xgeoid20b" and vd_to == "lmsl":
        h_g = xGEOID20B
        g_g = ITRF2014_to_ITRF2020
        g_h = LMSL_ITRF2020_2020
    if vd_from == "lmsl" and vd_to == "xgeoid20b":
        h_g = LMSL_ITRF2020_2020
        g_g = ITRF2020_to_ITRF2014
        g_h = xGEOID20B

    if vd_from == "navd88" and vd_to == "mllw":
        h_g = "us_noaa_g2018u0.tif"
        g_g = NAD832011_2010_to_ITRF2020_2020
        g_h = MLLW_ITRF2020_2020
    if vd_from == "mllw" and vd_to == "navd88":
        h_g = MLLW_ITRF2020_2020
        g_g = ITRF2020_2020_to_NAD832011_2010
        g_h = "us_noaa_g2018u0.tif"

    if vd_from == "navd88" and vd_to == "lmsl":
        h_g = "us_noaa_g2018u0.tif"
        g_g = NAD832011_2010_to_ITRF2020_2020
        g_h = LMSL_ITRF2020_2020
    if vd_from == "lmsl" and vd_to == "navd88":
        h_g = LMSL_ITRF2020_2020
        g_g = ITRF2020_2020_to_NAD832011_2010
        g_h = "us_noaa_g2018u0.tif"

    if vd_from == "mllw" and vd_to == "lmsl":
        h_g = MLLW_ITRF2020_2020
        g_g = None
        g_h = LMSL_ITRF2020_2020
    if vd_from == "lmsl" and vd_to == "mllw":
        h_g = LMSL_ITRF2020_2020
        g_g = None
        g_h = MLLW_ITRF2020_2020

    if vd_from == "navd88" and vd_to == "xgeoid20b":
        h_g = "us_noaa_g2018u0.tif"
        g_g = NAD832011_to_ITRF2014
        g_h = xGEOID20B
    if vd_from == "xgeoid20b" and vd_to == "navd88":
        h_g = xGEOID20B
        g_g = ITRF2014_to_NAD832011
        g_h = "us_noaa_g2018u0.tif"

    else:
        pass

    return h_g,g_g,g_h


def main(vd_from, vd_to, lat, lon ,z, epoch=None):
    """
    """
    h_g,g_g,g_h=inputs(vd_from,vd_to)
    clat,clon,cz=transform(lat, lon ,z ,h_g , g_g, g_h, epoch=epoch)

    return clat,clon,cz


if __name__ == '__main__':

    main(vd_from, vd_to, lat, lon ,z, epoch=None)
