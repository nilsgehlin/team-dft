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
    _ext = None

    ##### General class functions #####


    # Initializer for imageReader, takes one optional parameter
    # for the directory (Throws an error if more than 1).
    def __init__(self, *args):
        if len(args) > 0:
            self.setImageDirectory(args[0])
        if len(args) > 1:
            raise NameError("More than one argument for the constructor!")
        
    
    ##### Public class functions #####


    # Sets the image directory to be read
    def setImageDirectory(self, dir):
        self._directory = dir

        first_file_name = os.listdir(dir)[0]
        file_suffix = first_file_name.split(".")[-1]
        if file_suffix == "dcm":
            self._ext = file_suffix
        elif file_suffix == "tif" or file_suffix.isdigit():
            self._ext = "tif"
        else:
            # raise NameError("Unsupported image extension in the directory")
            raise NameError("File suffix {} is not supported!".format(file_suffix))


    # Reads a directory of images disregarding extensions and returns an
    # image reader object
    def readImages(self):
        if self._directory is None:
            raise NameError("Please set image directory")
        
        if self._ext == 'dcm':
            return self.readDicom()
        if self._ext == 'tif':
            return self.readTiff()


    # Reads a directory of TIFF images and returns an
    # image reader object
    def readTiff(self):
        if self._directory is None:
            raise NameError("Please set image directory")

        # Accumulate file names
        filenames = vtkStringArray()
        dir_list = os.listdir(self._directory)
        dir_list.sort()
        for filename in dir_list:
            filenames.InsertNextValue(os.path.join(self._directory, filename))

        with open(os.path.join(self._directory, "meta_data.json")) as meta_data_file:
            self._metaData = json.load(meta_data_file)

        # Create reader object with filenames
        reader = vtkTIFFReader()
        reader.SetFileNames(filenames)
        reader.SetDataSpacing(self._metaData["pixelSpacing"])
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
            # return tuple(self._metaData["pixelSpacing"])
            return self._reader.GetDataSpacing()
        return self._reader.GetPixelSpacing()

