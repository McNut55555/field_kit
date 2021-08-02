# field_kit
portable spectroscopy field kit for Avantes. 

# Instructions:
In these list of these instruction I assume that you are developing on Linux (unbuntu 18.01) and all commands are for terminal. Everything is created using python, python libraries, and qt designer. 

# Getting Code
Clone the code from GitHub (Including just for Completeness):
    $ sudo apt install git
    $ git clone https://github.com/McNut55555/field_kit.git

# Setting up Enviornment
In terminal (installing necessary software):
    - install Qt5: "$ sudo apt-get install qt5-default"
    - install QtCreator: "$ sudo apt-get install qtcreator"
    - install qwt: "$ sudo apt-get install libqwt-qt5-dev"
    - install PyQt5: "$ sudo apt-get install python3-pyqt5"
    - install pyqtgraph: "$ pip3 install pyqtgraph"
    - (optional) install VS Code IDE: "$ sudo apt-get install code"

# Editing GUI (.ui file):
Editing the GUI is done through Qt Designer. With Qt Designer the developer is also able to see all of the names associated with each button (objectName). Run the command below to convert the .ui file to a .py file so main can access the changes to the GUI. 
    - $ pyuic5 -x ui_main.ui -o ui_main.py

# Developement
Not sure if absolute Irradiance graph is accurate. Haven't got to test it yet. Continuous scanning doesn't work. This is out of the scope of my knowledge and requires parallel programming. Will be testing my directions with the pi. May seperate the MainWindow class into another file. Will rename it to Avalight or something. 

# Class MainWindow:
This class allows for the creation of the GUI and all of its functionality. All functions in class have included comments to explain the functionality. 

# Functions
All the functions should be commented appropriately so that a developer should be able to understand the functionality and use. 

# Globals.py 

VARIABES

    dev_handle: The serial number of the spectrometer
    
    pixels: the amount of pixels in the current spectrometer. This gets redefined in the fuction connectButton_clicked in main.py. 

    wavelength: This array stores all the wavelengths that each pixel views. 

    spectraldata: This array stores the counts of each pixel.

    darkData: This array stores the counts of each pixel when the spectrometer is dark

    refData: This array stores the counts of each pixel when the spectrometer is seeing virgin light. 

    integration_time: This vairable stores the integration time of the spectrometer

    averages: This variable stores the amount of averages the spectrometer takes when taking a measurement. 

    stopscanning: This variable is used when collecting data from the spectrometer. This is used in the function collect in main.py. 

    first:

    measureType: is variable holds the MeasConfigType variable from avaspec.py

    identity: this variable holds the AvsIdentityType variable from avaspec.py

    deviceConfig: this variable holds the DeviceConfigType variable from avaspec.py

    visGraph: This variable holds the variable telling the function startStopButton_clicked in main.py what fucntion to graph to both of the graphs on setup and measure tabs.  

    contiuous: This variable is meant to be used to tell startStopButton function to continue scanning if True. However the continuous aspect of the program doesn't work. 

    config:

    low: This sets the low end pixel to be displayed to the graphs. 

    high: This sets the high end pixel to be displayed to the graphs.

    darkTrue: This variable tells if a dark refrence has been saved. This is used when 

    refTrue: This varible tells if the refrence has been saved. This is used when

# ui_functions.py 

# avaspec.py
IMPORTANT: When using Raspberrian or ubuntu make sure that you are using the right dll for the operating system. Both of them fall into the logic for linux however use a different dll to communicate with the spectrometer. This means depending on the operating system you may have to change which dll it is reading in on avaspec.py. This can be done by changing the what comment is visible to the interpreter. 

The file that allows for communication with the spectrometer through the use of the .dll or .so. If you want to know what each function does in this file look at the avasoft dll manual. I didn't write this. However, I did make a few changes.  

# main.py 
This is where all the code gets executed. It also makes the mainwindow class which makes all the functionality of the application. 