import tkinter as tk
import threading
from gopigo import *

class GoPiGoRemoteControl:
    def __init__(self, root):
        self.root = root
        self.root.title("GoPiGo Remote Control")

        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        initialize()
        self.setup_key_events()

    def setup_key_events(self):
        self.forward_event = threading.Event()
        self.backward_event = threading.Event()
        self.left_event = threading.Event()
        self.right_event = threading.Event()

        self.root.bind("<KeyPress>", self.key_pressed)
        self.root.bind("<KeyRelease>", self.key_released)

    def key_pressed(self, event):
        key = event.keysym
        if key == "w":
            self.forward_event.set()
        elif key == "s":
            self.backward_event.set()
        elif key == "a":
            self.left_event.set()
        elif key == "d":
            self.right_event.set()

    def key_released(self, event):
        key = event.keysym
        if key == "w":
            self.forward_event.clear()
        elif key == "s":
            self.backward_event.clear()
        elif key == "a":
            self.left_event.clear()
        elif key == "d":
            self.right_event.clear()

    def update(self):
        while True:
            if self.forward_event.is_set():
                fwd()
            elif self.backward_event.is_set():
                bwd()
            elif self.left_event.is_set():
                left()
            elif self.right_event.is_set():
                right()
            else:
                stop()
            time.sleep(0.1)

    def start(self):
        update_thread = threading.Thread(target=self.update)
        update_thread.daemon = True
        update_thread.start()
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = GoPiGoRemoteControl(root)
    app.start()
