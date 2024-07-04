"""
    Name: ps4_gopigo.py
    Author: William A Loring
    Created: 07/03/24
    Purpose: PS4 gamecontroller on the GoPiGo
    https://github.com/ArturSpirin/pyPS4Controller
"""
# sudo pip3 install pyps4controller
# Import the Controller class from the pyPS4Controller library
from pyPS4Controller.controller import Controller

# Import EasyGoPiGo3 library
import easygopigo3 as easy


class MyController(Controller):
    """Custom controller class that inherits from the base Controller class"""

    def __init__(self, **kwargs):
        """Initialize the controller object using arguments
           passed to the constructor"""

        # Call base class constructor to handle common initialization logic
        super().__init__(**kwargs)

        # Create EasyGoPiGo3 object
        self.gpg = easy.EasyGoPiGo3()
        # Set initial speed
        self.speed = 0

# --------------------- FORWARD JOYSTICK --------------------------------- #
    # Event handler for moving the left joystick down
    def on_L3_down(self, value):

        self.speed = self.normalize_joystick_value(value)
        print(f"Down Speed: {self.speed}")

        self.gpg.set_speed(self.speed)
        self.gpg.backward()

# --------------------- REVERSE JOYSTICK --------------------------------- #
    # Event handler for moving the left joystick up
    def on_L3_up(self, value):

        self.speed = self.normalize_joystick_value(value)
        print(f"Up Speed: {self.speed}")

        self.gpg.set_speed(self.speed)
        self.gpg.forward()

# --------------------- NORMALIZE JOYSTICK ------------------------------- #
    def normalize_joystick_value(self, joystick_value):
        # Maximum speed for motor 0 to 550
        # The joystick value (value) ranges from -32767 to 32767
        # Normalize this to a range from 0 to 550
        min_joystick = 0
        max_joystick = 32767
        min_power = 0
        max_power = 550

        normalized_value = (
            (
                joystick_value - min_joystick
            ) * (
                max_power - min_power
            )
        ) / (
            max_joystick - min_joystick
        ) + min_power

        return abs(int(normalized_value))

    def on_L3_x_at_rest(self):
        self.gpg.stop()

    def on_L3_y_at_rest(self):
        self.gpg.stop()

    # Event handler for moving the left joystick left
    def on_L3_left(self, value):
        pass

    # Event handler for moving the left joystick right
    def on_L3_right(self, value):
        pass

    # Define a callback function that executes when the X button is pressed
    def on_x_press(self):
        print("Hello world! The X button has been pressed.")
        self.gpg.stop()

    # Define a callback function that executes when the X button is released
    def on_x_release(self):
        print("Goodbye world! The X button has been released.")
        self.gpg.stop()


# Create an instance of the MyController class, specifying the
# connection interface and disabling the use of ds4drv (if applicable)
controller = MyController(
    interface="/dev/input/js0",
    connecting_using_ds4drv=False
)

# Start listening for controller events with a timeout of 60 seconds
# (the controller should be paired within this timeframe)
controller.listen(timeout=60)
