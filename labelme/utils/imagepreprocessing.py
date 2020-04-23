import numpy as np
import io
import os.path as osp

from labelme import PY2
from labelme import QT4
from labelme import utils

import qimage2ndarray

from scipy.ndimage.filters import gaussian_filter


COLORSPACE_ORDER = ['R', 'G', 'B']

def sharpen(image, filename, a, b, sigma=10):
    image = qimage2ndarray.rgb_view(image)
    np_image = image / 255

    blurred = gaussian_filter(np_image, sigma=sigma)
    sharper = np.clip(np_image * a - blurred * b, 0, 1.0)
    np_image = sharper * 255

    return qimage2ndarray.array2qimage(np_image)

def adjustChannel(image, filename, color, values):
    image = qimage2ndarray.rgb_view(image)
    np_image = image / 255

    channel = np_image[:, :, COLORSPACE_ORDER.index(color)]

    orig_size = channel.shape
    flat_channel = channel.flatten()
    adjusted = np.interp(flat_channel, np.linspace(0, 1, len(values)), values)

    np_image[:, :, COLORSPACE_ORDER.index(color)] = adjusted.reshape(orig_size)
    np_image = np_image * 255

    return qimage2ndarray.array2qimage(np_image)
