"""
Module: pm_model

This module contains the AirQualityModel class, which represents the model component of the MVC architecture for the
air quality analysis tool.
"""
from math import radians, cos, sin, asin, sqrt
import pandas as pd



class AirQualityModel:
    def __init__(self, pm25_data, temperature_data, humidity_data):
        """
        Initialize the AirQualityModel object.
        """
        self.pm25_data = pm25_data
        self.temperature_data = temperature_data
        self.humidity_data = humidity_data

        self.coordinates = {
            "02t": (13.732209408708636, 100.49011823103785),
            "11t": (13.77652082459571, 100.57208382984774),
            "12t": (13.70740370222286, 100.54713976097712),
            "54t": (13.7642440339872, 100.55418099816625),
            "53t": (13.795263997529226, 100.59335406939272),
            "59t": (13.780574801627816, 100.53817599639395),
            "bkp112t": (13.692982196365548, 100.50245751112156),
            "bkp115t": (13.81308580514807, 100.5567686963916),
            "bkp129t": (13.85444675012722, 100.85896905528762),
            "bkp130t": (13.878003444157178, 100.62044846596419),
            "bkp128t": (13.720923957921034, 100.78119854362957),
            "bkp65t": (13.733749553788511, 100.5284046965944),
            "bkp64t": (13.7641831560783, 100.60572519639112),
            "bkp72t": (13.668622205457751, 100.63554611418128),
            "bkp75t": (13.89511672071199, 100.66049639025802),
            "bkp80t": (13.855566745921893, 100.86250590252648),
            "bkp90t": (13.638530493326543, 100.37231663749424),
            "bkp89t": (13.691342780481444, 100.34166561371465),
            "13t": (13.853442192837056, 100.52714131418323),
            "16t": (13.620945556760411, 100.56058979294127),
            "17t": (13.65075664069759, 100.53075974648702),
            "14t": (13.703493639422767, 100.32169741970371),
            "18t": (13.599421571021107, 100.59688746446852),
            "20t": (14.039526298916469, 100.61535386755857),
            "o10": (13.768086948199999, 100.64999379639114),
            "50t": (13.732462092201965, 100.53607355528632),
            "bkp116t": (13.80751017138618, 100.55542457082737),
            "bkp119t": (13.731408311636821, 100.567930666943),
            "bkp122t": (13.729544153507362, 100.55871339639071),
            "bkp121t": (13.652018662123847, 100.49140602199797),
            "bkp126t": (13.686273866744415, 100.3846529822208),
            "bkp125t": (13.787043155102085, 100.67442399639135),
            "bkp133t": (13.769310458423261, 100.49498097860005),
            "bkp131t": (13.68535165943233, 100.5180536963904),
            "bkp61t": (13.757332794560948, 100.51466145988448),
            "bkp60t": (13.776963646331252, 100.51969026875639),
            "bkp63t": (13.781296032312888, 100.53290028014874),
            "bkp62t": (13.7422132815451, 100.51353565121386),
            "bkp92t": (13.76489755604922, 100.49875840804674),
            "bkp87t": (13.74621662068962, 100.35486787445514),
            "bkp58t": (13.681947453478756, 100.50580256694248),
            "bkp57t": (13.702465949899972, 100.60201265528603),
            "bkp56t": (13.769869283938357, 100.5531413963911),
            "bkp124t": (13.771875110197714, 100.46815581755364),
            "bkp123t": (13.807522956576939, 100.55056037860047)}

    def load_data(self):
        """
        Load data from CSV files.
        """
        try:
            self.pm25_data = pd.read_csv("pm25_data.csv")
            self.temperature_data = pd.read_csv("temperature_data.csv")
            self.humidity_data = pd.read_csv("humidity_data.csv")
            self.stations = self.pm25_data.columns[3:]
            self.dates_times = pd.to_datetime(self.pm25_data['date'] + ' ' + self.pm25_data['time'])
            # self.pm25_data.set_index(['date', 'time'], inplace=True)
            print("Data loaded successfully.")
            return self.dates_times, self.stations
        except FileNotFoundError:
            print("CSV file not found.")

    @staticmethod
    def is_valid_date_range(start_date, end_date):
        """
        Check if the given date range is valid.
        """
        return end_date >= start_date

    def haversine(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        # Radius of earth in kilometers is 6371
        km = 6371 * c
        return km

    def nearest_station(self, given_lat, given_lon):
        """
        Find the nearest station to the given latitude and longitude.
        """
        distances = {}
        for name, coord in self.coordinates.items():
            distances[name] = self.haversine(given_lon, given_lat, coord[1], coord[0])
        nearest_station = min(distances, key=distances.get)
        nearest_distance = distances[nearest_station]
        return nearest_station, nearest_distance
