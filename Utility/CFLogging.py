"""
Simplified version of logging library
"""

from cflib.crazyflie.log import LogConfig


class CFLogging:
    # Class init
    # use_default - Add stateEstimate x,y and z variable
    # debug_mode - If True, print variables in console
    def __init__(self, scf, use_default=True, debug_mode=False):
        super().__init__()
        self.position_estimate = {}
        self.use_default = use_default
        self.callbacks = {}
        self.scf = scf
        self.debug_mode = debug_mode
        logconf = LogConfig(name='LoggingDefault', period_in_ms=10)
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
            if key in self.callbacks:
                self.callbacks[key](data[key])

    # Function that has to be called to start logging
    def start_logging(self):
        self.logconf.start()

    # Function that has to be called before terminate the script
    def stop_logging(self):
        self.logconf.stop()

    # Get a variable value in its last stare by key
    def get_value(self, key):
        if key in self.position_estimate:
            return self.position_estimate[key]
        else:
            raise IndexError('Index not found')

    # Returns all the variables added for logging
    def get_last_values(self):
        return self.position_estimate

    # Add a new variable using name and data type according to crazyflie TOC documentation
    def add_log_variable(self, variable, data_type):
        self.logconf.add_variable(variable, data_type)
        self.position_estimate[variable] = None

    # Register a new callback for a variable already present, use the name specified in the TOC
    # This function is called every time the value changes
    def register_callback(self, variable, callback):
        self.callbacks[variable] = callback
