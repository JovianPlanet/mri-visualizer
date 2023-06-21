from PyQt5 import QtGui
import numpy as np
import nibabel as nib

import PIL
from PIL import Image, ImageQt


def conv2QImage(im):

    # height, width, channel = im.shape
    # bytesPerLine = width

    im = np.flipud(np.moveaxis(im, -1, 0))

    img = Image.fromarray(im[:,:]/im.max()*255).convert('RGB')#(im[:,:,80], mode="RGBA")#
    #print(f'PIL tipo - {type(img)}')
    qim = ImageQt.ImageQt(img)
    pm = QtGui.QPixmap.fromImage(qim)

    return pm

def get_orientation(scan_obj):

    ori = {'X': None, 'Y': None, 'Z': None}

    scan_aff  = scan_obj.affine

    ori["X"], ori["Y"], ori["Z"] = nib.aff2axcodes(scan_aff)

    return ori

def swap_axis(o):

    swap = ''

    flip = -1 if o not in ['R', 'A', 'S'] else 1

    if o in ['R', 'L']:
        swap = 0
    elif o in ['A', 'P']:
        swap = 1
    else:
        swap = 2

    return swap, flip

def RAS_orientation(tgt_obj): #(pathtgt, pathout):

    #tgt_obj = nib.load(pathtgt)
    #tgt_aff  = tgt_obj.affine

    tgt_axc = get_orientation(tgt_obj)

    print(f'Orientacion raw:\nX:{tgt_axc["X"]}, Y:{tgt_axc["Y"]}, Z:{tgt_axc["Z"]}\n')

    ax, a0 = swap_axis(tgt_axc['X'])
    ay, a1 = swap_axis(tgt_axc['Y'])
    az, a2 = swap_axis(tgt_axc['Z'])

    ornt = [[ax, a0],
            [ay, a1],
            [az, a2]]

    print(f'{ornt}')

    img_orient = tgt_obj.as_reoriented(ornt)
    # nib.save(img_orient, pathout)

    return img_orient

def pad_img(im, width, height):

    tupla_width = (int((width - im.shape[0]) / 2), int((width - im.shape[0]) / 2))
    tupla_height = (int((height - im.shape[1]) / 2), int((height - im.shape[1]) / 2))
    im = np.pad(im, (tupla_width, tupla_height))

    return im

def set_dims(view_w, vol_w, view_h, vol_h):

    if view_w > vol_w:
        w = view_w
    else:
        w = vol_w
    if view_h > vol_h:
        h = view_h
    else:
        h = vol_h

    return w, h