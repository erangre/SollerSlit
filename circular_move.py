__author__ = 'gpd_user'

from geometry import get_xz_offset, get_xz_position_rel
from xps_trajectory.xps_trajectory import XPSTrajectory
import numpy as np
from threading import Thread, Timer
from epics import caput, caget
import time
import matplotlib.pyplot as plt

HOST = '164.54.160.34'
GROUP_NAME = 'G2'
POSITIONERS = "SLZ SLX SLT"

GATHER_OUTPUTS = ('CurrentPosition', 'FollowingError',
                  'SetpointPosition', 'CurrentVelocity')


def perform_rotation(center_offset, angle, theta_offset=0.0):
    old_theta = caget('13IDD:m95.RBV')
    old_x = caget('13IDD:m93.RBV')
    old_z = caget('13IDD:m94.RBV')

    offset = get_xz_offset(center_offset, (old_theta+theta_offset) / 180.0 * np.pi, angle / 180.0 * np.pi)

    new_theta = old_theta + angle
    new_x = old_x + offset[0]
    new_z = old_z + offset[1]

    caput('13IDD:m95.VAL', new_theta)
    caput('13IDD:m93.VAL', new_x)
    caput('13IDD:m94.VAL', new_z)


def perform_rotation_trajectory(center_offset, rotation_time, angle, theta_offset=0.0):
    old_theta = caget('13IDD:m95.RBV')

    theta = (old_theta+theta_offset) / 180. * np.pi
    angle = angle / 180.0 * np.pi

    soller_xps = XPSTrajectory(host=HOST, group=GROUP_NAME, positioners=POSITIONERS)

    angle_steps = np.linspace(0, angle, 101)
    angle_steps = angle_steps[1:]

    stop_values = []
    for angle_step in angle_steps:
        offset = get_xz_offset(center_offset, theta, angle_step)
        stop_values.append([offset[1], offset[0], angle_step / np.pi * 180.0])

    # offset = get_xz_offset(center_offset, theta, angle)
    # soller_xps.DefineLineTrajectoriesSoller(stop_values=(-offset[1], offset[0], angle),
    # scan_time=rotation_time)

    soller_xps.DefineLineTrajectoriesSollerMultiple(stop_values=stop_values,
                                                    scan_time=rotation_time)

    print "start trajectory scan"
    soller_xps.RunLineTrajectorySoller()
    print "finished trajectory scan"
    soller_xps.ftp_disconnect()
    del soller_xps


def perform_rotation_trajectory_corrected(center_offset, rotation_time, angle, theta_offset=0.0):

    #obtain current position
    old_theta = caget('13IDD:m95.RBV')
    old_x = caget('13IDD:m93.RBV')
    old_z = caget('13IDD:m94.RBV')

    offset = get_xz_offset(center_offset, (old_theta+theta_offset) / 180.0 * np.pi, angle / 180.0 * np.pi)

    new_theta = old_theta + angle
    new_x = old_x + offset[0]
    new_z = old_z + offset[1]

    #do a trajectory
    perform_rotation_trajectory(center_offset, rotation_time, angle, theta_offset=0.0)

    #correct for the trajectory overshoot
    caput('13IDD:m94.VAL', new_z, wait=True)
    caput('13IDD:m93.VAL', new_x, wait=True)
    caput('13IDD:m95.VAL', new_theta, wait=True)


def collect_data(center_offset, collection_time, angle, time_offset=5.0, theta_offset=0.0, back_rotation_time=10.0):
    old_theta = caget('13IDD:m95.RBV')
    old_x = caget('13IDD:m93.RBV')
    old_z = caget('13IDD:m94.RBV')

    # create parameters for trajectory scan
    rotation_time = collection_time + time_offset
    rotation_angle = float(rotation_time) / float(collection_time) * angle

    # create the timer for data_collection
    t = Timer(time_offset / 2.0, start_detector, args=(collection_time,))
    t.start()

    print 'SOLLER: rotation trajectory START'
    perform_rotation_trajectory(center_offset, rotation_time, rotation_angle, theta_offset=theta_offset)
    print 'SOLLER: rotation trajectory FINISHED'

    print 'SOLLER: moving to original position'
    print ' --performing backwards trajectory'
    perform_rotation_trajectory(center_offset, back_rotation_time, -rotation_angle)

    print ' --moving motors to starting position'
    caput('13IDD:m94.VAL', old_z, wait=False)
    caput('13IDD:m93.VAL', old_x, wait=False)
    caput('13IDD:m95.VAL', old_theta, wait=True)
    print 'SOLLER: movement FINISHED'


def start_detector(exposure_time):
    print "DETECTOR: data collection START"
    # detector = '13MARCCD2:cam1'
    detector = '13MAR345_2:cam1'
    caput(detector+':AcquireTime', exposure_time)
    caput(detector+':Acquire', 1, wait=True)
    print "DETECTOR: data collection FINISHED"


if __name__ == '__main__':
    # perform_rotation(35.65, 20, -0.33)

    collect_data(center_offset=35.65,
                 collection_time=60,
                 angle=3.19,
                 theta_offset=-0.33)

    # perform_rotation_trajectory_corrected(center_offset=35.65,
    #                                       rotation_time=10,
    #                                       angle=17,
    #                                       theta_offset=-0.33)


    # # for dummy_ind in range(num_of_collections):
    # #     collect_data(35.3, collection_time, collection_angle)
    # #     time.sleep(5)