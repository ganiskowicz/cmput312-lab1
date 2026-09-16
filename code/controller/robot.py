<<<<<<< Updated upstream
import math
import time
import config

from ev3dev2.motor import (
    LargeMotor,
    SpeedPercent
)

from odometry import Odometry

class Robot:
    def __init__(self):
        self.left_motor = LargeMotor(config.LEFT_MOTOR_PORT)
        self.right_motor = LargeMotor(config.RIGHT_MOTOR_PORT)

        self.odometry = Odometry(
            self.left_motor,
            self.right_motor,
            config.WHEEL_DIAMETER,
            config.AXLE_LENGTH,
        )

    def setPower(self, left_power, right_power):
        """
        Set motor powers as percentages (negatives included)
        """

        left_power = max(-100, min(100, left_power))
        right_power = max(-100, min(100, right_power))

        self.left_motor.on(
            SpeedPercent(left_power),
            brake=False,
            block=False
        )

        self.right_motor.on(
            SpeedPercent(right_power),
            brake=False,
            block=False
        )

    def stop(self):
        self.left_motor.off(brake=True)
        self.right_motor.off(brake=True)

    def executeCommand(self, left_power, right_power, duration):
        """
        Execute command while continuously updating odometry.
        """

        self.setPower(left_power, right_power)
        start = time.monotonic()

        while time.monotonic() - start < duration:
            self.odometry.heartbeat()
            time.sleep(HEARTBEAT_PERIOD)

        self.stop()

        # update encoders after stopping
        self.odometry.heartbeat()

    def executeCommands(self, commands):
        """
        Execute commands sequentially
        """

        self.odometry.reset()

        for command in commands:
            left_power, right_power, duration = command

            print(
                "Executing:",
                left_power,
                right_power,
                duration
            )

            self.executeCommand(
                left_power,
                right_power,
                duration
            )

        return self.odometry.getPose()

    def printPose(self):
        x, y, theta = self.odometry.getPose()

        theta_deg = math.degrees(theta)

        print()
        print("Estimated pose:")
        print("x = {:.3f} m".format(x))
        print("y = {:.3f} m".format(y))
        print("theta = {:.2f} deg".format(theta_deg))


def main():
    # testing use only

    commands = [
        [80, 60, 2],
        [60, 60, 1],
        [-50, 80, 2]
    ]

    robot = Robot()

    try:
        robot.executeCommands(commands)
        robot.printPose()

    finally:
        robot.stop()

=======
#!/usr/bin/env python3

"""
Group Members: Matvey Okoneshnikov (okoneshn), Graeme Aniskowicz (ganiskow), Dominik Vrbanek (vrbanek)

Date: September 14th 2026
 
Brick Number: ...

Lab Number: 1

Problem Number: n/a
 
Brief Program/Problem Description: 

	...

Brief Solution Summary:

	Algorithmic idea, underlying theory, etc...

Used Resources/Collaborators:
	...

I/we hereby certify that I/we have produced the following solution 
using only the resources listed above in accordance with the 
CMPUT 312 collaboration policy.
"""

# Written By Graeme Aniskowicz

# ===================== Modules ===================== #
import math
import time
import config as Config

from ev3dev2.motor import LargeMotor, SpeedPercent, SpeedRPS
from ev3dev2.sensor.lego import ColorSensor
from odometry import Odometry
from util import clamp

# ==================== Constants ==================== #

# ===================== Module ====================== #
class Robot:
    def __init__(self):
        self.leftMotor = LargeMotor(Config.LEFT_MOTOR_PORT)
        self.rightMotor = LargeMotor(Config.RIGHT_MOTOR_PORT)

        self.sensorLeft = ColorSensor(Config.LEFT_SENSOR_PORT)
        self.sensorRight = ColorSensor(Config.RIGHT_SENSOR_PORT)

        self.odometry = Odometry(
            self.leftMotor,
            self.rightMotor,
            Config.WHEEL_DIAMETER,
            Config.WHEEL_BASE
        )

        return

    def getPose(self):
        return self.odometry.getPose()

    def printPose(self):
        return self.odometry.printPose()

    def resetPose(self):
        return self.odometry.resetPose()

    def stop(self):
        self.leftMotor.off(brake=True)
        self.rightMotor.off(brake=True)

        return

    def setPower(self, leftPower, rightPower):
        self.leftMotor.on(SpeedPercent(clamp(leftPower, -100, 100)), False, False)
        self.rightMotor.on(SpeedPercent(clamp(rightPower, -100, 100)), False, False)

    def executeCommandAsync(self, leftPower, rightPower, duration):
        self.leftMotor.on(SpeedPercent(clamp(leftPower, -100, 100)), False, False)
        self.rightMotor.on(SpeedPercent(clamp(rightPower, -100, 100)), False, False)

        start = time.monotonic()
        while time.monotonic() - start < duration:
            self.odometry.heartbeat()
            time.sleep(Config.HEARTBEAT_PERIOD / 1000)

        self.stop()
        self.odometry.heartbeat()

        return

    def executeCommandsAsync(self, commands):
        for command in commands:
            leftPower, rightPower, duration = command
            self.executeCommand(leftPower, rightPower, duration)

        return

    def moveAsync(self, distance, velocity=100.0):
        print("Fix me: Direction ill defined")

        velocityRPS = velocity / self.odometry.wheelCircumference
        duration = abs(distance / velocity)

        self.leftMotor.on(SpeedRPS(velocityRPS), False, False)
        self.rightMotor.on(SpeedRPS(velocityRPS), False, False)

        start = time.monotonic()
        while time.monotonic() - start < duration:
            self.odometry.heartbeat()
            time.sleep(Config.HEARTBEAT_PERIOD / 1000)

        self.stop()
        self.odometry.heartbeat()

        return

    def pivotAsync(self, angleDeg, angularVelocityDeg=90.0):
        print("Fix me: Direction ill defined")

        angle = math.radians(angleDeg)
        angularVelocity = math.radians(angularVelocityDeg)
        duration = abs(angle / angularVelocity)

        velocity = angularVelocity * (self.odometry.wheelBase / 2)
        velocityRPS = velocity / self.odometry.wheelCircumference

        self.leftMotor.on(SpeedRPS(velocityRPS), False, False)
        self.rightMotor.on(SpeedRPS(-velocityRPS), False, False)

        start = time.monotonic()
        while time.monotonic() - start < duration:
            self.odometry.heartbeat()
            time.sleep(Config.HEARTBEAT_PERIOD / 1000)

        self.stop()
        self.odometry.heartbeat()

        return

    def arcAsync(self, angleDeg, angularVelocityDeg=90.0, radius=0.0):
        print("Fix me: Needs Implementation")

        # angle = math.radians(angleDeg)
        # angularVelocity = math.radians(angularVelocityDeg)
        # duration = abs(angle / angularVelocity)

        # velocity = angularVelocity * (self.odometry.wheelBase / 2)
        # velocityRPS = velocity / self.odometry.wheelCircumference

        # self.leftMotor.on(SpeedRPS(velocityRPS), False, False)
        # self.rightMotor.on(SpeedRPS(-velocityRPS), False, False)

        # start = time.monotonic()
        # while time.monotonic() - start < duration:
        #     self.odometry.heartbeat()
        #     time.sleep(Config.HEARTBEAT_PERIOD / 1000)

        # self.stop()
        # self.odometry.heartbeat()

        return

    def lemniscateAsync(self, scale, velocity=100.0):
        print("Fix me: Needs Implementation")

        # angle = math.radians(angleDeg)
        # angularVelocity = math.radians(angularVelocityDeg)
        # duration = abs(angle / angularVelocity)

        # velocity = angularVelocity * (self.odometry.wheelBase / 2)
        # velocityRPS = velocity / self.odometry.wheelCircumference

        # self.leftMotor.on(SpeedRPS(velocityRPS), False, False)
        # self.rightMotor.on(SpeedRPS(-velocityRPS), False, False)

        # start = time.monotonic()
        # while time.monotonic() - start < duration:
        #     self.odometry.heartbeat()
        #     time.sleep(Config.HEARTBEAT_PERIOD / 1000)

        # self.stop()
        # self.odometry.heartbeat()

        return

def main():
    robot = Robot()

    robot.moveAsync(150.0, 50.0)
    robot.pivotAsync(90.0, 15.0)
    robot.printPose()
    robot.moveAsync(150.0, 50.0)
    robot.pivotAsync(90.0, 15.0)
    robot.printPose()
    robot.moveAsync(150.0, 50.0)
    robot.pivotAsync(90.0, 15.0)
    robot.printPose()
    robot.moveAsync(150.0, 50.0)
    robot.pivotAsync(90.0, 15.0)
    robot.printPose()

    return
>>>>>>> Stashed changes

if __name__ == "__main__":
    main()