import pandas as pd

class AirQualityModel:
    def __init__(self, pm25_data, temperature_data, humidity_data):
        self.pm25_data = pm25_data
        self.temperature_data = temperature_data
        self.humidity_data = humidity_data
    def load_data(self):
        try:
            self.pm25_data = pd.read_csv("pm25_data.csv")
            self.temperature_data = pd.read_csv("temperature_data.csv")
            self.humidity_data = pd.read_csv("humidity_data.csv")
            self.stations = self.pm25_data.columns[3:]
            self.dates_times = pd.to_datetime(self.pm25_data['date'] + ' ' + self.pm25_data['time'])

            print("Data loaded successfully.")
            return self.dates_times, self.stations
        except FileNotFoundError:
            print("CSV file not found.")
    def estimate_pm25(self, location):
        pass

    def trends(self):
        pass
