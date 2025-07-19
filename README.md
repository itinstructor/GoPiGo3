# GoPiGo3 & Raspberry Pi Projects

![GoPiGo3](./img/GoPiGo3.jpg)

My GoPiGo3 with all its modifications.

## History

- 01/10/25 Update GoPiGo3_Code\Remote_Control to a better development sequence

## GoPiGo3 Code

- `ps4_gopigo_pygame.py` --> Remote control with wireless PS4 game controller to Pi Bluetooth. PyGame is used as the library for GoPiGo3 remote control.
- `rc_gui_ps4_bme280.py` --> Uses `ps4_gopigo.py` as a module to run the joystick with GUI and BME280. Screenshot below.
- `obstacle_scanner.py` --> Tkinter visualization of area using distance sensor.
- `radar_rich.py` --> ASCII visualization of area using distance sensor and Python Rich library.
- `radar_cli.py` --> ASCII visualization of area using distance sensor.
- `rc_tkinter_bme280.py` --> Tkinter remote control with BME280 sensor readings.
- `bme280_test.py`
- `bme280_thingspeak.py` --> Upload Temperature, Humidity, and Barometric pressure to ThingSpeak.com.
- `video_pi.py` --> Video streaming using Picam2 for Raspberry Pi Bullseye and Bookworm. Using the new libcamera2 camera stack.

![GoPiGo3 Remote Control](./img/GoPiGo3Remote.png)

### Obstacle Scanner

![Obstacle Scanner](./img/ObstacleScanner.png)

## Documentation

- **Threading folder** contains a threading tutorial and example code. Threads allow the robot to do many tasks at a time.
- **GoPiGo3 Pi Getting Started Bullseye Tutorial**
- **GoPiGo3 Getting Started Buster Tutorial**
- **GoPiGo3 Cloud Data with ThingSpeak Tutorial** --> Upload sensor data to [ThingSpeak.com](https://www.thingspeak.com).
  - Go to [billthecomputerguy.com/gopigo](https://www.billthecomputerguy.com/gopigo) for example readings.
- **GoPiGo3 Sensors Tutorial**
- **GoPiGo Tutorials**
- **Raspberry Pi Getting Started Bullseye and Bookworm Tutorial**
- **Raspberry Pi Sensors**

## Projects

- **OfficeCannon** --> The GoPiGo3 launches soft missiles with Dream Cheeky Thunder.

## Credit

- `setup_gopigo3_on_32-bit_Bullseye.sh` is from [slowrunner](https://github.com/slowrunner) --> This shell script sets up the GoPiGo3 drivers for Bullseye 32 or 64 bit.

## Purpose

I am an Information Technology Instructor at Western Nebraska Community College. I teach Information Technology Technical Support, CyberSecurity, and Computer Science.

This repository is for my personal projects and resources with the Raspberry Pi-based Modular Robotics GoPiGo3.

WNCC NASA GoPiGo3 projects are located at [https://github.com/itinstructor/WNCCNASA](https://github.com/itinstructor/WNCCNASA).

- **Facebook**: [Facebook WNCC IT Program](https://www.facebook.com/wnccitprogram/)
- **YouTube**: [YouTube WNCC IT Program](https://www.youtube.com/@williamloringitinstructor)

## License

[![Creative Commons License](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)  
This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).

Copyright (c) 2025 William A Loring
