#!/usr/bin/env python3
"""
    Name: video_star_2.py
    Author: 
    Created: 08/01/23
    Purpose: Stream video to a Tkinter interface using opencv
"""
# Raspberry Pi Buster
# sudo pip3 install pillow -U
# sudo apt install libatlas-base-dev -y
# sudo apt install libopenblas-dev -y
# sudo pip3 install numpy -U
# sudo pip3 install opencv-python==4.3.0.38 # 
# Edit /boot/config.txt comment out auto_detect_camera=1,
# add gpu_mem=128 and start_x=1

# Windows
# sudo pip3 install opencv-python
# sudo pip3 install pillow -U
# sudo pip3 install numpy -U

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
from PIL import Image
from PIL import ImageTk
import cv2
# Save and load configuration
import configparser
import os
# For image file time stamp
import time


class VideoStar():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Video Star OpenCV")
        # Set window location at
        # 600x50 for pi, 350x50 for pi zero
        self.root.geometry("+600+50")

        # Call self.quit when window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        # Create VideoCapture object 0 = 1st camera
        self.camera = cv2.VideoCapture(0)

        # Start streaming flag to false
        self.is_streaming = False
        self.rotation = 0

        # Calculate frame count
        self.frame_count = 0
        self.start_time = 0

        # Load settings from settings.ini file
        self.load_settings()

        self.create_widgets()
        self.root.mainloop()

# ----------------------- START STOP VIDEO STREAM -------------------------#
    def start_stop_stream(self):
        """Stop or start the video stream"""
        if not self.is_streaming:
            self.start_stream()
        else:
            self.stop_stream()

# ------------------------ STOP VIDEO STREAM ------------------------------#
    def stop_stream(self):
        """Stop video stream"""
        # self.streaming set to false stops the update_stream method
        self.is_streaming = False
        self.btn_start_stop.configure(text="Start Stream")
        self.lbl_status_bar.configure(text=" Video Stream Stopped")

# ----------------------- START VIDEO CAPTURE -----------------------------#
    def start_stream(self):
        """Start video stream"""
        self.is_streaming = True

        # Initialize frame count to 0 when stream starts
        self.frame_count = 0
        # Store the start time
        self.start_time = time.time()

        self.lbl_status_bar.configure(text=" Video Stream Running . . .")
        self.btn_start_stop.configure(text="Stop Stream")

        # Start update stream after thread every 10 seconds
        # This will keep going until is_streaming is set to False
        self.update_stream()

# ------------------------ UPDATE STREAM ----------------------------------#
    def update_stream(self):
        """Update the video stream by reading camera frames"""
        # Check if streaming is enabled
        if self.is_streaming == True:
            # Read a frame from the camera
            # ret: Indicates if a frame is available, frame: Captured image
            ret, frame = self.camera.read()
            if ret:
                # Convert the frame from BGR to RGB color space
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Create an Image object from the frame
                image = Image.fromarray(frame)

                # Rotate the image if the rotation angle is not zero
                if self.rotation != 0:
                    image = image.rotate(self.rotation)

                # Create a PhotoImage object from the Image
                photo = ImageTk.PhotoImage(image=image)

                # Create an image on the canvas at the specified coordinates
                self.canvas.create_image(
                    0,            # x-coordinate for the image's top-left corner
                    0,            # y-coordinate for the image's top-left corner
                    # Anchor image at top-left corner (North-West)
                    anchor=tk.NW,
                    image=photo   # Image to be displayed
                )

                # Store the PhotoImage to update the stream
                self.stream = photo

                # Add a frame to the frame count
                self.frame_count += 1

                # Display the frames per second information
                self.display_fps()

            else:
                # Display an error message if failed to grab a frame
                self.lbl_status_bar.configure(text=" Failed to grab frame")
                # Uncomment the following line to convert the frame from BGR to RGB
                # self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        # Schedule the function to update the stream every 10 milliseconds
        # when the main program isn't busy
        self.root.after(10, self.update_stream)

# ---------------------- CAPTURE IMAGE ------------------------------------#
    def capture_image(self):
        """Capture and save a single video frame as a jpg image"""
        # Get a frame from the video source
        ret, frame = self.camera.read()

        # Check if a frame is successfully retrieved
        if ret == True:
            # Convert frame color format from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Create an Image object from the frame
            image = Image.fromarray(frame)

            # Check if rotation angle is not zero, rotate the image
            if self.rotation != 0:
                image = image.rotate(self.rotation)

            # Generate a filename with the current date and time
            filename = f"capture_{time.strftime('%Y-%m-%d_%H-%M-%S')}.jpg"

            # Save the image with the generated filename
            image.save(filename)

            # Print a message confirming the image is saved with its filename
            mb.showinfo("Image Saved", f"Image saved as {filename}")

# --------------------------- ROTATE IMAGE --------------------------------#
    def rotate_image(self):
        """Rotate the incoming camera image"""
        self.rotation += 90
        if self.rotation >= 360:
            self.rotation = 0
        self.save_settings()

# --------------------------- SAVE SETTINGS -------------------------------#
    def save_settings(self):
        """Save program settings for RotationAngle"""
        # Create a ConfigParser object to handle configuration file
        config = configparser.ConfigParser()
        
        # Define the 'Settings' section
        # set 'RotationAngle' key with the value as a string
        config["Settings"] = {"RotationAngle": str(self.rotation)}

        # Open the settings.ini file in write mode
        with open("settings.ini", "w") as configfile:
            # Write the configuration data into the settings.ini file
            config.write(configfile)

# --------------------------- LOAD SETTINGS -------------------------------#
    def load_settings(self):
        """Load program settings for RotationAngle"""
        # Check if the settings file exists
        if os.path.exists("settings.ini"):
            # Create a ConfigParser object to handle configuration file
            config = configparser.ConfigParser()

            # Read the content of the settings file
            config.read("settings.ini")

            # Check if the 'Settings' section exists in the configuration
            if "Settings" in config:
                # Get the 'RotationAngle' value from the 'Settings' section
                rotation_angle = config['Settings'].get("RotationAngle", "0")
                
                # Convert the obtained value to an integer
                # and assign it to self.rotation_angle
                self.rotation = int(rotation_angle)

# --------------------------- DISPLAY FPS ---------------------------------#
    def display_fps(self):
        """Get and display FPS"""
        # Get frames per second from cam capture properties
        # self.fps = self.camera.get(cv2.CAP_PROP_FPS)

        # Calculate the elapsed time since the start
        elapsed_time = time.time() - self.start_time

        # Ensure elapsed time is greater than 0 to avoid division by zero
        if elapsed_time > 0:
            # Calculate frames per second (FPS)
            fps = self.frame_count / elapsed_time

            # Create a message string to display the FPS with 2 decimal places
            message = f"FPS: {fps:.2f}"

            # Update the status bar label with the FPS message
            self.lbl_status_bar.configure(text=message)

            # Refresh the status bar to reflect the updated message
            self.lbl_status_bar.update()

# ------------------ CREATE WIDGETS ---------------------------------------#
    def create_widgets(self):
        """Create widgets"""
        # Constant to have all the buttons the same width
        BUTTON_WIDTH = 16

        # Create canvas to size and display image
        self.canvas = tk.Canvas(
            self.root,
            width=640,
            height=480
        )

        self.btn_start_stop = ttk.Button(
            self.root,
            text="Start Stream",
            command=self.start_stop_stream,
            width=BUTTON_WIDTH
        )

        self.btn_rotate = ttk.Button(
            self.root,
            text="Rotate",
            command=self.rotate_image,
            width=BUTTON_WIDTH
        )
        self.btn_snapshot = ttk.Button(
            self.root,
            text="Capture Image",
            command=self.capture_image,
            width=BUTTON_WIDTH
        )
        self.btn_quit = ttk.Button(
            self.root,
            text="Quit",
            command=self.quit, width=BUTTON_WIDTH
        )

        message = f" OpenCV Video Stream"
        self.lbl_status_bar = tk.Label(
            self.root, text=message, anchor=tk.W, relief=tk.RIDGE
        )

        self.canvas.grid(row=0, column=0, columnspan=4)

        self.btn_start_stop.grid(row=1, column=0)
        self.btn_rotate.grid(row=1, column=1)
        self.btn_snapshot.grid(row=1, column=2)
        self.btn_quit.grid(row=1, column=3)

        self.lbl_status_bar.grid(row=2, column=0, columnspan=4, sticky="WE")

        # Set padding for all widgets
        for child in self.root.winfo_children():
            child.grid_configure(padx=6, pady=6, ipadx=1, ipady=1)

        # The Escape key will activate the quit method
        self.root.bind('<Escape>', self.quit)

        # Handle window closing clean up cv2  camera resources
        self.root.protocol("WM_DELETE_WINDOW", quit)

# --------------------------- QUIT PROGRAM --------------------------------#
    def quit(self, *args):
        """Close clean up cv2 cameraresources, close the program"""
        try:
            # If cam is in use, release it
            if self.camera.isOpened():
                self.camera.release()
        except:
            pass
        # Closes the window and exit the Tkinter main loop
        self.root.destroy()


video_star = VideoStar()
