
from PyQt5 import QtCore, QtGui







# saveFile.triggtered.connect(self.file_save)

def file_save(self):
    name = QtGui.QFileDialog.getSaveFileName(self, "savefile")
    file = open(name, 'w')
    file.write()
    file.close()

self.file_save()