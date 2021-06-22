# field_kit
portable spectroscopy field kit for Avantes

# Instructions:
In these list of these instruction I assume that you are developing on Linux (unbuntu 18.01). Everything is created using python, python libraries, and qt designer. 

# Python Libraries (may need to install through terminal):
    PyQt5
    pyqtgraph
    math
    ui_funtions

# Editing GUI (.ui file):
    Used Qt Desiginer to change the design of the GUI (ui_main.ui). After every edit need to run:
        $ pyuic5 -x ui_main.ui -o ui_main.py
    This command converts the .ui file to a .py file. In the main code it loads a .py file and this is why this command is necessary. If needed one can load the .ui file in with the uic library.