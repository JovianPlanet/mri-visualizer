from PyQt5 import QtGui
import numpy as np

import PIL
from PIL import Image, ImageQt


def conv2QImage(im):

	# height, width, channel = im.shape
	# bytesPerLine = width

	img = Image.fromarray(im[:,:,80]).convert('RGB')#.astype(np.uint16))
	qim = ImageQt.ImageQt(img)
	pm = QtGui.QPixmap.fromImage(qim)

	#qimg = QtGui.QImage(im[:,:,100], width, height, bytesPerLine, QtGui.QImage.Format_RGB888)#
	#pixmap = QtGui.QPixmap.fromImage(im[:,:,100])

	return pm
