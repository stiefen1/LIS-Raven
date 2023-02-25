from threading import Thread
import asyncio, uuid
import numpy as np

from bleak import BleakClient
from bleak import BleakScanner
from bleak import discover

from utils import actuator, imu

######################################### BLE #########################################

class BLE(Thread):
    def __init__(self, motorList):
        #"""Class to handle Bluetooth Low-Energy communication
        #  Wrapper for the 'bleak' library"""
        super().__init__()
        
        self._uuid_init = {
            "aX":"a876301a-11e2-483f-bc99-25bc9c7ce520",
            "aY":"0c6515ab-8006-4690-a297-e26b0850177d",
            "aZ":"1765d425-20da-48ea-989e-7ef47112c4ca",
            "gX":"1341d52d-efa4-452d-86bf-53a91935caa8",
            "gY":"b9e209c5-465d-4d04-974c-78e625764859",
            "gZ":"3d2bd9c9-8df0-426d-9e84-e72db8b1341a",
            "setZero_IMU":"e7a836a1-350a-4f65-8a6c-d670d064914f"}

        self._uuid = self._uuid_init

        self.ask2Connect = False
        self.ask2Discover = False
        self.ask2Disconnect = False
        self.device2Connect = None
        self.connectedDevice = None
        self.detectedDevices = None
        self.useIMU = False

        self.param_request = {} # CONTAINS ONLY {"name": str, "value": int} of the current request
        self.imu = imu()
        self.motors = {}
        self.selected_motor_name = None

        asyncio.ensure_future(self.discoverLoop())
        asyncio.ensure_future(self.connectLoop())
        self.loop = asyncio.get_event_loop()

    #------------------------------------------------------------#        

    def run(self):
        self.loop.run_forever()

    #------------------------------------------------------------#

    async def wait2Discover(self):
        while not(self.ask2Discover):
            await asyncio.sleep(0.5)

    #------------------------------------------------------------#

    async def wait2Connect(self):
        while not(self.ask2Connect):
            await asyncio.sleep(0.5)
        self.ask2Connect = False

    #------------------------------------------------------------#
    
    async def discoverLoop(self):
        while True:
            # Wait for discover request
            await self.wait2Discover()
            print("START DISCOVERING")
            self.detectedDevices = await BleakScanner.discover()
            self.ask2Discover = False
            
    #------------------------------------------------------------#
                        
    async def connectLoop(self):
        while True:
            await self.wait2Connect()
            print("START CONNECTING")
            if self.device2Connect is None:
                print("CHOOSE A DEVICE TO CONNECT")
            else:
                for d in self.detectedDevices:
                    if d.name == self.device2Connect:
                        try:
                            print("Trying to connect")
                            async with BleakClient(d.address) as self.client:
                                self.connectedDevice = d.name
                                while not(self.ask2Disconnect):
                                    await self.communicate()

                                await self.client.disconnect()
                                self.ask2Disconnect = False

                        except:
                            self.connectedDevice = "Fail"
                            print(self.connectedDevice)
                                
                        print("PERIPHERAL IS NOW DISCONNECTED")

    #------------------------------------------------------------#

    async def communicate(self):
        #----------------- IMU -----------------#
        acc = [0., 0., 0.]
        gyro = [0., 0., 0.]

        if(self.useIMU):
            try:
                acc[0] = await self.client.read_gatt_char(self._uuid["aX"])
                acc[1] = await self.client.read_gatt_char(self._uuid["aY"])
                acc[2] = await self.client.read_gatt_char(self._uuid["aZ"])

                gyro[0] = await self.client.read_gatt_char(self._uuid["gX"])
                gyro[1] = await self.client.read_gatt_char(self._uuid["gY"])
                gyro[2] = await self.client.read_gatt_char(self._uuid["gZ"])

                acc[0] = int.from_bytes(acc[0], "little")
                acc[1] = int.from_bytes(acc[1], "little")
                acc[2] = int.from_bytes(acc[2], "little")

                gyro[0] = int.from_bytes(gyro[0], "little")
                gyro[1] = int.from_bytes(gyro[1], "little")
                gyro[2] = int.from_bytes(gyro[2], "little")

                self.imu._set_acc(np.array(acc))
                self.imu._set_gyro(np.array(gyro))

                # Check for an offset request
                if(self.imu.setZero_request):
                    print("send setZero request")
                    await self.client.write_gatt_char(self._uuid["setZero_IMU"], bytearray([1]))
                    self.imu.setZero_request = 0
            except:
                print("IMU ERROR")

        #---------------- MOTORS ----------------#    

        # Check if there is a position or min/max request
        val = None
        for key in self.motors:
            if self.motors[key].setCommand_request == True:
                self.motors[key].setCommand_request = False
                val = self.motors[key].pos
                
        # Check if there was at least one request       
        if(val is not None):
            val = min([255, max([int(val), 0])]) # Clip value between 0 and 255
            await self.client.write_gatt_char(self._uuid[self.selected_motor_name], bytearray([val]))

        #---------------- PARAMETERS ----------------#

        if len(self.param_request) >= 2:
            try:
                val = min([255, max([int(self.param_request['value']), 0])])
                paramName = self.param_request['name'] # Get the name of the parameter to send
                await self.client.write_gatt_char(self._uuid[paramName], bytearray([val])) # Send a value to a specific uuid
            except:
                pass

            self.param_request = {}

    #------------------------------------------------------------#

    def connect(self, deviceName=None):
        self.device2Connect = deviceName
        self.ask2Connect = True

    #------------------------------------------------------------#

    def discover(self):
        self.ask2Discover = True

    #------------------------------------------------------------#

    def disconnect(self):
        self.connectedDevice = None
        self.ask2Disconnect = True
