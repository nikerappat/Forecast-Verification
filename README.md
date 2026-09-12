# Forecast Verification Tool

Comparison of Open-Meteo hourly temperature forecasts against observational data from the German Weather Service (DWD), including calculation of standard forecast verification metrics (MAE, RMSE, Bias), correlation and visualisation of results.

## Overview

This tool downloads a historical weather forecast for a given location and time range, downloads the corresponding observed measurements from a DWD weather station at that location, aligns both datasets by timestamp, and calculates how accurate the forecast was.

## Working Hypothesis

Forecast quality depends on the station's elevation. Higher-elevation stations show a greater discrepancy between the forecast and the observation than lower-elevation stations.

## Data Sources

- **Forecast**: [Open-Meteo Historical Forecast API](https://open-meteo.com/en/docs/historical-forecast-api)
- **Observations**: [DWD Open Data](https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/air_temperature/historical/), hourly air temperature

## Verification Metrics

| Metric | Description |
|---|---|
| MAE | Mean Absolute Error — average magnitude of forecast error |
| RMSE | Root Mean Square Error — penalizes larger errors more strongly than MAE |
| Bias | Mean signed error — positive means the forecast overestimated temperature, negative means it underestimated |
| Correlation | Correlation describes the strength and direction of the linear relationship between two variables. |

In this project, the Pearson correlation coefficient (r) is used. Its value ranges from -1 to +1:

- r = +1 → perfect positive linear relationship
- r = 0 → no linear relationship
- r = -1 → perfect negative linear relationship

A positive correlation means that higher values of one variable tend to be associated with higher values of the other variable. A negative correlation means that higher values of one variable tend to be associated with lower values of the other.

Correlation indicates an association, not causation. A strong correlation therefore does not necessarily mean that one variable causes changes in the other. In this project, correlation is used to evaluate how closely forecasted temperatures follow observed temperatures.

## Features

- Fetch historical hourly temperature forecasts from the Open-Meteo Historical Forecast API
- Fetch hourly temperature observations from DWD Open Data
- Automatically resolve the correct DWD archive filename per station (no hardcoded date ranges — the DWD file naming includes a station-specific date range, which is looked up dynamically)
- Merge forecast and observation data on matching timestamps
- Calculate MAE, RMSE, and Bias
- Handle missing DWD measurements correctly — the DWD convention marks missing values as `-999`, which is flagged as `NaN` before any metric is computed
- Categorize stations by height:

  | Category | Description |
  |---|---|
  | low | station height < 200 m |
  | mid | station height between 200 m and 500 m |
  | elevated | station height between 500 m and 1000 m |
  | high | station height > 1000 m |

- Calculate correlation between height and RMSE
- Scatter plot of height vs. RMSE incl. corresponding regression line

## Project Structure

```
Forecast-Verification/
├── Forecast Verification/
│   ├── src/
│   │   ├── main.py                 # Entry point for regular use: loads metrics, analyzes and plots results
│   │   ├── generate_metrics.py     # One-off/occasional: fetches data and (re)computes forecast-vs-observation metrics per DWD station
│   │   ├── dwd.py                  # DWD station list and observation data client
│   │   ├── openmeteo.py            # Open-Meteo forecast data client
│   │   └── verification.py         # Forecast verification metrics (MAE, RMSE, Bias)
│   ├── results/
│   │   └── stations_metrics.json   # Per-station metrics (MAE, Bias, RMSE, Pearson r) for stations with full data coverage in the configured time period
│   └── plots/
│       ├── height_rmse_low.png
│       ├── height_rmse_medium.png
│       ├── height_rmse_elev.png
│       └── height_rmse_high.png
└── README.md
```

## Requirements

- Python 3.9+
- pandas
- numpy
- matplotlib
- requests

```bash
pip install pandas numpy matplotlib requests
```

## Usage and Results

### 1. Single station of interest

Configure the time range in `generate_metrics.py`, then uncomment the following block in `main.py`:

```python
from generate_metrics import load_filtered_stations, stations_metrics

# type in the ID of the chosen station
filtered_list = load_filtered_stations()
station = next(
    s for s in filtered_list.itertuples(index=False)
    if s.station_id == "00164"
)
complete_pairs, mae, bias, rmse, r = stations_metrics(station)
plot_corr(complete_pairs, station.name, r, mae, bias, rmse,
          save_path=f"../Forecast Verification/plots/correlation_metrics_{station.name}.png")
```

Example output:

```
Station: Angermünde (00164)
period: 2025-01-01 to 2025-07-31
complete forecast-observation pairs: 5087 (99.98%)
excluded due to NaN: 1 (0.02%)
MAE:  0.56
BIAS: -0.18
RMSE: 0.77
pearson correlation coefficient: 0.996
```

![Scatter plot for Angermünde showing resulting metrics](Forecast%20Verification/plots/correlation_metrics_Angermünde.png)

### 2. Full set of stations with available data in the chosen time period

Configure the time range in `generate_metrics.py`, run it once to (re)generate `results/stations_metrics.json`, then run `main.py`.

Categorizing data by station height and calculating metrics:

```python
low_stations[["height", "rmse"]].corr()
mid_stations[["height", "rmse"]].corr()
higher_stations[["height", "rmse"]].corr()
high_stations[["height", "rmse"]].corr()
```

Correlation between station height and RMSE:

| Station category | correlation (r) |
|---|---|
| low | 0.397 |
| mid | -0.033 |
| elevated | 0.176 |
| high | 0.314 |
| overall | 0.27 |

- **Low:** r = 0.397 — at lower elevations, RMSE tends to increase with altitude.
- **Mid:** r = -0.033 — indicates virtually no linear relationship.
- **Elevated:** r = 0.176 — a slight positive trend, but rather weak.
- **High:** r = 0.314 — RMSE tends to increase with altitude, but note: there are only five stations above 1000 m, so this result should be treated with caution.

Observations:
- The correlation is not evenly distributed across all elevation ranges.
- The range ≤200 m, in particular, shows a significantly stronger correlation.
- In the 200–500 m range, the correlation disappears almost entirely.

![Scatter plot Station Height vs. Temperature Forecast RMSE low stations](Forecast%20Verification/plots/height_rmse_low.png)
![Scatter plot Station Height vs. Temperature Forecast RMSE mid stations](Forecast%20Verification/plots/height_rmse_medium.png)
![Scatter plot Station Height vs. Temperature Forecast RMSE elevated stations](Forecast%20Verification/plots/height_rmse_elev.png)
![Scatter plot Station Height vs. Temperature Forecast RMSE high stations](Forecast%20Verification/plots/height_rmse_high.png)

## Module Reference

### `openmeteo.py`

| Function | Description |
|---|---|
| `get_openmeteo_forecast(latitude, longitude, start_date, end_date, timezone="UTC")` | Downloads hourly 2 m temperature forecasts for the given location and date range. Returns a `DataFrame` with columns `time` and `temperature_forecast`. |

### `dwd.py`

| Function | Description |
|---|---|
| `get_station_list()` | Downloads metadata for all DWD air temperature stations. |
| `get_dwd_observation(station_id)` | Downloads and parses hourly air temperature observations for a station. Returns a `DataFrame` with columns `time` and `temperature_obs`. |

### `verification.py`

| Function | Description |
|---|---|
| `calculate_mae(forecast, observation)` | Mean Absolute Error. |
| `calculate_rmse(forecast, observation)` | Root Mean Square Error. |
| `calculate_bias(forecast, observation)` | Mean signed error. |

### `generate_metrics.py`

| Function | Description |
|---|---|
| `load_filtered_stations()` | Loads DWD stations that have available data across the full configured time range. |
| `stations_metrics(station)` | Fetches forecast and observation data for one station and calculates the metrics defined in `verification.py`, using only complete pairs (NaN values excluded). Returns `(complete_pairs, mae, bias, rmse, r)`. |
| `main()` | Loops over all filtered stations and returns a dictionary of per-station metrics, which is saved to `results/stations_metrics.json`. |

### `main.py`

| Function | Description |
|---|---|
| `plot_corr(df, station, r, mae, bias, rmse, save_path=None)` | Scatter plot of forecast vs. observed temperature for a single station. |
| `plot_height_rmse(df, category)` | Scatter plot of station height vs. RMSE with a linear regression line. Always shown interactively; no save option yet. |

## Known Limitations

- Only hourly air temperature (`temperature_2m` / `TT_TU`) is currently supported.
- DWD historical archives are only updated periodically; very recent observations may not yet be available.
- Network access is required at runtime; no local caching of downloaded data.
- Only five stations fall into the "high elevation" (>1000 m) group, so results for that category should be treated with caution.

## Roadmap

- Add a `save_path` option to `plot_height_rmse`, matching `plot_corr`, so height/RMSE plots can be saved automatically
- Add additional verification metrics (e.g. skill score)
- Significance testing
- Add automated tests for the data-fetching and merge logic
