# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 13:13:50 2026

@author: niker
"""

"""loads pre calculated Forecast-vs-Observation-metrics and plots them.

Prerequisite: ../results/stations_metrics.json already exists.
If it does not (or if START_DATE/END_DATE in generate_metrics.py have been changed),
first run `generate_metrics.py`.
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Only necessary if you want to regenerate the metrics or view a single station
# in detail (see the example at the very bottom):
# from generate_metrics import load_filtered_stations, stations_metrics, main as generate_all_metrics

with open("../results/stations_metrics.json", "r") as f:
    stations_dict = json.load(f)

stations_df = pd.DataFrame.from_dict(stations_dict, orient="index")

low_stations = stations_df[stations_df["height"] <= 200]
mid_stations = stations_df[(stations_df["height"] > 200) & (stations_df["height"] <= 500)]
higher_stations = stations_df[(stations_df["height"] > 500) & (stations_df["height"] <= 1000)]
high_stations = stations_df[stations_df["height"] > 1000]


def plot_corr(df: pd.DataFrame, station: str, r: float, mae: float, bias: float, rmse: float) -> None:
    #"Scatterplot of forecast vs. observed temperature for a single station.

    #df/r/mae/bias/rmse are obtained from generate_metrics.stations_metrics(station).
    
    x = df["temperature_forecast"].to_numpy(dtype=float)
    y = df["temperature_obs"].to_numpy(dtype=float)

    fig, ax = plt.subplots()
    ax.scatter(x, y, color="green", alpha=0.1, s=5)

    lo = min(x.min(), y.min())
    hi = max(x.max(), y.max())
    ax.plot([lo, hi], [lo, hi], color="black", linewidth=2)

    ax.set_xlabel("Forecasted Temperature [°C]")
    ax.set_ylabel("Observed Temperature [°C]")
    ax.set_title(f"2m Temperature Forecast vs. Observation {station}")
    ax.text(
        0.05, 0.75,
        f"Pearson r = {r:.3f}\nMAE = {mae:.2f} °C\nBias = {bias:.2f} °C\nRMSE = {rmse:.2f} °C",
        transform=ax.transAxes, bbox=dict(boxstyle="round", alpha=0.8),
    )
    plt.show()
    plt.close(fig)


def plot_height_rmse(df: pd.DataFrame, category: str, save_path: str | None = None) -> None:
    #Plots station elevation against RMSE, including a linear regression.
    #Hypothesis: Forecast quality depends on station elevation.
    #Works for any DataFrame with more than one station (e.g., filtered by elevation).
    
    x = df["height"]
    y = df["rmse"]

    fig, ax = plt.subplots()

    slope, intercept = np.polyfit(x, y, 1)
    x_reg = np.linspace(x.min(), x.max(), 100)
    y_reg = slope * x_reg + intercept
    ax.plot(x_reg, y_reg, linewidth=2)

    ax.scatter(x, y, alpha=0.5)

    ax.set_xlabel("Station Height [m]")
    ax.set_ylabel("RMSE [°C]")
    ax.set_title(f"Station Height vs. Temperature Forecast RMSE {category}")

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    else:
        plt.show()
    plt.close(fig)


plot_height_rmse(low_stations, "Low Stations < 200 m", "../plots/height_rmse_low.png")
plot_height_rmse(mid_stations, "Mid Stations > 200 m & < 500 m", "../plots/height_rmse_medium.png")
plot_height_rmse(higher_stations, "Elevated Stations > 500 m & < 1000 m", "../plots/height_rmse_elev.png")
plot_height_rmse(high_stations, "High Stations > 1000 m", "../plots/height_rmse_high.png")


# --- Example: Look up and plot a specific station in real time---------------
# from generate_metrics import load_filtered_stations, stations_metrics
#
# type in the ID of the chosen station
# filtered_list = load_filtered_stations()
# station = next(
#     s for s in filtered_list.itertuples(index=False)
#     if s.station_id == "00164"
# )
# complete_pairs, mae, bias, rmse, r = stations_metrics(station)
# plot_corr(complete_pairs, station.name, r, mae, bias, rmse)