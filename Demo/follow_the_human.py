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

'''
In this function, using the Multi-ranger deck,
we check if the drone is too close to an obstacle in a predetermined direction.
:param range: The direction to be checked.
:param MIN_DISTANCE: The distance to be checked.
:return: Return True if it is too close, otherwise it will return False.
'''


def is_close(range, MIN_DISTANCE):
    if range is None:
        return False
    else:
        return range < MIN_DISTANCE


'''
In this function, using the Multi-ranger deck,
we check if the drone is too far from an obstacle in a predetermined direction.
:param range: The direction to be checked.
:param MIN_DISTANCE: The distance to be checked.
:return: Return True if it is too far, otherwise it will return False.
'''


def is_far(range, MIN_DISTANCE):
        if range is None:
            return False
        else:
            return range > MIN_DISTANCE


'''
In this function, using the Multi-ranger deck,
we check if the drone has a certain distance from an obstacle in a predetermined direction.
:param range: The direction to be checked.
:param MIN_DISTANCE: The distance to be checked.
:return: Return True if it is equal, otherwise it will return False.
'''


def is_equal(range, MIN_DISTANCE):
    if range is None:
        return False
    else:
        return MIN_DISTANCE - 0.1 < range < MIN_DISTANCE + 0.1


'''
In the main function the front sensor of the multiranger is used to detect the person in front of it.
Using the is_close, is_far and is_equal functions the velocity along the x axis is set based of the distance from the person.
As final result the drone follow the person.
:param keep_flying: It is always set to True, when the back sensor of the Multi-ranger is to close to an object.
'''


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    cf = Crazyflie(rw_cache='./cache')
    with SyncCrazyflie(URI, cf=cf) as scf:

        with MotionCommander(scf, default_height=0.6) as motion_commander:
            with Multiranger(scf) as multiranger:
                keep_flying = True
                is_started = False
                velocity_x = 0.0
                velocity_y = 0.0

                while not is_started:
                    if is_close(multiranger.front, 0.3):
                        is_started = True
                    time.sleep(0.1)

                while keep_flying:

                    if is_equal(multiranger.front, 0.4):
                        velocity_x = 0

                    elif is_far(multiranger.front, 1.1):
                        velocity_x = 0.7

                    elif is_far(multiranger.front, 0.8):
                        velocity_x = 0.5

                    elif is_far(multiranger.front, 0.6):
                        velocity_x = 0.1

                    elif is_close(multiranger.front, 0.6):
                        velocity_x = -0.3

                    if multiranger.back < 0.3:
                        keep_flying = False

                    motion_commander.start_linear_motion(
                        velocity_x, 0, 0)

                    time.sleep(0.05)
