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

    # Store the initial image size
    init_image_size = None
    init_image_size = interactor.GetSize()

    # def on_mouse_move(obj, event):
    #     mouse_queue.put(obj.GetEventPosition())
    #     mouse_move_event.set()
    #     return

    def on_scroll_wheel_move(obj, event):
        slice_queue.put(image_viewer.GetSlice())
        return

    # Listener for left mouse button press:
    #   Gets mouse position in current window pixels and converts 
    #   them to pixel position based on initial image size,
    #   with the origin at the bottom left corner
    def on_left_mouse_button_press(obj, event):
        if(init_image_size != None):
            mouse_position = obj.GetEventPosition()
            current_image_size = obj.GetSize()
            posX = int(round(mouse_position[0] * init_image_size[0] / current_image_size[0]))
            posY = int(round(mouse_position[1] * init_image_size[1] / current_image_size[1]))
            print(posX,posY)
        return

    # Add left mouse button press observer
    interactor.AddObserver("LeftButtonPressEvent", on_left_mouse_button_press, 101.0)

    # interactor.AddObserver("MouseMoveEvent", on_mouse_move)
    interactor.AddObserver("MouseWheelForwardEvent", on_scroll_wheel_move, 100.0)
    interactor.AddObserver("MouseWheelBackwardEvent", on_scroll_wheel_move, 100.0)
    interactor.Start()

if __name__ == '__main__':
    dicom_viewer()
