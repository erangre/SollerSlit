#!/usr/bin/env python

# embedding_in_qt4.py --- Simple Qt4 application embedding matplotlib canvases
#
# Copyright (C) 2005 Florent Rougon
#               2006 Darren Dale
#
# This file is an example program for matplotlib. It may be used and
# modified with no restriction; raw copies as well as modified versions
# may be distributed without limitation.

from qtpy import QtCore, QtGui, QtWidgets
import sys
import numpy as np
from soller_slit.widgets.PlotWidget2 import PlotWidget


class SollerScanWidget(QtWidgets.QWidget):
    def __init__(self):
        super(SollerScanWidget, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        main_layout = QtWidgets.QVBoxLayout()

        # text layout:

        self.create_control_widgets(main_layout)
        self.create_plot_widgets(main_layout)

        self.create_grid_widgets(main_layout)
        self.create_grid_plot_widgets(main_layout)

        self.setLayout(main_layout)
        self.plot_widget.modify_mouse_behavior()
        self.grid_plot_widget.modify_mouse_behavior()

    def create_plot_widgets(self, main_layout):
        plot_layout = QtWidgets.QVBoxLayout()
        self.plot_widget = PlotWidget()
        self.mouse_pos_lbl = QtWidgets.QLabel("Testing the world")
        plot_layout.addWidget(self.plot_widget)
        plot_layout.addWidget(self.mouse_pos_lbl)
        main_layout.addLayout(plot_layout)

    def create_grid_plot_widgets(self, main_layout):
        plot_layout = QtWidgets.QVBoxLayout()
        self.grid_plot_widget = PlotWidget()
        self.grid_mouse_pos_lbl = QtWidgets.QLabel("Testing the world")
        plot_layout.addWidget(self.grid_plot_widget)
        plot_layout.addWidget(self.grid_mouse_pos_lbl)
        main_layout.addLayout(plot_layout)

    def create_control_widgets(self, main_layout):
        self.scaler_pv_txt = QtWidgets.QLineEdit("13IDC:scaler1")
        self.omega_pos_txt = NumberLineEdit("")
        self.range_txt = NumberLineEdit("0.1")
        self.step_txt = NumberLineEdit("0.005")
        self.time_txt = NumberLineEdit("0.1")
        self.scan_btn = QtWidgets.QPushButton("Scan")
        control_layout = QtWidgets.QHBoxLayout()
        control_layout.addWidget(QtWidgets.QLabel("Scaler PV:"))
        control_layout.addWidget(self.scaler_pv_txt)
        control_layout.addWidget(QtWidgets.QLabel("Position:"))
        control_layout.addWidget(self.omega_pos_txt)
        control_layout.addWidget(QtWidgets.QLabel("Range:"))
        control_layout.addWidget(self.range_txt)
        control_layout.addWidget(QtWidgets.QLabel("Step:"))
        control_layout.addWidget(self.step_txt)
        control_layout.addWidget(QtWidgets.QLabel("Time:"))
        control_layout.addWidget(self.time_txt)
        control_layout.addWidget(self.scan_btn)
        main_layout.addLayout(control_layout)

    def create_grid_widgets(self, main_layout):
        self.grid_range_txt = NumberLineEdit("0.05")
        self.grid_step_txt = NumberLineEdit("0.01")
        self.grid_btn = QtWidgets.QPushButton("Grid")
        self.abort_grid_btn = QtWidgets.QPushButton("Abort")
        grid_layout = QtWidgets.QHBoxLayout()
        grid_layout.addWidget(QtWidgets.QLabel("Grid Range:"))
        grid_layout.addWidget(self.grid_range_txt)
        grid_layout.addWidget(QtWidgets.QLabel("Step:"))
        grid_layout.addWidget(self.grid_step_txt)
        grid_layout.addWidget(self.grid_btn)
        grid_layout.addWidget(self.abort_grid_btn)
        grid_layout.addStretch()
        main_layout.addLayout(grid_layout)

    def raise_window(self):
        self.show()
        self.setWindowState(self.windowState() & QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.activateWindow()
        self.raise_()


class NumberLineEdit(QtWidgets.QLineEdit):
    def __init__(self, *args, **kwargs):
        super(NumberLineEdit, self).__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignRight)
        self.setValidator(QtGui.QDoubleValidator())


if __name__ == '__main__':
    qApp = QtWidgets.QApplication(sys.argv)

    aw = SollerScanWidget()
    aw.show()
    sys.exit(qApp.exec_())
    # qApp.exec_()
