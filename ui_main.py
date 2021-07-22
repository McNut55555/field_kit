# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(786, 411)
        MainWindow.setMinimumSize(QtCore.QSize(500, 250))
        MainWindow.setStyleSheet("background-color: rgb(45, 45, 45);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Top_Bar = QtWidgets.QFrame(self.centralwidget)
        self.Top_Bar.setMaximumSize(QtCore.QSize(16777215, 40))
        self.Top_Bar.setStyleSheet("background-color: rgb(35, 35, 35);")
        self.Top_Bar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Top_Bar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Top_Bar.setObjectName("Top_Bar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.Top_Bar)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_toggle = QtWidgets.QFrame(self.Top_Bar)
        self.frame_toggle.setMaximumSize(QtCore.QSize(70, 40))
        self.frame_toggle.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.frame_toggle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_toggle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_toggle.setObjectName("frame_toggle")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_toggle)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout.addWidget(self.frame_toggle)
        self.verticalLayout.addWidget(self.Top_Bar)
        self.Content = QtWidgets.QFrame(self.centralwidget)
        self.Content.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Content.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Content.setObjectName("Content")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.Content)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_left_menu = QtWidgets.QFrame(self.Content)
        self.frame_left_menu.setEnabled(True)
        self.frame_left_menu.setMinimumSize(QtCore.QSize(70, 0))
        self.frame_left_menu.setMaximumSize(QtCore.QSize(70, 16777215))
        self.frame_left_menu.setStyleSheet("background-color: rgb(35, 35, 35);")
        self.frame_left_menu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_left_menu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_left_menu.setObjectName("frame_left_menu")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_left_menu)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_top_menus = QtWidgets.QFrame(self.frame_left_menu)
        self.frame_top_menus.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_top_menus.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top_menus.setObjectName("frame_top_menus")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_top_menus)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.Btn_Toggle = QtWidgets.QPushButton(self.frame_top_menus)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_Toggle.sizePolicy().hasHeightForWidth())
        self.Btn_Toggle.setSizePolicy(sizePolicy)
        self.Btn_Toggle.setMinimumSize(QtCore.QSize(0, 40))
        self.Btn_Toggle.setStyleSheet("color: rgb(255, 255, 255);\n"
"border: 0px solid;\n"
"background-color: rgb(10,10,100);\n"
"")
        self.Btn_Toggle.setObjectName("Btn_Toggle")
        self.verticalLayout_4.addWidget(self.Btn_Toggle)
        self.btn_page_1 = QtWidgets.QPushButton(self.frame_top_menus)
        self.btn_page_1.setMinimumSize(QtCore.QSize(0, 40))
        self.btn_page_1.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_page_1.setObjectName("btn_page_1")
        self.verticalLayout_4.addWidget(self.btn_page_1)
        self.btn_page_2 = QtWidgets.QPushButton(self.frame_top_menus)
        self.btn_page_2.setMinimumSize(QtCore.QSize(0, 40))
        self.btn_page_2.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_page_2.setObjectName("btn_page_2")
        self.verticalLayout_4.addWidget(self.btn_page_2)
        self.btn_page_3 = QtWidgets.QPushButton(self.frame_top_menus)
        self.btn_page_3.setMinimumSize(QtCore.QSize(0, 40))
        self.btn_page_3.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_page_3.setObjectName("btn_page_3")
        self.verticalLayout_4.addWidget(self.btn_page_3)
        self.verticalLayout_3.addWidget(self.frame_top_menus, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout_2.addWidget(self.frame_left_menu)
        self.frame_pages = QtWidgets.QFrame(self.Content)
        self.frame_pages.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_pages.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_pages.setObjectName("frame_pages")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_pages)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame_pages)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.page_1)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.frame = QtWidgets.QFrame(self.page_1)
        self.frame.setMinimumSize(QtCore.QSize(0, 50))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.connectButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connectButton.sizePolicy().hasHeightForWidth())
        self.connectButton.setSizePolicy(sizePolicy)
        self.connectButton.setStyleSheet("color: #FFF;\n"
"")
        self.connectButton.setObjectName("connectButton")
        self.horizontalLayout_3.addWidget(self.connectButton)
        self.startStopButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startStopButton.sizePolicy().hasHeightForWidth())
        self.startStopButton.setSizePolicy(sizePolicy)
        self.startStopButton.setStyleSheet("color: #FFF;\n"
"")
        self.startStopButton.setObjectName("startStopButton")
        self.horizontalLayout_3.addWidget(self.startStopButton)
        self.darkButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.darkButton.sizePolicy().hasHeightForWidth())
        self.darkButton.setSizePolicy(sizePolicy)
        self.darkButton.setStyleSheet("color: #FFF;\n"
"")
        self.darkButton.setObjectName("darkButton")
        self.horizontalLayout_3.addWidget(self.darkButton)
        self.refButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refButton.sizePolicy().hasHeightForWidth())
        self.refButton.setSizePolicy(sizePolicy)
        self.refButton.setStyleSheet("color: #FFF;\n"
"")
        self.refButton.setObjectName("refButton")
        self.horizontalLayout_3.addWidget(self.refButton)
        self.configButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configButton.sizePolicy().hasHeightForWidth())
        self.configButton.setSizePolicy(sizePolicy)
        self.configButton.setStyleSheet("color: #FFF;\n"
"")
        self.configButton.setObjectName("configButton")
        self.horizontalLayout_3.addWidget(self.configButton)
        self.stopButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stopButton.sizePolicy().hasHeightForWidth())
        self.stopButton.setSizePolicy(sizePolicy)
        self.stopButton.setStyleSheet("color: #FFF;\n"
"")
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout_3.addWidget(self.stopButton)
        self.verticalLayout_7.addWidget(self.frame)
        self.graphWidget = PlotWidget(self.page_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphWidget.sizePolicy().hasHeightForWidth())
        self.graphWidget.setSizePolicy(sizePolicy)
        self.graphWidget.setObjectName("graphWidget")
        self.verticalLayout_7.addWidget(self.graphWidget)
        self.verticalLayout_14.addLayout(self.verticalLayout_7)
        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.widget = QtWidgets.QWidget(self.page_2)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 80))
        self.widget.setObjectName("widget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.collectButton_2 = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.collectButton_2.sizePolicy().hasHeightForWidth())
        self.collectButton_2.setSizePolicy(sizePolicy)
        self.collectButton_2.setStyleSheet("color: #FFF;\n"
"")
        self.collectButton_2.setObjectName("collectButton_2")
        self.horizontalLayout_4.addWidget(self.collectButton_2)
        self.saveButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setStyleSheet("color: #FFF;\n"
"")
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_4.addWidget(self.saveButton)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.scopeModeButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scopeModeButton.sizePolicy().hasHeightForWidth())
        self.scopeModeButton.setSizePolicy(sizePolicy)
        self.scopeModeButton.setStyleSheet("color: #FFF;\n"
"")
        self.scopeModeButton.setObjectName("scopeModeButton")
        self.verticalLayout_6.addWidget(self.scopeModeButton)
        self.reflectButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reflectButton.sizePolicy().hasHeightForWidth())
        self.reflectButton.setSizePolicy(sizePolicy)
        self.reflectButton.setStyleSheet("color: #FFF;\n"
"")
        self.reflectButton.setObjectName("reflectButton")
        self.verticalLayout_6.addWidget(self.reflectButton)
        self.horizontalLayout_4.addLayout(self.verticalLayout_6)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.scopeMinDarkButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scopeMinDarkButton.sizePolicy().hasHeightForWidth())
        self.scopeMinDarkButton.setSizePolicy(sizePolicy)
        self.scopeMinDarkButton.setStyleSheet("color: #FFF;\n"
"")
        self.scopeMinDarkButton.setObjectName("scopeMinDarkButton")
        self.verticalLayout_9.addWidget(self.scopeMinDarkButton)
        self.absIrrButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.absIrrButton.sizePolicy().hasHeightForWidth())
        self.absIrrButton.setSizePolicy(sizePolicy)
        self.absIrrButton.setStyleSheet("color: #FFF;\n"
"")
        self.absIrrButton.setObjectName("absIrrButton")
        self.verticalLayout_9.addWidget(self.absIrrButton)
        self.horizontalLayout_4.addLayout(self.verticalLayout_9)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.absButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.absButton.sizePolicy().hasHeightForWidth())
        self.absButton.setSizePolicy(sizePolicy)
        self.absButton.setStyleSheet("color: #FFF;\n"
"")
        self.absButton.setObjectName("absButton")
        self.verticalLayout_10.addWidget(self.absButton)
        self.relIrrButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.relIrrButton.sizePolicy().hasHeightForWidth())
        self.relIrrButton.setSizePolicy(sizePolicy)
        self.relIrrButton.setStyleSheet("color: #FFF;\n"
"")
        self.relIrrButton.setObjectName("relIrrButton")
        self.verticalLayout_10.addWidget(self.relIrrButton)
        self.horizontalLayout_4.addLayout(self.verticalLayout_10)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.transButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.transButton.sizePolicy().hasHeightForWidth())
        self.transButton.setSizePolicy(sizePolicy)
        self.transButton.setStyleSheet("color: #FFF;\n"
"")
        self.transButton.setObjectName("transButton")
        self.verticalLayout_11.addWidget(self.transButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_11.addItem(spacerItem)
        self.horizontalLayout_4.addLayout(self.verticalLayout_11)
        self.scaleButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scaleButton.sizePolicy().hasHeightForWidth())
        self.scaleButton.setSizePolicy(sizePolicy)
        self.scaleButton.setStyleSheet("color: #FFF;\n"
"")
        self.scaleButton.setObjectName("scaleButton")
        self.horizontalLayout_4.addWidget(self.scaleButton)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.verticalLayout_12.addWidget(self.widget)
        self.graphWidget_2 = PlotWidget(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphWidget_2.sizePolicy().hasHeightForWidth())
        self.graphWidget_2.setSizePolicy(sizePolicy)
        self.graphWidget_2.setMinimumSize(QtCore.QSize(0, 0))
        self.graphWidget_2.setObjectName("graphWidget_2")
        self.verticalLayout_12.addWidget(self.graphWidget_2)
        self.verticalLayout_13.addLayout(self.verticalLayout_12)
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.layoutWidget = QtWidgets.QWidget(self.page_3)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 394, 181))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setStyleSheet("color: #FFF;\n"
"")
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.SingleButton = QtWidgets.QRadioButton(self.layoutWidget)
        self.SingleButton.setStyleSheet("color: #FFF;\n"
"")
        self.SingleButton.setObjectName("SingleButton")
        self.verticalLayout_8.addWidget(self.SingleButton)
        self.ContinueButton = QtWidgets.QRadioButton(self.layoutWidget)
        self.ContinueButton.setStyleSheet("color: #FFF;\n"
"")
        self.ContinueButton.setObjectName("ContinueButton")
        self.verticalLayout_8.addWidget(self.ContinueButton)
        self.horizontalLayout_6.addLayout(self.verticalLayout_8)
        self.measureTypeApply = QtWidgets.QPushButton(self.layoutWidget)
        self.measureTypeApply.setStyleSheet("color: #FFF;\n"
"")
        self.measureTypeApply.setObjectName("measureTypeApply")
        self.horizontalLayout_6.addWidget(self.measureTypeApply)
        self.verticalLayout_15.addLayout(self.horizontalLayout_6)
        self.layoutWidget1 = QtWidgets.QWidget(self.page_3)
        self.layoutWidget1.setGeometry(QtCore.QRect(440, 30, 371, 152))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_4.setStyleSheet("color: #FFF;")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_9.addWidget(self.label_4)
        self.startEdit = QtWidgets.QTextEdit(self.layoutWidget1)
        self.startEdit.setStyleSheet("color: #FFF;")
        self.startEdit.setObjectName("startEdit")
        self.horizontalLayout_9.addWidget(self.startEdit)
        self.startApply = QtWidgets.QPushButton(self.layoutWidget1)
        self.startApply.setStyleSheet("color: #FFF;")
        self.startApply.setObjectName("startApply")
        self.horizontalLayout_9.addWidget(self.startApply)
        self.verticalLayout_16.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_5.setStyleSheet("color: #FFF;")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_10.addWidget(self.label_5)
        self.stopEdit = QtWidgets.QTextEdit(self.layoutWidget1)
        self.stopEdit.setStyleSheet("color: #FFF;")
        self.stopEdit.setObjectName("stopEdit")
        self.horizontalLayout_10.addWidget(self.stopEdit)
        self.stopApply = QtWidgets.QPushButton(self.layoutWidget1)
        self.stopApply.setStyleSheet("color: #FFF;")
        self.stopApply.setObjectName("stopApply")
        self.horizontalLayout_10.addWidget(self.stopApply)
        self.verticalLayout_16.addLayout(self.horizontalLayout_10)
        self.label_2 = QtWidgets.QLabel(self.page_3)
        self.label_2.setGeometry(QtCore.QRect(60, 280, 141, 31))
        self.label_2.setStyleSheet("color: #FFF;\n"
"")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.page_3)
        self.label_3.setGeometry(QtCore.QRect(50, 330, 101, 41))
        self.label_3.setStyleSheet("color: #FFF;\n"
"")
        self.label_3.setObjectName("label_3")
        self.intEdit = QtWidgets.QTextEdit(self.page_3)
        self.intEdit.setGeometry(QtCore.QRect(210, 270, 104, 70))
        self.intEdit.setStyleSheet("color: #FFF;\n"
"")
        self.intEdit.setObjectName("intEdit")
        self.avgEdit = QtWidgets.QTextEdit(self.page_3)
        self.avgEdit.setGeometry(QtCore.QRect(200, 350, 104, 70))
        self.avgEdit.setStyleSheet("color: #FFF;\n"
"")
        self.avgEdit.setObjectName("avgEdit")
        self.intApply = QtWidgets.QPushButton(self.page_3)
        self.intApply.setGeometry(QtCore.QRect(360, 280, 89, 25))
        self.intApply.setStyleSheet("color: #FFF;\n"
"")
        self.intApply.setObjectName("intApply")
        self.avgApply = QtWidgets.QPushButton(self.page_3)
        self.avgApply.setGeometry(QtCore.QRect(350, 350, 89, 25))
        self.avgApply.setStyleSheet("color: #FFF;\n"
"")
        self.avgApply.setObjectName("avgApply")
        self.stackedWidget.addWidget(self.page_3)
        self.verticalLayout_5.addWidget(self.stackedWidget)
        self.horizontalLayout_2.addWidget(self.frame_pages)
        self.verticalLayout.addWidget(self.Content)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Btn_Toggle.setText(_translate("MainWindow", "TOGGLE"))
        self.btn_page_1.setText(_translate("MainWindow", "Setup"))
        self.btn_page_2.setText(_translate("MainWindow", "Measure"))
        self.btn_page_3.setText(_translate("MainWindow", "Options"))
        self.connectButton.setText(_translate("MainWindow", "Connect"))
        self.startStopButton.setText(_translate("MainWindow", "Collect"))
        self.darkButton.setText(_translate("MainWindow", "Dark"))
        self.refButton.setText(_translate("MainWindow", "Reference"))
        self.configButton.setText(_translate("MainWindow", "Auto_configure"))
        self.stopButton.setText(_translate("MainWindow", "stop "))
        self.collectButton_2.setText(_translate("MainWindow", "Collect"))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.scopeModeButton.setText(_translate("MainWindow", "Scope"))
        self.reflectButton.setText(_translate("MainWindow", "Reflectance"))
        self.scopeMinDarkButton.setText(_translate("MainWindow", "Scope-Dark"))
        self.absIrrButton.setText(_translate("MainWindow", "Abs_Irr"))
        self.absButton.setText(_translate("MainWindow", "Absorbance"))
        self.relIrrButton.setText(_translate("MainWindow", "Rel-Irr"))
        self.transButton.setText(_translate("MainWindow", "Transmittance"))
        self.scaleButton.setText(_translate("MainWindow", "Scale"))
        self.label.setText(_translate("MainWindow", "Measurement Type"))
        self.SingleButton.setText(_translate("MainWindow", "Single Measurement"))
        self.ContinueButton.setText(_translate("MainWindow", "Continuously"))
        self.measureTypeApply.setText(_translate("MainWindow", "Apply"))
        self.label_4.setText(_translate("MainWindow", "Start Wavelength"))
        self.startApply.setText(_translate("MainWindow", "Apply"))
        self.label_5.setText(_translate("MainWindow", "Stop Wavelength"))
        self.stopApply.setText(_translate("MainWindow", "Apply"))
        self.label_2.setText(_translate("MainWindow", "Integration time:"))
        self.label_3.setText(_translate("MainWindow", "Averages:"))
        self.intApply.setText(_translate("MainWindow", "Apply"))
        self.avgApply.setText(_translate("MainWindow", "Apply"))
from pyqtgraph import PlotWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
