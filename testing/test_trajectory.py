__author__ = 'gpd_user'

from xps_trajectory.xps_trajectory import XPSTrajectory

HOST = '164.54.160.34'
GROUP_NAME = 'G2'
POSITIONERS = "SLZ SLX SLT"

GATHER_OUTPUTS = ('CurrentPosition', 'FollowingError',
                  'SetpointPosition', 'CurrentVelocity')

soller_xps = XPSTrajectory(host=HOST, group=GROUP_NAME, positioners=POSITIONERS)
# print XPSTrajectory.pvt_template % soller_xps.DefineLineTrajectories()

print XPSTrajectory.zxt_template % soller_xps.DefineLineTrajectoriesSoller(stop_values=(2, .1, 1),
                                                                           scan_time=1, step=0.001)

soller_xps.RunLineTrajectorySoller()