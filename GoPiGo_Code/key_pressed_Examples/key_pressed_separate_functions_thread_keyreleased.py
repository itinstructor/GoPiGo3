import tkinter as tk
import gopigo3
import threading

# Initialize the GoPiGo3 robot
gpg = gopigo3.GoPiGo3()

# Event to control the robot thread
stop_event = threading.Event()


# Function to move the robot forward
def move_forward():
    while not stop_event.is_set():
        gpg.forward()


# Function to move the robot backward
def move_backward():
    while not stop_event.is_set():
        gpg.backward()


# Function to turn the robot left
def turn_left():
    while not stop_event.is_set():
        gpg.left()


# Function to turn the robot right
def turn_right():
    while not stop_event.is_set():
        gpg.right()


# Function to stop the robot
def stop_robot():
    stop_event.set()
    gpg.stop()


# Create the main tkinter window
root = tk.Tk()
root.title("GoPiGo Remote Control")

# Bind keypress events to start robot movement
root.bind('w', lambda event: threading.Thread(target=move_forward).start())
root.bind('s', lambda event: threading.Thread(target=move_backward).start())
root.bind('a', lambda event: threading.Thread(target=turn_left).start())
root.bind('d', lambda event: threading.Thread(target=turn_right).start())

# Bind keyrelease events to stop the robot
root.bind('w', lambda event: stop_robot(), '<KeyRelease-w>')
root.bind('s', lambda event: stop_robot(), '<KeyRelease-s>')
root.bind('a', lambda event: stop_robot(), '<KeyRelease-a>')
root.bind('d', lambda event: stop_robot(), '<KeyRelease-d>')

# Start the tkinter main loop
root.mainloop()
