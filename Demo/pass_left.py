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

INITIAL_Y = 0
FINAL_Y = 0

if len(sys.argv) > 1:
    URI = sys.argv[1]

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


'''
In this function, using the Multi-ranger deck,
we check if the drone is too close to an obstacle in a predetermined direction.
:param range: The direction to be checked.
:param MIN_DISTANCE: The distance to be checked.
:return: Return True if it is too close, otherwise it will return False.
'''


def is_close(range, distance):
    if range is None:
        return False
    else:
        return range < distance


'''
In this function will try to overtake the obstacle on the left.
After the obstacle is being surpassed, the drone will return on the original value of the Y axis.
:param mc: The MotionCommander used.
:param mr: The MultiRanger used.
:param log: The Logging class used.
:return: Void.
'''


def pass_left(mc, mr, log):
    mc.start_linear_motion(0, 0, 0)
    time.sleep(0.1)
    while is_close(mr.front, 0.4):
        mc.start_linear_motion(0, 0.2, 0)
        time.sleep(0.05)
    time.sleep(0.5)
    mc.start_linear_motion(0, 0, 0)
    time.sleep(0.1)
    mc.start_linear_motion(0.2, 0, 0)
    time.sleep(2.1)
    while is_close(mr.right, 0.50):
        mc.start_linear_motion(0.2, 0, 0)
        time.sleep(0.05)
    time.sleep(1)
    mc.start_linear_motion(0, 0, 0)
    time.sleep(0.1)
    while log.get_value('stateEstimate.y') > INITIAL_Y:
        mc.start_linear_motion(0, -0.2, 0)
        time.sleep(0.05)
    mc.start_linear_motion(0, 0, 0)
    time.sleep(0.1)


'''
In the main function we check if the drone detects an obstacle in front of it and if that happens
it will save the value of the Y axis and will call the pass_left function.
:param keep_flying: It is always set to True and goes to False when the algorithm ends.
'''


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()
    cf = Crazyflie(rw_cache='./cache')
    with SyncCrazyflie(URI, cf=cf) as scf:
        log = CFLogging(scf, debug_mode=False)
        log.add_log_variable('range.right', 'uint16_t')
        log.start_logging()
        with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as motion_commander:
            with Multiranger(scf) as multiranger:
                keep_flying = True
                while keep_flying:
                    if is_close(multiranger.front, 0.4):
                        INITIAL_Y = log.get_value('stateEstimate.y')
                        pass_left(motion_commander, multiranger, log)
                        keep_flying = False

                    motion_commander.start_linear_motion(
                        0.2, 0, 0)
                    time.sleep(0.05)
            log.stop_logging()
