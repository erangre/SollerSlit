__author__ = 'gpd_user'

from epics import caget, caput, PV, camonitor

print(caget('13IDD:m95.VAL'))

caput('13IDD:m95.VELO', 1)
caput('13IDD:m95.VAL', 2, wait=True)

print(caget('13IDD:m95.VELO'))
caput('13IDD:m95.VELO', 0.1)
print(caget('13IDD:m95.VELO'))


omega_val = PV('13IDD:m95.VAL')


def get_value(val):
    print(val)


camonitor('13IDD:m95.VAL')

caput('13IDD:m95.VAL', 1, wait=True)
caput('13IDD:m95.VAL', 1.1, wait=True)
print('process finished')

