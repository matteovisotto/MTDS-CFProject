import logging
import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

from Utility.SafeFlyController import SafeFlyController

cf_number = '04'

uri = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7' + cf_number)
logging.basicConfig(level=logging.ERROR)


def fly_commands(mc):
    # use the motion commander variable to write your code
    time.sleep(1)
    mc.stop()


if __name__ == '__manin__':
    cflib.crtp.init_drivers()
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        time.sleep(1)
        flyController = SafeFlyController(scf)
        flyController.fly_commands = fly_commands
        flyController.start_flying()

