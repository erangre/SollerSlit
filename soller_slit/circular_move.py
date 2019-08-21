__author__ = 'gpd_user'

from threading import Timer
import time
import numpy as np
from epics import caput, caget
from geometry import get_xz_offset
from xps_trajectory.xps_trajectory import XPSTrajectory
from config import xps_config, epics_config, prior_collect, after_collect, values

HOST = xps_config['HOST']
GROUP_NAME = xps_config['GROUP NAME']
POSITIONERS = xps_config['POSITIONERS']

GATHER_OUTPUTS = xps_config['GATHER OUTPUTS']


def get_position():
    """
    Gets the current Soller Slit position
    :return: tuple with x,z,theta as values
    """
    x = None
    z = None
    theta = None
    while x is None:
        x = caget(epics_config['x'] + '.RBV')
    while z is None:
        z = caget(epics_config['z'] + '.RBV')
    while theta is None:
        theta = caget(epics_config['theta'] + '.RBV')
    print(x, z, theta)
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


def perform_rotation(angle, center_offset, theta_offset=0.0, wait=False):
    old_x, old_z, old_theta = get_position()

    offset = get_xz_offset(center_offset, (old_theta + theta_offset) / 180.0 * np.pi, angle / 180.0 * np.pi)

    new_theta = old_theta + angle
    new_x = old_x + offset[0]
    new_z = old_z + offset[1]

    set_position(new_x, new_z, new_theta, wait=wait)


def move_to_theta(new_theta, center_offset, theta_offset=0.0, wait=False):
    # obtain current position
    old_x, old_z, old_theta = get_position()

    angle = new_theta - old_theta
    offset = get_xz_offset(center_offset, (old_theta + theta_offset) / 180.0 * np.pi, angle / 180.0 * np.pi)

    new_x = old_x + offset[0]
    new_z = old_z + offset[1]

    # correct for the trajectory overshoot
    set_position(new_x, new_z, new_theta, wait=True)


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
    old_theta = caget(epics_config['theta'] + '.RBV')

    while old_theta is None:  # sometimes it gets None and the program breaks...
        time.sleep(0.1)
        old_theta = caget(epics_config['theta'] + '.RBV')

    print(old_theta)
    print(theta_offset)
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

    print("start trajectory scan")
    soller_xps.run_line_trajectory_soller()
    print("finished trajectory scan")
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


def collect_data(center_offset, collection_time, angle, time_offset=10.0, theta_offset=0.0, back_rotation_time=10.0,
                 start_angle=-22.238):
    # do the prior collect movements
    for key, val in prior_collect.items():
        if key == "sleep":
            time.sleep(val)
        else:
            if key == '13IDD:Unidig2Bo5' and caget(epics_config['ds_mirror_position']) > -110.0:
                continue
            else:
                caput(key, val)

    # get old position
    old_x, old_z, old_theta = get_position()

    # move to start angle
    if not np.isclose(old_theta, start_angle):
        print('Moving to correct start angle: {}'.format(start_angle))
        move_to_theta(start_angle, center_offset, theta_offset, wait=True)

    # create parameters for trajectory scan
    rotation_time = collection_time + time_offset
    rotation_angle = float(rotation_time) / float(collection_time) * angle

    # create the timer for data_collection
    t = Timer(4, start_detector, args=(collection_time,))
    t.start()

    print('SOLLER: rotation trajectory START')
    perform_rotation_trajectory(center_offset, rotation_time, rotation_angle, theta_offset=theta_offset)
    print('SOLLER: rotation trajectory FINISHED')

    print('SOLLER: moving to original position')
    print(' --performing backwards trajectory')
    perform_rotation_trajectory(center_offset, back_rotation_time, -rotation_angle)

    time.sleep(0.5)
    print(' --moving motors to starting position')
    set_position(old_x, old_z, old_theta, wait=True)
    print('SOLLER: movement FINISHED')

    for key, val in after_collect.items():
        caput(key, val)


def collect_data_ping_pong(center_offset, collection_time, angle, theta_offset=0.0, start_angle=-22.238,
                           update_function=None, parent=None, wait_for_injection=True):
    detector = epics_config['detector']
    # do the prior collect movements

    ping_time = values['time_per_ping']

    for key, val in prior_collect.items():
        if key == "sleep":
            time.sleep(val)
        else:
            if key == '13IDD:Unidig2Bo5' and caget(epics_config['ds_mirror_position']) > -110.0:
                continue
            else:
                caput(key, val)

    # get old position
    old_x, old_z, old_theta = get_position()

    # move to start angle
    if not np.isclose(old_theta, start_angle):
        print('Moving to correct start angle: {}'.format(start_angle))
        move_to_theta(start_angle, center_offset, theta_offset, wait=True)

    old_shutter_mode = caget(detector + ':ShutterMode')
    caput(detector + ':ShutterMode', 0, wait=True)

    n = collection_time // (2*ping_time)

    print('SOLLER: rotation trajectory START')
    for i in range(int(n)):
        if parent.abort_btn_pressed:
            while caget('13PIL300K:Proc1:NumFiltered_RBV') < caget('13PIL300K:Proc1:NumFilter_RBV'):
                caput('13PIL300K:Proc1:ProcessPlugin', 1, wait=True)
            # caput('13PIL300K:TIFF1:ProcessPlugin', 1, wait=True)
            # caput('13PIL300K:TIFF1:WriteFile', 1, wait=True)
            caput('13PIL300K:cam1:Acquire', 0, wait=True)
            set_position(old_x, old_z, old_theta, wait=True)
            print('SOLLER: movement ABORTED. returning to origin')
            if update_function is not None:
                update_function("Aborted before " + str(i + 1) + '/' + str(int(n)))
            return
        if wait_for_injection:
            check_for_injection_and_wait(update_function, ping_time)
        if update_function is not None:
            update_function("Collect ping " + str(i + 1) + '/' + str(int(n)))
        print("ping " + str(i + 1) + ' of ' + str(int(n)))
        perform_rotation_trajectory(center_offset, ping_time, angle, theta_offset=theta_offset)
        time.sleep(0.1)

        if wait_for_injection:
            check_for_injection_and_wait(update_function, ping_time)
        if update_function is not None:
            update_function("Collect pong " + str(i + 1) + '/' + str(int(n)))
        print("pong " + str(i + 1) + ' of ' + str(int(n)))
        perform_rotation_trajectory(center_offset, ping_time, -angle, theta_offset=theta_offset)
    print('SOLLER: rotation trajectory FINISHED')
    time.sleep(0.1)

    print(' --moving motors to starting position')
    set_position(old_x, old_z, old_theta, wait=True)
    print('SOLLER: movement FINISHED')

    # update_function('Reading Detector')
    # start_detector(1)

    for key, val in after_collect.items():
        caput(key, val)

    caput(detector + ':ShutterMode', old_shutter_mode)


def check_for_injection_and_wait(update_function, ping_time):
    time_to_next_injection = caget("Mt:TopUpTime2Inject.VAL")
    if time_to_next_injection < ping_time+1:
        if update_function is not None:
            update_function("Waiting for injection")
        time.sleep(time_to_next_injection + 3)


def start_detector(exposure_time):
    print("DETECTOR: data collection START")
    detector = epics_config['detector']

    time.sleep(1.5)  # wait for completion

    caput(detector + ':AcquireTime', exposure_time)
    print("DETECTOR: START Aquiring")
    caput(detector + ':Acquire', 1, wait=True, timeout=99999999)
    print("DETECTOR: data collection FINISHED")


if __name__ == '__main__':
    # # perform_rotation(35.65, 20, -0.33)

    caput('13IDD:m96', -100.7, wait=True)

    cur_pos_m83 = caget('13IDD:m83')
    caput('13IDD:m83', cur_pos_m83 - 0.010)

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
