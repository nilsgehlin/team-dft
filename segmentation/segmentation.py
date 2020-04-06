import numpy as np
import os
import PIL
import matplotlib.pyplot as plt
import cv2


def get_nbhd(pt, checked, dims):
    nbhd = []

    if (pt[0] > 0) and not checked[pt[0]-1, pt[1], pt[2]]:
        nbhd.append((pt[0]-1, pt[1], pt[2]))
    if (pt[1] > 0) and not checked[pt[0], pt[1]-1, pt[2]]:
        nbhd.append((pt[0], pt[1]-1, pt[2]))
    if (pt[2] > 0) and not checked[pt[0], pt[1], pt[2]-1]:
        nbhd.append((pt[0], pt[1], pt[2]-1))

    if (pt[0] < dims[0]-1) and not checked[pt[0]+1, pt[1], pt[2]]:
        nbhd.append((pt[0]+1, pt[1], pt[2]))
    if (pt[1] < dims[1]-1) and not checked[pt[0], pt[1]+1, pt[2]]:
        nbhd.append((pt[0], pt[1]+1, pt[2]))
    if (pt[2] < dims[2]-1) and not checked[pt[0], pt[1], pt[2]+1]:
        nbhd.append((pt[0], pt[1], pt[2]+1))

    return nbhd


def grow(img, seed, t):
    seg = np.zeros(img.shape, dtype=np.uint8)
    checked = np.zeros_like(seg)

    seg[seed] = 1
    checked[seed] = True
    needs_check = get_nbhd(seed, checked, img.shape)

    seg_avg = img[seed]
    i = 1
    while len(needs_check) > 0:
        pt = needs_check.pop()
        if checked[pt]:
            continue

        checked[pt] = True

        # # Handle borders.
        # imin = max(pt[0] - t, 0)
        # imax = min(pt[0] + t, img.shape[0] - 1)
        # jmin = max(pt[1] - t, 0)
        # jmax = min(pt[1] + t, img.shape[1] - 1)
        # kmin = max(pt[2] - t, 0)
        # kmax = min(pt[2] + t, img.shape[2] - 1)
        # if img[pt] >= img[imin:imax + 1, jmin:jmax + 1, kmin:kmax + 1].mean():
            # Include the voxel in the segmentation and
            # add its neighbors to be checked.

        if np.abs(img[pt] - seg_avg) < 20:
            seg[pt] = 1
            needs_check += get_nbhd(pt, checked, img.shape)
            i += 1
            seg_avg += (img[pt] - seg_avg) / i

    return seg


def load_volume(directory, no_slices=99):
    slice_shape = np.array(PIL.Image.open(os.path.join(directory, "image.1"))).shape
    vol_shape = slice_shape + (no_slices,)
    vol = np.zeros(vol_shape)
    for slice in range(no_slices):
        vol[:, :, slice] = np.array(PIL.Image.open(os.path.join(directory, "image.{}".format(slice + 1))))

    vol = (vol / np.max(vol)) * 255
    return vol


if __name__ == "__main__":
    directory = os.path.join("..", "2d3dprototype", "stanford-ct-new")
    vol = load_volume(directory)
    vol = vol[:, :, 43:50]
    slice_no = 2
    plt.figure()
    plt.imshow(vol[:, :, slice_no], cmap="gray")
    plt.title("CLICK ON POINT TO ANNOTATE")
    clicked_point_float = plt.ginput(1)[0]
    clicked_point = (int(clicked_point_float[1]), int(clicked_point_float[0]), slice_no)
    t = 10
    segmentation = grow(vol, clicked_point, t)
    colored_vol = np.repeat(vol[:, :, :, np.newaxis], 3, axis=3)
    colored_vol[segmentation == 1, 0] = 255
    colored_vol[segmentation == 1, 1] = 0
    colored_vol[segmentation == 1, 2] = 0

    for i in reversed(range(colored_vol.shape[2])):
        plt.figure()
        plt.imshow(colored_vol[:, :, i, :].astype(np.uint8))
        plt.title("SLICE NO {}".format(i + 1))

    plt.show()