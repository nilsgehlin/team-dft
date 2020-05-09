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
        self.page_login_button_login = QtWidgets.QPushButton(self.page_login)
        self.page_login_button_login.setGeometry(QtCore.QRect(370, 310, 80, 30))
        self.page_login_button_login.setObjectName("page_login_button_login")
        self.page_login_combobox_user_type = QtWidgets.QComboBox(self.page_login)
        self.page_login_combobox_user_type.setGeometry(QtCore.QRect(280, 310, 80, 30))
        self.page_login_combobox_user_type.setObjectName("page_login_combobox_user_type")
        self.page_login_combobox_user_type.addItem("")
        self.page_login_combobox_user_type.addItem("")
        self.page_login_combobox_user_type.addItem("")
        self.page_login_insert_id = QtWidgets.QLineEdit(self.page_login)
        self.page_login_insert_id.setGeometry(QtCore.QRect(310, 240, 113, 20))
        self.page_login_insert_id.setObjectName("page_login_insert_id")
        self.page_login_insert_password = QtWidgets.QLineEdit(self.page_login)
        self.page_login_insert_password.setGeometry(QtCore.QRect(310, 270, 113, 20))
        self.page_login_insert_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.page_login_insert_password.setClearButtonEnabled(False)
        self.page_login_insert_password.setObjectName("page_login_insert_password")
        self.textEdit = QtWidgets.QTextEdit(self.page_login)
        self.textEdit.setGeometry(QtCore.QRect(500, 50, 201, 241))
        self.textEdit.setObjectName("textEdit")
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
        self.stacked_main.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "MainWindow"))
        self.page_login_button_login.setText(_translate("main_window", "Login"))
        self.page_login_combobox_user_type.setItemText(0, _translate("main_window", "Patient"))
        self.page_login_combobox_user_type.setItemText(1, _translate("main_window", "Radiologist"))
        self.page_login_combobox_user_type.setItemText(2, _translate("main_window", "Doctor"))
        self.page_login_insert_id.setText(_translate("main_window", "0000"))
        self.page_login_insert_id.setPlaceholderText(_translate("main_window", "ID"))
        self.page_login_insert_password.setText(_translate("main_window", "0000"))
        self.page_login_insert_password.setPlaceholderText(_translate("main_window", "Password"))
        self.textEdit.setHtml(_translate("main_window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Patients:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">id: 0000 pw: 0000</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_main_window()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())

