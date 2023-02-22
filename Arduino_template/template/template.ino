#include <ArduinoBLE.h>  

BLEService seeedService("13012F00-F8C3-4F4A-A8F4-15CD926DA146"); // BLE Service

// BLE Characteristics - custom 128-bit UUID, read and writable by central device
BLEByteCharacteristic valChar("13012F03-F8C3-4F4A-A8F4-15CD926DA146", BLEWriteWithoutResponse | BLERead);

void setup() {
    Serial.begin(9600);
 
    // begin initialization
    if (!BLE.begin()) {
        Serial.println("STARTING BLE FAILED!");
        while (1);
    }

    // set advertised local name and service UUID:
    //BLE.setLocalName("Seeed XIAO nRF58240 BLE");
    BLE.setLocalName("LIS0");
    BLE.setAdvertisedService(seeedService);
    seeedService.addCharacteristic(valChar);

    // add service
    BLE.addService(seeedService);

    // set the initial value to 0:
    valChar.writeValue(0);

    // start advertising
    BLE.advertise();
    delay(100);
    Serial.println("#---------- Start Advertising -----------#");
}

void loop() {
    // listen for BLE centrals to connect:
    BLEDevice central = BLE.central();

    // if a central is connected to peripheral:
    if (central) {
        Serial.print("Connected to central: ");
        // print the central's MAC address:
        Serial.println(central.address());

        // while the central is still connected to peripheral:
        while (central.connected()) {   
            // Check if a value has been written on the characteristic "valChar"       
            if (valChar.written()) {
                Serial.println(valChar.value());
            }


            /***********************************************
            *
            *   YOUR CODE HERE WITH BLE CONNECTION
            *
            ***********************************************/


            delay(10); // Can be increased
        }

        central.disconnect();
        // when the central disconnects, print it out:
        Serial.print(F("Disconnected from central: "));
        Serial.println(central.address());
    } 

    /***********************************************
    *
    *   YOUR CODE HERE WITHOUT BLE CONNECTION
    *
    ***********************************************/

}
