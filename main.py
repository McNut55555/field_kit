# from re import L, S
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QFileDialog , QInputDialog
from pyqtgraph import PlotWidget, plot, ViewBox
import pyqtgraph as pg
import sys                                                                      # We need sys so that we can pass argv to QApplication
from pyqtgraph.functions import Color
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
        globals.visGraph = 0

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
        self.ui.connectButton.clicked.connect(self.connectButton_clicked)
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

    # Rescales the graph to allow for a better view
    @pyqtSlot()
    def scaleButton_clicked(self):
        print("scale")
        print("this doesnt work")
        return
        self.ui.graphWidget.ViewBox()
        self.ui.graphWidget_2.ViewBox()
        return

    # saves the dark data in globals
    @pyqtSlot()
    def darkButton_clicked(self):
        # saves data
        globals.darkData = globals.spectraldata
        # changes the buttons look to show user that data has been saved
        self.ui.darkButton.setStyleSheet("color: green")
        self.ui.darkButton.setIcon(QIcon("Icons/check.png"))
        print("darkData now saved")
        return

    # saves reference data to globals and changes the look of the button to alert user that data has been saved
    @pyqtSlot()
    def refButton_clicked(self):
        globals.refData = globals.spectraldata
        self.ui.refButton.setStyleSheet("color: green")
        self.ui.refButton.setIcon(QIcon("Icons/check.png"))
        print("reference data now saved")
        return

    '''
    configures the spectrometer to ensure that no pixel is saturated. Does this by slowly incrementing the the integration time. 
    One the largest pixel is between 60,000 and 55,000 the integration time gets set to that value. It then slowly adjusts the 
    number of averages so that each 
    '''
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
        # I think this value is in seconds but im not quite sure. 
        count = 0
        cycle_time = 500
        globals.averages = int(cycle_time / globals.integration_time)
        if globals.averages > 100:
            globals.averages = 100
        elif globals.averages < 2:
            globals.averages = 2
        print("done with configuration")
        print('cycle time:', cycle_time)
        print("integration time:", globals.integration_time)
        print("Averages:", globals.averages)   
        return

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
        return


    # collects data from the spectrometer. collect button. 
    @pyqtSlot()
    def startStopButton_clicked(self):
        self.repaint()                                                                      # gets rid of old data on the screen
        ret = AVS_UseHighResAdc(globals.dev_handle, True)                                   # sets the spectrometer to use 16 bit resolution instead of 14 bit

        # set the configuration
        measconfig = MeasConfigType()
        measconfig.m_StartPixel = 0
        measconfig.m_StopPixel = globals.pixels - 1
        measconfig.m_IntegrationTime = globals.integration_time                             # variables that will get changed
        measconfig.m_IntegrationDelay = 0
        measconfig.m_NrAverages = globals.averages                                          # variables that will get changed
        measconfig.m_CorDynDark_m_Enable = 0                                                # nesting of types does NOT work!!
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
        
        # choosing what graph should be displayed to the user
        if globals.visGraph == 0:
            self.scope()
        elif globals.visGraph == 2:
            self.scopeMinDarkButton_clicked()
        elif globals.visGraph == 1:
            self.absButton_clicked()
        elif globals.visGraph == 3:
            self.transButton_clicked()
        elif globals.visGraph == 4:
            self.refButton_clicked()
        elif globals.visGraph == 6:
            self.absIrrButton_clicked()
        elif globals.visGraph == 7:
            self.relIrrButton_clicked()
        else:
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

        # set the number of pixels the spectrometer has
        globals.pixels = AVS_GetNumPixels(globals.dev_handle)
        print(globals.pixels)

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


    # saves the data of the spectrometer for later use in Avasoft 8. Not finished
    @pyqtSlot()
    def saveButton_clicked(self):
        """
        This function saves the data of the spectrometer in a format so that Avasoft 8 will be able to open the data. 
        """
        print("Save Button clicked")
        numpix = globals.measureType.m_StopPixel - globals.measureType.m_StartPixel +1

        # find the file extension and the binary associated with it. 
        # the measuremode binary might not be right rn. 
        fileName = "avalight"
        extension = ""
        measureMode = ""
        choice = 0
        comment = ""

        # Get the comment from the user
        # here the comment is what the user inputs and result is if it was 
        comment, result = QInputDialog.getText(self, "Input", "Add Comment")

        # This will get the file path where the user would like to save the file. 
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        save_path, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","", options=options)

        # Get the extension of the file. This is what type of file the user would like to save
        if(globals.visGraph == 0):
            extension = ".RAW8"
            measureMode = b"\00"
        elif globals.visGraph == 2:
            extension = ".RWD8"
            measureMode = b"\02"
        elif globals.visGraph == 1:
            extension = ".ABS8"
            measureMode = b"\01"
        elif globals.visGraph == 3:
            extension = ".TRM8"
            measureMode = b"\03"
        elif globals.visGraph == 5:
            extension = ".IRR8"
            measureMode = b"\05"
        elif globals.visGraph == 4:
            extension = ".RFL8"
            measureMode = b"\04"
        elif globals.visGraph == 6:
            extension = ".RIR8"
            measureMode = b"\06"
        else:
            extension = ".RAW8"
            measureMode = b"\00"
            print("ERROR: DIDN'T FIND FILE TYPE SPECIFIED")

        # write data to the file
        with open(save_path + extension, "wb") as file:
            # Marker
            file.write(struct.pack("c", b'A'))
            file.write(struct.pack("c", b'V'))
            file.write(struct.pack("c", b'S'))
            file.write(struct.pack("c", b'8'))
            file.write(struct.pack("c", b'4'))
            # Number of spectra 
            file.write(struct.pack("B", 1))                                         
            # length
            file.write(struct.pack("<i", globals.deviceConfig.m_Len))
            print(globals.deviceConfig.m_Len)
            # seqnum    1
            file.write(b'\x00')
            # measure mode  1
            file.write(measureMode)
            # bitness   1
            file.write(b'\x00')
            #SDmarker   1
            file.write(b'\x00')
            #identity  75        
            #                                                                    # this may need to be 10 long intead of 9
            for x in range(0, len(globals.identity[0].SerialNumber)):
                file.write(struct.pack('<B', globals.identity[0].SerialNumber[x]))
            for x in range(0, 10- len(globals.identity[0].SerialNumber)):
                file.write(b'\x00')
            for x in globals.identity[0].UserFriendlyName:
                file.write(struct.pack("<B", x))
            for x in range(0,64-len(globals.identity[0].UserFriendlyName)):
                file.write(b'\x04')
            for x in globals.identity[0].Status:
                file.write(struct.pack("<B", x))
            #meascong
                # m_StartPixel
            file.write(struct.pack("<H", globals.measureType.m_StartPixel))
                # m_stopPixel
            file.write(struct.pack("<H", globals.measureType.m_StopPixel))
                # m_IntegrationTime single
            file.write(struct.pack("<f", globals.measureType.m_IntegrationTime))
                # m_IntegrationDelay
            file.write(struct.pack("<L", globals.measureType.m_IntegrationDelay))
                # m_NrAverages
            file.write(struct.pack("<L", globals.measureType.m_NrAverages))
                # m_CorDynDark
                    # m_Enable
            file.write(struct.pack("<B", globals.measureType.m_CorDynDark_m_Enable))
                    # m_ForgetPercentage
            file.write(struct.pack("<B", globals.measureType.m_CorDynDark_m_ForgetPercentage))
                # m_Smoothing
            file.write(struct.pack("<e", globals.measureType.m_Smoothing_m_SmoothPix))
            file.write(struct.pack("<B", globals.measureType.m_Smoothing_m_SmoothModel))
                # SaturationDetection
            file.write(struct.pack("<B", globals.measureType.m_SaturationDetection))
                # m_Trigger
            file.write(struct.pack("<B", globals.measureType.m_Trigger_m_Mode))
            file.write(struct.pack("<B", globals.measureType.m_Trigger_m_Source))
            file.write(struct.pack("<B", globals.measureType.m_Trigger_m_SourceType))
                # m_Control
            file.write(struct.pack("<H", globals.measureType.m_Control_m_StrobeControl))
            file.write(struct.pack("<I", globals.measureType.m_Control_m_LaserDelay))
            file.write(struct.pack("<I", globals.measureType.m_Control_m_LaserWidth))
            file.write(struct.pack("<f", globals.measureType.m_Control_m_LaserWaveLength))
            file.write(struct.pack("<H", globals.measureType.m_Control_m_StoreToRam))
            #timestamp                                                                                      DWORD
            for i in range(4):
                file.write(struct.pack("<B", 1))
            #SPCfiledate                                                                                    DWORD
            for i in range(4):
                file.write(struct.pack("<B", 1))
            #detectortemp                                                                                   Single
            for i in range(4):
                file.write(struct.pack("<B", 1))
            #boardtemp                                                                                      Single
            for i in range(4):
                file.write(struct.pack("<B", 1))
            #NTC2volt                                                                                       Single
            for i in range(4):
                file.write(struct.pack("<B", 1))
            #colorTemp                                                                                      Single
            for i in range(4):
                file.write(struct.pack("<B", 1))
            #calIntTime                                                                                     Single
            for i in range(4):
                file.write(b"E")
            #fitdata
            for i in globals.deviceConfig.m_Detector_m_aFit:
                file.write(struct.pack("<d", i))
            #comment                                                                                        AnsiChar
            if len(comment) <= 129:
                for i in comment:
                    file.write(struct.pack("c", bytes(i, 'utf-8')))
                for i in range(129-len(comment)):
                    file.write(b'\00')
            else:
                for i in range(129):
                    file.write(struct.pack("c", bytes(comment[i], 'utf-8')))
            file.write(b"\01")                                                                              # for some reason the file that gets saved has a seperator here
            #xcoord                                                                                         Should be a short ... long rn
            for x in range(numpix):
                file.write(struct.pack('<f', globals.wavelength[x]))   
            #scope                                                                                          Should be a short ... long rn
            for x in range(numpix):
                file.write(struct.pack("<f", globals.spectraldata[x]))
            #dark                                                                                           Should be a short ... long rn
            for x in range(numpix):
                file.write(struct.pack("<f", globals.darkData[x]))
            #reference                                                                                      Should be a short ... long rn
            for x in range(numpix):
                file.write(struct.pack("<f", globals.refData[x]))
            #mergegroup
            for x in range(10):
                file.write(b"\00")
            #straylightconf
            file.write(struct.pack('<?', False))
            file.write(struct.pack("<?", False))
            file.write(struct.pack("<l", 1))
            file.write(b'\00')
            #nonlincong
            file.write(struct.pack("<?", False))
            file.write(struct.pack("<?", False))
            file.write(b'\00')
            #customReflectance
            file.write(b"N")
            #customWhiteRefValue
            for x in range(471):
                file.write(struct.pack("<l", 0))
            #customDarkRefValue
            for x in range(471):
                file.write(struct.pack("<l", 0))
        return

            
    ## OTHER FUCNTIONS
    ###########################################################################
    def saveFileDialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","", options=options)

        if fileName:
            print(fileName)
        return

    def scope(self):
        # get the values
        globals.visGraph = 0
        y_value = []
        for x in range(21,globals.pixels-22):                                  # dropping off the last two data points
            y_value.append(globals.spectraldata[x])
            if globals.spectraldata[x] == 0:
                print("x value", x)
        self.plot(y_value, "Scope (ADC Counts)", "Scope Mode")
        return

    # creates the absorbance data and displays the graph
    @pyqtSlot()
    def absButton_clicked(self):
        globals.visGraph = 1
        y_value = []
        y_label = "Absorbance (A.U.)"
        title = "Absorbance Mode"
        for x in range(21, globals.pixels-22):
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
        return

    # creates the transmission data and displays the graph
    @pyqtSlot()
    def transButton_clicked(self):
        globals.visGraph = 3
        y_value = []
        y_label = "Percentage (%)"
        title = "Transmission Mode"
        for x in range(21, globals.pixels-22):
            y_value.append(100*((globals.spectraldata[x]-globals.darkData[x])/(globals.refData[x]-globals.darkData[x])))
        self.plot(y_value, y_label, title)
        return
        
    # creates the scope - dark graph and displays it with plot function. 
    @pyqtSlot()
    def scopeMinDarkButton_clicked(self):
        globals.visGraph = 2
        y_value = []
        title = "Scope Minus Dark"
        y_label = "Counts"
        for x in range(21, globals.pixels-22):
            y_value.append(globals.spectraldata[x]-globals.darkData[x])
        self.plot(y_value, y_label, title)
        return

    # creates the reflectance data and displays the graph
    @pyqtSlot()
    def reflectButton_clicked(self):
        globals.visGraph = 4
        y_value = []
        y_label = "Percent (%)"
        title = "Reflectance Mode"
        for x in range(21, globals.pixels-22):
            y_value.append( 100*((globals.spectraldata[x]-globals.darkData[x])/(globals.refData[x]-globals.darkData[x])) )
        self.plot(y_value, y_label, title)
        return

    @pyqtSlot()
    def absIrrButton_clicked(self):
        globals.visGraph = 5
        print("abs Irr")
        print(globals.deviceConfig.m_Irradiance_m_IntensityCalib_m_Smoothing_m_SmoothPix)
        print(globals.deviceConfig.m_Irradiance_m_IntensityCalib_m_Smoothing_m_SmoothModel)
        print(globals.deviceConfig.m_Irradiance_m_IntensityCalib_m_CalInttime)
        print(type(globals.deviceConfig.m_Irradiance_m_IntensityCalib_m_aCalibConvers))                       # array
        for i in range(globals.pixels):
            print(globals.deviceConfig.m_Irradiance_m_IntensityCalib_m_aCalibConvers[i])
        print(globals.pixels)
        print(globals.deviceConfig.m_Irradiance_m_CalibrationType)
        print(globals.deviceConfig.m_Irradiance_m_FiberDiameter)
        return

    @pyqtSlot()
    def relIrrButton_clicked(self):
        globals.visGraph = 6
        print("rel Irr")
        print('were gonna do this one')
        return


    # plots the data to both graphs on page 1 and page 2. 
    def plot(self, y_value, y_label, title):
        # get the values
        x_value = []
        for x in range(21,globals.pixels-22):                                    # not sure if this is going to effect it but dropping off the last two data points
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
        return


## MAIN
###########################################################################
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
