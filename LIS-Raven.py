# -*- coding: utf-8 -*-

# RESTE A FAIRE :
#       - METTRE POP-UP D'ERREUR QUAND ON EST PAS CONNECTE AU BLUETOOTH

from threading import Thread
import asyncio, os, uuid
import tkinter as tk
from tkinter import ttk, END, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.font import Font
from Thread_BLE import*
from utils import*

MOTORS_TYPE = ["servo", "bdc", "sma"]

######################################## GUI #########################################

class GUI:
    def __init__(self):
        #"""Class to describe the Graphical User Interface"""
        self.motorList = []
        self.motorSel = None
        self.scaleValue = None
        self.currentConfig = configuration()
        self.configList = [self.currentConfig]
        
        self._init_mainWindow()

        self.ThreadBLE = BLE(self.motorList)
        self.ThreadBLE.start()
        self.show()
        
    #------------------------------------------------------------#

    def _init_mainWindow(self):
        style = 'light'
        
        self.mainWindow = tk.Tk()
        self.mainWindow.option_add("*tearOff", False)
        self.mainWindow.tk.call('source', 'Theme/Forest-ttk-theme-master/forest-' + style + '.tcl')
        ttk.Style().theme_use('forest-' + style)

        self.title_font = Font(
            family = 'Calibri',
            size = 14,
            weight = 'bold',
            slant = 'roman',
            underline = 0,
            overstrike = 0,
        )

        self.title_foreground = '#444777444'
     
        self.mainWindow.title("LIS-Raven")
        self.mainWindow.geometry("650x550")
        self.mainWindow.resizable(0,0)

        for i in range(5):
            self.mainWindow.rowconfigure(i, weight=1)
            for j in range(5):
                self.mainWindow.columnconfigure(j, weight=1)

        self._init_menubar()
        self._init_connectPopup()
        self._init_helpPopup()
        self._init_addParamPopup()
        self._init_addMotorPopup()
        self._init_frmTable()
        self._init_frmConfig()
        self._init_frmControl()

    #------------------------------------------------------------#

    def _init_connectPopup(self):
        self.connectWindow = tk.Toplevel()
        self.connectWindow.withdraw() # Hide
        self.connectWindow.title("Connexion")
        self.connectWindow.geometry("300x260")
        self.connectWindow.resizable(0,0)

        self.connectLabel = ttk.Label(self.connectWindow, text="Connexion with BLE Peripheral", anchor="center")
        self.connectLabel.pack(fill=tk.BOTH)

        self.discoverButton = ttk.Button(self.connectWindow, text="Discover", cursor="hand2", style='Accent.TButton', command=self._discover)
        self.discoverButton.pack(fill = tk.BOTH)

        self.connectScroll = ttk.Scrollbar(self.connectWindow)
        self.connectScroll.pack(side=tk.RIGHT, fill = tk.BOTH)
        
        self.connectList = tk.Listbox(self.connectWindow, yscrollcommand = self.connectScroll.set)
        self.connectList.pack(fill = tk.BOTH)
        self.connectScroll.config(command=self.connectList.yview)

        self.connectButton = ttk.Button(self.connectWindow, text="Connect", style='Accent.TButton', cursor="hand2", command=self._connect)
        self.connectButton.pack(fill=tk.BOTH)

    #------------------------------------------------------------#

    def _init_helpPopup(self):
        self.helpWindow = tk.Toplevel()
        self.helpWindow.withdraw() # Hide
        self.helpWindow.title("Help")
        self.helpWindow.geometry("300x200")
        self.helpWindow.resizable(0,0)

        self.helpLabel = ttk.Label(self.helpWindow, text="Je suis là pour aider", anchor="center").pack()

    #------------------------------------------------------------#

    def _init_addParamPopup(self):
        self.addParam_window = tk.Toplevel()
        self.addParam_window.withdraw() # Hide
        self.addParam_window.title("New Parameter")
        self.addParam_window.geometry("280x100")
        self.addParam_window.resizable(0,0)

        # Add frame
        self.addParam_frame = ttk.Frame(self.addParam_window, style='Card')

        # Add entry for uuid
        self.uuidParam_label = ttk.Label(self.addParam_frame, text="UUID : ", anchor="center").grid(column=0, row=0, sticky="nsew")
        self.uuidParam_entry = ttk.Entry(self.addParam_frame)
        self.uuidParam_entry.delete(0, END)
        self.uuidParam_entry.insert(0, str(uuid.uuid4()))
        self.uuidParam_entry.grid(column=1, row=0, columnspan=3, sticky="nsew")

        # Add entry for name
        self.paramName_label = ttk.Label(self.addParam_frame, text="Name : ", anchor="center").grid(column=0, row=1, sticky="nsew")
        self.paramName_entry = ttk.Entry(self.addParam_frame)
        self.paramName_entry.grid(column=1, row=1, columnspan=3, sticky="nsew")

        # Add button to validate
        self.paramValidate_button = ttk.Button(self.addParam_frame, text="Validate", cursor="hand2", style='Accent.TButton', command=self._set_new_param)
        self.paramValidate_button.grid(column=0, row=2, columnspan=4, sticky="nsew")

        for i in range(3):
            for j in range(3):
                self.addParam_frame.rowconfigure(i, weight=1)
                self.addParam_frame.columnconfigure(j, weight=1)

        self.addParam_frame.pack(fill=tk.BOTH, expand=True)

    #------------------------------------------------------------#

    def _init_addMotorPopup(self):
        self.addMotor_window = tk.Toplevel()
        self.addMotor_window.withdraw() # Hide
        self.addMotor_window.title("New Motor")
        self.addMotor_window.geometry("280x140")
        self.addMotor_window.resizable(0,0)

        # Add frame
        self.addMotor_frame = ttk.Frame(self.addMotor_window, style='Card')

        # Add entry for uuid
        self.uuidMotor_label = ttk.Label(self.addMotor_frame, text="UUID : ", anchor="center").grid(column=0, row=0, sticky="nsew")
        self.uuidMotor_entry = ttk.Entry(self.addMotor_frame)
        self.uuidMotor_entry.delete(0, END)
        self.uuidMotor_entry.insert(0, str(uuid.uuid4()))
        self.uuidMotor_entry.grid(column=1, row=0, columnspan=3, sticky="nsew")

        # Add entry for name
        self.motorName_label = ttk.Label(self.addMotor_frame, text="Name : ", anchor="center").grid(column=0, row=1, sticky="nsew")
        self.motorName_entry = ttk.Entry(self.addMotor_frame)
        self.motorName_entry.grid(column=1, row=1, columnspan=3, sticky="nsew")

        # Add combobox to select motor type
        self.motorType_label = ttk.Label(self.addMotor_frame, text="Type : ", anchor="center").grid(column=0, row=2, sticky="nsew")
        self.motorType_comboBox = ttk.Combobox(self.addMotor_frame, values=MOTORS_TYPE, cursor="hand2", style='TCombobox')
        self.motorType_comboBox.grid(column=1, row=2, columnspan=3, sticky="nsew")

        # Add button to validate
        self.motorValidate_button = ttk.Button(self.addMotor_frame, text="Validate", cursor="hand2", style='Accent.TButton', command=self._set_new_motor)
        self.motorValidate_button.grid(column=0, row=3, columnspan=4, sticky="nsew")

        for i in range(3):
            for j in range(3):
                self.addMotor_frame.rowconfigure(i, weight=1)
                self.addMotor_frame.columnconfigure(j, weight=1)

        self.addMotor_frame.pack(fill=tk.BOTH, expand=True)
    #------------------------------------------------------------#
    
    def _init_menubar(self):
        self.menubar = tk.Menu(self.mainWindow)
        self.fileMenu = tk.Menu(self.menubar)
        self.connexionMenu = tk.Menu(self.menubar)
        self.measureMenu = tk.Menu(self.menubar)
        self.helpMenu = tk.Menu(self.menubar)

        # File menu
        self.fileMenu.add_command(label="New config", command=self._create_new_config)
        self.fileMenu.add_command(label="Save config", command=self._save_config)
        self.fileMenu.add_command(label="Save config as.. ", command=self._save_config_as)
        self.fileMenu.add_command(label="Load config.. ", command=self._load_config)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Generate code", command=self._generate_arduino_code)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Quit", command=self.mainWindow.destroy)

        # Connexion menu
        self.connexionMenu.add_command(label="Disconnect", command=self._disconnect)
        self.connexionMenu.add_command(label="Connect.. ", command=self._show_connectPopup)

        # Measure menu
        self.measureMenu.add_command(label="Save as ..", command=self._save_measure_as)
        self.measureMenu.add_command(label="Save ..", command=self._save_measure)

        # Help menu
        self.helpMenu.add_command(label="?", command=self._show_helpPopup)

        # Create menu bar
        self.menubar.add_cascade(label="File", menu=self.fileMenu)
        self.menubar.add_cascade(label="Connexion", menu=self.connexionMenu)
        self.menubar.add_cascade(label="Measurement", menu=self.measureMenu)
        self.menubar.add_cascade(label="Help", menu=self.helpMenu)

        self.mainWindow.config(menu=self.menubar)

    #------------------------------------------------------------#

    def _init_frmTable(self):
        self.frmTable = ttk.LabelFrame(self.mainWindow, text=" Parameters to Send ", style='TLabelframe')

        # Dimensions of the table
        self.nb_params = 5 # H
        self.nb_args = 2 # W
        
        self.frmTable_button = []
        self.frmTable_entry = [[0 for x in range(self.nb_args)] for y in range(self.nb_params)]

        self.frmTable_button.append(ttk.Button(self.frmTable, text="+", cursor="hand2", style='Accent.TButton', command=self._show_addParamPopup))
        self.frmTable_button[-1].grid(row=0, column=0, rowspan=1, columnspan=1, padx=(10, 5), pady=2)

        for i in range(self.nb_params):
            self.frmTable.rowconfigure(i, weight=1)
            for j in range(self.nb_args):
                self.frmTable.columnconfigure(j, weight=1)
                if j >= 1 and i==0:
                    # Only places W-1 entries on the first line
                    self.frmTable_entry[i][j] = ttk.Entry(self.frmTable)
                    self.frmTable_entry[i][j].grid(row=i, column=j, rowspan=1, columnspan=1, padx=(5, 10), pady=2)     
                
        self.frmTable.grid(row=1, column=0, rowspan=4, columnspan=3, padx=(10, 0), pady=(0, 10), sticky="nsew")

    #------------------------------------------------------------#

    def _reset_params_table(self):
        self._init_frmTable()

    #------------------------------------------------------------#

    def _init_frmControl(self):
        self.frmControl = ttk.Frame(self.mainWindow)

        ########################################### Configuration Label ####################################################
        self.currentConfig_label = ttk.Label(self.frmControl, text = "Current configuration : ")

        ########################################### Top Frame ####################################################
        self.subfrmControlT = ttk.LabelFrame(self.frmControl, text=" Measurements ", style="TLabelframe")

        self.subfrmControlT.rowconfigure(0, weight=1)
        self.subfrmControlT.columnconfigure(0, weight=1)

        ######################################## Accelerometer Frame ####################################################
        self.subfrmControlM = ttk.LabelFrame(self.frmControl, style='TLabelframe', text=" Inertial Measurement Unit ")

        self.ax_labelControlM = ttk.Label(self.subfrmControlM, text="ax").grid(row=1, column=0)
        self.ay_labelControlM = ttk.Label(self.subfrmControlM, text="ay").grid(row=2, column=0)
        self.az_labelControlM = ttk.Label(self.subfrmControlM, text="az").grid(row=3, column=0)
        self.axval_labelControlM = ttk.Label(self.subfrmControlM, text=str(0.0))
        self.ayval_labelControlM = ttk.Label(self.subfrmControlM, text=str(0.0))
        self.azval_labelControlM = ttk.Label(self.subfrmControlM, text=str(-9.81))
        
        self.axval_labelControlM.grid(row=1, column=1)
        self.ayval_labelControlM.grid(row=2, column=1)
        self.azval_labelControlM.grid(row=3, column=1)

        self.gx_labelControlM = ttk.Label(self.subfrmControlM, text="gx").grid(row=1, column=2)
        self.gy_labelControlM = ttk.Label(self.subfrmControlM, text="gy").grid(row=2, column=2)
        self.gz_labelControlM = ttk.Label(self.subfrmControlM, text="gz").grid(row=3, column=2)
        self.gxval_labelControlM = ttk.Label(self.subfrmControlM, text=str(0.0))
        self.gyval_labelControlM = ttk.Label(self.subfrmControlM, text=str(0.0))
        self.gzval_labelControlM = ttk.Label(self.subfrmControlM, text=str(0.0))

        self.gxval_labelControlM.grid(row=1, column=3)
        self.gyval_labelControlM.grid(row=2, column=3)
        self.gzval_labelControlM.grid(row=3, column=3)
        
        self.setZero_ButtonControlM = ttk.Button(self.subfrmControlM, command=self.do_nothing, text="", cursor="arrow")
        self.setZero_ButtonControlM.grid(row = 4, column=0, columnspan=1, padx=4, pady=10, sticky="ns")
        self.update_ButtonControlM = ttk.Button(self.subfrmControlM, command=self.do_nothing, text="", cursor="arrow")
        self.update_ButtonControlM.grid(row=4, column=1, columnspan=1, padx=4, pady=10, sticky="ns")

        self.useIMU_label = ttk.Label(self.subfrmControlM, text="Use IMU : ").grid(row=4, column=2, padx=20, pady=10, sticky="nsew")
        self.useIMU_intVal = tk.IntVar()
        self.useIMU_checkButtonM = ttk.Checkbutton(self.subfrmControlM, command=self.toggle_useIMU, variable=self.useIMU_intVal)
        self.useIMU_checkButtonM.grid(row=4, column=3, columnspan=1, padx=20, pady=10, sticky="nsew")

        for i in range(5):
            for j in range(5):
                self.subfrmControlM.rowconfigure(i, weight=1)
                self.subfrmControlM.columnconfigure(j, weight=1)

        ######################################## Motor Control Frame ####################################################
        
        self.subfrmControlB = ttk.LabelFrame(self.frmControl, text=" Motor Control ", style='TLabelframe')

        self.pos_scaleControlB = ttk.Scale(self.subfrmControlB, command=self._getScaleValue, from_=0, to=255, cursor="hand2", style="TScale").grid(row=0, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="nsew")
        self.currentPos_ButtonControlB = ttk.Button(self.subfrmControlB, text="Set Motor Command", cursor='hand2', command=self._setMotorCommand)
        self.currentPos_ButtonControlB.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="nsew")

        self.motorSel_comboBoxB = ttk.Combobox(self.subfrmControlB, values=self.motorList, cursor="hand2", style='TCombobox')
        self.motorSel_comboBoxB.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="we")

        self.addMotor_button = ttk.Button(self.subfrmControlB, text="+", style='Accent.TButton', command=self._show_addMotorPopup, cursor="hand2")
        self.addMotor_button.grid(row=2, column=2, padx=10, pady=(0, 10), sticky="nsew")
        
        for i in range(3):
            for j in range(3):
                self.subfrmControlB.rowconfigure(i, weight=1)
                self.subfrmControlB.columnconfigure(j, weight=1)

        
        ######################################## Packing all together ####################################################
        for i in range(4):
            for j in range(1):
                self.frmControl.rowconfigure(i, weight=1)
                self.frmControl.columnconfigure(j, weight=1)

        self.currentConfig_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.subfrmControlT.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.subfrmControlM.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.subfrmControlB.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.frmControl.grid(row=0, column=3, rowspan=5, columnspan=2, sticky="nsew")

    #------------------------------------------------------------#

    def _init_frmConfig(self):
        self.frmConfig = ttk.LabelFrame(self.mainWindow, style='TLabelframe', text=" Select Configuration ")
        
        self.scrollBarConfig = ttk.Scrollbar(self.frmConfig)
        self.scrollBarConfig.grid(row=0, column=3, rowspan=3, columnspan=1, padx=(5, 5), pady=10, sticky="nsew")

        self.tree = ttk.Treeview(self.frmConfig, columns=('type'),yscrollcommand=self.scrollBarConfig.set, height=2)#, selectmode="browse")

        self.tree.heading('#0', text="", anchor="center")
        self.tree.column('#0', minwidth=0, width=100)
        self.tree.heading('type', text='type', anchor="w")
        self.tree.column('type', minwidth=0, width=80)
        
        self.scrollBarConfig.config(command=self.tree.yview)

##        self.treeData = [
##            ("", 1, "Bird", ""),
##            (1, 2, "right motor", "(servo)"),
##            (1, 3, "left motor", "(servo)"),
##            (1, 4, "tail motor", "(servo)"),
##            (1, 5, "freq", "(input)"),
##            (1, 6, "dihedral", "(input)"),
##            ("", 7, "Quadcopter", ""),
##            (7, 8, "motor 1", "(brushless)"),
##            (7, 9, "motor 2", "(brushless)"),
##            (7, 10, "motor 3", "(brushless)"),
##            (7, 11, "motor 4", "(brushless)"),
##            (7, 12, "Kp", "(input)"),
##            (7, 13, "Ki", "(input)"),
##            (7, 14, "Kd", "(input)"),
##            ("", 15, "Fixed Wing", ""),
##            (15, 16, "Motor 1", "(brushless)"),
##            (15, 17, "Kp", "(input)"),
##            (15, 18, "Ki", "(input)"),
##            (15, 19, "Kd", "(input)"),
##            ]
        
        self.treeData = []
        self._configList_2_treeData()
        self._update_tree()
        self.tree.grid(row=0, column=0, rowspan=3, columnspan=3, padx=(5, 0), pady=10, sticky="nsew")
        
        self.configButton = ttk.Button(self.frmConfig, text="Set Configuration", cursor="hand2", command=self._set_config)
        self.delConfigButton = ttk.Button(self.frmConfig, text="Delete", cursor="hand2", command=self._del_config)
        self.configButton.grid(row=3, column=0, rowspan=1, columnspan=2, padx=5, pady=(0, 10), sticky="nsew")
        self.delConfigButton.grid(row=3, column=2, rowspan=1, columnspan=2, padx=5, pady=(0, 10), sticky="nsew")

        for i in range(4):
            self.frmConfig.rowconfigure(i, weight=1)
            for j in range(4):
                self.frmConfig.columnconfigure(j, weight=1)
        
        self.frmConfig.grid(row=0, column=0, rowspan=1, columnspan=3, padx=(10, 0), pady=10, sticky="nsew")            

    #------------------------------------------------------------#

    def toggle_useIMU(self):
        self.ThreadBLE.useIMU = self.useIMU_intVal.get()

        if self.ThreadBLE.useIMU: # Si on utilise l'IMU -> Affichage normal des boutons + link correct des bouttons
            self.setZero_ButtonControlM.configure(command=self.setZero_IMU, text="Offset", cursor="hand2")
            self.update_ButtonControlM.configure(command=self.updateTab_IMU, text="Update", cursor="hand2")
            
        elif not(self.ThreadBLE.useIMU): # Si on utilise pas l'IMU -> Affichage vide des boutons + link to do_nothing() des bouttons
            self.setZero_ButtonControlM.configure(command=self.do_nothing, text="", cursor="arrow")
            self.update_ButtonControlM.configure(command=self.do_nothing, text="", cursor="arrow")

    #------------------------------------------------------------#

    def _del_config(self):
        try:
            config_number = int(self.tree.focus())
            config_name = self.treeData[config_number-1][2]
            for i, config in enumerate(self.configList, start=0):
                if config.name == config_name:
                    del self.configList[i] # Delete first item that has the right name
                    break

            if len(self.configList) == 0: # If the list is empty, create a default (empty) configuration
                self.configList.append(configuration())
                self.currentConfig = self.configList[0]
            else:
                self.currentConfig = self.configList[i-1]

            self._set_config(config_number=i-1)
            self._configList_2_treeData()    
            self._update_tree()
            
        except:
            pass

    #------------------------------------------------------------#

    def _set_config(self, config_number=None):
        self._init_frmTable()
        self.motorSel_comboBoxB['values'] = []

        try:
            # Change current configuration
            if config_number is None:
                config_number = int(self.tree.focus())
                
            config_name = self.treeData[config_number-1][2]
            for i, config in enumerate(self.configList, start=0):
                if config.name == config_name:
                    self.currentConfig = self.configList[i] # Delete first item that has the right name
                    break
            
            # Modify motors and params list
            self.motorList = [] # Reset motor list accessible by interface
            self.ThreadBLE.motors = {} # Reset motor list accessible by BLE Thread
            self.ThreadBLE._uuid = self.ThreadBLE._uuid_init # Reset to initial configuration
            self.ThreadBLE.param_request = {}
            
            for key in self.currentConfig.data:
                if MOTORS_TYPE.count(key): # Check if the key is a motor of type : "servo" "bdc"
                    for motor, uuid in zip(self.currentConfig.data[key], self.currentConfig.uuid[key]):
                        self._set_new_motor(name=motor, uuid=uuid)
                if key == "param":
                    for param, uuid in zip(self.currentConfig.data[key], self.currentConfig.uuid[key]):
                        self._set_new_param(name=param, uuid=uuid)
            
        except:
            pass

        self.currentConfig_label.configure(text="Current configuration : " + self.currentConfig.name)

    #------------------------------------------------------------#

    def _configList_2_treeData(self):
        # self.configList = [config1, config2, config3]
        N = 0
        self.treeData = []
        
        for config in self.configList:
            config.get_treeData() # Set data into treeData format
            for i, item in enumerate(config.treeData, start=0):  
                if i == 0:
                    config.treeData[i] = ("", config.treeData[i][1] + N, config.treeData[i][2], config.treeData[i][3])
                else:
                    # Update numbering of the treeData to match the convention
                    config.treeData[i] = (config.treeData[0][1], config.treeData[i][1] + N, config.treeData[i][2], config.treeData[i][3])
                    
            self.treeData = self.treeData + config.treeData # Add to the list
            N = N + len(config.treeData) # Number of elements in config i

    #------------------------------------------------------------#

    def _update_tree(self): # Show the items currently stored in self.treeData
        self.clear_tree_display() # Remove every item in the tree (the display)
        for item in self.treeData:
            self.tree.insert(parent=item[0], index="end", iid=item[1], text=item[2], values=item[3])
            if item[0] == "":
                self.tree.item(item[1], open=True)

    #------------------------------------------------------------#
                
    def clear_tree_display(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
    #------------------------------------------------------------#

    def _set_new_param(self, uuid=None, name=None):
        # Read the entries
        if (uuid is None) and (name is None) : # If true, the new parameter has been added by the user (pop-up), not using a pre-configuration
            # -> We must add the new parameter to the current configuration
            name = self.paramName_entry.get()
            uuid = self.uuidParam_entry.get()
            # Add name and uuid to the current configuration
            idx = [config.name for config in self.configList].index(self.currentConfig.name)                    # ATTENTION ON AJOUTE QUE DES SERVO SANS SAVOIR CE QUE C'EST VRAIMENT -> AJOUTER L'OPTION BDC DANS LA POPUP?
            self.configList[idx].data["param"].append(name)
            self.configList[idx].uuid["param"].append(uuid)
            self.currentConfig = self.configList[idx]
            # Clear text from the popup
            self.uuidParam_entry.delete(0, END) # Clear the entry text
            self.paramName_entry.delete(0, END) # Clear the entry text

            # Update tree
            self._configList_2_treeData()
            self._update_tree()

        # Add uuid to the list
        self.ThreadBLE._uuid.update({name:uuid})      

        # Compute the row index where to place the new button
        rowIdx=len(self.frmTable_button)
        
        # Modify callback function and text (to check :  #print([name, self.frmTable_entry[rowIdx-1][1].get()])) )       
        self.frmTable_button[-1].configure(text=name, style='TButton', command=lambda: self.ThreadBLE.param_request.update({"name":name, "value":self.frmTable_entry[rowIdx-1][1].get()}))

        if rowIdx < self.nb_params:
            # Create another line in the input list
            self.frmTable_button.append(ttk.Button(self.frmTable, text="+", style='Accent.TButton', cursor="hand2", command=self._show_addParamPopup))
            self.frmTable_button[-1].grid(row=rowIdx, column=0, rowspan=1, columnspan=1, padx=(10, 5), pady=2)
            self.frmTable_entry[rowIdx][1] = ttk.Entry(self.frmTable)
            self.frmTable_entry[rowIdx][1].grid(row=rowIdx, column=1, rowspan=1, columnspan=1, padx=(5, 10), pady=2)

        # Close Popup
        self._close_addParamPopup()

    #------------------------------------------------------------#

    def _set_new_motor(self, name=None, uuid=None):
        if (uuid is None) and (name is None) : # If true, the new motor has been added by the user (pop-up), not using a pre-configuration
            # -> We must add the new motor to the current configuration
            uuid = self.uuidMotor_entry.get() # Get name and uuid from popup
            name = self.motorName_entry.get()
            motorType = self.motorType_comboBox.get()
            # Add name and uuid to the current configuration           
            idx = [config.name for config in self.configList].index(self.currentConfig.name)                    # ATTENTION ON AJOUTE QUE DES SERVO SANS SAVOIR CE QUE C'EST VRAIMENT -> AJOUTER L'OPTION BDC DANS LA POPUP?
            self.configList[idx].data[motorType].append(name)
            self.configList[idx].uuid[motorType].append(uuid)
            self.currentConfig = self.configList[idx]
            # Clear text from the popup
            self.motorName_entry.delete(0, END) # Clear the entry text            
            self.uuidMotor_entry.delete(0, END) # Clear the entry text

            # Update tree
            self._configList_2_treeData()
            self._update_tree()
        
        # Update motor list and uuids
        self.ThreadBLE._uuid.update({name:uuid})
        self.ThreadBLE.motors.update({name:actuator()})
        self.motorList.append(name)
        self.motorSel_comboBoxB['values'] = self.motorList

        # Close Popup
        self._close_addMotorPopup()
    
    #------------------------------------------------------------#

    def _getScaleValue(self, val):
        self.scaleValue = int(float(val))
        self.currentPos_ButtonControlB.configure(text="Set Motor Command : " + str(self.scaleValue) + ' [-]')

    #------------------------------------------------------------#

    def _setMotorCommand(self):
        if self.ThreadBLE.connectedDevice is not None:
            self._getComboBoxValue()

            self.ThreadBLE.selected_motor_name = self.motorSel
            
            self.ThreadBLE.motors[self.motorSel].setCommand_request = True
            self.ThreadBLE.motors[self.motorSel].pos = self.scaleValue

    #------------------------------------------------------------#

    def _setMotorMin(self):
        if self.ThreadBLE.connectedDevice is not None:
            self._getComboBoxValue()            
            self.ThreadBLE.motors[self.motorSel].setMin_request = True
            self.ThreadBLE.motors[self.motorSel].minPos = self.scaleValue

    #------------------------------------------------------------#

    def _setMotorMax(self):
        if self.ThreadBLE.connectedDevice is not None:
            self._getComboBoxValue()
            self.ThreadBLE.motors[self.motorSel].setMax_request = True
            self.ThreadBLE.motors[self.motorSel].maxPos = self.scaleValue

    #------------------------------------------------------------#

    def _getComboBoxValue(self):
        self.motorSel = self.motorSel_comboBoxB.get()
        
    #------------------------------------------------------------#    

    def _connect(self):
        # Connect to the selected peripheral
        self.connectButton.configure(text="Wait...", command=self.do_nothing)
        self.mainWindow.update()
        self.device2Connect = self.connectList.get(tk.ACTIVE)
        print("Connection to " + str(self.device2Connect))
        self.ThreadBLE.connect(deviceName=str(self.device2Connect))

        while self.ThreadBLE.connectedDevice is None:
            self.mainWindow.update()

        print(" C'est bon on est passé ! ")
        print(self.ThreadBLE.connectedDevice)

        if self.ThreadBLE.connectedDevice == "Fail":
            print("Detect failure")
            self.ThreadBLE.connectedDevice = None
            self.connectButton.configure(text="Connect", command=self._connect)
            
        else:
            self.connectButton.configure(text="Disconnect from "+ str(self.device2Connect), command=self._disconnect)

        self.mainWindow.update()
    #------------------------------------------------------------#

    def _disconnect(self):
        # Disconnect from the current peripheral
        self.ThreadBLE.disconnect()
        
        try:
            self.connectButton.configure(text="Connect", command=self._connect)
        except:
            pass
        
        self.mainWindow.update()

    #------------------------------------------------------------#

    def do_nothing(self):
        pass

    #------------------------------------------------------------#

    def _discover(self):
        self.ThreadBLE.detectedDevices = None
        self.discoverButton.configure(text="Wait...", command=self.do_nothing)
        self.connectList.delete(0, tk.END)
        self.mainWindow.update()
        self.ThreadBLE.discover()

        # Maintain tkinter thread alive while waiting for detected devices
        while self.ThreadBLE.detectedDevices is None:
            self.mainWindow.update()

        print("Device detected")
        
        peripheral = self.ThreadBLE.detectedDevices
        for p in peripheral:
            if p.name is not None:
                self.connectList.insert(tk.END, str(p.name))

        self.discoverButton.configure(text="Discover", command=self._discover)
        self.mainWindow.update()
        
    #------------------------------------------------------------#

    def updateTab_IMU(self):
        acc = self.ThreadBLE.imu.get_acc()
        gyro = self.ThreadBLE.imu.get_gyro()
        
        self.axval_labelControlM.configure(text=str(round(acc[0], 3)))
        self.ayval_labelControlM.configure(text=str(round(acc[1], 3)))
        self.azval_labelControlM.configure(text=str(round(acc[2], 3)))
        self.gxval_labelControlM.configure(text=str(round(gyro[0], 3)))
        self.gyval_labelControlM.configure(text=str(round(gyro[1], 3)))
        self.gzval_labelControlM.configure(text=str(round(gyro[2], 3)))

    #------------------------------------------------------------#

    def setZero_IMU(self):
        self.ThreadBLE.imu.setZero_request = True   
        
    #------------------------------------------------------------#

    def show(self):
        self.mainWindow.mainloop()

    #------------------------------------------------------------#

    def _show_connectPopup(self):
        self._init_connectPopup()
        self.connectWindow.deiconify()

    #------------------------------------------------------------#

    def _close_connectPopup(self):
        self.connectWindow.destroy()

    #------------------------------------------------------------#

    def _show_addParamPopup(self):
        self._init_addParamPopup()
        self.addParam_window.deiconify()

    #------------------------------------------------------------#

    def _close_addParamPopup(self):
        self.addParam_window.destroy()

    #------------------------------------------------------------#

    def _show_addMotorPopup(self):
        self._init_addMotorPopup()
        self.addMotor_window.deiconify()

    #------------------------------------------------------------#

    def _close_addMotorPopup(self):
        self.addMotor_window.destroy()
    #------------------------------------------------------------#

    def _show_helpPopup(self):
        self._init_helpPopup()
        self.helpWindow.deiconify()

    #------------------------------------------------------------#

    def _close_helpPopup(self):
        self.helpWindow.destroy()

    #------------------------------------------------------------#

    def kill(self):
        self.mainWindow.destroy()

    #------------------------------------------------------------#

    def _create_new_config(self):
        self.configList.insert(0, configuration())
        self.currentConfig = self.configList[0]
        self._set_config(config_number=0)
        self._configList_2_treeData()    
        self._update_tree()
        
    #------------------------------------------------------------#

    def _save_config(self):
        if self.currentConfig.name == "default":
            self._save_config_as()
        else:
            write_config_file(self.currentConfig)
            messagebox.showinfo(title="save configuration", message="File " + self.currentConfig.name + ".txt has been successfully saved !")

    #------------------------------------------------------------#

    def _save_config_as(self):
        path = asksaveasfilename()
        self.currentConfig.path = path
        self.currentConfig.name = os.path.basename(path)
        write_config_file(self.currentConfig)
        self._configList_2_treeData()
        self._update_tree()
        self.currentConfig_label.configure(text="Current configuration : " + self.currentConfig.name)
        messagebox.showinfo(title="save configuration as", message="File " + self.currentConfig.name + ".txt has been successfully saved !")

    #------------------------------------------------------------#

    def _load_config(self):
        config = read_config_file(askopenfilename())
        self.configList.append(config)
        self._configList_2_treeData()
        self._update_tree()

    #------------------------------------------------------------#

    def _save_measure(self):
        messagebox.showinfo(title="Oups", message="This option is not yet implemented")

    #------------------------------------------------------------#
    
    def _save_measure_as(self):
        messagebox.showinfo(title="Oups", message="This option is not yet implemented")

    #------------------------------------------------------------#

    def _generate_arduino_code(self):
        with open("Arduino_template/Arduino_template.txt", 'r') as template:
            try:
                os.mkdir(self.currentConfig.name) # Arduino requires to store .ino files into a folder of the same name
            except:
                pass
            
            newfile = open(self.currentConfig.name + "/" + self.currentConfig.name + ".ino", 'w')
            for line in template.readlines():
                newfile.write(line)
                if line == "// *BLE Characteristics*\n":
                    # Add characteristics
                    for key in self.currentConfig.data:
                        for element, uuid in zip(self.currentConfig.data[key], self.currentConfig.uuid[key]):
                            newfile.write("BLEByteCharacteristic " + element + "_char(\"" + uuid + "\", BLEWriteWithoutResponse | BLERead);\n")

                    if self.ThreadBLE.useIMU:
                        for axis in ["aX", "aY", "aZ", "gX", "gY", "gZ", "setZero_IMU"]:
                            newfile.write("BLEByteCharacteristic " + axis + "_char(\"" + self.ThreadBLE._uuid[axis] \
                                        + "\", BLEWriteWithoutResponse | BLERead);\n")
                
                elif line == "// *Declare variables to store datas*\n":
                    # Add variables
                    for key in self.currentConfig.data:
                        for element in self.currentConfig.data[key]:
                            newfile.write("uint8_t " + element + " = 0;\n")

                elif line == "    // *Add characteristics to the service*\n":
                    # Add characteristic to the service
                    for key in self.currentConfig.data:
                        for element in self.currentConfig.data[key]:
                            newfile.write("    seeedService.addCharacteristic(" + element + "_char);\n")

                    if self.ThreadBLE.useIMU:
                        for axis in ["aX", "aY", "aZ", "gX", "gY", "gZ", "setZero_IMU"]:
                            newfile.write("    seeedService.addCharacteristic(" + axis + "_char);\n")

                elif line == "    // set the initial value to 0\n":
                    # Set initial value of the variables to 0
                    for key in self.currentConfig.data:
                        for element in self.currentConfig.data[key]:
                            newfile.write("    " + element + "_char.writeValue(0);\n")

                    if self.ThreadBLE.useIMU:
                        for axis in ["aX", "aY", "aZ", "gX", "gY", "gZ", "setZero_IMU"]:
                            newfile.write("    " + axis + "_char.writeValue(0);\n")

                elif line == "    // *Set advertised local name and service UUID*\n":
                    # Set initial value of the variables to 0
                    newfile.write("    BLE.setLocalName(\"" + self.currentConfig.name + "\");\n")
                
                elif line == "            // *Read values*\n":
                    # Read values of each characteristic
                    for key in self.currentConfig.data:
                        for element in self.currentConfig.data[key]:
                            newfile.write("            if(" + element + "_char.written()){\n                " + element + " = " + element + "_char.value();\n            }\n")                    

                elif line == "// *IMU libraries*\n" and self.ThreadBLE.useIMU:
                    newfile.write("#include <LSM6DS3.h>\n#include <Wire.h>\n")

                elif line == "// *IMU class and variables*\n" and self.ThreadBLE.useIMU:
                    newfile.write("LSM6DS3 IMU(I2C_MODE, 0x6A);\n"\
                                + "float aX, aY, aZ, gX, gY, gZ;\n"\
                                + "uint32_t setZero_IMU = 0;\n"\
                                + "float imu[6];\n")

                elif line == "    // *Begin IMU*\n" and self.ThreadBLE.useIMU:
                    newfile.write("    if(IMU.begin())  {\n"\
                                + "        Serial.println(\"STARTING IMU FAILED\");\n"\
                                + "        while(1);\n    }\n")

                elif line == "            // *Read and write IMU values*\n" and self.ThreadBLE.useIMU:
                    tab = ["AccelX", "AccelY", "AccelZ", "GyroX", "GyroY", "GyroZ"]
                    for i, axis in enumerate(["aX", "aY", "aZ", "gX", "gY", "gZ"]):
                        newfile.write("            imu[" + str(i) + "] = IMU.readFloat" + tab[i] + "();\n")

                    for i, axis in enumerate(["aX", "aY", "aZ", "gX", "gY", "gZ"]):
                        newfile.write("            " + axis + "_char.writeValue(max(0, min(255, abs(int(255 * imu[" + str(i) + "]))))); // clip value as integer between 0 - 255\n")
                    
                    newfile.write("            if(setZero_IMU_char.written()){\n                setZero_IMU = setZero_IMU_char.value();\n            }\n") 

                elif line == "    // *Read IMU values*\n" and self.ThreadBLE.useIMU:
                    tab = ["AccelX", "AccelY", "AccelZ", "GyroX", "GyroY", "GyroZ"]
                    for i, axis in enumerate(["aX", "aY", "aZ", "gX", "gY", "gZ"]):
                        newfile.write("    imu[" + str(i) + "] = IMU.readFloat" + tab[i] + "();\n")

                    newfile.write("    if(setZero_IMU_char.written()){\n        setZero_IMU = setZero_IMU_char.value();\n    }\n")
                
            newfile.close()
            
        messagebox.showinfo(title="Generate code", message="Code has been successfully generated !")

######################################### TEST #########################################

a = imu()
b = actuator()
d = GUI()

