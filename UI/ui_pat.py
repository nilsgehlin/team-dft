# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_pat.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_stacked_pat(object):
    def setupUi(self, stacked_pat):
        stacked_pat.setObjectName("stacked_pat")
        stacked_pat.resize(800, 559)
        self.page_pat_home = QtWidgets.QWidget()
        self.page_pat_home.setObjectName("page_pat_home")
        self.label = QtWidgets.QLabel(self.page_pat_home)
        self.label.setGeometry(QtCore.QRect(280, 210, 191, 91))
        self.label.setObjectName("label")
        stacked_pat.addWidget(self.page_pat_home)

        self.retranslateUi(stacked_pat)
        QtCore.QMetaObject.connectSlotsByName(stacked_pat)

    def retranslateUi(self, stacked_pat):
        _translate = QtCore.QCoreApplication.translate
        stacked_pat.setWindowTitle(_translate("stacked_pat", "StackedWidget"))
        self.label.setText(_translate("stacked_pat", "PATIENT HOME PAGE"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    stacked_pat = QtWidgets.QStackedWidget()
    ui = Ui_stacked_pat()
    ui.setupUi(stacked_pat)
    stacked_pat.show()
    sys.exit(app.exec_())

