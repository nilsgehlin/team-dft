# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from vtk_test import VTK_Test
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(778, 635)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(240, 460, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(360, 230, 291, 191))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vtkWidget.setGeometry(QtCore.QRect(10, 10, 271, 171))
        self.vtkWidget.setObjectName("vtkWidget")


        self.frame2 = QtWidgets.QFrame(Dialog)
        self.frame2.setGeometry(QtCore.QRect(10, 10, 291, 191))
        self.frame2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame2.setObjectName("frame2")
        self.vtkWidget2 = QVTKRenderWindowInteractor(self.frame2)
        self.vtkWidget2.setGeometry(QtCore.QRect(10, 10, 271, 171))
        self.vtkWidget2.setObjectName("vtkWidget2")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    vtk_test = VTK_Test()
    vtk_test.setupUI(ui.vtkWidget)


    vtk_test2 = VTK_Test()
    vtk_test.setupUI(ui.vtkWidget2)
    Dialog.show()
    sys.exit(app.exec_())

