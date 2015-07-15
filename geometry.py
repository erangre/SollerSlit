__author__ = 'Clemens Prescher'

import numpy as np


def get_xz_position_rel(center_offset, theta):
    x = center_offset * np.sin(theta)
    c_sqr = (2 * (center_offset ** 2) * (1 - np.cos(theta)))
    z = np.sqrt(c_sqr - x ** 2)
    return x, z


def get_xz_offset(center_offset, cur_theta, theta_step):
    current_pos = get_xz_position_rel(center_offset, cur_theta)
    new_pos = get_xz_position_rel(center_offset, cur_theta + theta_step)
    return np.array(new_pos) - np.array(current_pos)


def get_xz_position_abs(center_offset, theta, zero_pos):
    pos_offset = get_xz_offset(center_offset, 0, theta)
    new_pos = np.array(zero_pos) + np.array(pos_offset)
    return new_pos



