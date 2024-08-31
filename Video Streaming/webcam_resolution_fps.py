# Does not work on windows

import cv2
import time
cam = cv2.VideoCapture(0)
num_frame = 0

# List of resolutions to test
resolution = [
    (640, 480), (640, 480), (704, 680), (800, 600), (960, 680),
    (1280, 720), (1440, 720), (1920, 1080)
]

for i, j in enumerate(resolution):
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, j[0])
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, j[1])

    w = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

    print(f"Resolution: {w} x {h}")
    start = time.time()
    while (True):
        ret, frame = cam.read()
        if num_frame < 60:
            num_frame = num_frame + 1
        else:
            total_time = (time.time() - start)
            fps = (num_frame / total_time)
            print(f"{num_frame} Frames {total_time:.2f} Seconds: {fps:.2f} fps")
            break

cam.release()
cv2.destroyAllWindows()
