# https://webcamtests.com/resolution

import json
import cv2
import time

# Begin timing
start = time.time()

cam = cv2.VideoCapture(0)
# List of standard resolutions to test
YOUTUBE_240p = (426, 240)
YOUTUBE_360p = (640, 360)
VGA = (640, 480)
SVGA = (800, 600)
YOUTUBE_480 = (854, 480)
DVCPRO_HD = (960, 720)
HD = (1280, 720)
SXVGA = (1280, 1024)
FHD = (1920, 1080)

resolution = (
    YOUTUBE_240p, YOUTUBE_360p, VGA, SVGA,
    YOUTUBE_480, DVCPRO_HD,
    HD, SXVGA, FHD
)

# Dictionary to store resolution test results
resolutions = {}
# Iterate through tuple of resolutions to test
for w, h in resolution:
    test_resolution = f"{w}.0 x {h}.0"
    print(f"  Test resolution: {test_resolution}")
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
    resolution = f"{width} x {height}"
    print(f"Result resolution: {resolution}\n")
    # Create dictionary of results
    resolutions[f"{width} x {height}"] = "OK"

# Serialize dictinary to json for nice display
json_object = json.dumps(resolutions, indent=4)
print(json_object)

# Save dictionary as json to file
with open("webcam_standard_resolution.json", "w") as outfile:
    json.dump(resolutions, outfile)

# End timing
end = time.time()
elapsed_time = end - start
formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
print(f"Elapsed time: {formatted_time}")


"""
{'640.0x360.0': 'OK', '640.0x480.0': 'OK', '800.0x600.0': 'OK',
 '800.0x448.0': 'OK','960.0x720.0': 'OK', '1280.0x720.0': 'OK',
  '1920.0x1080.0': 'OK'
}
"""


# cam.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[4][0])
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[4][1])

# w = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
# h = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

# print(f"Resolution: {w} {h}")
# # Check default resolution of camera
# w = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
# h = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

# resolution_tested = f"Resolution: {w} {h}"
# print(resolution_tested)

# Display resolutions
# while cam.isOpened():
#     ret, frame = cam.read()
#     cv2.imshow(f"{resolution_tested}", frame)
#     key = cv2.waitKey(10) & 0xff
#     # Press SPACEBAR
#     if key == 27:
#         # Press ESC
#         break
