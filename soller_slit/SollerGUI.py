__author__ = 'DAC_User'

import sys

from PyQt4 import QtGui

from soller_slit.controller.SollerController import SollerController

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    controller = SollerController()
    app.exec_()
    del app