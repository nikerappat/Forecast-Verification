# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 13:45:13 2026

@author: niker
"""
import requests
import pandas as pd


def get_forecast():
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        "latitude=52.52&"
        "longitude=13.41&"
        "hourly=temperature_2m"
    )

    response = requests.get(url)

    data = response.json()
    hourly_data = data["hourly"]
    
    df = pd.DataFrame({
        "time": hourly_data["time"],
        "temperature": hourly_data["temperature_2m"]
    })

    return df


if __name__ == "__main__":
    forecast = get_forecast()
    print(forecast.head())