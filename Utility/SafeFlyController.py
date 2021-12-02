import time

from cflib.positioning.motion_commander import MotionCommander

from Utility.PositionLogging import MCPositionLogging


class SafeFlyController:

    def __init__(self, scf, use_position_controller=True):
        super.__init__()
        self.use_position_controller = use_position_controller
        self.motion_commander = None
        self.motion_locked = False
        self.max_x = 0.5
        self.min_x = -0.5
        self.max_y = 0.5
        self.min_y = -0.5
        self.max_z = 1
        self.min_z = 0.1
        self.default_high = 0.5
        self.x_controller = self.default_x_controller
        self.y_controller = self.default_y_controller
        self.z_controller = self.default_z_controller
        self.scf = scf
        self.logging = MCPositionLogging(scf)
        self.fly_commands = self.empty_fly

    def start_flying(self):
        if self.use_position_controller:
            self.logging.set_on_x_changed(self.x_controller)
            self.logging.set_on_y_changed(self.y_controller)
            self.logging.set_on_z_changed(self.z_controller)
        self.logging.start_logging()
        self.create_motion_commander()

    def default_x_controller(self, value, mc):
        if not self.motion_locked:
            if value > self.max_x:
                self.motion_locked = True
                mc.stop()
                mc.move_distance(-self.max_x, 0, 0)
            elif value < self.min_x:
                self.motion_locked = True
                mc.stop()
                mc.move_distance(-self.min_x, 0, 0)
            self.motion_locked = False

    def default_y_controller(self, value, mc):
        if not self.motion_locked:
            if value > self.max_y:
                self.motion_locked = True
                mc.stop()
                mc.move_distance(0, -self.max_y, 0)
            elif value < self.min_y:
                self.motion_locked = True
                mc.stop()
                mc.move_distance(0, -self.min_y, 0)
            self.motion_locked = False

    def default_z_controller(self, value, mc):
        if not self.motion_locked:
            if value > self.max_z:
                self.motion_locked = True
                mc.stop()
                mc.move_distance(0, 0, self.default_high - self.max_z)
            elif value < self.min_z:
                self.motion_locked = True
                mc.stop()
                mc.move_distance(0, 0, self.default_high - self.min_z)
            self.motion_locked = False

    def create_motion_commander(self):
        with MotionCommander(self.scf, default_height=self.default_high) as mc:
            self.motion_commander = mc
            self.logging.set_motion_commander(mc)
            time.sleep(1)
            self.fly_commands(self.motion_commander)
            self.exit_execution()


    def empty_fly(self, mc):
        time.sleep(1)
        mc.stop()

    def exit_execution(self):
        self.logging.stop_logging()
