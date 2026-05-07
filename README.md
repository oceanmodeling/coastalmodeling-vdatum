# CoastalModeling-VDatum

.. image:: https://badge.fury.io/py/coastalmodeling-vdatum.svg
    :target: https://badge.fury.io/py/coastalmodeling-vdatum

.. image:: https://github.com/oceanmodeling/coastalmodeling-vdatum/actions/workflows/run-tests.yml/badge.svg
    :target: https://github.com/oceanmodeling/coastalmodeling-vdatum/actions/workflows/run-tests.yml

.. image:: https://github.com/oceanmodeling/coastalmodeling-vdatum/actions/workflows/docs.yml/badge.svg
    :target: https://oceanmodeling.github.io/coastalmodeling-vdatum/

.. image:: https://codecov.io/gh/oceanmodeling/coastalmodeling-vdatum/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/oceanmodeling/coastalmodeling-vdatum

.. image:: https://img.shields.io/badge/License-CC0%201.0-lightgrey.svg
    :target: http://creativecommons.org/publicdomain/zero/1.0/

.. image:: https://img.shields.io/badge/pylint-?.??-blue
    :target: https://github.com/oceanmodeling/coastalmodeling-vdatum/actions/workflows/lint.yml

`coastalmodeling-vdatum` is a Python package designed to support coastal modelers with vertical datum conversions.

Conversions between the following datums are supported:
`xgeoid20b`, `navd88`, `mllw`, `mlw`, `mhhw`, `mhw`, `lmsl`, `igld85`, and `lwd`.

## Key Features

- **Flexible Datum Conversions**: Supports a wide range of vertical datums commonly used in coastal modeling.
- **Online and Offline Modes**: Can perform conversions using either online services or locally stored geotiff files.
- **Mesh and Grid Support**: Includes tools for converting the vertical datum of entire meshes and grids.
- **Integration with Other Tools**: Designed to work with other popular coastal modeling tools like `OCSMesh` and `pylibs`.

## Installation

You can install `coastalmodeling-vdatum` from PyPI:

```bash
pip install coastalmodeling-vdatum
```

Alternatively, you can install the latest development version directly from GitHub:

```bash
pip install "git+https://github.com/oceanmodeling/coastalmodeling-vdatum.git"
```

For a conda-based installation, you can create a new environment and install the package using pip:

```bash
conda create --name cmvd python=3.11
conda activate cmvd
pip install coastalmodeling-vdatum
```

## Usage

### Vertical Datum Conversion

The main function for datum conversion is `vdatum.convert`.

```python
from coastalmodeling_vdatum import vdatum

x, y, z = vdatum.convert(vd_from, vd_to, lat, lon, z, online=True, epoch=None)
```

### Offline Conversions

For offline use (e.g., on a compute node with no internet access), you can download the necessary geotiff files and point the package to their local paths.

The required files can be downloaded from [here](https://noaa-nos-stofs2d-pds.s3.amazonaws.com/index.html#_archive/coastalmodeling-vdatum/).

```python
from coastalmodeling_vdatum import vdatum, _path

PATH = "/path/to/your/geotiff/files"

_path.NAVD88_G2018 = f"{PATH}/us_noaa_g2018u0.tif"
_path.XGEOID20B = f"{PATH}/xGEOID20B.tif"
_path.MLLW_ITRF2020_2020 = f"{PATH}/us_noaa_nos_MLLW-ITRF2020_2020.0_nwldatum_4.7.0_20240621_2.tif"
_path.LMSL_ITRF2020_2020 = f"{PATH}/us_noaa_nos_LMSL-ITRF2020_2020.0_nwldatum_4.7.0_20240621_2.tif"

x, y, z = vdatum.convert(vd_from, vd_to, lat, lon, z, online=False, epoch=None)
```

### Mesh Vertical Datum Conversion

`coastalmodeling-vdatum` can be used to update mesh bathymetry in conjunction with other tools like `OCSMesh` or `pylibs`.

#### With OCSMesh

```python
from coastalmodeling_vdatum import vdatum
import ocsmesh
import numpy as np

gd = ocsmesh.Mesh.open(HGRID_PATH, crs=4326)

# coastalmodeling-vdatum expects positive z overland and negative z under water,
# thus multiply gd.value by -1
x, y, z = vdatum.convert(
    vd_from,
    vd_to,
    gd.vert2['coord'][:, -1],
    gd.vert2['coord'][:, 0],
    gd.value * -1,
    online=True,
    epoch=None
)
z[np.isinf(z)] = gd.value[np.isinf(z)]

mesh_msht = ocsmesh.utils.msht_from_numpy(
    coordinates=gd.vert2['coord'],
    triangles=gd.tria3['index'],
    quadrilaterals=gd.quad4['index'] if len(gd.quad4['index']) > 0 else None,
    crs=4326
)

mesh_msht.value = np.array(z)

ocsmesh.Mesh(mesh_msht).write(f"{PATH_OUT}/mesh.2dm", format='2dm', overwrite=True)
```

#### With pylibs

```python
from coastalmodeling_vdatum import vdatum
from pylib import schism_grid as read_hgrid

gd = read_hgrid(HGRID_PATH)

# coastalmodeling-vdatum expects positive z overland and negative z under water,
# thus multiply gd.value by -1
x, y, z = vdatum.convert(vd_from, vd_to, gd.y, gd.x, -gd.z, online=True, epoch=None)
z = -z
z[np.isinf(z)] = gd.z[np.isinf(z)]

gd.dp = z

gd.write_hgrid(f"{PATH_OUT}/mesh.gr3")
```

## Contributing

We welcome contributions! If you have ideas for new features, find a bug, or would like to improve the documentation, please open an issue or submit a pull request.

## License

This project is licensed under the terms of the CC0 1.0 Universal license. See the `LICENSE.txt` file for details.

## Citation

If you use `coastalmodeling-vdatum` in your work, please cite the following publication:

Cassalho, F., Riley, J., Moghimi, S., Reeves Eyre, J., Mani, S., Seroka, G., Peeri, S., Myers, E., Allen, C. (2026) Coastal Modeling Vertical Datum Package. NOAA technical memorandum NOS CS; 62. https://doi.org/10.25923/tdec-td80

---
  
#### Disclaimer
This repository is a scientific product and is not official communication of the National Oceanic and Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project code is provided on an "as is" basis and the user assumes responsibility for its use. Any claims against the Department of Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.
