#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: rc_gui.py
Based on https://pythonprogramming.net/robotics-raspberry-pi-tutorial-gopigo-introduction
EasyGoPiGo3 documentation: https://gopigo3.readthedocs.io/en/latest
Purpose: GoPiGo3 Tkinter remote control program
------------------------------------------------
History
------------------------------------------------
Author     Date           Comments
Loring     09/12/21       Convert to EasyGoPiGo3, OOP, test with Python 3.5
Loring     10/23/21       Add battery voltage display

"""
from tkinter import *       # Import tkinter for GUI
from tkinter.ttk import *   # Add ttk themed widgets
import easygopigo3 as easy  # Import EasyGoPiGo3 library
MAX_SPEED = 600             # Maximum speed setting for GoPiGo3
MIN_SPEED = 100             # Minimum speed setting for GoPiGo3


class GoPiGoGUI:
    def __init__(self):
        # ------------------ INITIALIZE PROGRAM WINDOW --------------------- #
        self.window = Tk()
        self.window.title("GoPiGo3 Remote Control")

        # Set the window size and location
        # 350x250 pixels in size, location at 50x50
        self.window.geometry("375x275+50+50")
        # Color and padding to edge of window
        self.window.config(padx=10, pady=10)

        self.window.protocol("WM_DELETE_WINDOW", self.quit)

    # ---------------------- INITIALIZE GOPIGO3 ---------------------------- #
        # Create EasyGoPiGo3 object
        self.gpg = easy.EasyGoPiGo3()

        # Set initial speed
        self.gpg.set_speed(200)

        self.create_widgets()
        self.window.mainloop()

# ------------------------- INCREASE SPEED --------------------------------- #
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

# ------------------------ DECREASE SPEED ---------------------------------- #
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

# ----------------------- GET BATTERY VOLTAGE ------------------------------ #
    def get_battery_voltage(self):
        # Read GPG3 battery voltage
        voltage = round(self.gpg.volt(), 1)
        self.lbl_voltage.config(text=f"Voltage: {voltage}V")

# --------------------------- REMOTE CONTROL ------------------------------- #
    def remote_control(self, event):
        """Get keystrokes for remote control"""
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
        elif key_press == 'escape':
            self.quit()

# -------------------------- CREATE WIDGETS -------------------------------- #
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
        Excape = Exit    Exit button
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
        lbl_remote_z = Label(text="Escape: Exit")

        # Get and display battery voltage
        btn_voltage = Button(text="Voltage", command=self.get_battery_voltage)
        # Round the voltage to 1 decimal place
        voltage = round(self.gpg.volt(), 1)
        self.lbl_voltage = Label(
            text=f"Voltage: {voltage}V")

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
        self.lbl_speed.grid(row=5, column=0, sticky=W)
        btn_voltage.grid(row=5, column=1, sticky=E)
        self.lbl_voltage.grid(row=5, column=2, sticky=W)
        lbl_remote_z.grid(row=6, column=0, sticky=W)
        btn_exit.grid(row=6, column=1, sticky=E)

        # Set padding for all widgets
        for child in self.window.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # Bind all key input events to the window
        # This will capture all keystrokes for remote control of robot
        self.window.bind_all('<Key>', self.remote_control)

# --------------------------- QUIT PROGRAM --------------------------------- #
    def quit(self):
        """Deconfigure the sensors, disable the motors,
        restore the LED to the control of the GoPiGo3 firmware."""
        self.gpg.reset_all()
        self.window.destroy()


# Create remote control object
gopigo_gui = GoPiGoGUI()
