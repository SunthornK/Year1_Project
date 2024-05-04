from customtkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
import pandas as pd


class AirQualityView:
    def __init__(self):
        self.root = CTk()
        self.root.geometry(f"{850}x{600}")
        self.root.title("Bangkok Air Quality Station Analysis Tool")
        self.marker_coord = None

        # create map widget
        self.map_widget = TkinterMapView(self.root, width=600, height=400, corner_radius=15)
        self.map_widget.pack(side="left", fill="both", expand=True)
        self.checkbox = CTkFrame(self.root)
        self.pm25_checkbox = CTkCheckBox(self.checkbox, text="PM2.5", corner_radius=60)
        self.pm25_checkbox.pack(pady=7)
        self.humidity_checkbox = CTkCheckBox(self.checkbox, text="Humidity", corner_radius=60)
        self.humidity_checkbox.pack(pady=7)
        self.temperature_checkbox = CTkCheckBox(self.checkbox, text="Temperature", corner_radius=60)
        self.temperature_checkbox.pack(pady=7)

        # google normal tile server
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # set the default position to be Department of Computer Engineering Building at Kasetsart University
        self.map_widget.set_position(13.8463425, 100.5685577)
        self.search_frame = CTkFrame(self.root)
        self.search_frame.pack(side="top", fill="x")

        self.entry_search = CTkEntry(self.search_frame)
        self.entry_search.pack(side="left", padx=5, pady=5, fill="x", expand=True)

        self.button_search = CTkButton(self.search_frame, text="Search", command=self.search_location)
        self.button_search.pack(side="left", padx=5, pady=5)
        self.load_data_button = CTkButton(self.root, text="Load Data", command=self.load_data)
        self.load_data_button.pack(pady=10)

        self.station_label = CTkLabel(self.root, text="Select Station:")
        self.station_label.pack()

        self.station_combobox = CTkComboBox(self.root, state="disabled")
        self.station_combobox.pack()

        self.start_date_label = CTkLabel(self.root, text="Start Date:")
        self.start_date_label.pack()
        self.start_date_combobox = CTkComboBox(self.root, state="readonly")
        self.start_date_combobox.pack()

        self.start_time_label = CTkLabel(self.root, text="Select Date and Time:")
        self.start_time_label.pack()
        self.start_time_combobox = CTkComboBox(self.root, state="readonly")
        self.start_time_combobox.pack()

        self.end_date_label = CTkLabel(self.root, text="End Date:")
        self.end_date_label.pack()
        self.end_date_combobox = CTkComboBox(self.root, state="readonly")
        self.end_date_combobox.pack()

        self.end_time_label = CTkLabel(self.root, text="Select Date and Time:")
        self.end_time_label.pack()
        self.end_time_combobox = CTkComboBox(self.root, state="readonly")
        self.end_time_combobox.pack()

        self.checkbox.pack(pady=10)

        self.display_graph_button = CTkButton(self.root, text="Display Graph", command=self.display_graph)
        self.display_graph_button.pack(pady=10)
        # self.summary_text = CTkTextbox(self.root, height=10, wrap="word")
        # self.summary_text.pack(expand=True, fill="both")
        self.map_widget.add_right_click_menu_command(label="Add Marker",
                                                     command=self.add_marker_event,
                                                     pass_coords=True)
        self.exit_button = CTkButton(self.root, text="Exit", command=self.root.destroy)
        self.exit_button.pack(pady=10)

    def add_marker_event(self, coords):
        print("Add marker:", coords)
        self.map_widget.delete_all_marker()
        self.marker = self.map_widget.set_marker(coords[0], coords[1], text="marker")

    def search_location(self):
        location = self.entry_search.get()
        geolocator = Nominatim(user_agent="map_viewer")
        location_data = geolocator.geocode(location)
        if location_data:
            latitude = location_data.latitude
            longitude = location_data.longitude
            self.map_widget.set_position(latitude, longitude)
            self.map_widget.set_zoom(13)
            self.controller.find_nearest_station((latitude, longitude))
        else:
            print("Location not found")

    def load_data(self):
        try:
            self.pm25_data = pd.read_csv("pm25_data.csv")
            self.temperature_data = pd.read_csv("temperature_data.csv")
            self.humidity_data = pd.read_csv("humidity_data.csv")
            self.stations = self.pm25_data.columns[3:]
            self.station_combobox.configure(values=self.stations)
            self.station_combobox.configure(state="readonly")
            self.dates_times = pd.to_datetime(self.pm25_data['date'] + ' ' + self.pm25_data['time'])

            dates = self.dates_times.dt.date.unique()
            self.start_date_combobox['values'] = dates
            self.end_date_combobox['values'] = dates

            times = self.dates_times.dt.strftime("%H:%M").unique()
            self.start_time_combobox['values'] = times
            self.end_time_combobox['values'] = times

            print("Data loaded successfully.")
        except FileNotFoundError:
            print("CSV file not found.")

    def display_graph(self):
        if hasattr(self, 'pm25_data') and hasattr(self, 'temperature_data') and hasattr(self, 'humidity_data'):
            selected_station = self.station_combobox.get()
            if selected_station:
                plt.figure(figsize=(10, 6))
                plt.plot(self.pm25_data['date'] + ' ' + self.pm25_data['time'], self.pm25_data[selected_station],
                         label='PM2.5')
                plt.plot(self.temperature_data['date'] + ' ' + self.temperature_data['time'],
                         self.temperature_data[selected_station], label='Temperature')
                plt.plot(self.humidity_data['date'] + ' ' + self.humidity_data['time'],
                         self.humidity_data[selected_station], label='Humidity')
                plt.title(f'Data at {selected_station}')
                plt.xlabel('Time')
                plt.ylabel('Value')
                plt.xticks(rotation=45)
                plt.legend()
                plt.grid(True)
                plt.tight_layout()
                self.show_graph_in_window(plt)

            else:
                print("Please select a station.")
        else:
            print("You need to load data first.")

    def show_graph_in_window(self, plt):
        graph_window = CTkToplevel()
        graph_window.title("Graph")

        canvas = FigureCanvasTkAgg(plt.gcf(), master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def set_controller(self, controller):
        self.controller = controller

    def run(self):
        self.root.mainloop()
