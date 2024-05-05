#!/usr/bin/env python3
"""
    Name: gps_api_demo.py
    Author: William Loring
    Created: 10-11-2023
    Purpose: Get GPS info from Grove GPS air350 without battery or USB GPS
    https://wiki.seeedstudio.com/Grove-GPS-Air530
    https://gps-api.readthedocs.io/en/latest/modules.html 
"""
import sys
# Use custom gps_api library folder
# sudo pip3 install haversine
# sudo pip3 install pynmea2
import gps_api

METERS_TO_FEET = 3.28084

# Use ls /dev/tty* to find serial gps port
# port_name = ('/dev/ttyAMA0')
port_name = ('/dev/ttyACM0')
# Instantiate the GPS object with the port name on your device
# to which the GPS module is connected
GPS = gps_api.GPS(port_name)
counter = 1

while True:
    try:
        print(f" Read GPS: {counter}")
        # Get altitude in meters
        altitude_meters = GPS.get_altitude()
        # Convert altitude_meters to feet
        altitude_feet = altitude_meters * METERS_TO_FEET

        # Get separate lat and lon current location
        latitude = GPS.get_latitude()
        longitude = GPS.get_longitude()

        # Get combined lat and lon current location
        location = GPS.get_current_location()

        # Get number of sats
        sats = GPS.get_num_sats()

        print(f" Altitude: {altitude_feet:,.0f} ft ({altitude_meters:,.0f} m)")
        print(f"      Lat: {latitude}")
        print(f"      Lng: {longitude}")
        print(f" {location}")
        print(f"     Sats: {sats}")
        counter += 1

    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(f"Error reading GPS data: {e}")
