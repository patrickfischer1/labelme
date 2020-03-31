import numpy as np
import io
import os.path as osp

from labelme import PY2
from labelme import QT4
from labelme import utils

from PIL import Image, ImageEnhance, ImageQt, ImageChops

def loadImage(filepath):
    image_pil = Image.open(filepath)
    return image_pil

def imgAdjustBrightness(image, filename, perc):
    enhancer = ImageEnhance.Brightness(image)
    pilimg = enhancer.enhance(perc / 100.0)

    return streamImageAsIO(pilimg, filename)

def imgAdjustColor(image, filename, perc):
    enhancer = ImageEnhance.Color(image)
    pilimg = enhancer.enhance(perc / 100.0)

    return streamImageAsIO(pilimg, filename)    

def colorFilter(image, filename, color, alpha):
    if color == 'R':
        color_rgb = (255, 255 * (1 - alpha), 255 * (1 - alpha))   
    elif color == 'G':
        color_rgb = (255 * (1 - alpha), 255, 255 * (1 - alpha))
    else:
        color_rgb = (255 * (1 - alpha), 255 * (1 - alpha), 255)

    img_array = np.full((image.size[1], image.size[0], 3), color_rgb, np.uint8)
    blend_image = Image.fromarray(img_array, 'RGB')

    image = image.convert('RGBA')
    blend_image = blend_image.convert('RGBA')

    image = ImageChops.multiply(image, blend_image)

    return streamImageAsIO(image, filename)

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
