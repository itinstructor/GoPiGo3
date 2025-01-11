#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# Purpose: GoPiGo3 Tkinter remote control program
# ------------------------------------------------
# History
# ------------------------------------------------
# Author     Date           Comments
# Loring     11/10/24       Add threading for distance sensor
# Loring     09/12/21       Convert to EasyGoPiGo3, OOP, test with Python 3.5
# Loring     10/23/21       Add battery voltage display
"""
from tkinter import *       # Import tkinter for GUI
from tkinter.ttk import *   # Add ttk themed widgets
from time import sleep      # Import sleep function
from threading import Thread

import easygopigo3 as easy  # Import EasyGoPiGo3 library


class GoPiGoGUI:
    def __init__(self):
        """ Initialize the program """
    # -------------------- INITIALIZE PROGRAM WINDOW --------------------- #
        self.window = Tk()
        self.window.title("GoPiGo Remote Control")

        # Set the window size and location
        # 350x250 pixels in size, location at 50x50
        self.window.geometry("375x275+50+50")

        # Padding to edge of window
        self.window.config(padx=10, pady=10)

        self.window.protocol("WM_DELETE_WINDOW", self.quit)

        # Bind all key input events to the window
        # This will capture all keystrokes for remote control of robot
        self.window.bind_all('<Key>', self.key_input)

    # ---------------------- INITIALIZE GOPIGO3 -------------------------- #
        # Create EasyGoPiGo3 object
        self.gpg = easy.EasyGoPiGo3()

        # Set initial speed
        self.gpg.set_speed(200)

        # Initialize distance sensor
        self.distance_sensor = self.gpg.init_distance_sensor()

    # ---------------------- DISTANCE SENSOR THREAD ---------------------- #
        # Create flag for controlling the distance sensor thread
        self.running = True

        # Start distance sensor thread
        self.sensor_thread = Thread(target=self.distance_sensor_loop)
        # Thread will close when main program exits
        self.sensor_thread.daemon = True
        self.sensor_thread.start()

    # -------------------------- GUI WINDOW ------------------------------ #
        self.create_widgets()
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

                # Display the values
                self.lbl_distance_display.configure(
                    text=f"  {feet:.0f}' {remaining_inches:.0f}\"")

                # Add a small delay to prevent overwhelming the CPU
                sleep(0.1)

        except Exception as e:
            self.lbl_distance_display.configure(text=f"Error: {e}")
            # Uncomment the line below to see the error in the console
            # print(f"Error in distance sensor thread: {e}")

# -------------------------- CREATE WIDGETS -------------------------------#
    def create_widgets(self):
        """ Create and layout widgets """
        # Reference for GUI display
        """
        W = Forward      Q = Spin Left
        S = Backward     E = Spin Right
        A = Left         T = Increase Speed
        D = Right        G = Decrease Speed  
        Spacebar = Stop
        Temp
        Speed: 200      Voltage 
        Z = Exit    Exit button
        """
        # Create widgets
        lbl_remote_w = Label(text="W: Forward")
        lbl_remote_q = Label(text="Q: Spin Left")
        lbl_remote_s = Label(text="S: Backward")
        lbl_remote_e = Label(text="E: Spin Right")
        lbl_remote_a = Label(text="A: Left")
        lbl_remote_d = Label(text="D: Right")
        lbl_remote_t = Label(text="T: Increase Speed")
        lbl_remote_g = Label(text="G: Decrease Speed")
        lbl_remote_spacebar = Label(text="Spacebar: Stop")
        lbl_remote_z = Label(text="Z: Exit")

        self.lbl_distance = Label(text="Distance: ")
        self.lbl_distance_display = Label(text="")

        # Get and display battery voltage
        btn_voltage = Button(text="Voltage", command=self.get_battery_voltage)
        # Round the voltage to 1 decimal place
        voltage = round(self.gpg.volt(), 1)
        self.lbl_voltage = Label(
            text="Voltage: " + str(voltage) + "V")

        btn_exit = Button(text="Exit", command=self.quit)

        # Get and display current GoPiGo speed setting
        speed = self.gpg.get_speed()
        self.lbl_speed = Label(text=f"Speed: {speed}")

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

        self.lbl_distance.grid(row=4, column=1, sticky=E)
        self.lbl_distance_display.grid(row=4, column=2, sticky=W)

        self.lbl_speed.grid(row=5, column=0, sticky=W)
        btn_voltage.grid(row=5, column=1, sticky=E)
        self.lbl_voltage.grid(row=5, column=2, sticky=W)
        lbl_remote_z.grid(row=6, column=0, sticky=W)
        btn_exit.grid(row=6, column=1, sticky=E)

        # Set padding for all widgets
        for child in self.window.winfo_children():
            child.grid_configure(padx=5, pady=5)

# ------------------------- INCREASE SPEED ------------------------------- #
    def increase_speed(self):
        """ Increase the speed of the GoPiGo """
        speed = self.gpg.get_speed()    # Get the current speed
        speed = speed + 100             # Add 100 to the current speed
        # Keep speed from going beyond 1000
        if (speed > 1000):
            speed = 1000
        self.gpg.set_speed(speed)       # Set the new speed
        # Display current speed
        self.lbl_speed.config(text="Speed: " + str(speed))

# ------------------------ DECREASE SPEED -------------------------------- #
    def decrease_speed(self):
        """ Decrease the speed of the GoPiGo """
        speed = self.gpg.get_speed()    # Get current speed
        speed = speed - 100             # Subtract 100 from the current speed
        # Keep speed from going below 0
        if (speed < 100):
            speed = 100
        self.gpg.set_speed(speed)       # Set the new speed
        # Display current speed
        self.lbl_speed.config(text="Speed: " + str(speed))

# ----------------------- GET BATTERY VOLTAGE ---------------------------- #
    def get_battery_voltage(self):
        voltage = round(self.gpg.volt(), 1)
        self.lbl_voltage.config(text="Voltage: " + str(voltage) + "V")

# --------------------------- KEY INPUT ---------------------------------- #
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
            self.quit()

# ----------------------------- EXIT PROGRAM ----------------------------- #
    def quit(self):
        """Deconfigure the sensors, disable the motors,
        restore the LED to the control of the GoPiGo3 firmware."""
        self.gpg.reset_all()
        self.root.destroy()


# Create remote control object
gopigo_gui = GoPiGoGUI()
