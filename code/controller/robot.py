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

# Written By Matvey Okoneshnikov and Graeme Aniskowicz

# ===================== Modules ===================== #
import math
import time
import sys
import os

from ev3dev2.motor import LargeMotor, SpeedPercent, SpeedRPS
from ev3dev2.sensor.lego import ColorSensor

sys.path.append(os.path.abspath('../'))
import controller.config as Config
from controller.odometry import Odometry, Pose
from controller.util import clamp, sign

# ==================== Constants ==================== #

# ===================== Module ====================== #
class Robot:
    def __init__(self):
        self.leftMotor = LargeMotor(Config.LEFT_MOTOR_PORT)
        self.rightMotor = LargeMotor(Config.RIGHT_MOTOR_PORT)

        # self.sensorLeft = ColorSensor(Config.LEFT_SENSOR_PORT)
        # self.sensorRight = ColorSensor(Config.RIGHT_SENSOR_PORT)

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
            self.executeCommandAsync(leftPower, rightPower, duration)

        return

    def moveAsync(self, distance, velocity=100.0):
        if distance == 0 or velocity == 0:
            return

        direction = sign(distance) * sign(velocity)
        velocity = abs(velocity) * direction

        velocityRPS = velocity / self.odometry.wheelCircumference
        duration = abs(distance) / abs(velocity)

        self.leftMotor.on(SpeedRPS(velocityRPS), False, False)
        self.rightMotor.on(SpeedRPS(velocityRPS), False, False)

        start = time.monotonic()
        while time.monotonic() - start < duration:
            # Odometry
            self.odometry.heartbeat()
            time.sleep(Config.HEARTBEAT_PERIOD / 1000)

        self.stop()
        self.odometry.heartbeat()

        return

    def pivotAsync(self, angleDeg, angularVelocityDeg=90.0):
        return self.arcAsync(angleDeg, angularVelocityDeg, 0.0)

    def arcAsync(self, angleDeg, angularVelocityDeg=90.0, radius=0.0):
        angle = math.radians(angleDeg)
        angularVelocity = math.radians(angularVelocityDeg)
        duration = abs(angle / angularVelocity)

        velocityLeft = angularVelocity * (radius - self.odometry.wheelBase / 2)
        velocityLeftRPS = velocityLeft / self.odometry.wheelCircumference

        velocityRight = angularVelocity * (radius + self.odometry.wheelBase / 2)
        velocityRightRPS = velocityRight / self.odometry.wheelCircumference

        self.leftMotor.on(SpeedRPS(velocityLeftRPS), False, False)
        self.rightMotor.on(SpeedRPS(velocityRightRPS), False, False)

        start = time.monotonic()
        while time.monotonic() - start < duration:
            # Odometry
            self.odometry.heartbeat()
            time.sleep(Config.HEARTBEAT_PERIOD / 1000)

        self.stop()
        self.odometry.heartbeat()

        return

    def bernoulliLemniscateAsync(self, scale, velocity=100.0):
        # offset by math.pi / 2 to start in centre
        a = scale
        u = 0.0
        last = time.monotonic()
        while u < 2 * math.pi:
            # Get the Curvature of the curve at u, i.e. d(angle)/ds at u where s is the distance along the curve.
            curvature = (3 * math.cos(u)) / (a * math.sqrt(1 + math.sin(u)**2))

            # Get the Anugular Velocity
            angularVelocity = velocity * curvature
            # radius = velocity / angularVelocity = 1 / dads

            # Set Velocity
            # Simplified from arcAsync, radius not expicitly needed since radius is a function of velocity and angular velocity. Calculating radius could also lead to a divide by zero if curvature is zero.
            velocityLeft = velocity - angularVelocity * self.odometry.wheelBase / 2
            velocityLeftRPS = velocityLeft / self.odometry.wheelCircumference
    
            velocityRight = velocity + angularVelocity * self.odometry.wheelBase / 2
            velocityRightRPS = velocityRight / self.odometry.wheelCircumference
    
            self.leftMotor.on(SpeedRPS(velocityLeftRPS), False, False)
            self.rightMotor.on(SpeedRPS(velocityRightRPS), False, False)

            # Wait
            time.sleep(Config.HEARTBEAT_PERIOD / 1000)

            # Get dt from elapsed
            current = time.monotonic()
            dt = current - last
            last = current

            # Get du to increment u at a constant linear velocity v
            du = (velocity / scale) * math.sqrt(1 + math.sin(u)**2) * dt
            u += du

            self.odometry.heartbeat()

        self.stop()
        self.odometry.heartbeat()

        return

    def geronoLemniscateAsync(self, scale, velocity=100.0):
        a = scale
        u = 0.0
        last = time.monotonic()
        while u < 2 * math.pi:
            # Gerono lemniscate:
            #   x = a sin(u)
            #   y = a sin(u) cos(u)

            dx = a * math.cos(u)
            dy = a * math.cos(2 * u)

            ddx = -a * math.sin(u)
            ddy = -2 * a * math.sin(2 * u)

            ds = math.sqrt(dx * dx + dy * dy)

            # Curvature of a parametric curve
            curvature = (
                dx * ddy - dy * ddx
            ) / (ds ** 3)

            leftVelocity = velocity * (
                1 - curvature * self.odometry.wheelBase / 2
            )

            rightVelocity = velocity * (
                1 + curvature * self.odometry.wheelBase / 2
            )

            leftRPS = leftVelocity / self.odometry.wheelCircumference
            rightRPS = rightVelocity / self.odometry.wheelCircumference

            self.leftMotor.on(SpeedRPS(leftRPS), False, False)
            self.rightMotor.on(SpeedRPS(rightRPS), False, False)

            # wait
            time.sleep(Config.HEARTBEAT_PERIOD / 1000)

            # get dt
            current = time.monotonic()
            dt = current - last
            last = current

            # advance at constant linear velocity
            u += abs(velocity) / ds * dt

            self.odometry.heartbeat()

        self.stop()
        self.odometry.heartbeat()

        return

def main():
    robot = Robot()

    print("Performing General Error Test")
    print("The current pose is...")
    robot.printPose()

    print("Driving...")
    robot.moveAsync(150.0, 50.0)
    robot.printPose()
    robot.pivotAsync(90.0, 15.0)
    robot.printPose()
    time.sleep(3)
    robot.moveAsync(150.0, -50.0)
    robot.printPose()
    robot.pivotAsync(90.0, -15.0)
    robot.printPose()

    print("The new pose is...")
    robot.printPose()

    print("The error is ...")
    expectedPose = Pose.fromXYA(150, -150, 0)
    actualPose = robot.getPose()

    print("mag: {:7.3f} mm".format(actualPose.getTranslationError(expectedPose)))
    print("x: {:9.3f} mm".format(actualPose.getXError(expectedPose)))
    print("y: {:9.3f} mm".format(actualPose.getYError(expectedPose)))
    print("ang: {:7.3f} deg".format(actualPose.getAngleError(expectedPose) * 180))
    
    return

if __name__ == "__main__":
    main()