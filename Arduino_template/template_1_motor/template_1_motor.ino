#include <ArduinoBLE.h>  

// BLE Service handling communication with computer
BLEService seeedService("13012F00-F8C3-4F4A-A8F4-15CD926DA146"); // BLE Service

// BLE Characteristics - custom 128-bit UUID, read and writable by central device
BLEByteCharacteristic val0_char("13012F03-F8C3-4F4A-A8F4-15CD926DA146", BLEWriteWithoutResponse | BLERead);
BLEByteCharacteristic val1_char("14012F03-F8C3-4F4A-A8F4-15CD926DA146", BLEWriteWithoutResponse | BLERead);
// ...
BLEByteCharacteristic valN_char("15012F03-F8C3-4F4A-A8F4-15CD926DA146", BLEWriteWithoutResponse | BLERead);

// Variable to store datas
uint8_t val0 = 0;
uint8_t val1 = 0;
// ...
uint8_t valN = 0;

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
    BLE.setLocalName("LIS0");
    BLE.setAdvertisedService(seeedService);
    
    // Add characteristics to the service
    seeedService.addCharacteristic(val0_char);
    seeedService.addCharacteristic(val1_char);
    // ...
    seeedService.addCharacteristic(valN_char);

    // Add service
    BLE.addService(seeedService);

    // set the initial value to 0
    val0_char.writeValue(0);
    val1_char.writeValue(0);
    // ...
    valN_char.writeValue(0);

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
            if (val0_char.written()) {
                val0 = val0_char.value();
            }

            if (val1_char.written()) {
                val1 = val0_char.value();
            }
            
            // ...

            if (valN_char.written()) {
                valN = val0_char.value();
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
