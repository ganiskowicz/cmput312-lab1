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

from ev3dev2.motor import LargeMotor

# ==================== Constants ==================== #

# ===================== Module ====================== #
class Pose:
    def __init__(self, leftTicks, rightTicks, x=0, y=0, angle=0, time=time.monotonic()):
        print("Fix me: Reference frame unclear")

        self.x = x
        self.y = y
        self.angle = angle

        self.time = time
        self.leftTicks = leftTicks
        self.rightTicks = rightTicks

        return

    def __str__(self):
        angleDegrees = 180 - (180 - math.degrees(self.pose.angle)) % 360
        return f"x = {self.pose.x:9.3f} mm, y = {self.pose.y:9.3f} mm, angle = {angleDegrees:7.2f}°"

    def fromPose(self, pose):
        self.x = pose.x
        self.y = pose.y
        self.angle = pose.angle

        self.time = pose.time
        self.leftTicks = pose.leftTicks
        self.rightTicks = pose.rightTicks

        return

class Odometry:
    def __init__(self, leftMotor, rightMotor, wheelDiameter, wheelBase):
        self.leftMotor = leftMotor
        self.rightMotor = rightMotor

        self.wheelDiameter = wheelDiameter
        self.wheelBase = wheelBase

        self.wheelRadius = wheelDiameter / 2.0
        self.wheelCircumference = wheelDiameter * math.pi

        self.pose = Pose(self.leftMotor.position, self.rightMotor.position)
        self.reset()

        return

    def heartbeat(self):
        oldPose = self.pose
        newTime = time.monotonic()
        dt = newTime - oldPose.time

        if dt <= 0:
            return

        newLeftTicks = self.leftMotor.position
        newRightTicks = self.rightMotor.position

        leftTickDelta = newLeftTicks - oldPose.leftTicks
        rightTickDelta = newRightTicks - oldPose.rightTicks

        leftDelta = float(leftTickDelta) / float(self.leftMotor.count_per_rot) * self.wheelCircumference # mm
        rightDelta = float(rightTickDelta) / float(self.rightMotor.count_per_rot) * self.wheelCircumference # mm

        leftVelocity = leftDelta / dt # mm/s
        rightVelocity = rightDelta / dt # mm/s

        linearVelocity = (leftVelocity + rightVelocity) / 2 # mm/s
        angularVelocity = (rightVelocity - leftVelocity) / self.wheelBase # rad/s

        angleDelta = angularVelocity * dt
        newAngle = oldPose.angle + angleDelta

        xDelta, yDelta = 0, 0
        if abs(angularVelocity) < 1e-9:
            # Large Arc, Do Not Divide By Zero. Fine To Approximate Arc As Line.
            xDelta = linearVelocity * dt * math.cos(oldPose.angle)
            yDelta = linearVelocity * dt * math.sin(oldPose.angle)
        else:
            # Exact Arc Integration
            xDelta = (linearVelocity / angularVelocity) * (math.sin(newAngle) - math.sin(oldPose.angle))
            yDelta = (linearVelocity / angularVelocity) * (math.cos(newAngle) - math.cos(oldPose.angle))

        newX = oldPose.x + xDelta
        newY = oldPose.y + yDelta

        newPose = Pose(newLeftTicks, newRightTicks, newX, newY, newAngle, newTime)
        self.pose = newPose

        return

    def getPose(self):
        return Pose.fromPose(self.pose)

    def printPose(self):
        print(self.pose)

        return

    def resetPose(self):
        self.pose = Pose(self.leftMotor.position, self.rightMotor.position)

        return