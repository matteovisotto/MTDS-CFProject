import logging
import sys
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper
from cflib.utils.multiranger import Multiranger
from Utility.CFLogging import CFLogging

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E706')

if len(sys.argv) > 1:
    URI = sys.argv[1]

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


def is_close(range, distance):
    if range is None:
        return False
    else:
        return range < distance


def is_far(range, distance):
    if range is None:
        return False
    else:
        return range > distance


def is_equal(range, distance, interval=0.1):
    if range is None:
        return False
    else:
        return distance - interval < range < distance + interval


def z_cb(value):
    print(value / 1000)  # Print returned distance in meters


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()
    cf = Crazyflie(rw_cache='./cache')
    with SyncCrazyflie(URI, cf=cf) as scf:
        log = CFLogging(scf, debug_mode=False)
        log.add_log_variable('range.zrange', 'uint16_t')
        log.register_callback('range.zrange', z_cb)
        log.start_logging()
        with MotionCommander(scf, default_height=0.2) as motion_commander:
            with Multiranger(scf) as multiranger:
                keep_flying = True

                while keep_flying:
                    if is_far(multiranger.down, 0.6):
                        keep_flying = False

                    motion_commander.start_linear_motion(
                        0, 0, 0.1)

                    time.sleep(0.05)
            log.stop_logging()
