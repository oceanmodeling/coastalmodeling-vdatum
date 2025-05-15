#!/usr/bin/env python3
from typing import Union
import logging
import warnings

def read_station_in(file_path: str,
                    skip_lines: int=2,
                   ) -> list:
    """
    Reads the station.in file in the following format:

    1 1 1 1 1 1 1 1 1 !on (1)|off(0) flags for elev,air pressure,windx,windy,T,S,u,v,w,rest of tracers (expanded into subclasses of each module)
    3 !# of stations
    1 -81.871 26.648 0 !8725520
    2 -81.8075030 26.1317010 0 !8725110
    3 -81.808333 24.550833 0 !8724580

    and returns a list for each variable: index, lon, lat, z, and station name

    Parameters
    ----------    
    file_path : str
        Path to the station.in file
    skip_lines : int
        Number of lines that will be skiped when reading the file.
        default = 2

    Returns
    -------
    Lists
        Returns 5 lists: index,longitude,latitude,elevation,station

    Notes
    -----
    - 
    """

    index,longitude,latitude,elevation,station=[],[],[],[],[]
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for n,line in enumerate(lines[skip_lines:]):
            if line.strip():
                try:
                    parsed=line.split('!')
                    parsed,comment=parsed[0],parsed[-1]
                    parsed = parsed.split(' ')
                    idx,lon,lat,z = int(parsed[0]),float(parsed[1]),float(parsed[2]),float(parsed[3])
                    index.append(idx)
                    longitude.append(lon)
                    latitude.append(lat)
                    elevation.append(z)
                    station.append(comment)
                except:
                    raise ValueError(f"Please review your station.in. Failed to parse line {skip_lines+n+1}")

        return index,longitude,latitude,elevation,station
