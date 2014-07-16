__author__ = 'gpd_user'

import numpy as np
import matplotlib.pyplot as plt


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


def test1():
    d = 36  # mm
    theta = np.linspace(0, 360)
    theta = theta / 180 * np.pi
    x, y = get_xz_position_rel(d, theta)
    print x, y
    plt.plot(x, y)
    plt.xlabel('x_movement')
    plt.ylabel('y_movement')
    plt.figure()
    theta = theta / np.pi * 180
    plt.plot(theta, x)
    plt.plot(theta, y)
    plt.show()


if __name__ == '__main__':
    # test1()
    d = 36  # mm
    theta = np.linspace(0, 360)
    theta = theta / 180 * np.pi
    positions = []
    for val in theta:
        positions.append(get_xz_position_abs(36, val, (0, 0)))
    positions = np.array(positions)
    plt.plot(positions[:, 0], positions[:, 1])
    plt.show()


