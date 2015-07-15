import time
import numpy as np
import ftplib
from cStringIO import StringIO
from XPS_C8_drivers import XPS

from config import xps_config


class XPSTrajectory(object):
    pvt_template = """
%(ramptime)f, %(xramp)f, %(xvelo)f, %(yramp)f, %(yvelo)f, %(tramp)f, %(tvelo)f
%(scantime)f, %(xdist)f, %(xvelo)f, %(ydist)f, %(yvelo)f, %(tdist)f, %(tvelo)f
%(ramptime)f, %(xramp)f, %(xzero)f, %(yramp)f, %(xzero)f, %(tramp)f, %(xzero)f
"""

    zxt_template = """
%(ramptime)f, %(zramp)f, %(zvelo)f, %(xramp)f, %(xvelo)f, %(tramp)f, %(tvelo)f
%(scantime)f, %(zdist)f, %(zvelo)f, %(xdist)f, %(xvelo)f, %(tdist)f, %(tvelo)f
%(ramptime)f, %(zramp)f, %(zzero)f, %(xramp)f, %(xzero)f, %(tramp)f, %(tzero)f
"""
    ramp_template = "%(ramptime)f, %(zramp)f, %(zvelo)f, %(xramp)f, %(xvelo)f, %(tramp)f, %(tvelo)f"
    move_template = "%(scantime)f, %(zdist)f, %(zvelo)f, %(xdist)f, %(xvelo)f, %(tdist)f, %(tvelo)f"
    down_template = "%(ramptime)f, %(zramp)f, %(zzero)f, %(xramp)f, %(xzero)f, %(tramp)f, %(tzero)f"

    def __init__(self, host=None, user=None, passwd=None,
                 group=None, positioners=None, mode=None, type=None):
        self.host = host or xps_config['HOST']
        self.user = user or xps_config['USER']
        self.passwd = passwd or xps_config['PASSWORD']
        self.group_name = group or xps_config['GROUP NAME']
        self.positioners = positioners or xps_config['POSITIONERS']
        self.positioners = tuple(self.positioners.replace(',', ' ').split())

        gout = []
        gtit = []
        for pname in self.positioners:
            for out in xps_config['GATHER OUTPUTS']:
                gout.append('%s.%s.%s' % (self.group_name, pname, out))
                gtit.append('%s.%s' % (pname, out))
        self.gather_outputs = gout
        self.gather_titles = "%s\n#%s\n" % (xps_config['GATHER TITLES'],
                                            "  ".join(gtit))

        self.xps = XPS()
        self.ssid = self.xps.TCP_ConnectToServer(self.host, xps_config['PORT'], xps_config['TIMEOUT'])
        self.xps.Login(self.ssid, self.user, self.passwd)
        self.trajectories = {}

        self.ftpconn = ftplib.FTP()

        self.nlines_out = 0

        self.xps.GroupMotionDisable(self.ssid, self.group_name)
        time.sleep(0.1)
        self.xps.GroupMotionEnable(self.ssid, self.group_name)

        for i in range(64):
            self.xps.EventExtendedRemove(self.ssid, i)

    def ftp_connect(self):
        self.ftpconn.connect(self.host)
        self.ftpconn.login(self.user, self.passwd)
        self.FTP_connected = True

    def ftp_disconnect(self):
        "close ftp connnection"
        self.ftpconn.close()
        self.FTP_connected = False

    def upload_trajectory_file(self, fname, data):
        self.ftp_connect()
        self.ftpconn.cwd(xps_config['TRAJ_FOLDER'])
        self.ftpconn.storbinary('STOR %s' % fname, StringIO(data))
        self.ftp_disconnect()

    def define_line_trajectories_soller(self, name='default',
                                        axes=('z', 'x', 't'),
                                        start_values=(0, 0, 0),
                                        stop_values=(1, 1, 1),
                                        accel_values=(None, None, None),
                                        step=0.001, scan_time=10.0):
        """defines 'forward' and 'backward' trajectories for a line scan
        in PVT Mode"""
        accelerations = []
        for ind, accel_value in enumerate(accel_values):
            accel_value = accel_value or xps_config['DEFAULT ACCEL'][axes[ind]]
            accelerations.append(accel_value)
        accel_values = np.array(accelerations)
        start_values = np.array(start_values)
        stop_values = np.array(stop_values)

        distances = (stop_values - start_values) * 1.0
        velocities = distances / scan_time

        ramp_time = np.max(abs(velocities / accel_values))
        scan_time = abs(scan_time)
        pixel_time = (scan_time * step / abs(distances))[0]
        ramp = 0.5 * velocities * ramp_time

        trajectory = {'scantime': scan_time, 'ramptime': ramp_time, 'pixeltime': pixel_time,
                      'zzero': 0., 'xzero': 0., 'tzero': 0., 'step': step, 'axes': axes}

        this = {'start': start_values, 'stop': stop_values,
                'velo': velocities, 'ramp': ramp, 'dist': distances}

        for attr in this.keys():
            for ind, ax in enumerate(axes):
                trajectory["%s%s" % (ax, attr)] = this[attr][ind]

        self.trajectories[name] = trajectory

        try:
            self.upload_trajectory_file(name + '.trj', self.zxt_template % trajectory)
            print 'uploaded'
        except:
            pass
        return trajectory

    def define_line_trajectories_soller_multiple_motors(self, name='default',
                                                        axes=('z', 'x', 't'),
                                                        start_values=(0, 0, 0),
                                                        stop_values=([1, 1, 1], [1.4, 1.3, 1.2]),
                                                        accel_values=(None, None, None),
                                                        step=0.001, scan_time=10.0):
        """defines 'forward' and 'backward' trajectories for a line scan
        in PVT Mode"""
        accelerations = []
        for ind, accel_value in enumerate(accel_values):
            accel_value = accel_value or xps_config['DEFAULT ACCEL'][axes[ind]]
            accelerations.append(accel_value)
        accel_values = np.array(accelerations)
        start_values = np.array(start_values)
        stop_values = np.array(stop_values)

        distances = []
        velocities = []
        temp_start_values = start_values
        for ind, values in enumerate(stop_values):
            distances.append((values - temp_start_values) * 1.0)
            velocities.append(distances[-1] / scan_time * len(stop_values))
            temp_start_values = values

        ramp_time = np.max(abs(velocities[0] / accel_values))
        scan_time = float(abs(scan_time)) / len(stop_values)
        pixel_time = (scan_time * step / abs(distances[0][0]))
        ramp = 0.5 * velocities[0] * ramp_time

        # %(ramptime)f, %(zramp)f, %(zvelo)f, %(xramp)f, %(xvelo)f, %(tramp)f, %(tvelo)f
        ramp_attr = {'ramptime': ramp_time,
                     'zramp': ramp[0], 'zvelo': velocities[0][0],
                     'xramp': ramp[1], 'xvelo': velocities[0][1],
                     'tramp': ramp[2], 'tvelo': velocities[0][2]
                     }
        ramp_str = self.ramp_template % ramp_attr

        # "%(ramptime)f, %(zramp)f, %(zzero)f, %(xramp)f, %(xzero)f, %(tramp)f, %(tzero)f"
        down_attr = {'ramptime': ramp_time,
                     'zramp': ramp[0], 'zzero': 0,
                     'xramp': ramp[1], 'xzero': 0,
                     'tramp': ramp[2], 'tzero': 0}

        down_str = self.down_template % down_attr
        move_strings = []
        for ind in range(len(distances)):
            # "%(scantime)f, %(zdist)f, %(zvelo)f, %(xdist)f, %(xvelo)f, %(tdist)f, %(tvelo)f"
            attr = {'scantime': scan_time,
                    'zdist': distances[ind][0], 'zvelo': velocities[ind][0],
                    'xdist': distances[ind][1], 'xvelo': velocities[ind][1],
                    'tdist': distances[ind][2], 'tvelo': velocities[ind][2]}
            move_strings.append(self.move_template % attr)

        # construct trajectory:

        trajectory_str = ramp_str + '\n'
        for move_string in move_strings:
            trajectory_str += move_string + '\n'
        trajectory_str += down_str + '\n'

        self.trajectories[name] = {'pixeltime': pixel_time, 'zramp': ramp[0],
                                   'xramp': ramp[1], 'tramp': ramp[2],
                                   'step_number': len(distances)}

        ret = False

        try:
            self.upload_trajectory_file(name + '.trj', trajectory_str)
            ret = True
            print 'uploaded'
        except:
            pass
        return trajectory_str

    def run_line_trajectory_soller(self, name='default', verbose=False, save=True,
                                   outfile='Gather.dat'):
        """run trajectory in PVT mode"""
        traj = self.trajectories.get(name, None)
        if traj is None:
            print 'Cannot find trajectory named %s' % name
            return

        traj_file = '%s.trj' % name
        dtime = traj['pixeltime']
        ramps = (-traj['zramp'], -traj['xramp'], -traj['tramp'])
        try:
            step_number = traj['step_number']
        except KeyError:
            step_number = 1

        self.xps.GroupMoveRelative(self.ssid, 'G2', ramps)

        # print 'RUN TRAJ ', axis, ramps, traj_file

        pos_names = ['SLX', 'SLZ', 'SLT']

        self.gather_outputs = []
        gather_titles = []

        for pos_name in pos_names:
            for out in xps_config['GATHER OUTPUTS']:
                self.gather_outputs.append('%s.%s.%s' % (self.group_name, pos_name, out))
                gather_titles.append('%s.%s' % (pos_name, out))
        self.gather_titles = "%s\n#%s\n" % (xps_config['GATHER TITLES'],
                                            "  ".join(gather_titles))

        self.xps.GatheringReset(self.ssid)
        self.xps.GatheringConfigurationSet(self.ssid, self.gather_outputs)

        ret = self.xps.MultipleAxesPVTPulseOutputSet(self.ssid, self.group_name,
                                                     2, 2 + step_number, dtime)
        ret = self.xps.MultipleAxesPVTVerification(self.ssid, self.group_name, traj_file)

        buffer = ('Always', 'G2.PVT.TrajectoryPulse')
        o = self.xps.EventExtendedConfigurationTriggerSet(self.ssid, buffer,
                                                          ('0', '0'), ('0', '0'),
                                                          ('0', '0'), ('0', '0'))

        o = self.xps.EventExtendedConfigurationActionSet(self.ssid, ('GatheringOneData',),
                                                         ('',), ('',), ('',), ('',))

        eventID, m = self.xps.EventExtendedStart(self.ssid)

        ret = self.xps.MultipleAxesPVTExecution(self.ssid, self.group_name, traj_file, 1)
        o = self.xps.EventExtendedRemove(self.ssid, eventID)
        o = self.xps.GatheringStop(self.ssid)

        npulses = 0
        if save:
            npulses = self.save_results(outfile, verbose=verbose)

        self.xps.GroupMoveRelative(self.ssid, 'G2', -np.array(ramps))
        return npulses

    def abort_scan(self):
        pass

    def move(self, xpos=None, ypos=None, tpos=None):
        "move XY positioner to supplied position"
        ret = self.xps.GroupPositionCurrentGet(self.ssid, 'FINE', 3)
        if xpos is None:  xpos = ret[1]
        if ypos is None:  ypos = ret[2]
        if tpos is None:  tpos = ret[3]
        self.xps.GroupMoveAbsolute(self.ssid, 'FINE', (xpos, ypos, tpos))

    def save_results(self, fname, verbose=False):
        """read gathering data from XPS
        """
        # self.xps.GatheringStop(self.ssid)
        # db = debugtime()
        ret, npulses, nx = self.xps.GatheringCurrentNumberGet(self.ssid)
        counter = 0
        while npulses < 1 and counter < 5:
            counter += 1
            time.sleep(1.50)
            ret, npulses, nx = self.xps.GatheringCurrentNumberGet(self.ssid)
            print 'Had to do repeat XPS Gathering: ', ret, npulses, nx

        # db.add(' Will Save %i pulses , ret=%i ' % (npulses, ret))
        ret, buff = self.xps.GatheringDataMultipleLinesGet(self.ssid, 0, npulses)
        # db.add('MLGet ret=%i, buff_len = %i ' % (ret, len(buff)))

        if ret < 0:  # gathering too long: need to read in chunks
            print 'Need to read Data in Chunks!!!'  # how many chunks are needed??
            Nchunks = 3
            nx = int((npulses - 2) / Nchunks)
            ret = 1
            while True:
                time.sleep(0.1)
                ret, xbuff = self.xps.GatheringDataMultipleLinesGet(self.ssid, 0, nx)
                if ret == 0:
                    break
                Nchunks = Nchunks + 2
                nx = int((npulses - 2) / Nchunks)
                if Nchunks > 10:
                    print 'looks like something is wrong with the XPS!'
                    break
            print  ' -- will use %i Chunks for %i Pulses ' % (Nchunks, npulses)
            # db.add(' Will use %i chunks ' % (Nchunks))
            buff = [xbuff]
            for i in range(1, Nchunks):
                ret, xbuff = self.xps.GatheringDataMultipleLinesGet(self.ssid, i * nx, nx)
                buff.append(xbuff)
                # db.add('   chunk %i' % (i))
            ret, xbuff = self.xps.GatheringDataMultipleLinesGet(self.ssid, Nchunks * nx,
                                                                npulses - Nchunks * nx)
            buff.append(xbuff)
            buff = ''.join(buff)
            # db.add('   chunk last')

        obuff = buff[:]
        for x in ';\r\t':
            obuff = obuff.replace(x, ' ')
        # db.add('  data fixed')
        f = open(fname, 'w')
        f.write(self.gather_titles)
        f.write(obuff)
        f.close()
        nlines = len(obuff.split('\n')) - 1
        if verbose:
            print 'Wrote %i lines, %i bytes to %s' % (nlines, len(buff), fname)
        self.nlines_out = nlines
        # db.show()
        return npulses

