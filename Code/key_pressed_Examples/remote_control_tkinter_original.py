import Tkinter as tk
from gopigo import *

servo_range = [2,3,4,5,6,7,8]

def key_input(event):
    key_press = event.keysym.lower()
    print(key_press)

    if key_press == 'w':
        fwd()
    elif key_press == 's':
        bwd()
    elif key_press == 'a':
        left()
    elif key_press == 'd':
        right()
    elif key_press == 'q':
        left_rot()
    elif key_press == 'e':
        right_rot()
    elif key_press == 'space':
        stop()
    elif key_press == 'u':
        print(us_dist(15))

    elif key_press.isdigit():
        if int(key_press) in servo_range:
            enable_servo()
            servo(int(key_press)*14)
            time.sleep(1)
            disable_servo()

command = tk.Tk()
command.bind_all('', key_input)
command.mainloop()