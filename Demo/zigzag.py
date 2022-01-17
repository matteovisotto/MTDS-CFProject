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


'''
This is the core function of this demo.
Using the Multi-ranger deck, we check if the drone detect obstacles.
If no obstacles are detected it will try to turn right.
If an obstacle on the right is detected, it will try to turn left.
If two obstacles, one on the left and one the right, are detected it will return False and then will land.
:param mc: The MotionCommander used.
:param mr: The MultiRanger used.
:return: Return True if it can proceed, otherwise it will return False.
'''


def obstacle_avoidance(mc, mr):
    right_1 = True
    left_1 = True

    if is_close(mr.right, 0.4):
        right_1 = False

    if is_close(mr.left, 0.4):
        left_1 = False

    if left_1 and right_1:
        print("Right and Left")
        mc.turn_left(90)
        return True
    elif left_1 and not right_1:
        print("Left")
        mc.turn_left(90)
        return True
    elif right_1 and not left_1:
        print("Right")
        mc.turn_right(90)
        return True
    else:
        return False


'''
In the main function we check if the drone detects an obstacle in front of it and if that happens
it will call the obstacle_avoidance function.
:param keep_flying: It is always set to True, unless the drones goes into a dead ends, where it becomes False.
'''


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    cf = Crazyflie(rw_cache='./cache')
    with SyncCrazyflie(URI, cf=cf) as scf:

        with MotionCommander(scf, default_height=0.2) as motion_commander:
            with Multiranger(scf) as multiranger:
                keep_flying = True
                while keep_flying:
                    velocity = 0.3
                    if is_close(multiranger.front, 0.4):
                        motion_commander.start_linear_motion(0, 0, 0)
                        if not obstacle_avoidance(motion_commander, multiranger):
                            keep_flying = False
                    motion_commander.start_linear_motion(velocity, 0, 0)
                    time.sleep(0.1)
