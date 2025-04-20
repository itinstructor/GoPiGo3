import tkinter as tk
from threading import Thread, Event
import time


class ThreadingApp:
    def __init__(self):
        # Create the main window of the application
        self.root = tk.Tk()
        # Set the title of the window
        self.root.title("Threading Example")
        # Set the size of the window
        self.root.geometry("300x200")
        # Call the method to set up the GUI elements
        self.setup_gui()

        # Event to signal the thread to stop
        self.stop_event = Event()
        # Boolean flag to track the thread state
        self.is_running = False

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

# ----------------------------- SETUP GUI ---------------------------------- #
    def setup_gui(self):
        # Configure grid layout to center widgets
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Create and grid label widget to display text
        self.lbl_display = tk.Label(self.root, text="Threading Example")
        self.lbl_display.grid(
            row=0, column=0, columnspan=2, pady=20, sticky="nsew")

        # Create and grid a button that will start/stop the thread when clicked
        self.toggle_button = tk.Button(
            self.root,                    # Parent widget is the main window
            text="Start Thread",          # Text shown on the button
            command=self.toggle_thread    # Method called when button is clicked
        )
        self.toggle_button.grid(
            row=1, column=0, columnspan=2, pady=20, padx=10, sticky="nsew")

# ----------------------------- BACKGROUND TASK ---------------------------- #
    def background_task(self):
        """This method runs in a separate thread
           and performs a background task"""
        # While the stop event is not set, keep running the task
        while not self.stop_event.is_set():
            # Update the label text with the current timestamp
            now = time.localtime()
            now = f"{now.tm_min:02d}:{now.tm_sec:02d}"
            self.lbl_display.config(
                text=f"Running background task\n {now}"
            )

            # Pause for 1 second before the next update
            time.sleep(1)

# ----------------------------- TOGGLE THREAD ------------------------------ #
    def toggle_thread(self):
        if self.is_running:
            self.stop_thread()
        else:
            self.start_thread()

# ----------------------------- START THREAD ------------------------------- #
    def start_thread(self):
        # Clear the stop event before starting the thread
        self.stop_event.clear()
        # Create a new thread object
        self.thread = Thread(
            target=self.background_task,  # Function to run in the thread
            daemon=True                   # Thread stops when program ends
        )
        self.thread.start()
        # Update the button text and flag
        self.toggle_button.config(text="Stop Thread")
        self.is_running = True

# ----------------------------- STOP THREAD -------------------------------- #
    def stop_thread(self):
        # Set the stop event to signal the thread to stop
        self.stop_event.set()
        # Update the button text and flag
        self.toggle_button.config(text="Start Thread")
        self.is_running = False

# ----------------------------- ON CLOSING --------------------------------- #
    def on_closing(self):
        # Stop the thread when closing the window
        self.stop_thread()
        # Destroy the window
        self.root.destroy()


def main():
    app = ThreadingApp()


if __name__ == "__main__":
    main()
