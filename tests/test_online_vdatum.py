"""Simple tests for tidal datum conversions against vdatum online.

The 'result' in each of the tests below was taken from 
    https://vdatum.noaa.gov/vdatumweb/
specifying height = 0.0 in the source datum at the specified lat,lon.

The online results are to 3 decimal places (in meters), so the tolerance
is intended to be equivalent.

"""


import sys
sys.path.append('..')
from coastalmodeling_vdatum import vdatum
import numpy

def main():
    tol = 0.0005 # meters
    
    tests = [
        {'vfrom':'lmsl', 'vto':'mlw', 'lat':30.197168, 'lon':-87.842459, 'result':0.183},
        {'vfrom':'lmsl', 'vto':'mllw', 'lat':30.197168, 'lon':-87.842459, 'result':0.198},
        {'vfrom':'lmsl', 'vto':'mhw', 'lat':30.197168, 'lon':-87.842459, 'result':-0.187},
        {'vfrom':'lmsl', 'vto':'lmsl', 'lat':30.197168, 'lon':-87.842459, 'result':0.0}
    ]
    
    for t in tests:
        s = t['vfrom']
        d = t['vto']
        y = t['lat']
        x = t['lon']
        zs = 0.0
        _, _, zd = vdatum.convert(s, d, y, x, zs, online=True, epoch=None)
        assert numpy.abs(zd - t['result']) <= tol, \
            f"Converting from {s} to {d} at lat {y}, lon{x}; expected {t['result']}, got {zd}"

if __name__ == '__main__':
    main()
