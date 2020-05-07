import os
import pydicom
from vtk import vtkDICOMImageReader, vtkTIFFReader, vtkStringArray
import json
import pydicom

#TODO:

class imageReader():
    ##### Class Variables #####
    _directory = None
    _reader = None
    _metaData = None

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
        for filename in os.listdir(self._directory):
            filenames.InsertNextValue(os.path.join(self._directory, filename))

        with open(os.path.join(self._directory, "meta_data.json")) as meta_data_file:
            self._metaData = json.load(meta_data_file)



        # Create reader object with filenames
        reader = vtkTIFFReader()
        reader.SetFileNames(filenames)
        reader.Update()
        self._reader = reader
        return self._reader


    # Reads a directory of DICOM images and returns an
    # image reader object
    def readDicom(self):
        if self._directory is None:
            raise NameError("Please set image directory")

        # Get image metadata
        first_file_name = os.listdir(self._directory)[0]
        first_file_loc = os.path.join(self._directory, first_file_name)
        self._metaData = pydicom.filereader.dcmread(first_file_loc)
        # Create reader object and set directory name
        reader = vtkDICOMImageReader()
        reader.SetDirectoryName(self._directory)
        # Set other settings and update
        reader.SetDataByteOrderToLittleEndian()
        # data_spacing = (1, 1, 2)
        # reader.SetDataSpacing(data_spacing[0], data_spacing[1], data_spacing[2])
        reader.Update()

        self._reader = reader
        
        return self._reader


    # Returns the image reader object
    def getReader(self):
        if self._reader is None:
            raise NameError("Please read a DICOM or TIFF image directory")
        return self._reader


    # Returns the image modality
    def getModality(self):
        if self._metaData is None:
            raise NameError("Please read a DICOM image for modality")
        elif type(self._metaData) is dict:
            return self._metaData["modality"]
        return self._metaData.Modality


    # Returns the plane orientation
    def getPlaneOrientation(self):
        if self._metaData is None:
            raise NameError("Please read a DICOM image for orientation")
        elif type(self._metaData) is dict:
            return self._metaData["orientation"]
        arr = self._reader.GetImageOrientationPatient()
        if arr[2] == 0 and arr[5] == 0:
            return "AXIAL"
        if arr[0] == 0 and arr[3] == 0:
            return "SAGITTAL"
        if arr[1] == 0 and arr[4] == 0:
            return "CORONAL"
        return "OBLIQUE"

    
    # Returns image pixel spacing
    def getPixelSpacing(self):
        if self._metaData is None:
            return 1
        elif type(self._metaData) is dict:
            return tuple(self._metaData["pixelSpacing"])
        return self._reader.GetPixelSpacing()

