# LIS-Raven

# 1.0) Main Features
This repository provides a GUI (Python - Tkinter) to manage Bluetooth Low-Energy Communication between a computer and a vehicle programmed using Arduino. The GUI enables to create and save specific configurations and directly generate Arduino code that handles the BLE communication for the configuration's motors and parameters. It can also display accelerometer and gyroscope values for Arduino board that contain a LSM6DS3 IMU. When the GUI is launched, the following window appears :

![GUI_current](https://user-images.githubusercontent.com/78551150/221360210-f3093f3c-de08-47b3-9cea-7bf30539ac4f.png)

which contains several frames :

## 1.1) Select Configuration
A configuration is a set of motors and parameters and their associated [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) address. It is recommended to use the GUI to create configuration since it will automatically uses valid UUID identifier. Nevertheless, it is also possible to create it in a .txt file with the same convention as the examples provided in the [configurations](configurations) folder.

## 1.2) Parameters to Send

## 1.3) Measurements

## 1.4) Inertial Measurement Unit

## 1.5) Motor Control

## 1.6) Automatic Code Generation

# 2.0) Installation
## 2.1) Dependencies
The code has been tested on Windows 10 using Python 3.9 and has the following dependencies :
- [tkinter](https://docs.python.org/3/library/tkinter.html)
- [numpy](https://pypi.org/project/numpy/)
- [bleak](https://pypi.org/project/bleak/)
- [os](https://docs.python.org/3/library/os.html)
- [asyncio](https://docs.python.org/3/library/asyncio.html)
- [uuid](https://docs.python.org/3/library/uuid.html)
- [threading](https://docs.python.org/3/library/threading.html)

To install all, uses ```pip install -requirements.txt```

## 2.2) Using virtual environment

Then, to launch the GUI open ```LIS-Raven.py``` and click on ```Run->Run Module```.

## 2.3) Using executable

Then, simply run ```LIS-Raven.exe``` to launch the GUI.
