# LIS-Raven


# 1.0) Main Features
This repository provides a GUI (Python - Tkinter) to manage Bluetooth Low-Energy Communication between a computer and a vehicle programmed using Arduino. The GUI enables to create and save specific configurations and directly generate Arduino code that handles the BLE communication for the configuration's motors and parameters. It can also display accelerometer and gyroscope values for Arduino board that contain a LSM6DS3 IMU. When the GUI is launched, the following window appears :

![GUI_current](https://user-images.githubusercontent.com/78551150/221360210-f3093f3c-de08-47b3-9cea-7bf30539ac4f.png)

which contains several frames :

## 1.1) Select Configuration
A configuration is a set of motors and parameters and their associated [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) address. The GUI allows to send values in Bluetooth to each parameter and motor. For example, you may have a configuration with 2 Servos (left & right wings) and 2 parameters (gains Kp, Ki of a PI controller). Using such a configuration will allow to send values to each Servo (target angular position for example) and modify each gain remotely. It is recommended to use the GUI to create configuration since it will automatically uses valid UUID identifier. Nevertheless, it is also possible to create it in a .txt file with the same convention as the examples provided in the [configurations](configurations) folder. Note that you must select the desired configuration and click on the "Set Configuration" button to effectively use it. A configuration can also be deleted from the tree by selecting its title and clicking on the "Delete" button.

## 1.2) Parameters to Send
This frame allows tu add up to 5 parameters to a configuration. Each parameter is added using the green "+" button. For each of them, user needs to specify the name of the parameter while the uuid is automatically generated (but can be modified by the user). When you're done, a button with the name of the parameter on it and an entry appear. To send values, just fill in the entry with an 8-bits unsigned integer and click on the button.

************************ IMPORTANT : VALUES CAN ONLY BE UNSIGNED 8-BITS INTEGER, i.e. VALUES IN [0 ; 255] *************************

## 1.3) Measurements
This frame is left unused in this version but may be used latter to display onboard measurements from the vehicle.

## 1.4) Inertial Measurement Unit
For Arduino board with a LSM6DS3 IMU, this frame provide a visualization of accelerometer and gyroscope datas. To enable it, check the button "Use IMU". Then the IMU datas can be updated using the "Update" button (GUI is not automatically refreshing it). The "Offset" button can be used to set the current posiiton as the reference for the IMU. It has its own characteristic which is 1 when the "Offset" button is pressed and 0 otherwise. In the auto-generated Arduino code, this value is simply read but not used. The way of setting the actual position as reference is left free to the user.

## 1.5) Motor Control
This frame provides a way to send values to the motors of your current configuration. Motors can be selected using the combo box and new motors can be added to the current configuration with the green "+" button. Again, the user must provide a name, and an automatically generated uuid can be directly used or modified. User needs also to provide the type of actuator : "sma" (Shape Memory Alloy), "bdc" (Brushless DC) or "servo". Nevertheless, in this version the type is just used for organization purpose but all the actuator are treated the same in the code. The disctinction may be useful for further improvements of the interface. 
The value to send to the selected motor is adjustable using the scale which goes from 0 to 255. To send the value, click on the "Set Motor Command : *val* [-]" button.

## 1.6) Automatic Code Generation
The GUI is able to generate Arduino code skeleton that already handles Bluetooth communication for each component of a configuration. It also handles IMU communication if you check the "use IMU" button (Inertial Measurement Unit frame) when you generate the code. To generate the code, go to ```File -> Generate code```. It will create an Arduino code with the name of the current configuration and put it into a folder with the same name (structure required by Arduino IDLE).

# 2.0) Installation
## 2.1) Dependencies
The code has been tested on Windows 10 using Python 3.9 and has the following dependencies :
- [numpy](https://pypi.org/project/numpy/)
- [bleak](https://pypi.org/project/bleak/)
- [uuid](https://docs.python.org/3/library/uuid.html)

To install all, use ```pip install -r -requirements.txt```

## 2.2) Using virtual environment

Create a new virtual environment, for example using venv : ```python -m venv myenv```.
Activate you environment, for example in a Windows command prompt : ```cd myenv/Scripts && activate.bat```.
Then install the dependencies within your virtual environment using the ```requirements.txt``` file in the LIS-Raven folder : ```pip install -r requirements.txt```. This will install the numpy, bleak and uuid libraries.

Then, to launch the GUI simply run ```LIS-Raven.py``` from the LIS-Raven folder in the command prompt. 
