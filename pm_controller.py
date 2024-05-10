import pandas as pd
from matplotlib import pyplot as plt


class AirQualityController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def visualize_pm25(self):
        location = self.view.marker_coord
    def load_data_button_clicked(self):
        date, station = self.model.load_data()
        self.view.station_combobox.configure(values=station)
        self.view.station_combobox.configure(state="readonly")
        times = date.dt.strftime("%H:%M").unique()
        self.view.start_time_combobox['values'] = times
        self.view.end_time_combobox['values'] = times

    def display_graph_button_clicked(self):
        if self.model:
            pm25_data = self.model.pm25_data
            temperature_data = self.model.temperature_data
            humidity_data = self.model.humidity_data

            selected_station = self.view.station_combobox.get()
            if selected_station:
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(pm25_data['date'] + ' ' + pm25_data['time'], pm25_data[selected_station], label='PM2.5')
                ax.plot(temperature_data['date'] + ' ' + temperature_data['time'],
                        temperature_data[selected_station], label='Temperature')
                ax.plot(humidity_data['date'] + ' ' + humidity_data['time'], humidity_data[selected_station],
                        label='Humidity')
                ax.set_title(f'Data at {selected_station}')
                ax.set_xlabel('Time')
                ax.set_ylabel('Value')
                ax.tick_params(axis='x', rotation=45)
                ax.legend()
                ax.grid(True)

                self.view.display_graph(fig)
            else:
                print("Please select a station.")
        else:
            print("You need to load data first.")

    def run(self):
        self.view.run()
