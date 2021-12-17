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


def is_close(range):
    MIN_DISTANCE = 0.5  # m

    if range is None:
        return False
    else:
        return range < MIN_DISTANCE


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    cf = Crazyflie(rw_cache='./cache')
    with SyncCrazyflie(URI, cf=cf) as scf:
        log = CFLogging(scf, debug_mode= True)
        log.add_log_variable('range.front', 'uint16_t')
        log.start_logging()
        with MotionCommander(scf, default_height=0.2) as motion_commander:
            with Multiranger(scf) as multiranger:
                keep_flying = True

                velocity_x = 0.3
                velocity_y = 0.0

                while keep_flying:
                    VELOCITY = 0.3

                    if log.get_value('stateEstimate.x') < -0.2:
                        keep_flying = False

                    if is_close(multiranger.front):
                        velocity_x -= VELOCITY
                    if is_close(multiranger.back):
                        velocity_x += VELOCITY

                   # if is_close(multiranger.left):
                       # velocity_y -= VELOCITY
                    #if is_close(multiranger.right):
                        #velocity_y += VELOCITY

                    #if is_close(multiranger.up):
                        #keep_flying = False

                    motion_commander.start_linear_motion(
                        velocity_x, 0, 0)

                    time.sleep(0.1)
            log.stop_logging()
