import vtk
from vtk.util import keys
from imageReader.imageReader import imageReader

# TODO:
#1. Add MR volume properties

class visualizationEngine(object):
    ##### Class Variables #####
    renderWindow = None
    interactor = None

    # Reader
    imageReader = None
    reader = None

    # Renderer Variables
    _imageRenderer = "IMAGE_RENDERER"
    _volumeRenderer = "VOLUME_RENDERER"
    _rendererTypeKey = None
    _rendererNumKey = None
    _previousActiveRenderer = None

    # Interactor styles
    _imageInteractor = None
    _volumeInteractor = None

    # Slice control
    _cuttingPlaneState = False

    # 2d image viewers array
    imageViewers = []

    # CT tissue opacity ranges
    CT_BONE = [275, 3000]
    CT_MUSCLE = [20, 40]
    CT_SOFT_TISSUE = [75, 150]
    CT_FAT = [-70, -30]
    

    ##### General class functions #####

    # Initializer for the image engine, takes the directory of the files as argument
    def __init__(self, dir):
        # Create the renderer type and number key
        self._rendererTypeKey = vtk.vtkDataObject().DATA_TYPE_NAME()
        self._rendererNumKey = vtk.vtkDataObject().DATA_PIECE_NUMBER()

        # Set the default interactor styles
        self._imageInteractor = vtk.vtkInteractorStyleImage()
        self._volumeInteractor = vtk.vtkInteractorStyleTrackballCamera()

        # Set the image reader
        self.SetDirectory(dir)

    
    ##################################
    ##### Public class functions #####
    ##################################


    # Set the read DICOM information into the window
    def SetDirectory(self,dir):
        image_reader = imageReader(dir)
        self.reader = image_reader.readDicom()
        #self.reader = image_reader.readTiff()
        self.imageReader = image_reader


    # Sets up a 2D image window in the engine
    def SetupImageUI(self, vtkWidget):
        renderer = vtk.vtkRenderer()
        renderer.ResetCamera()
        renderer.GetInformation().Set(self._rendererTypeKey,self._imageRenderer)
        renderer.GetInformation().Set(self._rendererNumKey,len(self.imageViewers))

        vtkWidget.GetRenderWindow().AddRenderer(renderer)
        interactor = vtkWidget.GetRenderWindow().GetInteractor()

        image_viewer = vtk.vtkResliceImageViewer()
        image_viewer.SetInputData(self.reader.GetOutput())
        # image_viewer.SetInputConnection(reader.GetOutputPort())

        image_viewer.SetRenderWindow(vtkWidget.GetRenderWindow())
        image_viewer.SetupInteractor(interactor)
        image_viewer.SetRenderer(renderer)
        image_viewer.Render()

        self.imageViewers.append(image_viewer)

        picker = vtk.vtkPointPicker()
        interactor.SetPicker(picker)

        # Add interactor observers
        interactor.AddObserver("LeftButtonPressEvent", self.__on_left_mouse_button_press, 101.0)

        interactor.Initialize()
    
        
    # Sets up a 3D volume window in the engine
    def SetupVolumeUI(self, vtkWidget):
        renderer = vtk.vtkRenderer()
        renderer.GetInformation().Set(self._rendererTypeKey,self._volumeRenderer)
        
        vtkWidget.GetRenderWindow().AddRenderer(renderer)
        interactor = vtkWidget.GetRenderWindow().GetInteractor()

        # extract data from the volume
        # extract = vtk.vtkExtractVOI()
        # extract.SetInputConnection(self.reader.GetOutputPort())
        # extract.SetVOI(0, 200, 0, 100, 0, 90)
        # extract.SetSampleRate(1, 1, 1)

        volume_mapper = vtk.vtkSmartVolumeMapper()
        volume_mapper.SetInputConnection(self.reader.GetOutputPort())
        volume_mapper.SetBlendModeToComposite()
        
        volumeProperty = self.__SetVolumeProperties("ALL")
    
        # The vtkVolume is a vtkProp3D (like a vtkActor) and controls the position
        # and orientation of the volume in world coordinates.
        volume = vtk.vtkVolume()
        volume.SetMapper(volume_mapper)
        volume.SetProperty(volumeProperty)

        # Finally, add the volume to the renderer
        renderer.AddViewProp(volume)

        # Set up an initial view of the volume.  The focal point will be the
        # center of the volume, and the camera position will be 400mm to the
        # patient's left (which is our right).
        camera = renderer.GetActiveCamera()
        c = volume.GetCenter()
        camera.SetFocalPoint(c[0], c[1], c[2])
        camera.SetPosition(c[0] + 1000, c[1], c[2])
        camera.SetViewUp(0, 0, -1)

        interactor.Initialize()


    # Determines what tissue to show given the vtkWidget and the tissue name
    def SetTissue(self, vtkWidget, tissue):
        renderer = vtkWidget.FindPokedRenderer(1,1)
        volume = renderer.GetViewProps().GetLastProp()
        volumeProperty = self.__SetVolumeProperties(tissue)
        volume.SetProperty(volumeProperty)

        # Finally, add the volume to the renderer
        renderer.AddViewProp(volume)

        vtkWidget.Initialize() 


    ###################################
    ##### Private class functions #####
    ###################################


    ##### Event callback functions #####

    # Mouse move event call back:
    # 1. Determines the right interactor style for the renderer
    # 2. Sets the right mouse wheel response for the viewer
    def __on_mouse_move(self, obj, event):
        pos = obj.GetEventPosition()
        renderer = self.interactor.FindPokedRenderer(pos[0],pos[1])
        
        if(renderer is self._previousActiveRenderer):
            return
        else:
            self._previousActiveRenderer = renderer
        
        renderer_type = renderer.GetInformation().Get(self._rendererTypeKey)
        
        if(renderer_type == self._imageRenderer):
            self.interactor.SetInteractorStyle(self._imageInteractor)
            for viewer in self.imageViewers:
                viewer.SliceScrollOnMouseWheelOff()
            num = renderer.GetInformation().Get(self._rendererNumKey)
            self.imageViewers[num].SliceScrollOnMouseWheelOn()
        elif (renderer_type == self._volumeRenderer):
            for viewer in self.imageViewers:
                viewer.SliceScrollOnMouseWheelOff()
            self.interactor.SetInteractorStyle(self._volumeInteractor)


    # Listener for left mouse button press:
    #   Gets mouse position in current window pixels and converts 
    #   them to pixel position based on initial image size,
    #   with the origin at the bottom left corner
    def __on_left_mouse_button_press(self, obj, event):
        mouse_pos = obj.GetEventPosition()

        obj.GetPicker().Pick(mouse_pos[0],mouse_pos[1])

        current_image_size = obj.GetSize()
        init_image_size = obj.FindPokedRenderer(mouse_pos[0],mouse_pos[1]).GetInformation().Get(self._initSizeKey)
        posX = int(round(mouse_pos[0] * init_image_size[0] / current_image_size[0]))
        posY = int(round(mouse_pos[1] * init_image_size[1] / current_image_size[1]))
        


    ##### Image display functions #####

    # actor = vtk.vtkImageActor()
    # actor.SetInputData(extract.GetOutput())
    # actor.SetOrigin(0, 120, 0)
    # actor.SetOrientation(90, 0, 0)
    # actor.GetMapper().SetSliceNumber(25)

    # renderer.AddActor(actor)


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
    def __SetVolumeProperties(self, *args):
        modality = self.imageReader.getModality()

        volume_color = self.__SetColor(modality)
        volume_scalar_opacity = self.__SetScalarOpacity(modality, args)
        volume_gradient_opacity = self.__SetGradientOpacity()
        
        volumeProperty = vtk.vtkVolumeProperty()
        volumeProperty.SetColor(volume_color)
        volumeProperty.SetScalarOpacity(volume_scalar_opacity)
        volumeProperty.SetGradientOpacity(volume_gradient_opacity)
        volumeProperty.SetInterpolationTypeToLinear()
        volumeProperty.ShadeOn()
        volumeProperty.SetAmbient(0.4)
        volumeProperty.SetDiffuse(0.6)
        volumeProperty.SetSpecular(0.2)
        return volumeProperty


    # Defines different volume colors
    def __SetColor(self,modality):
        volume_color = vtk.vtkColorTransferFunction()
        if modality == "CT":
            volume_color.AddRGBPoint(-1024, 0.0, 1.0, 0.0)

            volume_color.AddRGBPoint(-71, 0.0, 0.0, 0.0)
            volume_color.AddRGBPoint(-70, 0.94, 0.8, 0.7)
            volume_color.AddRGBPoint(-30, 0.94, 0.8, 0.7)
            volume_color.AddRGBPoint(-29, 0.0, 0.0, 0.0)

            volume_color.AddRGBPoint(19, 0.0, 0.0, 0.0)
            volume_color.AddRGBPoint(20, 1.0, 0.0, 0.0)
            volume_color.AddRGBPoint(40, 1.0, 0.0, 0.0)
            volume_color.AddRGBPoint(41, 0.0, 0.0, 0.0)

            volume_color.AddRGBPoint(74, 0.0, 0.0, 0.0)
            volume_color.AddRGBPoint(75, 1.0, 0.6, 1.0)
            volume_color.AddRGBPoint(150, 1.0, 0.6, 1.0)
            volume_color.AddRGBPoint(151, 0.0, 0.0, 0.0)

            volume_color.AddRGBPoint(274, 0.0, 0.0, 0.0) # bone
            volume_color.AddRGBPoint(275, 1.0, 0.9, 0.9)
            volume_color.AddRGBPoint(3000, 1.0, 0.9, 0.9)
            volume_color.AddRGBPoint(3001, 0.0, 0.0, 0.0)

            volume_color.AddRGBPoint(4096, 0.0, 1.0, 0.0)
        elif modality == "MR":
            volume_color.AddRGBPoint(-1024, 0.0, 1.0, 0.0)

            volume_color.AddRGBPoint(-71, 0.0, 0.0, 0.0)
            volume_color.AddRGBPoint(-70, 0.94, 0.8, 0.7)
            volume_color.AddRGBPoint(-30, 0.94, 0.8, 0.7)
            volume_color.AddRGBPoint(-29, 0.0, 0.0, 0.0)

            volume_color.AddRGBPoint(19, 0.0, 0.0, 0.0)
            volume_color.AddRGBPoint(20, 1.0, 0.0, 0.0)
            volume_color.AddRGBPoint(40, 1.0, 0.0, 0.0)
            volume_color.AddRGBPoint(41, 0.0, 0.0, 0.0)

            volume_color.AddRGBPoint(74, 0.0, 0.0, 0.0)
            volume_color.AddRGBPoint(75, 1.0, 0.6, 1.0)
            volume_color.AddRGBPoint(150, 1.0, 0.6, 1.0)
            volume_color.AddRGBPoint(151, 0.0, 0.0, 0.0)

            volume_color.AddRGBPoint(274, 0.0, 0.0, 0.0) # bone
            volume_color.AddRGBPoint(275, 1.0, 0.9, 0.9)
            volume_color.AddRGBPoint(3000, 1.0, 0.9, 0.9)
            volume_color.AddRGBPoint(3001, 0.0, 0.0, 0.0)

            volume_color.AddRGBPoint(4096, 0.0, 1.0, 0.0)
        return volume_color


    # The opacity transfer function is used to control the opacity
    # of different tissue types.
    def __SetScalarOpacity(self, modality, opts):
        volume_scalar_opacity = vtk.vtkPiecewiseFunction()
        if modality == "CT":
            volume_scalar_opacity.AddPoint(-1024,0.00)
            volume_scalar_opacity.AddPoint(4095, 0.00)
            for opt in opts:
                if opt == "ALL":
                    self.__AddOpacityPoints([-100,3000], volume_scalar_opacity)
                    break
                if opt == "BONE":
                    self.__AddOpacityPoints([275, 3000], volume_scalar_opacity)
                if opt == "SOFT":
                    self.__AddOpacityPoints([75, 150], volume_scalar_opacity)
                if opt == "MUSCLE":
                    self.__AddOpacityPoints([20, 40], volume_scalar_opacity)
                if opt == "FAT":
                    self.__AddOpacityPoints([-70, -30], volume_scalar_opacity)
        elif modality == "MR":
            volume_scalar_opacity.AddPoint(-1024,0.00)
            volume_scalar_opacity.AddPoint(4095, 0.00)
            for opt in opts:
                if opt == "ALL":
                    self.__AddOpacityPoints([-100,3000], volume_scalar_opacity)
                    break
                if opt == "BONE":
                    self.__AddOpacityPoints([275, 3000], volume_scalar_opacity)
                if opt == "SOFT":
                    self.__AddOpacityPoints([75, 150], volume_scalar_opacity)
                if opt == "MUSCLE":
                    self.__AddOpacityPoints([20, 40], volume_scalar_opacity)
                if opt == "FAT":
                    self.__AddOpacityPoints([-70, -30], volume_scalar_opacity)
        return volume_scalar_opacity

    def __AddOpacityPoints(self, limits, volume_scalar_opacity):
        volume_scalar_opacity.AddPoint(limits[0] - 1, 0.00)
        volume_scalar_opacity.AddPoint(limits[0], 0.20)
        volume_scalar_opacity.AddPoint(limits[1], 0.20)
        volume_scalar_opacity.AddPoint(limits[1] + 1, 0.00)

    def __RemoveOpacityPoints(self, limits, volume_scalar_opacity):
        volume_scalar_opacity.RemovePoint(limits[0] - 1)
        volume_scalar_opacity.RemovePoint(limits[0])
        volume_scalar_opacity.RemovePoint(limits[1])
        volume_scalar_opacity.RemovePoint(limits[1] + 1)


    # The gradient opacity function is used to decrease the opacity
    # in the "flat" regions of the volume while maintaining the opacity
    # at the boundaries between tissue types.  The gradient is measured
    # as the amount by which the intensity changes over unit distance.
    # For most medical data, the unit distance is 1mm.
    def __SetGradientOpacity(self):
        volume_gradient_opacity = vtk.vtkPiecewiseFunction()
        volume_gradient_opacity.AddPoint(0, 0.0)
        volume_gradient_opacity.AddPoint(90, 0.5)
        volume_gradient_opacity.AddPoint(100, 1.0)
        return volume_gradient_opacity






