#!/usr/bin/env python3
"""
    Name: ps4_gopigo.py
    Author: William A Loring
    Created: 07/03/24
    Purpose: PS4 gamecontroller on the GoPiGo, no interface
    This program can be used as a program or a module 
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
        """
        Initialize the controller object using arguments
        passed to the constructor
        """
        # Call base class constructor to handle common initialization logic
        super().__init__(**kwargs)

        # Set min and max values for joystick
        # self.min_joystick = 0
        self.MIN_JOYSTICK = -32767
        self.MAX_JOYSTICK = 32767

        # Calculate the range of joystick values
        self.RANGE_JOYSTICK = self.MAX_JOYSTICK - self.MIN_JOYSTICK

        # Set min and max values for motor power
        self.min_power = 0
        self.max_power = 600

        # Calculate the range of power values
        self.RANGE_POWER = self.max_power - self.min_power

        # average_window = 5
        # self.average_window = average_window
        # self.joystick_history = deque(maxlen=average_window)

        # Power for turning
        # self.turn_speed = 300

        # Left right spin() joystick max value of 32767
        # set to higher level than 0 to smooth out turns
        self.turn_threshold = 10000

        # Create EasyGoPiGo3 object
        self.gpg = easy.EasyGoPiGo3()
        # Set initial speed
        self.speed = 0

# --------------------- NORMALIZE JOYSTICK ------------------------------- #
    def normalize_joystick_value(self, joystick_value: int) -> int:
        """
        This function takes a joystick value (between -32767 and 32767)
        and normalizes it to a motor power value (between min and max).

        Args:
            joystick_value (int): The raw joystick value from the controller.

        Returns:
            int: The normalized motor power value (min and max).
        """
        # Perform a linear transformation to map the joystick value
        # (-32767 to 32767) to the motor power range (min to max):
        # Normalize the joystick value to the range of power output values
        # Shift the joystick value to start from 0
        # Scale it to the power range and shift it to the minimum power value
        # normalized_value = (joystick_value - self.min_joystick) * \
        #     self.range_power / self.range_joystick + self.min_power

        # Subtract the minimum joystick value to normalize the input
        normalized_value = joystick_value - self.MIN_JOYSTICK

        # Scale the normalized value to the power range
        normalized_value = normalized_value * self.RANGE_POWER

        # Divide by the joystick range, using integer division
        normalized_value = normalized_value // self.RANGE_JOYSTICK

        # Add the minimum power to shift the range
        normalized_value = normalized_value + self.min_power

        # normalized_value = max(
        #     self.min_power,
        #     min(
        #         self.max_power,
        #         int(normalized_value)
        #     )
        # )
        # Ensure the normalized value is a positive integer
        return abs(normalized_value)

# --------------------- JOYSTICK FORWARD --------------------------------- #
    # Event handler for moving the left joystick down
    def on_L3_down(self, value: int) -> None:
        """
        Set speed based on normalized value from joystick,
        move backward

        Args:
            value (int): The normalized value from the joystick.
        """
        self.speed = self.normalize_joystick_value(value)
        # print(f"Down Speed: {self.speed}")

        self.gpg.set_speed(self.speed)
        self.gpg.backward()

# ------------------------ JOYSTICK REVERSE ------------------------------ #
    # Event handler for moving the left joystick up
    def on_L3_up(self, value: int) -> None:
        """
        Set speed based on normalized value from joystick,
        move forward

        Args:
            value (int): The normalized value from the joystick.
        """
        self.speed = self.normalize_joystick_value(value)
        self.gpg.set_speed(self.speed)
        self.gpg.forward()

# ------------------------ JOYSTICK STOP --------------------------------- #
    def on_L3_x_at_rest(self):
        """
        Stop GopiGo on joystick release
        """
        self.gpg.stop()

    def on_L3_y_at_rest(self):
        """
        Stop GopiGo on joystick release
        """
        self.gpg.stop()

# ---------------------- JOYSTICK TURN LEFT ------------------------------ #
    # Event handler for moving the left joystick left
    def on_L3_left(self, value: int) -> None:
        """
        If the positive value of the joystick is above the 
        turn_threshold, turn.
        """
        # if abs(value) > self.turn_threshold:
        #     self.gpg.set_speed(self.turn_speed)
        #     self.gpg.spin_left()
        self.speed = self.normalize_joystick_value(value)
        self.gpg.set_speed(self.speed)
        self.gpg.spin_left()

# ---------------------- JOYSTICK TURN RIGHT ----------------------------- #
    # Event handler for moving the left joystick right
    def on_L3_right(self, value: int) -> None:
        """
        If the positive value of the joystick is above the 
        turn_threshold, turn.
        """
        # if abs(value) > self.turn_threshold:
        #     self.gpg.spin_right()
        #     self.gpg.set_speed(self.turn_speed)
        self.speed = self.normalize_joystick_value(value)
        self.gpg.set_speed(self.speed)
        self.gpg.spin_right()

# --------------------- NORMALIZE JOYSTICK ------------------------------- #
    # def normalize_joystick_value(self, joystick_value: int, dead_zone: float = 0.05) -> int:
    #     """
    #     This function takes a joystick value (between -32767 and 32767)
    #     and normalizes it to a motor power value (between min and max),
    #     including a dead zone calculation and ensuring proper scaling.

    #     Args:
    #         joystick_value (int): The raw joystick value from the controller.
    #         dead_zone (float): The dead zone as a fraction of the total range (default: 0.1).

    #     Returns:
    #         int: The normalized motor power value (min to max).
    #     """
    #     # Calculate the dead zone threshold
    #     dead_zone_threshold = int(dead_zone * self.range_joystick)

    #     # Apply dead zone
    #     if abs(joystick_value) < dead_zone_threshold:
    #         return self.min_power  # Return minimum power if within dead zone

    #     # Determine direction and adjust for dead zone
    #     if joystick_value > 0:
    #         direction = 1
    #         adjusted_value = joystick_value - dead_zone_threshold
    #     else:
    #         direction = -1
    #         adjusted_value = joystick_value + dead_zone_threshold

    #     # Calculate the adjusted range
    #     adjusted_max = self.max_joystick - dead_zone_threshold
    #     adjusted_min = self.min_joystick + dead_zone_threshold
    #     adjusted_range = adjusted_max - adjusted_min

    #     # Normalize the adjusted joystick value to [0, 1]
    #     normalized_value = abs(adjusted_value) / adjusted_range

    #     # Scale to power range
    #     power_range = self.max_power - self.min_power
    #     scaled_value = normalized_value * power_range

    #     # Add minimum power and reapply direction
    #     final_value = int(scaled_value) + self.min_power
    #     final_value *= direction

    #     # Ensure the final value is within the valid range
    #     return max(self.min_power, min(self.max_power, final_value))

# --------------------- NORMALIZE JOYSTICK ------------------------------- #
    # def normalize_joystick_value(self, joystick_value: int) -> int:
    #     """
    #     This function takes a joystick value (between -32767 and 32767)
    #     and normalizes it to a motor power value (between min and max),
    #     using a moving average for smoother operation.

    #     Args:
    #         joystick_value (int): The raw joystick value from the controller.
    #     Returns:
    #         int: The normalized motor power value (min to max).
    #     """
    #     # Add the new joystick value to the history
    #     self.joystick_history.append(joystick_value)
    #     print(joystick_value)

    #     # Calculate the average of recent joystick values
    #     average_joystick_value = sum(
    #         self.joystick_history) // len(self.joystick_history)

    #     # Determine the direction
    #     direction = 1 if average_joystick_value >= 0 else -1

    #     # Normalize the averaged joystick value
    #     normalized_value = abs(average_joystick_value) - self.min_joystick

    #     # Scale the normalized value to half the power range (since we'll use both positive and negative)
    #     normalized_value = normalized_value * (self.range_power // 2)

    #     # Divide by the joystick range, using integer division
    #     normalized_value = normalized_value // (self.range_joystick // 2)

    #     # Apply the direction and shift the range
    #     if direction > 0:
    #         normalized_value += self.min_power
    #     else:
    #         normalized_value = -normalized_value + self.min_power

    #     # Ensure the normalized value is within the valid range
    #     normalized_value = max(self.min_power, min(
    #         self.max_power, normalized_value))

    #     return normalized_value

# ----------------------- JOYSTICK BUTTONS ------------------------------- #
    def on_x_press(self):
        """
        Define callback function that executes when the X button is pressed
        """
        print("Hello world! The X button has been pressed.")
        self.gpg.stop()

    def on_x_release(self):
        """
        Define callback function that executes when the X button is released
        """
        print("Goodbye world! The X button has been released.")
        self.gpg.stop()


def main():
    # Create an instance of the MyController class,
    # Specify the connection interface
    # js0 is commonly used for the first controller
    # Disable the use of ds4drv (if applicable)
    controller = MyController(
        # Specify the device interface to connect to
        interface="/dev/input/js0",
        connecting_using_ds4drv=False
    )
    try:
        # Start listening for joystick input from the controller
        # Continuously read data from the joystick until timeout occurs
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
