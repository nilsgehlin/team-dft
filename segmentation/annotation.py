from vtk import vtkAnnotation, vtkInformation, vtkInformationIterator
from vtk.util import keys


############################
##### Annotation Class #####
############################
class annotation(vtkInformation):
    ##### Class Variables #####
    _annotInstance = None

    _dataTypeName = "ANNOTATION"

    _locationKey = None

    ##### General class functions #####

    def __init__(self):
        super().__init__()

        self._annotInstance = vtkAnnotation()
        self._locationKey = keys.MakeKey(keys.IntegerVectorKey, "COORDINATES", "annotation")

        self.Set(self._annotInstance.DATA_TYPE_NAME(), self._dataTypeName)
        self.Enable()
        self.Show()
    
    ##### Public class functions #####

    # Returns the text set for the annotation
    def GetText(self):
        return self.Get(self._annotInstance.LABEL())

    # Sets the text on the annotation object. It completely replaces
    # any previous text set on the annotation
    def SetText(self, text):
        self.Set(self._annotInstance.LABEL(), text)

    # Returns the coordinates for the annotation
    def GetLocation(self):
        return self.Get(self._locationKey)

    # Sets the opacity on the annotation object. 
    def SetLocation(self, x,y,slice):
        arr = [int(x), int(y), int(slice)]
        self.Set(self._locationKey, arr, 3)

    # Returns the color set for the annotation
    def GetColor(self):
        return self.Get(self._annotInstance.COLOR())

    # Sets the color on the annotation object.
    def SetColor(self, color):
        self.Set(self._annotInstance.COLOR(), color)

    # Returns the opacity set for the annotation
    def GetOpacity(self):
        return self.Get(self._annotInstance.OPCAITY())

    # Sets the opacity on the annotation object. 
    def SetOpacity(self, opacity):
        self.Set(self._annotInstance.OPACITY(), opacity)

    # Enables the annotation
    def Enable(self):
        self.Set(self._annotInstance.ENABLE(), 1)

    # Disables the annotation
    def Disable(self):
        self.Set(self._annotInstance.ENABLE(), 0)

    # Whether or not annotation is enabled or disabled
    def isActive(self):
        return self.Get(self._annotInstance.ENABLE())

    # Activates the annotation show flag
    def Show(self):
        self.Set(self._annotInstance.HIDE(), 1)

    # Deactivates the annotation show flag
    def Hide(self):
        self.Set(self._annotInstance.HIDE(), 0)

    # Whether or not annotation is shown or hidden
    def isVisible(self, text):
        return self.Get(self._annotInstance.HIDE())


##################################
##### Annotation Store Class #####
##################################
class annotationStore(vtkInformation):
    ##### Class Variables #####
    _dataTypeName = "ANNOTATION STORE"

    ##### General class functions #####

    def __init__(self):
        super().__init__()
        #self.Set(vtkAnnotation.DATA_TYPE_NAME(), self._dataTypeName) #Removed for key numbers

    ##### Public class functions #####

    # Stores the annotation and returns the key to access it
    def StoreAnnotation(self, annot):
        key = keys.MakeKey(keys.InformationKey, "ANNOTATION", "annotationStore")
        self.Set(key, annot)
        return key

    # Removes the annotation from the map
    def RemoveAnnotation(self, key):
        self.Remove(key)

    # Returns the annotation for the given key
    def GetAnnotation(self, key):
        if self.Has(key):
            return self.Get(key)            
        else:
            return None

    # Returns the number of annotations stored
    def GetNumberOfAnnotations(self):
        return self.GetNumberOfKeys()            
        

    # Validates that the provided key is stored in the annotation store
    def isStoredValidID(self, key):
        if self.Has(key):
            return True
        else:
            return False


###########################################
##### Annotation Store Iterator Class #####
###########################################
class annotationStoreIterator(vtkInformationIterator):
    ##### General class functions #####

    # Initiation options
    def __init__(self, store = None):
        super().__init__()
        if not store is None:
            self.SetAnnotationStore(store)

    # Iterators
    def __iter__(self):
        self.GoToFirstKey()
        return self

    def __next__(self):
        if self.IsDoneStoreTraversal():
            raise StopIteration
        else:
            key = self.GetCurrentKey()
            self.GoToNextKey()
            return key

    ##### Public class functions #####

    # Sets the annotation object to iterate on
    def SetAnnotationStore(self, annot):
        self.SetInformation(annot)

    # Moves the iterator to the first annotation key
    # This is NOT necesarrily the firs stored annotation
    def GoToFirstKey(self):
        self.GoToFirstItem()

    # Moves the iterator to the next annotation key
    def GoToNextKey(self):
        self.GoToNextItem()

    # Starts annotation store traversal
    def StartStoreTraversal(self):
        return self.InitTraversal()

    # Test whether the iterator is still traversing
    def IsDoneStoreTraversal(self):
        return self.IsDoneWithTraversal()

    # Returns the current annotation key in the traversal
    def GetCurrentKey(self):
        return super().GetCurrentKey()          
    
    # Returns the annotation store being traversed
    def GetAnnotationStore(self):
        return self.GetInformation()


#####
##### Self run example to test the class #####
#####
if __name__ == "__main__":
    ## Create annotation instance
    annot = annotation()

    # Set annotation attributes
    annot.SetText("first annotation")
    annot.SetLocation(100,200,4)

    # Retreive stored text
    text = annot.GetText()
    print("The annotation text is:", text)

    # Modify annotation text
    annot.SetText("first annotation modification")

    # Retreive stored text
    text = annot.GetText()
    coord = annot.GetLocation()
    print("The annotation text now is:", text)
    print("The annotation location is:", coord)

    ## Create annotation store
    annotStore = annotationStore()
    
    # Store the first annotation and keep the key
    annotK = annotStore.StoreAnnotation(annot)

    # Create second annotation and store it too
    annot2 = annotation()
    annot2.SetText("second annotation")
    annot2K = annotStore.StoreAnnotation(annot2)

    # Retrieve stored
    print("First text is:", annotStore.GetAnnotation(annotK).GetText())
    print("Second text is:", annotStore.GetAnnotation(annot2K).GetText())

    ## 100 annotation storage tester
    store = annotationStore()

    # Create 100 annotations
    for i in range(100):
        a = annotation()
        a.SetText("annotation " + str(i))
        store.StoreAnnotation(a)
    
    print(str(store.GetNumberOfAnnotations()) + " annotations stored")

    # Print annotations using the annotation iterator
    it = annotationStoreIterator(store)
    for a in it:
        print(store.GetAnnotation(a).GetText())


        
