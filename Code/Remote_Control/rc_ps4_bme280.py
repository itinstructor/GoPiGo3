#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Filename: rc_ps4_bme280.py
# Based on
# https://pythonprogramming.net/robotics-raspberry-pi-tutorial-gopigo-introduction
# EasyGoPiGo3 documentation: https://gopigo3.readthedocs.io/en/latest
# Purpose: GoPiGo3 Tkinter remote control program
# with Bosch BME280 Temperature, Humidity, and Pressure sensor
# ------------------------------------------------
# History
# ------------------------------------------------
# Author     Date           Comments
# Loring     03/23/25       Add PS4 controller support with PyGame
# Loring     09/12/21       Convert to EasyGoPiGo3, OOP, test with Python 3.7
# Loring     10/23/21       Add battery voltage display
# Loring     11/11/21       Add BME280 sensor display
# Loring     08/15/24       Add PS4 controller support

from time import sleep      # Import sleep function
from threading import Thread

import tkinter as tk
import tkinter.ttk as ttk
# Import EasyGoPiGo3 library
import easygopigo3 as easy
from di_sensors.easy_temp_hum_press import EasyTHPSensor

# Import ps4 controller library
from ps4_gopigo_pygame import PS4Controller

# Set servo pointing straight ahead
# You may have to change the degrees to adapt to your servo
# All servos line up slightly differently
FORWARD = 90
MAX_SPEED = 600             # Maximum speed setting for GoPiGo3
MIN_SPEED = 100             # Minimum speed setting for GoPiGo3


class GoPiGoGUI:
    def __init__(self):
        # ------------------ INITIALIZE PROGRAM WINDOW --------------------- #
        self.window = tk.Tk()
        self.window.title("GoPiGo3 Remote")
        # Set the window size and location
        # horizontal vertical pixels in size, location at 50x50
        self.window.geometry("+50+50")
        # The window can't be resized
        self.window.resizable(0, 0)
        # Call self.quit when window is closed
        self.window.protocol("WM_DELETE_WINDOW", self.quit)
        # Color and padding to edge of window
        self.window.config(padx=5, pady=5)
        # Create EasyGoPiGo3 object

    # ---------------------- INITIALIZE GOPIGO3 ---------------------------- #
        self.gpg = easy.EasyGoPiGo3()

        # Create EasyTHPSensor object
        self.my_thp = EasyTHPSensor()

        # Initialize distance sensor, connect to AD1 port
        self.distance_sensor = self.gpg.init_distance_sensor('AD1')

        # Run PS4 controller in daemon thread
        self.controller_running = True
        self.ps4_controller = None

        # Start controller thread
        controller_thread = Thread(target=self.controller_task)
        controller_thread.daemon = True
        controller_thread.start()

    # ---------------------- DISTANCE SENSOR THREAD ------------------------ #
        # Create flag for controlling the distance sensor thread
        self.running = True

        # Start distance sensor thread
        self.sensor_thread = Thread(target=self.distance_sensor_loop)
        # Thread will close when main program exits
        self.sensor_thread.daemon = True
        self.sensor_thread.start()

        # Set initial speed
        self.gpg.set_speed(200)

        # Initialize servo object on Servo Port 2
        self.servo = self.gpg.init_servo("SERVO2")
        self.servo.rotate_servo(FORWARD)

        # Read sensors for the first time
        self.read_environment_data()

        self.create_frames()
        self.create_widgets()

        # Start the mainloop of the tkinter program
        self.window.mainloop()

# ---------------------- DISTANCE SENSOR LOOP ---------------------------- #
    def distance_sensor_loop(self):
        """Continuous loop for reading distance sensor"""
        try:
            while self.running:
                # Read the sensor data in inches or mm
                # mm = self.distance_sensor.read_mm()
                inches = self.distance_sensor.read_inches()

                # Calculate feet and inches
                # Use integer division to get the whole number of feet
                feet = inches // 12
                # Use modulus to get the remaining inches
                remaining_inches = inches % 12

                # Print the values
                self.lbl_distance.config(
                    text=f"Distance: {feet:.0f}' {remaining_inches:.0f}\"")

                # Add a small delay to prevent overwhelming the CPU
                sleep(0.1)

        except Exception as e:
            self.lbl_distance.config(text=f"Distance: Error {e}")
            # Uncomment the line below to see the error in the console
            # print(f"Error in distance sensor thread: {e}")

# --------------------- RUN CONTROLLER IN THREAD ------------------------- #
    def controller_task(self):
        """Background thread for PS4 controller"""
        try:
            self.ps4_controller = PS4Controller()
            while self.controller_running:
                # Non-blocking update
                sleep(0.016)  # ~60Hz refresh rate
        except Exception as e:
            print(f"Controller error: {e}")

# -------------------------- READ ENVIRONMENT DATA ----------------------- #
    def read_environment_data(self):
        """Read Bosch bme280 sensor, temp, humidity, pressure"""
        # Read temperature
        # temp = my_thp.safe_celsius()
        self.temp_f = self.my_thp.safe_fahrenheit()
        # Compensate for heat of Raspberry Pi
        self.temp_f = self.temp_f - 4
        # Read relative humidity
        self.humidity = self.my_thp.safe_humidity()

        # Read barometric pressure in pascals
        press_pascals = self.my_thp.safe_pressure()
        # Convert pascals to inHg
        press_inhg = press_pascals / 3386.3886666667

        # Compensate for 3960' altitude 4.04
        # Scottsbluff, NE, Heilig Field, 4.04
        self.press_inhg = press_inhg + 4.04

        # Read GPG3 battery voltage
        self.voltage = round(self.gpg.volt(), 1)

# ------------------- DISPLAY ENVIRONMENT DATA --------------------------- #
    def display_environment_data(self):
        """Display environment data on the GUI"""
        self.read_environment_data()

        # Display new readings
        self.lbl_voltage.config(text=f"Voltage: {self.voltage}V")
        self.lbl_temp.config(
            text=f"Temp: {self.temp_f:.2f}u'\N{DEGREE SIGN}'F")
        self.lbl_humidity.config(
            text=f"Humidity: {round(self.humidity, 1)}%")
        self.lbl_pressure.config(
            text=f"Press: {round(self.press_inhg, 2)} inHg")

        # Every 15 seconds (15000 ms), read the BME280 sensor
        # 'after' runs a function so many milliseconds after the mainloop starts
        # this callback function runs when the mainloop isn't busy
        # 'after' is a non blocking call, it does not interrupt or stall execution
        self.window.after(15000, self.display_environment_data)

# ------------------------- INCREASE SPEED --------------------------------#
    def increase_speed(self):
        """ Increase the speed of the GoPiGo """
        speed = self.gpg.get_speed()    # Get the current speed
        speed = speed + 100             # Add 100 to the current speed
        # Keep speed from going beyond MAX_SPEED
        if (speed > MAX_SPEED):
            speed = MAX_SPEED
        # Set the new speed
        self.gpg.set_speed(speed)
        # Display current speed
        self.lbl_speed.config(text=f"Speed: {speed}")

# ------------------------- DECREASE SPEED ------------------------------- #
    def decrease_speed(self):
        """ Decrease the speed of the GoPiGo """
        speed = self.gpg.get_speed()    # Get current speed
        speed = speed - 100             # Subtract 100 from the current speed
        # Keep speed from going below 0
        if (speed < MIN_SPEED):
            speed = MIN_SPEED
        self.gpg.set_speed(speed)       # Set the new speed
        # Display current speed
        self.lbl_speed.config(text=f"Speed: {speed}")

# -------------------------- KEY INPUT ----------------------------------- #
    def remote_control(self, event):
        """Get keystrokes for remote control"""
        # Get all key presses as lower case
        key_press = event.keysym.lower()

        # Get current speed setting
        base_speed = self.gpg.get_speed()
        left_speed = 0
        right_speed = 0

        # Move Forward
        if key_press == 'w':
            left_speed = base_speed
            right_speed = base_speed

        # Move Backward
        elif key_press == 's':
            left_speed = -base_speed
            right_speed = -base_speed
            self.gpg.led_on("left")
            self.gpg.led_on("right")

        # Turn Left
        elif key_press == 'a':
            left_speed = base_speed * 0.3  # Reduce inside wheel speed
            right_speed = base_speed
            self.gpg.led_on("left")

        # Turn Right
        elif key_press == 'd':
            left_speed = base_speed
            right_speed = base_speed * 0.3  # Reduce inside wheel speed
            self.gpg.led_on("right")

        # Spin Left
        elif key_press == 'q':
            left_speed = -base_speed
            right_speed = base_speed
            self.gpg.led_on("left")

        # Spin Right
        elif key_press == 'e':
            left_speed = base_speed
            right_speed = -base_speed
            self.gpg.led_on("right")

        # Stop
        elif key_press == "space":
            left_speed = 0
            right_speed = 0
            self.gpg.led_off("left")
            self.gpg.led_off("right")

        # Increase Speed
        elif key_press == 't':
            self.increase_speed()

        # Decrease Speed
        elif key_press == 'g':
            self.decrease_speed()

        # Quit program
        elif key_press == "escape":
            self.quit()

        # Set motor speeds using DPS (Degrees Per Second)
        self.gpg.set_motor_dps(self.gpg.MOTOR_LEFT, left_speed)
        self.gpg.set_motor_dps(self.gpg.MOTOR_RIGHT, right_speed)

# ------------------------- CREATE FRAMES -------------------------------- #
    def create_frames(self):
        """Create and set frames to fill up window"""
        self.top_frame = ttk.LabelFrame(
            self.window,
            text="Keyboard Control",
            relief=tk.GROOVE)

        self.middle_frame = ttk.LabelFrame(
            self.window,
            text="Sensors",
            relief=tk.GROOVE)

        self.bottom_frame = ttk.Frame(
            self.window, relief=tk.GROOVE)

        self.top_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        self.middle_frame.pack(fill=tk.X, padx=10, pady=10)
        self.bottom_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.top_frame.pack_propagate(False)
        self.middle_frame.pack_propagate(False)
        self.bottom_frame.pack_propagate(False)

# ------------------------- CREATE WIDGETS ------------------------------- #
    def create_widgets(self):
        """Create and layout widgets"""
        # Reference for GUI display
        """
                    W: Forward      
        A: Left    Spacebar: Stop   D: Right   
                    S: Backward     
        Q = Spin Left   E = Spin Right
        T = Increase Speed  G = Decrease Speed  
        
        Speed: 200      Voltage 
        Temp          Humidity     Pressure
        Exit button
        
        """
        # Create widgets
        lbl_remote_w = ttk.Label(
            self.top_frame, text=" W: Forward", relief=tk.RIDGE)
        lbl_remote_a = ttk.Label(
            self.top_frame, text=" A: Left", relief=tk.RIDGE)
        lbl_remote_spacebar = ttk.Label(
            self.top_frame, text=" Spacebar: Stop", relief=tk.RIDGE)
        lbl_remote_d = ttk.Label(
            self.top_frame, text=" D: Right", relief=tk.RIDGE)
        lbl_remote_s = ttk.Label(
            self.top_frame, text=" S: Reverse", relief=tk.RIDGE)

        lbl_remote_q = ttk.Label(
            self.top_frame, text=" Q: Spin Left", relief=tk.RIDGE)
        lbl_remote_e = ttk.Label(
            self.top_frame, text=" E: Spin Right", relief=tk.RIDGE)

        lbl_remote_t = ttk.Label(
            self.top_frame, text=" T: Increase Speed", relief=tk.RIDGE)
        lbl_remote_g = ttk.Label(
            self.top_frame, text=" G: Decrease Speed", relief=tk.RIDGE)

        # Get and display current GoPiGo speed setting
        speed = self.gpg.get_speed()
        self.lbl_speed = ttk.Label(
            self.middle_frame, text=f"Speed: {speed}")
        self.lbl_voltage = ttk.Label(
            self.middle_frame,
            text=f"Voltage: {self.voltage}V")

        # Display temp, humidity, and pressure
        self.lbl_temp = ttk.Label(
            self.middle_frame, text=f"Temp: {round(self.temp_f, 2)} \u00B0F")
        self.lbl_humidity = ttk.Label(
            self.middle_frame,
            text=f"Humidity: {round(self.humidity, 1)}%")
        self.lbl_pressure = ttk.Label(
            self.middle_frame,
            text=f"Press: {round(self.press_inhg, 2)} inHg")

        self.lbl_distance = ttk.Label(
            self.middle_frame,
            text="Distance: ")

        btn_exit = ttk.Button(self.bottom_frame, text="Exit",
                              command=self.quit)

        # Grid top frame widgets
        lbl_remote_w.grid(row=0, column=1, columnspan=2, sticky=tk.W)
        lbl_remote_a.grid(row=1, column=0, sticky=tk.W)
        lbl_remote_spacebar.grid(row=1, column=1, columnspan=2, sticky=tk.W)
        lbl_remote_d.grid(row=1, column=3, sticky=tk.E)
        lbl_remote_s.grid(row=2, column=1, columnspan=2, sticky=tk.W)

        lbl_remote_q.grid(row=3, column=0, sticky=tk.W)
        lbl_remote_e.grid(row=3, column=3, sticky=tk.W)

        lbl_remote_t.grid(row=4, column=0, columnspan=2, sticky=tk.W)
        lbl_remote_g.grid(row=4, column=2, columnspan=2, sticky=tk.E)

        # Grid middle frame widgets
        self.lbl_speed.grid(row=0, column=0, sticky=tk.W)
        self.lbl_voltage.grid(row=0, column=1, sticky=tk.W)

        self.lbl_temp.grid(row=1, column=0, sticky=tk.W)
        self.lbl_humidity.grid(row=1, column=1, sticky=tk.W)
        self.lbl_pressure.grid(row=2, column=0, sticky=tk.W)
        self.lbl_distance.grid(row=2, column=1, sticky=tk.W)

        # Bottom Frame Widgets
        btn_exit.grid(row=1, column=1, sticky=tk.E)

        # Set padding for all widgets
        PAD = 7
        for widget in self.top_frame.winfo_children():
            widget.grid_configure(padx=PAD, pady=PAD, ipadx=PAD, ipady=PAD)
        for widget in self.middle_frame.winfo_children():
            widget.grid_configure(padx=PAD, pady=PAD)
        for widget in self.bottom_frame.winfo_children():
            widget.grid_configure(padx=PAD, pady=PAD)

        # Bind all key input events to the window
        # This will capture all keystrokes for remote control of robot
        self.window.bind_all('<Key>', self.remote_control)

# ----------------------------- QUIT PROGRAM ------------------------------- #
    def quit(self):
        """Clean shutdown"""
        self.controller_running = False
        self.running = False  # Stop distance sensor
        self.window.destroy()


# Create remote control object
gopigo_gui = GoPiGoGUI()

