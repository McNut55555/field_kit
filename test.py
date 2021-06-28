""" this is where im going to test code so i dont have to keep ruunning the whole program """

from re import S
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMessageBox
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from pyqtgraph.functions import disconnect
import globals
from avaspec import *
import time
import math
from ui_functions import *
from ui_main import Ui_MainWindow
import json 
import struct

print("connected")
ret = AVS_Init(0)                                                                                   # init(0) means were using a USB
                                                                                                    # will return the number of devices on success this should be 1 

ret = AVS_GetNrOfDevices()                                                                          # will check the list of connected usb devices and returns the number attached   
mylist = AvsIdentityType()                                                                          # pretty sure these do the same thing but whatever you know it works
mylist = AVS_GetList(1)          
globals.identity = mylist                                                                   
# may need to come back and see what this function does

# displaying information on the serial number and working with it
serienummer = str(mylist[0].SerialNumber.decode("utf-8"))


# this activates the spectrometer for communication
globals.dev_handle = AVS_Activate(mylist[0])

# gets all the information about the spectrometer
devcon = DeviceConfigType()
devcon = AVS_GetParameter(globals.dev_handle, 63484)
globals.deviceConfig = devcon
globals.pixels = devcon.m_Detector_m_NrPixels
globals.wavelength = AVS_GetLambda(globals.dev_handle)

# self.startStopButton.setEnabled(False)                                                                  # gets rid of old data on the screen
ret = AVS_UseHighResAdc(globals.dev_handle, True)                                   # sets the spectrometer to use 16 bit resolution instead of 14 bit
measconfig = MeasConfigType()
measconfig.m_StartPixel = 0
measconfig.m_StopPixel = globals.pixels - 1
measconfig.m_IntegrationTime = globals.integration_time                                                    # variables that will get changed
measconfig.m_IntegrationDelay = 0
measconfig.m_NrAverages = globals.averages                                                         # variables that will get changed
measconfig.m_CorDynDark_m_Enable = 0  # nesting of types does NOT work!!
measconfig.m_CorDynDark_m_ForgetPercentage = 0
measconfig.m_Smoothing_m_SmoothPix = 0
measconfig.m_Smoothing_m_SmoothModel = 0
measconfig.m_SaturationDetection = 0
measconfig.m_Trigger_m_Mode = 0
measconfig.m_Trigger_m_Source = 0
measconfig.m_Trigger_m_SourceType = 0
measconfig.m_Control_m_StrobeControl = 0
measconfig.m_Control_m_LaserDelay = 0
measconfig.m_Control_m_LaserWidth = 0
measconfig.m_Control_m_LaserWaveLength = 0.0
measconfig.m_Control_m_StoreToRam = 0
ret = AVS_PrepareMeasure(globals.dev_handle, measconfig)
nummeas = 1                                                                         # variables that will get changed

scans = 0                                                                           # counter
globals.stopscanning = False                                                        # dont want to stop scanning until we say so
while (globals.stopscanning == False):                                              # keep scanning until we dont want to anymore
    ret = AVS_Measure(globals.dev_handle, 0, 1)                                     # tell it to scan
    dataready = False                                                               # while the data is false
    while (dataready == False):
        dataready = (AVS_PollScan(globals.dev_handle) == True)                      # get the status of data
        time.sleep(0.001)
    if dataready == True:
        ret = AVS_GetScopeData(globals.dev_handle)
        globals.spectraldata = ret[1]
        scans = scans + 1
        if (scans >= nummeas):
            globals.stopscanning = True  
    # self.app.processEvents()                          ##########################################      look into this line
    time.sleep(0.001)  
globals.measureType = measconfig
#
#
# Done getting data
# lets look at saving shit

# print all the identity stuff
print(globals.identity[0].SerialNumber)
print(globals.identity[0].UserFriendlyName)
print(globals.identity[0].Status)
print()

# print measure configuration data
print(globals.measureType.m_StartPixel)
print(globals.measureType.m_StopPixel)
print(globals.measureType.m_IntegrationTime)
print(globals.measureType.m_IntegrationDelay)
print(globals.measureType.m_NrAverages)
print(globals.measureType.m_CorDynDark_m_Enable)
print(globals.measureType.m_CorDynDark_m_ForgetPercentage)
print(globals.measureType.m_Smoothing_m_SmoothPix)
print(globals.measureType.m_Smoothing_m_SmoothModel)
print(globals.measureType.m_SaturationDetection)
print(globals.measureType.m_Trigger_m_Mode)
print(globals.measureType.m_Trigger_m_Source)
print(globals.measureType.m_Trigger_m_SourceType)
print(globals.measureType.m_Control_m_StrobeControl)
print(globals.measureType.m_Control_m_LaserDelay)
print(globals.measureType.m_Control_m_LaserWidth)
print(globals.measureType.m_Control_m_LaserWaveLength)
print(globals.measureType.m_Control_m_StoreToRam)


