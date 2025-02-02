#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: ps4_pygame_gopigo_1.py
    Author: William A Loring
    Created: 01/24/2025
    Purpose: PS4 joystick on a Raspberry Pi with pygame and GoPiGo3
    Left stick Y-axis controls forward/backward movement
    Right stick X-axis controls turning
    Square button is an emergency stop
    Triangle button exits the program
"""
# PS4 Controller Button Mapping:
# Button 0: X (Cross)
# Button 1: Circle
# Button 2: Triangle
# Button 3: Square
# Button 4: L1
# Button 5: R1
# Button 6: L2
# Button 7: R2
# Button 8: Share
# Button 9: Options
# Button 10: PS (PlayStation Button)
# Button 11: L3 (Left Stick Press)
# Button 12: R3 (Right Stick Press)
# Button 13: Touchpad Press

import pygame  # Import the Pygame library for handling the game controller
# Import the EasyGoPiGo3 library for controlling the GoPiGo3 robot
import easygopigo3 as easy

# Initialize Pygame and joystick
pygame.init()  # Initialize all Pygame modules
pygame.joystick.init()  # Initialize the joystick module

# Check if any joystick/game controller is connected
if pygame.joystick.get_count() == 0:
    print("No joystick detected")
    exit()  # Exit the program if no joystick is detected

# Create a Joystick object for the first joystick
joystick = pygame.joystick.Joystick(0)
# Initialize the joystick, needed for GoPiGo3 with pygame 1.96
joystick.init()

# Create an EasyGoPiGo3 object to control the GoPiGo3 robot
gpg = easy.EasyGoPiGo3()

# Maximum speed in degrees/s for the GoPiGo3 robot
MAX_SPEED = 300

# Joystick deadzone to prevent drift (small movements around the center are ignored)
DEADZONE = 0.1
FPS = 30  # Frames per second for the main loop

# Debug flag
DEBUG = False  # Set to True to print joystick values for debugging purposes
clock = pygame.time.Clock()  # Create a Clock object to manage the frame rate


# -------------------------- SCALE INPUT ----------------------------------- #
def scale_input(value, deadzone=DEADZONE):
    """Scale joystick input accounting for deadzone"""
    # If the absolute value of the movment is less than the deadzone value
    if abs(value) < DEADZONE:
        return 0  # Return 0 if the joystick value is within the deadzone
    return value  # Return the original value if it is outside the deadzone


# -------------------------- MAIN FUNCTION --------------------------------- #
def main():
    # Set the running flag to True to start the main loop
    # Set this flag to to False to exit the main loop
    running = True  
    try:
        while running:
            # Loop through all captured events, this is a list
            for event in pygame.event.get():
                # Exit the main loop if the window is closed
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.JOYBUTTONDOWN:
                    # Square button (button 3) - emergency stop
                    if event.button == 3:
                        gpg.stop()  # Stop the GoPiGo3 robot
                        print("Emergency Stop!")
                    # Triangle button (button 2) - exit program
                    elif event.button == 2:
                        running = False  # Exit the main loop

            # Get joystick values
            # Get the Y-axis value of the left stick (inverted for forward/backward)
            left_y = -scale_input(joystick.get_axis(1))
            # Get the X-axis value of the right stick (for turning)
            right_x = scale_input(joystick.get_axis(3))

            # Debug print
            if DEBUG:
                print(f"Left Y: {left_y:.2f}, Right X: {right_x:.2f}")

            # Calculate motor speeds for differential steering
            # Calculate the base speed from the left stick Y-axis value
            base_speed = left_y * MAX_SPEED

            # Handle turning
            # If not moving forward/backward, spin in place
            if abs(base_speed) < 1:
                left_speed = right_x * MAX_SPEED  # Set the left motor speed for turning
                # Set the right motor speed for turning (opposite direction)
                right_speed = -right_x * MAX_SPEED
             # If moving, adjust speeds for turning
            else:
                # Reduce inside wheel speed based on the right stick X-axis value
                turn_factor = 1 - abs(right_x)
                if right_x > 0:  # Turning right
                    left_speed = base_speed  # Set the left motor speed to the base speed
                    right_speed = base_speed * turn_factor  # Reduce the right motor speed
                else:  # Turning left
                    left_speed = base_speed * turn_factor  # Reduce the left motor speed
                    right_speed = base_speed  # Set the right motor speed to the base speed

            # Debug print if DEBUG flag is True
            if DEBUG:
                print(
                    f"Left Speed: {left_speed:.2f}\
                    , Right Speed: {right_speed:.2f}"
                )

            # Set the speed of the left motor
            gpg.set_motor_dps(gpg.MOTOR_LEFT, left_speed)
            # Set the speed of the right motor
            gpg.set_motor_dps(gpg.MOTOR_RIGHT, right_speed)

            # Limit the frame rate to the specified FPS
            clock.tick(FPS)

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        gpg.stop()  # Stop the GoPiGo3 robot when exiting the program
        pygame.quit()  # Quit Pygame


if __name__ == "__main__":
    main()  # Call the main function to start the program
