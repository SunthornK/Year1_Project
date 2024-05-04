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
    view.controller = controller

    controller.view.run()
