"""Simple tests for tidal datum conversions against vdatum online.

The 'result' in each of the tests below was taken from 
    https://vdatum.noaa.gov/vdatumweb/
specifying height = 0.0 in the source datum at the specified lat,lon.

The online results are to 3 decimal places (in meters), so the tolerance
is intended to be equivalent.

"""

import pytest
from coastalmodeling_vdatum import vdatum
import numpy


@pytest.mark.parametrize("vfrom, vto, lat, lon, result", [
    ('lmsl', 'mlw', 30.197168, -87.842459, 0.183),
    ('lmsl', 'mllw', 30.197168, -87.842459, 0.198),
    ('lmsl', 'mhw', 30.197168, -87.842459, -0.187),
    ('lmsl', 'lmsl', 30.197168, -87.842459, 0.0)
])
def test_online_vdatum_conversion(vfrom, vto, lat, lon, result):
    tol = 0.0005 # meters
    zs = 0.0
    _, _, zd = vdatum.convert(vfrom, vto, lat, lon, zs, online=True, epoch=None)
    assert numpy.abs(zd - result) <= tol, \
        f"Converting from {vfrom} to {vto} at lat {lat}, lon{lon}; expected {result}, got {zd}"
