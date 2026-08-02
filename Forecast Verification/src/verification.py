# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 14:09:03 2026

@author: niker
"""

import numpy as np

def calculate_mae(forecast, observation):
    """
    Calculate Mean Absolute Error.
    """

    error = forecast - observation

    mae = np.mean(np.abs(error))

    return mae


def calculate_rmse(forecast, observation):
    """
    Calculate Root Mean Square Error.
    """

    error = forecast - observation

    rmse = np.sqrt(np.mean(error ** 2))

    return rmse

def calculate_bias(forecast, observation):
    """
    Calculate forecast bias.
    Positive values indicate overforecasting.
    """

    error = forecast - observation

    bias = np.mean(error)

    return bias


if __name__ == "__main__":

    forecast = np.array([20, 22, 24])
    observation = np.array([21, 21, 23])
    mae = calculate_mae(forecast, observation)
    rmse = calculate_rmse(forecast, observation)
    bias = calculate_bias(forecast, observation)

    print("MAE:", mae)
    print("RMSE:", rmse)
    print("BIAS:", bias)