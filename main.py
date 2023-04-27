#-*- coding: utf-8 -*-
#
#          ITM           #
#        Catedra         #
# David Jimenez Murillo  #

from PyQt5 import QtWidgets
import sys
import setup


def main():

    app = QtWidgets.QApplication(sys.argv)
    form = setup.GuiSetUp()#GUI()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':

    main()

