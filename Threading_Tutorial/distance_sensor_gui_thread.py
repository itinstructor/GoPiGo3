#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import tkinter as tk  # Import the Tkinter library for creating the GUI
from tkinter import ttk  # Import the themed Tkinter widgets
# Import the EasyGoPiGo3 library for interacting with the distance sensor
import easygopigo3 as easy
import threading  # Import the threading library for creating a separate thread
import time  # Import the time library for adding delays in the thread


class DistanceSensorTkinter:
    def __init__(self, root):
        # Initialize the class with the main Tkinter window (master)
        self.root = root
        # Set the title of the main window
        root.title("Distance Sensor Test")

        # Initialize the EasyGoPiGo3 object and the distance sensor
        self.gpg = easy.EasyGoPiGo3()
        self.distance_sensor = self.gpg.init_distance_sensor("AD1")
        self.initialize_thread()
        self.create_widgets()

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

        # Create a button to update the distance (not used in this version)
        self.update_button = ttk.Button(
            self.main_frame, text="Update Distance", command=self.update_distance)
        # Pack the update button with vertical padding
        self.update_button.pack(pady=10)

        # Create a button to quit the application
        self.quit_button = ttk.Button(
            self.main_frame, text="Quit", command=self.quit)
        # Pack the quit button with vertical padding
        self.quit_button.pack(pady=10)

# ----------------------- INITIALIZE THREAD ------------------------------ #
    def initialize_thread(self):
        # Initialize the running flag and start the update thread
        # Setting daemon=True allows the thread to quit
        # when the main application quits
        self.running = True
        self.update_thread = threading.Thread(
            target=self.update_distance_thread,
            daemon=True
        )
        self.update_thread.start()  # Start the update thread

# ----------------------- UPDATE DISTANCE THREAD ------------------------- #
    def update_distance_thread(self):
        # This method runs in a separate thread and continuously updates the distance
        while self.running:
            # Read the distance from the sensor and calculate the feet and inches
            inches = self.distance_sensor.read_inches()
            feet = int(inches // 12)
            remaining_inches = int(inches % 12)

            # Format the distance text and update the label
            distance_text = f"{feet}' {remaining_inches}\""
            self.distance_label.configure(text=distance_text)

            # Pause for 1 second before the next update
            time.sleep(1)

# -------------------------- UPDATE DISTANCE ----------------------------- #
    def update_distance(self):
        # This method is called when the "Update Distance" button is clicked
        # However, it doesn't do anything, as the distance is already being updated in the separate thread
        pass

# -------------------------- QUIT APPLICATION ---------------------------- #
    def quit(self):
        # This method is called when the "Quit" button is clicked
        # It sets the running flag to False to stop the update thread
        # and then waits for the thread to join before quitting the application
        self.running = False
        self.update_thread.join()
        self.root.quit()


# Create the main Tkinter window and the DistanceSensorTkinter application
root = tk.Tk()
app = DistanceSensorTkinter(root)
root.mainloop()  # Start the main event loop to display the application
