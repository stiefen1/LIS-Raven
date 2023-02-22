#include <ArduinoBLE.h>  

// BLE Service handling communication with computer
BLEService seeedService("13012F00-F8C3-4F4A-A8F4-15CD926DA146");

// *BLE Characteristics*
BLEByteCharacteristic kp_char("c4832", BLEWriteWithoutResponse | BLERead);
BLEByteCharacteristic ki_char("d9287c", BLEWriteWithoutResponse | BLERead);
BLEByteCharacteristic kd_char("t0019", BLEWriteWithoutResponse | BLERead);
BLEByteCharacteristic motor1_char("a3456", BLEWriteWithoutResponse | BLERead);
BLEByteCharacteristic motor2_char("b737", BLEWriteWithoutResponse | BLERead);

// *Declare variables to store datas*
uint8_t kp = 0;
uint8_t ki = 0;
uint8_t kd = 0;
uint8_t motor1 = 0;
uint8_t motor2 = 0;

///////////////////////////////////////////////////A\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

/*******************************************************************************\
*                                                                               *
*                                                                               *
*                                                                               *
*                     YOUR CODE HERE FOR GLOBAL VARIABLES                       *
*                                                                               *
*                                                                               *
*                                                                               *
\*******************************************************************************/

///////////////////////////////////////////////////A\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

void setup() {
    Serial.begin(9600);
 
    // begin initialization
    if (!BLE.begin()) {
        Serial.println("STARTING BLE FAILED!");
        while (1);
    }

    // *Set advertised local name and service UUID*
    BLE.setLocalName("Quadcopter");
    BLE.setAdvertisedService(seeedService);
    
    // *Add characteristics to the service*
    seeedService.addCharacteristic(kp_char);
    seeedService.addCharacteristic(ki_char);
    seeedService.addCharacteristic(kd_char);
    seeedService.addCharacteristic(motor1_char);
    seeedService.addCharacteristic(motor2_char);

    // Add service
    BLE.addService(seeedService);

    // set the initial value to 0
    kp_char.writeValue(0);
    ki_char.writeValue(0);
    kd_char.writeValue(0);
    motor1_char.writeValue(0);
    motor2_char.writeValue(0);

///////////////////////////////////////////////////B\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    /*******************************************************************************\
    *                                                                               *
    *                                                                               *
    *                                                                               *
    *                            YOUR CODE HERE FOR SETUP                           *
    *                                                                               *
    *                                                                               *
    *                                                                               *
    \*******************************************************************************/

///////////////////////////////////////////////////B\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    // start advertising
    BLE.advertise();
    delay(100);
    Serial.println("#---------- Start Advertising -----------#");
}

void loop() {
    BLEDevice central = BLE.central();
    if (central) {
        while (central.connected()) {
	    // *Read values*
            if(kp_char.written()){
                kp = kp_char.value();
            }
            if(ki_char.written()){
                ki = ki_char.value();
            }
            if(kd_char.written()){
                kd = kd_char.value();
            }
            if(motor1_char.written()){
                motor1 = motor1_char.value();
            }
            if(motor2_char.written()){
                motor2 = motor2_char.value();
            }
           
///////////////////////////////////////////////////C\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

            /*******************************************************************************\
            *                                                                               *
            *                                                                               *
            *                                                                               *
            *                     YOUR CODE HERE WITH BLE CONNECTION                        *
            *                                                                               *
            *                                                                               *
            *                                                                               *
            \*******************************************************************************/

///////////////////////////////////////////////////C\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

            delay(100); // Can be modified
        }
        central.disconnect(); // Disconnect from peripheral
    } 

///////////////////////////////////////////////////D\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    /*******************************************************************************\
    *                                                                               *
    *                                                                               *
    *                                                                               *
    *                     YOUR CODE HERE WITHOUT BLE CONNECTION                     *
    *                                                                               *
    *                                                                               *
    *                                                                               *
    \*******************************************************************************/

///////////////////////////////////////////////////D\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    delay(100); // Can be modified
}