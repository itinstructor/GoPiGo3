import tkinter as tk


# Create a function that will be called when a key is pressed
def on_key_press(event):
    pressed_key = event.keysym
    print(f"Key {pressed_key} pressed")


# Create a tkinter window
root = tk.Tk()
root.title("Key Event Example")

# Bind the key press event to the on_key_press function
root.bind("<KeyPress>", on_key_press)

# Start the tkinter main loop
root.mainloop()
