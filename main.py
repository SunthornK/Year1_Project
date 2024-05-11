"""
Main module

This module initializes the Air Quality Analysis Tool by creating instances of the AirQualityModel, AirQualityView,
and AirQualityController classes, and running the controller.

Usage:
    - Run this script to start the Air Quality Analysis Tool.

Note: - Make sure to have the required CSV files ('pm25_data.csv', 'temperature_data.csv', 'humidity_data.csv') in
the same directory as this script.

"""
from pm_model import AirQualityModel
from pm_view import AirQualityView
from pm_controller import AirQualityController
import pandas as pd

if __name__ == "__main__":

    pm25_data = pd.read_csv("pm25_data.csv")
    temperature_data = pd.read_csv("temperature_data.csv")
    humidity_data = pd.read_csv("humidity_data.csv")

    model = AirQualityModel(pm25_data, temperature_data, humidity_data)
    view = AirQualityView()
    controller = AirQualityController(model, view)
    view.set_controller(controller)
    controller.run()
