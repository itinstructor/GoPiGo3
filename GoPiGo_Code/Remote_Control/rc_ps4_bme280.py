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
from ps4_gopigo import MyController

# Set servo pointing straight ahead
# You may have to change the degrees to adapt to your servo
# All servos line up slightly differently
FORWARD = 90


class GoPiGoGUI:
    def __init__(self):
        # -------------------- INITIALIZE PROGRAM WINDOW --------------------- #
        self.root = tk.Tk()
        self.root.title("GoPiGo3 Remote")
        # Set the window size and location
        # horizontal vertical pixels in size, location at 50x50
        self.root.geometry("+50+50")
        # The window can't be resized
        self.root.resizable(0, 0)
        # Call self.quit when window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        # Color and padding to edge of window
        self.root.config(padx=5, pady=5)
        # Create EasyGoPiGo3 object

    # ---------------------- INITIALIZE GOPIGO3 -------------------------- #
        self.gpg = easy.EasyGoPiGo3()

        # Create EasyTHPSensor object
        self.my_thp = EasyTHPSensor()

        # Initialize distance sensor, connect to AD1 port
        self.distance_sensor = self.gpg.init_distance_sensor('AD1')

        # Run PS4 controller in daemon thread
        self.run_controller_in_thread()

    # ---------------------- DISTANCE SENSOR THREAD ---------------------- #
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
        self.root.mainloop()

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
    def run_controller_in_thread(self):
        def controller_task():
            # Create an instance of the MyController class,
            # Specify the connection interface
            # js0 is commonly used for the first controller
            # Disable the use of ds4drv (if applicable)
            controller = MyController(
                # Specify the device interface to connect to
                interface="/dev/input/js0",
                connecting_using_ds4drv=False
            )
            # Start listening for joystick input from the controller
            # Continuously read data from the joystick until timeout occurs
            # (the controller should be paired within this timeframe)
            # Argument: Timeout in seconds (optional, defaults to None) timeout=60
            controller.listen(timeout=60)

        # Create and start a daemon thread for the controller
        controller_thread = Thread(target=controller_task)
        controller_thread.daemon = True
        controller_thread.start()

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
        self.root.after(15000, self.display_environment_data)

# ------------------------- INCREASE SPEED --------------------------------#
    def increase_speed(self):
        """Increase speed of the GoPiGo"""
        # Get the current speed
        speed = self.gpg.get_speed()
        # Add 100 to the current speed
        speed = speed + 100
        # Keep speed from going beyond 1000
        if (speed > 600):
            speed = 600
        # Set new speed
        self.gpg.set_speed(speed)
        # Display current speed
        self.lbl_speed.config(text=f"Speed: {speed}")

# ------------------------- DECREASE SPEED ------------------------------- #
    def decrease_speed(self):
        """Decrease speed of the GoPiGo"""
        # Get current speed
        speed = self.gpg.get_speed()
        # Subtract 100 from the current speed
        speed = speed - 100
        # Keep speed from going below 0
        if (speed < 100):
            speed = 100
        # Set new speed
        self.gpg.set_speed(speed)
        # Display current speed
        self.lbl_speed.config(text=f"Speed: {speed}")

# -------------------------- KEY INPUT ----------------------------------- #
    def remote_control(self, event):
        """Get keystrokes for remote control"""
        # Get all key presses as lower case
        key_press = event.keysym.lower()
        # Set initial speed for keystroke capture
        self.gpg.set_speed(200)

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
        elif key_press == "space":
            self.gpg.stop()
            # Turn off the blinkers
            self.gpg.led_off("left")
            self.gpg.led_off("right")

        # Quit program
        elif key_press == "escape":
            self.quit()

# ------------------------- CREATE FRAMES -------------------------------- #
    def create_frames(self):
        """Create and set frames to fill up window"""
        self.top_frame = ttk.LabelFrame(
            self.root,
            text="Keyboard Control",
            relief=tk.GROOVE)

        self.middle_frame = ttk.LabelFrame(
            self.root,
            text="Sensors",
            relief=tk.GROOVE)

        self.bottom_frame = ttk.Frame(
            self.root, relief=tk.GROOVE)

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
            self.middle_frame, text=f"Temp: {round(self.temp_f, 2)} °F")
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
        self.root.bind_all('<Key>', self.remote_control)

    # ------------------------- QUIT PROGRAM ----------------------------- #
    def quit(self):
        """Deconfigure the sensors, disable the motors,
        restore the LED to the control of the GoPiGo3 firmware."""
        self.servo.disable_servo()
        self.gpg.reset_all()
        self.root.destroy()


# Create remote control object
gopigo_gui = GoPiGoGUI()
