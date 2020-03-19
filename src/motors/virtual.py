# Virtual motor connection
from motor_wrapper import MotorWrapper, ConnectionWrapper

class VirtualMotor(MotorWrapper):
    def __init__(self, connection, config):
        self.connection = connection
        self.guid = config.get("guid")
        self.name = config.get("name")

    def set_speed(self, speed):
        pass

class VirtualConnection(ConnectionWrapper):
    # What type of motor this wrapper handles
    type_ = 'virtual'

    def __init__(self, config):
        MotorWrapper.__init__(self, config)

    def stop_all(self):
        pass

    def close(self):
        pass