#!/usr/bin/env python3
"""
    Name:    bme280_thingspeak.py
    Author:  William A Loring
    Created: 10/27/21 Revised:
    Purpose: Upload temperature, humidity, and barometric pressure
    to a ThingSpeak Channel
"""
# This uses the EasyGoPiGo3 library
# https://gopigo3.readthedocs.io/en/master/api-basic/easygopigo3.html#easygopigo3

# Import the time library for the sleep function
import time
import sys  # For clean CTRL-C break
import requests
# Import GoPiGo3 library
from easygopigo3 import EasyGoPiGo3
# Import sensor library
from di_sensors.easy_temp_hum_press import EasyTHPSensor

# api key for updating ThingSpeak
TS_KEY = "Your ThingSpeak API Key"

# ThingSpeak data dictionary
ts_data = {}

# Create an instance of the GoPiGo3 class
gpg = EasyGoPiGo3()

# Initialize a bme280 Temperature, Humidity, Pressure object
my_thp = EasyTHPSensor()


def main():
    print(" +-------------------------------------------------------+")
    print(" | Thingspeak BME280 Temperature, Humidity, and Pressure |")
    print(" +-------------------------------------------------------+")
    minutes = float(input(" Minutes between uploads: "))
    read_time = minutes * 60
    
    while True:
        # ============================================================
        # field1: Read Temperature in Fahrenheit
        temp = my_thp.safe_fahrenheit()

        # ============================================================
        # field2: Read Relative Humidity in percent
        hum = my_thp.safe_humidity()

        # ============================================================
        # field3: Read barometric pressure in pascals
        press_pascals = my_thp.safe_pressure()

        # Convert pascals to inHg
        press_inhg = press_pascals / 3386.3886666667
        # Compensate for 3960' altitude 4.04
        # Scottsbluff, NE, Heilig Field, 4.04
        press_inhg = press_inhg + 4.04

        # Print the values to the console
        print(" Upload data to ThingSpeak (CTRL-C to quit)")
        message = f" Temperature: {temp:3.0f}°F | "
        message = message + f"Humidity: {hum:3.0f}% | "
        message = message + f"Pressure: {press_inhg:3.2f} inHg"
        print(message)

        # Send sensor data to ThingSpeak
        thingspeak_send(temp, hum, press_inhg)

        # 20 seconds is the minimum amount of time between uploads
        time.sleep(read_time)


# --------------------- SEND TO THINGSPEAK ------------------------------- #
def thingspeak_send(temp, hum, press):
    """
        Update the ThingSpeak channel using the requests library
    """
    print(" Update Thingspeak Channel")

    # Each field number corresponds to a field in ThingSpeak
    params = {
        "api_key": TS_KEY,
        "field1": temp,
        "field2": hum,
        "field3": press
    }

    # Update data on Thingspeak
    ts_update = requests.get(
        "https://api.thingspeak.com/update",
        params=params
    )

    # Was the update successful?
    if ts_update.status_code == requests.codes.ok:
        print(" Data Received!")
    else:
        print(f"Error Code: {ts_update.status_code}")

    # Print ThngSpeak response to console
    # ts_update.text is the thingspeak data entry number in the channel
    print(f" ThingSpeak Channel Entry: {ts_update.text}")


# If a standalone program, call the main function
# Else, use as a module
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # Unconfigure the sensors, disable the motors,
        # and restore the LED to the control of the GoPiGo3 firmware
        gpg.reset_all()
        sys.exit(0)
