import pandas as pd

class AirQualityController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def visualize_pm25(self):
        location = self.view.marker_coord
