# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 14:23:09 2026

@author: niker
"""
import requests
import pandas as pd
import zipfile
from io import BytesIO


DWD_STATION_URL = (
    "https://opendata.dwd.de/"
    "climate_environment/CDC/"
    "observations_germany/"
    "climate/hourly/"
    "air_temperature/"
    "historical/"
    "TU_Stundenwerte_Beschreibung_Stationen.txt"
)

DWD_DATA_URL = (
    "https://opendata.dwd.de/"
    "climate_environment/CDC/"
    "observations_germany/"
    "climate/hourly/"
    "air_temperature/"
    "historical/"
)


def get_station_list():
    """
    Download DWD station metadata.

    Returns
    -------
    pandas.DataFrame
        Station information
    """


    response = requests.get(DWD_STATION_URL)

    response.raise_for_status()

    lines = response.text.splitlines()

    stations = []
    
    for line in lines[2:]:
    
        parts = line.split()
    
        if len(parts) >= 8:
    
            station = {
                "station_id": parts[0],
                "from_date": parts[1],
                "to_date": parts[2],
                "height": parts[3],
                "latitude": parts[4],
                "longitude": parts[5],
                "name": parts[6],
            }
    
            stations.append(station)
    
    
    df = pd.DataFrame(stations)
    
    return df




def get_dwd_observation(station_id):

    filename = (
        f"stundenwerte_TU_{station_id}_20070401_20251231_hist.zip"
    )

    url = DWD_DATA_URL + filename

    response = requests.get(url)

    response.raise_for_status()

    zip_file = zipfile.ZipFile(
        BytesIO(response.content)
    )

    data_file = (
        f"produkt_tu_stunde_20070401_20251231_{station_id}.txt"
    )
    
    with zip_file.open(data_file) as f:
        df = pd.read_csv(
    f,
    sep=";",
    skipinitialspace=True
)
    df["MESS_DATUM"] = pd.to_datetime(
    df["MESS_DATUM"].astype(str),
    format="%Y%m%d%H"
)
    df = df[["MESS_DATUM", "TT_TU"]]
    df.rename(
        columns={
            "MESS_DATUM": "time",
            "TT_TU": "temperature_obs"
        },
        inplace=True
    )
    
    # print(df.head())
    # print(df.columns)
    return df




if __name__ == "__main__":

    stations = get_station_list()

    station_id = "00044"

    get_dwd_observation(station_id)
