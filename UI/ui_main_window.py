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
        main_window.resize(763, 639)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.stacked_main = QtWidgets.QStackedWidget(self.central_widget)
        self.stacked_main.setGeometry(QtCore.QRect(0, 0, 763, 598))
        self.stacked_main.setObjectName("stacked_main")
        self.page_login = QtWidgets.QWidget()
        self.page_login.setObjectName("page_login")
        self.button_login = QtWidgets.QPushButton(self.page_login)
        self.button_login.setGeometry(QtCore.QRect(340, 300, 80, 30))
        self.button_login.setObjectName("button_login")
        self.combo_box_login = QtWidgets.QComboBox(self.page_login)
        self.combo_box_login.setGeometry(QtCore.QRect(340, 260, 80, 30))
        self.combo_box_login.setObjectName("combo_box_login")
        self.combo_box_login.addItem("")
        self.combo_box_login.addItem("")
        self.combo_box_login.addItem("")
        self.stacked_main.addWidget(self.page_login)
        self.page_rad = QtWidgets.QWidget()
        self.page_rad.setObjectName("page_rad")
        self.stacked_rad = QtWidgets.QStackedWidget(self.page_rad)
        self.stacked_rad.setGeometry(QtCore.QRect(0, 0, 800, 559))
        self.stacked_rad.setObjectName("stacked_rad")
        self.stacked_main.addWidget(self.page_rad)
        self.page_pat = QtWidgets.QWidget()
        self.page_pat.setObjectName("page_pat")
        self.stacked_pat = QtWidgets.QStackedWidget(self.page_pat)
        self.stacked_pat.setGeometry(QtCore.QRect(0, 0, 800, 559))
        self.stacked_pat.setObjectName("stacked_pat")
        self.stacked_main.addWidget(self.page_pat)
        self.page_sur = QtWidgets.QWidget()
        self.page_sur.setObjectName("page_sur")
        self.stacked_sur = QtWidgets.QStackedWidget(self.page_sur)
        self.stacked_sur.setGeometry(QtCore.QRect(0, 0, 800, 559))
        self.stacked_sur.setObjectName("stacked_sur")
        self.stacked_main.addWidget(self.page_sur)
        main_window.setCentralWidget(self.central_widget)
        self.menu_bar = QtWidgets.QMenuBar(main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 763, 21))
        self.menu_bar.setObjectName("menu_bar")
        main_window.setMenuBar(self.menu_bar)
        self.status_bar = QtWidgets.QStatusBar(main_window)
        self.status_bar.setObjectName("status_bar")
        main_window.setStatusBar(self.status_bar)

        self.retranslateUi(main_window)
        self.stacked_main.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "MainWindow"))
        self.button_login.setText(_translate("main_window", "Login"))
        self.combo_box_login.setItemText(0, _translate("main_window", "Patient"))
        self.combo_box_login.setItemText(1, _translate("main_window", "Radiologist"))
        self.combo_box_login.setItemText(2, _translate("main_window", "Doctor"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_main_window()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())

