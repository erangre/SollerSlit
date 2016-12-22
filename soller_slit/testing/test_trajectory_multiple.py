__author__ = 'gpd_user'

from soller_slit.xps_trajectory.xps_trajectory import XPSTrajectory

HOST = '164.54.160.34'
GROUP_NAME = 'G2'
POSITIONERS = "SLZ SLX SLT"

GATHER_OUTPUTS = ('CurrentPosition', 'FollowingError',
                  'SetpointPosition', 'CurrentVelocity')

soller_xps = XPSTrajectory(host=HOST, group=GROUP_NAME, positioners=POSITIONERS)
# print(XPSTrajectory.pvt_template % soller_xps.DefineLineTrajectories())

print(soller_xps.define_line_trajectories_soller_multiple_motors(stop_values=([0.5, 0.5, 0.1], [0.6, 0.7, 1]),
                                                      scan_time=10.0))

soller_xps.run_line_trajectory_soller()
