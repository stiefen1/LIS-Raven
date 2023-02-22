#include <ArduinoBLE.h>  

// BLE Service handling communication with computer
BLEService seeedService("13012F00-F8C3-4F4A-A8F4-15CD926DA146");

// *BLE Characteristics*
BLEByteCharacteristic maxAngle_char("8d0d9a5b-fbcb-48c2-8ddd-d864165eeb8b", BLEWriteWithoutResponse | BLERead);
BLEByteCharacteristic minAngle_char("026fe7a8-7de9-42be-9be1-9894ae9ab9ae", BLEWriteWithoutResponse | BLERead);
BLEByteCharacteristic average_val_char("7193b40e-9b15-4f3a-8291-a31b121852d5", BLEWriteWithoutResponse | BLERead);
BLEByteCharacteristic servo_left_char("1acf536f-60e5-481e-9220-fa0dde2a42ec", BLEWriteWithoutResponse | BLERead);
BLEByteCharacteristic bdc_middle_char("8b9032e6-48dc-41b0-857c-83c20cc461a5", BLEWriteWithoutResponse | BLERead);
BLEByteCharacteristic bdc_tail_char("6a01dd81-7a2d-4323-b6a9-134863dfe7dc", BLEWriteWithoutResponse | BLERead);

// *Declare variables to store datas*
uint8_t maxAngle = 0;
uint8_t minAngle = 0;
uint8_t average_val = 0;
uint8_t servo_left = 0;
uint8_t bdc_middle = 0;
uint8_t bdc_tail = 0;

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
    BLE.setLocalName("hybrid");
    BLE.setAdvertisedService(seeedService);
    
    // *Add characteristics to the service*
    seeedService.addCharacteristic(maxAngle_char);
    seeedService.addCharacteristic(minAngle_char);
    seeedService.addCharacteristic(average_val_char);
    seeedService.addCharacteristic(servo_left_char);
    seeedService.addCharacteristic(bdc_middle_char);
    seeedService.addCharacteristic(bdc_tail_char);

    // Add service
    BLE.addService(seeedService);

    // set the initial value to 0
    maxAngle_char.writeValue(0);
    minAngle_char.writeValue(0);
    average_val_char.writeValue(0);
    servo_left_char.writeValue(0);
    bdc_middle_char.writeValue(0);
    bdc_tail_char.writeValue(0);

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
            if(maxAngle_char.written()){
                maxAngle = maxAngle_char.value();
            }
            if(minAngle_char.written()){
                minAngle = minAngle_char.value();
            }
            if(average_val_char.written()){
                average_val = average_val_char.value();
            }
            if(servo_left_char.written()){
                servo_left = servo_left_char.value();
            }
            if(bdc_middle_char.written()){
                bdc_middle = bdc_middle_char.value();
            }
            if(bdc_tail_char.written()){
                bdc_tail = bdc_tail_char.value();
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