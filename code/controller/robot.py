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

from ev3dev2.motor import LargeMotor, SpeedPercent, SpeedRPS
from ev3dev2.sensor.lego import ColorSensor

from controller import config as Config
from controller.odometry import Odometry
from controller.util import clamp, sign
from controller.menu import Menu, Option

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
        angle = math.radians(angleDeg)
        angularVelocity = abs(math.radians(angularVelocityDeg)) * sign(angularVelocityDeg)
        duration = abs(angle / angularVelocity)

        velocity = angularVelocity * (self.odometry.wheelBase / 2)
        velocityRPS = velocity / self.odometry.wheelCircumference

        self.leftMotor.on(SpeedRPS(-velocityRPS), False, False)
        self.rightMotor.on(SpeedRPS(velocityRPS), False, False)

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

    menu = Menu("Title", [
        Option("One", robot.arcAsync),
        Option("Two", robot.arcAsync),
        Option("Three", robot.arcAsync),
        Option("Four", robot.arcAsync),
    ])

    result = menu.inputAsync()

    # robot.moveAsync(150.0, 50.0)
    # robot.printPose()
    # robot.pivotAsync(90.0, 15.0)
    # robot.printPose()

    # time.sleep(3)

    # robot.moveAsync(150.0, -50.0)
    # robot.printPose()
    # robot.pivotAsync(90.0, -15.0)
    # robot.printPose()

    # robot.moveAsync(150.0, 50.0)
    # robot.pivotAsync(90.0, 15.0)
    # robot.printPose()
    # robot.moveAsync(150.0, 50.0)
    # robot.pivotAsync(90.0, 15.0)
    # robot.printPose()
    # robot.moveAsync(150.0, 50.0)
    # robot.pivotAsync(90.0, 15.0)
    # robot.printPose()

    return

if __name__ == "__main__":
    main()