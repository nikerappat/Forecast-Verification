# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 11:57:20 2026

@author: niker
"""

"""Calculates Forecast-vs-Observation-metrics per DWD-Station and saves it
in ../results/stations_metrics.json.

Re-Calculate whenever START_DATE / END_DATE changes because that might change which of the stations
has available data for that period
"""

import json
import pandas as pd

from dwd import get_dwd_observation, get_station_list
from openmeteo import get_openmeteo_forecast
from verification import calculate_bias, calculate_mae, calculate_rmse, pearson_corr

START_DATE = pd.Timestamp("2025-01-01")
END_DATE = pd.Timestamp("2025-07-31")


def load_filtered_stations() -> pd.DataFrame:
    # load DWD station list and filter for set dates
    stations_list = get_station_list()
    stations_list["from_date"] = pd.to_datetime(stations_list["from_date"], format="%Y%m%d")
    stations_list["to_date"] = pd.to_datetime(stations_list["to_date"], format="%Y%m%d")

    mask = (stations_list["from_date"] <= START_DATE) & (stations_list["to_date"] >= END_DATE)
    return stations_list.loc[mask]


def stations_metrics(station) -> tuple[pd.DataFrame, float, float, float, float]:
    # call functions to calculate metrics
    forecast = get_openmeteo_forecast(
        station.latitude,
        station.longitude,
        START_DATE.strftime("%Y-%m-%d"),
        END_DATE.strftime("%Y-%m-%d"),
    )
    observations = get_dwd_observation(station.station_id)

    merged = pd.merge(forecast, observations, on="time")
    if merged.empty:
        raise ValueError("No overlapping timestamps between forecast and observation")

    cols = ["temperature_forecast", "temperature_obs"]
    is_na = merged[cols].isna().any(axis=1)
    complete_pairs = merged.loc[~is_na, cols]

    n_total = len(merged)
    n_na = int(is_na.sum())
    n_complete = n_total - n_na
    perc_na = round((n_na / n_total) * 100, 2)
    perc_comp = round((n_complete / n_total) * 100, 2)

    mae = calculate_mae(complete_pairs["temperature_forecast"], complete_pairs["temperature_obs"])
    bias = calculate_bias(complete_pairs["temperature_forecast"], complete_pairs["temperature_obs"])
    rmse = calculate_rmse(complete_pairs["temperature_forecast"], complete_pairs["temperature_obs"])
    r = pearson_corr(complete_pairs)  # erwartet den vollständigen DataFrame

    print(f"Station: {station.name} ({station.station_id})")
    print(f"period: {START_DATE.date()} to {END_DATE.date()}")
    print(f"complete forecast-observation pairs: {n_complete} ({perc_comp}%)")
    print(f"excluded due to NaN: {n_na} ({perc_na}%)")
    print(f"MAE:  {mae:.2f}")
    print(f"BIAS: {bias:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"pearson correlation coefficient: {r:.3f}")

    return complete_pairs, mae, bias, rmse, r


def main() -> dict:
    #calculates metrics for all stations within the filtered list
    filtered_list = load_filtered_stations()
    stations_dict = {}

    for station in filtered_list.itertuples(index=False):
        try:
            _, mae, bias, rmse, r = stations_metrics(station)
            stations_dict[station.station_id] = {
                "name": station.name,
                "height": station.height,
                "latitude": station.latitude,
                "longitude": station.longitude,
                "mae": mae,
                "bias": bias,
                "rmse": rmse,
                "pearson_r": r,
            }
        except ValueError as e:
            print(f"Station {station.station_id} skipped: {e}")

    return stations_dict


if __name__ == "__main__":
    results = main()
    with open("../results/stations_metrics.json", "w") as f:
        json.dump(results, f, indent=4)

    # ---Debugging ------------------------------------
    # filtered_list = load_filtered_stations()
    # station = next(
    #     s for s in filtered_list.itertuples(index=False)
    #     if s.station_id == "00164"
    # )
    # complete_pairs, mae, bias, rmse, r = stations_metrics(station)