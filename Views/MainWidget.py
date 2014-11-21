__author__ = 'DAC_User'
from UiFiles.MainUI import Ui_MainWidget

from PyQt4 import QtGui, QtCore


class MainWidget(QtGui.QWidget, Ui_MainWidget):
    def __init__(self, title=''):
        super(MainWidget, self).__init__(None)
        self.setupUi(self)
        self.set_validator()
        self.setWindowTitle(title)

    def set_validator(self):
        self.theta_offset_txt.setValidator(QtGui.QDoubleValidator())
        self.center_offset_txt.setValidator(QtGui.QDoubleValidator())

        self.soller_x_pos_txt.setValidator(QtGui.QDoubleValidator())
        self.soller_z_pos_txt.setValidator(QtGui.QDoubleValidator())
        self.soller_theta_pos_txt.setValidator(QtGui.QDoubleValidator())

        self.soller_x_step_txt.setValidator(QtGui.QDoubleValidator())
        self.soller_z_step_txt.setValidator(QtGui.QDoubleValidator())
        self.soller_theta_step_txt.setValidator(QtGui.QDoubleValidator())

        self.collection_time_txt.setValidator(QtGui.QDoubleValidator())
        self.collection_angle_txt.setValidator(QtGui.QDoubleValidator())

    def update_motor_values(self, soller_x, soller_z, soller_theta):
        if soller_x is not None:
            if not self.soller_x_pos_txt.hasFocus():
                self.soller_x_pos_txt.setText("{:.3f}".format(float(soller_x)))
        if soller_z is not None:
            if not self.soller_z_pos_txt.hasFocus():
                self.soller_z_pos_txt.setText("{:.3f}".format(float(soller_z)))
        if soller_theta is not None:
            if not self.soller_theta_pos_txt.hasFocus():
                self.soller_theta_pos_txt.setText("{:.3f}".format(float(soller_theta)))

    def enable_controls(self, bool_value):
        self.soller_x_pos_txt.setEnabled(bool_value)
        self.soller_z_pos_txt.setEnabled(bool_value)
        self.soller_theta_pos_txt.setEnabled(bool_value)

        self.soller_x_down_btn.setEnabled(bool_value)
        self.soller_x_up_btn.setEnabled(bool_value)

        self.soller_z_down_btn.setEnabled(bool_value)
        self.soller_z_up_btn.setEnabled(bool_value)

        self.soller_theta_down_btn.setEnabled(bool_value)
        self.soller_theta_up_btn.setEnabled(bool_value)

        self.collect_btn.setEnabled(bool_value)
