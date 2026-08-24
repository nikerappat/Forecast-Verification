# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 14:23:09 2026

@author: niker
"""
"""Download and Parse DWD-observational data (temperature, hourly)."""

import re
import zipfile
from io import BytesIO

import pandas as pd
import requests

DWD_STATION_URL = (
    "https://opendata.dwd.de/climate_environment/CDC/observations_germany/"
    "climate/hourly/air_temperature/historical/TU_Stundenwerte_Beschreibung_Stationen.txt"
)
DWD_DATA_URL = (
    "https://opendata.dwd.de/climate_environment/CDC/observations_germany/"
    "climate/hourly/air_temperature/historical/"
)
REQUEST_TIMEOUT = 30  # secs
MISSING_VALUE = -999  # DWD-notion for missing values


def get_station_list() -> pd.DataFrame:
    """
    Download of DWD-Stationsmetadaten.

    Returns
    -------
    pandas.DataFrame
        cols: station_id, from_date, to_date, height, latitude,
        longitude, name.
    """
    response = requests.get(DWD_STATION_URL, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    lines = response.text.splitlines()
    stations = []
    for line in lines[2:]:
        parts = line.split()
        if len(parts) >= 8:
            stations.append({
                "station_id": parts[0],
                "from_date": parts[1],
                "to_date": parts[2],
                "height": parts[3],
                "latitude": parts[4],
                "longitude": parts[5],
                "name": parts[6],
            })

    df = pd.DataFrame(stations)
    # numbered cols come from text file as string
    for col in ("height", "latitude", "longitude"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def _find_station_zip_filename(station_id: str) -> str:
    """
    gives station name from archive file
    timeframe is dependent on station (no hard coding possible) - read from DWD-Verzeichnislisting
    """
    response = requests.get(DWD_DATA_URL, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    pattern = rf"stundenwerte_TU_{station_id}_\d{{8}}_\d{{8}}_hist\.zip"
    match = re.search(pattern, response.text)
    if not match:
        raise ValueError(
            f"no historic data for Station '{station_id}' found."
        )
    return match.group(0)


def get_dwd_observation(station_id: str) -> pd.DataFrame:
    """
    Download and Parse hourly tempeature data from one station

    Parameters
    ----------
    station_id : str
        DWD-Stations number, z. B. "00044".

    Returns
    -------
    pandas.DataFrame
        cols: time (datetime64), temperature_obs (°C).
    """
    filename = _find_station_zip_filename(station_id)
    url = DWD_DATA_URL + filename

    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
        data_file = next(
            name for name in zip_file.namelist()
            if name.startswith("produkt_tu_stunde")
        )
        with zip_file.open(data_file) as f:
            df = pd.read_csv(f, sep=";", skipinitialspace=True)

    df["MESS_DATUM"] = pd.to_datetime(df["MESS_DATUM"].astype(str), format="%Y%m%d%H")
    df = df[["MESS_DATUM", "TT_TU"]].rename(
        columns={"MESS_DATUM": "time", "TT_TU": "temperature_obs"}
    )

    df["temperature_obs"] = df["temperature_obs"].replace(MISSING_VALUE, pd.NA)

    return df


if __name__ == "__main__":
    stations = get_station_list()
    print(stations.head())

    observations = get_dwd_observation("00044")
    print(observations.head())