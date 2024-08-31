#!/usr/bin/env python3
# Import the time library for the sleep function
import time                             
# Import the GoPiGo3 library
import easygopigo3 as easy              

# Initialize EasyGoPiGo3 object
gpg = easy.EasyGoPiGo3()         

# Initialize servo object on Servo Port 2, right side of GoPiGo
servo = gpg.init_servo("SERVO2")

# Set servo pointing straight ahead at 90 degrees
# You may have to change the degrees to adapt to your servo
# All servos line up slightly differently
FORWARD = 85
servo.rotate_servo(FORWARD)
print("Forward")
time.sleep(1)


# ---------------------- MAIN PROGRAM -------------------------------------#
def main():
    # Right
    print("Right")
    servo.rotate_servo(FORWARD + 55)
    time.sleep(2)

    # Left
    print("Left")
    servo.rotate_servo(FORWARD - 55)
    time.sleep(1)

    # Forward
    print("Forward")
    servo.rotate_servo(FORWARD)
    time.sleep(1)

    # Disable or "float" the servo
    servo.disable_servo()

    gpg.reset_all()

# If a standalone program, call the main function
# Else, use as a module
if __name__ == '__main__':
    main()

