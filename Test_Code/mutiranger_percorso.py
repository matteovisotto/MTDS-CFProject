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


def is_close(range, MIN_DISTANCE):
    if range is None:
        return False
    else:
        return range < MIN_DISTANCE

def is_far(range, MIN_DISTANCE):
        if range is None:
            return False
        else:
            return range > MIN_DISTANCE


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    cf = Crazyflie(rw_cache='./cache')
    with SyncCrazyflie(URI, cf=cf) as scf:
        log = CFLogging(scf, debug_mode= True)
        log.add_log_variable('range.front', 'uint16_t')
        #log.start_logging()
        with MotionCommander(scf, default_height=0.2) as motion_commander:
            with Multiranger(scf) as multiranger:
                    turn_left = False
                    turn_right = True
                    land = False
                    keep_flying = True

                    while keep_flying:
                        velocity = 0.3

                        if is_close(multiranger.front, 0.4):
                            if (turn_right):
                                motion_commander.start_linear_motion(0, 0, 0)
                                motion_commander.turn_right(90)
                                turn_left = True
                                turn_right = False
                            if (turn_left):
                                motion_commander.start_linear_motion(0, 0, 0)
                                motion_commander.turn_left(180)
                                turn_left = False
                                turn_right = True

                            if is_close(multiranger.front, 0.4):
                                land = True

                            if (land):
                                keep_flying = False

                            

                        if is_close(multiranger.back, 0.3):
                            keep_flying = False

                        motion_commander.start_linear_motion(velocity, 0, 0)
                        time.sleep(0.1)

