__author__ = 'DAC_User'

import sys

from qtpy import QtGui, QtWidgets

from controller.SollerScanController import SollerScanController

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    controller = SollerScanController()
    app.exec_()
    del app
