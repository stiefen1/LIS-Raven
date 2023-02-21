import numpy as np

# ALL UNITS ARE METRICS & ANGLE IN RADIANS & SPEED IN RPM

######################################### ACTUATOR #########################################

class actuator:
    def __init__(self, model='servo', minPos=0, maxPos=180, maxRpm=1):
        """Class to describe an actuator (Servo, BDC, ..)"""
        self.model = model # servo, bdc
        self.minPos = minPos # rad
        self.maxPos = maxPos # rad
        self.maxRpm = maxRpm # tr/min
        self.pos = None
        self.rpm = None
        
        self.setCommand_request = False
        self.setMax_request = False
        self.setMin_request = False

    #------------------------------------------------------------#

    def get_pos(self):
        return self.pos

    #------------------------------------------------------------#

    def get_rpm(self):
        return self.rpm

    #------------------------------------------------------------#

    def _set_pos(self, pos):
        self.pos = pos

    #------------------------------------------------------------#

    def _set_rpm(self, rpm):
        self.rpm = rpm
        
######################################### IMU #########################################

class imu:
    def __init__(self, acc_offset=np.array([0.,0.,0.]), acc_scale=1, gyro_scale=1):
        """Class to describe an Inertial Measurement Unit
           --> Normalization in 'set' functions"""
        self.__acc = np.array([0., 0., 0.])
        self.__gyro = np.array([0., 0., 0.])
        self.offset = {"acc":acc_offset,
                       "gyro":np.array([0., 0., 0.])}
        self.acc_scale = acc_scale
        self.gyro_scale = gyro_scale
        self.setZero_request = False

    #------------------------------------------------------------#

    def get_acc(self):
        return self.__acc

    #------------------------------------------------------------#

    def get_gyro(self):
        return self.__gyro

    #------------------------------------------------------------#

    def _set_acc(self, acc):
        self.__acc = self.acc_scale * (acc  - self.offset["acc"])

    #------------------------------------------------------------#

    def _set_gyro(self, gyro):
        self.__gyro = self.gyro_scale * (gyro - self.offset["gyro"])

    #------------------------------------------------------------#

    def _set_offset(self):
        self.offset["acc"] = self.__acc
        self.offset["gyro"] = self.__gyro

########################### READ AND WRITE CONFIGURATION #######################

#from tkinter.filedialog import askopenfilename
#filename = askopenfilename()

class configuration:
    def __init__(self):
        self.name = "default"
        self.data = {"param":[], "servo":[], "bdc":[]}
        self.uuid = {"param":[], "servo":[], "bdc":[]}
        self.treeData = None

    def get_treeData(self):
        self.treeData = [("", 1, self.name, "")]
        i=1
        for key in self.data:
            for obj in self.data[key]:
                i=i+1
                self.treeData.append((1, i, obj, key))
                

def read_config_file(filename):
    config = configuration()

    # Get the filename as "name.txt"
    with open(filename) as file:
        # Get name of the configuration : for example "Quadcopter"
        name = file.readline()
        config.name = name.partition("\n")[0]
    
        for line in file.readlines():
            line = line.partition("\n")[0] # Remove '\n' character
        
            if line[0:1] == '\t':
                # This line is an attribute to last object
                line = line[1::].partition("\t") # remove first "\t" and separate name from uuid
                config.data[temp_class].append(line[0])
                config.uuid[temp_class].append(line[2])
            else:
                # This is a new object
                config.data.update({line:[]})
                config.uuid.update({line:[]})
                temp_class = line

    return config

def write_config_file(config):
    """ name [str] : Name of the configuration
        config [dict(list)] : Configuration architecture"""
    while(config.name[-4::] == '.txt'):
        config.name = config.name[0:-4]
    with open(config.name + '.txt', 'w') as file:
        file.write(config.name + "\n")
        for key in config.data:
            file.write(key + "\n")
            for obj, uuid in zip(config.data[key], config.uuid[key]):
                file.write("\t" + obj + "\t" + uuid + "\n")








    
