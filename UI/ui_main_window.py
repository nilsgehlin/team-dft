# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.setWindowModality(QtCore.Qt.NonModal)
        main_window.resize(596, 431)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_window.sizePolicy().hasHeightForWidth())
        main_window.setSizePolicy(sizePolicy)
        main_window.setStyleSheet("QMainWindow {\n"
"    background-color:#151a1e;\n"
"}\n"
"QCalendar {\n"
"    background-color: #151a1e;\n"
"}\n"
"QTextEdit {\n"
"    border-width: 1px;\n"
"    border-style: solid;\n"
"    border-color: #4fa08b;\n"
"    background-color: #222b2e;\n"
"    color: #d3dae3;\n"
"}\n"
"QPlainTextEdit {\n"
"    border-width: 1px;\n"
"    border-style: solid;\n"
"    border-color: #4fa08b;\n"
"    background-color: #222b2e;\n"
"    color: #d3dae3;\n"
"}\n"
"QToolButton {\n"
"    border-style: solid;\n"
"    border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));\n"
"    border-right-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(217, 217, 217), stop:1 rgb(227, 227, 227));\n"
"    border-left-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(227, 227, 227), stop:1 rgb(217, 217, 217));\n"
"    border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: #d3dae3;\n"
"    padding: 2px;\n"
"    background-color: rgb(255,255,255);\n"
"}\n"
"QToolButton:hover{\n"
"    border-style: solid;\n"
"    border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(195, 195, 195), stop:1 rgb(222, 222, 222));\n"
"    border-right-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(197, 197, 197), stop:1 rgb(227, 227, 227));\n"
"    border-left-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(227, 227, 227), stop:1 rgb(197, 197, 197));\n"
"    border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(195, 195, 195), stop:1 rgb(222, 222, 222));\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: rgb(0,0,0);\n"
"    padding: 2px;\n"
"    background-color: rgb(255,255,255);\n"
"}\n"
"QToolButton:pressed{\n"
"    border-style: solid;\n"
"    border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));\n"
"    border-right-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(217, 217, 217), stop:1 rgb(227, 227, 227));\n"
"    border-left-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(227, 227, 227), stop:1 rgb(217, 217, 217));\n"
"    border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: rgb(0,0,0);\n"
"    padding: 2px;\n"
"    background-color: rgb(142,142,142);\n"
"}\n"
"QPushButton{\n"
"    font: 11pt \"MS Shell Dlg 2\";\n"
"    border-style: solid;\n"
"    border-color: #050a0e;\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: #d3dae3;\n"
"    padding: 2px;\n"
"    background-color: #151a1e;\n"
"}\n"
"QPushButton::default{\n"
"    border-style: solid;\n"
"    border-color: #050a0e;\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: #FFFFFF;\n"
"    padding: 2px;\n"
"    background-color: #151a1e;;\n"
"}\n"
"QPushButton:hover{\n"
"    border-style: solid;\n"
"    border-color: #050a0e;\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: #d3dae3;\n"
"    padding: 2px;\n"
"    background-color: #1c1f1f;\n"
"}\n"
"QPushButton:pressed{\n"
"    border-style: solid;\n"
"    border-color: #050a0e;\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: #d3dae3;\n"
"    padding: 2px;\n"
"    background-color: #2c2f2f;\n"
"}\n"
"QPushButton:disabled{\n"
"    border-style: solid;\n"
"    border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));\n"
"    border-right-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(217, 217, 217), stop:1 rgb(227, 227, 227));\n"
"    border-left-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(227, 227, 227), stop:1 rgb(217, 217, 217));\n"
"    border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: #808086;\n"
"    padding: 2px;\n"
"    background-color: rgb(142,142,142);\n"
"}\n"
"QLineEdit {\n"
"    border-width: 1px;\n"
"    border-style: solid;\n"
"    border-color: #4fa08b;\n"
"    background-color: #222b2e;\n"
"    color: #d3dae3;\n"
"}\n"
"QLabel {\n"
"    color: #d3dae3;\n"
"}\n"
"QLCDNumber {\n"
"    color: #4d9b87;\n"
"}\n"
"QProgressBar {\n"
"    text-align: center;\n"
"    color: #d3dae3;\n"
"    border-radius: 10px;\n"
"    border-color: transparent;\n"
"    border-style: solid;\n"
"    background-color: #52595d;\n"
"}\n"
"QProgressBar::chunk {\n"
"    background-color: #214037    ;\n"
"    border-radius: 10px;\n"
"}\n"
"QMenuBar {\n"
"    background-color: #151a1e;\n"
"}\n"
"QMenuBar::item {\n"
"    color: #d3dae3;\n"
"      spacing: 3px;\n"
"      padding: 1px 4px;\n"
"    background-color: #151a1e;\n"
"}\n"
"\n"
"QMenuBar::item:selected {\n"
"      background-color: #252a2e;\n"
"    color: #FFFFFF;\n"
"}\n"
"QMenu {\n"
"    background-color: #151a1e;\n"
"}\n"
"QMenu::item:selected {\n"
"    background-color: #252a2e;\n"
"    color: #FFFFFF;\n"
"}\n"
"QMenu::item {\n"
"    color: #d3dae3;\n"
"    background-color: #151a1e;\n"
"}\n"
"QTabWidget {\n"
"    color:rgb(0,0,0);\n"
"    background-color:#000000;\n"
"}\n"
"QTabWidget::pane {\n"
"        border-color: #050a0e;\n"
"        background-color: #1e282c;\n"
"        border-style: solid;\n"
"        border-width: 1px;\n"
"        border-bottom-left-radius: 4px;\n"
"        border-bottom-right-radius: 4px;\n"
"}\n"
"QTabBar::tab:first {\n"
"    border-style: solid;\n"
"    border-left-width:1px;\n"
"    border-right-width:0px;\n"
"    border-top-width:1px;\n"
"    border-bottom-width:0px;\n"
"    border-top-color: #050a0e;\n"
"    border-left-color: #050a0e;\n"
"    border-bottom-color: #050a0e;\n"
"    border-top-left-radius: 4px;\n"
"    color: #d3dae3;\n"
"    padding: 3px;\n"
"    margin-left:0px;\n"
"    background-color: #151a1e;\n"
"}\n"
"QTabBar::tab:last {\n"
"    border-style: solid;\n"
"    border-top-width:1px;\n"
"    border-left-width:1px;\n"
"    border-right-width:1px;\n"
"    border-bottom-width:0px;\n"
"    border-color: #050a0e;\n"
"    border-top-right-radius: 4px;\n"
"    color: #d3dae3;\n"
"    padding: 3px;\n"
"    margin-left:0px;\n"
"    background-color: #151a1e;\n"
"}\n"
"QTabBar::tab {\n"
"    border-style: solid;\n"
"    border-top-width:1px;\n"
"    border-bottom-width:0px;\n"
"    border-left-width:1px;\n"
"    border-top-color: #050a0e;\n"
"    border-left-color: #050a0e;\n"
"    border-bottom-color: #050a0e;\n"
"    color: #d3dae3;\n"
"    padding: 3px;\n"
"    margin-left:0px;\n"
"    background-color: #151a1e;\n"
"}\n"
"QTabBar::tab:selected, QTabBar::tab:last:selected, QTabBar::tab:hover {\n"
"      border-style: solid;\n"
"      border-left-width:1px;\n"
"    border-bottom-width:0px;\n"
"    border-right-color: transparent;\n"
"    border-top-color: #050a0e;\n"
"    border-left-color: #050a0e;\n"
"    border-bottom-color: #050a0e;\n"
"    color: #FFFFFF;\n"
"    padding: 3px;\n"
"    margin-left:0px;\n"
"    background-color: #1e282c;\n"
"}\n"
"\n"
"QTabBar::tab:selected, QTabBar::tab:first:selected, QTabBar::tab:hover {\n"
"      border-style: solid;\n"
"      border-left-width:1px;\n"
"      border-bottom-width:0px;\n"
"      border-top-width:1px;\n"
"    border-right-color: transparent;\n"
"    border-top-color: #050a0e;\n"
"    border-left-color: #050a0e;\n"
"    border-bottom-color: #050a0e;\n"
"    color: #FFFFFF;\n"
"    padding: 3px;\n"
"    margin-left:0px;\n"
"    background-color: #1e282c;\n"
"}\n"
"\n"
"QCheckBox {\n"
"    color: #d3dae3;\n"
"    padding: 2px;\n"
"}\n"
"QCheckBox:disabled {\n"
"    color: #808086;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"QCheckBox:hover {\n"
"    border-radius:4px;\n"
"    border-style:solid;\n"
"    padding-left: 1px;\n"
"    padding-right: 1px;\n"
"    padding-bottom: 1px;\n"
"    padding-top: 1px;\n"
"    border-width:1px;\n"
"    border-color: transparent;\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    border-style:solid;\n"
"    border-width: 1px;\n"
"    border-color: #4fa08b;\n"
"    color: #000000;\n"
"    background-color: qradialgradient(cx:0.4, cy:0.4, radius: 1.5,fx:0, fy:0, stop:0 #1e282c, stop:0.3 #1e282c, stop:0.4 #4fa08b, stop:0.5 #1e282c, stop:1 #1e282c);\n"
"}\n"
"QCheckBox::indicator:unchecked {\n"
"\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    border-style:solid;\n"
"    border-width: 1px;\n"
"    border-color: #4fa08b;\n"
"    color: #000000;\n"
"}\n"
"QRadioButton {\n"
"    color: #d3dae3;\n"
"    padding: 1px;\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    border-style:solid;\n"
"    border-radius:5px;\n"
"    border-width: 1px;\n"
"    border-color: #4fa08b;\n"
"    color: #a9b7c6;\n"
"    background-color: qradialgradient(cx:0.5, cy:0.5, radius:0.4,fx:0.5, fy:0.5, stop:0 #4fa08b, stop:1 #1e282c);\n"
"}\n"
"QRadioButton::indicator:!checked {\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    border-style:solid;\n"
"    border-radius:5px;\n"
"    border-width: 1px;\n"
"    border-color: #4fa08b;\n"
"    color: #a9b7c6;\n"
"    background-color: transparent;\n"
"}\n"
"QStatusBar {\n"
"    color:#027f7f;\n"
"}\n"
"QSpinBox {\n"
"    color: #d3dae3;\n"
"    background-color: #222b2e;\n"
"    border-width: 1px;\n"
"    border-style: solid;\n"
"    border-color: #4fa08b;\n"
"}\n"
"QDoubleSpinBox {\n"
"    color: #d3dae3;\n"
"    background-color: #222b2e;\n"
"    border-width: 1px;\n"
"    border-style: solid;\n"
"    border-color: #4fa08b;\n"
"}\n"
"QTimeEdit {\n"
"    color: #d3dae3;\n"
"    background-color: #222b2e;\n"
"    border-width: 1px;\n"
"    border-style: solid;\n"
"    border-color: #4fa08b;\n"
"}\n"
"QDateTimeEdit {\n"
"    color: #d3dae3;\n"
"    background-color: #222b2e;\n"
"    border-width: 1px;\n"
"    border-style: solid;\n"
"    border-color: #4fa08b;\n"
"}\n"
"QDateEdit {\n"
"    color: #d3dae3;\n"
"    background-color: #222b2e;\n"
"    border-width: 1px;\n"
"    border-style: solid;\n"
"    border-color: #4fa08b;\n"
"}\n"
"QFontComboBox {\n"
"    color: #d3dae3;\n"
"    background-color: #222b2e;\n"
"    border-width: 1px;\n"
"    border-style: solid;\n"
"    border-color: #4fa08b;\n"
"}\n"
"QComboBox {\n"
"    color: #d3dae3;\n"
"    background-color: #222b2e;\n"
"    border-width: 1px;\n"
"    border-style: solid;\n"
"    border-color: #4fa08b;\n"
"}\n"
"\n"
"QDial {\n"
"    background: #16a085;\n"
"}\n"
"\n"
"QToolBox {\n"
"    color: #a9b7c6;\n"
"    background-color: #222b2e;\n"
"}\n"
"QToolBox::tab {\n"
"    color: #a9b7c6;\n"
"    background-color:#222b2e;\n"
"}\n"
"QToolBox::tab:selected {\n"
"    color: #FFFFFF;\n"
"    background-color:#222b2e;\n"
"}\n"
"QScrollArea {\n"
"    color: #FFFFFF;\n"
"    background-color:#222b2e;\n"
"}\n"
"QSlider::groove:horizontal {\n"
"    height: 5px;\n"
"    background-color: #52595d;\n"
"}\n"
"QSlider::groove:vertical {\n"
"    width: 5px;\n"
"    background-color: #52595d;\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background: #1a2224;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    border-color: rgb(207,207,207);\n"
"    width: 12px;\n"
"    margin: -5px 0;\n"
"    border-radius: 7px;\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background: #1a2224;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    border-color: rgb(207,207,207);\n"
"    height: 12px;\n"
"    margin: 0 -5px;\n"
"    border-radius: 7px;\n"
"}\n"
"QSlider::add-page:horizontal {\n"
"    background: #52595d;\n"
"}\n"
"QSlider::add-page:vertical {\n"
"    background: #52595d;\n"
"}\n"
"QSlider::sub-page:horizontal {\n"
"    background-color: #15433a;\n"
"}\n"
"QSlider::sub-page:vertical {\n"
"    background-color: #15433a;\n"
"}\n"
"QScrollBar:horizontal {\n"
"    max-height: 10px;\n"
"    border: 1px transparent grey;\n"
"    margin: 0px 20px 0px 20px;\n"
"    background: transparent;\n"
"}\n"
"QScrollBar:vertical {\n"
"    max-width: 10px;\n"
"    border: 1px transparent grey;\n"
"    margin: 20px 0px 20px 0px;\n"
"    background: transparent;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: #52595d;\n"
"    border-style: transparent;\n"
"    border-radius: 4px;\n"
"    min-width: 25px;\n"
"}\n"
"QScrollBar::handle:horizontal:hover {\n"
"    background: #58a492;\n"
"    border-style: transparent;\n"
"    border-radius: 4px;\n"
"    min-width: 25px;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"    background: #52595d;\n"
"    border-style: transparent;\n"
"    border-radius: 4px;\n"
"    min-height: 25px;\n"
"}\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: #58a492;\n"
"    border-style: transparent;\n"
"    border-radius: 4px;\n"
"    min-height: 25px;\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"   border: 2px transparent grey;\n"
"   border-top-right-radius: 4px;\n"
"   border-bottom-right-radius: 4px;\n"
"   background: #15433a;\n"
"   width: 20px;\n"
"   subcontrol-position: right;\n"
"   subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::add-line:horizontal:pressed {\n"
"   border: 2px transparent grey;\n"
"   border-top-right-radius: 4px;\n"
"   border-bottom-right-radius: 4px;\n"
"   background: rgb(181,181,181);\n"
"   width: 20px;\n"
"   subcontrol-position: right;\n"
"   subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::add-line:vertical {\n"
"   border: 2px transparent grey;\n"
"   border-bottom-left-radius: 4px;\n"
"   border-bottom-right-radius: 4px;\n"
"   background: #15433a;\n"
"   height: 20px;\n"
"   subcontrol-position: bottom;\n"
"   subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::add-line:vertical:pressed {\n"
"   border: 2px transparent grey;\n"
"   border-bottom-left-radius: 4px;\n"
"   border-bottom-right-radius: 4px;\n"
"   background: rgb(181,181,181);\n"
"   height: 20px;\n"
"   subcontrol-position: bottom;\n"
"   subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"   border: 2px transparent grey;\n"
"   border-top-left-radius: 4px;\n"
"   border-bottom-left-radius: 4px;\n"
"   background: #15433a;\n"
"   width: 20px;\n"
"   subcontrol-position: left;\n"
"   subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal:pressed {\n"
"   border: 2px transparent grey;\n"
"   border-top-left-radius: 4px;\n"
"   border-bottom-left-radius: 4px;\n"
"   background: rgb(181,181,181);\n"
"   width: 20px;\n"
"   subcontrol-position: left;\n"
"   subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:vertical {\n"
"   border: 2px transparent grey;\n"
"   border-top-left-radius: 4px;\n"
"   border-top-right-radius: 4px;\n"
"   background: #15433a;\n"
"   height: 20px;\n"
"   subcontrol-position: top;\n"
"   subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:vertical:pressed {\n"
"   border: 2px transparent grey;\n"
"   border-top-left-radius: 4px;\n"
"   border-top-right-radius: 4px;\n"
"   background: rgb(181,181,181);\n"
"   height: 20px;\n"
"   subcontrol-position: top;\n"
"   subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
"   background: none;\n"
"}\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"   background: none;\n"
"}\n"
"QTreeWidget{\n"
"    border-width: 1px;\n"
"    border-style: solid;\n"
"    border-color: #4fa08b;\n"
"    background-color: #222b2e;\n"
"    color: #d3dae3;\n"
"}")
        main_window.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setStyleSheet("")
        self.central_widget.setObjectName("central_widget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.central_widget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.stacked_main = QtWidgets.QStackedWidget(self.central_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stacked_main.sizePolicy().hasHeightForWidth())
        self.stacked_main.setSizePolicy(sizePolicy)
        self.stacked_main.setObjectName("stacked_main")
        self.page_login = QtWidgets.QWidget()
        self.page_login.setObjectName("page_login")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page_login)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 8, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 7, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 5, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.page_login)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 4, 1, 1, 1)
        self.page_login_button_login = QtWidgets.QToolButton(self.page_login)
        self.page_login_button_login.setMaximumSize(QtCore.QSize(200, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/unlock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.page_login_button_login.setIcon(icon)
        self.page_login_button_login.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.page_login_button_login.setObjectName("page_login_button_login")
        self.gridLayout_2.addWidget(self.page_login_button_login, 5, 2, 1, 1)
        self.page_login_insert_id = QtWidgets.QLineEdit(self.page_login)
        self.page_login_insert_id.setMaximumSize(QtCore.QSize(200, 16777215))
        self.page_login_insert_id.setObjectName("page_login_insert_id")
        self.gridLayout_2.addWidget(self.page_login_insert_id, 3, 2, 1, 1)
        self.page_login_combobox_user_type = QtWidgets.QComboBox(self.page_login)
        self.page_login_combobox_user_type.setMinimumSize(QtCore.QSize(100, 0))
        self.page_login_combobox_user_type.setObjectName("page_login_combobox_user_type")
        self.page_login_combobox_user_type.addItem("")
        self.page_login_combobox_user_type.addItem("")
        self.page_login_combobox_user_type.addItem("")
        self.gridLayout_2.addWidget(self.page_login_combobox_user_type, 5, 1, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.page_login)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_2.addWidget(self.textEdit, 7, 1, 1, 2)
        self.label = QtWidgets.QLabel(self.page_login)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 3, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem3, 1, 1, 1, 4)
        self.page_login_insert_password = QtWidgets.QLineEdit(self.page_login)
        self.page_login_insert_password.setMaximumSize(QtCore.QSize(200, 16777215))
        self.page_login_insert_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.page_login_insert_password.setClearButtonEnabled(False)
        self.page_login_insert_password.setObjectName("page_login_insert_password")
        self.gridLayout_2.addWidget(self.page_login_insert_password, 4, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.page_login)
        self.label_3.setStyleSheet("color: rgb(253, 147, 50);\n"
"font: 30pt;")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 1, 1, 2)
        self.stacked_main.addWidget(self.page_login)
        self.page_rad = QtWidgets.QWidget()
        self.page_rad.setObjectName("page_rad")
        self.gridLayout = QtWidgets.QGridLayout(self.page_rad)
        self.gridLayout.setObjectName("gridLayout")
        self.stacked_rad = QtWidgets.QStackedWidget(self.page_rad)
        self.stacked_rad.setObjectName("stacked_rad")
        self.gridLayout.addWidget(self.stacked_rad, 0, 0, 1, 1)
        self.stacked_main.addWidget(self.page_rad)
        self.page_pat = QtWidgets.QWidget()
        self.page_pat.setObjectName("page_pat")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.page_pat)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.stacked_pat = QtWidgets.QStackedWidget(self.page_pat)
        self.stacked_pat.setObjectName("stacked_pat")
        self.gridLayout_4.addWidget(self.stacked_pat, 0, 0, 1, 1)
        self.stacked_main.addWidget(self.page_pat)
        self.page_sur = QtWidgets.QWidget()
        self.page_sur.setObjectName("page_sur")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.page_sur)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.stacked_sur = QtWidgets.QStackedWidget(self.page_sur)
        self.stacked_sur.setObjectName("stacked_sur")
        self.gridLayout_6.addWidget(self.stacked_sur, 0, 0, 1, 1)
        self.stacked_main.addWidget(self.page_sur)
        self.gridLayout_5.addWidget(self.stacked_main, 0, 0, 1, 1)
        main_window.setCentralWidget(self.central_widget)
        self.menu_bar = QtWidgets.QMenuBar(main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 596, 22))
        self.menu_bar.setObjectName("menu_bar")
        self.menu_bar_theme = QtWidgets.QMenu(self.menu_bar)
        self.menu_bar_theme.setObjectName("menu_bar_theme")
        main_window.setMenuBar(self.menu_bar)
        self.status_bar = QtWidgets.QStatusBar(main_window)
        self.status_bar.setObjectName("status_bar")
        main_window.setStatusBar(self.status_bar)
        self.menu_bar_theme_button_night_mode = QtWidgets.QAction(main_window)
        self.menu_bar_theme_button_night_mode.setCheckable(True)
        self.menu_bar_theme_button_night_mode.setChecked(True)
        self.menu_bar_theme_button_night_mode.setObjectName("menu_bar_theme_button_night_mode")
        self.menu_bar_theme_button_day_mode = QtWidgets.QAction(main_window)
        self.menu_bar_theme_button_day_mode.setCheckable(True)
        self.menu_bar_theme_button_day_mode.setChecked(False)
        self.menu_bar_theme_button_day_mode.setObjectName("menu_bar_theme_button_day_mode")
        self.menu_bar_theme.addAction(self.menu_bar_theme_button_day_mode)
        self.menu_bar_theme.addAction(self.menu_bar_theme_button_night_mode)
        self.menu_bar.addAction(self.menu_bar_theme.menuAction())

        self.retranslateUi(main_window)
        self.stacked_main.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "MainWindow"))
        self.label_2.setText(_translate("main_window", "Password:"))
        self.page_login_button_login.setText(_translate("main_window", "Login"))
        self.page_login_insert_id.setText(_translate("main_window", "0000"))
        self.page_login_insert_id.setPlaceholderText(_translate("main_window", "ID"))
        self.page_login_combobox_user_type.setItemText(0, _translate("main_window", "Patient"))
        self.page_login_combobox_user_type.setItemText(1, _translate("main_window", "Radiologist"))
        self.page_login_combobox_user_type.setItemText(2, _translate("main_window", "Surgeon"))
        self.textEdit.setHtml(_translate("main_window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt;\">Patients:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt;\">id: 0000 pw: 0000</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt;\">id: 0001 pw: 0001</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8.25pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt;\">Radiologist:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt;\">id: 0000 pw: 0000</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8.25pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt;\">Surgeon:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt;\">id: 0000 pw: 0000</span></p></body></html>"))
        self.label.setText(_translate("main_window", "User ID:"))
        self.page_login_insert_password.setText(_translate("main_window", "0000"))
        self.page_login_insert_password.setPlaceholderText(_translate("main_window", "Password"))
        self.label_3.setText(_translate("main_window", "CLARITY"))
        self.menu_bar_theme.setTitle(_translate("main_window", "Theme"))
        self.menu_bar_theme_button_night_mode.setText(_translate("main_window", "Night mode"))
        self.menu_bar_theme_button_day_mode.setText(_translate("main_window", "Day mode"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_main_window()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())

