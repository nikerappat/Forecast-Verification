# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 13:13:50 2026

@author: niker
"""

"""Compares Open-Meteo-Forecast with DWD-Observation for one Station."""

import pandas as pd

from dwd import get_dwd_observation
from openmeteo import get_openmeteo_forecast
from verification import calculate_bias, calculate_mae, calculate_rmse

STATION = {
    "id": "00044",
    "name": "Großenkneten",
    "latitude": 52.9336,
    "longitude": 8.2370,
}
START_DATE = "2025-07-01"
END_DATE = "2025-07-31"


def main() -> None:
    forecast = get_openmeteo_forecast(
        STATION["latitude"], STATION["longitude"], START_DATE, END_DATE
    )
    observations = get_dwd_observation(STATION["id"])

    merged = pd.merge(forecast, observations, on="time")
    if merged.empty:
        raise ValueError(
            "No overlapping timestamps between forecast and "
            "observation"
        )

    mae = calculate_mae(merged["temperature_forecast"], merged["temperature_obs"])
    bias = calculate_bias(merged["temperature_forecast"], merged["temperature_obs"])
    rmse = calculate_rmse(merged["temperature_forecast"], merged["temperature_obs"])

    print(f"Station: {STATION['name']} ({STATION['id']})")
    print(f"Zeitraum: {START_DATE} bis {END_DATE}")
    print(f"MAE:  {mae:.2f}")
    print(f"BIAS: {bias:.2f}")
    print(f"RMSE: {rmse:.2f}")


if __name__ == "__main__":
    main()