from customtkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim
from tkcalendar import DateEntry
from datetime import datetime
import matplotlib.pyplot as plt
# from pm_controller import AirQualityController

MIN_DATE = datetime(2024, 4, 12, 1, 0)
MAX_DATE = datetime(2024, 4, 19, 0, 0)

class AirQualityView:
    def __init__(self):
        self.root = CTk()
        self.root.title("Bangkok Air Quality Station Analysis Tool")
        self.marker_coord = None
        self.controller = None
        self.init_components()

    def set_controller(self, controller):
        self.controller = controller

    def init_components(self):
        option_frame = self.create_option_frame()
        option_frame.pack(side='left', fill="both", padx=5)
        self.main_frame = CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        self.home_page()

    def create_option_frame(self):
        frame = CTkFrame(self.root)
        home_btn = CTkButton(frame, text="Home", fg_color="transparent", font=('bold', 15),
                             command=lambda: self.swap_page(self.home_page))
        home_btn.pack(side="top", pady=40)

        graph_btn = CTkButton(frame, text="Graph", fg_color="transparent", font=('bold', 15),
                              command=lambda: self.swap_page(self.graph_page))
        graph_btn.pack(side="top")

        exit_btn = CTkButton(frame, text="Exit", command=self.root.destroy, font=('bold', 15))
        exit_btn.pack(side="bottom", pady=40)
        return frame

    def swap_page(self, page):
        for frame in self.main_frame.winfo_children():
            frame.destroy()
        page()

    def home_page(self):
        frame = CTkFrame(self.main_frame)
        map_frame = self.create_map_frame(frame)
        search_frame = self.create_searchbar(frame)

        map_frame.pack(side="top", fill="both", expand=True)
        search_frame.pack(side="top", fill="x", pady=7, expand=True)
        frame.pack(side="top", fill="both", expand=True)

    def graph_page(self):

        tabview = CTkTabview(self.main_frame)
        tabview.add("Overall Distribution")
        tabview.add("Datewise Comparison")
        tabview.pack(fill="both", expand=True)
        frame = CTkFrame(master=tabview.tab("Overall Distribution"))
        top_frame = self.create_station(frame)
        top_frame.pack(fill="x")

        mid_frame = self.create_choices(frame)
        mid_frame.pack(fill="x")

        bot_frame = CTkFrame(frame)

        start_date = CTkFrame(bot_frame)
        start_time_label = CTkLabel(start_date, text="Start Date and Time:", anchor="w")
        start_time_label.pack(side="top", fill="x", expand=True, padx=13)

        self.start_date = DateEntry(start_date, width=12, background='darkblue', foreground='white', borderwidth=2,
                                    mindate=MIN_DATE, maxdate=MAX_DATE)
        self.start_date.pack(side="left", padx=13)
        self.start_time_combobox = CTkComboBox(start_date, state="readonly")
        self.start_time_combobox.pack(side="left", fill="x", expand=True)
        start_date.pack(side="left", fill="x", expand=True)

        end_date = CTkFrame(bot_frame)
        end_time_label = CTkLabel(end_date, text="End Date and Time:", anchor="w")
        end_time_label.pack(side="top", fill="x", expand=True, padx=13)

        self.end_date = DateEntry(end_date, width=12, background='darkblue', foreground='white', borderwidth=2,
                                  mindate=MIN_DATE, maxdate=MAX_DATE)
        self.end_date.pack(side="left", padx=13)
        self.end_time_combobox = CTkComboBox(end_date, state="readonly")
        self.end_time_combobox.pack(side="left", fill="x", expand=True)

        self.display_btn = CTkButton(end_date, text="Display Graph", command=self.controller.display_graph_button_clicked)
        self.display_btn.pack(side="left", padx=10)
        end_date.pack(side="left", fill="x", expand=True)
        bot_frame.pack(fill="x", expand=False)
        # self.summary_text = CTkTextbox(self.root, height=10, wrap="word")
        # self.summary_text.pack(expand=True, fill="both")

        frame.pack(fill="both", expand=True)

    def create_station(self, parent):
        frame = CTkFrame(parent)
        self.station_label = CTkLabel(frame, text="Select Station:")
        self.station_label.pack(side="left", padx=20)
        self.station_combobox = CTkComboBox(frame, state="disabled")
        self.station_combobox.pack(side="left", fill="x", expand=True)
        self.load_data = CTkButton(frame, text="Load Data", command=self.controller.load_data_button_clicked)
        self.load_data.pack(side="left", pady=5)
        return frame

    def create_choices(self, parent):
        frame = CTkFrame(parent)
        self.pm25_checkbox = CTkCheckBox(frame, text="PM2.5")
        self.pm25_checkbox.pack(side="left", padx=20, pady=10)
        self.humidity_checkbox = CTkCheckBox(frame, text="Humidity")
        self.humidity_checkbox.pack(side="left", padx=20, pady=10)
        self.temperature_checkbox = CTkCheckBox(frame, text="Temperature")
        self.temperature_checkbox.pack(side="left", padx=20, pady=10)
        return frame

    def create_map_frame(self, parent):
        frame = CTkFrame(parent)
        self.map_widget = TkinterMapView(frame, width=600, height=400, corner_radius=15)
        self.map_widget.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        # google normal tile server
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        # set the default position to be Department of Computer Engineering Building at Kasetsart University
        self.map_widget.set_position(13.8463425, 100.5685577)
        self.map_widget.add_right_click_menu_command(label="Add Marker",
                                                     command=self.add_marker_event,
                                                     pass_coords=True)
        return frame

    def create_searchbar(self, parent):
        frame = CTkFrame(parent)

        self.entry_search = CTkEntry(frame)
        self.entry_search.pack(side="left", padx=5, pady=5, fill="x", expand=True)

        self._search = CTkButton(frame, text="Search", command=self.search_location)
        self._search.pack(side="left", padx=5, pady=5)

        return frame

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
            # self.controller.find_nearest_station((latitude, longitude))
        else:
            print("Location not found")

    def display_graph(self, fig):
        graph_window = CTkToplevel()
        graph_window.title("Graph")

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)


    def set_controller(self, controller):
        self.controller = controller

    def run(self):
        self.root.mainloop()
