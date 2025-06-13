#!/usr/bin/env -S python3
from os import system
from os import name
from time import sleep
from gpiozero import CPUTemperature


while True:
    # Use 'cls' for Windows and 'clear' for Linux/Mac
    system("cls" if name == "nt" else "clear")
    temp = CPUTemperature()
    cpu_temp = round(temp.temperature, 1)

    print("-----------------------------------------")
    print(f"CPU Temperature: {cpu_temp}°C")

    sleep(2)
