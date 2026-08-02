# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 13:13:50 2026

@author: niker
"""

from dwd import get_dwd_observation
from openmeteo import get_openmeteo_forecast
import inspect
import openmeteo
import pandas as pd

station = {
    "id": "00044",
    "name": "Großenkneten",
    "latitude": 52.9336,
    "longitude": 8.2370
}


forecast = get_openmeteo_forecast(
    station["latitude"],
    station["longitude"],
    "2025-07-01",
    "2025-07-31"
)


observations = get_dwd_observation(
    station["id"]
)

merged = pd.merge(
    forecast,
    observations,
    on="time"
)

from verification import calculate_bias, calculate_mae, calculate_rmse

mae = calculate_mae(merged["temperature_forecast"], merged["temperature_obs"])
bias = calculate_bias(merged["temperature_forecast"], merged["temperature_obs"])
rmse = calculate_rmse(merged["temperature_forecast"], merged["temperature_obs"])

print("MAE:", mae)
print("BIAS:", bias)
print("RMSE:", rmse)