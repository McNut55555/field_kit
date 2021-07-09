# from re import L, S
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from pyqtgraph import PlotWidget, plot, ViewBox
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
from pyqtgraph.functions import Color, disconnect
import globals
from avaspec import *
import time
import math
from ui_functions import *
from ui_main import Ui_MainWindow
import struct
import os


## MAIN WINDOW CLASS
##########################################################
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        ## LOAD THE UI PAGE
        ######################################################################## 
        uic.loadUi('ui_main.ui', self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## TOGGLE/BURGUER MENU
        ########################################################################
        self.ui.Btn_Toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 250, True))

        ## PAGES
        ########################################################################

        # PAGE 1
        self.ui.btn_page_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_1))
        self.ui.connectButton.clicked.connect(self.connectButton_clicked)

        # PAGE 2
        self.ui.btn_page_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))

        # PAGE 3
        self.ui.btn_page_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_3))

        # makes sure that the inital page that the GUI displays is page 1. 
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_1)

        ## INITALIZE THE INITAL GLOBAL VARIABLES
        ########################################################################
        globals.integration_time = 10
        globals.averages = 5
        globals.first = True 

        ## SET INITAL ALLOWABLE CLICKS
        ########################################################################
        self.ui.startStopButton.setEnabled(False)
        self.ui.startStopButton.setStyleSheet("background-color : black")
        self.ui.darkButton.setEnabled(False)
        self.ui.darkButton.setStyleSheet("background-color : black")
        self.ui.configButton.setEnabled(False)
        self.ui.configButton.setStyleSheet("background-color : black")
        self.ui.refButton.setEnabled(False)
        self.ui.refButton.setStyleSheet("background-color : black")
        self.ui.stopButton.setEnabled(False)
        self.ui.stopButton.setStyleSheet("background-color : black")

        ## MAKE ALL THE CONNECTIONS
        #######################################################################
        self.ui.connectButton.clicked.connect(lambda: self.connectButton_clicked)
        self.ui.startStopButton.clicked.connect(self.startStopButton_clicked)
        self.ui.darkButton.clicked.connect(self.darkButton_clicked)
        self.ui.refButton.clicked.connect(self.refButton_clicked)
        self.ui.configButton.clicked.connect(self.configButton_clicked)
        self.ui.stopButton.clicked.connect(self.stopButton_clicked)
        self.ui.scopeModeButton.clicked.connect(self.scope)
        self.ui.scopeMinDarkButton.clicked.connect(self.scopeMinDarkButton_clicked)
        self.ui.absButton.clicked.connect(self.absButton_clicked)
        self.ui.reflectButton.clicked.connect(self.reflectButton_clicked)
        self.ui.saveButton.clicked.connect(self.saveButton_clicked)
        self.ui.transButton.clicked.connect(self.transButton_clicked)
        self.ui.collectButton_2.clicked.connect(self.startStopButton_clicked)
        self.ui.scaleButton.clicked.connect(self.scaleButton_clicked)
        self.ui.absIrrButton.clicked.connect(self.absIrrButton_clicked)
        self.ui.relIrrButton.clicked.connect(self.relIrrButton_clicked)

        ## show the screen
        #######################################################################
        self.show()



    ## BUTTON CLICK FUNCTIONALITY  
    ###########################################################################
    @pyqtSlot()
    def absIrrButton_clicked(self):
        print("abs Irr")

    @pyqtSlot()
    def relIrrButton_clicked(self):
        print("rel Irr")
        print('were gonna do this one')

    # Rescales the graph to allow for a better view
    @pyqtSlot()
    def scaleButton_clicked(self):
        print("scale")
        print("this doesnt work")
        return
        self.ui.graphWidget.ViewBox()
        self.ui.graphWidget_2.ViewBox()

    # creates the transmission data and displays the graph
    @pyqtSlot()
    def transButton_clicked(self):
        globals.visGraph = 4
        y_value = []
        y_label = "Percentage (%)"
        title = "Transmission Mode"
        for x in range(0, len(globals.spectraldata)-2):
            y_value.append(100*((globals.spectraldata[x]-globals.darkData[x])/(globals.refData[x]-globals.darkData[x])))
        self.plot(y_value, y_label, title)

    # creates the absorbance data and displays the graph
    @pyqtSlot()
    def absButton_clicked(self):
        globals.visGraph = 3
        y_value = []
        y_label = "Absorbance (A.U.)"
        title = "Absorbance Mode"
        for x in range(0, len(globals.spectraldata)-2):
            # seems that im grabbing outside pixels making the end of the graph bad... will have to look into it. 
            if math.fabs(globals.refData[x]-globals.darkData[x]) == 0:
                y_value.append(5)
                print("divide by zero")
            elif (math.fabs(globals.spectraldata[x]-globals.darkData[x]))/(math.fabs(globals.refData[x]-globals.darkData[x])) <= 0:
                y_value.append(5)
                print("domain = 0")
            else:
                y_value.append( -1 * math.log((math.fabs(globals.spectraldata[x]-globals.darkData[x]))/(math.fabs(globals.refData[x]-globals.darkData[x])),10))
        self.plot(y_value, y_label, title)

    # creates the reflectance data and displays the graph
    @pyqtSlot()
    def reflectButton_clicked(self):
        globals.visGraph = 5
        y_value = []
        y_label = "Percent (%)"
        title = "Reflectance Mode"
        for x in range(0,len(globals.spectraldata)-2):
            y_value.append( 100*((globals.spectraldata[x]-globals.darkData[x])/(globals.refData[x]-globals.darkData[x])) )
        self.plot(y_value, y_label, title)

    # saves the dark data in globals
    @pyqtSlot()
    def darkButton_clicked(self):
        # saves data
        globals.darkData = globals.spectraldata
        # changes the buttons look to show user that data has been saved
        self.ui.darkButton.setStyleSheet("color: green")
        self.ui.darkButton.setIcon(QIcon("Icons/check.png"))
        print("darkData now saved")

    # disconnects from the spectrometer and adjusts the enabled buttons
    @pyqtSlot()
    def stopButton_clicked(self):
        AVS_Done()
        self.ui.startStopButton.setEnabled(False)
        self.ui.startStopButton.setStyleSheet("background-color: black;")
        self.ui.connectButton.setEnabled(True)
        self.ui.connectButton.setStyleSheet("color: #FFF;")
        self.ui.darkButton.setEnabled(False)
        self.ui.darkButton.setStyleSheet("background-color: black")
        self.ui.configButton.setEnabled(False)
        self.ui.configButton.setStyleSheet("background-color: black")
        self.ui.refButton.setEnabled(False)
        self.ui.refButton.setStyleSheet("background-color: black")
        self.ui.stopButton.setEnabled(False)
        self.ui.stopButton.setStyleSheet("background-color: black")
        self.ui.darkButton.setIcon(QIcon())
        self.ui.refButton.setIcon(QIcon())
        print("disconnected")

    # saves reference data to globals and changes the look of the button to alert user that data has been saved
    @pyqtSlot()
    def refButton_clicked(self):
        globals.refData = globals.spectraldata
        self.ui.refButton.setStyleSheet("color: green")
        self.ui.refButton.setIcon(QIcon("Icons/check.png"))
        print("reference data now saved")

    # configures the spectrometer to ensure that no pixel is saturated
    @pyqtSlot()
    def configButton_clicked(self):
        print("configuration")

        largest_pixel = 0
        count = 0
        increment = 5
        # changes the increment depending on the current integration time... for debugging 
        if globals.integration_time <= 5 and globals.integration_time > 1:
            increment = 1
        elif globals.integration_time <= 1 and globals.integration_time > 0.2:
            increment = 0.5

        # stays in the loop until the largest pixel count is in the range of the loop. slowly adjusts integration time till it gets
        # to the range
        while( largest_pixel > 60000 or largest_pixel < 55000 ):
            largest_pixel = 0
            for x in range(0, len(globals.spectraldata)-2):
                if(globals.spectraldata[x] > largest_pixel):
                    largest_pixel = globals.spectraldata[x]
    
            if globals.integration_time <= 0:
                globals.integration_time = math.fabs(globals.integration_time)

            if globals.integration_time - increment <= 0:
                increment = increment / 2

            if(largest_pixel > 60000):
                # lower the integration time:
                globals.integration_time = globals.integration_time - increment

            if(largest_pixel < 55000):
                # increase integration time: 
                globals.integration_time = globals.integration_time + increment

            # code below allows the user to disconnect from the spectrometer mid configuration
            QtWidgets.QApplication.processEvents()                                        # This works. however ew. 

            # Added a count so the configuration doesn't get stuck in a infinite loop... will eventually exit
            count += 1
            if count == 100:
                break
            # takes another reading
            self.startStopButton_clicked()
        print(largest_pixel)
        globals.max = largest_pixel
        
        # this will adjust the number of averages to get in the cycle_time range... the amount of time to take one reading
        count = 0
        cycle_time = globals.integration_time * globals.averages
        while( cycle_time > 580 or cycle_time < 420):
            cycle_time = globals.integration_time * globals.averages
            if cycle_time > 550: 
                globals.averages -= 1 
            if cycle_time < 450: 
                globals.averages += 1
            self.startStopButton_clicked()
            count += 1 
            if count >= 50:
                break
        print("done with configuration")
        print(globals.integration_time)
        print(globals.averages)   

    # collects data from the spectrometer. collect button. 
    @pyqtSlot()
    def startStopButton_clicked(self):
        # self.startStopButton.setEnabled(False)
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
            # self.app.processEvents()                          
            time.sleep(0.001)  


        globals.measureType = measconfig

        # while globals.first == True:
        #     self.plot_scope()
        #     globals.first = False

        # if globals.visGraph == 1:
        #     print()
        #     self.scope()
        # elif globals.visGraph == 2:
        #     print()
        #     self.scopeMinDarkButton()
        # elif globals.visGraph == 3:
        #     print()
        #     self.absButton()
        # elif globals.visGraph == 4:
        #     print()
        #     self.transButton()
        # elif globals.visGraph == 5:
        #     print()
        #     self.refButton()
        # elif globals.visGraph == 6:
        #     print()
        # elif globals.visGraph == 7:
        #     print()
        # else:
        #     print()
        self.scope()    
        return   

    # connects to the spectrometer
    @pyqtSlot()
    def connectButton_clicked(self):
        print("connected")
        # initialize the usb... were not gonna care about eithernet for now only usb
        ret = AVS_Init(0)                                                                                   # init(0) means were using a USB
                                                                                                            # will return the number of devices on success this should be 1 

        ret = AVS_GetNrOfDevices()                                                                          # will check the list of connected usb devices and returns the number attached   
        mylist = AvsIdentityType()                                                                          # pretty sure these do the same thing but whatever you know it works
        mylist = AVS_GetList(1)          
        globals.identity = mylist                                                                   

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

        # change if the button should be able to be used or not 
        self.ui.startStopButton.setEnabled(True)
        self.ui.startStopButton.setStyleSheet("color: #FFF;")
        self.ui.darkButton.setEnabled(True)
        self.ui.darkButton.setStyleSheet("color: #FFF;")
        self.ui.configButton.setEnabled(True)
        self.ui.configButton.setStyleSheet("color: #FFF;")
        self.ui.refButton.setEnabled(True)
        self.ui.refButton.setStyleSheet("color: #FFF;")
        self.ui.stopButton.setEnabled(True)
        self.ui.stopButton.setStyleSheet("color: #FFF;")
        self.ui.connectButton.setEnabled(False)
        self.ui.connectButton.setStyleSheet("color: #FFF;")
        self.ui.connectButton.setStyleSheet("background-color: black")

        return

    # creates the scope - dark graph and displays it with plot function. 
    @pyqtSlot()
    def scopeMinDarkButton_clicked(self):
        globals.visGraph = 2
        y_value = []
        title = "Scope Minus Dark"
        y_label = "Counts"
        for x in range(0, len(globals.spectraldata)-2):
            y_value.append(globals.spectraldata[x]-globals.darkData[x])
        self.plot(y_value, y_label, title)

    # saves the data of the spectrometer for later use in Avasoft 8. Not finished
    @pyqtSlot()
    def saveButton_clicked(self):
        print("Save Button clicked")
        numpix = globals.measureType.m_StopPixel - globals.measureType.m_StartPixel +1

        # find the file extension and the binary associated with it. 
        # the measuremode binary might not be right rn. 
        fileName = "saveFile"
        extension = ""
        measureMode = ""
        choice = 0
        if(choice == 0):
            extension = ".RAW8"
            measureMode = b"0"
        elif choice == 2:
            extension = ".RWD8"
            measureMode = b"2"
        elif choice == 1:
            extension = ".ABS8"
            measureMode = b"1"
        elif choice == 3:
            extension = ".TRM8"
            measureMode = b"3"
        elif choice == 5:
            extension = ".IRR8"
            measureMode = b"5"
        elif choice == 4:
            extension = ".RFL8"
            measureMode = b"4"
        elif choice == 6:
            extension = ".RIR8"
            measureMode = b"6"
        else:
            extension = ".RAW8"
            measureMode = b"0"
            print("ERROR: DIDN'T FIND FILE TYPE SPECIFIED")

        # write data see what happens
        with open(fileName + extension, "wb") as file:
            # Marker
            file.write(struct.pack("c", b'A'))
            file.write(struct.pack("c", b'V'))
            file.write(struct.pack("c", b'S'))
            file.write(struct.pack("c", b'8'))
            file.write(struct.pack("c", b'4'))
            # Number of spectra 
            file.write(b'1')                                                             # this is going to be 4 bytes and not 1 thats a problem
            # length
            file.write(struct.pack("i", globals.deviceConfig.m_Len))
            # seqnum
            file.write(b'0')
            # measure mode 
            file.write(measureMode)
            # bitness
            file.write(b'1')
                                                                                                        # file.write("00000001")
            #SDmarker
            file.write(b'0')
                                                                                                        # file.write("00000000")
            #identity       
            #                                                                    # this may need to be 10 long intead of 9
                #serial number
            for x in range(0, len(globals.identity[0].SerialNumber)):
                # file.write(eightBits(str(decimalToBinary(globals.identity[0].SerialNumber[x]))))
                file.write(struct.pack('B', globals.identity[0].SerialNumber[x]))


                # user friendly name
            for x in range(0,64):
                if x < 10:
                    if x < len(globals.identity[0].UserFriendlyName):
                        file.write(struct.pack("B", globals.identity[0].UserFriendlyName[x]))
                    else:
                        file.write(b"0")
                else:
                    file.write(b"0")
                # status
            for x in globals.identity[0].Status:
                # print(eightBits(decimalToBinary(x)))
                print(x)
                # file.write(eightBits(decimalToBinary(x)))
            #meascong

            #timestamp                                                                                      DWORD
            for i in range(4):
                file.write(b"0")
            #SPCfiledate                                                                                    DWORD
            for i in range(4):
                file.write(b"0")
            #detectortemp                                                                                   Single
            for i in range(4):
                file.write(b"0")
            #boardtemp                                                                                      Single
            for i in range(4):
                file.write(b"0")
            #NTC2volt                                                                                       Single
            for i in range(4):
                file.write(b"0")
            #colorTemp                                                                                      Single
            for i in range(4):
                file.write(b"0")
            #calIntTime                                                                                     Single
            for i in range(4):
                file.write(b"0")
            #fitdata
            for i in globals.deviceConfig.m_Detector_m_aFit:
                file.write(struct.pack("<d", i))
                print(i)
            #comment                                                                                        AnsiChar
            for i in range(129):
                file.write(b" ")
            #xcoord                                                                                         Should be a short ... long rn
            for x in range(numpix):
                file.write(struct.pack('f', globals.wavelength[x]))                                         
            #scope                                                                                          Should be a short ... long rn
            for x in range(numpix):
                file.write(struct.pack("f", globals.spectraldata[x]))
            #dark                                                                                           Should be a short ... long rn
            for x in range(numpix):
                file.write(struct.pack("f", globals.darkData[x]))
            #reference                                                                                      Should be a short ... long rn
            for x in range(numpix):
                file.write(struct.pack("f", globals.refData[x]))
            #mergegroup
            for x in range(10):
                file.write(b" ")
            #straylightconf
            file.write(struct.pack('?', True))
            file.write(struct.pack("?", False))
            file.write(struct.pack("l", 1))
            file.write(b'0')
            #nonlincong
            file.write(struct.pack("?", False))
            file.write(struct.pack("?", False))
            file.write(b'0')
            #customReflectance
            file.write(b"N")
            #customWhiteRefValue
            for x in range(471):
                file.write(struct.pack("l", 0))
            #customDarkRefValue
            for x in range(471):
                file.write(struct.pack("l", 1))


    ## OTHER FUCNTIONS
    ###########################################################################
    def scope(self):
        # get the values
        globals.visGraph = 1
        y_value = []
        for x in range(0,len(globals.spectraldata)-2):                                  # dropping off the last two data points
            y_value.append(globals.spectraldata[x])
        self.plot(y_value, "Scope (ADC Counts)", "Scope Mode")

    # plots the data to both graphs on page 1 and page 2. 
    def plot(self, y_value, y_label, title):
        # get the values
        x_value = []
        for x in range(0,len(globals.wavelength)-2):                                    # not sure if this is going to effect it but dropping off the last two data points
            x_value.append(globals.wavelength[x])
        
        # Set the label for x axis
        self.ui.graphWidget.setLabel('bottom', 'Wavelength (nm)')
        self.ui.graphWidget_2.setLabel('bottom', 'Wavelength (nm)')

        # Set the label for y-axis
        self.ui.graphWidget.setLabel('left', y_label)
        self.ui.graphWidget_2.setLabel('left', y_label)

        # Set the title of the graph and plots
        self.ui.graphWidget.setTitle(title)
        self.ui.graphWidget_2.setTitle(title)
        self.ui.graphWidget.clear()
        self.ui.graphWidget.plot(x_value, y_value)
        self.ui.graphWidget_2.clear()
        self.ui.graphWidget_2.plot(x_value, y_value)

def decimalToBinary(n):
    # this thing returns a string
    return bin(n).replace("0b", "")

## MAKES A STRING A BYTE SIZE
#############################################
def eightBits(n):
    if len(n) == 1:
        n = "0000000" + n
    elif len(n) == 2:
        n = "000000" + n
    elif len(n) == 3:
        n = "00000" + n
    elif len(n) == 4:
        n = "0000" + n
    elif len(n) == 5:
        n = "000" + n
    elif len(n) == 6:
        n = "00" + n
    elif len(n) == 7:
        n = "0" + n
    else:
        print("eight bits")
        return n
    return n

## CONVERTS DECIMAL TO BINARY
###############################################
def double_to_binary(num):
    # convert to binary using IEEE 754
    print("decimal to binary")
    print(float.hex(num))
    bin = ''
    # find the initial bit to see if its negative or not
    if num < 0:
        bin += "1"
    else:
        bin += "0"

    # find the exponent in scientific notation 
    # can potenially have a 4 digit exponent 2 ^ 11 
    string = "{:e}".format(num)
    val = ''
    for i in range(4,-1, -1):
        if string[len(string)-1-i] != "e":
            val += string[len(string)-1-i]
        if string[len(string)-1-i] == "e":
            val = ""
    exponent = int(val) + 1023

    # return the value
    return bin


## MAIN
###########################################################################
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
