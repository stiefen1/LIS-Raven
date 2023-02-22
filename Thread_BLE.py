from threading import Thread
import asyncio
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
            "motorVal":'13012F03-F8C3-4700-A8F4-15CD926DA146',
            "motorSel":'13012F03-F8C3-4701-A8F4-15CD926DA146',
            "aX":'6b64b0c4-b675-4720-a02a-d7f6b02ae9db',
            "aY":'6b64b0c4-b675-4721-a02a-d7f6b02ae9db',
            "aZ":'6b64b0c4-b675-4722-a02a-d7f6b02ae9db',
            "gX":'6b64b0c4-b675-4723-a02a-d7f6b02ae9db',
            "gY":'6b64b0c4-b675-4724-a02a-d7f6b02ae9db',
            "gZ":'6b64b0c4-b675-4725-a02a-d7f6b02ae9db',
            "setZero":'6b64b0c4-b675-4726-a02a-d7f6b02ae9db',
            "temperature":'aa06d7d0-3496-4868-8990-faccf1581d40'}

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
            #print("wait2discover")
            await asyncio.sleep(0.5)

    #------------------------------------------------------------#

    async def wait2Connect(self):
        while not(self.ask2Connect):
            #print("wait2connect")
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
                                    print("com")
                                    await self.communicate()
                                    print("com fin")

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

                acc[0] = int.from_bytes(acc[0], "little")/100 - 1000
                acc[1] = int.from_bytes(acc[1], "little")/100 - 1000
                acc[2] = int.from_bytes(acc[2], "little")/100 - 1000

                gyro[0] = int.from_bytes(gyro[0], "little")/100 - 1000
                gyro[1] = int.from_bytes(gyro[1], "little")/100 - 1000
                gyro[2] = int.from_bytes(gyro[2], "little")/100 - 1000

                self.imu._set_acc(np.array(acc))
                self.imu._set_gyro(np.array(gyro))

                # Check for an offset request
                if(self.imu.setZero_request):
                    print("send setZero request")
                    await self.client.write_gatt_char(self._uuid["setZero"], bytearray([1]))
                    self.imu.setZero_request = 0
            except:
                print("IMU ERROR")

        #---------------- MOTORS ----------------#    

        # Check if there is a position or min/max request
        # temporary variable that will select the right value to send into the motor selection characteristic

##        sel = 0
##        val = None
##        for i, m in enumerate(self.motors):
##            sel = i
##            if self.motors[m].setMin_request == True:
##                self.motors[m].setMin_request = False
##                sel += 0
##                val = self.motors[m].minPos
##                break
##
##            elif self.motors[m].setCommand_request == True:
##                self.motors[m].setCommand_request = False
##                sel += len(self.motors)
##                val = self.motors[m].pos
##                break
##
##            elif self.motors[m].setMax_request == True:
##                self.motors[m].setMax_request = False
##                sel += 2 * len(self.motors)
##                val = self.motors[m].maxPos
##                break

        val = None
        for key in self.motors:
            if self.motors[key].setCommand_request == True:
                self.motors[key].setCommand_request = False
                val = self.motors[key].pos
                
        # Check if there was at least one request       
        if(val is not None):
            # await self.client.write_gatt_char(self._uuid["motorVal"], bytearray([int(val)])) # Delete floating part
            # await self.client.write_gatt_char(self._uuid["motorSel"], bytearray([sel]))
            
            val = min([255, max([int(val), 0])]) # Clip value between 0 and 255
            await self.client.write_gatt_char(self._uuid[self.selected_motor_name], bytearray([val]))

        #---------------- PARAMETERS ----------------#
        print(self.param_request)
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
        pass

    #------------------------------------------------------------#

    async def read(self):
        pass

    #------------------------------------------------------------#

    async def write(self):
        pass
