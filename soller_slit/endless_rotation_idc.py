__author__ = 'DAC_User'


from epics import caput
import sys


while True:
    caput('13IDC:m25', -30, wait=True, timeout=100000)
    caput('13IDC:m25',  60, wait=True, timeout=100000)