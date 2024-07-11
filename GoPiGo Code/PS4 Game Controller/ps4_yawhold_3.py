"""
    Name: ps4_yawhold.py
    Author: William A Loring
    Created: 06/17/24
    Purpose: Raspblock remote control with the Y axis held in place
"""
from pyPS4Controller.controller import Controller
# Import Raspblock drive library
from Raspblock import Raspblock
from time import sleep
import threading

# Create an instance of the Raspblock class to control the robot
robot = Raspblock()


class MyController(Controller):
    """Define a custom controller class inheriting from the
       PS4 Controller class"""

    def __init__(self, **kwargs):
        # Initialize the Controller parent class
        super().__init__(**kwargs)

        self.Speed_axis_X = 0  # Initialize X-axis speed value
        self.Speed_axis_Y = 0  # Initialize Y-axis speed value

        self.leftrightpulse = 1500  # Initial pulse width for left-right control
        self.updownpulse = 1500  # Initial pulse width for up-down control
        self.is_up_arrow_pressed = False

        # Flag to control the running state of the update thread
        self.running = True

        # Create a daemon for continuous movement updates
        self.update_thread = threading.Thread(
            target=self.run
        )
        # Set the thread as a daemon, when program exits, the thread stops
        self.update_thread.daemon = True
        # Start the thread
        self.update_thread.start()

# ---------------------- UPDATE MOVEMENT CONTINUOUSLY -------------------- #
    def run(self):
        """ Continuously update the movement of the robot
        Run by a thread, updates the movement every .01 ms"""
        while True:
            # Call the update movement method which sets the speed
            # of x and y axis of the motors
            self.update_movement()

            if self.is_up_arrow_pressed:  # Check if button is pressed
                while self.is_up_arrow_pressed:
                    self.camUpFunction()
                    sleep(0.1)

            else:
                self.is_up_arrow_pressed = False
                # Add any cleanup code here if needed when the button is released

            # if self.up_arrow_released:  # Check if button is pressed
            #     while self.up_arrow_released:
            #         self.camDownFunction()

            # else:
            #     self.up_arrow_released = False

            # Adjust the sleep time as needed for smooth control
            sleep(0.01)

# ------------------------- UPDATE MOVEMENT ------------------------------ #
    def update_movement(self):
        """Update the robot's movement based on the current speed values"""
        # Prevent minor joystick movements from causing unintended actions
        if -2 < self.Speed_axis_X < 2:
            self.Speed_axis_X = 0
        if -2 < self.Speed_axis_Y < 2:
            self.Speed_axis_Y = 0

        # Print for debugging purposes
        # print(f"Speed_axis_X: {self.Speed_axis_X}, Speed_axis_Y: {self.Speed_axis_Y}")

        # Control the robot with the calculated speed values
        robot.Speed_axis_Yawhold_control(self.Speed_axis_X, self.Speed_axis_Y)

# --------------------- JOYSTICK CONTROL --------------------------------- #
    # Event handler for moving the left joystick up
    def on_L3_up(self, value):
        self.update_y_axis(value)

    # Event handler for moving the left joystick down
    def on_L3_down(self, value):
        self.update_y_axis(value)

    # Event handler for moving the left joystick left
    def on_L3_left(self, value):
        self.update_x_axis(value)

    # Event handler for moving the left joystick right
    def on_L3_right(self, value):
        self.update_x_axis(value)

# ------------------------ UPDATE X AXIS SPEED --------------------------- #
    def update_x_axis(self, value):
        """changed 50 to 25 to reduce the scaling factor.
        Adjusted -25 to -12 in the final calculation to maintain the 
        desired range of -25 to 25 after scaling.
        These changes should decrease the maximum speed while keeping
        the same range of values (-25 to 25) based on joystick input.
        Adjust the multiplication factor (25 in this case) as needed to 
        achieve the desired maximum speed reduction.
        """

        # Normalize joystick value (-32767 to 32767) to power level (-25 to 25)
        self.Speed_axis_X = int(25 * ((value + 32767) / 65534)) - 12

        # This is 100% power to the motors
        # Normalize joystick value (-32767 to 32767) to power level (-25 to 25)
        # self.Speed_axis_X = int(50 * ((value + 32767) / 65534)) - 25

# ------------------------ UPDATE Y AXIS SPEED --------------------------- #
    # Update the Y-axis speed based on joystick value
    def update_y_axis(self, value):
        """changed 50 to 25 to reduce the scaling factor.
        Adjusted -25 to -12 in the final calculation to maintain the 
        desired range of -25 to 25 after scaling.
        These changes should decrease the maximum speed while keeping
        the same range of values (-25 to 25) based on joystick input.
        Adjust the multiplication factor (25 in this case) as needed to 
        achieve the desired maximum speed reduction.
        """

        # Normalize joystick value (32767 to -32767) to power level (-25 to 25)
        self.Speed_axis_Y = int(25 * ((-value + 32767) / 65534)) - 12

        # This is 100% power to the motors
        # Normalize joystick value (32767 to -32767) to power level (-25 to 25)
        # self.Speed_axis_Y = int(50 * ((-value + 32767) / 65534)) - 25

# ---------------------- BUTTON CONTROL ---------------------------------- #
# Button event handlers
    def on_x_press(self):
        self.run_buzzer()
        self.camservoInitFunction()

    def on_x_release(self):
        self.stop_buzzer()

    def on_up_arrow_press(self):
        print("Up Arrow Pressed")
        self.is_up_arrow_pressed = True

    def on_up_down_arrow_release(self):
        print("Up Arrow Released")
        self.is_up_arrow_pressed = False

    def on_left_arrow_press(self):
        self.camLeftFunction()

    def on_left_right_arrow_release(self):
        print("Left Arrow Released")

    def on_right_arrow_press(self):
        self.camRightFunction()

    def on_left_right_arrow_release(self):
        pass

    def on_down_arrow_press(self):
        self.camUpFunction()

    def on_up_down_arrow_release(self):
        pass

    def run_buzzer(self):
        robot.Buzzer_control(1)

    def stop_buzzer(self):
        robot.Buzzer_control(0)

    # def camUpRepeat(self):
    #     # Function to repeatedly call camUpFunction while button is pressed
    #     while self.check_button_pressed():  # Replace with actual button check function
    #         self.camUpFunction()
    #         sleep(0.1)  # Adjust sleep time as needed to control repetition rate
    #     # Add any cleanup code here if needed when the button is released

    def camUpFunction(self):
        # Function to move the camera up
        self.updownpulse += 10  # Increase the pulse width to move up
        if self.updownpulse > 2500:  # Limit the maximum pulse width
            self.updownpulse = 2500
        # Control the servo
        robot.Servo_control(
            self.leftrightpulse,
            self.updownpulse
        )

    def camDownFunction(self):
        # Function to move the camera down
        self.updownpulse -= 10  # Decrease the pulse width to move down
        if self.updownpulse < 500:  # Limit the minimum pulse width
            self.updownpulse = 500
        # Control the servo
        robot.Servo_control(
            self.leftrightpulse,
            self.updownpulse
        )

    def camLeftFunction(self):
        self.leftrightpulse += 10  # Increase the pulse width to move left
        if self.leftrightpulse > 2500:  # Limit the maximum pulse width
            self.leftrightpulse = 2500
        robot.Servo_control(self.leftrightpulse,
                            self.updownpulse)  # Control the servo

    def camRightFunction(self):
        # Function to move the camera right
        self.leftrightpulse -= 10  # Decrease the pulse width to move right
        if self.leftrightpulse < 500:  # Limit the minimum pulse width
            self.leftrightpulse = 500
        robot.Servo_control(self.leftrightpulse,
                            self.updownpulse)  # Control the servo

    def camservoInitFunction(self):
        # Function to initialize the camera servo position
        self.leftrightpulse = 1500  # Reset left-right pulse width to initial value
        self.updownpulse = 1500  # Reset up-down pulse width to initial value
        robot.Servo_control(self.leftrightpulse,
                            self.updownpulse)  # Control the servo


# Create an instance of MyController, connecting to the correct interface
# for the joystick
controller = MyController(
    interface="/dev/input/js0",
    connecting_using_ds4drv=False
)

try:
    # Listen for events from the controller for 60 seconds
    controller.listen(timeout=60)

except KeyboardInterrupt:
    del robot
    # Handle program interruption (e.g., Ctrl+C)
    print("Program interrupted by the user")

finally:
    print("Controller stopped and program exited cleanly")
