__author__ = 'gpd_user'

from threading import Timer
import time

import numpy as np
from epics import caput, caget

from geometry import get_xz_offset
from soller_slit.xps_trajectory.xps_trajectory import XPSTrajectory
from config import xps_config, epics_config, prior_collect, after_collect

HOST = xps_config['HOST']
GROUP_NAME = xps_config['GROUP NAME']
POSITIONERS = xps_config['POSITIONERS']

GATHER_OUTPUTS = xps_config['GATHER OUTPUTS']


def get_position():
    """
    Gets the current Soller Slit position
    :return: tuple with x,z,theta as values
    """
    x = caget(epics_config['x']+'.RBV')
    z = caget(epics_config['z']+'.RBV')
    theta = caget(epics_config['theta']+'.RBV')
    return x, z, theta


def set_position(x, z, theta, wait=True):
    """
    Sets the soller slit position to x, z and y
    :param x: new x position
    :param z: new y position
    :param theta: new theta position
    :param wait: whether or not to wait for each individual movement and then only proceed with the next motor
    """

    caput(epics_config['z'], z, wait=False)
    caput(epics_config['x'], x, wait=False)
    caput(epics_config['theta'], theta, wait=wait)


def perform_rotation(center_offset, angle, theta_offset=0.0):
    old_x, old_z, old_theta = get_position()

    offset = get_xz_offset(center_offset, (old_theta + theta_offset) / 180.0 * np.pi, angle / 180.0 * np.pi)

    new_theta = old_theta + angle
    new_x = old_x + offset[0]
    new_z = old_z + offset[1]

    set_position(new_x, new_z, new_theta, wait=False)


def perform_rotation_trajectory(center_offset, rotation_time, angle, theta_offset=0.0):
    """
    Performs a rotation of the soller slit using XPS trajectory. However this does not correct for the
    deceleration offset after the movement, therefore the end position will not be at the correct position.
    perform_rotation_trajectory_corrected is the function which will correct for that
    :param center_offset:
    :param rotation_time:
    :param angle:
    :param theta_offset:
    :return:
    """
    old_theta = caget(epics_config['theta']+'.RBV')

    theta = (old_theta + theta_offset) / 180. * np.pi
    angle = angle / 180.0 * np.pi

    soller_xps = XPSTrajectory(host=HOST, group=GROUP_NAME, positioners=POSITIONERS)

    angle_steps = np.linspace(0, angle, rotation_time * 30)
    angle_steps = angle_steps[1:]

    stop_values = []
    for angle_step in angle_steps:
        offset = get_xz_offset(center_offset, theta, angle_step)
        stop_values.append([offset[1], offset[0], angle_step / np.pi * 180.0])

    soller_xps.define_line_trajectories_soller_multiple_motors(stop_values=stop_values,
                                                    scan_time=rotation_time)

    print "start trajectory scan"
    soller_xps.run_line_trajectory_soller()
    print "finished trajectory scan"
    soller_xps.ftp_disconnect()
    del soller_xps


def perform_rotation_trajectory_corrected(center_offset, rotation_time, angle, theta_offset=0.0):
    # obtain current position
    old_x, old_z, old_theta = get_position()

    offset = get_xz_offset(center_offset, (old_theta + theta_offset) / 180.0 * np.pi, angle / 180.0 * np.pi)

    new_theta = old_theta + angle
    new_x = old_x + offset[0]
    new_z = old_z + offset[1]

    # do a trajectory
    perform_rotation_trajectory(center_offset, rotation_time, angle, theta_offset=theta_offset)

    # correct for the trajectory overshoot
    set_position(new_x, new_z, new_theta, wait=True)


def collect_data(center_offset, collection_time, angle, time_offset=5.0, theta_offset=0.0, back_rotation_time=10.0):
    # do the prior collect movements
    for key, val in prior_collect.iteritems():
        if key == "sleep":
            time.sleep(val)
        else:
            caput(key, val)

    # get old position
    old_x, old_z, old_theta = get_position()

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

    time.sleep(0.5)
    print ' --moving motors to starting position'
    set_position(old_x, old_z, old_theta, wait=True)
    print 'SOLLER: movement FINISHED'

    for key, val in after_collect.iteritems():
        caput(key, val)


def start_detector(exposure_time):
    print "DETECTOR: data collection START"
    detector = epics_config['detector']

    time.sleep(1.5) # wait for completion

    caput(detector + ':AcquireTime', exposure_time)
    caput(detector + ':Acquire', 1, wait=True, timeout=99999999)
    print "DETECTOR: data collection FINISHED"


if __name__ == '__main__':
    # # perform_rotation(35.65, 20, -0.33)

    caput('13IDD:m96', -100.7, wait=True)

    cur_pos_m83 = caget('13IDD:m83')
    caput('13IDD:m83', cur_pos_m83-0.010)

    collect_data(center_offset=35.65,
                 collection_time=300,
                 angle=3.205,  # 3.205
                 theta_offset=-0.33)

    caput('13IDD:m83', cur_pos_m83)
    time.sleep(110)
    collect_data(center_offset=35.65,
                 collection_time=300,
                 angle=3.205,  # 3.205
                 theta_offset=-0.33)
