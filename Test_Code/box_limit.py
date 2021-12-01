import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander


URI = 'radio://0/80/2M/E7E7E7E705'
DEFAULT_HEIGHT = 0.5
BOX_LIMIT_X = 0.5
BOX_LIMIT_Y = 0.2
BOX_LIMIT_Z = 0.3

is_deck_attached = True

logging.basicConfig(level=logging.ERROR)

position_estimate = [0, 0, 0]


def move_box_limit(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        body_x_cmd = 0.5
        body_y_cmd = 0.0
        body_z_cmd = 0.3
        max_vel = 0.2

        while (1):


            if position_estimate[0] > BOX_LIMIT_X:
               body_x_cmd = -max_vel
            elif position_estimate[0] < -BOX_LIMIT_X:
               body_x_cmd = max_vel
            if position_estimate[1] > BOX_LIMIT_Y:
               body_y_cmd = -max_vel
            elif position_estimate[1] < -BOX_LIMIT_Y:
               body_y_cmd = max_vel

            if position_estimate[2] > BOX_LIMIT_Z+0.3:
                body_z_cmd = -max_vel
            elif position_estimate[2] < BOX_LIMIT_Z:
                body_z_cmd = max_vel

            mc.start_linear_motion(body_x_cmd, body_y_cmd, body_z_cmd)

            time.sleep(0.1)



def log_pos_callback(timestamp, data, logconf):
    print(data)
    global position_estimate
    position_estimate[0] = data['stateEstimate.x']
    position_estimate[1] = data['stateEstimate.y']
    position_estimate[2] = data['stateEstimate.z']


def param_deck_flow(name, value_str):
    value = int(value_str)
    print(value)
    global is_deck_attached
    if value:
        is_deck_attached = True
        print('Deck is attached!')
    else:
        is_deck_attached = False
        print('Deck is NOT attached!')


if __name__ == '__main__':
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:

        time.sleep(1)

        logconf = LogConfig(name='Position', period_in_ms=10)
        logconf.add_variable('stateEstimate.x', 'float')
        logconf.add_variable('stateEstimate.y', 'float')
        logconf.add_variable('stateEstimate.z', 'float')
        scf.cf.log.add_config(logconf)
        logconf.data_received_cb.add_callback(log_pos_callback)

        if is_deck_attached:
            logconf.start()
            move_box_limit(scf)
            logconf.stop()