__author__ = 'DAC_User'
from circular_move import collect_data
from epics import caput, caget
import numpy as np
import time

if __name__ == '__main__':
    scan_pv = '13IDD:m93'
    scan_range = 0.05
    scan_steps = 11
    collection_time = 30

    pv_pos = caget(scan_pv)

    pv_scan_positions = np.linspace(pv_pos-scan_range, pv_pos+scan_range, scan_steps)

    for pv_scan_position in pv_scan_positions:
        caput(scan_pv, pv_scan_position, wait=True)
        collect_data(center_offset=35.65,
                     collection_time=collection_time,
                     angle=3.19,
                     theta_offset=-0.33)
        time.sleep(110)

    caput(scan_pv, pv_pos, wait=True)