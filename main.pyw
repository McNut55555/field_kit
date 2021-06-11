from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import globals
from avaspec import *
import time


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi('mainwindow.ui', self)

        # call the spectrometer 
        # getData()
        ret = AVS_Init(0)                                                                                        # init(0) means were using a USB
                                                                                                                # will return the number of devices on success this should be 1 

        ret = AVS_GetNrOfDevices()                                                                               # will check the list of connected usb devices and returns the number attached   
        mylist = AvsIdentityType()                                                                              # pretty sure these do the same thing but whatever you know it works
        mylist = AVS_GetList(1)                                                                                 # may need to come back and see what this function does

        # displaying information on the serial number and working with it
        serienummer = str(mylist[0].SerialNumber.decode("utf-8"))
        # QMessageBox.information(self,"Info","Found Serialnumber: " + serienummer)


        # this activates the spectrometer for communication
        globals.dev_handle = AVS_Activate(mylist[0])

        # gets all the information about the spectrometer
        devcon = DeviceConfigType()
        devcon = AVS_GetParameter(globals.dev_handle, 63484)
        

        globals.pixels = devcon.m_Detector_m_NrPixels
        globals.wavelength = AVS_GetLambda(globals.dev_handle)



        ## measurement button is pressed 
                                                                    # gets rid of old data on the screen
        ret = AVS_UseHighResAdc(globals.dev_handle, True)                                   # sets the spectrometer to use 16 bit resolution instead of 14 bit
        measconfig = MeasConfigType()
        measconfig.m_StartPixel = 0
        measconfig.m_StopPixel = globals.pixels - 1
        measconfig.m_IntegrationTime = 5
        measconfig.m_IntegrationDelay = 0
        measconfig.m_NrAverages = 1
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
        nummeas = 1                                          #default value out of text boxes is a string must cast to int
            
            # to use Windows messages, supply a window handle to send the messages to
            # ret = AVS_Measure(globals.dev_handle, int(self.winId()), nummeas)
            # single message sent from DLL, confirmed with Spy++
            # when using polling, just pass a 0 for the windows handle

        scans = 0                                                                       # counter
        globals.stopscanning = False                                                    # dont want to stop scanning until we say so
        while (globals.stopscanning == False):                                          # keep scanning until we dont want to anymore
            ret = AVS_Measure(globals.dev_handle, 0, 1)                                 # tell it to scan
            dataready = False                                                           # while the data is false
            while (dataready == False):
                dataready = (AVS_PollScan(globals.dev_handle) == True)                  # get the status of data
                time.sleep(0.001)
            if dataready == True:
                ret = AVS_GetScopeData(globals.dev_handle)
                globals.spectraldata = ret[1]
                scans = scans + 1
                if (scans >= nummeas):
                    globals.stopscanning = True               
            time.sleep(0.001)

        # get the values
        x_value = []
        y_value = []
        for x in range(0,len(globals.wavelength)-2):                                    # not sure if this is going to effect it but dropping off the last two data points
            x_value.append(globals.wavelength[x])
        
        for x in range(0,len(globals.spectraldata)-2):                                  # dropping off the last two data points
            y_value.append(globals.spectraldata[x])

        # for x in globals.wavelength:
        #     x_value.append(x)
        # for x in globals.spectraldata:
        #     y_value.append(x)
        
        

        self.plot(x_value, y_value)

    def plot(self, x_value, y_value):
        # Set the label for x axis
        self.graphWidget.setLabel('bottom', 'Wavelength (nm)')

        # Set the label for y-axis
        self.graphWidget.setLabel('left', 'Scope (ADC Counts)')

        # Set the title of the graph
        self.graphWidget.setTitle("Scope Mode")

        self.graphWidget.clear()
        self.graphWidget.plot(x_value, y_value)



def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()













# # first lets import all the necessary libraries
# import os
# import platform
# import sys
# import time
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# from PyQt5 import uic
# from PyQt5.uic.uiparser import QtWidgets
# from avaspec import *
# from pyqtgraph import PlotWidget, plot
# import pyqtgraph as pg 
# # import Gui
# import Gui2
# import globals

# # i have to define a MainWindow class because i don't have one and in my main 
# # class im calling the class that i havent created
# class MainWindow(QtWidgets.QMainWindow):
#     newdata = pyqtSignal()
#     def __init__(self, *args, **kwargs):
#         super(MainWindow,self).__init__(*args, **kwargs)
#         uic.loadUi("Gui.ui", self)
#         self.setupUi(self)
        
#         #set up inital buttons
#         self.startStopButton.setEnabled(False)
#         self.darkButton.setEnabled(False)
#         self.refButton.setEnabled(False)
#         self.configButton.setEnabled(False)


#         # set the information in the boxes
#         # self.timeInput.setText("{:3.1f}".format(5.0))
#         # self.averageInput.setText("{0:d}".format(1))
#         # self.numberInput.setText("{0:d}".format(1))
                
#         # Addint all the connections to the buttons
#         self.connectButton.clicked.connect(self.connectButton_clicked)  
#         # self.closeButton.clicked.connect(self.closeButton_clicked)

#         self.startStopButton.clicked.connect(self.startStopButton_clicked)
#         self.darkButton.clicked.connect(self.darkButton_clicked)
#         self.refButton.clicked.connect(self.refButton_clicked)
#         self.configButton.clicked.connect(self.configButton_clicked)


#         #       do not use explicit connect together with the on_ notation, or you will get
#         #       two signals instead of one!
#         self.newdata.connect(self.handle_newdata)
   


    
# #   if you leave out the @pyqtSlot() line, you will also get an extra signal!
# #   so you might even get three!
# # this function is called when the connect buttion is called. This will begin the process of linking the computer to the spectrometer and will display the 
# # serial number of the device so that you know that the connection actually happened!!!!
#     @pyqtSlot()
#     def connectButton_clicked(self):
#         # initialize the usb... were not gonna care about eithernet for now only usb
#         ret = AVS_Init(0)                                                                                        # init(0) means were using a USB
#                                                                                                                  # will return the number of devices on success this should be 1 

#         ret = AVS_GetNrOfDevices()                                                                               # will check the list of connected usb devices and returns the number attached   

#         mylist = AvsIdentityType()                                                                              # pretty sure these do the same thing but whatever you know it works
#         mylist = AVS_GetList(1)                                                                                 # may need to come back and see what this function does

#         # displaying information on the serial number and working with it
#         serienummer = str(mylist[0].SerialNumber.decode("utf-8"))
#         # QMessageBox.information(self,"Info","Found Serialnumber: " + serienummer)


#         # this activates the spectrometer for communication
#         globals.dev_handle = AVS_Activate(mylist[0])

#         # gets all the information about the spectrometer
#         devcon = DeviceConfigType()
#         devcon = AVS_GetParameter(globals.dev_handle, 63484)
        

#         globals.pixels = devcon.m_Detector_m_NrPixels
#         globals.wavelength = AVS_GetLambda(globals.dev_handle)

#         # change if the button should be able to be used or not 
#         # self.closeButton.setEnabled(True)
#         # self.connectButton.setEnabled(False)
#         # self.startMeasurement.setEnabled(True)
#         self.startStopButton.setEnabled(True)
#         self.darkButton.setEnabled(True)
#         self.refButton.setEnabled(True)
#         self.configButton.setEnabled(True)
#         return

#     @pyqtSlot()
#     def darkButton_clicked(self):
#         print("Dark")

#     @pyqtSlot()
#     def refButton_clicked(self):
#         print("reference")

#     @pyqtSlot()
#     def configButton_clicked(self):
#         print("configuration")

#     @pyqtSlot()
#     def startStopButton_clicked(self):
#         print("startStopButton")
#         self.startStopButton.setEnabled(False)
#         self.repaint()                                                                      # gets rid of old data on the screen
#         ret = AVS_UseHighResAdc(globals.dev_handle, True)                                   # sets the spectrometer to use 16 bit resolution instead of 14 bit
#         measconfig = MeasConfigType()
#         measconfig.m_StartPixel = 0
#         measconfig.m_StopPixel = globals.pixels - 1
#         measconfig.m_IntegrationTime = 5                                                    # variables that will get changed
#         measconfig.m_IntegrationDelay = 0
#         measconfig.m_NrAverages = 1                                                         # variables that will get changed
#         measconfig.m_CorDynDark_m_Enable = 0  # nesting of types does NOT work!!
#         measconfig.m_CorDynDark_m_ForgetPercentage = 0
#         measconfig.m_Smoothing_m_SmoothPix = 0
#         measconfig.m_Smoothing_m_SmoothModel = 0
#         measconfig.m_SaturationDetection = 0
#         measconfig.m_Trigger_m_Mode = 0
#         measconfig.m_Trigger_m_Source = 0
#         measconfig.m_Trigger_m_SourceType = 0
#         measconfig.m_Control_m_StrobeControl = 0
#         measconfig.m_Control_m_LaserDelay = 0
#         measconfig.m_Control_m_LaserWidth = 0
#         measconfig.m_Control_m_LaserWaveLength = 0.0
#         measconfig.m_Control_m_StoreToRam = 0
#         ret = AVS_PrepareMeasure(globals.dev_handle, measconfig)
#         nummeas = 1                                                                         # variables that will get changed
        
#         # to use Windows messages, supply a window handle to send the messages to
#         # ret = AVS_Measure(globals.dev_handle, int(self.winId()), nummeas)
#         # single message sent from DLL, confirmed with Spy++
#         # when using polling, just pass a 0 for the windows handle

#         scans = 0                                                                       # counter
#         globals.stopscanning = False                                                    # dont want to stop scanning until we say so
#         while (globals.stopscanning == False):                                          # keep scanning until we dont want to anymore
#             ret = AVS_Measure(globals.dev_handle, 0, 1)                                 # tell it to scan
#             dataready = False                                                           # while the data is false
#             while (dataready == False):
#                 dataready = (AVS_PollScan(globals.dev_handle) == True)                  # get the status of data
#                 time.sleep(0.001)
#             if dataready == True:
#                 scans = scans + 1
#                 if (scans >= nummeas):
#                     globals.stopscanning = True
#                 self.newdata.emit()                                                     # this line tells the computer that newdata has been "pressed and to update that stuff"
#             self.repaint()                
#             time.sleep(0.001)
#             qApp.processEvents() # allows clicking of the StopMeasBtn to be seen while the function is running. allowing immediate canceliation              
#         self.startStopButton.setEnabled(True)            
#         self.repaint()          
#         return   


#     def plot(self):
#         print("plotting data")  
#         x_value = []
#         y_value = []
#         for x in range(0,len(globals.wavelength)-2):                                    # not sure if this is going to effect it but dropping off the last two data points
#             x_value.append(globals.wavelength[x])
        
#         for x in range(0,len(globals.spectraldata)-2):                                  # dropping off the last two data points
#             y_value.append(globals.spectraldata[x])

#         # Set the label for x axis
#         self.pyqtPlot.setLabel('bottom', 'Wavelength (nm)')

#         # Set the label for y-axis
#         self.pyqtPlot.setLabel('left', 'Scope (ADC Counts)')

#         # Set the title of the graph
#         self.pyqtPlot.setTitle("Scope Mode")

#         self.pyqtPlot.clear()
#         self.pyqtPlot.plot(x_value, y_value)


#     @pyqtSlot()
#     def handle_newdata(self):
#         timestamp = 0
#         ret = AVS_GetScopeData(globals.dev_handle)
#         timestamp = ret[0]

#         # the spectraldata is how the rederarea knows what to print to the graph... this might be the readings in scope mode??? 
#         globals.spectraldata = ret[1]
        
        
#         # QMessageBox.devconinformation(self,"Info","Received data")
#         self.pyqtPlot.update()                                                                    
#         time.sleep(0.001)
#         qApp.processEvents() # allows repaint to occur between scans  
#         return          

# # first lets define the main window!
# def main():
#     app = QApplication(sys.argv)
#     app.lastWindowClosed.connect(app.quit)
#     app.setApplicationName("Connection application")
#     form = MainWindow()
#     form.show()
#     app.exec_()

# main()