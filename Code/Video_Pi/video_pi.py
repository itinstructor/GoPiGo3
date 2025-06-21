#!/usr/bin/env python3
"""
    Name: video_pi.py
    Purpose: Stream video to a Tkinter interface using Picamera2
    Description: This script demonstrates how to display a live video stream
    and still images from the Raspberry Pi camera using the PiCamera2 library and Tkinter.
    Raspberry Pi Buster
    sudo pip3 install pillow -U
------------------------------------------------
History
------------------------------------------------
Author     Date           Comments
Loring     03/22/25       Change stop start streamining threads to use Event object
Loring     03/21/25       Added FPS to status bar   
"""

import tkinter as tk
import tkinter.ttk as ttk
from picamera2 import Picamera2
from PIL import Image, ImageTk
from datetime import datetime
from threading import Thread, Event
from time import time, sleep

# Constants
# Frames per second (FPS) for the video stream
# Set this lower for slower Pi's
FPS = 15
FRAME_INTERVAL_MS = 1000 / FPS
# Button width for consistent UI
BUTTON_WIDTH = 16


class PiCameraApp:
    def __init__(self):
        # Create the main application window
        self.window = tk.Tk()
        self.window.geometry("+600+50")
        self.window.title("Video Pi")
        self.window.protocol("WM_DELETE_WINDOW", self.quit)

        # Initialize camera and configuration
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration())

        # Create an Event object to control start and stop of the video stream.
        # The self.stream_event is used to control whether the video stream
        # is running or stopped. When the event is "set," the stream runs;
        # when it's "cleared," the stream stops.
        self.stream_event = Event()

        self.frame_count = 0
        self.start_time = time()
        # Initialize image variable to store the captured frame
        self.image = None
        # Flag to track if the update image thread has started
        self.update_thread_started = False

        # Create GUI widgets
        self.create_widgets()

        # Start the Tkinter main loop
        self.window.mainloop()

    # ---------------------- STREAM CONTROL -------------------------------- #
    def start_stream(self):
        """Start the video stream."""
        # This checks whether the Event object (self.stream_event)
        # is currently not "set."
        # If it is "set," the video stream is already running.
        # If it's not "set," the video stream is currently stopped.
        if not self.stream_event.is_set():
            # Signal to start the video stream by setting the event flag
            # and starting the camera
            self.stream_event.set()
            self.lbl_status_bar.configure(text=" Video Stream Running . . .")
            self.btn_start_stop.configure(text="Stop Stream")
            self.picam2.start()

            # Reset frame count and start time
            self.frame_count = 0
            self.start_time = time()

            # Start threads for capturing frames and updating the canvas
            self.start_thread(self._capture_frames)
            self.start_update_image_thread()

    # ---------------------- STOP STREAM ----------------------------------- #
    def stop_stream(self):
        """Stop the video stream."""
        # Check if the video stream is currently running and stop it if it is.
        # Is the Event object (self.stream_event) is currently "set."
        if self.stream_event.is_set():
            # Stop the video stream by clearing the event flag
            # and stopping the camera
            self.stream_event.clear()
            self.lbl_status_bar.configure(text=" Video Stream Stopped")
            self.btn_start_stop.configure(text="Start Stream")
            self.picam2.stop()

            # Reset thread state
            self.update_thread_started = False
            self.frame_count = 0

    # ---------------------- START/STOP STREAM ----------------------------- #
    def start_stop_stream(self):
        """Toggle the video stream on or off."""
        if self.stream_event.is_set():
            self.stop_stream()
        else:
            self.start_stream()

    # ---------------------- THREAD MANAGEMENT ----------------------------- #
    def start_thread(self, target):
        """Start a new thread for the given target function."""
        thread = Thread(target=target)
        thread.daemon = True  # Ensure thread exits with the program
        thread.start()

    # ---------------------- UPDATE IMAGE THREAD --------------------------- #
    def start_update_image_thread(self):
        """Start the update_image method in a separate thread."""
        if not self.update_thread_started:
            self.start_thread(self.update_image)
            self.update_thread_started = True

    # ---------------------- FRAME CAPTURE --------------------------------- #
    def _capture_frames(self):
        """Continuously capture frames from the camera."""
        while self.stream_event.is_set():
            self.image = self.picam2.capture_array()
            self.frame_count += 1

            # Update FPS every second
            # Use `time` from the imported function
            elapsed_time = time() - self.start_time
            if elapsed_time >= 1.0:
                fps = self.frame_count / elapsed_time
                self.lbl_status_bar.configure(
                    text=f" Video Stream Running . . . | FPS: {fps:.2f}"
                )
                self.frame_count = 0
                self.start_time = time()

            # Pause the thread to maintain the desired frame rate
            # sleep expects seconds, convert milliseconds to seconds
            sleep(FRAME_INTERVAL_MS / 1000.0)

    # ---------------------- IMAGE UPDATING -------------------------------- #
    def update_image(self):
        """Update the Canvas widget with the latest image from the camera."""
        while self.stream_event.is_set():
            if self.image is not None:
                # Convert the frame to a Tkinter-compatible image
                image = Image.fromarray(self.image)
                image = ImageTk.PhotoImage(image)

                # Display the image on the canvas
                self.canvas.create_image(0, 0, anchor=tk.NW, image=image)

                # Prevent the image from being garbage collected
                # by keeping a reference to it
                self.photo = image

            # Pause the thread to maintain the desired frame rate
            # sleep expects seconds, convert milliseconds to seconds
            sleep(FRAME_INTERVAL_MS / 1000.0)

    # ---------------------- CAPTURE IMAGE --------------------------------- #
    def capture_image(self):
        """Capture a still image and save it to the hard drive."""
        self.stop_stream()
        # Start the image capture thread if it's not already running
        # This ensures that the image capture thread is started only once
        if not self.stream_event.is_set():
            self.start_thread(self._capture_image_thread)
        self.start_stream()

    # ---------------------- CAPTURE IMAGE THREAD -------------------------- #
    def _capture_image_thread(self):
        """Save the current frame as an image file."""
        if self.image is not None:
            # Convert the frame to a PIL image and save it
            image = Image.fromarray(self.image)

            # Convert RGBA to RGB if the image has an alpha channel
            if image.mode == 'RGBA':
                image = image.convert('RGB')

            # Save the image with a timestamped filename
            # Use datetime to create a unique filename
            filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
            image.save(filename, 'JPEG')
            print(f"Image saved as {filename}")

    # ---------------------- CREATE WIDGETS -------------------------------- #
    def create_widgets(self):
        """Create the GUI widgets."""
        # Canvas for displaying the video stream
        self.canvas = tk.Canvas(self.window, width=640, height=480)

        # Buttons for controlling the application
        self.btn_start_stop = ttk.Button(
            self.window, text="Start Stream", command=self.start_stop_stream, width=BUTTON_WIDTH
        )
        self.btn_capture_image = ttk.Button(
            self.window, text="Capture Image", command=self.capture_image, width=BUTTON_WIDTH
        )
        self.btn_quit = ttk.Button(
            self.window, text="Quit", command=self.quit, width=BUTTON_WIDTH
        )

        # Status bar for displaying messages
        self.lbl_status_bar = tk.Label(
            self.window, text=" Picamera2 Video Stream", anchor=tk.W, relief=tk.RIDGE
        )

        # Arrange widgets in a grid layout
        self.canvas.grid(row=0, column=0, columnspan=4)
        self.btn_start_stop.grid(row=1, column=0)
        self.btn_capture_image.grid(row=1, column=2)
        self.btn_quit.grid(row=1, column=3)
        self.lbl_status_bar.grid(row=2, column=0, columnspan=4, sticky="WE")

        # Add padding to all widgets
        for child in self.window.winfo_children():
            child.grid_configure(padx=6, pady=6, ipadx=1, ipady=1)

        # Bind the Escape key to quit the application
        self.window.bind('<Escape>', self.quit)

    # ---------------------- APPLICATION EXIT ------------------------------ #
    def quit(self, *args):
        """Clean up resources and exit the application."""
        self.stop_stream()
        self.window.destroy()


def main():
    """Main function to run the application."""
    PiCameraApp()


if __name__ == "__main__":
    main()
