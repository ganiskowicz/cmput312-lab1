#!/usr/bin/env python3

"""
Group Members: Matvey Okoneshnikov (okoneshn), Graeme Aniskowicz (ganiskow), Dominik Vrbanek (vrbanek)

Date: September 14th 2026
 
Brick Number: ...

Lab Number: 1

Problem Number: n/a
 
Brief Program/Problem Description: 
    This is the base Odometry class used for tracking the robots pose as a function 
    of ticks on the left and right wheel encoders. When a new Odometry class through Robot, 
    the pose defaults to x = 0, y = 0, theta = 0. Pose is another class which tracks not just
    position data, but time data and ticks. Calling the heartbeat function will update the pose
    using the information available. It is to be called at the rate of the heartbeat period.

    The pose class provides some useful methods for digesting the info.

Brief Solution Summary:
    Pose stores time so the Odometry class is able to calculate the delta time between the last 
    calculated pose and the new pose that is currently being calculated. This gives us dt. The
    Pose also stores left and right encoder ticks. This means the Odometry class can calculate 
    the delta in encoder ticks for each side. These quantities together are enough to approximate
    the wheel velocities using a finite difference calculation (the backward difference in particular).
    calling the hearbeat function as a high rate (such as 120Hz) ensures that the backward difference
    approximation of the wheel velocity is acurate.

    Using the approximated velocity, we integrate wrt time to get the updated pose.

    Coordinate frame, sign convension, reference point, units, other quantities and full
    derivations are defined in the lab report. 

Used Resources/Collaborators:
    CMPUT 312 Slide materials
	https://en.wikipedia.org/wiki/Finite_difference

I/we hereby certify that I/we have produced the following solution 
using only the resources listed above in accordance with the 
CMPUT 312 collaboration policy.
"""

# Written By Matvey Okoneshnikov and Graeme Aniskowicz

# ===================== Modules ===================== #
import math
import time

from ev3dev2.motor import LargeMotor

# ==================== Constants ==================== #

# ===================== Module ====================== #
class Pose:
    def __init__(self, leftTicks, rightTicks, time, x=0, y=0, angle=0):
        self.x = x
        self.y = y
        self.angle = angle

        self.time = time
        self.leftTicks = leftTicks
        self.rightTicks = rightTicks

        return

    def __str__(self):
        return "x = {:9.3f} mm, y = {:9.3f} mm, angle = {:7.2f} deg".format(self.x, self.y, math.degrees(self.getWrappedAngle()))

    def fromPose(pose):
        copy = Pose(pose.leftTicks, pose.rightTicks, pose.time, pose.x, pose.y, pose.angle)
        return copy

    def fromXYA(x=0, y=0, angle=0):
        pose = Pose(0, 0, time.monotonic(), x, y, angle)
        return pose

    def getTranslationError(self, expected):
        return math.sqrt((self.x - expected.x)**2 + (self.y - expected.y)**2)

    def getXError(self, expected):
        return self.x - expected.x

    def getYError(self, expected):
        return self.y - expected.y

    def getAngleError(self, expected):
        return self.angle - expected.angle

    def getWrappedAngle(self):
        wrapped = math.pi - (math.pi - math.degrees(self.angle)) % (math.pi * 2)
        return wrapped

class Odometry:
    def __init__(self, leftMotor, rightMotor, wheelDiameter, axleLength):
        self.leftMotor = leftMotor
        self.rightMotor = rightMotor

        self.wheelDiameter = wheelDiameter
        self.axleLength = axleLength

        self.wheelRadius = wheelDiameter / 2.0
        self.wheelCircumference = wheelDiameter * math.pi

        self.pose = Pose(self.leftMotor.position, self.rightMotor.position, time.monotonic())
        self.resetPose()

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
        angularVelocity = (rightVelocity - leftVelocity) / self.axleLength # rad/s

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
            yDelta = (linearVelocity / angularVelocity) * (math.cos(oldPose.angle) - math.cos(newAngle))

        newX = oldPose.x + xDelta
        newY = oldPose.y + yDelta

        newPose = Pose(newLeftTicks, newRightTicks, newTime, newX, newY, newAngle)
        self.pose = newPose

        return

    def getPose(self):
        return Pose.fromPose(self.pose)

    def printPose(self):
        print(self.pose)
        return

    def resetPose(self):
        self.pose = Pose(self.leftMotor.position, self.rightMotor.position, time.monotonic())
        return