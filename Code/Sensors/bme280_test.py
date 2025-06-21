#!/usr/bin/env python3
# Name: bme280_sensor_test.py
# Purpose: Read temperature, humidity and barometric pressure
# ------------------------------------------------
# History
# ------------------------------------------------
# Author    Date        Comments
# Loring    10/24/21    Changed to fahrenheit, convert pressure to inHg,
#                       compensate for altitude

# Barometric pressure compensation for altitude:
# https://www.engineeringtoolbox.com/barometers-elevation-compensation-d_1812.html
#
# DI sensor documentation: https://di-sensors.readthedocs.io/en/latest
# BME280 Temperature Humidity Pressure Sensor
#
# !Connect to I2C bus
#
###################################################################################

from time import sleep
# EasyTHPSensor rounds data to 0 decimal for temp and humidty
from di_sensors.easy_temp_hum_press import EasyTHPSensor
from easygopigo3 import EasyGoPiGo3  # Import GoPiGo3 library

# Create an instance of the GoPiGo3 class
gpg = EasyGoPiGo3()

print("Example program for reading BME280")
print("Temperature Humidity Pressure Sensor on an I2C port.")

# Initialize an EasyTHPSensor object
my_thp = EasyTHPSensor()

try:
    while True:
        # Read temperature
        # temp = my_thp.safe_celsius()
        temperature = my_thp.safe_fahrenheit()

        # Read relative humidity
        humidity = my_thp.safe_humidity()

        # Read pressure in pascals
        pressure = my_thp.safe_pressure()

        # Convert pascals to inHg, compensate for 4000' altitude
        pressure = (pressure / 3386.38867) + 4.08

        # Print values to the console
        print(f"Temperature: {temperature:3.0f}°F | Humidity: {humidity:3.0f}% | Pressure: {pressure:3.2f} inHg")

        # Pause between readings
        sleep(5)

# Except the program gets interrupted by Ctrl+C on the keyboard.
except KeyboardInterrupt:
    # Unconfigure the sensors, disable the motors,
    # and restore the LED to the control of the GoPiGo3 firmware
    gpg.reset_all()

