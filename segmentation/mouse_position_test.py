import os
import vtk
from vtk import vtkDICOMImageReader

def read_tiff(directory):
    # Accumulate file names
    filenames = vtk.vtkStringArray()
    for i, filename in enumerate(os.listdir(directory)):
        filenames.InsertNextValue(os.path.join(directory, filename))
    # Create reader object with filenames
    reader = vtk.vtkTIFFReader()
    reader.SetFileNames(filenames)
    reader.Update()
    return reader

def read_dicom(directory):
    # Create reader object ans set directory name
    reader = vtkDICOMImageReader()
    reader.SetDirectoryName(directory)
    # Set other settings and update
    reader.SetDataByteOrderToLittleEndian()
    #data_spacing = (1, 1, 2)
    #reader.SetDataSpacing(data_spacing[0], data_spacing[1], data_spacing[2])
    reader.Update()
    return reader

def display_images(reader):
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

    interactor.Start()


if __name__ == '__main__':
    ## Reads dicom files defined on the directory
    # directory_dicom = os.path.join("..", "sample_files", "dicom")
    # reader = read_dicom(directory_dicom)
    
    ## Reads the tiff images in 2d3dprototype/stanford-ct-new
    directory = os.path.join("..", "2d3dprototype", "stanford-ct-new")
    reader = read_tiff(directory)    

    ## Setsup display window and display images
    display_images(reader)
    

