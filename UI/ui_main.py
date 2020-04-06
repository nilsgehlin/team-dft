# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(800, 600)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.stacked_main = QtWidgets.QStackedWidget(self.central_widget)
        self.stacked_main.setGeometry(QtCore.QRect(0, 0, 800, 559))
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
        self.label = QtWidgets.QLabel(self.page_rad)
        self.label.setGeometry(QtCore.QRect(390, 160, 47, 13))
        self.label.setObjectName("label")
        self.stacked_rad_temp = QtWidgets.QStackedWidget(self.page_rad)
        self.stacked_rad_temp.setGeometry(QtCore.QRect(0, 0, 800, 559))
        self.stacked_rad_temp.setObjectName("stacked_rad_temp")
        self.stacked_main.addWidget(self.page_rad)
        self.page_pat = QtWidgets.QWidget()
        self.page_pat.setObjectName("page_pat")
        self.label_2 = QtWidgets.QLabel(self.page_pat)
        self.label_2.setGeometry(QtCore.QRect(370, 160, 47, 13))
        self.label_2.setObjectName("label_2")
        self.stacked_pat_temp = QtWidgets.QStackedWidget(self.page_pat)
        self.stacked_pat_temp.setGeometry(QtCore.QRect(0, 0, 800, 559))
        self.stacked_pat_temp.setObjectName("stacked_pat_temp")
        self.stacked_main.addWidget(self.page_pat)
        self.page_doc = QtWidgets.QWidget()
        self.page_doc.setObjectName("page_doc")
        self.label_3 = QtWidgets.QLabel(self.page_doc)
        self.label_3.setGeometry(QtCore.QRect(400, 170, 47, 13))
        self.label_3.setObjectName("label_3")
        self.stacked_doc_temp = QtWidgets.QStackedWidget(self.page_doc)
        self.stacked_doc_temp.setGeometry(QtCore.QRect(0, 0, 800, 559))
        self.stacked_doc_temp.setObjectName("stacked_doc_temp")
        self.stacked_main.addWidget(self.page_doc)
        main_window.setCentralWidget(self.central_widget)
        self.menu_bar = QtWidgets.QMenuBar(main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 800, 21))
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
        self.label.setText(_translate("main_window", "RAD"))
        self.label_2.setText(_translate("main_window", "PAT"))
        self.label_3.setText(_translate("main_window", "DOC"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_main_window()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())

