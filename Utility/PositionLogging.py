from cflib.crazyflie.log import LogConfig


class MCPositionLogging:
    def __init__(self, scf):
        super.__init__()
        self.position_estimate = [0, 0, 0]
        self.scf = scf
        logconf = LogConfig(name='Position', period_in_ms=10)
        logconf.add_variable('stateEstimate.x', 'float')
        logconf.add_variable('stateEstimate.y', 'float')
        logconf.add_variable('stateEstimate.z', 'float')
        scf.cf.log.add_config(logconf)
        logconf.data_received_cb.add_callback(self.data_callback)
        self.logconf = logconf
        self.on_x_change = self.placeholder
        self.on_y_change = self.placeholder
        self.on_z_change = self.placeholder
        self.on_variables_changes = self.placeholder
        self.motion_commander = None

    def data_callback(self, timestamp, data, logconf):
        self.position_estimate[0] = data['stateEstimate.x']
        self.position_estimate[1] = data['stateEstimate.y']
        self.position_estimate[2] = data['stateEstimate.z']
        self.on_x_change(self.position_estimate[0], self.motion_commander)
        self.on_y_change(self.position_estimate[1], self.motion_commander)
        self.on_z_change(self.position_estimate[2], self.motion_commander)
        self.on_variables_changes(self.position_estimate, self.motion_commander)

    def start_logging(self):
        self.logconf.start()

    def stop_logging(self):
        self.logconf.stop()

    def placeholder(self, value, mc):
        pass

    def set_motion_commander(self, mc):
        self.motion_commander = mc

    def set_on_x_changed(self, callback):
        self.on_x_change = callback

    def set_on_y_changed(self, callback):
        self.on_y_change = callback

    def set_on_z_changed(self, callback):
        self.on_z_change = callback

    def get_last_x(self):
        return self.position_estimate[0]

    def get_last_y(self):
        return self.position_estimate[1]

    def get_last_z(self):
        return self.position_estimate[2]
