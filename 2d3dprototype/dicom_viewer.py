import vtk
import os


def dicom_viewer(directory, slice_queue, mouse_move_event):
    filenames = vtk.vtkStringArray()
    for i, filename in enumerate(os.listdir(directory)):
        filenames.InsertNextValue(os.path.join(directory, filename))

    reader = vtk.vtkTIFFReader()
    reader.SetFileNames(filenames)
    reader.Update()

    image_viewer = vtk.vtkResliceImageViewer()
    image_viewer.SetInputData(reader.GetOutput())
    # image_viewer.SetInputConnection(reader.GetOutputPort())
    interactor = vtk.vtkRenderWindowInteractor()
    image_viewer.SetupInteractor(interactor)
    image_viewer.Render()
    image_viewer.GetRenderer().ResetCamera()
    image_viewer.Render()

    # def on_mouse_move(obj, event):
    #     mouse_queue.put(obj.GetEventPosition())
    #     mouse_move_event.set()
    #     return

    def on_scroll_wheel_move(obj, event):
        slice_queue.put(image_viewer.GetSlice())
        return

    # interactor.AddObserver("MouseMoveEvent", on_mouse_move)
    interactor.AddObserver("MouseWheelForwardEvent", on_scroll_wheel_move, 100.0)
    interactor.AddObserver("MouseWheelBackwardEvent", on_scroll_wheel_move, 100.0)
    interactor.Start()

if __name__ == '__main__':
    dicom_viewer()
