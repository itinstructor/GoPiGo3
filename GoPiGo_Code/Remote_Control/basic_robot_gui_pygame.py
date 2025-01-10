#!/usr/bin/env python3

# Based on https://pythonprogramming.net/robotics-raspberry-pi-tutorial-gopigo-introduction
# Purpose: GoPiGo3 Tkinter remote control program
############################################################################
# Basic example for controlling the GoPiGo using the Keyboard
# Contributed by casten on Gitub https://github.com/DexterInd/GoPiGo/pull/112
#
# This code lets you control the GoPiGo from the VNC or Pi Desktop.
# Also, these are non-blocking calls so it is much more easier to use too.
#
# Controls:
# w:	Move forward
# a:	Turn left
# d:	Turn right
# s:	Move back
# x:	Stop
# t:	Increase speed
# g:	Decrease speed
# z: 	Exit
# http://www.dexterindustries.com/GoPiGo/
# History
# ------------------------------------------------
# Author     	Date      		Comments
# Karan		27 June 14			Code cleanup
# Casten	31 Dec  15			Added async io, action until keyup
# Karan		04 Jan	16			Cleaned up the GUI

############################################################################

# Import EasyGoPiGo3 library
import pygame  # Gives access to KEYUP/KEYDOWN events
import sys  # Used for closing the running program
import easygopigo3 as easy
# Create EasyGoPiGo3 object
gpg = easy.EasyGoPiGo3()

# Initialization for pygame
pygame.init()
screen = pygame.display.set_mode((700, 400))
pygame.display.set_caption('Remote Control Window')

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

# Display some text
instructions = '''
                      BASIC GOPIGO CONTROL GUI

This is a basic example for the GoPiGo Robot control 

(Be sure to put focus on thi window to control the gopigo!)

Press:
      ->w: Move GoPiGo Robot forward
      ->a: Turn GoPiGo Robot left
      ->d: Turn GoPiGo Robot right
      ->s: Move GoPiGo Robot backward
      ->t: Increase speed
      ->g: Decrease speed
      ->z: Exit
'''
size_inc = 22
index = 0
for i in instructions.split('\n'):
    font = pygame.font.Font(None, 36)
    text = font.render(i, 1, (10, 10, 10))
    background.blit(text, (10, 10+size_inc*index))
    index += 1

# Blit everything to the screen
screen.blit(background, (0, 0))
pygame.display.flip()

while True:
    event = pygame.event.wait()
    if (event.type == pygame.KEYUP):
        gpg.stop()
        continue
    if (event.type != pygame.KEYDOWN):
        continue
    char = event.unicode
    if char == 'w':
        gpg.forward()  # Move forward
    # elif char == 'a':
    #     left()  # Turn left
    # elif char == 'd':
    #     right()  # Turn Right
    elif char == 's':
        gpg.backward()  # Move back
    # elif char == 't':
    #     increase_speed()  # Increase speed
    # elif char == 'g':
    #     decrease_speed()  # Decrease speed
    elif char == 'z':
        print("Exiting")		# Exit
        sys.exit()
