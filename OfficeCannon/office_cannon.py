#!/usr/bin/env python3
# Much of this code comes from Dexter Industries' GoPiGo with office cannon script,
# with minor changes for user-input from a keyboard.
#
# http://www.dexterindustries.com/GoPiGo/
# ------------------------------------------------
# History
# ------------------------------------------------
# Author     	Date      		Comments
# John Cole  	April 14  		Initial Authoring
# Karan			27 June 14		Code cleanup and made more responsive
# 25 Aug  14		USB high current mode for Raspberry Pi Model B+ added
# Loring        10/16/21        Convert to EasyGoPyGo3 and Python 3.5
##
##

import usb.util
import usb.core
# import base64
# import urllib
# import json
# import re
# import socket
import time
import platform
import sys
import os
# import struct
from tkinter import *       # Import tkinter for GUI
import easygopigo3 as easy  # Import EasyGoPiGo3 library
gpg = easy.EasyGoPiGo3()    # Create EasyGoPiGo3 object

servo_range = [2, 3, 4, 5, 6, 7, 8]


# Enable for Model B+ and disable for Model B
# For the model B+ we need to turn this variable on to run the Office Cannon.
model_b_plus = True
# This can be left on for the Model B and not cause problems.
# This pulls GPIO 38 to high, which overrides USB overcurrent setting.
# With this set, the USB can deliver up to 1.2 Amps.
tdelay = 80
# Protocol command bytes
DOWN = 0x01
UP = 0x02
LEFT = 0x04
RIGHT = 0x08
FIRE = 0x10
STOP = 0x20

DEVICE = None
DEVICE_TYPE = None

# file = open("/dev/input/mice", "rb")
debug = 0


# Setup the Office Cannon
def setup_usb():
    print("Setting up USB")
    global DEVICE
    global DEVICE_TYPE

    DEVICE = usb.core.find(idVendor=0x2123, idProduct=0x1010)

    if DEVICE is None:
        DEVICE = usb.core.find(idVendor=0x0a81, idProduct=0x0701)
        if DEVICE is None:
            raise ValueError('Missile device not found')
        else:
            DEVICE_TYPE = "Original"
    else:
        DEVICE_TYPE = "Thunder"

    # On Linux we need to detach usb HID first
    if "Linux" == platform.system():
        try:
            DEVICE.detach_kernel_driver(0)
        except Exception:
            pass  # already unregistered
    DEVICE.set_configuration()
    print("USB setup successful")


# Send command to the office cannon
def send_cmd(cmd):
    if "Thunder" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0, 0, [
                             0x02, cmd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    elif "Original" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0x0200, 0, [cmd])


# Send command to control the LED on the office cannon
def led(cmd):
    if "Thunder" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0, 0, [
                             0x03, cmd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    elif "Original" == DEVICE_TYPE:
        print("There is no LED on this device")


# Send command to move the office cannon
def send_move(cmd, duration_ms):
    send_cmd(cmd)
    time.sleep(duration_ms / 1000.0)
    send_cmd(STOP)


def run_command(command, value):
    command = command.lower()
    if command == "right":
        send_move(RIGHT, value)
    elif command == "left":
        send_move(LEFT, value)
    elif command == "up":
        send_move(UP, value)
    elif command == "down":
        send_move(DOWN, value)
    elif command == "zero" or command == "park" or command == "reset":
        # Move to bottom-left
        send_move(DOWN, 2000)
        send_move(LEFT, 8000)
    elif command == "pause" or command == "sleep":
        time.sleep(value / 1000.0)
    elif command == "led":
        if value == 0:
            led(0x00)
        else:
            led(0x01)
    elif command == "fire" or command == "shoot":
        if value < 1 or value > 4:
            value = 1
        # Stabilize prior to the shot, then allow for reload time after.
        time.sleep(0.5)
        for i in range(value):
            send_cmd(FIRE)
            time.sleep(4.5)
    else:
        print("Error: Unknown command: '%s'" % command)


def run_command_set(commands):
    for cmd, value in commands:
        run_command(cmd, value)


# # Read the values from the mouse
# def getMouseEvent():
#     buf = file.read(3)
#     button = ord(buf[0])
#     bLeft = button & 0x1
#     bMiddle = (button & 0x4) > 0
#     bRight = (button & 0x2) > 0
#     x, y = struct.unpack("bb", buf[1:])
#     if debug:
#         print("L:%d, M: %d, R: %d, x: %d, y: %d\n" %
#               (bLeft, bMiddle, bRight, x, y))
#     return [bLeft, bMiddle, bRight, x, y]


flag = 0


# # Control the office cannon
# def control():
#     global flag
#     # Get the inputs from the mouse
#     [bLeft, bMiddle, bRight, x, y] = getMouseEvent()

#     # GoPiGo control
#     if flag == 1:  # If left or right mouse not pressed, move forward
#         gpg.forward()
#         flag = 0
#     if bLeft:  # If left mouse buton pressed, turn left
#         gpg.left()
#         flag = 1

#     if bRight:  # If right mouse button presses, turn right
#         gpg.right()
#         flag = 1
#     if bLeft and bRight:  # If both the left and right mouse buttons pressed, go back
#         gpg.stop()
#         flag = 0

#     # Office cannon control
#     if bMiddle > 0:
#         print("fire rockets")
#         run_command("fire", tdelay)

#     # Move the mouse left to move the cannon left
#     # Move the mouse right to move the cannon right
#     # Press middle button to fire
#     if x == 0:
#         print("Stop rockets")
#     elif x > 10:
#         print("Left rockets")
#         run_command("left", tdelay)
#     elif x < -10:
#         print("Right rockets")
#         run_command("right", tdelay)
#     if y == 0:
#         print("Stop Rockets Y")
#     elif y > 10:
#         print("Up Rockets")
#         run_command("up", tdelay)
#     elif y < -10:
#         print("Down rockets")
#         run_command("down", tdelay)

#     time.sleep(.1)
#     return


def key_input(event):
    key_press = event.keysym.lower()
    print(key_press)

    if key_press == 'w':
        gpg.forward()
    elif key_press == 's':
        gpg.backward()
    elif key_press == 'a':
        gpg.left()
    elif key_press == 'd':
        gpg.right()
    elif key_press == 'q':
        gpg.spin_left()
    elif key_press == 'e':
        gpg.spin_right()
    # Stop when spacebar pressed
    elif key_press == ' ':
        gpg.stop()
    # Exit program
    elif key_press == 'z':
        print("Exiting")
        sys.exit()

    # elif key_press.isdigit():
    #     if int(key_press) in servo_range:
    #         enable_servo()
    #         servo(int(key_press)*14)
    #         time.sleep(1)
    #         disable_servo()

    elif key_press == 'control_r' or key_press == 'control_l':
        print('Fire rockets!')
        run_command("fire", tdelay)

    elif key_press == 'left':
        print('Left rockets')
        run_command('left', tdelay)
    elif key_press == 'right':
        print('right rockets')
        run_command('right', tdelay)
    elif key_press == 'up':
        print('up rockets')
        run_command('up', tdelay)
    elif key_press == 'down':
        print('down rockets')
        run_command('down', tdelay)


#--------------------------------- CREATE WIDGETS -------------------------------------#
def create_widgets():
    """ Create and layout widgets
        Reference for GUI display

    W = Forward      Q = Spin Left
    S = Backward     E = Spin Right
    A = Left         
    D = Right        Spacebar = Stop
    T = Increase Speed
    G = Decrease Speed
    arrow keys rocket position
    CTRL R or CTRL L Fires!
    Speed: 300
    """
    # Create widgets
    lbl_remote_w = Label(text="W: Forward")
    lbl_remote_q = Label(text="Q: Spin Left")
    lbl_remote_s = Label(text="S: Backward")
    lbl_remote_e = Label(text="E: Spin Right")
    lbl_remote_a = Label(text="A: Left")
    lbl_remote_spacebar = Label(text="Spacebar: Stop")
    lbl_remote_d = Label(text="D: Right")
    lbl_remote_t = Label(text="T: Increase Speed")
    lbl_remote_g = Label(text="G: Decrease Speed")
    lbl_remote_z = Label(text="Z: Exit")
    lbl_move_cannon = Label(text="Cursor keys move cannon")
    lbl_fire_cannon = Label(text="CTRL R or CTRL L FIRE!!!")

    # Get and display current GoPiGo speed setting
    speed = gpg.get_speed()
    lbl_speed = Label(text="Speed: " + str(speed))

    # Grid the widgets
    lbl_remote_w.grid(row=0, column=0, sticky=W)
    lbl_remote_q.grid(row=0, column=1, sticky=W)
    lbl_remote_s.grid(row=1, column=0, sticky=W)
    lbl_remote_e.grid(row=1, column=1, sticky=W)
    lbl_remote_a.grid(row=2, column=0, sticky=W)
    lbl_remote_spacebar.grid(row=2, column=1, sticky=W)
    lbl_remote_d.grid(row=3, column=0, sticky=W)
    lbl_remote_t.grid(row=4, column=0, sticky=W)
    lbl_remote_g.grid(row=5, column=0, sticky=W)
    lbl_speed.grid(row=6, column=0, sticky=W)
    lbl_remote_z.grid(row=6, column=1, sticky=W)
    lbl_move_cannon.grid(row=7, column=0, columnspan=2, sticky=W)
    lbl_fire_cannon.grid(row=8, column=0, columnspan=2, sticky=W)

    # Set padding for all widgets
    for child in window.winfo_children():
        child.grid_configure(padx=4, pady=4)


setup_usb()

# Enable USB to give supply upto 1.2A on model B+
if model_b_plus:
    os.system("gpio -g write 38 0")
    os.system("gpio -g mode 38 out")
    os.system("gpio -g write 38 1")

run_command("zero", 100)
gpg.stop()

window = Tk()
# 320x200 pixels in size, location at 100x100
window.geometry("350x400+100+100")
window.bind_all('<Key>', key_input)
create_widgets()
window.mainloop()
