# field_kit
portable spectroscopy field kit for Avantes. 

# Instructions:
In these list of these instruction I assume that you are developing on Linux (unbuntu 18.01) and all commands are for terminal. Everything is created using 
python, python libraries, and qt designer. 

# Issues
Currently working on developing the Irradiance graphs and saving the data to a file that is openable by Avasoft 8. 

# Getting Code
Clone the code from GitHub (Including just for Completeness):
    $ sudo apt install git
    $ git clone https://github.com/McNut55555/field_kit.git

# Setting up Enviornment
In terminal (installing necessary software):
    - install Qt5: "sudo apt-get install qt5-default"
    - install QtCreator: "sudo apt-get install qtcreator"
    - install qwt: "sudo apt-get install libqwt-qt5-dev"
    - install PyQt5: "sudo apt-get install python3-pyqt5"
    - install pyqtgraph: "pip3 install pyqtgraph"
    - (optional) install VS Code IDE: "sudo apt-get install code"

# Editing GUI (.ui file):
Editing the GUI is done through Qt Designer. With Qt Designer the developer is also able to see all of the names associated with each object (button).  

# Class MainWindow:
This class allows for the creation of the GUI and all of its functionality. The functions inside of this class I tried to include enough comments so a Developer is able to understand the funtionality of each of the functions.


