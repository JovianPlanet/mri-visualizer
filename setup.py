import os
import nibabel as nib
import numpy as np
from PyQt5 import QtWidgets
from popups import ErrorDialog
import GUI
from utils import conv2QImage


class GuiSetUp(QtWidgets.QMainWindow, GUI.Ui_Form):

    def __init__(self):

        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.browse_button.clicked.connect(self.get_path)
        self.loadSlice_button.clicked.connect(self.load_slice)
        self.loadMRI_button.clicked.connect(self.load_mri)

        #self.sliceSlider.valueChanged.connect(self.make_)

        self.axial_cb.stateChanged.connect(self.update_gui)
        self.sagital_cb.stateChanged.connect(self.update_gui)
        self.coronal_cb.stateChanged.connect(self.update_gui)

        self.scene = None

        self.path = './data/sub-A00028352_ses-NFB3_T1w.nii.gz'

        self.view = ''

        self.vol = None

    def get_path(self):

        self.path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "Images (*.nii *.nii.gz)")
        self.path_edit.setText(self.path)
        return

    def load_mri(self):
        self.vol = nib.load(self.path).get_data()
        print(f'{self.vol.shape=}, type - {self.vol.dtype}')

        init_slice = 0

        if self.axial_cb.isChecked():
            self.view = 'axial'
            self.sliceSlider.setMaximum(self.vol.shape[2])
            self.sliceSlider.setValue(self.vol.shape[2]/2)
            self.pixmap = conv2QImage(self.vol[:, :, self.sliceSlider.value()])
        elif self.sagital_cb.isChecked():
            self.view = 'sagital'
            self.sliceSlider.setMaximum(self.vol.shape[1])
            self.sliceSlider.setValue(self.vol.shape[1]/2)
            self.pixmap = conv2QImage(self.vol[:, self.sliceSlider.value(), :])
        elif self.coronal_cb.isChecked():
            self.view = 'coronal'
            self.sliceSlider.setMaximum(self.vol.shape[0])
            self.sliceSlider.setValue(self.vol.shape[0]/2)
            self.pixmap = conv2QImage(self.vol[self.sliceSlider.value(), :, :])
        else:
            self.show_message('ERROR: Debe seleccionar una vista antes de cargar la imagen', False)
            return

        self.scene = QtWidgets.QGraphicsScene(0, 0, self.vol.shape[0], self.vol.shape[1])

        pixmapitem = self.scene.addPixmap(self.pixmap)
        pixmapitem.setPos(0, 0)

        self.graphicsView.setScene(self.scene)
        self.graphicsView.show()
        #app.exec_()
        return

    def load_slice(self):
        try:
            slicenum = int(self.lineEdit_slice.text())
        except:
            self.show_message('ERROR: Inserte un valor númerico valido', False)
            return

        if self.view == 'axial':
            if slicenum > self.vol.shape[2]:
                self.show_message('ERROR: El número de slice seleccionado es mayor al número total de slices', False)
                return
            self.pixmap = conv2QImage(self.vol[:, :, slicenum])
        elif self.view == 'sagital':
            if slicenum > self.vol.shape[1]:
                self.show_message('ERROR: El número de slice seleccionado es mayor al número total de slices', False)
                return
            self.pixmap = conv2QImage(self.vol[:, slicenum, :])
        elif self.view == 'coronal':
            if slicenum > self.vol.shape[0]:
                self.show_message('ERROR: El número de slice seleccionado es mayor al número total de slices', False)
                return
            self.pixmap = conv2QImage(self.vol[slicenum, :, :])
        else:
            self.show_message('ERROR: Aún no se ha seleccionado una vista', False)
        pixmapitem = self.scene.addPixmap(self.pixmap)
        pixmapitem.setPos(0, 0)
        self.scene.update()

        return


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


# def make_dl(self):

#     flag=False

#     try:
#         with open('dl.py', 'x') as dl:
#             for line in template.splitlines(keepends=True):

#                 if "self.path = './data/train'" in line:
#                     dl.write(line.replace('./data/train', self.path))

#                 elif "self.mri_name = 'T1.nii'" in line:
#                     if self.load_mri_cb.isChecked():
#                         dl.write(line.replace('T1.nii', self.mri_name_le.text()))
#                     else:
#                         dl.write(line)

#                 elif "self.labels_name = None" in line:
#                     if self.load_labels_cb.isChecked():
#                         dl.write(line.replace('None', "'"+self.label_name_le.text()+"'"))
#                     else:
#                         dl.write(line)

#                 elif "self.dims = False" in line:
#                     if self.resize_cb.isChecked():
#                         dl.write(line.replace('False', f'({self.width_spinbox.value()}, {self.height_spinbox.value()})', -1))
#                     else:
#                         dl.write(line)

#                 elif "self.remove_bgnd = False" in line:
#                     if self.bgnd_cb.isChecked():
#                         dl.write(line.replace('False', 'True'))
#                     else:
#                         dl.write(line)

#                 elif "self.crop = False" in line:
#                     print(f'crop false in line')
#                     if self.crop_cb.isChecked():
#                         print(f'crop is checked')
#                         if self.low_slice_sb.value() < self.up_slice_sb.value():
#                             print('Es menor')
#                             dl.write(line.replace('False', f'({self.low_slice_sb.value()}, {self.up_slice_sb.value()})', -1))
#                         else:
#                             print('Es mayor')
#                             self.show_message('ERROR: Low slice must be smaller than upper slice', True)
#                             flag=True
#                             break
#                     else:
#                         dl.write(line)

#                 else:
#                     dl.write(line)

#     except:
#         self.show_message('El archivo ya existe, por favor borrelo e intente de nuevo', False)
#         return

#     if flag:
#         os.remove('dl.py')
#     else:
#         self.show_message('El dataset fue creado exitosamente', False)
#         self.close()

#     return