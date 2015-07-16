__author__ = 'Clemens Prescher'

# This file defines the configuration for the soller slit device:

# xps_config contains ip address and the mote groupnames with specific positioners positioners should be in the order
# Z X Theta
xps_config = {
    'HOST': '164.54.160.34',
    'PORT': 5001,
    'TIMEOUT': 10,
    'GROUP NAME': 'G2',
    'POSITIONERS': "SLZ SLX SLT",
    'USER': 'Administrator',
    'PASSWORD': 'Administrator',
    'TRAJ_FOLDER': 'Public/trajectories',
    'GATHER TITLES': "# XPS Gathering Data\n#--------------",
    'GATHER OUTPUTS': ('CurrentPosition', 'FollowingError',
                       'SetpointPosition', 'CurrentVelocity'),
    'DEFAULT ACCEL':  {'z': 10.0, 'x': 10.0, 't': 2.0},
}


# epics_config defines the to the xps corresponding epics pv names
epics_config = {
    'theta':    '13IDD:m95',
    'x':        '13IDD:m93',
    'z':        '13IDD:m94',
    'detector': '13MARCCD2:cam1'
}

# prior_collect is a dictionary where you can set specific PV's to certain values prior to measurement. This can be used
# to e.g. move beamstop in or photodiode out prior to every measurement

prior_collect = {
    '13IDD:Unidig2Bo5': 0,  # move in beamstop
    '13IDD:Unidig1Bo9': 1,  # move out photo diode
    'sleep': 10,
}

after_collect = {
    '13IDD:Unidig1Bo9': 0,  # move out photo diode
}



