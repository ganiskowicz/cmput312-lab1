<<<<<<< Updated upstream
import math
import time


class Odometry:
    """
    Differential-drive odometry.

    Coordinates breakdown:
        x: forward from the starting pose (m)
        y: left from the starting pose (m)
        theta: counter-clockwise positive (rad)
    """

    def __init__(
        self,
        left_motor,
        right_motor,
        wheel_diameter,
        axle_length,
        # if encoders reversed change
        left_encoder_sign=1,
        right_encoder_sign=1
    ):
        self.left_motor = left_motor
        self.right_motor = right_motor

        self.wheel_radius = wheel_diameter / 2.0
        self.axle_length = axle_length

        self.left_encoder_sign = left_encoder_sign
        self.right_encoder_sign = right_encoder_sign

        self.reset()

    def heartbeat(self):
        """
        Read the motor encoders and update the estimated pose.
        """

        now = time.monotonic()

        left_deg = (
            self.left_encoder_sign * self.left_motor.position
        )
        right_deg = (
            self.right_encoder_sign * self.right_motor.position
        )

        dt = now - self.last_time
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
>>>>>>> Stashed changes

        if dt <= 0:
            return

<<<<<<< Updated upstream
        # Encoder change in radians
        delta_left_angle = math.radians(
            left_deg - self.last_left_deg
        )

        delta_right_angle = math.radians(
            right_deg - self.last_right_deg
        )

        # Distance travelled by each wheel
        delta_left = self.wheel_radius * delta_left_angle
        delta_right = self.wheel_radius * delta_right_angle

        # Measured wheel velocities from encoders
        v_left = delta_left / dt
        v_right = delta_right / dt

        # Differential-drive forward kinematics
        v = (v_right + v_left) / 2.0

        omega = (
            v_right - v_left
        ) / self.axle_length

        delta_theta = omega * dt
        delta_distance = v * dt

        old_theta = self.theta
        new_theta = old_theta + delta_theta

        # Exact integration for an arc
        if abs(delta_theta) < 1e-9:
            # Essentially straight
            self.x += delta_distance * math.cos(old_theta)
            self.y += delta_distance * math.sin(old_theta)

        else:
            radius = delta_distance / delta_theta

            self.x += radius * (
                math.sin(new_theta) -
                math.sin(old_theta)
            )

            self.y += -radius * (
                math.cos(new_theta) -
                math.cos(old_theta)
            )

        self.theta = self._wrap_angle(new_theta)

        # Save values for next heartbeat
        self.last_left_deg = left_deg
        self.last_right_deg = right_deg
        self.last_time = now

    def getPose(self):
        """
        Return (x, y, theta).

        x, y in metres
        theta in radians
        """
        return self.x, self.y, self.theta

    def reset(self):
        """
        Reset estimated pose to (0, 0, 0).
        """

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.last_left_deg = (
            self.left_encoder_sign *
            self.left_motor.position
        )

        self.last_right_deg = (
            self.right_encoder_sign *
            self.right_motor.position
        )

        self.last_time = time.monotonic()

    @staticmethod
    def _wrap_angle(angle):
        """
        Wrap radians to (-pi, pi].
        """
        while angle <= -math.pi:
            angle += 2.0 * math.pi

        while angle > math.pi:
            angle -= 2.0 * math.pi

        return angle
=======
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
>>>>>>> Stashed changes
