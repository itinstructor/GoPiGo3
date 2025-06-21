#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
    Name:    obstacle_scanner.py
    Author:  William A Loring
    Created: 11/17/2024 Revised:
    Purpose: Scan the area in front of the GoPiGo3 with the distance sensor
    Display objects on a radar display
    Code helper: Claude.ai
"""
import tkinter as tk
from tkinter import ttk, filedialog
from easygopigo3 import EasyGoPiGo3
import math
import time
from threading import Thread
import configparser
import os
from PIL import ImageGrab


class ObstacleScanner(tk.Tk):
    def __init__(self):
        super().__init__()
        # Configure the window
        self.title("GoPiGo3 Obstacle Scanner")
        self.geometry("860x750+20+40")

        # Initialize GoPiGo3 components
        self.gpg = EasyGoPiGo3()
        self.distance_sensor = self.gpg.init_distance_sensor("AD1")
        self.servo2 = self.gpg.init_servo("SERVO2")

        # Load configuration
        self.config = configparser.ConfigParser()
        self.config_file = 'obstacle_scanner_config.ini'
        self.load_config()

        # Scanner settings
        self.scanning = False
        self.scan_data = {}
        # Maximum distance to display (in cm)
        self.max_distance = 300

        # Create canvas for visualization
        self.canvas = tk.Canvas(self, width=860, height=600, bg='black')
        self.canvas.grid(row=0, column=0, pady=10, padx=10)

        # Create all control panels at the bottom
        self.create_bottom_controls()

        # Initialize the display
        self.draw_radar_background()

# ---------------------- DRAW RADAR BACKGROUND --------------------------- #
    def draw_radar_background(self):
        """Draw the radar background with distance circles and angle lines"""
        # Clear any existing "background" elements on the canvas.
        self.canvas.delete("background")

        # Define the radar's center point.
        center_x = 430
        center_y = 550

        # Draw concentric circles to represent distance from the center.
        # Increment by 50 cm.
        for distance in range(50, self.max_distance + 1, 50):
            radius = distance * 1.6  # Scale the radius for better visibility.

            # Draw the circle outline at the calculated radius.
            self.canvas.create_oval(
                # Top-left corner of bounding box.
                center_x - radius, center_y - radius,
                # Bottom-right corner of bounding box.
                center_x + radius, center_y + radius,
                outline='darkgreen',  # Green color for the circle outline.
                tags="background"  # Tag for identifying these elements later.
            )

            # Add a distance label above the circle.
            self.canvas.create_text(
                # Position directly above the circle.
                center_x, center_y - radius,
                text=f"{distance}cm",  # Display distance in centimeters.
                fill='darkgreen',  # Match the color of the circle outline.
                tags="background"  # Tag for easy reference.
            )

        # Draw angle lines extending outward from the radar's center.
        # Angle range is determined by self.right_limit and self.left_limit.
        # Increment by 20°.
        for angle in range(self.right_limit, self.left_limit + 1, 20):
            # Convert angle to radians for trigonometric calculations.
            rad = math.radians(angle)
            line_length = self.max_distance * 1.6  # Scale the line length.

            # Calculate display angle by offsetting based on
            # center position and orientation.
            display_angle = angle - self.center_pos + 90

            # Calculate the endpoint of the angle line.
            x = center_x + line_length * \
                math.cos(math.radians(180 - display_angle))
            y = center_y - line_length * \
                math.sin(math.radians(180 - display_angle))

            # Draw the angle line.
            self.canvas.create_line(
                center_x, center_y,  # Start at the radar's center.
                x, y,  # End at the calculated point.
                fill='darkgreen',  # Green color for the line.
                tags="background"  # Tag for grouping.
            )

            # Calculate the position for the angle label.
            label_x = center_x + (line_length + 20) * \
                math.cos(math.radians(display_angle))
            label_y = center_y - (line_length + 20) * \
                math.sin(math.radians(display_angle))

            # Add the angle label at the calculated position.
            self.canvas.create_text(
                # Position slightly beyond the line's endpoint.
                label_x, label_y,
                text=f"{angle}°",  # Display the angle in degrees.
                fill='darkgreen',  # Match the color of the line.
                tags="background"  # Tag for grouping.
            )

# --------------------------- PLOT POINT --------------------------------- #
    def plot_point(self, angle, distance):
        """Plot a point on the radar display"""
        if distance > self.max_distance:
            distance = self.max_distance

        # Define radar's center point
        center_x = 430
        center_y = 550

        radius = distance * 1.6

        display_angle = angle - self.center_pos + 90
        x = center_x + radius * math.cos(math.radians(display_angle))
        y = center_y - radius * math.sin(math.radians(display_angle))

        point_size = 5
        self.canvas.create_oval(
            x - point_size, y - point_size,
            x + point_size, y + point_size,
            fill='red', outline='red',
            tags="scan_point"
        )

        # Uncomment for debugging
        self.lbl_plot_points.configure(
            text=f"Distance: {distance}cm Angle: {angle}°")

# ------------------------ CALCULATE SCAN RANGE -------------------------- #
    def calculate_scan_range(self):
        """Calculate left and right scan limits based on center position"""
        # Total scan range 120 / 2
        range_half = 60
        self.left_limit = min(180, self.center_pos + range_half)
        self.right_limit = max(0, self.center_pos - range_half)

# ---------------------- UPDATE CENTER POSITION -------------------------- #
    def update_center_position(self):
        """Update the center position and recalculate scan range"""
        try:
            new_center = int(self.center_spinbox.get())
            if 0 <= new_center <= 180:
                self.center_pos = new_center
                self.config.set('Servo', 'center_position',
                                str(self.center_pos))
                self.save_config()
                self.calculate_scan_range()
                self.range_label.config(
                    text=f"Range: {self.left_limit}° (L) to {self.right_limit}° (R)")
                self.draw_radar_background()
        except ValueError:
            self.center_spinbox.set(self.center_pos)

    def test_center_position(self):
        """Move servo to center position for testing"""
        self.servo2.rotate_servo(self.center_pos)
        time.sleep(1)

# ----------------------- UPDATE RESOLUTION ------------------------------ #
    def update_resolution(self):
        """Update the scan resolution"""
        try:
            new_resolution = int(self.resolution_spinbox.get())
            if 1 <= new_resolution <= 10:
                self.scan_resolution = new_resolution
                self.config.set('Servo', 'scan_resolution',
                                str(self.scan_resolution))
                self.save_config()
        except ValueError:
            self.resolution_spinbox.set(self.scan_resolution)

# ----------------------------- SCAN ------------------------------------- #
    def scan(self):
        """Perform the scanning operation"""
        while self.scanning:
            # Scan from left to right
            for angle in range(self.left_limit, self.right_limit - 1, -self.scan_resolution):
                if not self.scanning:
                    break
                self.servo2.rotate_servo(angle)
                time.sleep(0.1)
                distance = self.distance_sensor.read_mm() / 10
                self.scan_data[angle] = distance
                self.plot_point(angle, distance)

            # Scan from right to left
            for angle in range(self.right_limit, self.left_limit + 1, self.scan_resolution):
                if not self.scanning:
                    break
                self.servo2.rotate_servo(angle)
                time.sleep(0.1)
                distance = self.distance_sensor.read_mm() / 10
                self.scan_data[angle] = distance
                self.plot_point(angle, distance)

# -------------------------- TOGGLE SCAN --------------------------------- #
    def toggle_scan(self):
        """Start or stop the scanning process"""
        if not self.scanning:
            self.scanning = True
            self.start_button.config(text="Stop Scan")
            self.scan_thread = Thread(target=self.scan)
            self.scan_thread.daemon = True
            self.scan_thread.start()
        else:
            self.scanning = False
            self.start_button.config(text="Start Scan")

# --------------------------- CLEAR SCAN --------------------------------- #
    def clear_scan(self):
        """Clear all scan points from the display"""
        self.canvas.delete("scan_point")
        self.scan_data = {}

# -------------------------- LOAD CONFIG --------------------------------- #
    def load_config(self):
        """Load configuration from file or create with defaults"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)

        if not self.config.has_section('Servo'):
            self.config.add_section('Servo')
            self.config.set('Servo', 'center_position', '90')
            self.config.set('Servo', 'scan_resolution', '2')
            self.save_config()

        self.center_pos = self.config.getint('Servo', 'center_position')
        self.servo2.rotate_servo(self.center_pos)
        self.scan_resolution = self.config.getint('Servo', 'scan_resolution')
        self.calculate_scan_range()

# -------------------------- SAVE CONFIG --------------------------------- #
    def save_config(self):
        """Save current configuration to file"""
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

# --------------------------- SAVE SCAN ---------------------------------- #
    def save_scan(self):
        """Save the current scan view as a PNG file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Save Scan As"
        )
        if file_path:
            # Get canvas coordinates
            x = self.canvas.winfo_rootx()
            y = self.canvas.winfo_rooty()
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()

            # Capture the canvas area
            screenshot = ImageGrab.grab(bbox=(x, y, x+width, y+height))
            screenshot.save(file_path)

# -------------------- CREATE BOTTOM CONTROLS ---------------------------- #
    def create_bottom_controls(self):
        """Create all controls at the bottom of the window using Grid layout manager"""
        # Create a container frame for the bottom controls
        bottom_frame = ttk.Frame(self, relief=tk.RIDGE)
        bottom_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        # Configure grid columns to expand properly
        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)
        bottom_frame.columnconfigure(2, weight=1)

        # Create labeled frames for each group of controls
        config_frame = ttk.LabelFrame(
            bottom_frame, text="Scanner Configuration")
        config_frame.grid(row=0, column=0, padx=5, rowspan=2, sticky="nsew")

        scan_frame = ttk.LabelFrame(bottom_frame, text="Scan Controls")
        scan_frame.grid(row=0, column=1, padx=5, sticky="nsew")

        save_frame = ttk.LabelFrame(bottom_frame, text="Save Controls")
        save_frame.grid(row=0, column=2, padx=5, sticky="nsew")

        display_frame = ttk.Frame(bottom_frame)
        display_frame.grid(row=1, column=1, columnspan=2,
                           padx=5, sticky="nsew")

        # Configuration Controls
        # Center Position Control
        center_frame = ttk.Frame(config_frame)
        center_frame.grid(row=0, column=0, pady=2, sticky="w")

        ttk.Label(center_frame, text="Center:").grid(
            row=0, column=0, padx=2, sticky="w")
        self.center_spinbox = ttk.Spinbox(
            center_frame,
            from_=0,
            to=180,
            width=5,
            command=self.update_center_position
        )
        self.center_spinbox.set(self.center_pos)
        self.center_spinbox.grid(row=0, column=1, padx=2)

        ttk.Button(
            center_frame,
            text="Test",
            command=self.test_center_position
        ).grid(row=0, column=2, padx=2)

        # Resolution Control
        res_frame = ttk.Frame(config_frame)
        res_frame.grid(row=1, column=0, pady=2, sticky="w")

        ttk.Label(res_frame, text="Resolution:").grid(
            row=0, column=0, padx=2, sticky="w")
        self.resolution_spinbox = ttk.Spinbox(
            res_frame,
            from_=1,
            to=10,
            width=5,
            command=self.update_resolution
        )
        self.resolution_spinbox.set(self.scan_resolution)
        self.resolution_spinbox.grid(row=0, column=1, padx=2)

        # Range Display
        self.range_label = ttk.Label(
            config_frame,
            text=f"Range: {self.right_limit}° (L) to {self.left_limit}° (R)"
        )
        self.range_label.grid(row=2, column=0, pady=2, sticky="w")

        # Scan Controls
        self.start_button = ttk.Button(scan_frame, text="Start Scan",
                                       command=self.toggle_scan)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.clear_button = ttk.Button(scan_frame, text="Clear",
                                       command=self.clear_scan)
        self.clear_button.grid(row=0, column=1, padx=5, pady=5)

        # Save Controls
        self.save_button = ttk.Button(save_frame, text="Save as PNG",
                                      command=self.save_scan)
        self.save_button.grid(row=0, column=0, padx=5, pady=5)

        self.btn_quit = ttk.Button(
            save_frame, text="Quit", command=self.on_closing)
        self.btn_quit.grid(row=0, column=1, padx=5, pady=5)

        # Display plot points label
        self.lbl_plot_points = ttk.Label(display_frame)
        self.lbl_plot_points.grid(row=0, column=2, padx=5, pady=5)

# -------------------------- ON CLOSING ---------------------------------- #
    def on_closing(self):
        """Clean up when the window is closed"""
        self.servo2.rotate_servo(self.center_pos)
        self.scanning = False
        self.servo2.reset_servo()
        self.destroy()


if __name__ == "__main__":
    app = ObstacleScanner()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
