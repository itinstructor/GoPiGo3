#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the joystick
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

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

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                print("X button pressed")
            elif event.button == 1:
                print("Circle button pressed")
            elif event.button == 2:
                print("Triangle button pressed")
            elif event.button == 3:
                print("Square button pressed")
            elif event.button == 4:
                print("L1 button pressed")
            elif event.button == 5:
                print("R1 button pressed")
            elif event.button == 6:
                print("L2 button pressed")
            elif event.button == 7:
                print("R2 button pressed")
            elif event.button == 8:
                print("Share button pressed")
            elif event.button == 9:
                print("Options button pressed")
            elif event.button == 10:
                print("PS button pressed")
            elif event.button == 11:
                print("11 L3 button pressed")
            elif event.button == 12:
                print("12 R3 button pressed")
            elif event.button == 13:
                print("Touchpad button pressed")
        elif event.type == pygame.JOYBUTTONUP:
            if event.button == 0:
                print("X button released")
            elif event.button == 1:
                print("Circle button released")
            elif event.button == 2:
                print("Triangle button released")
            elif event.button == 3:
                print("Square button released")
            elif event.button == 4:
                print("L1 button released")
            elif event.button == 5:
                print("R1 button released")
            elif event.button == 6:
                print("L2 button released")
            elif event.button == 7:
                print("R2 button released")
            elif event.button == 8:
                print("Share button released")
            elif event.button == 9:
                print("Options button released")
            elif event.button == 10:
                print("10 PS button released")
            elif event.button == 11:
                print("11 R3 button released")
            elif event.button == 12:
                print("12 R3 button released")
            elif event.button == 13:
                print("Touchpad button released")
        # elif event.type == pygame.JOYAXISMOTION:
        #     for i in range(joystick.get_numaxes()):
        #         axis = joystick.get_axis(i)
        #         print(f"Axis {i}: {axis}")
        #         if i == 2:
        #             print(f"L2 trigger value: {axis}")
        #         elif i == 5:
        #             print(f"R2 trigger value: {axis}")
        elif event.type == pygame.JOYHATMOTION:
            for i in range(joystick.get_numhats()):
                hat = joystick.get_hat(i)
                if hat == (0, 0):
                    print("D-pad centered")
                elif hat == (1, 0):
                    print("D-pad right")
                elif hat == (-1, 0):
                    print("D-pad left")
                elif hat == (0, 1):
                    print("D-pad up")
                elif hat == (0, -1):
                    print("D-pad down")
                elif hat == (1, 1):
                    print("D-pad up-right")
                elif hat == (-1, 1):
                    print("D-pad up-left")
                elif hat == (1, -1):
                    print("D-pad down-right")
                elif hat == (-1, -1):
                    print("D-pad down-left")