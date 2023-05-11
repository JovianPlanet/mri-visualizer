from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QPushButton, QDialogButtonBox, QVBoxLayout, QLabel, QMessageBox


class ErrorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Atención")

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.message = QLabel(" ")
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.buttonBox, alignment=QtCore.Qt.AlignCenter)
        self.setLayout(self.layout)