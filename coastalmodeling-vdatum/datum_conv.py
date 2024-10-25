
import pyproj
import numpy as np
pyproj.network.set_network_enabled(active=True)

def navd88_to_xgeoid20b(lat,lon,z,t):
    nad832011_navd88geoid18_to_itrf14_2010_xgeoid20b =r"""+proj=pipeline
  +step +proj=axisswap +order=2,1
  +step +proj=unitconvert +xy_in=deg +xy_out=rad
  +step +proj=vgridshift +grids=us_noaa_g2018u0.tif +multiplier=1
  +step +proj=cart +ellps=GRS80
  +step +inv +proj=helmert +x=1.0053 +y=-1.9092 +z=-0.5416 +rx=0.0267814
        +ry=-0.0004203 +rz=0.0109321 +s=0.00037 +dx=0.0008 +dy=-0.0006
        +dz=-0.0014 +drx=6.67e-05 +dry=-0.0007574 +drz=-5.13e-05 +ds=-7e-05
        +t_epoch=2010 +convention=coordinate_frame
  +step +inv +proj=cart +ellps=GRS80
  +step +proj=vgridshift +grids=C:/Users/Felicio.Cassalho/Downloads/xGEOID20B.tif +multiplier=-1
  +step +proj=unitconvert +xy_in=rad +xy_out=deg
  +step +proj=axisswap +order=2,1"""

    t_nad832011_navd88geoid18_to_itrf14_2010_xgeoid20b = pyproj.Transformer.from_pipeline(nad832011_navd88geoid18_to_itrf14_2010_xgeoid20b).transform
    out = t_nad832011_navd88geoid18_to_itrf14_2010_xgeoid20b(lat,lon,z,t)

    return out



if __name__ == '__main__':

    print(navd88_to_xgeoid20b(np.array([40,30,10]),[-100,-80,-80],[0,0,0],[2010,2010,2010]))
