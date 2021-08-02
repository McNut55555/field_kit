# from re import L, S
from PyQt5 import QtWidgets
from ui_functions import *
from MainWindow import *

## MAIN
###########################################################################
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
