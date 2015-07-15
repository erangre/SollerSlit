__author__ = 'Clemens Prescher'
import time

from epics import caput, caget
import numpy as np

from soller_slit.circular_move import collect_data

if __name__ == '__main__':
    scan_pv = '13IDD:m96'
    scan_range = .8
    scan_steps = 17
    collection_time = 150

    pv_pos = caget(scan_pv)

    pv_scan_positions = np.linspace(pv_pos-scan_range, pv_pos+scan_range, scan_steps)
    # pv_scan_positions = [-100.1, -100.1, -99., -90., -90.]

    for pv_scan_position in pv_scan_positions:
        caput(scan_pv, pv_scan_position, wait=True)
        collect_data(center_offset=35.73,
                     collection_time=collection_time,
                     angle=3.195,
                     theta_offset=-1.5)
        time.sleep(110)

    caput(scan_pv, pv_pos, wait=True)