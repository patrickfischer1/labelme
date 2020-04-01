import numpy as np
import io
import os.path as osp

from labelme import PY2
from labelme import QT4
from labelme import utils

from scipy.ndimage.filters import gaussian_filter

from PIL import Image, ImageEnhance, ImageQt, ImageChops

COLORSPACE_ORDER = ['R', 'G', 'B']

def loadImage(filepath):
    image_pil = Image.open(filepath)
    return image_pil

def sharpen(image, filename, a, b, sigma=10):
    image = image.convert('RGB')

    np_image = np.array(image)
    np_image = np_image / 255

    blurred = gaussian_filter(np_image, sigma=sigma)
    sharper = np.clip(np_image * a - blurred * b, 0, 1.0)
    np_image = sharper * 255

    image_filtered = Image.fromarray(np_image.astype('uint8'), 'RGB')

    return streamImageAsIO(image_filtered, filename)

def adjustChannel(image, filename, color, values):
    image = image.convert('RGB')

    np_image = np.array(image)
    np_image = np_image / 255

    channel = np_image[:, :, COLORSPACE_ORDER.index(color)]

    orig_size = channel.shape
    flat_channel = channel.flatten()
    adjusted = np.interp(flat_channel, np.linspace(0, 1, len(values)), values)

    np_image[:, :, COLORSPACE_ORDER.index(color)] = adjusted.reshape(orig_size)
    np_image = np_image * 255

    image_filtered = Image.fromarray(np_image.astype('uint8'), 'RGB')

    return streamImageAsIO(image_filtered, filename)

def streamImageAsIO(image, filename):
    with io.BytesIO() as f:
        ext = osp.splitext(filename)[1].lower()
        if PY2 and QT4:
            format = 'PNG'
        elif ext in ['.jpg', '.jpeg']:
               format = 'JPEG'
        else:
            format = 'PNG'
        image.save(f, format=format)
        f.seek(0)
        return f.read()
