# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 13:45:13 2026

@author: niker
"""
import requests
import pandas as pd


def get_openmeteo_forecast(
    latitude,
    longitude,
    start_date,
    end_date
):

    url = (
    "https://historical-forecast-api.open-meteo.com/v1/forecast?"
    f"latitude={latitude}&"
    f"longitude={longitude}&"
    f"start_date={start_date}&"
    f"end_date={end_date}&"
    "hourly=temperature_2m"
)
    response = requests.get(url)

    data = response.json()

    hourly_data = data["hourly"]

    df = pd.DataFrame({
        "time": hourly_data["time"],
        "temperature": hourly_data["temperature_2m"]
    })

    df["time"] = pd.to_datetime(
        df["time"]
    )

    df = df.rename(
        columns={
            "temperature": "temperature_forecast"
        }
    )

    return df

if __name__ == "__main__":
    forecast = get_openmeteo_forecast(
    52.9336,
    8.2370
)
    print(forecast.head())