from re import S
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

        # initalize the inital globals
        globals.integration_time = 1
        globals.averages = 2
        globals.first = True 

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
        self.scopeModeButton.clicked.connect(self.scope)
        self.scopeMinDarkButton.clicked.connect(self.scopeMinDarkButton_clicked)
        self.absButton.clicked.connect(self.absButton_clicked)
        self.reflectButton.clicked.connect(self.reflectButton_clicked)
        self.saveButton.clicked.connect(self.saveButton_clicked)

    #   Adding all the clicked button functionality 
    #
    #
    #
    #

    @pyqtSlot()
    def absButton_clicked(self):
        y_value = []
        y_label = "Percent (%)"
        title = "Absorbance Mode"
        for x in range(0, len(globals.spectraldata)-2):
            # print((math.fabs(globals.spectraldata[x]-globals.darkData[x]))/(math.fabs(globals.refData[x]-globals.darkData[x])))
            if (globals.refData[x] - globals.darkData[x]) < 0.1:
                y_value.append(0.0)
            elif (math.fabs(globals.spectraldata[x]-globals.darkData[x]))/(math.fabs(globals.refData[x] - globals.darkData[x])) == 0.0:
                y_value.append(0.0)
            elif (math.fabs(globals.spectraldata[x]-globals.darkData[x]))/(math.fabs(globals.refData[x] - globals.darkData[x])) > 1:
                y_value.append(1)
            else:
                y_value.append( -1 * math.log((math.fabs(globals.spectraldata[x]-globals.darkData[x]))/(math.fabs(globals.refData[x]-globals.darkData[x])),10))
        for x in range(0, len(y_value)):
            if y_value[x] > 1:
                y_value[x] = 1

        self.plot(y_value, y_label, title)

    @pyqtSlot()
    def reflectButton_clicked(self):
        print()
        y_value = []
        y_label = "Percent (%)"
        title = "Reflectance Mode"
        for x in range(0,len(globals.spectraldata)-2):
            y_value.append( 100*((globals.spectraldata[x]-globals.darkData[x])/(globals.refData[x]-globals.darkData[x])) )


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

    # this is a little glitchy 
    # this is a little glitchy 
    # this is a little glitchy
    # this is a little glitchy
    # seems that the dark reading is just noise and increasing the integration time has no effect on it
    # not sure how to solve this just yet
    # if it continues on without stopping or coming out of the loop the device needs to be disconnected and then reconnected
    # the above should get fixed

    @pyqtSlot()
    def configButton_clicked(self):
        print("configuration")

        largest_pixel = 0
        count = 0
        while( largest_pixel > 60000 or largest_pixel < 55000 ):
            largest_pixel = 0
            for x in range(0, len(globals.spectraldata)-2):
                if(globals.spectraldata[x] > largest_pixel):
                    largest_pixel = globals.spectraldata[x]

            if(largest_pixel > 60000):
                # lower the integration time:
                globals.integration_time = globals.integration_time - 2

            if(largest_pixel < 55000):
                # increase integration time: 
                globals.integration_time = globals.integration_time + 2

            # QtWidgets.QApplication.processEvents()                                        # look into this line
            count += 1
            if count >= 100:
                break
            self.startStopButton_clicked()
        print(largest_pixel)
        
        count = 0
        cycle_time = globals.integration_time * globals.averages
        while( cycle_time > 550 or cycle_time < 450):
            if cycle_time > 550: 
                globals.averages -= 1 
            if cycle_time < 450: 
                globals.averages += 1
            cycle_time = globals.integration_time * globals.averages
            self.startStopButton_clicked()
            count += 1 
            if count >= 100:
                break
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

        self.darkButton.setEnabled(True)
        self.configButton.setEnabled(True)
        self.refButton.setEnabled(True)
        self.startStopButton.setEnabled(True)
        globals.measureType = measconfig

        # while globals.first == True:
        #     self.plot_scope()
        #     globals.first = False

        self.scope()    

        return   

    @pyqtSlot()
    def connectButton_clicked(self):
        # initialize the usb... were not gonna care about eithernet for now only usb
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
        globals.pixels = devcon.m_Detector_m_NrPixels
        globals.wavelength = AVS_GetLambda(globals.dev_handle)

        # change if the button should be able to be used or not 
        self.startStopButton.setEnabled(True)
        self.connectButton.setEnabled(False)

        return

    @pyqtSlot()
    def scopeMinDarkButton_clicked(self):
        y_value = []
        title = "Scope Minus Dark"
        y_label = "Counts"
        for x in range(0, len(globals.spectraldata)-2):
            y_value.append(globals.spectraldata[x]-globals.darkData[x])
        self.plot(y_value, y_label, title)

    @pyqtSlot()
    def saveButton_clicked(self):
        print("Save Button clicked")
        # may need to add a path variable so you can choose where the file gets saved. 

        # would like to open another window to get all the infromation that is need when saving basically the name
        # need to save to the right file extension depending on the graph they want
        fileName = "saveFile"
        extension = ""
        measureMode = ""
        choice = 0
        if(choice == 0):
            extension = ".raw8"
            measureMode = "00000000"
        elif choice == 1:
            extension = ".rwd8"
            measureMode = "00000010"
        elif choice == 2:
            extension = ".abs8"
            measureMode = "00000001"
        elif choice == 3:
            extension = ".trm8"
            measureMode = "00000011"
        elif choice == 4:
            extension = ".irr8"
            measureMode = "00000101"
        elif choice == 5:
            extension = ".rfl8"
            measureMode = "00000100"
        elif choice == 6:
            extension = ".rir8"
            measureMode = "00000110"
        else:
            extension = ".raw8"
            measureMode = "00000000"
            print("ERROR: DIDN'T FIND FILE TYPE SPECIFIED")

        with open(fileName + extension, "w") as file:
            # Marker
            file.write("01000001")
            file.write("01010110")
            file.write("01010011")
            file.write("00111000")
            file.write("00110100")
            # Number of spectra 
            file.write("00000001")
            # length
            # seqnum
            file.write("00000000")
            # measure mode 
            file.write(measureMode)
            # bitness
            file.write("00000001")
            #SDmarker
            file.write("00000000")
            #identity 
            for x in range(0, len(globals.identity[0].SerialNumber)):
                if len(str(decimalToBinary(globals.identity[0].SerialNumber[x]))) == 6:
                    file.write("00" + str(decimalToBinary(globals.identity[0].SerialNumber[x])))
                elif len(str(decimalToBinary(globals.identity[0].SerialNumber[x]))) == 7:
                    file.write("0" + str(decimalToBinary(globals.identity[0].SerialNumber[x])))
                elif len(str(decimalToBinary(globals.identity[0].SerialNumber[x]))) == 5:
                    file.write("000" + str(decimalToBinary(globals.identity[0].SerialNumber[x])))
                elif len(str(decimalToBinary(globals.identity[0].SerialNumber[x]))) == 4:
                    file.write("0000" + str(decimalToBinary(globals.identity[0].SerialNumber[x])))
            for x in range(0,64):
                print()
                
            #meascong
            #timestamp
            #SPCfiledate
            #detectortemp
            #boardtemp
            #NTC2volt
            #colorTemp
            #calIntTime
            #fitdata
            #comment
            #xcoord
            #scope
            #dark
            #reference
            #mergegroup
            #straylightconf
            #nonlincong
            #customReflectance
            #customWhiteRefValue
            #customDarkRefValue


    #   clicked button functionality
    #
    #
    #
    #   


    # def plot_absorbance(self):
    #     for x in range(0, len(globals.spectraldata)-2):
    #         globals.absData.append( -math.log((globals.spectraldata[x]-globals.darkData[x])/(globals.refData[x]-globals.darkData[x])))

    # def plot_transmittance(self):
    #     print("transmission")
    #     for x in range(0, len(globals.spectraldata)-2):
    #         globals.transData.append( (globals.spectraldata[x]-globals.darkData[x])/(globals.refData[x]-globals.darkData[x]) )

    # def plot_reflectance(self):
    #     print("reflectance")
    #     for x in range(0, len(globals.spectraldata)-2):
    #         globals.reflectData.append( (globals.spectraldata[x] - globals.darkData[x])/(globals.refData[x]-globals.darkData[x]) )

    def scope(self):
        # get the values
        y_value = []
        for x in range(0,len(globals.spectraldata)-2):                                  # dropping off the last two data points
            y_value.append(globals.spectraldata[x])
        self.plot(y_value, "Scope (ADC Counts)", "Scope Mode")

    def plot(self, y_value, y_label, title):

        # get the values
        x_value = []
        for x in range(0,len(globals.wavelength)-2):                                    # not sure if this is going to effect it but dropping off the last two data points
            x_value.append(globals.wavelength[x])
        
        # Set the label for x axis
        self.graphWidget.setLabel('bottom', 'Wavelength (nm)')

        # Set the label for y-axis
        self.graphWidget.setLabel('left', y_label)

        # Set the title of the graph
        self.graphWidget.setTitle(title)

        self.graphWidget.clear()
        self.graphWidget.plot(x_value, y_value)



#
#
#   This function takes the input and converts it to binary 
#
#
def decimalToBinary(n):
    return bin(n).replace("0b", "")

#
#
#
#

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
