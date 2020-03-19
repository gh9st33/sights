from motor_wrapper import MotorWrapper, ConnectionWrapper
import serial

class PololuSimpleMotor(MotorWrapper):
    def __init__(self, connection, config):
        self.connection = connection
        self.guid = config.get("guid")
        self.name = config.get("name")
        # Exit safe start and enable movement
        self.connection.exit_safe_start()

    # Sets the SMC's target speed (-100, 100)
    def set_speed(self, speed):
        # Scale to (-3200 to 3200).
        speed = speed * 32
        
        cmd = 0x85  # Motor forward
        if speed < 0:
            cmd = 0x86  # Motor reverse
            speed = -speed
        self.connection.send_command(cmd, speed & 0x1F, speed >> 5 & 0x7F)

    # Gets the target speed (-3200 to 3200).
    def get_speed(self):
        return self.connection.get_variable_signed(20)


class PololuSimpleConnection(ConnectionWrapper):
    def __init__(self, config):
        MotorWrapper.__init__(self, config)
        self.port = config.get('port')
        self.baudrate = config.get('baudrate')
        self.device_number = config.get('device_number')

    def send_command(self, cmd, *data_bytes):
        if self.device_number == None:
            header = [cmd]  # Compact protocol
        else:
            header = [0xAA, self.device_number, cmd & 0x7F]  # Pololu protocol
        self.port.write(bytes(header + list(data_bytes)))

    # Sends the Exit Safe Start command, which is required to drive the motor.
    def exit_safe_start(self):
        self.send_command(0x83)

    # Gets the specified variable as an unsigned value.
    def get_variable(self, id):
        self.send_command(0xA1, id)
        result = self.port.read(2)
        if len(result) != 2:
            raise RuntimeError("Expected to read 2 bytes, got {}.".format(len(result)))
        b = bytearray(result)
        return b[0] + 256 * b[1]

    # Gets the specified variable as a signed value.
    def get_variable_signed(self, id):
        value = self.get_variable(id)
        if value >= 0x8000:
            value -= 0x10000
        return value

    # Gets a number where each bit represents a different error, and the
    # bit is 1 if the error is currently active.
    # See the user's guide for definitions of the different error bits.
    def get_error_status(self):
        return self.get_variable(0)
