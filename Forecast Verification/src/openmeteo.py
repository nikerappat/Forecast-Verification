# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 13:45:13 2026

@author: niker
"""
import requests
import pandas as pd


"""Client zum Abrufen historischer Vorhersagedaten von Open-Meteo."""

import pandas as pd
import requests

OPENMETEO_URL = "https://historical-forecast-api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT = 30  # Sekunden


def get_openmeteo_forecast(
    latitude: float,
    longitude: float,
    start_date: str,
    end_date: str,
    timezone: str = "UTC",
) -> pd.DataFrame:
    """
    Download stuendlicher 2m-Temperaturvorhersagen ueber die
    Open-Meteo Historical-Forecast-API.

    Parameters
    ----------
    latitude, longitude : float
        Koordinaten des Standorts.
    start_date, end_date : str
        ISO-Datumsangaben, z. B. "2025-07-01".
    timezone : str
        Zeitzone der zurueckgegebenen Zeitstempel. Standard ist "UTC",
        damit die Werte zu den DWD-Beobachtungen passen, die ebenfalls
        in UTC vorliegen.

    Returns
    -------
    pandas.DataFrame
        Spalten: time (datetime64), temperature_forecast (°C).
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m",
        "timezone": timezone,
    }
    response = requests.get(OPENMETEO_URL, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    data = response.json()

    if "hourly" not in data:
        raise ValueError(f"Unerwartete Antwort der Open-Meteo API: {data}")

    hourly_data = data["hourly"]
    df = pd.DataFrame({
        "time": pd.to_datetime(hourly_data["time"]),
        "temperature_forecast": hourly_data["temperature_2m"],
    })
    return df


if __name__ == "__main__":
    forecast = get_openmeteo_forecast(52.9336, 8.2370, "2025-07-01", "2025-07-31")
    print(forecast.head())