"""
Module: pm_controller

This module contains the AirQualityController class, which controls the interaction between the Air Quality Model and
the Air Quality View.
"""
from datetime import datetime
from tkinter import messagebox
import pandas as pd
from matplotlib import pyplot as plt


class AirQualityController:
    def __init__(self, model, view):
        """
        Initialize the AirQualityController object.

        Parameters:
        - model: The model object
        - view: The view object
        """
        self.pm25_value = None
        self.model = model
        self.view = view

    @property
    def get_pm25_data(self):
        """
        Get the PM2.5 data.
        """
        return self.pm25_value

    def load_data_button_clicked(self):
        """
        Load data when the Load Data button is clicked.
        """
        date, station = self.model.load_data()
        self.view.station_combobox.configure(values=station)
        self.view.station_combobox.configure(state="readonly")
        times = date.dt.strftime("%H:%M").unique()
        self.view.start_time_combobox['values'] = times
        self.view.end_time_combobox['values'] = times

    def display_statistics(self):
        """
        Display statistics for PM2.5, temperature, and humidity.

        This function calculates and displays statistics such as mean, median, minimum, and maximum
        values for PM2.5, temperature, and humidity data.

        """
        if not self.model:
            messagebox.showerror("Error", "You need to load data first.")
            return

        pm25_data = self.model.pm25_data
        temperature_data = self.model.temperature_data
        humidity_data = self.model.humidity_data

        if pm25_data is None or temperature_data is None or humidity_data is None:
            messagebox.showerror("Error", "One or more data tables are missing.")
            return

        # Calculate statistics for PM2.5
        pm25_statistics = pm25_data.describe().round(2)
        pm25_statistics_text = "PM2.5 Statistics:\n" + pm25_statistics.to_string() + "\n\n"

        # Calculate statistics for temperature
        temperature_statistics = temperature_data.describe().round(2)
        temperature_statistics_text = "Temperature Statistics:\n" + temperature_statistics.to_string() + "\n\n"

        # Calculate statistics for humidity
        humidity_statistics = humidity_data.describe().round(2)
        humidity_statistics_text = "Humidity Statistics:\n" + humidity_statistics.to_string()

        # Prepare statistics text
        statistics_text = pm25_statistics_text + temperature_statistics_text + humidity_statistics_text

        # Display statistics
        messagebox.showinfo("Statistics", statistics_text)

    def display_pie_chart(self):
        """
        Display a pie chart of PM2.5 categories distribution.
        """
        if self.model:
            pm25_data = self.model.pm25_data
            selected_station = self.view.station_combobox.get()
            if selected_station:
                if pm25_data is not None:
                    pm25_categories = pd.cut(pm25_data[selected_station],
                                             bins=[0, 12, 35.5, 43, 54, 75, 91],
                                             labels=['Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy',
                                                     'Very Unhealthy', 'Hazardous'])
                    plt.figure(figsize=(8, 6))
                    pm25_categories.value_counts().plot.pie(autopct='%1.1f%%', startangle=140)
                    plt.title(f'PM2.5 Categories Distribution of {selected_station}')
                    plt.ylabel('')
                    plt.tight_layout()
                    fig = plt.gcf()
                    self.view.display_graph2(fig)
                else:
                    messagebox.showerror("Error", "No PM2.5 data available.")
            else:
                messagebox.showerror("Error", "Please select a station")
        else:
            messagebox.showerror("Error", "You need to load data first.")

    def display_distribution_graph(self):
        """
        Display a distribution graph of PM2.5 concentration.
        """
        if self.model:
            pm25_data = self.model.pm25_data
            selected_station = self.view.station_combobox.get()
            if selected_station:
                if pm25_data is not None:
                    plt.figure(figsize=(8, 6))
                    plt.hist(pm25_data[selected_station], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
                    plt.title(f'PM2.5 Concentration Distribution of {selected_station}')
                    plt.xlabel('PM2.5 Concentration')
                    plt.ylabel('Frequency')
                    plt.grid(True)
                    plt.tight_layout()
                    fig = plt.gcf()
                    self.view.display_graph2(fig)
                else:
                    messagebox.showerror("Error", "No PM2.5 data available or 'PM2.5' column not found.")
            else:
                messagebox.showerror("Error", "Please select a station")
        else:
            messagebox.showerror("Error", "You need to load data first.")

    def display_graph_button_clicked(self):
        """
        Handle the click event of the Display Graph button.
        """
        if self.model:
            pm25_data = self.model.pm25_data
            temperature_data = self.model.temperature_data
            humidity_data = self.model.humidity_data

            selected_station = self.view.station_combobox.get()
            if selected_station:

                start_date = self.view.get_start_date()
                end_date = self.view.get_end_date()
                start_time = self.view.get_start_time()
                end_time = self.view.get_end_time()
                print(start_date)
                # Check if all the inputs are provided
                if start_date and end_date and start_time and end_time:
                    try:
                        # Convert start_time and end_time strings to datetime.time objects
                        start_time_obj = datetime.strptime(start_time, '%H:%M').time()
                        end_time_obj = datetime.strptime(end_time, '%H:%M').time()

                        # Combine start_date and start_time_obj
                        start_datetime = datetime.combine(start_date, start_time_obj)
                        end_datetime = datetime.combine(end_date, end_time_obj)

                        # Filter data based on selected date and time range
                        pm25_data_filtered = pm25_data[(pm25_data['date'] + ' ' + pm25_data['time']).apply(
                            lambda x: start_datetime <= datetime.strptime(x, '%m/%d/%Y %H:%M') <= end_datetime)]
                        temperature_data_filtered = temperature_data[
                            (temperature_data['date'] + ' ' + temperature_data['time']).apply(
                                lambda x: start_datetime <= datetime.strptime(x, '%m/%d/%Y %H:%M') <= end_datetime)]
                        humidity_data_filtered = humidity_data[
                            (humidity_data['date'] + ' ' + humidity_data['time']).apply(
                                lambda x: start_datetime <= datetime.strptime(x, '%m/%d/%Y %H:%M') <= end_datetime)]
                        checkboxes_selected = {
                            "PM2.5": self.view.pm25_checkbox.get(),
                            "Temperature": self.view.temperature_checkbox.get(),
                            "Humidity": self.view.humidity_checkbox.get()
                        }

                        num_selected = sum(checkboxes_selected.values())

                        if num_selected == 1:
                            selected_var = [var for var, selected in checkboxes_selected.items() if selected][0]
                            self.display_line_graph(pm25_data_filtered, temperature_data_filtered,
                                                    humidity_data_filtered, selected_station, selected_var)
                        elif num_selected == 2:
                            selected_vars = [var for var, selected in checkboxes_selected.items() if selected == 1]
                            if len(selected_vars) == 2:
                                var1, var2 = selected_vars
                                self.display_correlation(pm25_data_filtered, temperature_data_filtered,
                                                         humidity_data_filtered, selected_station, var1, var2)
                        else:
                            messagebox.showerror("Error", "Please select either one or two checkboxes")

                    except ValueError:
                        messagebox.showerror("Error", "Invalid date or time format")
                else:
                    messagebox.showerror("Error", "Please fill all the date and time fields")
            else:
                messagebox.showerror("Error", "Please select a station")
        else:
            messagebox.showerror("Error", "You need to load data first")

    def display_line_graph(self, pm25_data, temperature_data, humidity_data, selected_station, var):
        """
        Plot the graph based on selected data type (PM2.5, Temperature, Humidity)

        Parameters:
        - pm25_data: DataFrame containing PM2.5 data
        - temperature_data: DataFrame containing temperature data
        - humidity_data: DataFrame containing humidity data
        - selected_station: The selected station
        - var: The variable to display (PM2.5, Temperature, or Humidity)
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        if var == 'PM2.5':
            ax.plot(pm25_data['date'] + ' ' + pm25_data['time'],
                    pm25_data[selected_station], label='PM2.5')
            ax.set_ylabel('Micrograms/Cubic meter of air')
        elif var == 'Temperature':
            ax.plot(temperature_data['date'] + ' ' + temperature_data['time'],
                    temperature_data[selected_station], label='Temperature')
            ax.set_ylabel('Celsius')
        elif var == 'Humidity':
            ax.plot(humidity_data['date'] + ' ' + humidity_data['time'],
                    humidity_data[selected_station], label='Humidity')
            ax.set_ylabel('Grams/Cubic meter of air')

        ax.set_title(f'{var} Data at {selected_station}')
        ax.set_xlabel('Time')
        ax.tick_params(axis='x', rotation=30)
        ax.legend()
        ax.grid(True)
        self.view.display_graph1(fig)

    def display_correlation(self, pm25_data, temperature_data, humidity_data, selected_station, var1, var2):
        """
        Display a correlation scatter plot.

        Parameters:
        - pm25_data: DataFrame containing PM2.5 data
        - temperature_data: DataFrame containing temperature data
        - humidity_data: DataFrame containing humidity data
        - selected_station: The selected station
        - var1: The first variable for correlation
        - var2: The second variable for correlation
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        if var1 and var2 in ['PM2.5', 'Humidity']:
            ax.scatter(pm25_data[selected_station], humidity_data[selected_station],
                       label='PM2.5 - Humidity')
            ax.set_xlabel('PM2.5 Concentration')
            ax.set_ylabel('Humidity')
        elif var1 and var2 in ['PM2.5', 'Temperature']:
            ax.scatter(pm25_data[selected_station], temperature_data[selected_station],
                       label='PM2.5 - Temperature')
            ax.set_xlabel('PM2.5 Concentration')
            ax.set_ylabel('Temperature')
        else:
            ax.scatter(humidity_data[selected_station], temperature_data[selected_station],
                       label='Humidity - Temperature')
            ax.set_xlabel('Humidity')
            ax.set_ylabel('Temperature')
        ax.set_title(f'Correlation Scatter Plot at {selected_station}')

        ax.legend()
        ax.grid(True)
        self.view.display_graph1(fig)

    def get_pm25(self, date, time, nearest_station):
        """
        Get the PM2.5 value for a specific date, time, and station.

        Parameters:
        - date: The date
        - time: The time
        - nearest_station: The nearest station

        Returns:
        - PM2.5 value
        """
        time_obj = datetime.strptime(time, "%H:%M").time()
        start_datetime = datetime.combine(date, time_obj)

        pm25_data_filtered = self.model.pm25_data[
            (self.model.pm25_data['date'] + ' ' + self.model.pm25_data['time']).apply(
                lambda x: start_datetime <= datetime.strptime(x, '%m/%d/%Y %H:%M') <= start_datetime)]
        print(nearest_station)

        pm25_value = pm25_data_filtered.iloc[0][nearest_station]
        return pm25_value

    def find_nearest_station(self, latitude, longitude):
        """
        Find the nearest station to a given latitude and longitude.

        Parameters:
        - latitude: Latitude coordinate
        - longitude: Longitude coordinate

        Returns:
        - Nearest station name
        """
        nearest_station, nearest_distance = self.model.nearest_station(latitude, longitude)

        print("Nearest place:", nearest_station)
        print("Distance:", nearest_distance, "km")
        if nearest_distance > 15:
            print("The given location is too far from the nearest station")
        else:
            print("No PM2.5 data available for the selected date and time")
        return nearest_station

    def check_date(self):
        """
        Check if the selected end date is after the start date.
        """
        start_date = self.view.get_start_date()
        end_date = self.view.get_end_date()
        if not self.model.is_valid_date_range(start_date, end_date):
            messagebox.showerror("Error", "End date must be after start date")
            self.view.set_end_date(start_date)

    def check_time(self):
        """
        Checks if the selected end time is different from the start time.
        """
        start_date = self.view.get_start_date()
        start_time = self.view.get_start_time()
        end_date = self.view.get_end_date()
        end_time = self.view.get_end_time()
        if start_date == end_date and start_time == end_time:
            messagebox.showerror("Error", "End time must be different from start time")

    def run(self):
        """
        Run the application.
        """
        self.view.run()
