import vtk
from vtk.util import keys, numpy_support
from imageReader.ImageReader import ImageReader
from segmentation.Segmentation import Segmentation
from annotation.Annotation import Annotation
from measurement.Measurement import Measurement

# TODO:
#1. Way to identify if segmentation in already in the renderer
#4. Improve opacity of the segmentation in the 3D viewer
#5. Define color for measurement line

class VisualizationEngine(object):
    ##### Class Variables #####
    
    # Reader
    imageReader = None
    reader = None
    _pixelSpacing = None

    # Annotations
    activeAnnotation = None

    # Renderer Variables
    _imageRenderer = "IMAGE_RENDERER"
    _volumeRenderer = "VOLUME_RENDERER"
    _rendererTypeKey = None
    _rendererNumKey = None
    _rendererMPRKey = None
    _rendererObserverKey = None

    # Prop Variables
    _SegmentationProp = "SEGMENTATION_PROP"
    _MeasurementProp = "MEASUREMENT_PROP"
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
    _sliceFrameColor = [1,0,0]

    # Slave Render Timer
    _renderTimerID = 0
    _renderTimeCount = 0

    # 2d image viewers array
    imageViewers = []

    # 3D Properties
    _3DTransparency = 0.2
    _3DTissue = ["ALL"]

    # Directory
    _dir = None


    ##### General class functions #####

    # Initializer for the image engine, takes the directory of the files as argument
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

    
    ##################################
    ##### Public class functions #####
    ##################################


    # Manually changes the read DICOM information into the engine
    # AVOID CALLING IF WINDOWS HAVE BEEN SET UP
    #   Parameters:
    #       1. Directory, containing DICOM files
    def SetDirectory(self, dir):
        self._dir = dir
        image_reader = ImageReader(dir)
        self.reader = image_reader.readImages()
        self._pixelSpacing = image_reader.getPixelSpacing()
        self.imageReader = image_reader


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
        
        volume_property = self.__SetVolumeProperties(self._3DTissue)
    
        # The vtkVolume is a vtkProp3D (like a vtkActor) and controls the position
        # and orientation of the volume in world coordinates.
        volume = vtk.vtkVolume()
        volume.SetMapper(volume_mapper)
        volume.SetProperty(volume_property)

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
    #       2. List of Tissues i.e. ALL, BONE, SOFT, MUSCLE or FAT
    #   Notes:
    #       -If only passing one tissue, make sure to put it in a list
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


    # Sets the attributes of the cutting plane on a 3D window
    # Parameters:
    #       1. showSlice - This determines if the image of the active slice on the
    #               master window is also shown on the 3d volume 
    #       2. crop3D - This determines if the 3D volume is cropped to show the active
    #               position on the master window
    def ConfigureVolumeCuttingPlane(self, showSlice = True, crop3D = True):
        self._showActiveSlice = showSlice
        self._crop3D = crop3D


    # Links scrolling of master window 'masterWidget' to slave windows in 'args'
    # ONLY a 2D image window can be a master.
    #   Parameters: 
    #       1. vtkWidget - Master
    #       2,3,4... vtkWidgets - Slaves
    #   Notes:
    #       -Provide each slave as its own arguments, NOT as an array
    #       -There can be only one master window for any engine instance. You have
    #           to unlink slaves before creating a new set of links.
    def LinkWindows(self, masterWidget, *args):
        if self._masterID == None:
            master_renderer_info = self.__GetRenderer(masterWidget).GetInformation()
            self._masterID = master_renderer_info.Get(self._rendererNumKey)
            self._masterMPR = master_renderer_info.Get(self._rendererMPRKey)
            if master_renderer_info.Get(self._rendererTypeKey) == self._imageRenderer:
                self._slaves = []
                for arg in args:
                    self._slaves.append(arg)
                ob_id = masterWidget.AddObserver(vtk.vtkCommand.TimerEvent, self.__on_cutting_plane_change,2)
                master_renderer_info.Set(self._rendererObserverKey, ob_id)
                self.__ShowFrameOnMaster(masterWidget)
                self.__on_cutting_plane_change(masterWidget, "None")


    # Safely unlinks all window scrolling from the master window
    #   Parameters: 
    #       1. vtkWidget - Master
    #   Notes:
    #       -If a wrong master window is provided nothing happens
    def UnlinkWindows(self, masterWidget):
        master_renderer_info = self.__GetRenderer(masterWidget).GetInformation()
        if master_renderer_info.Get(self._rendererNumKey) == self._masterID: 
            self.__CleanUpSlicePos(masterWidget)
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
    #       -Will not segment if widget passed is a 3D window
    #       -Still have to fix bug where some times segmentation does not show up immediately
    def SegmentObject(self, widget, mouse_pos):
        renderer = widget.FindPokedRenderer(mouse_pos[0], mouse_pos[1])
        renderer_info = renderer.GetInformation()
        
        if renderer_info.Get(self._rendererTypeKey) == self._imageRenderer:

            # Get picked coordinate and convert viewer coordinate into pixel value coordinate
            widget.GetPicker().Pick(mouse_pos[0], mouse_pos[1], 0, renderer)
            clicked_coordinate = list(widget.GetPicker().GetPickPosition())
            for i in range(3):
                clicked_coordinate[i] = clicked_coordinate[i] / self._pixelSpacing[i]
            clicked_coordinate = tuple(clicked_coordinate)

            # Returns NONE if the clicked coordinate is out of bounds
            if any(coord < 0 for coord in clicked_coordinate) == True:
                return
            if any(not coord.is_integer() for coord in clicked_coordinate):
                return

            # Create the segmentation
            segmentation = self.__CreateSegmentation(clicked_coordinate)
            segment_array = segmentation.GetScalars()
            segment_color = segmentation.GetColor()
            [segment_image_actor,_] = self.__CreateSegmentationActor(segment_array, segment_color)

            renderer.AddActor(segment_image_actor)
            viewer = self.imageViewers[renderer_info.Get(self._rendererNumKey)]
            self.__on_slice_change(viewer, "None")

            # Make segment as annotation
            segment_annot = Annotation()
            segment_annot.SetCoordinate(clicked_coordinate)
            segment_annot.SetVtkColor(segment_color)
            segment_annot.SetSegmentFlag(True, segment_array)
   
            return segment_annot


    # Displays the segmentations in the provided keys in the vtkWidget
    #   Parameters:
    #       1. vtkWidget - the target window
    #       2. annots - an array of segmentation annotations
    #   Notes:
    #       -Volume widgets show in a very light way
    def AddSegmentations(self, widget, annots):
        renderer = self.__GetRenderer(widget)
        renderer_info = renderer.GetInformation()

        for annot in annots:
            if(annot.isSegment()):
                segment_array = annot.GetSegmentData()
                segment_color = annot.GetVtkColor()

                # Create segmentation array if loading from file
                if segment_array is None:
                    segment_array = self.__CreateSegmentation(annot.GetCoordinate()).GetScalars()
                    annot.AddSegmentData(segment_array)
                
                [segment_image_actor, segment_image_data] = self.__CreateSegmentationActor(segment_array, segment_color)

                if renderer_info.Get(self._rendererTypeKey) == self._imageRenderer:
                    renderer.AddActor(segment_image_actor)
                    viewer = self.imageViewers[renderer_info.Get(self._rendererNumKey)]
                    viewer.UpdateDisplayExtent()           
        
                elif renderer_info.Get(self._rendererTypeKey) == self._volumeRenderer:
                    volume_mapper = vtk.vtkSmartVolumeMapper()
                    volume_mapper.SetInputData(segment_image_data)        
                    volume_mapper.SetBlendModeToComposite()

                    volume_property = self.__SetSegementPropety(segment_color)

                    volume = vtk.vtkVolume()
                    volume.SetMapper(volume_mapper)
                    volume.SetProperty(volume_property)

                    renderer.AddViewProp(volume)
        
        widget.GetRenderWindow().Render()

    
    # Displays the annotations' measurements in the provided the vtkWidget
    #   Parameters:
    #       1. vtkWidget - the target window
    #       2. annots - an array of segmentation annotations
    #   Notes:
    #       -It assumes the segmentaion is already performed
    def AddMeasurements(self, widget, annots):
        renderer = self.__GetRenderer(widget)
        renderer_info = renderer.GetInformation()

        for annot in annots:
            if(annot.isSegment()):
                segment_array = annot.GetSegmentData()
                segment_color = annot.GetVtkColor()

                # Create segmentation array if loading from file
                if segment_array is None:
                    segment_array = self.__CreateSegmentation(annot.GetCoordinate()).GetScalars()
                    annot.AddSegmentData(segment_array)
                
                measurement = Measurement(segment_array, self._pixelSpacing)

                if renderer_info.Get(self._rendererTypeKey) == self._imageRenderer:
                    viewer = self.imageViewers[renderer_info.Get(self._rendererNumKey)]
                    measurement_info = measurement.GetInfo(viewer.GetSliceOrientation())
                    measurement_actor = self.__CreateMeasurementLine(measurement_info['startPoint'], measurement_info['endPoint'], [1,0,0])
                    renderer.AddActor(measurement_actor)            
                    self.__on_slice_change(viewer, "None")

    
    # Removes all the segmentations in the window
    #   Parameters:
    #       1. vtkWidget - the target window
    #   Notes:
    #       -Measurements should be removed separately by calling RemoveMeasurements
    def RemoveSegmentations(self, widget):
        renderer = self.__GetRenderer(widget)
        
        props = renderer.GetViewProps()
        for prop in props:
            prop_property = prop.GetPropertyKeys()
            if prop_property == None: continue
            if prop_property.Get(self._propTypeKey) == self._SegmentationProp:
                renderer.RemoveViewProp(prop)

        widget.GetRenderWindow().Render()


    # Removes all the measurements in the window
    #   Parameters:
    #       1. vtkWidget - the target window
    #   Notes:
    #       -Segmentations should be removed separately by calling RemoveSegmentations
    def RemoveMeasurements(self, widget):
        renderer = self.__GetRenderer(widget)
        
        props = renderer.GetViewProps()
        for prop in props:
            prop_property = prop.GetPropertyKeys()
            if prop_property == None: continue
            if prop_property.Get(self._propTypeKey) == self._MeasurementProp:
                renderer.RemoveViewProp(prop)

        widget.GetRenderWindow().Render()

    
    # Removes all the annotations in the window i.e segmentations and measurements
    #   Parameters:
    #       1. vtkWidget - the target window
    def RemoveAllAnnotations(self, widget):
        renderer = self.__GetRenderer(widget)
        
        props = renderer.GetViewProps()
        for prop in props:
            prop_property = prop.GetPropertyKeys()
            if prop_property == None: continue
            if prop_property.Get(self._propTypeKey) == self._SegmentationProp:
                renderer.RemoveViewProp(prop)
                continue
            if prop_property.Get(self._propTypeKey) == self._MeasurementProp:
                renderer.RemoveViewProp(prop)

        widget.GetRenderWindow().Render()
        

    ###################################
    ##### Private class functions #####
    ###################################


    ##### GENERAL HELPER FUNCTIONS #####
    
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

    
    ##### CUTTING PLANE FUNCTIONS #####

    # Adds the frame around the master widget to show linking is active
    def __ShowFrameOnMaster(self, widget):    
        viewer = self.imageViewers[self._masterID]
        bounds = list(viewer.GetImageActor().GetBounds())
        frame_actor = self.__CreateFrame(bounds)
        frame_actor_info = vtk.vtkInformation()
        frame_actor_info.Set(self._propTypeKey, self._CuttingPlaneProp)
        frame_actor.SetPropertyKeys(frame_actor_info)
        
        renderer = self.__GetRenderer(widget)
        renderer.AddActor(frame_actor)
        
        viewer.Render()


    # Updates the position of the cutting plane in a 3D window
    def __UpdateCuttingPlanePos(self, widget, active_slice, mpr):
        renderer = self.__GetRenderer(widget)
        
        if (self._showActiveSlice):
            self.__AddSliceToVolume(renderer)

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
    def __AddSliceToVolume(self, renderer):
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

        self.__AddFrameToSlice(renderer, viewer_actor.GetBounds())
    

    # Adds a frame to the active slice in the 3D renderer
    def __AddFrameToSlice(self, renderer, bounds):
        actors = renderer.GetActors()
        for actor in actors:
            actor_property = actor.GetPropertyKeys()
            if actor_property == None: continue
            if actor_property.Get(self._propTypeKey) == self._CuttingPlaneProp:
                renderer.RemoveActor(actor)
                break
        frame_actor = self.__CreateFrame(list(bounds))
        frame_actor_info = vtk.vtkInformation()
        frame_actor_info.Set(self._propTypeKey, self._CuttingPlaneProp)
        frame_actor.SetPropertyKeys(frame_actor_info)
        renderer.AddActor(frame_actor)

    
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
            renderer = self.__GetRenderer(widget)
            actors = renderer.GetActors()
            for actor in actors:
                actor_property = actor.GetPropertyKeys()
                if actor_property == None: continue
                if actor_property.Get(self._propTypeKey) == self._CuttingPlaneProp:
                    renderer.RemoveActor(actor)
                    break

            bounds = list(self.imageViewers[self._masterID].GetImageActor().GetBounds())   
            frame_actor = self.__CreateFrame(bounds)
            frame_actor_info = vtk.vtkInformation()
            frame_actor_info.Set(self._propTypeKey, self._CuttingPlaneProp)
            frame_actor.SetPropertyKeys(frame_actor_info)
            renderer.AddActor(frame_actor)

            viewer.UpdateDisplayExtent()
            viewer.Render()


    # Cleans up 2D window to remove cutting plane line
    def __CleanUpSlicePos(self, widget):
        renderer = self.__GetRenderer(widget)
        actors = renderer.GetActors()
        for actor in actors:
            actor_property = actor.GetPropertyKeys()
            if actor_property == None: continue
            if actor_property.Get(self._propTypeKey) == self._CuttingPlaneProp:
                renderer.RemoveActor(actor)
                break
        viewer = self.imageViewers[renderer.GetInformation().Get(self._rendererNumKey)]
        viewer.Render()

    
    ##### SEGMENTATION AND MEASUREMENT FUNCTIONS #####

    # Creates a segmentation object from the clicked coordinate
    def __CreateSegmentation(self, coordinate, *color):
        image_data = self.reader.GetOutput()

        # Read the image data from vtk to numpy array and
        # reorganises the dimensions and scales the data
        cols, rows, slc = image_data.GetDimensions()
        volume = numpy_support.vtk_to_numpy(image_data.GetPointData().GetScalars())
        volume = volume.reshape(slc, rows, cols)
        volume = volume.transpose(2, 1, 0)

        # Create the segmentation
        segmentation = Segmentation(coordinate, volume, segmentation_threshold=0.2, verbose=True)
        return segmentation
        

    ##### ACTOR CREATION FUNCTIONS #####
    
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
        actor.GetProperty().SetColor(self._sliceFrameColor)

        return actor

    
    # Creates a measurement line
    def __CreateMeasurementLine(self, startPoint, endPoint, color):
        linesPolyData = vtk.vtkPolyData()

        pt0 = startPoint
        for i in range(3):
            pt0[i] = pt0[i] * self._pixelSpacing[i]

        pt1 = endPoint
        for i in range(3):
            pt1[i] = pt1[i] * self._pixelSpacing[i]

        pts = vtk.vtkPoints()
        pts.InsertNextPoint(pt0)
        pts.InsertNextPoint(pt1)

        lines = vtk.vtkCellArray()
        for i in range(1):
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
        actor.GetProperty().SetColor(color)

        actor_info = vtk.vtkInformation()
        actor_info.Set(self._propTypeKey, self._MeasurementProp)
        actor.SetPropertyKeys(actor_info)

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

        volume_segment_data = vtk.vtkImageData()
        volume_segment_data.DeepCopy(segment_data)

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
        actor.Update()

        actor_info = vtk.vtkInformation()
        actor_info.Set(self._propTypeKey, self._SegmentationProp)
        actor.SetPropertyKeys(actor_info)

        return [actor, volume_segment_data]


    ##### EVENT CALLBACK FUNCTIONS #####

    # Listener for left mouse button press:
    #   Gets mouse position in current window pixels and passes
    #   them to segmentation functions
    def __on_left_mouse_button_press(self, obj, event):
        if obj.GetShiftKey():
            mouse_pos = obj.GetEventPosition()
            self.activeAnnotation = self.SegmentObject(obj, mouse_pos)
            self.AddMeasurements(obj, [self.activeAnnotation])


    # Listener for slice change event:
    #   This updates the segmentations if any and cutting planes if the caller is the master    
    def __on_slice_change(self, viewer, event):
        # Get the viewer props and renderer
        renderer = viewer.GetRenderer()
        props = renderer.GetViewProps()

        # First consider if the viewer has any additional prop
        if props.GetNumberOfItems() > 1:
            # Perform necessary update to props
            for prop in props:
                prop_property = prop.GetPropertyKeys()
                if prop_property == None: continue
                # Update segmentation prop
                if prop_property.Get(self._propTypeKey) == self._SegmentationProp:                
                    prop.SetDisplayExtent(list(viewer.GetImageActor().GetDisplayExtent()))
                    prop.Update()
                    continue
                # Update measurement prop
                if prop_property.Get(self._propTypeKey) == self._MeasurementProp:
                    plane_id = viewer.GetSliceOrientation()
                    image_extent = viewer.GetImageActor().GetDisplayExtent()[plane_id*2]
                    prop_extent = prop.GetBounds()[plane_id*2] / self._pixelSpacing[plane_id]
                    if image_extent == prop_extent:
                        prop.VisibilityOn()
                    else:
                        prop.VisibilityOff()

            viewer.Render()
        
        if renderer.GetInformation().Get(self._rendererNumKey) == self._masterID:
            self.__on_cutting_plane_change(viewer.GetInteractor(), event)


    # Update cutting planes from master widget:
    #   This performs the cutting plane reconciliation between the master widget
    #   and the slaves. For speed, A 3D slave is only rendered after a time interval
    def __on_cutting_plane_change(self, obj, event):
        active_slice = self.imageViewers[self._masterID].GetSlice()
        mpr = self._masterMPR

        if self._renderTimeCount == 0:
            self._renderTimerID = obj.CreateOneShotTimer(10)

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
                        slave.GetRenderWindow().Render()
                        obj.DestroyTimer(self._renderTimerID)


    ##### VOLUME DISPLAY FUNCTIONS #####


    def __SetSegementPropety(self, color):
        # Color
        volume_property = self.__SetVolumeProperties(self._3DTissue)
        volume_color = volume_property.GetRGBTransferFunction()
        volume_color.AddRGBPoint(0, 0.0, 0.0, 0.0)
        volume_color.AddRGBPoint(1, color[0], color[1], color[2])
        volume_color.AddRGBPoint(2, color[0], color[1], color[2])
        volume_color.AddRGBPoint(3, 0.0, 0.0, 0.0)

        volume_scalar_opacity = volume_property.GetScalarOpacity()
        volume_scalar_opacity.AddPoint(0, 0.00)
        volume_scalar_opacity.AddPoint(0.5, 1.0)
        volume_scalar_opacity.AddPoint(1.5, 1.0)
        volume_scalar_opacity.AddPoint(2, 0.00)
        
        return volume_property


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
    def __SetVolumeProperties(self, tissue):
        modality = self.imageReader.getModality()

        volume_color = self.__SetColor(modality)
        volume_scalar_opacity = self.__SetScalarOpacity(modality, tissue)
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


