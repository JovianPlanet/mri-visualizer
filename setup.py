import os
import nibabel as nib
import numpy as np
from PyQt5 import QtWidgets, QtCore
from popups import ErrorDialog
import GUI
from utils import conv2QImage, RAS_orientation, pad_img, set_dims


class GuiSetUp(QtWidgets.QMainWindow, GUI.Ui_Form):

    def __init__(self):

        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.browse_button.clicked.connect(self.get_path)
        self.loadSlice_button.clicked.connect(self.load_slice)
        self.sliceSlider.sliderMoved.connect(self.slide)
        self.loadMRI_button.clicked.connect(self.load_mri)

        self.axial_cb.stateChanged.connect(self.update_gui)
        self.sagital_cb.stateChanged.connect(self.update_gui)
        self.coronal_cb.stateChanged.connect(self.update_gui)

        self.scene = None
        self.width = self.graphicsView.geometry().width()
        self.height = self.graphicsView.geometry().height()

        self.path = './data/sub-A00028352_ses-NFB3_T1w.nii.gz'

        self.view = ''

        self.vol = None

    # Función que captura la ruta donde se encuentra la imagen
    def get_path(self):

        self.path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File")#, "Images (*.nii *.nii.gz)")
        self.path_edit.setText(self.path)
        return

    # Función que carga la imagen, ubica la vista que se quiere desplegar y crea la escena
    # a partir del slice central
    def load_mri(self):

        mri = RAS_orientation(nib.load(self.path)) # Orient image to RAS
        print(f'Orientacion swapped:\n{nib.aff2axcodes(mri.affine)}\n')

        try:
            self.vol = mri.get_fdata().squeeze(3)
        except:
            self.vol = mri.get_fdata()

        print(self.vol.shape)

        gview_w = self.graphicsView.geometry().width()
        gview_h = self.graphicsView.geometry().height()

        # axial (x-y), coronal (x-z) and sagittal (y-z)
        if self.axial_cb.isChecked():
            self.view = 'axial'
            self.sliceSlider.setMaximum(self.vol.shape[2])
            self.sliceSlider.setValue(int(self.vol.shape[2]/2))
            im = self.vol[:, :, self.sliceSlider.value()]
            self.width, self.height = set_dims(gview_w, self.vol.shape[0], gview_h, self.vol.shape[1])

        elif self.coronal_cb.isChecked():
            self.view = 'coronal'
            self.sliceSlider.setMaximum(self.vol.shape[1])
            self.sliceSlider.setValue(int(self.vol.shape[1]/2))
            im = self.vol[:, self.sliceSlider.value(), :]
            self.width, self.height = set_dims(gview_w, self.vol.shape[0], gview_h, self.vol.shape[2])

        elif self.sagital_cb.isChecked():
            self.view = 'sagital'
            self.sliceSlider.setMaximum(self.vol.shape[0])
            self.sliceSlider.setValue(int(self.vol.shape[0]/2))
            im = self.vol[self.sliceSlider.value(), :, :]
            self.width, self.height = set_dims(gview_w, self.vol.shape[1], gview_h, self.vol.shape[2])

        else:
            self.show_message('ERROR: Debe seleccionar una vista antes de cargar la imagen', False)
            return

        im = pad_img(im, self.width, self.height)
        self.pixmap = conv2QImage(im)

        self.scene = QtWidgets.QGraphicsScene(0, 0, self.width, self.height)

        pixmapitem = self.scene.addPixmap(self.pixmap)
        pixmapitem.setPos(0, 0)

        #self.graphicsView.fitInView(pixmapitem, QtCore.Qt.KeepAspectRatio)

        self.graphicsView.setScene(self.scene)
        self.graphicsView.show()

        return

    # Función para cargar el slice, especificado en el campo de texto, al presionar el botón 'Load'
    def load_slice(self):
        try:
            n = int(self.lineEdit_slice.text())
        except:
            self.show_message('ERROR: Ingrese un valor númerico valido', False)
            return    

        self.update_scene(n)       

        return

    # Función que permite "deslizarse" a lo largo de todos los slices de la imagen
    def slide(self):
        try:
            n = int(self.sliceSlider.value())
        except:
            self.show_message('ERROR: Ingrese un valor númerico valido', False)
            return

        self.update_scene(n)
        return

    # Función que actualiza la escena de acuerdo con el slice especificado
    def update_scene(self, s):

        if self.view == 'axial':
            if s > self.vol.shape[2]:
                self.show_message('ERROR: El número de slice seleccionado es mayor al número total de slices', False)
                return
            # self.pixmap = conv2QImage(self.vol[:, :, s])
            self.pixmap = conv2QImage(pad_img(self.vol[:, :, s], self.width, self.height))

        elif self.view == 'coronal':
            if s > self.vol.shape[1]:
                self.show_message('ERROR: El número de slice seleccionado es mayor al número total de slices', False)
                return
            # self.pixmap = conv2QImage(self.vol[:, s, :])
            self.pixmap = conv2QImage(pad_img(self.vol[:, s, :], self.width, self.height))

        elif self.view == 'sagital':
            if s > self.vol.shape[0]:
                self.show_message('ERROR: El número de slice seleccionado es mayor al número total de slices', False)
                return
            # self.pixmap = conv2QImage(self.vol[s, :, :])
            self.pixmap = conv2QImage(pad_img(self.vol[s, :, :], self.width, self.height))
            
        else:
            self.show_message('ERROR: Aún no se ha seleccionado una vista', False)

        pixmapitem = self.scene.addPixmap(self.pixmap)
        pixmapitem.setPos(0, 0)
        self.scene.update()
        return

    # Función que actualiza la GUI cuando se activa o desactiva un campo de selección
    def update_gui(self):

        if self.axial_cb.isChecked():
            self.sagital_cb.setEnabled(False)
            self.coronal_cb.setEnabled(False)

        elif self.sagital_cb.isChecked():
            self.axial_cb.setEnabled(False)
            self.coronal_cb.setEnabled(False)

        elif self.coronal_cb.isChecked():
            self.axial_cb.setEnabled(False)
            self.sagital_cb.setEnabled(False)
            
        else:
            self.axial_cb.setEnabled(True)
            self.sagital_cb.setEnabled(True)
            self.coronal_cb.setEnabled(True)


    # Función para desplegar los mensajes de error
    def show_message(self, s, rem):
        print("click", s)

        dlg = ErrorDialog(self)
        dlg.message.setText(s)
        if dlg.exec():
            print("Error!")

'''
app = QApplication(sys.argv)

# Defining a scene rect of 400x200, with it's origin at 0,0.
# If we don't set this on creation, we can set it later with .setSceneRect
scene = QGraphicsScene(0, 0, 400, 200)

view = QGraphicsView(scene)
view.show()
app.exec_()
'''
