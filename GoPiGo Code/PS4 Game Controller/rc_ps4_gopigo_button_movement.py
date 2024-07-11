"""
    Name: ps4_test.py
    Author: William A Loring
    Created: 06/17/24
    Purpose: Test the PS4 Gamepad
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

        # Call the base class constructor to handle common initialization logic
        super().__init__(**kwargs)

        # Create EasyGoPiGo3 object
        self.gpg = easy.EasyGoPiGo3()
        # Set initial speed
        self.gpg.set_speed(200)

    # Define a callback function that executes when the X button is pressed
    def on_x_press(self):
        print("Hello world! The X button has been pressed.")
        self.gpg.forward()

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
