#!/usr/bin/env python3
# Based on
# https://pythonprogramming.net/robotics-raspberry-pi-tutorial-gopigo-introduction
# EasyGoPiGo3 documentation: https://gopigo3.readthedocs.io/en/latest
# Purpose: GoPiGo3 Tkinter remote control program
# with Dexter Temperature, Humidity and Pressure sensor
# ------------------------------------------------
# History
# ------------------------------------------------
# Author     Date           Comments
# Loring     09/12/21       Convert to EasyGoPiGo3, OOP, test with Python 3.5
# Loring     10/23/21       Add battery voltage display
# Loring     11/11/21       Add BME280 sensor display

from tkinter import *       # Import tkinter for GUI
import sys                  # Used to exit the program
import easygopigo3 as easy  # Import EasyGoPiGo3 library
from di_sensors.easy_temp_hum_press import EasyTHPSensor


class GoPiGoGUI:
    def __init__(self):
        """ Initialize the program """
        self.BG = "white"
        # Create EasyGoPiGo3 object
        self.gpg = easy.EasyGoPiGo3()
        self.gpg.set_speed(200)  # Set initial speed
        # Initialize an EasyTHPSensor object
        self.my_thp = EasyTHPSensor()

        self.window = Tk()
        self.window.title("GoPiGo Remote Control")
        # Set the window size and location
        # 350x250 pixels in size, location at 50x50
        self.window.geometry("400x325+50+50")
        # The window can't be resized
        self.window.resizable(0, 0)
        # Color and padding to edge of window
        self.window.config(padx=10, pady=10)
        self.window.config(bg=self.BG)
        # Bind all key input events to the window
        # This will capture all keystrokes for remote control of robot
        self.window.bind_all('<Key>', self.key_input)

        # Read the sensor the first time
        self.read_environment()

        self.create_widgets()       # Create and layout widgets

        # Every 15 seconds (15000 ms), read the BME280 sensor
        # after runs a function so many milliseconds after the mainloop starts
        # this callback function runs when the mainloop isn't busy
        # after is a non blocking call, it does not interrupt or stall execution
        self.window.after(15000, self.refresh_readings)

        self.window.mainloop()      # Start the mainloop of the tkinter program

#--------------------------------- CREATE WIDGETS -------------------------------------#
    def create_widgets(self):
        """ Create and layout widgets """
        # Reference for GUI display
        """
        W = Forward      Q = Spin Left
        S = Backward     E = Spin Right
        A = Left         T = Increase Speed
        D = Right        G = Decrease Speed  
        Spacebar = Stop
        Speed: 200      Voltage 
        Temp          Humidty     Pressure
        Z = Exit    Exit button
        
        """
        # Create widgets
        lbl_remote_w = Label(text="W: Forward", bg=self.BG)
        lbl_remote_q = Label(text="Q: Spin Left", bg=self.BG)
        lbl_remote_s = Label(text="S: Backward", bg=self.BG)
        lbl_remote_e = Label(text="E: Spin Right", bg=self.BG)
        lbl_remote_a = Label(text="A: Left", bg=self.BG)
        lbl_remote_d = Label(text="D: Right", bg=self.BG)
        lbl_remote_t = Label(text="T: Increase Speed", bg=self.BG)
        lbl_remote_g = Label(text="G: Decrease Speed", bg=self.BG)
        lbl_remote_spacebar = Label(text="Spacebar: Stop", bg=self.BG)
        lbl_remote_z = Label(text="Z: Exit", bg=self.BG)

        # Get and display current GoPiGo speed setting
        speed = self.gpg.get_speed()
        self.lbl_speed = Label(text="Speed: " + str(speed), bg=self.BG)

        self.lbl_voltage = Label(
            text="Voltage: " + str(self.voltage) + "V", bg=self.BG)

        self.lbl_temperature = Label(text="Temp: " + str(round(
            self.temperature, 2)) + "°F", bg=self.BG)
        self.lbl_humidity = Label(text="Humidity: " + str(round(
            self.humidity, 1)) + "%", bg=self.BG)
        self.lbl_pressure = Label(text="Press: " + str(round(
            self.pressure, 2)) + " inHg", bg=self.BG)

        btn_exit = Button(text="Exit", command=self.exit_program)

        # Grid the widgets
        lbl_remote_w.grid(row=0, column=0, sticky=W)
        lbl_remote_q.grid(row=0, column=1, sticky=W)

        lbl_remote_s.grid(row=1, column=0, sticky=W)
        lbl_remote_e.grid(row=1, column=1, sticky=W)

        lbl_remote_a.grid(row=2, column=0, sticky=W)
        lbl_remote_t.grid(row=2, column=1, sticky=W)

        lbl_remote_d.grid(row=3, column=0, sticky=W)
        lbl_remote_g.grid(row=3, column=1, sticky=W)

        lbl_remote_spacebar.grid(row=4, column=0, sticky=W)

        self.lbl_speed.grid(row=5, column=0, sticky=W)
        self.lbl_voltage.grid(row=5, column=1, sticky=W)

        self.lbl_temperature.grid(row=6, column=0, sticky=W)
        self.lbl_humidity.grid(row=6, column=1, sticky=W)
        self.lbl_pressure.grid(row=6, column=2, sticky=W)
        lbl_remote_z.grid(row=8, column=0, sticky=W)
        btn_exit.grid(row=8, column=1, sticky=E)

        # Set padding for all widgets
        for child in self.window.winfo_children():
            child.grid_configure(padx=5, pady=5)

#--------------------------------- READ ENVIRONMENT -------------------------------------#
    def read_environment(self):
        """ Read the bme280 sensor """
        # Read temperature
        # temp = my_thp.safe_celsius()
        self.temperature = self.my_thp.safe_fahrenheit()

        # Read relative humidity
        self.humidity = self.my_thp.safe_humidity()

        # Read pressure in pascals
        press = self.my_thp.safe_pressure()

        # Convert pascals to inHg, compensate for 4000' altitude
        self.pressure = (press / 3386.38867) + 4.08

        self.voltage = round(self.gpg.volt(), 1)


#--------------------------------- INCREASE SPEED -------------------------------------#

    def refresh_readings(self):
        """ Call the fead the bme280 sensor method """
        self.read_environment()
        # Display new readings
        self.lbl_voltage.config(text="Voltage: " + str(self.voltage) + "V")
        self.lbl_temperature.config(text="Temp: " + str(round(
            self.temperature, 2)) + "°F", bg=self.BG)
        self.lbl_humidity.config(text="Humidity: " + str(round(
            self.humidity, 1)) + "%", bg=self.BG)
        self.lbl_pressure.config(text="Press: " + str(round(
            self.pressure, 2)) + " inHg", bg=self.BG)

        self.window.after(15000, self.refresh_readings)

#--------------------------------- INCREASE SPEED -------------------------------------#
    def increase_speed(self):
        """ Increase the speed of the GoPiGo """
        speed = self.gpg.get_speed()    # Get the current speed
        speed = speed + 100             # Add 100 to the current speed
        # Keep speed from going beyond 1000
        if(speed > 1000):
            speed = 1000
        self.gpg.set_speed(speed)       # Set the new speed
        # Display current speed
        self.lbl_speed.config(text="Speed: " + str(speed))

#--------------------------------- DECREASE SPEED -------------------------------------#
    def decrease_speed(self):
        """ Decrease the speed of the GoPiGo """
        speed = self.gpg.get_speed()    # Get current speed
        speed = speed - 100             # Subtract 100 from the current speed
        # Keep speed from going below 0
        if(speed < 100):
            speed = 100
        self.gpg.set_speed(speed)       # Set the new speed
        # Display current speed
        self.lbl_speed.config(text="Speed: " + str(speed))

#----------------------------- EXIT PROGRAM ---------------------------------#
    def exit_program(self):
        print("\nExiting")
        sys.exit()

#--------------------------------- KEY INPUT -----------------------------------------#
    def key_input(self, event):
        # Get all key preseses as lower case
        key_press = event.keysym.lower()
        # print(key_press)  # For testing

        # Move Forward
        if key_press == 'w':
            self.gpg.forward()

        # Move Backward
        elif key_press == 's':
            self.gpg.backward()
            # Turn both blinkers on
            self.gpg.led_on("left")
            self.gpg.led_on("right")

        # Turn Left
        elif key_press == 'a':
            self.gpg.left()
            self.gpg.led_on("left")

        # Turn Right
        elif key_press == 'd':
            self.gpg.right()
            self.gpg.led_on("right")

        # Spin Left
        elif key_press == 'q':
            self.gpg.spin_left()
            self.gpg.led_on("left")

        # Spin Right
        elif key_press == 'e':
            self.gpg.spin_right()
            self.gpg.led_on("right")

        # Increase Speed
        elif key_press == 't':
            self.increase_speed()

        # Decrease Speed
        elif key_press == 'g':
            self.decrease_speed()

        # Stop
        elif key_press == 'space':
            self.gpg.stop()
            # Turn off the blinkers
            self.gpg.led_off("left")
            self.gpg.led_off("right")

        # Exit program
        elif key_press == 'z':
            self.exit_program()


# Create remote control object
gopigo_gui = GoPiGoGUI()
