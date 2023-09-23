#!/usr/bin/env python3
"""
    Name: video_stream_tkinter.py
    Author: 
    Created: 09/08/22
    Purpose: Stream video to a Tkinter interface
    Rotate image 90 degrees as camera is sideways on MARS Rover
    Enable legacy camera support for now as opencv doesn't work with Bullseye libcamera stack
"""
# Raspberry Pi/Linux
# sudo pip3 install opencv-python
# sudo pip3 install pillow -U
# sudo apt-get install libatlas-base-dev
# sudo pip3 install numpy -U

# Windows
# sudo pip3 install opencv-python
# sudo pip3 install pillow -U
# sudo pip3 install numpy -U
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
from PIL import Image
from PIL import ImageTk
import cv2
# For image file time stamp
import time


class VideoStar():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Video Star OpenCV")
        # Set the window size and location
        # horizontal vertical pixels in size, location at 50x50
        self.root.geometry("+400+50")
        # Call self.quit when window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        # Create numpy array to hold image data from cv2
        # uint8: 8-bit unsigned integer max value: 255
        # size is [height, width, 3]
        self.frame = np.random.randint(
            low=0, high=255, size=[640, 480, 3], dtype='uint8'
        )
        # Create img from numpy array
        self.img = ImageTk.PhotoImage(Image.fromarray(self.frame))
        self.create_widgets()
        # Start video capture on startup
        self.start_capture()
        self.root.mainloop()

# ------------------ STOP VIDEO CAPTURE -----------------------------------#
    def stop_capture(self):
        """Stop video capture"""
        # Release the camera capture object
        if self.cam.isOpened():
            self.cam.release()
        self.lbl_status_bar.configure(text=" Video Capture Stopped")

# ------------------ START VIDEO CAPTURE ----------------------------------#
    def start_capture(self):
        """Start video capture"""
        self.lbl_status_bar.configure(text=" Video Capture Starting Up . . .")
        self.lbl_status_bar.update()
        # Create VideoCapture object 0 = 1st camera
        self.cam = cv2.VideoCapture(0)
        self.lbl_status_bar.configure(text=" Video Capture Running . . .")
        try:
            while True:
                # Read camera image frame by frame
                # ret: Is a frame available True
                # frame: captured image
                ret, self.frame = self.cam.read()
                # Convert cv2 colorspace BGR to RGB
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                # Rotate image 90 degrees as camera is sideways on MARS Rover
                # self.frame = cv2.rotate(self.frame, cv2.ROTATE_90_CLOCKWISE)
                # PIL Image.fromarray creates image from numpy array self.frame
                # ImageTk.PhotoImage converts image to Tkinter image format
                img_update = ImageTk.PhotoImage(Image.fromarray(self.frame))
                # Set label image to new image
                self.lbl_image.configure(image=img_update)
                self.lbl_image.image = img_update
                # Update the label to display the new image
                self.lbl_image.update()
                # self.display_fps()
                if not ret:
                    print("Failed to grab frame")
                    break

        except Exception as e:
            pass
            # print(f"{e}")

# ---------------------- TAKE SNAPSHOT ------------------------------------#
    def snapshot(self):
        """Get and write a single video frame to a jpg image"""
        # Get a frame from the video source
        ret, frame = self.get_frame()
        if ret == True:
            # Write video frame to jpg image
            cv2.imwrite(
                "frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") +
                ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

# ---------------------- GET FRAME ----------------------------------------#
    def get_frame(self):
        """Get single frame from video stream"""
        # Set ret variable to false in case the camera is not open
        ret = False
        if self.cam.isOpened():
            ret, frame = self.cam.read()
            if ret:
                # Return a boolean success flag
                # and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            self.lbl_status_bar.configure(
                text=" Video Capture must be started to capture a snapshot"
            )
            return (ret, None)

# ------------------ CREATE WIDGETS ---------------------------------------#
    def create_widgets(self):
        """Create widgets"""
        # Create zero size image to resize label by pixels
        img = tk.PhotoImage()
        # Label to display video stream with zero size pixel
        self.lbl_image = tk.Label(self.root, image=img, width=640, height=480)

        message = f" OpenCV Video Stream"
        self.lbl_status_bar = tk.Label(
            self.root, text=message, anchor=tk.W, relief=tk.RIDGE)

        BUTTON_WIDTH = 16
        btn_start_capture = ttk.Button(
            self.root, text="Start Capture",
            command=self.start_capture, width=BUTTON_WIDTH)
        btn_stop_capture = ttk.Button(
            self.root, text="Stop Capture",
            command=self.stop_capture, width=16)
        btn_snapshot = ttk.Button(
            self.root, text="Snapshot",
            command=self.snapshot, width=BUTTON_WIDTH
        )
        btn_quit = ttk.Button(
            self.root, text="Quit", command=self.quit, width=BUTTON_WIDTH)

        self.lbl_image.grid(row=0, column=0, columnspan=4)

        btn_start_capture.grid(row=1, column=0)
        btn_stop_capture.grid(row=1, column=1)
        btn_snapshot.grid(row=1, column=2)
        btn_quit.grid(row=1, column=3)

        self.lbl_status_bar.grid(row=2, column=0, columnspan=4, sticky="WE")

        # Set padding for all widgets
        for child in self.root.winfo_children():
            child.grid_configure(padx=6, pady=6, ipadx=1, ipady=1)

# ------------------ DISPLAY FPS ------------------------------------------#
    def display_fps(self):
        """Get and display FPS"""
        # Get frames per second from cam capture properties
        self.fps = self.cam.get(cv2.CAP_PROP_FPS)
        message = f"FPS: {self.fps}"
        self.lbl_status_bar.configure(text=message)
        self.lbl_status_bar.update()

# ------------------ QUIT -------------------------------------------------#
    def quit(self):
        try:
            # If cam is in use, release it
            if self.cam.isOpened():
                self.cam.release()
        except:
            pass
        self.root.destroy()


video_star = VideoStar()
