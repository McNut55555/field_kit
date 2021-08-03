# from re import L, S
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog , QInputDialog
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


## MAIN WINDOW CLASS
##########################################################
class MainWindow(QtWidgets.QMainWindow):

    '''
    Functionality: This is the function that get called when a MainWindow object is created. This sets up the
    inital state for the field_kit. It also links all the buttons to the associated function within the MainWindow
    class. It also sets up the allowable clicks for the user and the color of each button. As well as some inital 
    global variables that are used in later functions. 
    '''
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
        self.ui.SingleButton.setChecked(True)
        self.ui.intApply.setEnabled(False)
        self.ui.avgApply.setEnabled(False)
        self.ui.avgApply.setStyleSheet("background-color : black")
        self.ui.intApply.setStyleSheet("background-color : black")
        self.ui.startApply.setEnabled(False)
        self.ui.stopApply.setEnabled(False)
        self.ui.startApply.setStyleSheet("background-color : black")
        self.ui.stopApply.setStyleSheet("background-color : black")

        self.ui.collectButton_2.setEnabled(False)
        self.ui.scopeModeButton.setEnabled(False)
        self.ui.scopeMinDarkButton.setEnabled(False)
        self.ui.absButton.setEnabled(False)
        self.ui.transButton.setEnabled(False)
        self.ui.reflectButton.setEnabled(False)
        self.ui.absIrrButton.setEnabled(False)
        self.ui.relIrrButton.setEnabled(False)
        self.ui.saveButton.setEnabled(False)
        self.ui.collectButton_2.setStyleSheet("background-color : black")
        self.ui.scopeModeButton.setStyleSheet("background-color : black")
        self.ui.scopeMinDarkButton.setStyleSheet("background-color : black")
        self.ui.absButton.setStyleSheet("background-color : black")
        self.ui.transButton.setStyleSheet("background-color : black")
        self.ui.reflectButton.setStyleSheet("background-color : black")
        self.ui.absIrrButton.setStyleSheet("background-color : black")
        self.ui.relIrrButton.setStyleSheet("background-color : black")
        self.ui.saveButton.setStyleSheet('background-color : black')

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
        self.ui.absIrrButton.clicked.connect(self.absIrrButton_clicked)
        self.ui.relIrrButton.clicked.connect(self.relIrrButton_clicked)
        self.ui.stopApply.clicked.connect(self.setStopWavelength)
        self.ui.startApply.clicked.connect(self.setStartWavelength)
        self.ui.intApply.clicked.connect(self.setIntegration)
        self.ui.avgApply.clicked.connect(self.setAverages)
        self.ui.measureTypeApply.clicked.connect(self.applyMeasureType)

        ## Disabling panning in x and y directions on graph
        ##########################################################
        self.ui.graphWidget.setMouseEnabled(False, False)
        self.ui.graphWidget_2.setMouseEnabled(False, False)

        ## show the screen
        #######################################################################
        self.show()


    ## BUTTON CLICK FUNCTIONALITY  
    ###########################################################################
    '''
    parameters: self
    return: None
    functionality: this will switch the global data type continuous to true or false. Depending on the 
    global variable is how the stop start button will work. 
    BUG: The continuous measure mode doesn't work properly. Needs work.
    '''
    @pyqtSlot()
    def applyMeasureType(self):
        if self.ui.SingleButton.isChecked():
            globals.continuous = False
            print("Single Measurement")
        else:
            globals.continuous = True
            print("Continuous Applied")
    '''
    parameters: self
    return: None 
    functionality: This sets the integration time of the spectrometer manually. 
    '''
    @pyqtSlot()
    def setIntegration(self):
        # reset the look of dark and reference 
        self.ui.darkButton.setIcon(QIcon())
        self.ui.refButton.setIcon(QIcon())
        self.ui.darkButton.setStyleSheet("color: white")
        self.ui.refButton.setStyleSheet("color: white")

        # actual meat
        x = self.ui.intEdit.toPlainText()
        for i in range(len(x)):
            print('x[i]:', x[i], 'type:', type(x[i]))
            if x[i].isdigit() == False and x[i] != ".":
                QMessageBox.warning(self, "Warning", "Please enter a valid number")
                return
        globals.integration_time = float(x)
        return

    '''
    parameters: self
    return: None
    functionality: Will change the value set in globals averages with the data in the avgEdit.
    '''
    @pyqtSlot()
    def setAverages(self):
        # reset the look of dark and reference 
        self.ui.darkButton.setIcon(QIcon())
        self.ui.refButton.setIcon(QIcon())
        self.ui.darkButton.setStyleSheet("color: white")
        self.ui.refButton.setStyleSheet("color: white")

        # actual code associated with function
        x = self.ui.avgEdit.toPlainText()
        for i in range(len(x)):
            print('x[i]:', x[i], 'type:', type(x[i]))
            if x[i].isdigit() == False and x[i] != ".":
                QMessageBox.warning(self, "Warning", "Please enter a valid number")
                return
        x = float(x)
        globals.averages = int(x)
        self.ui.avgEdit.clear()
        self.ui.avgEdit.append(str(int(x)))
        return

    '''
    parameters: self
    return: none
    functionality: This function stores the dark data to the globals file when the dark button is clicked. It 
    then changes the look of the button so the user knows that the data has been stored. The dark informtion 
    is used to generate other types of graphs. 
    '''
    # saves the dark data in globals
    @pyqtSlot()
    def darkButton_clicked(self):
        # saves data
        globals.darkData = globals.spectraldata
        globals.darkTrue = True
        # changes the buttons look to show user that data has been saved
        self.ui.scopeMinDarkButton.setEnabled(True)
        self.ui.scopeMinDarkButton.setStyleSheet("color: #FFF;")
        self.ui.darkButton.setStyleSheet("color: green")
        self.ui.darkButton.setIcon(QIcon("Icons/check.png"))
        if globals.darkTrue and globals.refTrue:
            self.ui.absButton.setEnabled(True)
            self.ui.transButton.setEnabled(True)
            self.ui.reflectButton.setEnabled(True)
            self.ui.absIrrButton.setEnabled(True)
            self.ui.relIrrButton.setEnabled(True)
            self.ui.saveButton.setEnabled(True)
            self.ui.absButton.setStyleSheet("color: #FFF;")
            self.ui.transButton.setStyleSheet("color: #FFF;")
            self.ui.reflectButton.setStyleSheet("color: #FFF;")
            self.ui.absIrrButton.setStyleSheet("color: #FFF;")
            self.ui.relIrrButton.setStyleSheet("color: #FFF;")
            self.ui.saveButton.setStyleSheet("color: #FFF;")
        print("darkData now saved")
        return

    '''
    paramaters: self
    return: none
    functionality: This function stores data to globals when the refrence button is clicked. it then changes the look 
    of the button so the user knows that the data has been saved.
    '''
    # saves reference data to globals and changes the look of the button to alert user that data has been saved
    @pyqtSlot()
    def refButton_clicked(self):
        globals.refData = globals.spectraldata
        globals.refTrue = True
        if globals.darkTrue and globals.refTrue:
            self.ui.absButton.setEnabled(True)
            self.ui.transButton.setEnabled(True)
            self.ui.reflectButton.setEnabled(True)
            self.ui.absIrrButton.setEnabled(True)
            self.ui.relIrrButton.setEnabled(True)
            self.ui.saveButton.setEnabled(True)
            self.ui.absButton.setStyleSheet("color: #FFF;")
            self.ui.transButton.setStyleSheet("color: #FFF;")
            self.ui.reflectButton.setStyleSheet("color: #FFF;")
            self.ui.absIrrButton.setStyleSheet("color: #FFF;")
            self.ui.relIrrButton.setStyleSheet("color: #FFF;")
            self.ui.saveButton.setStyleSheet("color: #FFF;")
        self.ui.refButton.setStyleSheet("color: green")
        self.ui.refButton.setIcon(QIcon("Icons/check.png"))
        print("reference data now saved")
        return

    '''
    Parameters: self
    return: none
    functionality: configures the spectrometer to ensure that no pixel is saturated. Does this by slowly incrementing the the integration time. 
    One the largest pixel is between 60,000 and 55,000 the integration time gets set to that value. It then slowly adjusts the 
    number of averages so that each 
    BUG: htting the configure button twice in a row doesn't work properly all the time and requires the user to 
    hit it more then once 
    '''
    # @pyqtSlot()
    def configButton_clicked(self):
        print("configuration")

        # reset the look of dark and reference 
        self.ui.darkButton.setIcon(QIcon())
        self.ui.refButton.setIcon(QIcon())
        self.ui.darkButton.setStyleSheet("color: white")
        self.ui.refButton.setStyleSheet("color: white")

        # declare variables
        globals.config = True
        globals.refTrue = False
        globals.darkTrue = False
        globals.averages = 2
        largest_pixel = 0
        count = 0
        increment = globals.integration_time / 2

        # changes the increment depending on the current integration time... for debugging 
        # if globals.integration_time <= 5 and globals.integration_time > 1:
        #     increment = 1
        # elif globals.integration_time <= 1 and globals.integration_time > 0.2:
        #     increment = 0.5

        # stays in the loop until the largest pixel count is in the range of the loop. slowly adjusts integration time till it gets
        # to the range
        while( largest_pixel > 60000 or largest_pixel < 52500 ):
            largest_pixel = 0
            for x in range(0, len(globals.spectraldata)-2):
                if(globals.spectraldata[x] > largest_pixel):
                    largest_pixel = globals.spectraldata[x]
    
            if globals.integration_time <= 0:
                globals.integration_time = math.fabs(globals.integration_time)

            if globals.integration_time - increment <= 0:
                increment = increment / 2

            # change the integration time so it can't go negative
            if(largest_pixel > 60000):
                globals.integration_time = globals.integration_time - increment
            if(largest_pixel < 55000): 
                globals.integration_time = globals.integration_time + increment

            # code below allows the user to disconnect from the spectrometer mid configuration
            QtWidgets.QApplication.processEvents()                                        # This works. however ew. 

            # Added a count so the configuration doesn't get stuck in a infinite loop... will eventually exit
            if count == 15:
                increment = increment / 2
            elif count == 30:
                increment = increment / 2
            if count == 100:
                break
            count += 1

            # setting a minimum integration time... this one is for the mini
            if globals.integration_time <= 0.03:
                QMessageBox.warning(self, "minimum integration time", "Cannot go below 30 micro seconds")
                return

            # takes another reading
            self.startStopButton_clicked()
        largest_pixel = 0
        
        # this will adjust the number of averages to get in the cycle_time range... the amount of time to take one reading 
        # I think this value is in seconds but im not quite sure. 
        globals.config = False
        count = 0
        cycle_time = 500
        globals.averages = int(cycle_time / globals.integration_time)
        if globals.averages > 100:
            globals.averages = 100
        elif globals.averages < 2:
            globals.averages = 2
        print('largest pixel', largest_pixel)
        print('cycle time:', cycle_time)
        print("integration time:", globals.integration_time)
        print("Averages:", globals.averages)   
        print("done with configuration")

        # changing format
        self.ui.scopeMinDarkButton.setEnabled(False)
        self.ui.absButton.setEnabled(False)
        self.ui.transButton.setEnabled(False)
        self.ui.reflectButton.setEnabled(False)
        self.ui.absIrrButton.setEnabled(False)
        self.ui.relIrrButton.setEnabled(False)
        self.ui.scopeMinDarkButton.setStyleSheet("background-color : black;")
        self.ui.absButton.setStyleSheet("background-color : black;")
        self.ui.transButton.setStyleSheet("background-color : black;")
        self.ui.reflectButton.setStyleSheet("background-color : black;")
        self.ui.absIrrButton.setStyleSheet("background-color : black;")
        self.ui.relIrrButton.setStyleSheet("background-color : black;")
        self.ui.intEdit.clear()
        self.ui.avgEdit.clear()
        self.ui.intEdit.append(str(round(globals.integration_time,2)))
        self.ui.avgEdit.append(str(round(globals.averages,2)))
        
        return

    '''
    parameters:
    return:
    functionality: This fucntion disconnects the spectrometer when the stop button in the Gui is pressed. 
    It then resets some of the access to buttons for the user. 
    '''
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
        self.ui.intApply.setEnabled(False)
        self.ui.avgApply.setEnabled(False)
        self.ui.avgApply.setStyleSheet("background-color : black")
        self.ui.intApply.setStyleSheet("background-color : black")
        self.ui.startApply.setEnabled(False)
        self.ui.stopApply.setEnabled(False)
        self.ui.startApply.setStyleSheet("background-color : black")
        self.ui.stopApply.setStyleSheet("background-color : black")

        self.ui.collectButton_2.setEnabled(False)
        self.ui.scopeMinDarkButton.setEnabled(False)
        self.ui.scopeModeButton.setEnabled(False)
        self.ui.absButton.setEnabled(False)
        self.ui.transButton.setEnabled(False)
        self.ui.reflectButton.setEnabled(False)
        self.ui.relIrrButton.setEnabled(False)
        self.ui.absIrrButton.setEnabled(False)
        self.ui.saveButton.setEnabled(False)

        # setting the background color of all the buttons
        self.ui.collectButton_2.setStyleSheet("background-color : black")
        self.ui.scopeModeButton.setStyleSheet("background-color : black")
        self.ui.scopeMinDarkButton.setStyleSheet("background-color : black")
        self.ui.absButton.setStyleSheet("background-color : black")
        self.ui.transButton.setStyleSheet("background-color : black")
        self.ui.reflectButton.setStyleSheet("background-color : black")
        self.ui.absIrrButton.setStyleSheet("background-color : black")
        self.ui.relIrrButton.setStyleSheet("background-color : black")
        self.ui.saveButton.setStyleSheet("background-color : black")
        print("disconnected")
        return

    '''
    parameters:
    return:
    functionality: This fuction is for when the collect Button on the GUI is pressed. It collects data from 
    the spectrometer. Then it chooses what graph the user wants displayed and displayes that graph. It chooses 
    the graph by what last graph was chosen to be displayed. 
    BUG: This is where the continuous scanning mode is implemented. The continuous scanning mode doesn't work. 
    Seems that it requires parallel programming. 
    '''
    # collects data from the spectrometer. collect button. 
    @pyqtSlot()
    def startStopButton_clicked(self):
        if AVS_GetNrOfDevices() == 0:
            self.stopButton_clicked()
            QMessageBox.warning(self, "Disconnected", "No Spectrometer found")
            exit
        self.repaint()                                                                      # gets rid of old data on the screen
        ret = AVS_UseHighResAdc(globals.dev_handle, True)                                   # sets the spectrometer to use 16 bit resolution instead of 14 bit

        self.ui.startStopButton.setIcon(QIcon("/Icons/loading.png"))

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
        ret = AVS_PrepareMeasure(globals.dev_handle, measconfig)                                                                      # variables that will get changed

        # this is where the program decides if the measurments should be continuous or not
        if globals.continuous == False or globals.config == True:
            nummeas = 1 
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

        else:
            nummeas = 10
            scans = 0 
            globals.stopscanning = False
            while(globals.stopscanning == False):
                ret = AVS_Measure(globals.dev_handle,0,1)
                dataready = False
                while dataready ==False:
                    dataready = (AVS_PollScan(globals.dev_handle) == True)
                    time.sleep(0.001)
                if dataready == True:
                    ret = AVS_GetScopeData(globals.dev_handle)
                    globals.spectraldata = ret[1]
                    scans = scans + 1 
                    print("yup")
                    if (scans >= nummeas):
                        globals.stopscanning = True
                    QApplication.processEvents()
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

        self.ui.avgEdit.clear()
        self.ui.intEdit.clear()
        self.ui.intEdit.append(str(round(globals.integration_time,2)))
        self.ui.avgEdit.append(str(round(globals.averages,2)))
        self.ui.refButton.setIcon(QIcon())
        return   

    '''
    parameters: self
    return: none
    functonality: This function is for when the connect button in the GUI is clicked. It will connect to the 
    spectrometer and get all necessary information from it. It will then change the activated buttons to the 
    user and other stuff for the GUI.
    '''
    # connects to the spectrometer
    @pyqtSlot()
    def connectButton_clicked(self):
        # initialize the usb... were not gonna care about eithernet for now only usb
        ret = AVS_Init(0)                                                                                   # init(0) means were using a USB
        if ret == 0:
            QMessageBox.warning(self, "No spectrometer", "No Spectrometer connected")
            return

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
        print('Pixels:', globals.pixels)

        # gets all the information about the spectrometer
        devcon = DeviceConfigType()
        devcon = AVS_GetParameter(globals.dev_handle, 63484)
        globals.deviceConfig = devcon
        globals.pixels = devcon.m_Detector_m_NrPixels
        globals.high = globals.pixels - 24
        globals.wavelength = AVS_GetLambda(globals.dev_handle)

        # changing users access to buttons and look
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
        self.ui.stopEdit.clear()
        self.ui.startEdit.clear()
        self.ui.stopEdit.append(str(round(globals.wavelength[len(globals.wavelength)-23],3)))
        self.ui.startEdit.append(str(round(globals.wavelength[0],3)))
        self.ui.intApply.setEnabled(True)
        self.ui.avgApply.setEnabled(True)
        self.ui.intApply.setStyleSheet("color: #FFF;")
        self.ui.avgApply.setStyleSheet("color: #FFF;")
        self.ui.startApply.setEnabled(True)
        self.ui.stopApply.setEnabled(True)
        self.ui.startApply.setStyleSheet("color: #FFF;")
        self.ui.stopApply.setStyleSheet("color: #FFF;")
        self.ui.collectButton_2.setEnabled(True)
        self.ui.scopeModeButton.setEnabled(True)
        self.ui.collectButton_2.setStyleSheet("color: #FFF;")
        self.ui.scopeModeButton.setStyleSheet("color: #FFF;")

        # return message
        print("connected")
        return


    # saves the data of the spectrometer for later use in Avasoft 8. Not finished
    '''
    parameters:
    return:"
    functionality: This function main purpose is to save a file so that the data can then be opened in 
    Avasoft 8. This is done by saving all the data in the file format given by the file format document. 
    All the data is saved in little endian. Some of the full functionality isn't finished. Some of the data 
    in the save isn't right. Like date and time when the spectrum was collected. Doesn't seem overly important 
    yet.
    '''
    @pyqtSlot()
    def saveButton_clicked(self):
        """
        This function saves the data of the spectrometer in a format so that Avasoft 8 will be able to open the data.
        It asks the user for a comment and where to save the file. The file extension that it chooses will be the 
        last graph that was displayed to the user/displaying to the user. The format of the file can be found in the 
        file format manuel.
        """
        print("Save Button clicked")
        numpix = globals.measureType.m_StopPixel - globals.measureType.m_StartPixel +1

        # find the file extension and the binary associated with it. 
        # the measuremode binary might not be right rn. 
        fileName = "avalight"
        extension = ""
        measureMode = ""
        comment = ""

        # Get the comment from the user
        # here the comment is what the user inputs and result is if it was 
        comment, result = QInputDialog.getText(self, "Input", "Add Comment")

        # This will get the file path where the user would like to save the file. 
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","", options=options)

        # Get the extension of the file. This is what type of file the user would like to save
        # currently just saves the graph of the graph being displayed. 
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

    '''
    paramters: self
    return: none
    functionality: This function will get all the scope data and will pass it to the plot function to be 
    displayed to the user. 
    '''
    def scope(self):
        # get the values
        globals.visGraph = 0
        y_value = []
        for x in range(globals.low,globals.high):                                  # dropping off the last two data points
            y_value.append(globals.spectraldata[x])
        self.plot(y_value, "Scope (ADC Counts)", "Scope Mode")
        return

    '''
    parameters: self
    return: none
    functionality: Makes an array tht stores the absorbance data in it. This array is then passed to plot to be 
    displayed to the user.
    '''
    # creates the absorbance data and displays the graph
    @pyqtSlot()
    def absButton_clicked(self):
        globals.visGraph = 1
        y_value = []
        y_label = "Absorbance (A.U.)"
        title = "Absorbance Mode"
        for x in range(globals.low, globals.high):
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

    '''
    parameters:
    return:
    Functionality: This function will find all the transmission data and then will pass this information to the 
    plot function to be displayed to the user. 
    '''
    # creates the transmission data and displays the graph
    @pyqtSlot()
    def transButton_clicked(self):
        globals.visGraph = 3
        y_value = []
        y_label = "Percentage (%)"
        title = "Transmission Mode"
        for x in range(globals.low, globals.high):
            if globals.refData[x]-globals.darkData[x] == 0:
                print("float division by zero")
                y_value.append(100)
            else:
                y_value.append(100*((globals.spectraldata[x]-globals.darkData[x])/(globals.refData[x]-globals.darkData[x])))
        self.plot(y_value, y_label, title)
        return
        
    '''
    parameters:
    return:
    functionality: This function will find the scope minus the dark data and then will pass this information 
    to the plot function to be displayed to the user. 
    '''
    # creates the scope - dark graph and displays it with plot function. 
    @pyqtSlot()
    def scopeMinDarkButton_clicked(self):
        globals.visGraph = 2
        y_value = []
        title = "Scope Minus Dark"
        y_label = "Counts"
        for x in range(globals.low, globals.high):
            y_value.append(globals.spectraldata[x]-globals.darkData[x])
        self.plot(y_value, y_label, title)
        return

    '''
    parameters:
    return:
    functionality: This function will find all the reflectance data and will then pass that to the plot 
    function to be displayed to the user.
    '''
    # creates the reflectance data and displays the graph
    @pyqtSlot()
    def reflectButton_clicked(self):
        globals.visGraph = 4
        y_value = []
        y_label = "Percent (%)"
        title = "Reflectance Mode"
        for x in range(globals.low, globals.high):
            if (globals.refData[x]-globals.darkData[x]) == 0:
                print("float division by zero")
                y_value.append(100)
            else:
                y_value.append( 100*((globals.spectraldata[x]-globals.darkData[x])/(globals.refData[x]-globals.darkData[x])) )
        self.plot(y_value, y_label, title)
        return

    '''
    parameters: self
    return:
    functionality: This fucntion will find the absolute irradiance values. It will then pass these values
    to be graphed by the plot function. 
    '''
    @pyqtSlot()
    def absIrrButton_clicked(self):
        globals.visGraph = 5
        print("abs Irr")
        print(globals.deviceConfig.m_Irradiance_m_IntensityCalib_m_Smoothing_m_SmoothPix)
        print(globals.deviceConfig.m_Irradiance_m_IntensityCalib_m_Smoothing_m_SmoothModel)
        print(globals.deviceConfig.m_Irradiance_m_IntensityCalib_m_CalInttime)
        print(type(globals.deviceConfig.m_Irradiance_m_IntensityCalib_m_aCalibConvers))                       # array
        print(globals.pixels)
        print(globals.deviceConfig.m_Irradiance_m_CalibrationType)
        print(globals.deviceConfig.m_Irradiance_m_FiberDiameter)
        y_label = "uWatt/cm^2"
        title = "Absolute Irradiance"
        y_value = []
        for i in range(globals.low, globals.high):
            y_value.append(globals.deviceConfig.m_Irradiance_m_IntensityCalib_m_aCalibConvers[i]*(globals.spectraldata[i]-globals.darkData[i])*(globals.deviceConfig.m_Irradiance_m_IntensityCalib_m_CalInttime/globals.integration_time))
        self.plot(y_value, y_label, title)
        return

    '''
    parameters: self
    return: none
    functionality: This function is supposed to find that y_values of the reletive irradiance graph and 
    then pass them to be plotted by the plot function.
    '''
    @pyqtSlot()
    def relIrrButton_clicked(self):
        globals.visGraph = 6
        print("rel Irr")
        print('were gonna do this one')
        return

    '''
    Parameters: self, array, string, string
    Return: None
    Functionality: This function takes y_values, y_label, and a title and graphs all the data
    to both graphs on page 1 and on page 2. In the function, it gets all the data for the x axis 
    (the wavelength range). It then sets the labels for the x axis. sets the labels for the y 
    axis. sets the titles. Then plots all the data
    '''
    # plots the data to both graphs on page 1 and page 2. 
    def plot(self, y_value, y_label, title):
        # get the values
        x_value = []
        for x in range(globals.low,globals.high):                                    # not sure if this is going to effect it but dropping off the last two data points
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

    '''
    parameters: self
    return: None
    functionality: This function will change the global variable for the stop pixel 
    '''
    @pyqtSlot()
    def setStopWavelength(self):
        print("set stop")
        val = self.ui.stopEdit.toPlainText()
        for i in range(len(val)):
            if val[i].isdigit() == False and val[i] != ".":
                QMessageBox.warning(self, "Input Warning", "Please make sure to enter a proper number")
                return
        val = float(val)
        for i in range(len(globals.wavelength)-1, -1, -1):
            if globals.wavelength[i] == 0:
                continue
            if val >= globals.wavelength[i]:
                globals.high = i
                print("assigned:", globals.high)
                return
        return

    '''
    parameters: self
    return: None
    functionality: This function will change the global variable for the start pixel. 
    '''
    @pyqtSlot()
    def setStartWavelength(self):
        print("set start")
        val = self.ui.startEdit.toPlainText()
        for i in range(len(val)):
            if val[i].isdigit() == False and val[i] != ".":
                QMessageBox.warning(self, "Input Warning", "Please make sure to enter a proper number")
                return
        val = float(val)
        # given the wavelength must find the pixel associated with wavelegth
        for i in range(len(globals.wavelength)):
            if val <= globals.wavelength[i]:
                globals.low = i
                print("assigned:", globals.low)
                return
        return
    
