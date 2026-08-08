# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 14:09:03 2026

@author: niker
"""

""" (MAE, RMSE, Bias) for forecasts."""

import numpy as np
import numpy.typing as npt


def calculate_mae(forecast: npt.ArrayLike, observation: npt.ArrayLike) -> float:
    """Calculate Mean Absolute Error."""
    error = np.asarray(forecast) - np.asarray(observation)
    return float(np.mean(np.abs(error)))


def calculate_rmse(forecast: npt.ArrayLike, observation: npt.ArrayLike) -> float:
    """Calculate Root Mean Square Error."""
    error = np.asarray(forecast) - np.asarray(observation)
    return float(np.sqrt(np.mean(error ** 2)))


def calculate_bias(forecast: npt.ArrayLike, observation: npt.ArrayLike) -> float:
    """
    Calculate forecast bias.

    Positive values indicate overforecasting.
    """
    error = np.asarray(forecast) - np.asarray(observation)
    return float(np.mean(error))


if __name__ == "__main__":
    forecast = np.array([20, 22, 24])
    observation = np.array([21, 21, 23])
    print("MAE:", calculate_mae(forecast, observation))
    print("RMSE:", calculate_rmse(forecast, observation))
    print("BIAS:", calculate_bias(forecast, observation))