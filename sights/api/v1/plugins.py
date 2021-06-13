from ...components.sensor import Sensor, sensor_plugins
from ...components.motor import Motor, motor_plugins


def register_sensor_plugin(sensor: Sensor):
    sensor_plugins[sensor.name] = sensor


def register_motor_plugin(motor: Motor):
    motor_plugins[motor.name] = motor


def list_all():
    return [plugin for plugin in sensor_plugins + motor_plugins]
