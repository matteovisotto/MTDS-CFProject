import logging
import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

from Utility.CFLogging import CFLogging

cf_number = '07'

uri = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7' + cf_number)
logging.basicConfig(level=logging.ERROR)


def x_callback(value):
    pass


def battery_leve_cbk(value):
    print(value)

def motion_commander(scf):
    with MotionCommander(scf) as mc:
        time.sleep(1)
        mc.up(0.5)
        time.sleep(3)
        mc.down(0.7)
        time.sleep(1)



if __name__ == '__main__':
    cflib.crtp.init_drivers()
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        time.sleep(1)
        log = CFLogging(scf, use_default=True, debug_mode=False)
        log.register_callback('stateEstimate.x', x_callback)
        log.add_log_variable('stateEstimate.az', 'float')
        log.register_callback('stateEstimate.az', battery_leve_cbk)
        log.start_logging()
        motion_commander(scf)
        log.stop_logging()

