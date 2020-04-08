import vtk
import os

from vtk import vtkDICOMImageReader
from vtk import vtkImageShiftScale
from vtk import vtkPNGWriter

# class CommandSubclass2(vtk.vtkCommand):
#     def __init__(self, interactor):
#         self.interactor = interactor
#         super().__init__()
#
#         def Execute(caller, eventId, callData):
#             print("timer callback")
#             self.ExitCallback()

def render3d(directory):
    # Create the renderer, the render window, and the interactor. The renderer
    # draws into the render window, the interactor enables mouse- and
    # keyboard-based interaction with the scene.
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.SetWindowName("Test")
    render_window.AddRenderer(renderer)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    # The following reader is used to read a series of 2D slices (images)
    # that compose the volume. The slice dimensions are set, and the
    # pixel spacing. The data Endianness must also be specified. The reader
    # usese the FilePrefix in combination with the slice number to construct
    # filenames using the format FilePrefix.%d. (In this case the FilePrefix
    # is the root name of the file: quarter.)
    reader = vtkDICOMImageReader()
    reader.SetDataByteOrderToLittleEndian()
    # reader.SetFilePrefix(os.path.join(directory, "000"))
    reader.SetDirectoryName(directory)
    data_spacing = (1, 1, 2)
    reader.SetDataSpacing(data_spacing[0], data_spacing[1], data_spacing[2])
    # reader.update()
    image = reader.GetOutput()

    # pointData = image.GetPointData()
    # pointDataRange = pointData.GetScalars().GetRange()
    # print(pointDataRange)

    shiftScaleFilter = vtkImageShiftScale()
    shiftScaleFilter.SetOutputScalarTypeToUnsignedChar()
    shiftScaleFilter.SetInputConnection(reader.GetOutputPort())

    shiftScaleFilter.SetShift(-1.0 * image.GetScalarRange()[0])
    oldRange = image.GetScalarRange()[1] - image.GetScalarRange()[0]
    newRange = 255

    shiftScaleFilter.SetScale(newRange / oldRange)
    shiftScaleFilter.Update()

    # reader.SetDataDimensions(256, 256)
    # reader.SetImageRange(1, 203)
    # reader.SetDataByteOrderToLittleEndian()
    # reader.SetFilePrefix(os.path.join(directory,'MRbrain'))
    # data_spacing = (1, 1, 2)
    # reader.SetDataSpacing(data_spacing[0], data_spacing[1], data_spacing[2])

    volume_mapper = vtk.vtkSmartVolumeMapper()
    volume_mapper.SetInputConnection(reader.GetOutputPort())
    volume_mapper.SetBlendModeToComposite()

    # Cutting plane
    plane = vtk.vtkPlane()
    plane.SetOrigin(0, 0, 2)
    plane.SetNormal(0, 0, 1)

    # create cutter
    cutter = vtk.vtkCutter()
    cutter.SetCutFunction(plane)
    cutter.SetInputConnection(reader.GetOutputPort())
    cutter.Update()
    cutterMapper = vtk.vtkPolyDataMapper()
    cutterMapper.SetInputConnection(cutter.GetOutputPort())

    # create plane actor
    planeActor = vtk.vtkActor()
    planeActor.GetProperty().SetColor(1.0, 1, 0)
    planeActor.GetProperty().SetLineWidth(2)
    planeActor.SetMapper(cutterMapper)

    volume_color = vtk.vtkColorTransferFunction()
    # volume_color.AddRGBPoint(0, 0.0, 0.0, 0.0)
    # volume_color.AddRGBPoint(500, 1.0, 0.5, 0.3)
    # volume_color.AddRGBPoint(1000, 1.0, 0.5, 0.3)
    # volume_color.AddRGBPoint(1150, 1.0, 1.0, 0.9)

    volume_color.AddRGBPoint(0, 0.0, 0.0, 1.0) # soft tissue
    volume_color.AddRGBPoint(500, 0.0, 1.0, 0.0) # bone
    # volume_color.AddRGBPoint(250, 0.0, 1.0, 0.0)
    volume_color.AddRGBPoint(1000, 0.0, 1.0, 0.0) # bone
    volume_color.AddRGBPoint(1150, 0.0, 1.0, 0.0) # bone

    # The opacity transfer function is used to control the opacity
    # of different tissue types.
    volume_scalar_opacity = vtk.vtkPiecewiseFunction()
    volume_scalar_opacity.AddPoint(0, 0.00)
    volume_scalar_opacity.AddPoint(500, 0.15)
    volume_scalar_opacity.AddPoint(1000, 0.85)
    volume_scalar_opacity.AddPoint(1150, 0.85)
    # volume_scalar_opacity.AddPoint(0, 0.15)
    # volume_scalar_opacity.AddPoint(100, 0.00)
    # volume_scalar_opacity.AddPoint(200, 0.00)
    # volume_scalar_opacity.AddPoint(300, 0.00)
    # volume_scalar_opacity.AddPoint(400, 0.00)
    # volume_scalar_opacity.AddPoint(500, 0.00)




    # The gradient opacity function is used to decrease the opacity
    # in the "flat" regions of the volume while maintaining the opacity
    # at the boundaries between tissue types.  The gradient is measured
    # as the amount by which the intensity changes over unit distance.
    # For most medical data, the unit distance is 1mm.
    volume_gradient_opacity = vtk.vtkPiecewiseFunction()
    volume_gradient_opacity.AddPoint(0, 0.0)
    volume_gradient_opacity.AddPoint(90, 0.5)
    volume_gradient_opacity.AddPoint(100, 1.0)

    # The VolumeProperty attaches the color and opacity functions to the
    # volume, and sets other volume properties.  The interpolation should
    # be set to linear to do a high-quality rendering.  The ShadeOn option
    # turns on directional lighting, which will usually enhance the
    # appearance of the volume and make it look more "3D".  However,
    # the quality of the shading depends on how accurately the gradient
    # of the volume can be calculated, and for noisy data the gradient
    # estimation will be very poor.  The impact of the shading can be
    # decreased by increasing the Ambient coefficient while decreasing
    # the Diffuse and Specular coefficient.  To increase the impact
    # of shading, decrease the Ambient and increase the Diffuse and Specular.
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(volume_color)
    volumeProperty.SetScalarOpacity(volume_scalar_opacity)
    volumeProperty.SetGradientOpacity(volume_gradient_opacity)
    volumeProperty.SetInterpolationTypeToLinear()
    volumeProperty.ShadeOn()
    volumeProperty.SetAmbient(0.4)
    volumeProperty.SetDiffuse(0.6)
    volumeProperty.SetSpecular(0.2)

    # The vtkVolume is a vtkProp3D (like a vtkActor) and controls the position
    # and orientation of the volume in world coordinates.
    volume = vtk.vtkVolume()
    volume.SetMapper(volume_mapper)
    volume.SetProperty(volumeProperty)

    # Finally, add the volume to the renderer
    renderer.AddViewProp(volume)
    renderer.AddActor(planeActor)

    # Set up an initial view of the volume.  The focal point will be the
    # center of the volume, and the camera position will be 400mm to the
    # patient's left (which is our right).
    camera = renderer.GetActiveCamera()
    c = volume.GetCenter()
    camera.SetFocalPoint(c[0], c[1], c[2])
    camera.SetPosition(c[0] + 1000, c[1], c[2])
    camera.SetViewUp(0, 0, -1)

    # Increase the size of the render window
    render_window.SetSize(640, 480)

    # Interact with the data.
    interactor.Initialize()

    # def test(arg1, arg2):
    #     slice_numbers = []
    #     while not mouse_queue.empty():
    #         slice_numbers += [mouse_queue.get()]
    #     if len(slice_numbers) > 0:
    #         slice = slice_numbers[-1]
    #         plane.SetOrigin(0, 0, data_spacing[2] * slice)
    #         render_window.Render()
    #
    # interactor.AddObserver(vtk.vtkCommand.TimerEvent, test)
    # timerId = interactor.CreateRepeatingTimer(1)
    render_window.Render()
    interactor.Start()


if __name__ == '__main__':
    # directory = r"chestDICOM"
    directory = r"chestDICOM"
    render3d(directory)