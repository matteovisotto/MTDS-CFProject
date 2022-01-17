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
In this function will try to overtake the obstacle above it.
After the obstacle is being surpassed, the drone will return on its original height.
:param mc: The MotionCommander used.
:param mr: The MultiRanger used.
:return: Void.
'''


def pass_over(mc, mr):
    while is_close(mr.front, 0.4):
        mc.start_linear_motion(0, 0, 0.2)
        time.sleep(0.05)
    time.sleep(0.5)
    mc.start_linear_motion(0.2, 0, 0)
    time.sleep(4)


'''
In the main function we check if the drone detects an obstacle in front of it and if that happens
it will call the pass_over function.
:param keep_flying: It is always set to True and goes to False when the algorithm ends.
'''


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()
    cf = Crazyflie(rw_cache='./cache')
    with SyncCrazyflie(URI, cf=cf) as scf:
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
