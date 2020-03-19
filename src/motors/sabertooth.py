# Sabertooth motor connection using serial
from motor_wrapper import MotorWrapper, ConnectionWrapper
import serial
import logging

class SabertoothMotor(MotorWrapper):
    def __init__(self, connection, config):
        self.connection = connection
        self.guid = config.get("guid")
        self.name = config.get("name")
        self.channel = config.get("channel")

    def set_speed(self, speed):
        if (self.channel == 1):
            msg = 64 + round(63 / 100 * max(min(left, 100), -100))
            self.serial.write(bytes([msg]))
        elif (self.channel == 2):
            msg = 192 + round(63 / 100 * max(min(left, 100), -100))
            self.serial.write(bytes([msg]))


class SabertoothConnection(ConnectionWrapper):
    # What type of motor this wrapper handles
    type_ = 'sabertooth'

    def __init__(self, config):
        MotorWrapper.__init__(self, config)
        self.port = config.get('port')
        self.baudrate = config.get('baudrate')
        self.serial = serial.Serial(port=self.port, baudrate=self.baudrate)

    def stop_all(self):
        self.serial.write(bytes([0]))

    def close(self):
        self.serial.close()
