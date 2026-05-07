"""Tests for offline tidal datum conversions."""

import pytest
from coastalmodeling_vdatum import vdatum, _path
import numpy

@pytest.fixture(scope="module")
def setup_paths():
    # This fixture can be used to download the necessary files if they don't exist
    # For now, it assumes the files are present at a known location.
    # In a real-world scenario, you might want to automatically download these from
    # https://noaa-nos-stofs2d-pds.s3.amazonaws.com/index.html#_archive/coastalmodeling-vdatum/
    PATH = "/home/Felicio.Cassalho/coastalmodeling-vdatum/geotiff_files" # IMPORTANT: Update this path
    _path.NAVD88_G2018 = f"{PATH}/us_noaa_g2018u0.tif"
    _path.XGEOID20B = f"{PATH}/xGEOID20B.tif"
    _path.MLLW_ITRF2020_2020 = f"{PATH}/us_noaa_nos_MLLW-ITRF2020_2020.0_nwldatum_4.7.0_20240621_2.tif"
    _path.LMSL_ITRF2020_2020 = f"{PATH}/us_noaa_nos_LMSL-ITRF2020_2020.0_nwldatum_4.7.0_20240621_2.tif"

# @pytest.mark.parametrize("vfrom, vto, lat, lon, result", [
#     ('lmsl', 'mlw', 30.197168, -87.842459, 0.183),
# ])
# def test_offline_vdatum_conversion(setup_paths, vfrom, vto, lat, lon, result):
#     tol = 0.0005 # meters
#     zs = 0.0
#     _, _, zd = vdatum.convert(vfrom, vto, lat, lon, zs, online=False, epoch=None)
#     assert numpy.abs(zd - result) <= tol, f"Converting from {vfrom} to {vto} at lat {lat}, lon{lon}; expected {result}, got {zd}"