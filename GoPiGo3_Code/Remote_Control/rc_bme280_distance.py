#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purpose: GoPiGo3 Tkinter remote control program
with Bosch BME280 Temperature, Humidity, and Pressure sensor
!!! Distance sensor is not implemented yet in this program !!!
 ------------------------------------------------
 History
 ------------------------------------------------
 Author     Date           Comments
 Loring     09/12/21       Convert to EasyGoPiGo3, OOP, test with Python 3.7
 Loring     10/23/21       Add battery voltage display
 Loring     11/11/21       Add BME280 sensor display
"""
from time import sleep
import tkinter as tk
import tkinter.ttk as ttk
from threading import Thread
# Import EasyGoPiGo3 library
import easygopigo3 as easy
from di_sensors.easy_temp_hum_press import EasyTHPSensor

# Set servo pointing straight ahead
# You may have to change the degrees to adapt to your servo
# All servos line up slightly differently
FORWARD = 90
MAX_SPEED = 300             # Maximum speed setting for GoPiGo3
MIN_SPEED = 100             # Minimum speed setting for GoPiGo3


class GoPiGoGUI:
    def __init__(self):
        # ------------------- INITIALIZE GUI ------------------------------- #
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

        # ------------------- INITIALIZE GOPIGO ---------------------------- #
        # Create EasyGoPiGo3 object
        self.gpg = easy.EasyGoPiGo3()
        # Set initial speed
        self.gpg.set_speed(200)

        # Create EasyTHPSensor object
        self.my_thp = EasyTHPSensor()
        # Create distance sensor object
        self.distance_sensor = self.gpg.init_distance_sensor("AD1")

        # Initialize servo object on Servo Port 2
        self.servo = self.gpg.init_servo("SERVO1")
        self.servo.rotate_servo(FORWARD)

        # Initial reading of environment data for initial display
        self.read_environment_data()

        self.create_frames()
        self.create_widgets()

        # ---------------------- SENSOR THREADS ---------------------------- #
        # Start distance sensor thread
        self.sensor_thread = Thread(target=self.display_environment_data)
        # Thread will close when main program exits
        self.sensor_thread.daemon = True
        self.sensor_thread.start()

        # Start the mainloop of the tkinter program
        self.window.mainloop()

# -------------------------- READ ENVIRONMENT DATA ------------------------- #
    def read_environment_data(self):
        """Read Bosch bme280 sensor, temp, humidity, pressure"""
        # Read temperature
        # temp = my_thp.safe_celsius()
        self.temp_fahrenheit = self.my_thp.safe_fahrenheit()

        # Compensate for heat of Raspberry Pi
        self.temp_fahrenheit = self.temp_fahrenheit - 4

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
        """Display environment data"""
        self.read_environment_data()
        # Display new readings
        self.lbl_voltage.config(text=f"Voltage: {self.voltage}V")
        self.lbl_temp.config(text=f"Temp: {self.temp_fahrenheit:,.2f}°F")
        self.lbl_humidity.config(
            text=f"Humidity: {self.humidity:.1f}%")
        self.lbl_pressure.config(
            text=f"Press: {self.press_inhg:.2f} inHg")
        # Read sensor data every 15 seconds
        sleep(15)

# ------------------------- INCREASE SPEED ------------------------------- #
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
            self.window,
            text="Remote Control",
            relief=tk.GROOVE)
        self.middle_frame = ttk.LabelFrame(
            self.window,
            text="Environmental Sensors",
            relief=tk.GROOVE)
        self.bottom_frame = ttk.Frame(
            self.window, relief=tk.GROOVE)
        self.top_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        self.middle_frame.pack(fill=tk.X, padx=10, pady=10)
        self.bottom_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.top_frame.pack_propagate(False)
        self.middle_frame.pack_propagate(False)
        self.bottom_frame.pack_propagate(False)

# ------------------------- CREATE WIDGETS --------------------------------- #
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
            self.middle_frame, text=f"Temp: {round(self.temp_fahrenheit, 2)} °F")
        self.lbl_humidity = ttk.Label(
            self.middle_frame, text=f"Humidity: {round(self.humidity, 1)}%")
        self.lbl_pressure = ttk.Label(
            self.middle_frame, text=f"Press: {round(self.press_inhg, 2)} inHg")

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


    # ------------------------- QUIT PROGRAM ----------------------------- #
    def quit(self):
        self.window.destroy()


# Create remote control object
gopigo_gui = GoPiGoGUI()
