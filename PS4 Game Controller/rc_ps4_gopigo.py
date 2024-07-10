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

        # Set min and max values for joystick
        self.min_joystick = 0
        self.max_joystick = 32767
        # Set min and max values for power
        self.min_power = 0
        self.max_power = 550

        # Calculate the range of power and joystick values
        self.range_power = self.max_power - self.min_power
        self.range_joystick = self.max_joystick - self.min_joystick

        # Power for turning
        self.turn_speed = 200
        # Left right spin() joystick max value of 32767
        # set to higher level than 0 to smooth out turns
        self.turn_threshold = 10000

        # Create EasyGoPiGo3 object
        self.gpg = easy.EasyGoPiGo3()
        # Set initial speed
        self.speed = 0

# --------------------- FORWARD JOYSTICK --------------------------------- #
    # Event handler for moving the left joystick down
    def on_L3_down(self, value: int) -> None:
        """Set speed based on normalized value from joystick,
        move backward

        Args:
            value (int): The normalized value from the joystick.
        """
        self.speed = self.normalize_joystick_value(value)
        print(f"Down Speed: {self.speed}")

        self.gpg.set_speed(self.speed)
        self.gpg.backward()

# ------------------------ REVERSE --------------------------------------- #
    # Event handler for moving the left joystick up
    def on_L3_up(self, value: int) -> None:
        """Set speed based on normalized value from joystick,
        move forward

        Args:
            value (int): The normalized value from the joystick.
        """
        self.speed = self.normalize_joystick_value(value)
        self.gpg.set_speed(self.speed)
        self.gpg.forward()

    def on_L3_x_at_rest(self):
        """Stop GopiGo on joystick release"""
        self.gpg.stop()

    def on_L3_y_at_rest(self):
        """Stop GopiGo on joystick release"""
        self.gpg.stop()

# ---------------------- TURN LEFT --------------------------------------- #
    # Event handler for moving the left joystick left
    def on_L3_left(self, value: int) -> None:
        """If the positive value of the joystick is above the 
        turn_threshold, turn."""
        if abs(value) > self.turn_threshold:
            self.gpg.set_speed(self.turn_speed)
            self.gpg.spin_left()

# ---------------------- TURN RIGHT -------------------------------------- #
    # Event handler for moving the left joystick right
    def on_L3_right(self, value: int) -> None:
        """If the positive value of the joystick is above the 
        turn_threshold, turn."""
        if abs(value) > self.turn_threshold:
            self.gpg.spin_right()
            self.gpg.set_speed(self.turn_speed)

# --------------------- NORMALIZE JOYSTICK ------------------------------- #
    def normalize_joystick_value(self, joystick_value: int) -> int:
        """
        This function takes a joystick value (between -32767 and 32767)
        and normalizes it to a motor power value (between 0 and 550).

        Args:
            joystick_value (int): The raw joystick value from the controller.

        Returns:
            int: The normalized motor power value (0 to 550).
        """
        # Perform a linear transformation to map the joystick value
        # (-32767 to 32767) to the motor power range (0 to 550):
        # Normalize the joystick value to the range of power output values
        # Shift the joystick value to start from 0
        # Xcale it to the power range and shift it to the minimum power value
        normalized_value = (joystick_value - self.min_joystick) * \
            self.range_power / self.range_joystick + self.min_power

        # Ensure the normalized balue is a positive integer
        return abs(int(normalized_value))

# ----------------------- JOYSTICK BUTTONS ------------------------------- #
     # Define a callback function that executes when the X button is pressed
    def on_x_press(self):
        print("Hello world! The X button has been pressed.")
        self.gpg.stop()

    # Define a callback function that executes when the X button is released
    def on_x_release(self):
        print("Goodbye world! The X button has been released.")
        self.gpg.stop()


def main():
    # Create an instance of the MyController class,
    # Specify the connection interface
    # Disable the use of ds4drv (if applicable)
    controller = MyController(
        # Specify the device interface to connect to
        interface="/dev/input/js0",
        connecting_using_ds4drv=False
    )
    try:
        # Start listening for joystick input from the controller
        # This will continuously read data from the joystick until timeout occurs
        # (the controller should be paired within this timeframe)
        # Argument: Timeout in seconds (optional, defaults to None) timeout=60
        controller.listen(timeout=60)

    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C)
        # Perform cleanup operations before exiting
        controller.gpg.reset_all()
        print("\nExiting the program.")


if __name__ == "__main__":
    main()
