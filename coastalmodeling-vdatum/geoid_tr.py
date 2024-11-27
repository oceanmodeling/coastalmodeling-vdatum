#!/usr/bin/env python3

ITRF2020_to_ITRF2014 = """\
    +step +proj=cart +ellps=GRS80
    +step +inv +proj=helmert +x=0.0014 +y=0.0009 +z=-0.0014 +rx=0 +ry=0 +rz=0 \
        +s=0.00042 +dx=0 +dy=0.0001 +dz=-0.0002 +drx=0 +dry=0 +drz=0 +ds=0 \
        +t_epoch=2015 +convention=position_vector \
    +step +inv +proj=cart +ellps=GRS80"""

ITRF2014_to_ITRF2020 = """\
    +step +proj=cart +ellps=GRS80
    +step +proj=helmert +x=0.0014 +y=0.0009 +z=-0.0014 +rx=0 +ry=0 +rz=0 \
        +s=0.00042 +dx=0 +dy=0.0001 +dz=-0.0002 +drx=0 +dry=0 +drz=0 +ds=0 \
        +t_epoch=2015 +convention=position_vector \
    +step +inv +proj=cart +ellps=GRS80"""

ITRF2020_2020_to_NAD832011_2010 = """\
    +step +proj=cart +ellps=GRS80 \
    +step +proj=set +v_4=2010 \
    +step +proj=helmert \
        +dx=0.00037 +dy=0.00035 +dz=0.00074 +drx=0.000045 +dry=-0.000666 +drz=-0.000098 \
        +t_epoch=2020 \
        +convention=position_vector \
    +step +proj=set +v_4=2010 \
    +step +inv +proj=helmert +x=0.0014 +y=0.0009 +z=-0.0014 +rx=0 +ry=0 +rz=0 \
        +s=0.00042 +dx=0 +dy=0.0001 +dz=-0.0002 +drx=0 +dry=0 +drz=0 +ds=0 \
        +t_epoch=2015 \
        +convention=position_vector \
    +step +proj=set +v_4=2010 \
    +step +proj=helmert +x=1.0053 +y=-1.9092 +z=-0.5416 +rx=0.0267814 \
        +ry=-0.0004203 +rz=0.0109321 +s=0.00037 +dx=0.0008 +dy=-0.0006 \
        +dz=-0.0014 +drx=6.67e-05 +dry=-0.0007574 +drz=-5.13e-05 +ds=-7e-05 \
        +t_epoch=2010 \
        +convention=coordinate_frame \
    +step +inv +proj=cart +ellps=GRS80"""

NAD832011_2010_to_ITRF2020_2020 = """\
  +step +proj=cart +ellps=GRS80 \
    +step +proj=set +v_4=2010 \
    +step +inv +proj=helmert \
        +dx=0.00037 +dy=0.00035 +dz=0.00074 +drx=0.000045 +dry=-0.000666 +drz=-0.000098 \
        +t_epoch=2020 \
        +convention=position_vector \
    +step +proj=set +v_4=2010 \
    +step +proj=helmert +x=0.0014 +y=0.0009 +z=-0.0014 +rx=0 +ry=0 +rz=0 \
        +s=0.00042 +dx=0 +dy=0.0001 +dz=-0.0002 +drx=0 +dry=0 +drz=0 +ds=0 \
        +t_epoch=2015 \
        +convention=position_vector \
    +step +proj=set +v_4=2010 \
    +step +inv +proj=helmert +x=1.0053 +y=-1.9092 +z=-0.5416 +rx=0.0267814 \
        +ry=-0.0004203 +rz=0.0109321 +s=0.00037 +dx=0.0008 +dy=-0.0006 \
        +dz=-0.0014 +drx=6.67e-05 +dry=-0.0007574 +drz=-5.13e-05 +ds=-7e-05 \
        +t_epoch=2010 \
        +convention=coordinate_frame \
  +step +inv +proj=cart +ellps=GRS80"""

NAD832011_to_ITRF2014 = """\
  +step +proj=cart +ellps=GRS80
  +step +inv +proj=helmert +x=1.0053 +y=-1.9092 +z=-0.5416 +rx=0.0267814
        +ry=-0.0004203 +rz=0.0109321 +s=0.00037 +dx=0.0008 +dy=-0.0006
        +dz=-0.0014 +drx=6.67e-05 +dry=-0.0007574 +drz=-5.13e-05 +ds=-7e-05
        +t_epoch=2010 +convention=coordinate_frame
  +step +inv +proj=cart +ellps=GRS80"""

ITRF2014_to_NAD832011 = """\
  +step +proj=cart +ellps=GRS80
  +step +proj=helmert +x=1.0053 +y=-1.9092 +z=-0.5416 +rx=0.0267814
        +ry=-0.0004203 +rz=0.0109321 +s=0.00037 +dx=0.0008 +dy=-0.0006
        +dz=-0.0014 +drx=6.67e-05 +dry=-0.0007574 +drz=-5.13e-05 +ds=-7e-05
        +t_epoch=2010 +convention=coordinate_frame
  +step +inv +proj=cart +ellps=GRS80"""
