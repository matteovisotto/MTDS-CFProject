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


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()
    cf = Crazyflie(rw_cache='./cache')
    with SyncCrazyflie(URI, cf=cf) as scf:
        log = CFLogging(scf, debug_mode=False)
        log.start_logging()
        with MotionCommander(scf, default_height=0.2) as motion_commander:
            with Multiranger(scf) as multiranger:
                keep_flying = True
                is_started = False
                is_sliding = False
                velocity_x = 0.3
                velocity_y = 0.0

                start_y = 0
                end_y = 0

                while keep_flying:
                    if is_close(multiranger.front, 0.4):
                        is_sliding = True
                        if is_close(multiranger.right, 0.4):
                            velocity_y = 0.3
                        elif is_close(multiranger.left, 0.4):
                            velocity_y = -0.3
                        else:
                            velocity_y = 0.3
                        velocity_x = 0
                        if start_y == 0:
                            start_y = log.get_value('stateEstimate.y')
                    elif is_far(multiranger.front, 0.4):
                        if is_sliding:
                            time.sleep(0.4 * abs(velocity_y))
                            is_sliding = False
                        velocity_x = 0.3
                        velocity_y = 0
                        #Inserire qui il rientro alla traiettoria precedente

                    if is_close(multiranger.back, 0.3):
                        keep_flying = False

                    motion_commander.start_linear_motion(
                        velocity_x, velocity_y, 0)

                    time.sleep(0.05)
            log.stop_logging()
