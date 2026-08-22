# Forecast Verification Tool

Comparison of Open Meteo hourly temperature forecasts against observational data from German Weather Service (DWD).

Calculation of Standard forecast verification metrics (MAE, RMSE, Bias).



Download of historical weather forecasts for a given Location and time from nearby DWD weather Station.

Alignment of DWD and Open Meteo data by timestamp.

Calculation of forecast accuracy.



1. Data Sources
* Open-Meteo
* DWD



2\. Calculated verification metrics

* MAE
* RMSE
* Bias



3\. Content

* fetch historical hourly temperature forecasts from the Open Meteo Historical Forecasts API
* fetch hourly temperature observations from DWD Open Data
* automatically resolve the correct DWD Archive file Name of the Station
* merge forecast and Observation on matching time stamps
* calculate MAE, RMSE and bias
* missing values are -999 as per DWD convention; flagged as NaN



Project is still in the works and will be updated continually.



