"""
    Name: webcam_resolution_wikipedia.py
    Author: 
    Created: 
    Purpose: 
    Original idea from:
    https://www.learnpythonwithrune.org/find-all-possible-webcam-resolutions-with-opencv-in-python/
"""
# Raspberry Pi
# sudo pip3 install opencv-python
# sudo pip3 install pillow -U
# sudo apt-get install libatlas-base-dev
# sudo pip3 install numpy
# sudo pip3 install pandas

# Windows
# pip install opencv-python
# pip install pillow
# pip install numpy
# pip install pandas
# pip install lxmlsudo


import json
import pandas as pd
import cv2
import time


#------------- CONVERT SECONDS TO HOURS, MINUTES, SECONDS ---------------------#
def convert(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))


# Begin timing
start_time = time.time()
cam = cv2.VideoCapture(0)

url = "https://en.wikipedia.org/wiki/List_of_common_resolutions"
table = pd.read_html(url)[0]
print(table)
# Get rows in talbe
row_count = len(table.index)
table.columns = table.columns.droplevel()
# Store result resolutions in dictionary
resolutions = {}
for index, row in table[["W", "H"]].iterrows():
    print(f" {index + 1} of {row_count}")
    w = row["W"]
    h = row["H"]
    test_resolution = f"{w}.0 x {h}.0"
    print(f"      Test resolution: {test_resolution}")

    # Try to set resolution on camera
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, row["W"])
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, row["H"])

    # Get supported camera resolution
    # If camera doesn't have that resolution,
    # cv will go to the nearest supported resolution
    width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

    resolution = f"{width} x {height}"
    print(f" Supported resolution: {resolution}")
    # Create dictionary of results
    resolutions[f" {width} x {height}"] = "OK"

    # Loop timing
    elapsed_time = time.time()
    current_elapsed_time = elapsed_time - start_time
    print(f"         Elapsed time: {convert(current_elapsed_time)}\n")

# Serialize dictinary to json for nice display
json_object = json.dumps(resolutions, indent=4)
print(json_object)

# Save dictionary as json to file
with open("webcam_wikipedia_resolution.json", "w") as outfile:
    json.dump(resolutions, outfile)

# End timing
end = time.time()
elapsed_time = end - start_time
print(f" Total elapsed time: {convert(elapsed_time)}")
