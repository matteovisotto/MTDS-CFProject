from cflib.crazyflie.log import LogConfig


class PositionLogging:
    def __init__(self, scf, use_default=True, debug_mode=False):
        super().__init__()
        self.position_estimate = {}
        self.use_default = use_default
        self.callbacks = {}
        self.scf = scf
        self.debug_mode = debug_mode
        logconf = LogConfig(name='Position', period_in_ms=10)
        if use_default:
            logconf.add_variable('stateEstimate.x', 'float')
            self.position_estimate['stateEstimate.x'] = 0
            logconf.add_variable('stateEstimate.y', 'float')
            self.position_estimate['stateEstimate.y'] = 0
            logconf.add_variable('stateEstimate.z', 'float')
            self.position_estimate['stateEstimate.z'] = 0
        scf.cf.log.add_config(logconf)
        logconf.data_received_cb.add_callback(self._data_callback)
        self.logconf = logconf

    def _data_callback(self, timestamp, data, logconf):
        if self.debug_mode:
            print(data)
        for key in self.position_estimate:
            self.position_estimate[key] = data[key]
            if self.callbacks[key] is not None:
                self.callbacks[key](data[key])

    def start_logging(self):
        self.logconf.start()

    def stop_logging(self):
        self.logconf.stop()

    def get_value(self, key):
        if self.position_estimate[key] is not None:
            return self.position_estimate[key]
        else:
            raise IndexError('Index not found')

    def get_last_values(self):
        return self.position_estimate

    def add_log_variable(self, variable, data_type):
        self.logconf.add_variable(variable, data_type)
        self.position_estimate[variable] = None

    def register_callback(self, variable, callback):
        self.callbacks[variable] = callback
