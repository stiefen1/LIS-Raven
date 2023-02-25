# LIS-Raven

# Main Features
This repository provides a GUI (Python - Tkinter) to manage Bluetooth Low-Energy Communication between a computer and a vehicle programmed using Arduino. The GUI enables to create and save specific configurations and directly generate Arduino code that handles the BLE communication for the configuration's motors and parameters. It can also display accelerometer and gyroscope values for Arduino board that contain a LSM6DS3 IMU.

# But what is a configuration ?
A configuration is a set of motors and parameters and their associated [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) address. It is recommended to use the GUI to create configuration since it will automatically uses valid UUID identifier. Nevertheless, it is also possible to create it in a .txt file with the same convention as the examples provided in the [configurations]() folder.
 
