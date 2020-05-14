import vtk
from vtk.util import keys, numpy_support
# import os, sys
# path = os.path.join("imageReader")
# sys.path.insert(0, path)
# print(sys.path)
from imageReader.imageReader import imageReader
from segmentation.Segmentation import Segmentation
from annotation.annotation import Annotation, AnnotationStore, AnnotationStoreIterator

# TODO:
#1. Check rendering timer issues
#   -Behaving as if duration is fixed at 10ms
#2. Add color to cutting plane frames
#3. Expand tissue selection to allow multiple tissues
#4. Add coordinate limits for negatives and out of bounds segmentation point
#5. Way to know if segmentation in already in the renderer
#6. Find good way of updating display extent after creating actors
#   -In current implementations they update after the window is scrolled
#7. Add opacity of 1 to the 3D viewer so segmentation show up, or change segmentaion scalar?

class visualizationEngine(object):
    ##### Class Variables #####
    
    # Reader
    imageReader = None
    reader = None
    _pixelSpacing = None

    # Annotations
    annotationStore = None
    annotationKeys = []

    # Renderer Variables
    _imageRenderer = "IMAGE_RENDERER"
    _volumeRenderer = "VOLUME_RENDERER"
    _rendererTypeKey = None
    _rendererNumKey = None
    _rendererMPRKey = None
    _rendererObserverKey = None

    # Prop Variables
    _SegmentationProp = "SEGMENTATION_PROP"
    _CuttingPlaneProp = "CUTTING_PLANE_PROP"
    _propTypeKey = None

    # Interactor styles
    _imageInteractorStyle = None
    _volumeInteractorStyle = None

    # Slice control
    _masterID = None
    _masterMPR = None
    _slaves = None
    _showActiveSlice = True
    _crop3D = True

    # Slave Render Timer
    _renderTimerID = 0
    _renderTimeCount = 0

    # 2d image viewers array
    imageViewers = []

    # 3D Properties
    _3DTransparency = 0.2
    _3DTissue = "ALL"


    ##### General class functions #####

    # Initializer for the image engine
    def __init__(self):
        # Create the renderer relevant keys for accessing information
        self._rendererTypeKey = vtk.vtkDataObject().DATA_TYPE_NAME()
        self._rendererNumKey = vtk.vtkDataObject().DATA_PIECE_NUMBER()
        self._rendererObserverKey = keys.MakeKey(keys.IntegerKey, "OBSERVER", "Engine")
        self._rendererMPRKey = keys.MakeKey(keys.StringKey, "ORIENTATION", "Engine")
        self._propTypeKey = vtk.vtkDataObject().DATA_TYPE_NAME()

        # Set the default interactor styles
        self._imageInteractorStyle = vtk.vtkInteractorStyleImage()
        self._volumeInteractorStyle = vtk.vtkInteractorStyleTrackballCamera()

        # Set the annotation store
        self.annotationStore = AnnotationStore()
    
    ##################################
    ##### Public class functions #####
    ##################################


    # Manually changes the read DICOM information into the engine
    # AVOID CALLING IF WINDOWS HAVE BEEN SET UP
    #   Parameters:
    #       1. Directory, containing DICOM files
    def SetDirectory(self, dir):
        print("1")
        image_reader = imageReader(dir)
        print("2")
        print(dir)
        self.reader = image_reader.readImages()
        print("3")
        self._pixelSpacing = image_reader.getPixelSpacing()
        print("4")
        self.imageReader = image_reader
        print("5")


    # Sets up a 2D image window for the given widget
    #   Parameters: 
    #       1. vtkWidget, 
    #       2. (optional) plane orientation i.e AXIAL, SAGITTAL or CORONAL
    #   Notes:
    #       -If not orientation is provided it shows default orientation
    #       -Currently only does MPR with AXIAL, SAGITTAL and CORONAL only
    def SetupImageUI(self, vtkWidget, *args):
        # Creating image viewer
        image_viewer = vtk.vtkResliceImageViewer()
        image_viewer.SetInputData(self.reader.GetOutput())
        # image_viewer.SetInputConnection(rgbConverter.GetOutputPort())
        image_viewer.SetRenderWindow(vtkWidget.GetRenderWindow())

        # Connecting interactor to image viewer
        interactor = vtkWidget.GetRenderWindow().GetInteractor()
        image_viewer.SetupInteractor(interactor)

        # Setting up a renderer and connecting it to the image viewer
        renderer = vtk.vtkRenderer()
        renderer.ResetCamera()
        renderer.GetInformation().Set(self._rendererTypeKey, self._imageRenderer)
        renderer.GetInformation().Set(self._rendererNumKey, len(self.imageViewers))
        vtkWidget.GetRenderWindow().AddRenderer(renderer)
        image_viewer.SetRenderer(renderer)
        
        # Render the image_viewer
        image_viewer.Render()

        ## Perform MPR if required
        img_orien = self.imageReader.getPlaneOrientation()
        if(len(args) > 0):
            mpr = args[0]
            plane_id = self.__GetPlaneID(img_orien, mpr)
            image_viewer.SetSliceOrientation(plane_id)
            renderer.GetInformation().Set(self._rendererMPRKey, mpr)
        else:
            renderer.GetInformation().Set(self._rendererMPRKey, img_orien)

        self.imageViewers.append(image_viewer)

        # Add scroll listener to the viewer
        image_viewer.AddObserver("InteractionEvent", self.__on_slice_change, 1)

        # For now, add interactor ability for segmentation
        picker = vtk.vtkPointPicker()
        interactor.SetPicker(picker)
        interactor.AddObserver("LeftButtonPressEvent", self.__on_left_mouse_button_press, 1)

        interactor.Initialize()
    
        
    # Sets up a 3D volume window for the given widget
    #   Parameters: 
    #       1. vtkWidget
    #   Notes:
    #       -This initial setup does not do any tissue selection
    def SetupVolumeUI(self, vtkWidget):
        renderer = vtk.vtkRenderer()
        renderer.GetInformation().Set(self._rendererTypeKey,self._volumeRenderer)
        
        vtkWidget.GetRenderWindow().AddRenderer(renderer)
        interactor = vtkWidget.GetRenderWindow().GetInteractor()
        
        volume_mapper = vtk.vtkSmartVolumeMapper()
        volume_mapper.SetInputConnection(self.reader.GetOutputPort())        
        volume_mapper.SetBlendModeToComposite()
        
        volumeProperty = self.__SetVolumeProperties(self._3DTissue)
    
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

        interactor.SetInteractorStyle(self._volumeInteractorStyle)
        interactor.Initialize()


    # Determines what tissue to show given the vtkWidget and the tissue name
    #   Parameters: 
    #       1. vtkWidget
    #       2. Tissue i.e. ALL, BONE, SOFT, MUSCLE or FAT
    #   Notes:
    #       -Currently only takes one tissue at a time, could expand for more
    def SetTissue(self, vtkWidget, tissue):
        self._3DTissue = tissue
        renderer = self.__GetRenderer(vtkWidget)
        props = renderer.GetViewProps()
        props.InitTraversal()
        volume = props.GetNextProp()
        volumeProperty = self.__SetVolumeProperties(tissue)
        volume.SetProperty(volumeProperty)
        vtkWidget.GetRenderWindow().Render()


    # Changes the transparency of the tissue to show given the vtkWidget and the tissue name
    #   Parameters: 
    #       1. vtkWidget
    #       2. Transparency value
    #   Notes:
    def SetTransparency(self, vtkWidget, transparency):
        self._3DTransparency = transparency
        renderer = self.__GetRenderer(vtkWidget)
        props = renderer.GetViewProps()
        props.InitTraversal()
        volume = props.GetNextProp()
        volumeProperty = self.__SetVolumeProperties(self._3DTissue)
        volume.SetProperty(volumeProperty)
        vtkWidget.GetRenderWindow().Render()


    # Links scrolling of master window 'masterWidget' to slave windows in 'args'
    # ONLY a 2D image window can be a master.
    #   Parameters: 
    #       1. vtkWidget - Master
    #       2,3,4... vtkWidgets - Slaves
    #   Notes:
    #       -Provide each slave as its own arguments, NOT as an array
    #       -There can be only one master window for any engine instance. Make sure
    #           to unlink slaves before creating a new set of links. Unexpected behaviour
    #           if a new set of links are made without unlinking previous links
    def LinkWindows(self, masterWidget, *args):
        master_renderer_info = self.__GetRenderer(masterWidget).GetInformation()
        self._masterID = master_renderer_info.Get(self._rendererNumKey)
        self._masterMPR = master_renderer_info.Get(self._rendererMPRKey)
        if master_renderer_info.Get(self._rendererTypeKey) == self._imageRenderer:
            self._slaves = []
            for arg in args:
                self._slaves.append(arg)
            ob_id = masterWidget.AddObserver(vtk.vtkCommand.TimerEvent, self.__on_cutting_plane_change,2)
            master_renderer_info.Set(self._rendererObserverKey, ob_id)


    # Safely unlinks all window scrolling from the master window
    #   Parameters: 
    #       1. vtkWidget - Master
    #   Notes:
    #       -If a wrong master window is provided nothing happens
    def UnlinkWindows(self, masterWidget):
        master_renderer_info = self.__GetRenderer(masterWidget).GetInformation()
        if master_renderer_info.Get(self._rendererNumKey) == self._masterID: 
            self._masterID = None
            self._masterMPR = None
            ob_id = master_renderer_info.Get(self._rendererObserverKey)
            masterWidget.RemoveObserver(ob_id)

            for slave in self._slaves:
                renderer_info = self.__GetRenderer(slave).GetInformation()
                if renderer_info.Get(self._rendererTypeKey) == self._imageRenderer:
                    self.__CleanUpSlicePos(slave)
                elif renderer_info.Get(self._rendererTypeKey) == self._volumeRenderer:
                    self.__CleanUpCuttingPlanePos(slave)
            self._slaves = None


    # Performs segmentation for the given
    # ONLY segment if clicked in a 2D window
    #   Parameters:
    #       1. widget - vtkWidget
    #       2. mouse_pos - Mouse poisition of click
    #   Note:
    #       -Still in development
    def SegmentObject(self, widget, mouse_pos):

        renderer = widget.FindPokedRenderer(mouse_pos[0], mouse_pos[1])
        image_data = self.reader.GetOutput()

        # Get picked coordinate and convert viewer coordinate into pixel value coordinate
        widget.GetPicker().Pick(mouse_pos[0], mouse_pos[1], 0, renderer)
        clicked_coordinate = list(widget.GetPicker().GetPickPosition())
        for i in range(3):
            clicked_coordinate[i] = clicked_coordinate[i] / self._pixelSpacing[i]
        clicked_coordinate = tuple(clicked_coordinate)
        
        # Read the image data from vtk to numpy array and
        # reorganises the dimensions and scales the data
        cols, rows, slc = image_data.GetDimensions()
        volume = numpy_support.vtk_to_numpy(image_data.GetPointData().GetScalars())
        volume = volume.reshape(slc, rows, cols)
        volume = volume.transpose(2, 1, 0)

        # Create the segmentation
        segmentation = Segmentation(clicked_coordinate, volume, segmentation_threshold=0.2, verbose=True)
        segment_array = segmentation.GetScalars()
        segment_color = segmentation.GetColor()
        segment_actor = self.__CreateSegmentationActor(segment_array, segment_color)
        
        renderer.AddActor(segment_actor)
        widget.GetRenderWindow().Render()
        segment_actor.GetPropertyKeys().Set(self._propTypeKey, self._SegmentationProp)

        # Add segment as annotation
        segment_annot = Annotation()
        segment_annot.SetLocation(clicked_coordinate)
        segment_annot.SetColor(segment_color)
        segment_annot.FlagAsSegment(segment_array)
        key = self.annotationStore.StoreAnnotation(segment_annot)
        self.annotationKeys.append(key)
        
        return key


    # Displays the segmentations in the provided keys in the vtkWidget
    #   Parameters:
    #       1. vtkWidget - the target window
    #       2. keys - an array of segmentation keys to be accessed from the store
    #   Notes:
    #       -Have to update display extent after creating actor, not working for volume widgets
    def AddSegmentations(self, widget, keys):
        renderer = self.__GetRenderer(widget)
        renderer_info = renderer.GetInformation()

        for key in keys:
            annot = self.annotationStore.GetAnnotation(key)
            if(annot.isSegment()):
                segment_array = annot.GetSegmentData()
                segment_color = annot.GetColor()
                segment_actor = self.__CreateSegmentationActor(segment_array, segment_color)

                if renderer_info.Get(self._rendererTypeKey) == self._imageRenderer:
                    renderer.AddActor(segment_actor)            
                    widget.GetRenderWindow().Render()
                    segment_actor.GetPropertyKeys().Set(self._propTypeKey, self._SegmentationProp)
        
                elif renderer_info.Get(self._rendererTypeKey) == self._volumeRenderer:
                    segment_actor_info = vtk.vtkInformation()
                    segment_actor_info.Set(self._propTypeKey, self._SegmentationProp)
                    segment_actor.SetPropertyKeys(segment_actor_info)

                    renderer.AddActor(segment_actor)
        
        widget.GetRenderWindow().Render()


    # Returns all the annotation keys that are segmentations
    #   Parameters: None
    def GetAllSegmentationKeys(self):
        arr = []
        it = AnnotationStoreIterator(self.annotationStore)
        for key in it:
            if(self.annotationStore.GetAnnotation(key).isSegment()):
                arr.append(key)
        return arr


    # Returns all the annotation keys regardless of annotation type
    #   Parameters: None
    def GetAllAnnotationKeys(self):
        return self.annotationKeys


    # Returns a copy of the annotation store
    #   Parameters: None
    def GetAnnotationStore(self):
        store = AnnotationStore()
        store.DeepCopy(self.annotationStore)     
        

    ###################################
    ##### Private class functions #####
    ###################################


    ##### HELPER FUNCTIONS #####
    
    # Retrieves the renderer from the qvtkinteractor widget 
    def __GetRenderer(self, widget):
        # return widget.FindPokedRenderer(1,1)
        return widget.GetRenderWindow().GetRenderers().GetFirstRenderer()


    # Returns the plane ID depending on the original image orientation and
    # requested orientation
    def __GetPlaneID(self, img_orientation, win_orientation):
        if img_orientation == "SAGITTAL": orientation = 4
        elif img_orientation == "CORONAL": orientation = 3
        elif img_orientation == "AXIAL": orientation = 2
        else: orientation = 2
        
        if win_orientation == "SAGITTAL": orientation += 1
        elif win_orientation == "CORONAL": orientation += 2
        elif win_orientation == "AXIAL": orientation += 3

        return orientation % 3


    # Updates the position of the cutting plane in a 3D window
    def __UpdateCuttingPlanePos(self, widget, active_slice, mpr):
        renderer = self.__GetRenderer(widget)
        
        if (self._showActiveSlice):
            self.__addSliceToVolume(renderer)

        if (self._crop3D):
            img_orien = self.imageReader.getPlaneOrientation()
            plane_id = self.__GetPlaneID(img_orien, mpr)
            active_slice = active_slice * self._pixelSpacing[plane_id]
            if (plane_id == 0): idx = 1
            elif (plane_id == 1): idx = 3
            elif (plane_id == 2): idx = 5
            
            volume_mapper = renderer.GetVolumes().GetLastProp().GetMapper()
            if volume_mapper.GetCropping() == 0:
                volume_mapper.CroppingOn()
                volume_mapper.SetCroppingRegionFlagsToFence()
                cropping = [0,0.1,0,0.1,0,0.1]
                cropping[idx] = active_slice
                cropping = tuple(cropping)
                volume_mapper.SetCroppingRegionPlanes(cropping)
            else:
                cropping = list(volume_mapper.GetCroppingRegionPlanes())
                cropping[idx] = active_slice
                cropping = tuple(cropping)
                volume_mapper.SetCroppingRegionPlanes(cropping)


    # Adds the active slice of the master image viewer to the 3D renderer
    def __addSliceToVolume(self, renderer):
        props = renderer.GetViewProps()
        viewer = self.imageViewers[self._masterID]

        image_actor = None
        for prop in props:
            prop_property = prop.GetPropertyKeys()
            if prop_property == None: continue
            if prop_property.Get(self._propTypeKey) == self._CuttingPlaneProp:
                image_actor = prop
                break

        if image_actor == None:
            image_actor = vtk.vtkImageActor()
            image_actor.SetInputData(viewer.GetInput())
            image_actor_info = vtk.vtkInformation()
            image_actor_info.Set(self._propTypeKey, self._CuttingPlaneProp)
            image_actor.SetPropertyKeys(image_actor_info)
            renderer.AddActor(image_actor)

        viewer_actor = viewer.GetImageActor()
        image_actor.SetDisplayExtent(viewer_actor.GetDisplayExtent())
        image_actor.Update()

    
    # Cleans up 3D window to remove cutting plane 
    def __CleanUpCuttingPlanePos(self, widget):
        renderer = self.__GetRenderer(widget)
        volume_mapper = renderer.GetVolumes().GetLastProp().GetMapper()
        volume_mapper.CroppingOff()
        
        if (self._showActiveSlice):
            props = renderer.GetViewProps()
            for prop in props:
                prop_property = prop.GetPropertyKeys()
                if prop_property == None: continue
                if prop_property.Get(self._propTypeKey) == self._CuttingPlaneProp:
                    renderer.RemoveViewProp(prop)
                    break

        widget.GetRenderWindow().Render()


    # Updates the position of the cutting plane line in a 2D window
    # If two images are the same orientation, it just reconciles the slices
    def __UpdateSlicePos(self, widget, active_slice, mpr):
        renderer_info = self.__GetRenderer(widget).GetInformation()

        widget_orien = renderer_info.Get(self._rendererMPRKey)
        
        viewer = self.imageViewers[renderer_info.Get(self._rendererNumKey)]
        
        if widget_orien == mpr:
            viewer.SetSlice(active_slice)
        else:
            bounds = list(self.imageViewers[self._masterID].GetImageActor().GetBounds())
            
            renderer = self.__GetRenderer(widget)
            frame_actor = renderer.GetActors().GetLastActor()
            if frame_actor != None:
                renderer.RemoveActor(frame_actor)

            frame_actor = self.__CreateFrame(bounds)
            renderer.AddActor(frame_actor)

            viewer.Render()


    # Cleans up 2D window to remove cutting plane line
    def __CleanUpSlicePos(self, widget):
        renderer = self.__GetRenderer(widget)
        frame_actor = renderer.GetActors().GetLastActor()
        if frame_actor != None:
            renderer.RemoveActor(frame_actor)
        viewer = self.imageViewers[renderer.GetInformation().Get(self._rendererNumKey)]
        viewer.Render()
        

    # Creates a 3D frame around the bounding points
    def __CreateFrame(self, bounds):
        linesPolyData = vtk.vtkPolyData()

        pt0 = [bounds[0], bounds[2], bounds[4]]
        pt1 = [bounds[1], bounds[2], bounds[4]]
        pt2 = [bounds[1], bounds[3], bounds[4]]
        pt3 = [bounds[1], bounds[3], bounds[5]]
        pt4 = [bounds[0], bounds[3], bounds[5]]
        pt5 = [bounds[0], bounds[2], bounds[5]]
        pt6 = [bounds[0], bounds[2], bounds[4]]

        pts = vtk.vtkPoints()
        pts.InsertNextPoint(pt0)
        pts.InsertNextPoint(pt1)
        pts.InsertNextPoint(pt2)
        pts.InsertNextPoint(pt3)
        pts.InsertNextPoint(pt4)
        pts.InsertNextPoint(pt5)
        pts.InsertNextPoint(pt6)

        lines = vtk.vtkCellArray()
        for i in range(5):
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, i)  # the second 0 is the index of Start in linesPolyData's points
            line.GetPointIds().SetId(1, i+1)  # the second 1 is the index of End in linesPolyData's points
            lines.InsertNextCell(line)

        linesPolyData.SetPoints(pts)
        linesPolyData.SetLines(lines)

        ## Setup the visualization pipeline
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(linesPolyData)

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetLineWidth(2)
        actor.GetProperty().SetColor(255,255,255)
        # actor.GetProperty().SetOpacity(0.5)

        return actor


    # Creates a an image actor with scalars from the segmentation
    def __CreateSegmentationActor(self, segmentation, color):
        r, c, d = segmentation.shape

        # Copnvert numpy array to a vtkArray
        segmentation = segmentation.transpose(2,1,0)
        segment_data_array = numpy_support.numpy_to_vtk(segmentation.ravel(), deep=True)
        segment_data_array.SetNumberOfComponents(1)

        # Create the image data
        segment_data = vtk.vtkImageData()
        segment_data.SetDimensions(segmentation.shape)
        segment_data.SetSpacing(self._pixelSpacing)
        segment_data.SetExtent(0, c - 1, 0, r - 1, 0, d - 1)
        segment_data.GetPointData().SetScalars(segment_data_array)

        lookupTable = vtk.vtkLookupTable()
        lookupTable.SetNumberOfTableValues(2)
        lookupTable.SetRange(0.0, 1.0)
        lookupTable.SetTableValue(0, 1.0, 0.0, 0.0, 0.0)  # label 0 is transparent
        lookupTable.SetTableValue(1, color+[1.0])  # label 1 is opaque
        lookupTable.Build()

        mapTransparency = vtk.vtkImageMapToColors()
        mapTransparency.SetLookupTable(lookupTable)
        mapTransparency.PassAlphaToOutputOn()
        mapTransparency.SetOutputFormatToRGBA()
        mapTransparency.SetInputData(segment_data)
        mapTransparency.Update()

        actor = vtk.vtkImageActor()
        actor.GetMapper().SetInputData(mapTransparency.GetOutput())
        actor.AddPosition(0.0001, 0.0001, 0.0001)

        actor.Update()

        return actor


    ##### EVENT CALLBACK FUNCTIONS #####

    # Listener for left mouse button press:
    #   Gets mouse position in current window pixels and passes
    #   them to segmentation functions
    def __on_left_mouse_button_press(self, obj, event):
        if obj.GetShiftKey():
            mouse_pos = obj.GetEventPosition()
            self.SegmentObject(obj, mouse_pos)


    # Listener for slice change event:
    #   This updates the segmentations if any and cutting planes if the caller is the master    
    def __on_slice_change(self, viewer, event):
        # Get the viewer props and renderer
        renderer = viewer.GetRenderer()
        props = renderer.GetViewProps()

        # First consider if the viewer has any additional prop
        if props.GetNumberOfItems() > 1:
            # Only perform update for segmentation props
            for prop in props:
                prop_type = prop.GetPropertyKeys().Get(self._propTypeKey)
                if prop_type == self._SegmentationProp:                
                    prop.SetDisplayExtent(list(viewer.GetImageActor().GetDisplayExtent()))
                    prop.Update()
            viewer.Render()
        
        if renderer.GetInformation().Get(self._rendererNumKey) == self._masterID:
            self.__on_cutting_plane_change(viewer.GetInteractor(), event)


    # Update cutting planes from master widget:
    #   This performs the cutting plane reconciliation between the master widget
    #   and the slaves. For speed, A 3D slave is only rendered after a time interval
    def __on_cutting_plane_change(self, obj, event):
        active_slice = self.imageViewers[self._masterID].GetSlice()
        mpr = self._masterMPR

        for slave in self._slaves:
            renderer_info = self.__GetRenderer(slave).GetInformation()

            if renderer_info.Get(self._rendererTypeKey) == self._imageRenderer:
                self.__UpdateSlicePos(slave, active_slice, mpr)
            elif renderer_info.Get(self._rendererTypeKey) == self._volumeRenderer:
                self.__UpdateCuttingPlanePos(slave, active_slice, mpr)

            if(event == "TimerEvent"):
                self._renderTimeCount += 1
                if self._renderTimeCount == 10:
                    self._renderTimeCount = 0
                    if renderer_info.Get(self._rendererTypeKey) == self._volumeRenderer:
                        slave.GetRenderWindow().Render()
                        obj.DestroyTimer(self._renderTimerID)
        
        if self._renderTimeCount == 0:
            self._renderTimerID = obj.CreateOneShotTimer(1000)


    ##### Image display functions #####


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
    def __SetColor(self, modality):
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
            volume_color.AddRGBPoint(99, 0.0, 0.0, 0.0)
            volume_color.AddRGBPoint(100, 0.94, 0.8, 0.7)
            volume_color.AddRGBPoint(600, 0.74, 0.6, 0.5)
            volume_color.AddRGBPoint(601, 0.0, 0.0, 0.0)

            volume_color.AddRGBPoint(599, 0.0, 0.0, 0.0)
            volume_color.AddRGBPoint(600, 0.7, 0.7, 0.7)
            volume_color.AddRGBPoint(2500, 0.9, 0.7, 0.9)
            volume_color.AddRGBPoint(2501, 0.0, 0.0, 0.0)
        
        volume_color.AddRGBPoint(4998, 0.0, 0.0, 0.0)
        volume_color.AddRGBPoint(4999, 1.0, 0.0, 0.0)
        volume_color.AddRGBPoint(5001, 1.0, 0.0, 0.0)
        volume_color.AddRGBPoint(5002, 0.0, 0.0, 0.0)
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
            volume_scalar_opacity.AddPoint(0, 0.00)
            volume_scalar_opacity.AddPoint(2550, 0.00)
            for opt in opts:
                if opt == "ALL":
                    self.__AddOpacityPoints([50,2500], volume_scalar_opacity)
                    break
                # if opt == "BONE":
                #     self.__AddOpacityPoints([275, 3000], volume_scalar_opacity)
                if opt == "SOFT":
                    self.__AddOpacityPoints([900, 2500], volume_scalar_opacity)
                if opt == "SKIN":
                    self.__AddOpacityPoints([100, 600], volume_scalar_opacity)
                # if opt == "MUSCLE":
                #     self.__AddOpacityPoints([20, 40], volume_scalar_opacity)
                # if opt == "FAT":
                #     self.__AddOpacityPoints([-70, -30], volume_scalar_opacity)
        volume_scalar_opacity.AddPoint(4998, 0.0)
        volume_scalar_opacity.AddPoint(4999, 1.0)
        volume_scalar_opacity.AddPoint(5001, 1.0)
        volume_scalar_opacity.AddPoint(5002, 0.0)
        return volume_scalar_opacity

    # Adds opacity points to the transfer funtion
    def __AddOpacityPoints(self, limits, volume_scalar_opacity):
        transparency = self._3DTransparency
        volume_scalar_opacity.AddPoint(limits[0] - 1, 0.00)
        volume_scalar_opacity.AddPoint(limits[0], transparency)
        volume_scalar_opacity.AddPoint(limits[1], transparency)
        volume_scalar_opacity.AddPoint(limits[1] + 1, 0.00)

    # Removes opacity points to the transfer funtions
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


