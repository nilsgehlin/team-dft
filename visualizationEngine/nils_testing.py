import vtk
import os
import numpy as np
from vtk.util import numpy_support
import pydicom

def vtk_type(numpy_type):
    vtk_type_by_numpy_type = {
        np.uint8: vtk.VTK_UNSIGNED_CHAR,
        np.uint16: vtk.VTK_UNSIGNED_SHORT,
        np.uint32: vtk.VTK_UNSIGNED_INT,
        np.uint64: vtk.VTK_UNSIGNED_LONG if vtk.VTK_SIZEOF_LONG == 64 else vtk.VTK_UNSIGNED_LONG_LONG,
        np.int8: vtk.VTK_CHAR,
        np.int16: vtk.VTK_SHORT,
        np.int32: vtk.VTK_INT,
        np.int64: vtk.VTK_LONG if vtk.VTK_SIZEOF_LONG == 64 else vtk.VTK_LONG_LONG,
        np.float32: vtk.VTK_FLOAT,
        np.float64: vtk.VTK_DOUBLE
    }
    return vtk_type_by_numpy_type[numpy_type.type]

def np_to_vtk(array):
    vtk_datatype = vtk_type(array.dtype)
    vtk_array = numpy_support.numpy_to_vtk(array.ravel(), deep=True, array_type=vtk_datatype)
    vtk_array.SetNumberOfComponents(array.shape[-1])

    output_vtk_image = vtk.vtkImageData()
    output_vtk_image.SetDimensions(array.shape[1], array.shape[0], array.shape[-1])
    output_vtk_image.SetSpacing([1, 1, 1])
    output_vtk_image.SetOrigin([0, 0, 0])
    output_vtk_image.GetPointData().SetScalars(vtk_array)

    return output_vtk_image

def update_vtk_with_np(vtk_image_data, array):
    vtk_array = numpy_support.numpy_to_vtk(array.ravel(), deep=True, array_type=vtk_type(array.dtype))
    vtk_array.SetNumberOfComponents(array.shape[-1])
    vtk_image_data.GetPointData().SetScalars(vtk_array)
    vtk_image_data.Modified()


def dicom_to_array(dir):
    dir_list = os.listdir(dir)
    rows, cols = pydicom.dcmread(os.path.join(dir, dir_list[0])).pixel_array.shape
    depth = len(dir_list)
    output_array = np.zeros((rows, cols, depth))
    for slice_idx, filename in enumerate(dir_list):
        output_array[:, :, slice_idx] = pydicom.dcmread(os.path.join(dir, filename)).pixel_array
    output_array = np.stack((output_array,) * 3, axis=-1)
    return output_array

def on_left_mouse_button_press(obj, event):
    mouse_pos = obj.GetEventPosition()
    renderer = obj.FindPokedRenderer(mouse_pos[0], mouse_pos[1])
    obj.GetPicker().Pick(mouse_pos[0], mouse_pos[1], 0, renderer)
    clicked_coordinate = obj.GetPicker().GetPickPosition()
    array[int(clicked_coordinate[1])-50:int(clicked_coordinate[1])+50:, int(clicked_coordinate[0])-50:int(clicked_coordinate[0])+50, 2] = 255
    update_vtk_with_np(image, array)


slice_no = 25
array = dicom_to_array(os.path.join("..", "sample_dicom", "1"))
array = array[:, :, 20, :]
image = np_to_vtk(array)


imageActor = vtk.vtkImageActor()
imageActor.SetInputData(image)
renderer = vtk.vtkRenderer()
renderer.AddActor(imageActor)
renderer.ResetCamera()

renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtk.vtkRenderWindowInteractor()
style = vtk.vtkInteractorStyleImage()
renderWindowInteractor.SetInteractorStyle(style)
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.AddObserver("LeftButtonPressEvent", on_left_mouse_button_press, 101.0)
# renderWindowInteractor.AddObserver("MouseWheelForwardEvent", on_mouse_wheel_forward, 101.0)
renderWindowInteractor.Initialize()
renderWindowInteractor.Start()
