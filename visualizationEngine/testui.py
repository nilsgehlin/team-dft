# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

import os
from visualizationEngine import visualizationEngine

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1250, 1000)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(700, 950, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(640, 10, 600, 450))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vtkWidget.setGeometry(QtCore.QRect(10, 10, 580, 480))
        self.vtkWidget.setObjectName("vtkWidget")

        self.frame1 = QtWidgets.QFrame(Dialog)
        self.frame1.setGeometry(QtCore.QRect(640, 475, 600, 450))
        self.frame1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame1.setObjectName("frame1")
        self.vtkWidget1 = QVTKRenderWindowInteractor(self.frame1)
        self.vtkWidget1.setGeometry(QtCore.QRect(10, 10, 580, 480))
        self.vtkWidget1.setObjectName("vtkWidget1")

        self.frame2 = QtWidgets.QFrame(Dialog)
        self.frame2.setGeometry(QtCore.QRect(10, 10, 600, 500))
        self.frame2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame2.setObjectName("frame2")
        self.vtkWidget2 = QVTKRenderWindowInteractor(self.frame2)
        self.vtkWidget2.setGeometry(QtCore.QRect(10, 10, 580, 480))
        self.vtkWidget2.setObjectName("vtkWidget2")

        # Button group for part X Demo
        self.tissueButtonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.tissueButtonBox.setGeometry(QtCore.QRect(100, 550, 341, 32))
        self.tissueButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.tissueButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Save|QtWidgets.QDialogButtonBox.Open)
        self.tissueButtonBox.button(self.tissueButtonBox.Ok).setText('ALL')
        self.tissueButtonBox.button(self.tissueButtonBox.Cancel).setText('SOFT')
        self.tissueButtonBox.button(self.tissueButtonBox.Save).setText('BONE')
        self.tissueButtonBox.button(self.tissueButtonBox.Open).setText('FAT')
        self.tissueButtonBox.setObjectName("tissueButtonBox")

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

    # DICOM file directory in sample_files/dicom
    # directory = os.path.join("..", "sample_dicom", "chestDICOM")
    directory = os.path.join("..", "sample_dicom", "stanford-ct-new")
    
    # Tiff images in 2d3dprototype/stanford-ct-new
    #directory = os.path.join("..", "2d3dprototype", "stanford-ct-new")  

    vtk_engine = visualizationEngine(directory)
    vtk_engine.SetupImageUI(ui.vtkWidget, "CORONAL")
    vtk_engine.SetupImageUI(ui.vtkWidget1, "SAGITTAL")
    #vtk_engine.SetupImageUI(ui.vtkWidget2, "SAGITTAL")
    vtk_engine.SetupVolumeUI(ui.vtkWidget2)

    linked = False

    # Rough implementation of button press for Part X demo
    def clicked_all():
        vtk_engine.SetTissue(ui.vtkWidget2, "ALL")

    def clicked_soft():
        vtk_engine.SetTissue(ui.vtkWidget2, "SOFT")

    def clicked_bone():
        vtk_engine.SetTissue(ui.vtkWidget2, "BONE")

    def clicked_fat():
        #vtk_engine.SetTissue(ui.vtkWidget2, "FAT")
        global linked
        if linked:
            linked = False
            vtk_engine.UnlinkWindows(ui.vtkWidget)
            vtk_engine.SetTransparency(ui.vtkWidget2, 0.2)
        else:
            linked = True
            vtk_engine.SetTransparency(ui.vtkWidget2, 0.08)
            vtk_engine.LinkWindows(ui.vtkWidget, ui.vtkWidget1, ui.vtkWidget2)

    ui.tissueButtonBox.button(ui.tissueButtonBox.Ok).clicked.connect(clicked_all)
    ui.tissueButtonBox.button(ui.tissueButtonBox.Cancel).clicked.connect(clicked_soft)
    ui.tissueButtonBox.button(ui.tissueButtonBox.Save).clicked.connect(clicked_bone)
    ui.tissueButtonBox.button(ui.tissueButtonBox.Open).clicked.connect(clicked_fat)

    Dialog.show()
    sys.exit(app.exec_())



