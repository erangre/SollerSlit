__author__ = 'DAC_User'

__version__ = 0.1

from Views.MainWidget import MainWidget
from epics import PV, caget, caput

from PyQt4 import QtCore, QtGui
import os
import csv

from circular_move import perform_rotation_trajectory_corrected, collect_data

pv_names = {
    'soller_x': '13IDD:m93',
    'soller_z': '13IDD:m94',
    'soller_theta': '13IDD:m95'
}


class MainController(object):
    def __init__(self):
        self.widget = MainWidget('Soller Slit Controller - {}'.format(__version__))
        self.create_signals()
        self.connect_pv()
        self.update_values()

        self.load_configuration()
        self.raise_window()

    def create_signals(self):
        self.widget.soller_x_down_btn.clicked.connect(self.soller_x_down_btn_clicked)
        self.widget.soller_x_up_btn.clicked.connect(self.soller_x_up_btn_clicked)

        self.widget.soller_z_down_btn.clicked.connect(self.soller_z_down_btn_clicked)
        self.widget.soller_z_up_btn.clicked.connect(self.soller_z_up_btn_clicked)

        self.widget.soller_theta_down_btn.clicked.connect(self.soller_theta_down_btn_clicked)
        self.widget.soller_theta_up_btn.clicked.connect(self.soller_theta_up_btn_clicked)

        self.widget.soller_x_pos_txt.returnPressed.connect(self.soller_x_pos_changed)
        self.widget.soller_z_pos_txt.returnPressed.connect(self.soller_z_pos_changed)
        self.widget.soller_theta_pos_txt.returnPressed.connect(self.soller_theta_pos_changed)

        self.widget.collect_btn.clicked.connect(self.collect_btn_click)

        self.widget.closeEvent = self.close_event

    def connect_pv(self):
        self.update_timer = QtCore.QTimer(self.widget)
        self.update_timer.timeout.connect(self.update_values)
        self.update_timer.start(100)

    def update_values(self):
        soller_x = caget(pv_names['soller_x'] + '.RBV')
        soller_z = caget(pv_names['soller_z'] + '.RBV')
        soller_theta = caget(pv_names['soller_theta'] + '.RBV')

        self.widget.update_values(soller_x, soller_z, soller_theta)

    def soller_x_down_btn_clicked(self):
        cur_pos = caget(pv_names['soller_x'] + '.RBV')
        step = float(str(self.widget.soller_x_step_txt.text()))
        caput(pv_names['soller_x'] + '.VAL', cur_pos - step)

    def soller_x_up_btn_clicked(self):
        cur_pos = caget(pv_names['soller_x'] + '.RBV')
        step = float(str(self.widget.soller_x_step_txt.text()))
        caput(pv_names['soller_x'] + '.VAL', cur_pos + step)

    def soller_z_down_btn_clicked(self):
        cur_pos = caget(pv_names['soller_z'] + '.RBV')
        step = float(str(self.widget.soller_z_step_txt.text()))
        caput(pv_names['soller_z'] + '.VAL', cur_pos - step)

    def soller_z_up_btn_clicked(self):
        cur_pos = caget(pv_names['soller_z'] + '.RBV')
        step = float(str(self.widget.soller_z_step_txt.text()))
        caput(pv_names['soller_z'] + '.VAL', cur_pos + step)

    def soller_theta_down_btn_clicked(self):
        self.widget.enable_controls(False)
        self.widget.status_txt.text('Rotating')
        step = float(str(self.widget.soller_theta_step_txt.text()))
        center_offset = float(str(self.widget.center_offset_txt.text()))
        theta_offset = float(str(self.widget.theta_offset_txt.text()))

        QtGui.QApplication.processEvents()
        perform_rotation_trajectory_corrected(center_offset=center_offset,
                                              rotation_time=step * 2,
                                              angle=-step,
                                              theta_offset=theta_offset)
        self.widget.enable_controls(True)
        self.widget.status_txt.text('')

    def soller_theta_up_btn_clicked(self):
        self.widget.enable_controls(False)
        self.widget.status_txt.text('Rotating')

        step = float(str(self.widget.soller_theta_step_txt.text()))
        center_offset = float(str(self.widget.center_offset_txt.text()))
        theta_offset = float(str(self.widget.theta_offset_txt.text()))

        QtGui.QApplication.processEvents()
        perform_rotation_trajectory_corrected(center_offset=center_offset,
                                              rotation_time=step * 2,
                                              angle=step,
                                              theta_offset=theta_offset)
        self.widget.enable_controls(True)
        self.widget.status_txt.text('')

    def soller_x_pos_changed(self):
        new_value = float(str(self.widget.soller_x_pos_txt.text()))
        caput(pv_names['soller_x'] + '.VAL', new_value)

    def soller_z_pos_changed(self):
        new_value = float(str(self.widget.soller_z_pos_txt.text()))
        caput(pv_names['soller_z'] + '.VAL', new_value)

    def soller_theta_pos_changed(self):
        self.widget.enable_controls(False)
        self.widget.status_txt.text('Rotating')

        cur_value = float(caget(pv_names['soller_theta'] + '.RBV'))
        new_value = float(str(self.widget.soller_theta_pos_txt.text()))

        step = new_value - cur_value

        center_offset = float(str(self.widget.center_offset_txt.text()))
        theta_offset = float(str(self.widget.theta_offset_txt.text()))

        QtGui.QApplication.processEvents()

        print cur_value, new_value, step, center_offset, theta_offset
        perform_rotation_trajectory_corrected(center_offset=center_offset,
                                              rotation_time=abs(step) * 2,
                                              angle=step,
                                              theta_offset=theta_offset)
        self.widget.enable_controls(True)
        self.widget.status_txt.text('')

    def collect_btn_click(self):
        detector_pv = str(self.widget.detector_pv_txt.text())
        collection_time = float(str(self.widget.collection_time_txt.text()))
        collection_angle = float(str(self.widget.collection_angle_txt.text()))

        center_offset = float(str(self.widget.center_offset_txt.text()))
        theta_offset = float(str(self.widget.theta_offset_txt.text()))

        collect_data(center_offset=center_offset,
                     collection_time=collection_time,
                     angle=collection_angle,
                     theta_offset=theta_offset)

    def raise_window(self):
        self.widget.show()
        self.widget.setWindowState(self.widget.windowState() & QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.widget.activateWindow()
        self.widget.raise_()

    def load_configuration(self):
        if os.path.exists('config.ini'):
            reader = csv.reader(open('config.ini', 'r'))
            configuration = dict(x for x in reader)
        else:
            configuration = {
                'center_offset': '35.65',
                'theta_offset': '-0.33',
                'detector_pv': '13MAR345_2:cam1',
                'collection_time': '60',
                'collection_angle': '3.199',
            }

        self.widget.center_offset_txt.setText(configuration['center_offset'])
        self.widget.theta_offset_txt.setText(configuration['theta_offset'])
        self.widget.detector_pv_txt.setText(configuration['detector_pv'])
        self.widget.collection_time_txt.setText(configuration['collection_time'])
        self.widget.collection_angle_txt.setText(configuration['collection_angle'])

    def save_configuration(self):
        writer = csv.writer(open('config.ini', 'w'))
        configuration = {
            'center_offset': str(self.widget.center_offset_txt.text()),
            'theta_offset': str(self.widget.theta_offset_txt.text()),
            'detector_pv': str(self.widget.detector_pv_txt.text()),
            'collection_time': str(self.widget.collection_time_txt.text()),
            'collection_angle': str(self.widget.collection_angle_txt.text())
        }
        for key, value in list(configuration.items()):
            writer.writerow([key, value])

    def close_event(self, _):
        self.save_configuration()
        QtGui.QApplication.closeAllWindows()
        QtGui.QApplication.quit()

