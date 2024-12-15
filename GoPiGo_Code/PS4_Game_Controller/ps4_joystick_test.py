"""
    Name: ps4_joystick_test.py
    Author: William A Loring
    Created: 06/17/24
    Purpose: Test the PS4 joystick on a Raspberry Pi
    https://github.com/ArturSpirin/pyPS4Controller
"""
# sudo pip3 install pyps4controller
# Import the Controller class from the pyPS4Controller library
from pyPS4Controller.controller import Controller


class MyController(Controller):
    def __init__(self, **kwargs):
        # Call base class constructor to handle common initialization logic
        super().__init__(**kwargs)

    def on_L3_up(self, value):
        print("Joystick moved up with value:", value)

    def on_L3_down(self, value):
        print("Joystick moved down with value:", value)

    def on_L3_left(self, value):
        print("Joystick moved left with value:", value)

    def on_L3_right(self, value):
        print("Joystick moved right with value:", value)


controller = MyController(
    interface="/dev/input/js0", connecting_using_ds4drv=False
)
controller.listen(timeout=60)
