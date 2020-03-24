from PyQt5 import uic
from PyQt5 import QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk


Form, Window = uic.loadUiType("test.ui")

app = QtWidgets.QApplication([])
window = Window()

#Kanske bort
window.frame = QtWidgets.QFrame()

window.vl = QtWidgets.QVBoxLayout()
window.vtkWidget = QVTKRenderWindowInteractor(window.frame)
window.vl.addWidget(window.vtkWidget)

window.ren = vtk.vtkRenderer()
window.vtkWidget.GetRenderWindow().AddRenderer(window.ren)
window.iren = window.vtkWidget.GetRenderWindow().GetInteractor()

# Create source
source = vtk.vtkSphereSource()
source.SetCenter(0, 0, 0)
source.SetRadius(5.0)

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

window.ren.AddActor(actor)

window.ren.ResetCamera()

window.frame.setLayout(window.vl)
print(window.objectName())




form = Form()
form.setupUi(window)
window.show()
app.exec_()