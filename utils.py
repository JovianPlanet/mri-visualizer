from PyQt5 import QtGui
import numpy as np

import PIL
from PIL import Image, ImageQt


def conv2QImage(im):

    # height, width, channel = im.shape
    # bytesPerLine = width

    img = Image.fromarray(im[:,:]/im.max()*255).convert('RGB')#(im[:,:,80], mode="RGBA")#
    #print(f'PIL tipo - {type(img)}')
    qim = ImageQt.ImageQt(img)
    pm = QtGui.QPixmap.fromImage(qim)

    return pm
