# field_kit
portable spectroscopy field kit for Avantes. 

# Instructions:
In these list of these instruction I assume that you are developing on Linux (unbuntu 18.01) and all commands are for terminal. Everything is created using 
python, python libraries, and qt designer. 

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

    measureType:

    identity:

    deviceConfig:

    visGraph:

    contiuous:

    config:

    low:

    high:

    darkTrue:

    refTrue:

# ui_functions.py 

# avaspec.py
The file that allows for communication with the spectrometer through the use of the .dll or .so. If you want to know what each function does in this file look at the avasoft dll manual. I didn't write this. 

# main.py 
This is where all the code gets executed. It also makes the mainwindow class which makes all the functionality of the application. 