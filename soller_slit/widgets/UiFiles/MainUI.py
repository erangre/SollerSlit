# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        MainWidget.setObjectName("MainWidget")
        MainWidget.resize(541, 377)
        MainWidget.setMinimumSize(QtCore.QSize(0, 0))
        MainWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.gridLayout_5 = QtWidgets.QGridLayout(MainWidget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(MainWidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.soller_x_down_btn = QtWidgets.QPushButton(self.groupBox)
        self.soller_x_down_btn.setMaximumSize(QtCore.QSize(20, 16777215))
        self.soller_x_down_btn.setObjectName("soller_x_down_btn")
        self.gridLayout.addWidget(self.soller_x_down_btn, 0, 2, 1, 1)
        self.soller_x_step_txt = QtWidgets.QLineEdit(self.groupBox)
        self.soller_x_step_txt.setMaximumSize(QtCore.QSize(50, 16777215))
        self.soller_x_step_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.soller_x_step_txt.setObjectName("soller_x_step_txt")
        self.gridLayout.addWidget(self.soller_x_step_txt, 0, 3, 1, 1)
        self.soller_x_pos_txt = QtWidgets.QLineEdit(self.groupBox)
        self.soller_x_pos_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.soller_x_pos_txt.setObjectName("soller_x_pos_txt")
        self.gridLayout.addWidget(self.soller_x_pos_txt, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.soller_z_up_btn = QtWidgets.QPushButton(self.groupBox)
        self.soller_z_up_btn.setMaximumSize(QtCore.QSize(20, 16777215))
        self.soller_z_up_btn.setObjectName("soller_z_up_btn")
        self.gridLayout.addWidget(self.soller_z_up_btn, 1, 4, 1, 1)
        self.soller_z_down_btn = QtWidgets.QPushButton(self.groupBox)
        self.soller_z_down_btn.setMaximumSize(QtCore.QSize(20, 16777215))
        self.soller_z_down_btn.setObjectName("soller_z_down_btn")
        self.gridLayout.addWidget(self.soller_z_down_btn, 1, 2, 1, 1)
        self.soller_z_step_txt = QtWidgets.QLineEdit(self.groupBox)
        self.soller_z_step_txt.setMaximumSize(QtCore.QSize(50, 16777215))
        self.soller_z_step_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.soller_z_step_txt.setObjectName("soller_z_step_txt")
        self.gridLayout.addWidget(self.soller_z_step_txt, 1, 3, 1, 1)
        self.soller_z_pos_txt = QtWidgets.QLineEdit(self.groupBox)
        self.soller_z_pos_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.soller_z_pos_txt.setObjectName("soller_z_pos_txt")
        self.gridLayout.addWidget(self.soller_z_pos_txt, 1, 1, 1, 1)
        self.soller_x_up_btn = QtWidgets.QPushButton(self.groupBox)
        self.soller_x_up_btn.setMaximumSize(QtCore.QSize(20, 16777215))
        self.soller_x_up_btn.setObjectName("soller_x_up_btn")
        self.gridLayout.addWidget(self.soller_x_up_btn, 0, 4, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(MainWidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_9 = QtWidgets.QLabel(self.groupBox_3)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 0, 0, 1, 1)
        self.center_offset_txt = QtWidgets.QLineEdit(self.groupBox_3)
        self.center_offset_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.center_offset_txt.setObjectName("center_offset_txt")
        self.gridLayout_3.addWidget(self.center_offset_txt, 0, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox_3)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 1, 0, 1, 1)
        self.theta_offset_txt = QtWidgets.QLineEdit(self.groupBox_3)
        self.theta_offset_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.theta_offset_txt.setObjectName("theta_offset_txt")
        self.gridLayout_3.addWidget(self.theta_offset_txt, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox_3)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 2, 0, 1, 1)
        self.soller_theta_pos_txt = QtWidgets.QLineEdit(self.groupBox_3)
        self.soller_theta_pos_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.soller_theta_pos_txt.setObjectName("soller_theta_pos_txt")
        self.gridLayout_3.addWidget(self.soller_theta_pos_txt, 2, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.soller_theta_down_btn = QtWidgets.QPushButton(self.groupBox_3)
        self.soller_theta_down_btn.setMaximumSize(QtCore.QSize(20, 16777215))
        self.soller_theta_down_btn.setObjectName("soller_theta_down_btn")
        self.horizontalLayout.addWidget(self.soller_theta_down_btn)
        self.soller_theta_step_txt = QtWidgets.QLineEdit(self.groupBox_3)
        self.soller_theta_step_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.soller_theta_step_txt.setObjectName("soller_theta_step_txt")
        self.horizontalLayout.addWidget(self.soller_theta_step_txt)
        self.soller_theta_up_btn = QtWidgets.QPushButton(self.groupBox_3)
        self.soller_theta_up_btn.setMaximumSize(QtCore.QSize(20, 16777215))
        self.soller_theta_up_btn.setObjectName("soller_theta_up_btn")
        self.horizontalLayout.addWidget(self.soller_theta_up_btn)
        self.gridLayout_3.addLayout(self.horizontalLayout, 3, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.gridLayout_5.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.status_txt = QtWidgets.QLabel(MainWidget)
        self.status_txt.setStyleSheet("font-size: 20px; color: red;")
        self.status_txt.setText("")
        self.status_txt.setAlignment(QtCore.Qt.AlignCenter)
        self.status_txt.setObjectName("status_txt")
        self.verticalLayout.addWidget(self.status_txt)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.groupBox_2 = QtWidgets.QGroupBox(MainWidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.collection_time_txt = QtWidgets.QLineEdit(self.groupBox_2)
        self.collection_time_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.collection_time_txt.setObjectName("collection_time_txt")
        self.gridLayout_2.addWidget(self.collection_time_txt, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 2, 1, 1)
        self.detector_pv_txt = QtWidgets.QLineEdit(self.groupBox_2)
        self.detector_pv_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.detector_pv_txt.setObjectName("detector_pv_txt")
        self.gridLayout_2.addWidget(self.detector_pv_txt, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.collect_btn = QtWidgets.QPushButton(self.groupBox_2)
        self.collect_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.collect_btn.setObjectName("collect_btn")
        self.gridLayout_2.addWidget(self.collect_btn, 4, 1, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        self.collection_angle_txt = QtWidgets.QLineEdit(self.groupBox_2)
        self.collection_angle_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.collection_angle_txt.setObjectName("collection_angle_txt")
        self.gridLayout_2.addWidget(self.collection_angle_txt, 2, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 2, 2, 1, 1)
        self.start_angle_txt = QtWidgets.QLineEdit(self.groupBox_2)
        self.start_angle_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.start_angle_txt.setObjectName("start_angle_txt")
        self.gridLayout_2.addWidget(self.start_angle_txt, 3, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 3, 0, 1, 1)
        self.collect_ping_pong_btn = QtWidgets.QPushButton(self.groupBox_2)
        self.collect_ping_pong_btn.setObjectName("collect_ping_pong_btn")
        self.gridLayout_2.addWidget(self.collect_ping_pong_btn, 4, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.gridLayout_5.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(MainWidget)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.pv2_min_txt = QtWidgets.QLineEdit(self.groupBox_4)
        self.pv2_min_txt.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pv2_min_txt.sizePolicy().hasHeightForWidth())
        self.pv2_min_txt.setSizePolicy(sizePolicy)
        self.pv2_min_txt.setMaximumSize(QtCore.QSize(65, 16777215))
        self.pv2_min_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pv2_min_txt.setObjectName("pv2_min_txt")
        self.gridLayout_4.addWidget(self.pv2_min_txt, 2, 2, 1, 1)
        self.pv1_min_txt = QtWidgets.QLineEdit(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pv1_min_txt.sizePolicy().hasHeightForWidth())
        self.pv1_min_txt.setSizePolicy(sizePolicy)
        self.pv1_min_txt.setMaximumSize(QtCore.QSize(65, 16777215))
        self.pv1_min_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pv1_min_txt.setObjectName("pv1_min_txt")
        self.gridLayout_4.addWidget(self.pv1_min_txt, 1, 2, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.groupBox_4)
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.gridLayout_4.addWidget(self.label_16, 3, 3, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.gridLayout_4.addWidget(self.label_15, 0, 3, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.groupBox_4)
        self.label_18.setObjectName("label_18")
        self.gridLayout_4.addWidget(self.label_18, 3, 5, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.gridLayout_4.addWidget(self.label_14, 0, 2, 1, 1)
        self.pv2_max_txt = QtWidgets.QLineEdit(self.groupBox_4)
        self.pv2_max_txt.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pv2_max_txt.sizePolicy().hasHeightForWidth())
        self.pv2_max_txt.setSizePolicy(sizePolicy)
        self.pv2_max_txt.setMaximumSize(QtCore.QSize(65, 16777215))
        self.pv2_max_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pv2_max_txt.setObjectName("pv2_max_txt")
        self.gridLayout_4.addWidget(self.pv2_max_txt, 2, 3, 1, 1)
        self.pv1_step_txt = QtWidgets.QLineEdit(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pv1_step_txt.sizePolicy().hasHeightForWidth())
        self.pv1_step_txt.setSizePolicy(sizePolicy)
        self.pv1_step_txt.setMaximumSize(QtCore.QSize(65, 16777215))
        self.pv1_step_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pv1_step_txt.setObjectName("pv1_step_txt")
        self.gridLayout_4.addWidget(self.pv1_step_txt, 1, 4, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox_4)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout_4.addWidget(self.label_11, 0, 1, 1, 1)
        self.pv1_name_txt = QtWidgets.QLineEdit(self.groupBox_4)
        self.pv1_name_txt.setObjectName("pv1_name_txt")
        self.gridLayout_4.addWidget(self.pv1_name_txt, 1, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout_4.addWidget(self.label_13, 0, 4, 1, 1)
        self.pv2_step_txt = QtWidgets.QLineEdit(self.groupBox_4)
        self.pv2_step_txt.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pv2_step_txt.sizePolicy().hasHeightForWidth())
        self.pv2_step_txt.setSizePolicy(sizePolicy)
        self.pv2_step_txt.setMaximumSize(QtCore.QSize(65, 16777215))
        self.pv2_step_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pv2_step_txt.setObjectName("pv2_step_txt")
        self.gridLayout_4.addWidget(self.pv2_step_txt, 2, 4, 1, 1)
        self.map_sleep_txt = QtWidgets.QLineEdit(self.groupBox_4)
        self.map_sleep_txt.setMinimumSize(QtCore.QSize(50, 0))
        self.map_sleep_txt.setMaximumSize(QtCore.QSize(65, 16777215))
        self.map_sleep_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.map_sleep_txt.setObjectName("map_sleep_txt")
        self.gridLayout_4.addWidget(self.map_sleep_txt, 3, 4, 1, 1)
        self.pv1_max_txt = QtWidgets.QLineEdit(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pv1_max_txt.sizePolicy().hasHeightForWidth())
        self.pv1_max_txt.setSizePolicy(sizePolicy)
        self.pv1_max_txt.setMaximumSize(QtCore.QSize(65, 16777215))
        self.pv1_max_txt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pv1_max_txt.setObjectName("pv1_max_txt")
        self.gridLayout_4.addWidget(self.pv1_max_txt, 1, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem1, 0, 7, 1, 1)
        self.pv2_name_txt = QtWidgets.QLineEdit(self.groupBox_4)
        self.pv2_name_txt.setEnabled(False)
        self.pv2_name_txt.setObjectName("pv2_name_txt")
        self.gridLayout_4.addWidget(self.pv2_name_txt, 2, 1, 1, 1)
        self.collect_map_btn = QtWidgets.QPushButton(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.collect_map_btn.sizePolicy().hasHeightForWidth())
        self.collect_map_btn.setSizePolicy(sizePolicy)
        self.collect_map_btn.setObjectName("collect_map_btn")
        self.gridLayout_4.addWidget(self.collect_map_btn, 1, 7, 3, 1)
        self.pv1_cur_lbl = QtWidgets.QLabel(self.groupBox_4)
        self.pv1_cur_lbl.setObjectName("pv1_cur_lbl")
        self.gridLayout_4.addWidget(self.pv1_cur_lbl, 1, 5, 1, 1)
        self.pv2_cb = QtWidgets.QCheckBox(self.groupBox_4)
        self.pv2_cb.setText("")
        self.pv2_cb.setChecked(False)
        self.pv2_cb.setObjectName("pv2_cb")
        self.gridLayout_4.addWidget(self.pv2_cb, 2, 0, 1, 1)
        self.pv2_cur_lbl = QtWidgets.QLabel(self.groupBox_4)
        self.pv2_cur_lbl.setObjectName("pv2_cur_lbl")
        self.gridLayout_4.addWidget(self.pv2_cur_lbl, 2, 5, 1, 1)
        self.pv1_num_lbl = QtWidgets.QLabel(self.groupBox_4)
        self.pv1_num_lbl.setObjectName("pv1_num_lbl")
        self.gridLayout_4.addWidget(self.pv1_num_lbl, 1, 6, 1, 1)
        self.pv2_num_lbl = QtWidgets.QLabel(self.groupBox_4)
        self.pv2_num_lbl.setObjectName("pv2_num_lbl")
        self.gridLayout_4.addWidget(self.pv2_num_lbl, 2, 6, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_4, 1, 0, 1, 2)

        self.retranslateUi(MainWidget)
        QtCore.QMetaObject.connectSlotsByName(MainWidget)

    def retranslateUi(self, MainWidget):
        _translate = QtCore.QCoreApplication.translate
        MainWidget.setWindowTitle(_translate("MainWidget", "Form"))
        self.groupBox.setTitle(_translate("MainWidget", "Soller Slit Position"))
        self.soller_x_down_btn.setText(_translate("MainWidget", "<"))
        self.soller_x_step_txt.setText(_translate("MainWidget", "0.01"))
        self.soller_x_pos_txt.setText(_translate("MainWidget", "0.000"))
        self.label_2.setText(_translate("MainWidget", "Soller Z:"))
        self.soller_z_up_btn.setText(_translate("MainWidget", ">"))
        self.soller_z_down_btn.setText(_translate("MainWidget", "<"))
        self.soller_z_step_txt.setText(_translate("MainWidget", "0.01"))
        self.soller_z_pos_txt.setText(_translate("MainWidget", "0.000"))
        self.soller_x_up_btn.setText(_translate("MainWidget", ">"))
        self.label.setText(_translate("MainWidget", "Soller X:"))
        self.groupBox_3.setTitle(_translate("MainWidget", "Rotation"))
        self.label_9.setText(_translate("MainWidget", "Center Offset:"))
        self.label_10.setText(_translate("MainWidget", "Theta Offset:"))
        self.label_8.setText(_translate("MainWidget", "Soller Theta:"))
        self.soller_theta_down_btn.setText(_translate("MainWidget", "<"))
        self.soller_theta_step_txt.setText(_translate("MainWidget", "5"))
        self.soller_theta_up_btn.setText(_translate("MainWidget", ">"))
        self.groupBox_2.setTitle(_translate("MainWidget", "Data Collection"))
        self.label_5.setText(_translate("MainWidget", "s"))
        self.label_4.setText(_translate("MainWidget", "Collection time:"))
        self.collect_btn.setText(_translate("MainWidget", "Collect"))
        self.label_3.setText(_translate("MainWidget", "Detector PV:"))
        self.label_6.setText(_translate("MainWidget", "Angle:"))
        self.label_7.setText(_translate("MainWidget", "°"))
        self.label_12.setText(_translate("MainWidget", "Start Angle:"))
        self.collect_ping_pong_btn.setText(_translate("MainWidget", "Ping Pong"))
        self.groupBox_4.setTitle(_translate("MainWidget", "Mapping"))
        self.pv2_min_txt.setText(_translate("MainWidget", "-0.01"))
        self.pv1_min_txt.setText(_translate("MainWidget", "-0.01"))
        self.label_16.setText(_translate("MainWidget", "Sleep:"))
        self.label_15.setText(_translate("MainWidget", "max"))
        self.label_18.setText(_translate("MainWidget", "s"))
        self.label_14.setText(_translate("MainWidget", "min"))
        self.pv2_max_txt.setText(_translate("MainWidget", "0.01"))
        self.pv1_step_txt.setText(_translate("MainWidget", "0.005"))
        self.label_11.setText(_translate("MainWidget", "PV name"))
        self.label_13.setText(_translate("MainWidget", "step"))
        self.pv2_step_txt.setText(_translate("MainWidget", "0.005"))
        self.map_sleep_txt.setToolTip(_translate("MainWidget", "<html><head/><body><p>Time to wait between each collection (especially useful for MarIP).</p></body></html>"))
        self.map_sleep_txt.setText(_translate("MainWidget", "0"))
        self.pv1_max_txt.setText(_translate("MainWidget", "0.01"))
        self.collect_map_btn.setText(_translate("MainWidget", "Collect Map"))
        self.pv1_cur_lbl.setText(_translate("MainWidget", "0"))
        self.pv2_cur_lbl.setText(_translate("MainWidget", "0"))
        self.pv1_num_lbl.setText(_translate("MainWidget", "0"))
        self.pv2_num_lbl.setText(_translate("MainWidget", "0"))

