__author__ = 'DAC_User'

import sys

from qtpy import QtGui, QtWidgets

from soller_slit.controller.SollerController import SollerController

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    controller = SollerController()
    app.exec_()
    del app