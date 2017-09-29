from widgets.SollerScanWidget import SollerScanWidget
from epics import caget, caput
from epics.devices import Scaler
from qtpy import QtGui, QtWidgets
import numpy as np
import time
from config import epics_config, beamline_controls
from fitting import fit_gaussian
from circular_move import move_to_theta


class SollerScanController(object):
    def __init__(self):
        self.widget = SollerScanWidget()
        self.connect_signals()
        self.scaler = Scaler("13IDD:scaler1")
        self.widget.raise_window()

    def connect_signals(self):
        self.widget.plot_widget.mouse_moved.connect(self.scan_mouse_move_event)
        self.widget.scan_btn.clicked.connect(self.scan)

        self.widget.grid_plot_widget.mouse_moved.connect(self.grid_mouse_move_event)
        self.widget.grid_btn.clicked.connect(self.grid_scan)
        self.widget.abort_grid_btn.clicked.connect(self.abort_grid_scan)

    def scan_mouse_move_event(self, x, y):
        self.widget.mouse_pos_lbl.setText("x: {:.4f}   y: {:.4f}".format(x, y))
        self.widget.plot_widget.vline_item.setPos(x)
        self.widget.plot_widget.hline_item.setPos(y)

    def grid_mouse_move_event(self, x, y):
        self.widget.grid_mouse_pos_lbl.setText("x: {:.4f}   y: {:.4f}".format(x, y))
        self.widget.grid_plot_widget.vline_item.setPos(x)
        self.widget.grid_plot_widget.hline_item.setPos(y)

    def scan(self):
        theta_pv = epics_config['theta']
        # center_offset = 6.65
        # theta_offset = -18.8
        center_offset = 35.35
        theta_offset = -15.4

        motor_pos = float(caget(theta_pv + '.RBV'))
        soller_x_pos = float(caget(epics_config['x']+'.RBV'))
        soller_z_pos = float(caget(epics_config['z']+'.RBV'))

        scan_range = float(str(self.widget.range_txt.text()))
        scan_step = float(str(self.widget.step_txt.text()))
        scan_time = float(str(self.widget.time_txt.text()))

        scan_position = np.arange(-scan_range + motor_pos, motor_pos + scan_range + scan_step * 0.5, scan_step)

        pos = []
        data = []

        caput(beamline_controls['table_shutter'], 0)

        for position in scan_position:
            cur_position = float(caget(theta_pv + '.RBV'))

            move_to_theta(position, center_offset, theta_offset, wait=True)
            self.scaler.Count(scan_time, wait=True)
            read_data = self.scaler.Read()
            print(read_data)
            data.append(read_data[3])
            pos.append(position)
            self.widget.plot_widget.plot_data(pos, data)
            QtWidgets.QApplication.processEvents()

        caput(beamline_controls['table_shutter'], 1)
        move_to_theta(motor_pos, center_offset, theta_offset, wait=True)

        caput(epics_config['x'], soller_x_pos)
        caput(epics_config['z'], soller_z_pos)

        pos = np.array(pos)
        data = np.array(data)
        fit_pos = pos[data > 10]
        fit_data = data[data > 10]

        y_fit, center, fwhm, amp = fit_gaussian(fit_pos, fit_data)

        self.widget.plot_widget.plot_fit(fit_pos, y_fit)

        print(fwhm)
        return np.abs(fwhm)

    def grid_scan(self):

        self._abort_grid_scan = False
        cur_pos = float(caget(epics_config['x'] + '.RBV'))

        scan_range = float(str(self.widget.grid_range_txt.text()))
        scan_step = float(str(self.widget.grid_step_txt.text()))

        scan_position = np.arange(-scan_range + cur_pos, cur_pos + scan_range + scan_step * 0.5, scan_step)

        pos = []
        data = []
        for position in scan_position:
            if self._abort_grid_scan is True:
                break
            caput(epics_config['x'], position, wait=True)
            pos.append(position)
            data.append(self.scan())

            self.widget.grid_plot_widget.plot_data(pos, data)
            QtWidgets.QApplication.processEvents()

        caput(epics_config['x'], cur_pos, wait=True)

    def abort_grid_scan(self):
        self._abort_grid_scan = True

    def wait(self, wait_time, update_time=0.02):
        passed_time = 0
        while passed_time < wait_time:
            time.sleep(update_time)
            passed_time += update_time
            QtWidgets.QApplication.processEvents()

