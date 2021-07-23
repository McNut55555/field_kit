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
