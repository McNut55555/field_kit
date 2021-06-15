from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import globals
from avaspec import *
import time
import math


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi('Gui.ui', self)
        globals.integration_time = 1
        globals.averages = 2

        # set all the buttons that should be enabled or not
        self.startStopButton.setEnabled(False)
        self.darkButton.setEnabled(False)
        self.configButton.setEnabled(False)
        self.refButton.setEnabled(False)


        # make all the connections
        self.connectButton.clicked.connect(self.connectButton_clicked)
        self.startStopButton.clicked.connect(self.startStopButton_clicked)
        self.darkButton.clicked.connect(self.darkButton_clicked)
        self.refButton.clicked.connect(self.refButton_clicked)
        self.configButton.clicked.connect(self.configButton_clicked)
        self.stopButton.clicked.connect(self.stopButton_clicked)

    @pyqtSlot()
    def darkButton_clicked(self):
        globals.darkData = globals.spectraldata
        print("darkData now saved")

    @pyqtSlot()
    def stopButton_clicked(self):
        AVS_Done()
        self.startStopButton.setEnabled(False)
        self.connectButton.setEnabled(True)
        self.darkButton.setEnabled(False)
        self.configButton.setEnabled(False)
        self.refButton.setEnabled(False)
        print("disconnected")

    @pyqtSlot()
    def refButton_clicked(self):
        globals.refData = globals.spectraldata
        print("reference data now saved")

    @pyqtSlot()
    def configButton_clicked(self):
        print("configuration")
        # this is a little glitchy 
        # this is a little glitchy 
        # this is a little glitchy
        # this is a little glitchy
        # seems that the dark reading is just noise and increasing the integration time has no effect on it
        # not sure how to solve this just yet
        # if it continues on without stopping or coming out of the loop the device needs to be disconnected and then reconnected
        # the above should get fixed
        largest_pixel = 0
        while( largest_pixel > 60000 or largest_pixel < 55000 ):
            largest_pixel = 0
            for x in range(0, len(globals.spectraldata)-2):
                if(globals.spectraldata[x] > largest_pixel):
                    largest_pixel = globals.spectraldata[x]

            if(largest_pixel > 60000):
                # lower the integration time:
                globals.integration_time = globals.integration_time - 0.5

            if(largest_pixel < 55000):
                # increase integration time: 
                globals.integration_time = globals.integration_time + 0.5

            # QtWidgets.QApplication.processEvents()                                        # look into this line
            self.startStopButton_clicked()
        print(largest_pixel)
        
        cycle_time = globals.integration_time * globals.averages
        while( cycle_time > 550 or cycle_time < 450):
            if cycle_time > 550: 
                globals.averages -= 1 
            if cycle_time < 450: 
                globals.averages += 1
            cycle_time = globals.integration_time * globals.averages
            self.startStopButton_clicked()
        print("done with configuration")
        print(globals.integration_time)
        print(globals.averages)
        

    @pyqtSlot()
    def startStopButton_clicked(self):
        self.startStopButton.setEnabled(False)
        self.repaint()                                                                      # gets rid of old data on the screen
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
            # self.app.processEvents()                          ##########################################      look into this line
            time.sleep(0.001)  

        self.darkButton.setEnabled(True)
        self.configButton.setEnabled(True)
        self.refButton.setEnabled(True)
        self.startStopButton.setEnabled(True)

        self.plot_scope()    
        return   

    @pyqtSlot()
    def connectButton_clicked(self):
        # initialize the usb... were not gonna care about eithernet for now only usb
        ret = AVS_Init(0)                                                                                        # init(0) means were using a USB
                                                                                                                 # will return the number of devices on success this should be 1 

        ret = AVS_GetNrOfDevices()                                                                               # will check the list of connected usb devices and returns the number attached   
        mylist = AvsIdentityType()                                                                              # pretty sure these do the same thing but whatever you know it works
        mylist = AVS_GetList(1)                                                                                 # may need to come back and see what this function does

        # displaying information on the serial number and working with it
        serienummer = str(mylist[0].SerialNumber.decode("utf-8"))


        # this activates the spectrometer for communication
        globals.dev_handle = AVS_Activate(mylist[0])

        # gets all the information about the spectrometer
        devcon = DeviceConfigType()
        devcon = AVS_GetParameter(globals.dev_handle, 63484)
        globals.pixels = devcon.m_Detector_m_NrPixels
        globals.wavelength = AVS_GetLambda(globals.dev_handle)

        # change if the button should be able to be used or not 
        self.startStopButton.setEnabled(True)
        self.connectButton.setEnabled(False)

        return

    def plot_absorbance(self):
        for x in range(0, len(globals.spectraldata)-2):
            globals.absData.append( -math.log((globals.spectraldata[x]-globals.darkData[x])/(globals.refData[x]-globals.darkData[x])))

    def plot_transmittance(self):
        print("transmission")
        for x in range(0, len(globals.spectraldata)-2):
            globals.transData.append( (globals.spectraldata[x]-globals.darkData[x])/(globals.refData[x]-globals.darkData[x]) )

    def plot_reflectance(self):
        print("reflectance")
        for x in range(0, len(globals.spectraldata)-2):
            globals.reflectData.append( (globals.spectraldata[x] - globals.darkData[x])/(globals.refData[x]-globals.darkData[x]) )

    def plot_scope(self):

        # get the values
        x_value = []
        y_value = []
        for x in range(0,len(globals.wavelength)-2):                                    # not sure if this is going to effect it but dropping off the last two data points
            x_value.append(globals.wavelength[x])
        
        for x in range(0,len(globals.spectraldata)-2):                                  # dropping off the last two data points
            y_value.append(globals.spectraldata[x])

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
