"""when a key is pressed, the keypress_event function sets the
key_event event, notifying the worker thread to start processing.
The worker thread waits for the event to be set
using key_event.wait() and then performs its background processing."""

import tkinter as tk
import threading


class KeypressTest:
    def __init__(self) -> None:
        root = tk.Tk()

        # Create a Tkinter window
        root.title("Key Press Event Example")

        # Bind the keypress event to the keypress_event function
        root.bind('<KeyPress>', self.keypress_event)

        # Create a threading.Event to coordinate between threads
        self.key_event = threading.Event()
        # Create and start a separate thread for background processing
        thread = threading.Thread(target=self.worker_thread)
        thread.start()

        root.mainloop()

    def keypress_event(self, event):
        # This function will be called when a key is pressed
        self.key = event.char
        print(f'Key pressed: {self.key}')
        self.key_event.set()

    def worker_thread(self):
        while True:
            # Wait for the key event to be set
            self.key_event.wait()
            # Your background processing logic here
            print("Worker thread is processing...")
            # Reset the event
            self.key_event.clear()
            # print(f"Pressed {self.key}")


keypress_test = KeypressTest()
