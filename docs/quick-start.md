# Quick Start

## Vertical Datum Conversion

The main function for datum conversion is `vdatum.convert`.

```python
from coastalmodeling_vdatum import vdatum

x, y, z = vdatum.convert(vd_from, vd_to, lat, lon, z, online=True, epoch=None)
```

## Offline Conversions

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

## Mesh Vertical Datum Conversion

`coastalmodeling-vdatum` can be used to update mesh bathymetry in conjunction with other tools like `OCSMesh` or `pylibs`.

### With OCSMesh

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

### With pylibs

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
