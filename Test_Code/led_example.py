# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2019 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
"""
Simple example that connects to the crazyflie at `URI` and writes to
the LED memory so that individual leds in the LED-ring can be set,
it has been tested with (and designed for) the LED-ring deck.
Change the URI variable to your Crazyflie configuration.
"""
import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.mem import MemoryElement
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

# URI to the Crazyflie to connect to
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E707')

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf

        # Get LED memory and write to it
        cf.param.set_value('ring.effect', '13')
        mem = cf.mem.get_mems(MemoryElement.TYPE_DRIVER_LED)
        if len(mem) > 0:
            mem[0].leds[0].set(r=0, g=0, b=0)
            mem[0].leds[1].set(r=0, g=0, b=0)
            mem[0].leds[2].set(r=0, g=0, b=0)
            mem[0].leds[3].set(r=0, g=0, b=0)
            mem[0].leds[4].set(r=0, g=0, b=0)
            mem[0].leds[5].set(r=0, g=0, b=0)
            mem[0].leds[6].set(r=0, g=0, b=0)
            mem[0].leds[7].set(r=0, g=0, b=0)
            mem[0].leds[8].set(r=0, g=0, b=0)
            mem[0].leds[9].set(r=0, g=0, b=0)
            mem[0].leds[10].set(r=0, g=0, b=0)
            mem[0].leds[11].set(r=0, g=0, b=0)
            mem[0].write_data(None)
        else:
            print('No LED ring present')


        time.sleep(2)