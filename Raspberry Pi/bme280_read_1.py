#!/usr/bin/env python3
"""
    Name: bme280_read_1.py
    Purpose: Use Pimoroni library to read
    temperature, pressure, and humidity from Bosch bme280 sensor
    !Connect to I2C bus
    Press Ctrl+C to exit
"""
from time import sleep
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

# sudo pip3 install pimoroni-bme280
from bme280 import BME280

# Initialize the BME280 sensor
bus = SMBus(1)
sensor = BME280(i2c_dev=bus)

print("BME280 Read temperature, pressure, and humidity")
print("Ctrl+C to exit!")

while True:
    # Temperature in celsius
    print(sensor.get_temperature())

    # Barometric ressure in hPa (hectopascal)
    print(sensor.get_pressure())

    # Relative humidity in %
    print(sensor.get_humidity())

    sleep(1)



