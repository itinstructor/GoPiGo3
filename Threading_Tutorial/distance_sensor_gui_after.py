#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
    Name: distance_sensor-gui.py
"""
import tkinter as tk
from tkinter import ttk
# Import the EasyGoPiGo3 library for interacting with the distance sensor
import easygopigo3 as easy


class DistanceSensorTkinter:
    def __init__(self, root):
        # Initialize the class with the main Tkinter window (master)
        self.root = root
        # Set the title of the main window
        root.title("Distance Sensor Test")

        # Initialize the EasyGoPiGo3 object and the distance sensor
        self.gpg = easy.EasyGoPiGo3()
        self.distance_sensor = self.gpg.init_distance_sensor("AD1")
        self.create_widgets()
        # Call the update_distance method to initialize the distance display
        self.update_distance()

# -------------------------- UPDATE DISTANCE ----------------------------- #
    def update_distance(self):
        # Read the sensor data in inches or mm
        # mm = self.distance_sensor.read_mm()
        inches = self.distance_sensor.read_inches()

        # Calculate feet and inches
        # Use integer division to get the whole number of feet
        feet = inches // 12
        # Use modulus to get the remaining inches
        remaining_inches = inches % 12

        # Format the distance text and update the label
        distance_text = f"{feet:.0f}' {remaining_inches:.0f}\""
        self.distance_label.configure(text=distance_text)

        # Call this method again after 10 ms to update the distance
        # This creates a loop that updates the distance continuously
        # in the GUI window thread when it isn't busy
        self.main_frame.after(10, self.update_distance)

# -------------------------- CREATE WIDGETS ------------------------------ #
    def create_widgets(self):
        # Create the main frame to hold the widgets
        self.main_frame = ttk.Frame(self.root)
        # Pack the main frame with padding
        self.main_frame.pack(padx=20, pady=20)

        # Create a label to display the distance
        self.distance_label = ttk.Label(
            self.main_frame, text="", font=("Arial", 24))
        # Pack the distance label with vertical padding
        self.distance_label.pack(pady=10)

        # Create a button to update the distance
        self.update_button = ttk.Button(
            self.main_frame, text="Update Distance",
            command=self.update_distance)
        # Pack the update button with vertical padding
        self.update_button.pack(pady=10)

        # Create a button to quit the application
        self.quit_button = ttk.Button(
            self.main_frame, text="Quit", command=self.quit)
        # Pack the quit button with vertical padding
        self.quit_button.pack(pady=10)

# -------------------------- QUIT PROGRAM -------------------------------- #
    def quit(self):
        self.root.destroy()


# Create the main Tkinter window and the DistanceSensorTkinter object
root = tk.Tk()
app = DistanceSensorTkinter(root)
root.mainloop()  # Start the main event loop to display the application
