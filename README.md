# coastalmodeling-vdatum
To support costal modelers with vertical datum conversion.\
Conversions between the following datums are suported: 
__xgeoid20b__, __navd88__, __mllw__, and __lmsl__.

## Installation 
```
conda create --name cmvd python=3.11
conda activate cmvd
pip install "git+https://github.com/oceanmodeling/coastalmodeling-vdatum.git"
```

## Usage Examples:
### Vertical Datum Conversion
The package can be used as:
```
from coastalmodeling_vdatum import vdatum

x,y,z = vdatum.convert(vd_from, vd_to, lat, lon , z, online=True, epoch=None)
```

### Compute Node (offline) Applications
coastalmodeling-vdatum can be used offline (no aws connection) by 
changing the pre-defined geotiff file paths to a local directory
(the geotiff files can be downloaded from [here](https://noaa-nos-stofs2d-pds.s3.amazonaws.com/index.html#_archive/coastalmodeling-vdatum/)):
```
from coastalmodeling_vdatum import vdatum, _path

_path.NAVD88_G2018=f"{PATH}/us_noaa_g2018u0.tif"
_path.xGEOID20B=f"{PATH}/xGEOID20B.tif"
_path.MLLW_ITRF2020_2020=f"{PATH}/us_noaa_nos_MLLW-ITRF2020_2020.0_nwldatum_4.7.0_20240621_.tif"
_path.LMSL_ITRF2020_2020f"{PATH}/us_noaa_nos_LMSL-ITRF2020_2020.0_nwldatum_4.7.0_20240621_.tif"

x,y,z = vdatum.convert(vd_from, vd_to, lat, lon , z, online=False, epoch=None)
```

### Mesh Vertical Datum Conversion (SCHISM-[OCSMesh](https://github.com/noaa-ocs-modeling/OCSMesh/tree/main))
coastalmodeling-vdatum can be used update mesh bathymetry via OCSMesh.
```
from coastalmodeling_vdatum import vdatum
import ocsmesh
import numpy as np

gd = ocsmesh.Mesh.open(HGRID_PATH, crs=4326)

x,y,z = vdatum.convert(vd_from, vd_to, gd.vert2['coord'][:, -1], gd.vert2['coord'][:, 0] , gd.value, online=True, epoch=None)
z[np.isinf(z)] = gd.value[np.isinf(z)]

mesh_msht = ocsmesh.utils.msht_from_numpy(
        coordinates=gd.vert2['coord'],
        triangles=gd.tria3['index'],
        quadrilaterals=gd.quad4['index'] if len(gd.quad4['index']) > 0 else None,
        crs=4326
    )

mesh_msht.value= np.array(z)

ocsmesh.Mesh(mesh_msht).write({PATH_OUT}/mesh.2dm, format='2dm', overwrite=True)
```

### Mesh Vertical Datum Conversion (SCHISM-[pylibs](https://github.com/wzhengui/pylibs))
coastalmodeling-vdatum can be used update mesh bathymetry via pylibs.
```
from coastalmodeling_vdatum import vdatum
from pylib import schism_grid as read_hgrid

gd = read_hgrid(HGRID_PATH)

x,y,z = vdatum.convert(vd_from, vd_to, gd.y, gd.x , gd.z, online=True, epoch=None)
z[np.isinf(z)] = gd.z[np.isinf(z)]
gd.dp=z

gd.write_hgrid({PATH_OUT}/mesh.gr3')
```

