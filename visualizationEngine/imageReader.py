import os
from vtk import vtkDICOMImageReader, vtkTIFFReader, vtkStringArray

#TODO:
#1. Implement reading meta data
#   - Update reading modality on readDicom function

class imageReader():
    ##### Class Variables #####
    _directory = None
    _reader = None
    _modality = None

    ##### General class functions #####


    # Initializer for imageReader, takes one optional parameter
    # for the directory (Throws an error if more than 1).
    def __init__(self, *args):
        if len(args) > 0:
            self._directory = args[0]
        if len(args) > 1:
            raise NameError("More than one argument for !")
        
    
    ##### Public class functions #####


    # Sets the image directory to be read
    def setImageDirectory(self, dir):
        self._directory = dir


    # Reads a directory of TIFF images and returns an
    # image reader object
    def readTiff(self):
        if self._directory is None:
            raise NameError("Please set image directory")

        # Accumulate file names
        filenames = vtkStringArray()
        for filename in enumerate(os.listdir(self._directory)):
            filenames.InsertNextValue(os.path.join(self._directory, filename))
        # Create reader object with filenames
        reader = vtkTIFFReader()
        reader.SetFileNames(filenames)
        reader.Update()

        self._modality = None
        self.reader = reader
        return self._reader


    # Reads a directory of DICOM images and returns an
    # image reader object
    def readDicom(self):
        if self._directory is None:
            raise NameError("Please set image directory")

        # Create reader object ans set directory name
        reader = vtkDICOMImageReader()
        reader.SetDirectoryName(self._directory)
        # Set other settings and update
        reader.SetDataByteOrderToLittleEndian()
        data_spacing = (1, 1, 2)
        reader.SetDataSpacing(data_spacing[0], data_spacing[1], data_spacing[2])
        reader.Update()

        self._reader = reader
        return self._reader


    # Returns the image reader object
    def getReader(self):
        if self._reader is None:
            raise NameError("Please read a DICOM or TIFF image directory")
        return self._reader

    # Returns the image reader object
    def getModality(self):
        if self._modality is None:
            raise NameError("Please read a DICOM image for modality")
        return self._modality


    

