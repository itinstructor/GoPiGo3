#!/usr/bin/env python
import tkinter as tk
import pygame
import threading

# Initialize Pygame
pygame.init()

# Create a function to run the Pygame loop


def run_pygame():
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Pygame in Tkinter")
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  # Exit the loop and the function

        # Fill the screen with a color
        screen.fill((0, 128, 255))  # Light blue
        pygame.display.flip()  # Update the display
        clock.tick(60)  # Limit frames per second


# Create the main Tkinter window
root = tk.Tk()
root.title("Tkinter with Pygame")
root.geometry("400x300")

# Create a button to start the Pygame loop
start_button = tk.Button(root, text="Start Pygame",
                         command=lambda: threading.Thread(target=run_pygame).start())
start_button.pack(pady=20)

# Run the Tkinter main loop
root.mainloop()
