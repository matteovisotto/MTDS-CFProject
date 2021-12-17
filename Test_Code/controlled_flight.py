
import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

# URI to the Crazyflie to connect to
uri = 'radio://0/80/2M/E7E7E7E704'

is_deck_attached = True

DEFAULT_HEIGHT = 0.3

logging.basicConfig(level=logging.ERROR)

def take_off_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        '''
        time.sleep(3)
        mc.forward(0.3)
        time.sleep(3)
        mc.circle_right(0.5, velocity=0.2, angle_degrees=90)
        time.sleep(3)
        mc.forward(0.3)
        time.sleep(3)
        mc.turn_right(90)
        time.sleep(3)
        mc.forward(0.6)
        time.sleep(3)
        mc.turn_right(90)
        time.sleep(3)
        mc.forward(0.6)
        time.sleep(3)
        mc.turn_right(90)
        time.sleep(3)
        '''

        time.sleep(1)
        mc.forward(0.5)
        mc.circle_right(0.5, velocity=0.2, angle_degrees=180)
        mc.forward(0.2)
        mc.circle_right(0.5, velocity=0.2, angle_degrees=180)
        time.sleep(1)


if __name__ == '__main__':
    cflib.crtp.init_drivers()
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        if is_deck_attached:
            take_off_simple(scf)

