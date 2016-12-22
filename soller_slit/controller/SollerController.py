__author__ = 'Clemens Prescher'
__version__ = 0.1

import os
import csv
from threading import Thread
import time

from epics import caget, caput

from qtpy import QtCore, QtGui, QtWidgets
import numpy as np

from soller_slit.widgets.SollerWidget import MainWidget
from soller_slit.circular_move import perform_rotation_trajectory_corrected, collect_data
from ..config import epics_config


class SollerController(object):
    def __init__(self):
        self.widget = MainWidget('Soller Slit controller - {}'.format(__version__))
        self.create_signals()
        self.connect_pv()
        self.update_values()

        self.load_configuration()
        self.raise_window()

        self.map_aborted = False

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

        self.widget.detector_pv_txt.returnPressed.connect(self.detector_pv_txt_changed)

        self.widget.collect_btn.clicked.connect(self.collect_btn_click)
        self.widget.collect_map_btn.clicked.connect(self.collect_map_btn_click)
        self.widget.pv2_cb.toggled.connect(self.pv2_cb_toggled)

        self.widget.closeEvent = self.close_event

    def connect_pv(self):
        self.update_timer = QtCore.QTimer(self.widget)
        self.update_timer.timeout.connect(self.update_values)
        self.update_timer.start(100)

    def update_values(self):
        soller_x = caget(epics_config['x'] + '.RBV')
        soller_z = caget(epics_config['z'] + '.RBV')
        soller_theta = caget(epics_config['theta'] + '.RBV')

        self.widget.update_motor_values(soller_x, soller_z, soller_theta)

    def soller_x_down_btn_clicked(self):
        cur_pos = caget(epics_config['x'] + '.RBV')
        step = float(str(self.widget.soller_x_step_txt.text()))
        caput(epics_config['x'] + '.VAL', cur_pos - step)

    def soller_x_up_btn_clicked(self):
        cur_pos = caget(epics_config['x'] + '.RBV')
        step = float(str(self.widget.soller_x_step_txt.text()))
        caput(epics_config['x'] + '.VAL', cur_pos + step)

    def soller_z_down_btn_clicked(self):
        cur_pos = caget(epics_config['z'] + '.RBV')
        step = float(str(self.widget.soller_z_step_txt.text()))
        caput(epics_config['z'] + '.VAL', cur_pos - step)

    def soller_z_up_btn_clicked(self):
        cur_pos = caget(epics_config['z'] + '.RBV')
        step = float(str(self.widget.soller_z_step_txt.text()))
        caput(epics_config['z'] + '.VAL', cur_pos + step)

    def soller_theta_down_btn_clicked(self):
        self.widget.enable_controls(False)
        self.widget.status_txt.setText('Rotating')
        step = float(str(self.widget.soller_theta_step_txt.text()))
        center_offset = float(str(self.widget.center_offset_txt.text()))
        theta_offset = float(str(self.widget.theta_offset_txt.text()))

        QtWidgets.QApplication.processEvents()
        perform_rotation_trajectory_corrected(center_offset=center_offset,
                                              rotation_time=step * 2,
                                              angle=-step,
                                              theta_offset=theta_offset)
        self.widget.enable_controls(True)
        self.widget.status_txt.setText('')

    def soller_theta_up_btn_clicked(self):
        self.widget.enable_controls(False)
        self.widget.status_txt.setText('Rotating')

        step = float(str(self.widget.soller_theta_step_txt.text()))
        center_offset = float(str(self.widget.center_offset_txt.text()))
        theta_offset = float(str(self.widget.theta_offset_txt.text()))

        QtWidgets.QApplication.processEvents()
        perform_rotation_trajectory_corrected(center_offset=center_offset,
                                              rotation_time=step * 2,
                                              angle=step,
                                              theta_offset=theta_offset)
        self.widget.enable_controls(True)
        self.widget.status_txt.setText('')

    def soller_x_pos_changed(self):
        new_value = float(str(self.widget.soller_x_pos_txt.text()))
        caput(epics_config['x'] + '.VAL', new_value)

    def soller_z_pos_changed(self):
        new_value = float(str(self.widget.soller_z_pos_txt.text()))
        print(new_value)
        caput(epics_config['z'] + '.VAL', new_value)

    def detector_pv_txt_changed(self):
        new_pv_name = str(self.widget.detector_pv_txt.text())
        epics_config['detector'] = new_pv_name

    def soller_theta_pos_changed(self):
        self.widget.enable_controls(False)
        self.widget.status_txt.setText('Rotating')

        cur_value = float(caget(epics_config['theta'] + '.RBV'))
        new_value = float(str(self.widget.soller_theta_pos_txt.text()))

        step = new_value - cur_value

        center_offset = float(str(self.widget.center_offset_txt.text()))
        theta_offset = float(str(self.widget.theta_offset_txt.text()))

        print(cur_value, new_value, step, center_offset, theta_offset)
        perform_rotation_thread = Thread(target=perform_rotation_trajectory_corrected,
                                         kwargs={"center_offset": center_offset,
                                                 "rotation_time": abs(step) * 2,
                                                 "angle": step,
                                                 "theta_offset": theta_offset})

        perform_rotation_thread.start()
        while perform_rotation_thread.isAlive():
            QtWidgets.QApplication.processEvents()
            time.sleep(0.01)

        self.widget.enable_controls(True)
        self.widget.status_txt.setText('')

    def collect_btn_click(self):
        self.widget.enable_controls(False)
        self.widget.status_txt.setText('Collecting Data')

        collection_time = float(str(self.widget.collection_time_txt.text()))
        collection_angle = float(str(self.widget.collection_angle_txt.text()))
        start_angle = float(str(self.widget.start_angle_txt.text()))

        center_offset = float(str(self.widget.center_offset_txt.text()))
        theta_offset = float(str(self.widget.theta_offset_txt.text()))

        QtWidgets.QApplication.processEvents()

        collect_data_thread = Thread(target=collect_data,
                                     kwargs={"center_offset": center_offset,
                                             "collection_time": collection_time,
                                             "angle": collection_angle,
                                             "theta_offset": theta_offset,
                                             "start_angle": start_angle})
        collect_data_thread.start()

        while collect_data_thread.isAlive():
            QtWidgets.QApplication.processEvents()
            time.sleep(0.01)

        self.widget.enable_controls(True)
        self.widget.status_txt.setText('')

    def prepare_map(self):
        self.widget.enable_map_controls(False)
        self.widget.collect_map_btn.setText('Abort')
        self.widget.collect_map_btn.clicked.disconnect(self.collect_map_btn_click)
        self.widget.collect_map_btn.clicked.connect(self.abort_map)

    def cleanup_map(self):
        self.widget.status_txt.setText('')
        self.widget.enable_map_controls(True)
        self.widget.collect_map_btn.clicked.disconnect(self.abort_map)
        self.widget.collect_map_btn.clicked.connect(self.collect_map_btn_click)
        self.map_aborted = False
        self.widget.collect_map_btn.setEnabled(True)
        self.widget.collect_map_btn.setText('Collect Map')

    def abort_map(self):
        self.map_aborted = True
        self.widget.collect_map_btn.setText("Aborting")
        self.widget.collect_map_btn.setEnabled(False)

    def pv_names_valid(self):

        def pv_is_valid(pv_name):
            if pv_name == '':
                return False
            pv_value = caget(pv1)
            if pv_value is None:
                return False
            return True

        pv1 = str(self.widget.pv1_name_txt.text())
        if not pv_is_valid(pv1):
            return False

        if bool(self.widget.pv2_cb.isChecked()):
            pv2 = str(self.widget.pv2_name_txt.text())
            if not pv_is_valid(pv2):
                return False
        return True

    def collect_map_btn_click(self):
        self.prepare_map()
        QtWidgets.QApplication.processEvents()

        if not self.pv_names_valid():
            self.show_error_message_box("Invalid PV names!")
            self.cleanup_map()
            return

        sleep = float(str(self.widget.map_sleep_txt.text()))
        pv1 = str(self.widget.pv1_name_txt.text())
        pv1_pos = caget(pv1)
        pv1_min = float(str(self.widget.pv1_min_txt.text()))
        pv1_max = float(str(self.widget.pv1_max_txt.text()))
        pv1_step = float(str(self.widget.pv1_step_txt.text()))

        if pv1_step == 0:
            self.show_error_message_box("Invalid step size. \nPlease use a step size different from 0.")
            self.cleanup_map()
            return

        pv1_values = pv1_pos + np.arange(pv1_min, pv1_max+pv1_step, pv1_step)
        self.widget.pv1_num_lbl.setText('{}'.format(len(pv1_values)))

        if not bool(self.widget.pv2_cb.isChecked()):
            for ind, value in enumerate(pv1_values):
                if self.map_aborted:
                    break
                self.widget.pv1_cur_lbl.setText('{}/'.format(ind+1))
                caput(pv1, value, wait=True)
                time.sleep(0.15)
                self.collect_btn_click()
                for s in np.arange(sleep, step=0.1):
                    self.widget.status_txt.setText('Sleeping {:.1f} s'.format(sleep-s))
                    QtWidgets.QApplication.processEvents()
                    if self.map_aborted:
                        break
                    time.sleep(0.1)
            caput(pv1, pv1_pos)
        else:
            pv2 = str(self.widget.pv2_name_txt.text())
            pv2_pos = caget(pv2)
            pv2_min = float(str(self.widget.pv2_min_txt.text()))
            pv2_max = float(str(self.widget.pv2_max_txt.text()))
            pv2_step = float(str(self.widget.pv2_step_txt.text()))

            if pv2_step == 0:
                self.show_error_message_box("Invalid step size. \nPlease use a step different from 0.")
                self.cleanup_map()
                return

            pv2_values = pv2_pos + np.arange(pv2_min, pv2_max+pv2_step, pv2_step)
            self.widget.pv2_num_lbl.setText('{}'.format(len(pv2_values)))

            for pv1_ind, pv1_value in enumerate(pv1_values):
                for pv2_ind, pv2_value in enumerate(pv2_values):
                    if self.map_aborted:
                        break
                    self.widget.pv1_cur_lbl.setText('{}/'.format(pv1_ind+1))
                    self.widget.pv2_cur_lbl.setText('{}/'.format(pv2_ind+1))
                    caput(pv1, pv1_value, wait=True)
                    caput(pv2, pv2_value, wait=True)
                    time.sleep(0.15)
                    self.collect_btn_click()

                    for s in np.arange(sleep, step=0.1):
                        self.widget.status_txt.setText('Sleeping {:.1f} s'.format(sleep-s))
                        QtWidgets.QApplication.processEvents()
                        QtWidgets.QApplication.processEvents()
                        if self.map_aborted:
                            break
                        time.sleep(0.11)
            caput(pv1, pv1_pos)
            caput(pv2, pv2_pos)

        self.cleanup_map()

    def pv2_cb_toggled(self, value):
        self.widget.pv2_name_txt.setEnabled(value)
        self.widget.pv2_min_txt.setEnabled(value)
        self.widget.pv2_max_txt.setEnabled(value)
        self.widget.pv2_step_txt.setEnabled(value)

    def raise_window(self):
        self.widget.show()
        self.widget.setWindowState(self.widget.windowState() & QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.widget.activateWindow()
        self.widget.raise_()

    def show_error_message_box(self, msg):
        msg_box = QtWidgets.QMessageBox(self.widget)
        msg_box.setWindowFlags(QtCore.Qt.Tool)
        msg_box.setText(msg)
        msg_box.setIcon(QtWidgets.QMessageBox.Critical)
        msg_box.setWindowTitle('Error')
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.setDefaultButton(QtWidgets.QMessageBox.Ok)
        msg_box.exec_()

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
                'start_angle': '-22.238'
            }

        self.widget.center_offset_txt.setText(configuration['center_offset'])
        self.widget.theta_offset_txt.setText(configuration['theta_offset'])
        self.widget.detector_pv_txt.setText(configuration['detector_pv'])
        epics_config['detector'] = configuration['detector_pv']

        self.widget.collection_time_txt.setText(configuration['collection_time'])
        self.widget.collection_angle_txt.setText(configuration['collection_angle'])
        self.widget.start_angle_txt.setText(configuration['start_angle'])

    def save_configuration(self):
        writer = csv.writer(open('config.ini', 'w'))
        configuration = {
            'center_offset': str(self.widget.center_offset_txt.text()),
            'theta_offset': str(self.widget.theta_offset_txt.text()),
            'detector_pv': str(self.widget.detector_pv_txt.text()),
            'collection_time': str(self.widget.collection_time_txt.text()),
            'collection_angle': str(self.widget.collection_angle_txt.text()),
            'start_angle': str(self.widget.start_angle_txt.text())
        }
        for key, value in list(configuration.items()):
            writer.writerow([key, value])

    def close_event(self, _):
        self.save_configuration()
        QtWidgets.QApplication.closeAllWindows()
        QtWidgets.QApplication.quit()

