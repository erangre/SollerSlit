__author__ = 'gpd_user'

import numpy as np
zero_x = 22.69
zero_z = 18.08

rot_x = 19.319
rot_z = 18.079

delta_x = zero_x-rot_x
delta_z = zero_z-rot_z
angle = 5/180.0*np.pi
print(delta_x/np.arcsin(5/180.0*np.pi))
print(delta_z/np.sqrt(2*(1-np.cos(angle))-np.cos(angle)**2))