import numpy as np


def moving_average_forecast(actual_values, window=4):

    forecasts = [np.nan] * len(actual_values)

    for i in range(window, len(actual_values)):

        forecasts[i] = np.mean(
            actual_values[i-window:i]
        )

    return np.array(forecasts)


def exponential_smoothing_forecast(
    actual_values,
    alpha=0.4
):

    forecasts = np.zeros(len(actual_values))

    forecasts[0] = actual_values[0]

    for i in range(1, len(actual_values)):

        forecasts[i] = (
            alpha * actual_values[i-1]
            + (1-alpha) * forecasts[i-1]
        )

    return forecasts


def calculate_accuracy(
    actual_values,
    forecast_values,
    start_index=1
):

    actual = np.array(
        actual_values[start_index:]
    )

    forecast = np.array(
        forecast_values[start_index:]
    )

    errors = actual - forecast

    absolute_errors = np.abs(errors)

    percentage_errors = (
        absolute_errors / actual
    ) * 100

    mad = np.mean(absolute_errors)

    mape = np.mean(percentage_errors)

    return mad, mape