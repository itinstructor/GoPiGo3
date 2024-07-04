import tkinter as tk

# Constants for robot movement
STEP_SIZE = 10

# Initial robot position
robot_x = 100
robot_y = 100

# Create a function to move the robot
def move_robot(event):
    global robot_x, robot_y
    key = event.keysym

    if key == 'w':
        robot_canvas.move(robot, 0, -STEP_SIZE)
        robot_y -= STEP_SIZE
    elif key == 's':
        robot_canvas.move(robot, 0, STEP_SIZE)
        robot_y += STEP_SIZE
    elif key == 'a':
        robot_canvas.move(robot, -STEP_SIZE, 0)
        robot_x -= STEP_SIZE
    elif key == 'd':
        robot_canvas.move(robot, STEP_SIZE, 0)
        robot_x += STEP_SIZE

# Create a function to stop the robot when key is released
def stop_robot(event):
    pass  # Do nothing, just capturing the key release event

# Create a tkinter window
root = tk.Tk()
root.title("Robot Control")

# Create a canvas for the robot
robot_canvas = tk.Canvas(root, width=400, height=400)
robot_canvas.pack()

# Draw the robot as a rectangle
robot = robot_canvas.create_rectangle(
    robot_x, robot_y, robot_x + 30, robot_y + 30, fill="blue"
)

# Bind key press events to move the robot
root.bind("<KeyPress>", move_robot)
root.bind("<KeyRelease>", stop_robot)

# Set focus to the canvas so that it receives key events
robot_canvas.focus_set()

# Start the tkinter main loop
root.mainloop()
