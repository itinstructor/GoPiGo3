#!/usr/bin/env python3
"""
    Name:    bme280_tkinter.py
    Author:  William A Loring
    Created: 10/27/21 Revised:
    Purpose: Tkinter read temperature, humidity,
    and barometric pressure every 15 seconds
"""

from tkinter import *
from tkinter.ttk import *
from easygopigo3 import EasyGoPiGo3
from di_sensors.easy_temp_hum_press import EasyTHPSensor


class THP_Sensor:
    def __init__(self):
        self.window = Tk()
        self.window.title("BME280")
        # Set the window size and location
        # 350x250 pixels in size, location at 50x50
        self.window.geometry("+100+100")
        # Color and padding to edge of window
        self.window.config(padx=10, pady=10)

        # Setup after to call function every 15 seconds
        self.window.after(15000, self.read_sensors)
        # Initialize GoPiGo3 object
        self.gpg = EasyGoPiGo3()
        # Initialize THP object
        self.my_thp = EasyTHPSensor()

        self.create_widgets()
        self.read_sensors()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        mainloop()

# -------------------------- READ SENSORS -------------------------------- #
    def read_sensors(self):
        """Read sensors and display data"""
        # Read temperature in fahrenheit
        self.temperature = self.my_thp.safe_fahrenheit()
        # Read relative humidity
        self.humidity = self.my_thp.safe_humidity()
        # Read the pressure in pascals
        press = self.my_thp.safe_pressure()
        # Convert pascals to inHg, compensate for 4000' altitude
        self.pressure = (press/3386.33857) + 4.08
        self.display_sensors()

# ------------------------- DISPLAY SENSORS ------------------------------ #
    def display_sensors(self):
        """Display sensor data"""
        self.lbl_temp.config(text=f"{self.temperature:.0f}°F")
        self.lbl_hum.config(text=f"{self.humidity:.0f}%")
        self.lbl_press.config(text=f"{self.pressure:.2f} inHg")

# -------------------------- CREATE WIDGETS ------------------------------- #
    def create_widgets(self):
        """Create and grid widgets"""
        # Create a main label frame to hold widgets
        self.main_frame = LabelFrame(
            self.window,
            text="BME280 Sensor",
            relief=GROOVE)

        # label to display temp
        self.lbl_temp = Label(
            self.main_frame,
            width=10,
            anchor="w")
        # label to display press
        self.lbl_press = Label(
            self.main_frame,
            width=10,
            anchor="w")
        # label to display hum
        self.lbl_hum = Label(
            self.main_frame,
            width=10,
            anchor="w")
        lbl_temperature = Label(
            self.main_frame,
            text="Temperature:"
        )
        lbl_humidity = Label(
            self.main_frame,
            text="Humidity:"
        )
        lbl_pressure = Label(
            self.main_frame,
            text="Pressure:"
        )
        # Use grid layout manager to place widgets in the frame
        lbl_temperature.grid(row=0, column=0, sticky=E)
        self.lbl_temp.grid(row=0, column=1)
        lbl_humidity.grid(row=1, column=0, sticky=E)
        self.lbl_hum.grid(row=1, column=1)
        lbl_pressure.grid(row=2, column=0, sticky=E)
        self.lbl_press.grid(row=2, column=1)

        # Set padding between frame and window
        self.main_frame.grid_configure(padx=5, pady=5)
        # set padding for all widgets in the frame
        for widget in self.main_frame.winfo_children():
            widget.grid_configure(padx=4, pady=4)

# --------------------------- ON CLOSING ----------------------------------#
    def on_closing(self):
        # Unconfigure the sensors, disable the motors,
        # and restore the LED to the control of the GoPiGo3 firmware
        self.gpg.reset_all()
        self.window.destroy()


thp_sensor = THP_Sensor()
