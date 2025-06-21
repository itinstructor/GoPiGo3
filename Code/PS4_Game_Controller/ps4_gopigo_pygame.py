#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: ps4_pygame_gopigo.py
    Author: William A Loring
    Created: 01/24/2025
    Purpose: Test the PS4 joystick on a Raspberry Pi with pygame and GoPiGo3
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

import pygame
import easygopigo3 as easy


class PS4Controller:
    """PlayStation 4 controller class"""

    def __init__(self, controller_number=0):
        pygame.init()
        pygame.joystick.init()
        # Check if any joystick/game controller is connected
        if pygame.joystick.get_count() == 0:
            print("No joystick detected")
            exit()

        self.controller = pygame.joystick.Joystick(controller_number)
        # This is needed for Pygame below V 2.0.0
        # Buster comes with Pygame 1.9.6
        self.controller.init()

    def get_button(self, button_number):
        return self.controller.get_button(button_number)

    def get_axis(self, axis_number):
        return self.controller.get_axis(axis_number)

    def get_hat(self, hat_number):
        return self.controller.get_hat(hat_number)

    def quit(self):
        pygame.quit()

    def __del__(self):
        self.quit()


class GoPiGoController:
    """GoPiGo3 PlayStation 4 controller interface"""

    def __init__(self, controller_number=0):
        # Constants
        self.MAX_SPEED = 300   # Maximum speed in degrees per second
        self.DEADZONE = 0.1    # Joystick deadzone
        self.TURN_SCALE = 0.8  # Turn scaling factor
        self.DEBUG = False     # Debug output flag
        self.FPS = 30          # Frames per second

        # Initialize components
        self.controller = PS4Controller(controller_number)
        self.gpg = easy.EasyGoPiGo3()
        self.running = False

        # Initialize pygame clock object to control frame rate
        self.clock = pygame.time.Clock()

        # Block all events initially
        pygame.event.set_blocked(None)
        # Only allow necessary events
        pygame.event.set_allowed([pygame.JOYBUTTONDOWN, pygame.JOYAXISMOTION])

# ------------------------------ SCALE INPUT ------------------------------- #
    def scale_input(self, value):
        """Scale joystick input accounting for deadzone"""
        if abs(value) < self.DEADZONE:
            return 0
        return value

# -------------------------------- UPDATE ---------------------------------- #
    def update(self):
        """Non-blocking update"""
        pygame.event.pump()  # Process event queue without blocking

        # Get joystick values directly without event loop
        left_y = -self.scale_input(self.controller.get_axis(1))
        right_x = self.scale_input(self.controller.get_axis(3))

        # Handle emergency stop button (Square)
        if self.controller.get_button(0):
            self.gpg.stop()
            return

        # Calculate motor speeds
        base_speed = left_y * self.MAX_SPEED

        if abs(base_speed) < 1:  # If not moving forward/backward, spin in place
            left_speed = right_x * self.MAX_SPEED
            right_speed = -right_x * self.MAX_SPEED
        else:  # If moving, adjust speeds for turning
            # Reduce inside wheel speed to turn
            turn_factor = 1 - abs(right_x)
            if right_x > 0:  # Turning right
                left_speed = base_speed
                right_speed = base_speed * turn_factor
            else:  # Turning left
                left_speed = base_speed * turn_factor
                right_speed = base_speed

        if self.DEBUG:
            print(f"L: {left_speed:.0f} R: {right_speed:.0f}")

        # Set motor speeds
        self.gpg.set_motor_dps(self.gpg.MOTOR_LEFT, left_speed)
        self.gpg.set_motor_dps(self.gpg.MOTOR_RIGHT, right_speed)

        # Cap frame rate
        self.clock.tick(self.FPS)

# -------------------------------- START ----------------------------------- #
    def start(self):
        """Start the control loop"""
        self.running = True
        try:
            while self.running:
                self.update()
        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            self.cleanup()

# -------------------------------- STOP ------------------------------------ #
    def stop(self):
        """Stop the control loop"""
        self.running = False

# ------------------------------- CLEANUP ---------------------------------- #
    def cleanup(self):
        """Clean up resources"""
        self.gpg.stop()
        self.controller.quit()


def main():
    """Standalone usage"""
    controller = GoPiGoController()
    controller.start()


# Run the main function if the script is executed
# (as opposed to being imported as a module)
if __name__ == "__main__":
    main()
