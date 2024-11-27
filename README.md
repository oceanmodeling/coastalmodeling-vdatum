# coastalmodeling-vdatum
To support costal modelers with vertical datum conversion

### Installation 
`pip install "git+https://github.com/oceanmodeling/coastalmodeling-vdatum.git"` 

## Vertical Datum Conversion
The package can be loaded as:
```
from coastalmodeling_vdatum import vdatum

x,y,z = vdatum.convert(vd_from, vd_to, lat, lon ,z, online=True, epoch=None) #where vd_from and vd_to are: "xgeoid20b","navd88","mllw", or"lmsl"
```
