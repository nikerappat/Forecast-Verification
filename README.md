# Forecast Verification Tool

Comparison of Open-Meteo hourly temperature forecasts against observational data from the German Weather Service (DWD), including calculation of standard forecast verification metrics (MAE, RMSE, Bias).

## Overview

This tool downloads a historical weather forecast for a given location and time range, downloads the corresponding observed measurements from a nearby DWD weather station, aligns both datasets by timestamp, and calculates how accurate the forecast was.

## Data Sources

- **Forecast**: [Open-Meteo Historical Forecast API](https://open-meteo.com/en/docs/historical-forecast-api)
- **Observations**: [DWD Open Data](https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/air_temperature/historical/), hourly air temperature

## Verification Metrics

| Metric | Description |
|---|---|
| MAE | Mean Absolute Error — average magnitude of forecast error |
| RMSE | Root Mean Square Error — penalizes larger errors more strongly than MAE |
| Bias | Mean signed error — positive means the forecast overestimated temperature, negative means it underestimated |

## Features

- Fetch historical hourly temperature forecasts from the Open-Meteo Historical Forecast API
- Fetch hourly temperature observations from DWD Open Data
- Automatically resolve the correct DWD archive filename per station (no hardcoded date ranges — the DWD file naming includes a station-specific date range, which is looked up dynamically)
- Merge forecast and observation data on matching timestamps
- Calculate MAE, RMSE, and Bias
- Handle missing DWD measurements correctly — the DWD convention marks missing values as `-999`, which is flagged as `NaN` before any metric is computed

## Project Structure

```
├── src/
   ├── main.py            # Entry point: orchestrates the full workflow
   ├── dwd.py              # DWD station list and observation data client
   ├── openmeteo.py         # Open-Meteo forecast data client
   ├── verification.py       # Forecast verification metrics (MAE, RMSE, Bias)
└── README.md
```

## Requirements

- Python 3.9+
- pandas
- numpy
- requests

```bash
pip install pandas numpy requests
```

## Usage

Configure the station and time range in `main.py`:

```python
STATION = {
    "id": "00044",
    "name": "Großenkneten",
    "latitude": 52.9336,
    "longitude": 8.2370,
}
START_DATE = "2025-07-01"
END_DATE = "2025-07-31"
```

Then run:

```bash
python main.py
```

Example output:

```
Station: Großenkneten (00044)
Zeitraum: 2025-07-01 bis 2025-07-31
MAE:  0.62
BIAS: -0.15
RMSE: 0.83
```

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

## Known Limitations

- Only hourly air temperature (`temperature_2m` / `TT_TU`) is currently supported.
- DWD historical archives are only updated periodically; very recent observations may not yet be available.
- Network access is required at runtime; no local caching of downloaded data.

## Roadmap

- Support multiple stations in a single run
- Add additional verification metrics (e.g. correlation, skill score)
- Add automated tests for the data-fetching and merge logic





