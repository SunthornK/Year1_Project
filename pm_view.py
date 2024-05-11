"""
Module: pm_view

This module contains the PMView class, which represents the view component of the MVC architecture for the air
quality analysis tool.
"""
from tkinter import messagebox
from customtkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim
from tkcalendar import DateEntry
from datetime import datetime

MIN_DATE = datetime(2024, 4, 12, 1, 0)
MAX_DATE = datetime(2024, 4, 19, 0, 0)
set_default_color_theme("dark-blue")


class AirQualityView:
    def __init__(self):
        """
          Initialize the AirQualityView object.
          """
        self.root = CTk()
        self.root.title("Bangkok Air Quality Station Analysis Tool")
        self.marker_coord = None
        self.controller = None
        self.nearest_station = "bkp115t"
        self.init_components()

    def set_controller(self, controller):
        """
        Set the controller for the view.

        Parameters:
        - controller: The controller object to set
        """
        self.controller = controller

    def init_components(self):
        """
        Initialize the components of the view.
        """
        option_frame = self.create_option_frame()
        self.main_frame = CTkFrame(self.root)

        option_frame.pack(side='left', fill="both", padx=5)
        self.main_frame.pack(fill="both", expand=True)
        self.home_page()

    def create_option_frame(self):
        """
        Create the option frame containing navigation buttons.
        """
        frame = CTkFrame(self.root)
        home_btn = CTkButton(frame, text="Home", fg_color="transparent", font=('bold', 15),
                             command=lambda: self.swap_page(self.home_page))
        graph_btn = CTkButton(frame, text="Graph", fg_color="transparent", font=('bold', 15),
                              command=lambda: self.swap_page(self.graph_page))
        exit_btn = CTkButton(frame, text="Exit", command=self.root.destroy, font=('bold', 15))

        home_btn.pack(side="top", pady=40)
        graph_btn.pack(side="top")

        exit_btn.pack(side="bottom", pady=40)
        return frame

    def swap_page(self, page):
        """
        Swap between pages in the main frame.

        Parameters:
        - page: The function to call to display the desired page
        """
        for frame in self.main_frame.winfo_children():
            frame.destroy()
        page()

    def home_page(self):
        """
        Display the home page.
        """
        frame = CTkFrame(self.main_frame)
        select_time, self.choose_date = self.create_date_entry(frame, "Choose Date and Time:")
        hours = [f"{i:02d}:00" for i in range(1, 24)] + ["00:00"]
        self.choose_time = CTkComboBox(select_time, state="readonly", values=hours)
        self.choose_time.set(hours[0])
        self.choose_time.pack(side="top", fill="x", expand=True)
        select_time.pack(side="top", fill="x", expand=True)

        map_frame = self.create_map_frame(frame)
        search_frame = self.create_searchbar(frame)
        big_label = self.create_big_display(frame)

        search_frame.pack(side="top", fill="x", pady=7, expand=True)
        map_frame.pack(side="top", fill="both", expand=True)
        frame.pack(side="top", fill="both", expand=True)
        big_label.pack(side="top", fill="both", expand=True)

    def create_big_display(self, parent):
        """
        Create the big display frame showing PM2.5 data.

        Parameters:
        - parent: The parent frame to contain the big display frame
        """
        frame = CTkFrame(parent)
        date = self.choose_date.get_date()
        time = 1
        big_frame, color0, label0 = self.create_pm_display(frame, date, f"{time:2d}:00", "10")
        label0.configure(width=100)
        big_frame.configure(width=100)
        big_frame.pack(side="left", fill="both", expand=True)
        small_frame = CTkFrame(frame)
        small1, color1, label1 = self.create_pm_display(small_frame, date, f"{time+1:2d}:00", "25")
        small1.pack(side="left", fill="both", expand=True, padx=6)
        small2, color2, label2 = self.create_pm_display(small_frame, date, f"{time+2:2d}:00", "37")
        small2.pack(side="left", fill="both", expand=True, padx=6)
        small3, color3, label3 = self.create_pm_display(small_frame, date, f"{time+3:2d}:00", "50")
        small3.pack(side="left", fill="both", expand=True, padx=6)
        small4, color4, label4 = self.create_pm_display(small_frame, date, f"{time+4:2d}:00", "90")
        small4.pack(side="left", fill="both", expand=True, padx=6)
        small5, color5, label5 = self.create_pm_display(small_frame, date, f"{time+5:2d}:00", "300")
        small5.pack(side="left", fill="both", expand=True, padx=6)
        small_frame.pack(side="left", fill="both")

        return frame

    def create_pm_display(self, parent, date, time, pm25):
        """
        Create the small PM display frame.

        Parameters:
        - parent: The parent frame to contain the PM display frame
        - date: Date for which the PM data is displayed
        - time: Time for which the PM data is displayed
        - pm25: PM2.5 value to display
        """
        pm25_int = int(pm25)
        if pm25_int <= 25:
            color_code = "cyan"  # Good air quality
        elif 26 < pm25_int <= 37:
            color_code = "lawn green"  # Moderate air quality
        elif 38 < pm25_int <= 50:
            color_code = "gold"  # Unhealthy for sensitive groups
        elif 51 < pm25_int <= 90:
            color_code = "orange"  # Unhealthy air quality
        else:
            color_code = "maroon"  # Very unhealthy air quality

        frame = CTkFrame(parent, fg_color="white", border_width=4, corner_radius=40)
        color = CTkLabel(frame, text="", anchor="n", corner_radius=60, fg_color=color_code)
        label = CTkLabel(frame, text=f"{time}    {pm25}", font=('bold', 17), anchor="center", corner_radius=60,
                         bg_color="white", fg_color="lightsteelblue", text_color="gray23", height=50)

        color.pack(side="top", fill="x", padx=30, pady=10)
        label.pack(side="top", fill="both", expand=True, padx=20, pady=15)
        return frame, color, label

    def graph_page(self):
        """
        Display the graph page.
        """
        tabview = CTkTabview(self.main_frame)
        tabview.add("Time Series & Correlation")
        tabview.add("Statistics & Other graph")
        tabview.pack(fill="both", expand=True)
        self.tab1 = self.create_tab1(tabview.tab("Time Series & Correlation"))
        self.tab2 = self.create_tab2(tabview.tab("Statistics & Other graph"))

        self.tab1.pack(fill="both", expand=True)
        self.tab2.pack(fill="both", expand=True)

    def create_tab1(self, parent):
        """
        Create the first tab of the graph page.

        Parameters:
        - parent: The parent frame to contain the first tab
        """
        frame = CTkFrame(parent)
        top_frame = self.create_station(frame)
        mid_frame = self.creat_choices(frame)
        bot_frame = self.create_time_selection(frame, self.controller.display_graph_button_clicked)
        self.canvas_frame1 = CTkFrame(frame)
        top_frame.pack(fill="x")
        mid_frame.pack(fill="x")
        bot_frame.pack(fill="x")
        self.canvas_frame1.pack(fill="both", expand=True)
        return frame

    def create_tab2(self, parent):
        """
        Create the second tab of the graph page for other graph.

        Parameters:
        - parent: The parent frame to contain the second tab
        """
        frame = CTkFrame(parent)
        self.canvas_frame2 = CTkFrame(frame)
        pie_chart_btn = CTkButton(frame, text="Pie Chart", font=('bold', 15),
                                  command=self.controller.display_pie_chart)
        distribution_graph_btn = CTkButton(frame, text="Distribution Graph", font=('bold', 15),
                                           command=self.controller.display_distribution_graph)
        statistics_btn = CTkButton(frame, text="Descriptive Statistics", font=('bold', 15),
                                           command=self.controller.display_statistics)
        pie_chart_btn.pack(side="top", pady=10)
        distribution_graph_btn.pack(side="top")
        statistics_btn.pack(side="top", pady=10)
        self.canvas_frame2.pack(fill="both", expand=True)
        return frame

    def create_station(self, parent):
        """
        Create the first tab of the graph page.

        Parameters:
        - parent: The parent frame to contain the first tab
        """
        frame = CTkFrame(parent)
        self.station_label = CTkLabel(frame, text="Select Station:")
        self.station_combobox = CTkComboBox(frame, state="disabled")
        self.load_data = CTkButton(frame, text="Load Data", command=self.controller.load_data_button_clicked)

        self.station_label.pack(side="left", padx=20)
        self.station_combobox.pack(side="left", fill="x", expand=True)
        self.load_data.pack(side="left", pady=5, padx=10)
        return frame

    def creat_choices(self, parent):
        """
        Create the data table choices section.

        Parameters:
        - parent: The parent frame to contain the data choices section
        """
        frame = CTkFrame(parent)
        self.pm25_checkbox = CTkCheckBox(frame, text="PM2.5")
        self.humidity_checkbox = CTkCheckBox(frame, text="Humidity")
        self.temperature_checkbox = CTkCheckBox(frame, text="Temperature")

        self.pm25_checkbox.pack(side="left", padx=20, pady=10)
        self.humidity_checkbox.pack(side="left", padx=20, pady=10)
        self.temperature_checkbox.pack(side="left", padx=20, pady=10)
        return frame

    def create_time_selection(self, parent, func):
        """
        Create the time selection section.

        Parameters:
        - parent: The parent frame to contain the time selection section
        - func: Function to call when the display button is clicked
        """
        frame = CTkFrame(parent)
        start_frame, self.start_date_entry = self.create_date_entry(frame, "Start Date and Time:")
        end_frame, self.end_date_entry = self.create_date_entry(frame, "End Date and Time:")
        hours = [f"{i:02d}:00" for i in range(1, 24)] + ["00:00"]
        self.start_time_combobox = CTkComboBox(start_frame, state="readonly", values=hours)
        self.end_time_combobox = CTkComboBox(end_frame, state="readonly", values=hours)
        self.display_btn = CTkButton(end_frame, text="Display Graph",
                                     command=func)

        start_frame.pack(side="left", fill="x", expand=True)
        end_frame.pack(side="left", fill="x", expand=True)
        self.start_time_combobox.pack(side="left", fill="x", expand=True)
        self.end_time_combobox.pack(side="left", fill="x", expand=True)
        self.display_btn.pack(side="left", padx=10)

        self.start_date_entry.bind("<<DateEntrySelected>>", lambda event: self.controller.check_date())
        self.start_time_combobox.bind('<<ComboboxSelected>>', self.controller.check_time)
        self.end_date_entry.bind("<<DateEntrySelected>>", lambda event: self.controller.check_date())
        self.end_time_combobox.bind('<<ComboboxSelected>>', self.controller.check_time)
        return frame

    def create_date_entry(self, parent, label_text):
        """
        Create a DateEntry widget.

        Parameters:
        - parent: The parent frame to contain the DateEntry widget
        - label_text: Text for the label associated with the DateEntry widget
        """
        frame = CTkFrame(parent)
        start_time_label = CTkLabel(frame, text=label_text, anchor="w")
        date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                               mindate=MIN_DATE, maxdate=MAX_DATE)

        start_time_label.pack(side="top", fill="x", expand=True, padx=13)
        date_entry.pack(side="left", padx=13)
        return frame, date_entry

    def create_map_frame(self, parent):
        """
        Create the map frame containing the map widget.

        Parameters:
        - parent: The parent frame to contain the map frame
        """
        frame = CTkFrame(parent)
        self.map_widget = TkinterMapView(frame, width=600, height=400, corner_radius=15)
        # google normal tile server
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        # set the default position to be Department of Computer Engineering Building at Kasetsart University
        self.map_widget.set_position(13.8463425, 100.5685577)
        self.map_widget.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.map_widget.add_right_click_menu_command(label="Add Marker",
                                                     command=self.add_marker_event,
                                                     pass_coords=True)
        return frame

    def create_searchbar(self, parent):
        """
        Create the search bar for location search.

        Parameters:
        - parent: The parent frame to contain the search bar
        """
        frame = CTkFrame(parent)
        self.entry_search = CTkEntry(frame)
        self._search = CTkButton(frame, text="Search", command=self.search_location)

        self.entry_search.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        self._search.pack(side="left", padx=5, pady=5)
        return frame

    def add_marker_event(self, coords):
        """
        Add a marker to the map when right-clicked.

        Parameters:
        - coords: Coordinates of the right-clicked point
        """
        print("Add marker:", coords)
        self.map_widget.delete_all_marker()
        self.marker = self.map_widget.set_marker(coords[0], coords[1], text="marker")
        self.nearest_station = self.controller.find_nearest_station(coords[0], coords[1])

        self.pm25 = self.controller.get_pm25(self.get_choose_date(), self.get_choose_time(), self.nearest_station)
        messagebox.showinfo("Nearest Station", f"Nearest Station is {self.nearest_station} has pm2.5 = {self.pm25}")
        print(self.pm25)

    def search_location(self):
        """
        Search for a location entered the search bar and set the map position.
        """
        location = self.entry_search.get()
        geolocator = Nominatim(user_agent="map_viewer")
        location_data = geolocator.geocode(location)
        if location_data:
            latitude = location_data.latitude
            longitude = location_data.longitude
            self.map_widget.set_position(latitude, longitude)
            self.map_widget.set_zoom(13)
        else:
            print("Location not found")

    def has_canvas(self, frame):
        """
        Check if a frame contains a Canvas widget.

        Parameters:
        - frame: The frame to check

        Returns:
        - True if the frame contains a Canvas widget, False otherwise
        """
        for child in frame.winfo_children():
            if frame.nametowidget(child).winfo_class() == 'Canvas':
                return True
        return False

    def display_graph1(self, fig):
        """
        Display the in first graph tab.

        Parameters:
        - fig: The figure to display
        """
        if self.has_canvas(self.canvas_frame1):
            new_window = CTkToplevel(self.root)
            new_window.title("Graph Window")
            canvas = FigureCanvasTkAgg(fig, master=new_window)
        else:
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame1)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def display_graph2(self, fig):
        """
         Display the in second graph tab.

         Parameters:
         - fig: The figure to display
         """
        if self.has_canvas(self.canvas_frame2):
            new_window = CTkToplevel(self.root)
            new_window.title("Graph Window")
            canvas = FigureCanvasTkAgg(fig, master=new_window)
        else:
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame2)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def get_start_date(self):
        """
        Get the start date from the DateEntry widget.

        Returns:
        - Start date as a datetime object
        """
        return self.start_date_entry.get_date()

    def get_end_date(self):
        """
         Get the end date from the DateEntry widget.

         Returns:
         - End date as a datetime object
         """
        return self.end_date_entry.get_date()

    def get_start_time(self):
        """
        Get the start time from the ComboBox widget.

        Returns:
        - Start time as a string
        """
        return self.start_time_combobox.get()

    def get_end_time(self):
        """
        Get the start time from the ComboBox widget.

        Returns:
        - Start time as a string
        """
        return self.end_time_combobox.get()

    def get_choose_date(self):
        """
        Get the start time from the ComboBox widget.

        Returns:
        - Start time as a string
        """
        return self.choose_date.get_date()

    def get_choose_time(self):
        """
        Get the selected time from the ComboBox widget.

        Returns:
        - Selected time as a string
        """
        return self.choose_time.get()

    def set_end_date(self, date):
        """
        Set the end date in the DateEntry widget.

        Parameters:
        - date: The date to set as the end date
        """
        self.end_date_entry.set_date(date)

    def run(self):
        """
        Run the application.
        """
        self.root.mainloop()
