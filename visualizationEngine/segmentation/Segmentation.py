import numpy as np
import os
import ctypes
import random
import time
from sys import platform
if platform == "darwin":
    lib_dir = os.path.join("region_growing", "mac_build")
else:
    lib_dir = os.path.join("region_growing", "windows_build")

if __name__ == "segmentation.Segmentation":
    lib_dir = os.path.join("visualizationEngine", "segmentation", lib_dir)
    # lib_dir = os.path.join("segmentation", lib_dir)


region_growing_C = np.ctypeslib.load_library("libregion_growing_lib", lib_dir)
array_1d_double = np.ctypeslib.ndpointer(dtype=np.double, ndim=1, flags='CONTIGUOUS')
array_1d_bool = np.ctypeslib.ndpointer(dtype=np.bool, ndim=1, flags='CONTIGUOUS')

region_growing_C.grow.restype = None
region_growing_C.grow.argtypes = [ctypes.c_int,    ctypes.c_int,    ctypes.c_int,
                                  array_1d_double, array_1d_bool,   ctypes.c_int,
                                  ctypes.c_int,    ctypes.c_int,    ctypes.c_double]


class Segmentation:
    def __init__(self, clicked_coordinate, volume, color=None, segmentation_threshold=0.2, verbose=False,
                 normalize_data=False):
        """
        Constructor for annotation class. __grow runs 3D region growing when the constructor is run.
        :param clicked_coordinate: Tuple conatining the coordinates of the point the user clicked on. Will be used
        as the start of segmentation.
        :param volume: 3D numpy array containing the volume to segment.
        :param color: Tuple or length 3 containing RGB values (0-255) for the color to set the annotations to. Default
        is None which randomizes the color.
        :param segmentation_threshold: Threshold for the region growing. The percentage of how much
        new voxels values values are allowed to deviate from the average of the current
        segmentation. t = 0.2 leads voxel withs values with 20% of the segmentation
        average being included every iteration.
        """
        # Attribute initializationss
        if color is None:
            color_list = []
            color_list += [round(random.uniform(0.0, 1.0), 2)]
            color_list += [round(random.uniform(0.65, 1.0), 2)]
            color_list += [round(random.uniform(0.0, 0.35), 2)]
            random.shuffle(color_list)
            self.color = (color_list[0], color_list[1], color_list[2])

        else:
            self.color = color
        self.segmentation = np.zeros_like(volume, dtype=np.bool)
        self.segmentation_threshold = segmentation_threshold
        # Setup actions
        if normalize_data:
            volume = self.__normalize_volume(volume)

        self.__grow(volume,
                    (int(clicked_coordinate[0]),
                     int(clicked_coordinate[1]),
                     int(clicked_coordinate[2])),
                    verbose=verbose)

    
    # Creating a 3D array like segmentation,
    # but with 1's and 0's instead of True and False
    def GetScalars(self):
        return self.segmentation.astype(np.int)

    
    def GetColor(self):
        return list(self.color)

    
    def add_to_vol(self, volume):
        """
        Colorized the given volume with its segmentation
        :param volume: 4-D numpy array for which to add the annotation to.
        :return: None
        """
        volume[self.segmentation, 0] = self.color[0]/255
        volume[self.segmentation, 1] = self.color[1]/255
        volume[self.segmentation, 2] = self.color[2]/255

    def __grow(self, volume, clicked_coordinate, verbose=False):
        """
        :param volume: 3D numpy array containing the volume to segment.
        :param clicked_coordinate: Tuple conatining the coordinates of the point from
        which to start the segementation.
        :return: None, the segmentation is stored in self.segmentation.
        """
        if verbose:
            print("Segmenting...")
        start = time.time()
        seg = self.segmentation.flatten()

        region_growing_C.grow(volume.shape[0], volume.shape[1], volume.shape[2], volume.flatten().astype(np.float64), seg,
                              clicked_coordinate[0], clicked_coordinate[1], clicked_coordinate[2],
                              self.segmentation_threshold)
        self.segmentation = np.reshape(seg, volume.shape)
        stop = time.time()
        print(self.segmentation.shape)
        time_elapsed = stop - start
        if verbose:
            percent_segmented = (np.count_nonzero(self.segmentation) / len(seg)) * 100
            print("Done. \n"
                  "Number of point in segment: {}\n"
                  "Segmentation percentage of volume: {} %\n"
                  "Time: {} s".format(len(list(np.where(seg))[0]),
                                      np.round(percent_segmented),
                                      np.round(time_elapsed, 2)))

    @staticmethod
    def __normalize_volume(volume):
        normalized_volume = volume - np.min(volume)
        normalized_volume = (normalized_volume / np.max(normalized_volume)) * 255
        return normalized_volume

    def __grow_py(self, clicked_coordinate, volume, t):
        """
        Python implemenation of __grow. At least 16 times slower then the C-implementation.
        Currently not used or tested for a while. Stored for possible future needs.
        :param clicked_coordinate: Tuple conatining the coordinates of the point from
        which to start the segementation.
        :param t: Threshold for the region growing. The allowed absolute difference
        between a new possible voxel and the segmentation average.
        :return: None, the segmentation is stored in self.segmentation.
        """
        checked = np.zeros_like(volume)
        self.segmentation[clicked_coordinate] = 1
        checked[clicked_coordinate] = True

        def get_nbhd_py(pt, checked, dims):
            nbhd = []
            if (pt[0] > 0) and not checked[pt[0] - 1, pt[1], pt[2]]:
                nbhd.append((pt[0] - 1, pt[1], pt[2]))
            if (pt[1] > 0) and not checked[pt[0], pt[1] - 1, pt[2]]:
                nbhd.append((pt[0], pt[1] - 1, pt[2]))
            if (pt[2] > 0) and not checked[pt[0], pt[1], pt[2] - 1]:
                nbhd.append((pt[0], pt[1], pt[2] - 1))
            if (pt[0] < dims[0] - 1) and not checked[pt[0] + 1, pt[1], pt[2]]:
                nbhd.append((pt[0] + 1, pt[1], pt[2]))
            if (pt[1] < dims[1] - 1) and not checked[pt[0], pt[1] + 1, pt[2]]:
                nbhd.append((pt[0], pt[1] + 1, pt[2]))
            if (pt[2] < dims[2] - 1) and not checked[pt[0], pt[1], pt[2] + 1]:
                nbhd.append((pt[0], pt[1], pt[2] + 1))
            return nbhd

        needs_check = get_nbhd_py(clicked_coordinate, checked, volume.shape)
        seg_avg = volume[clicked_coordinate]
        i = 1
        while len(needs_check) > 0:
            pt = needs_check.pop()
            if checked[pt]:
                continue
            checked[pt] = True
            if np.abs(volume[pt] - seg_avg) < t:
                self.segmentation[pt] = 1
                needs_check += get_nbhd_py(pt, checked, volume.shape)
                i += 1
                seg_avg += (volume[pt] - seg_avg) / i


if __name__ == "__main__":
    import PIL.Image
    import matplotlib.pyplot as plt


    class IndexTracker(object):
        def __init__(self, ax, volume):
            self.ax = ax
            ax.set_title('use scroll wheel to navigate images')

            self.volume = volume
            self.x = np.repeat(self.volume[:, :, :, np.newaxis], 3, axis=3)
            self.x = self.x/np.max(self.x)
            rows, cols, self.slices, _ = self.x.shape
            self.ind = self.slices // 2

            self.im = ax.imshow(self.x[:, :, self.ind, :])
            self.update()

            self.annotations = []

        def onscroll(self, event):
            if event.button == 'up':
                self.ind = (self.ind + 1) % self.slices
            else:
                self.ind = (self.ind - 1) % self.slices
            self.update()

        def onclick(self, event):
            clicked_coordinate = (int(event.ydata), int(event.xdata), self.ind)
            new_annotation = Segmentation(clicked_coordinate, self.volume, segmentation_threshold=0.3)
            # np.save("reference_segmentation", new_annotation.segmentation)
            # new_annotation.segmentation = np.load("reference_segmentation.npy")
            self.annotations += [new_annotation]
            new_annotation.add_to_vol(self.x)
            # self.x /= np.max(self.x)
            self.update()

        def update(self):
            self.im.set_data(self.x[:, :, self.ind])
            self.ax.set_ylabel('slice %s' % self.ind)
            self.im.axes.figure.canvas.draw()


    def load_volume(directory):
        slice_shape = np.array(PIL.Image.open(os.path.join(directory, "02.tif"))).shape
        dir_list = os.listdir(directory)
        dir_list = [item for item in dir_list if item.split(".")[-1] == "tif"]
        vol_shape = slice_shape + (len(dir_list),)
        vol = np.zeros(vol_shape, dtype=np.double, order='C')
        for vol_slice, filename in enumerate(dir_list):
            vol[:, :, vol_slice] = np.array(PIL.Image.open(os.path.join(directory, filename)))
        vol = (vol / np.max(vol)) * 255
        return vol

    directory = os.path.join("..", "..", "sample_dicom", "stanford-ct-new")
    vol = load_volume(directory) # (256, 256, 99)

    fig, ax = plt.subplots(1, 1)
    tracker = IndexTracker(ax, vol)

    fig.canvas.mpl_connect("scroll_event", tracker.onscroll)
    fig.canvas.mpl_connect("button_press_event", tracker.onclick)

    plt.show()
