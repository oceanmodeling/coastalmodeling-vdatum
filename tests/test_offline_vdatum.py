"""Tests for offline tidal datum conversions."""

import pytest
from coastalmodeling_vdatum import vdatum, _path
import numpy

import pytest
from coastalmodeling_vdatum import vdatum, _path
import numpy
import os
import tempfile
import subprocess

@pytest.fixture(scope="module")
def setup_paths():
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.run(["wget", "-P", tmpdir, "https://noaa-nos-stofs2d-pds.s3.amazonaws.com/_archive/coastalmodeling-vdatum/us_noaa_g2018u0.tif"])
        subprocess.run(["wget", "-P", tmpdir, "https://noaa-nos-stofs2d-pds.s3.amazonaws.com/_archive/coastalmodeling-vdatum/xGEOID20B.tif"])
        subprocess.run(["wget", "-P", tmpdir, "https://noaa-nos-stofs2d-pds.s3.amazonaws.com/_archive/coastalmodeling-vdatum/us_noaa_nos_MLLW-ITRF2020_2020.0_nwldatum_4.7.0_20240621_2.tif"])
        subprocess.run(["wget", "-P", tmpdir, "https://noaa-nos-stofs2d-pds.s3.amazonaws.com/_archive/coastalmodeling-vdatum/us_noaa_nos_LMSL-ITRF2020_2020.0_nwldatum_4.7.0_20240621_2.tif"])
        _path.NAVD88_G2018 = os.path.join(tmpdir, "us_noaa_g2018u0.tif")
        _path.XGEOID20B = os.path.join(tmpdir, "xGEOID20B.tif")
        _path.MLLW_ITRF2020_2020 = os.path.join(tmpdir, "us_noaa_nos_MLLW-ITRF2020_2020.0_nwldatum_4.7.0_20240621_2.tif")
        _path.LMSL_ITRF2020_2020 = os.path.join(tmpdir, "us_noaa_nos_LMSL-ITRF2020_2020.0_nwldatum_4.7.0_20240621_2.tif")
        yield

# @pytest.mark.parametrize("vfrom, vto, lat, lon, result", [
#     ('lmsl', 'mlw', 30.197168, -87.842459, 0.183),
# ])
# def test_offline_vdatum_conversion(setup_paths, vfrom, vto, lat, lon, result):
#     tol = 0.0005 # meters
#     zs = 0.0
#     _, _, zd = vdatum.convert(vfrom, vto, lat, lon, zs, online=False, epoch=None)
#     assert numpy.abs(zd - result) <= tol, f"Converting from {vfrom} to {vto} at lat {lat}, lon{lon}; expected {result}, got {zd}"