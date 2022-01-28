'''
The bottom (down) sensor of multiranger class works both with the Z-Range and FlowV2 deck.
The variable used to log the distance from the ground (or anything else under the drone)
is the range.zrange of type uint16_t. The log returns an int value that corresponds to the distance in millimeters.
To use it directly inside the code use the multiranger.down property of Multiranger class.
In this example both log and Multiranger have been used.
'''

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

DEFAULT_HEIGHT = 0.2

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


def pass_over(mc, mr):
    while is_close(mr.front, 0.4):
        mc.start_linear_motion(0, 0, 0.2)
        time.sleep(0.05)
    time.sleep(0.5)
    mc.start_linear_motion(0.2, 0, 0)
    time.sleep(2.1)
    while is_close(mr.down, 0.50):
        mc.start_linear_motion(0.2, 0, 0)
        time.sleep(0.05)
    time.sleep(1)

    while is_far(mr.down, DEFAULT_HEIGHT):
        mc.start_linear_motion(0, 0, -0.2)
        time.sleep(0.05)



if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()
    cf = Crazyflie(rw_cache='./cache')
    with SyncCrazyflie(URI, cf=cf) as scf:
        log = CFLogging(scf, debug_mode=False)
        log.add_log_variable('range.down', 'uint16_t')  # Z range log variable
        log.register_callback('range.down', z_cb)
        #log.start_logging()
        with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as motion_commander:
            with Multiranger(scf) as multiranger:
                keep_flying = True
                while keep_flying:
                    if is_close(multiranger.front, 0.4):
                        pass_over(motion_commander, multiranger)
                        keep_flying = False

                    motion_commander.start_linear_motion(
                        0.2, 0, 0)
                    time.sleep(0.05)
            #log.stop_logging()