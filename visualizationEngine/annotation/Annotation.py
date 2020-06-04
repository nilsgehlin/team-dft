from vtk import vtkAnnotation, vtkInformation, vtkInformationIterator
from vtk.util import keys
import uuid


############################
##### Annotation Class #####
############################
class Annotation(vtkInformation):
    ##### Class Variables #####
    
    # vtkCompatibility
    _annotInstance = None
    _dataTypeName = "ANNOTATION"
    _locationKey = None
    _vtkKey = None

    # Optimization
    _segmentData = None
    _measurement = None
    _imageActor = None
    _volume = None

    # Clinical
    _anatomicalLocation = None
    _color = None
    _physicianNote = None
    _webLink = None

    ##### General class functions #####

    def __init__(self):
        super().__init__()
        
        self._annotInstance = vtkAnnotation()
        self._locationKey = keys.MakeKey(keys.IntegerVectorKey, "COORDINATES", "Annotation")
        self._vtkKey = keys.MakeKey(keys.InformationKey, "ANNOTATION", "Annotation")

        self.annot_id = uuid.uuid4().hex

        self.Set(self._annotInstance.DATA_TYPE_NAME(), self._dataTypeName)
        self.SetSegmentFlag(False)
        self.reviewed = False
    

    ##### Public class functions #####


    # Returns the ID for the annotation
    def GetID(self):
        return self.annot_id

    # Returns the text set for the annotation
    def GetFinding(self):
        return self.Get(self._annotInstance.LABEL())

    # Sets the text on the annotation object. It completely replaces
    # any previous text set on the annotation
    def SetFinding(self, text):
        self.Set(self._annotInstance.LABEL(), text)

    # Returns the anatomical location of the annotation
    def GetLocation(self):
        return self._anatomicalLocation

    # Sets the opacity on the annotation object. 
    def SetLocation(self, loc):
        self._anatomicalLocation = loc

    # Returns the coordinates for the annotation
    def GetCoordinate(self):
        return self.Get(self._locationKey)

    # Sets the opacity on the annotation object. 
    def SetCoordinate(self, loc):
        if loc is not None:
            loc = list(map(int, loc))
            self.Set(self._locationKey, loc, 3)

    # Returns the color set for the annotation, from 0-255
    def GetColor(self):
        return tuple(self._color)

    # Sets the color on the annotation object, from 0-255
    # Converts the color to vtk color as well
    def SetColor(self, color):
        self._color = color
        vtk_color = [round(float((x/255)*1.0),1) for x in color]
        self.SetVtkColor(vtk_color)

    # Returns the color set for the annotation, from 0.0-1.0
    def GetVtkColor(self):
        return list(self.Get(self._annotInstance.COLOR()))

    # Sets the color on the annotation object, from 0.0-1.0
    # Converts the color to normal 255 RGB as well
    def SetVtkColor(self, color):
        self.Set(self._annotInstance.COLOR(), color, 3)
        self._color = [int((x/1.0)*255) for x in color]

    # Returns the opacity set for the annotation
    def GetOpacity(self):
        return self.Get(self._annotInstance.OPACITY())

    # Sets the opacity on the annotation object. 
    def SetOpacity(self, opacity):
        self.Set(self._annotInstance.OPACITY(), opacity)

    # Add the physician note to the annotation
    def AddNote(self, note):
        self._physicianNote = note

    # Returns the physician note on the annotation
    def GetNote(self):
        return self._physicianNote

    # Whether or not annotation has a physician note
    def HasNote(self):
        if self._physicianNote is not None: return True
        return False

    # Adds a web link to the annotation
    def AddWebLink(self, link):
        self._webLink = link

    # Returns the weblink on the annotation
    def GetWebLink(self):
        return self._webLink

    # Whether or not annotation has a web link attached to it
    def HasWebLink(self):
        if self._webLink is not None: return True
        return False

    # Flag to know that the annotation is a segmentation
    def SetSegmentFlag(self, state, *seg_data):
        self.Set(self._annotInstance.ICON_INDEX(), int(state))
        if len(seg_data) > 0:
            self._segmentData = seg_data[0]

    # Add segmentation array data to annotation
    def AddSegmentData(self, seg_data):
        self._segmentData = seg_data

    # Get the segmentation data array
    def GetSegmentData(self):
        return self._segmentData

    # Check whether this annotation is a segmentation or not
    def isSegment(self):
        return bool(self.Get(self._annotInstance.ICON_INDEX()))

    # Add measurement to annotation, only for speed optimization
    def AddMeasurement(self, measurement):
        self._measurement = measurement

    # Return the measurement
    def GetMeasurement(self):
        return self._measurement

    # Add volume actor to anotation, only for speed optimization
    def AddVolume(self, volume):
        self._volume = volume

    # Return the volume actor
    def GetVolume(self):
        return self._volume

    # Get this annotation's key for engine functionality
    def GetVtkKey(self):
        return self._vtkKey

    # Serializes the annotation to Json
    def toJson(self):
        json = dict(id =  self.annot_id, 
                     location = self.GetLocation(),
                     finding = self.GetFinding(),
                     color = self.GetColor(),
                     coordinate = self.GetCoordinate(),
                     isSegment = self.isSegment(),
                     note = self.GetNote(),
                     webLink = self.GetWebLink()
                     )
        return json

    # Deserializes an annotation from Json
    @staticmethod
    def fromJson(data):
        annot = Annotation()
        annot.SetLocation(data['location'])
        annot.SetFinding(data['finding']) 
        annot.SetColor(data['color'])
        annot.SetCoordinate(data['coordinate'])
        annot.SetSegmentFlag(data['isSegment'])
        annot.reviewed = True
        annot.AddNote(data['note'])
        annot.AddWebLink(data['webLink'])
        return annot

    # String conversion
    def __str__(self):
        strn = dict(id =  self.annot_id, 
                    location = self.GetLocation(),
                    finding = self.GetFinding(),
                    color = self.GetColor(),
                    coordinate = self.GetCoordinate(),
                    isSegment = self.isSegment()
                    )
        return str(strn)
        

##################################
##### Annotation List Class #####
##################################
class AnnotationList(list):

    ##### General class functions #####

    def __init__(self):
        super().__init__()

    ##### Public class functions #####

    # Stores the annotation and returns the key to access it
    def AddAnnotation(self, annot):
        self.append(annot)

    # Removes the annotation from the map
    def RemoveAnnotation(self, annot):
        self.remove(annot)

    # Returns the annotation for the given ID
    def GetAnnotationFromID(self, ID):
        for annot in self:
            if ID == annot.GetID(): 
                return annot              

    # Returns the annotation for the given vtk key
    def GetAnnotationFromKey(self, key):
        for annot in self:
            if key == annot.GetVtkKey(): 
                return annot              

    # Returns all the segmentation annotations
    def GetAllSegmentations(self):
        arr = []
        for annot in self:
            if annot.isSegment():
                arr.append(annot)
        return arr

    # Returns the number of annotations stored
    def GetNumberOfAnnotations(self):
        return len(self)
        
