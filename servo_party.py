#!/usr/bin/env python3
from pyax12.connection import Connection
from enum import IntEnum

class Servo(IntEnum):
    LEFT_FRONT = 1
    RIGHT_FRONT = 2
    LEFT_BACK = 3
    RIGHT_BACK = 4

# Replicates the pyax12 Connection class
class DummyConnection:
    def __init__(self, port="/dev/null", baudrate=1000000):
        self.port = port
        self.baudrate = baudrate
        print("DEBUG: Opened dummy servo connection")

    def set_speed (self, id, speed):
        #print(id, "set to", speed)
        pass

    def close (self):
        print("DEBUG: Closed dummy servo connection")
        pass
    
    def set_cw_angle_limit (self, dynamixel_id, angle_limit, degrees=False):
        pass
    
    def set_ccw_angle_limit (self, dynamixel_id, angle_limit, degrees=False):
        pass


class ServoParty:
    def __init__(self, port="/dev/null", baudrate=1000000, speed_factor=512, dummy=False):
        if (dummy):
            self.sc = DummyConnection()
        else:   
            self.sc = Connection(port=port, baudrate=baudrate)
        self.speed_factor = speed_factor
        self.last_left = 0
        self.last_right = 0

    def stop(self):
        # Set all servos to 0
        self.sc.set_speed(1, 0)
        self.sc.set_speed(2, 0)
        self.sc.set_speed(3, 0)
        self.sc.set_speed(4, 0)
    
    def close(self):
        # Set all servos to 0
        self.stop();
        # Close the connection
        self.sc.close()

    def setup_servo(self, dynamixel_id):
        # Set the "wheel mode"
        self.sc.set_cw_angle_limit(dynamixel_id, 0, degrees=False)
        self.sc.set_ccw_angle_limit(dynamixel_id, 0, degrees=False)

    def move_raw(self, left, right):
        # Left side
        self.sc.set_speed(Servo.LEFT_FRONT, left)
        self.sc.set_speed(Servo.LEFT_BACK, left)
        # Right side
        self.sc.set_speed(Servo.RIGHT_FRONT, right)
        self.sc.set_speed(Servo.RIGHT_BACK, right)

    def move_raw_left(self, left):
        # Left side
        self.sc.set_speed(Servo.LEFT_FRONT, left)
        self.sc.set_speed(Servo.LEFT_BACK, left)

    def move_raw_right(self, right):
        # Right side
        self.sc.set_speed(Servo.RIGHT_FRONT, right)
        self.sc.set_speed(Servo.RIGHT_BACK, right)

    def move(self, left, right, independent=False):
        # Make sure we don't have any decimals
        left = round(left)
        right = round(right)

        # Different motors need to spin in different directions. We account for that here.
        if (left < 0):
            left *= -1
            left += 1024
        if (right < 0):
            right *= -1
        elif right < 1024:
            right += 1024

        # Only send message if it's different to the last one
        if (independent):
            # Allow left and right to be independent
            if (left != self.last_left):
                self.move_raw_left(left)
            if (right != self.last_right):
                self.move_raw_right(right)
        else:
            # Not independent, both left and right must be different
            if (left != self.last_left and right != self.last_right):
                self.move_raw(left, right)

        # Store this message for comparison next time
        self.last_left = left
        self.last_right = right