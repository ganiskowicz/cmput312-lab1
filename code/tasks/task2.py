#!/usr/bin/env python3

"""
Group Members: Matvey Okoneshnikov (okoneshn), Graeme Aniskowicz (ganiskow), Dominik Vrbanek (vrbanek)

Date: September 14th 2026
 
Brick Number: ...

Lab Number: 1

Problem Number: 2
 
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
import sys
import os

sys.path.append(os.path.abspath('../'))
from controller.robot import Robot
from controller.odometry import Pose
from controller.menu import Menu, Text, Button

# ==================== Constants ==================== #
LINEAR_DISTANCE = 500.0 # mm
LINEAR_VELOCITY = 270.0 # mm/s
ANGULAR_OFFSET = 360.0 # deg
ANGULAR_VELOCITY = 180.0 # deg/s

# ===================== Module ====================== #
velocityMultiplier = 1

def setVelocityMultiplier(multiplier):
    global velocityMultiplier
    velocityMultiplier = multiplier

def linear():
    Menu([
        Text("Performing Linear"),
        Text("Error Analysis")
    ]).draw()

    robot = Robot()

    print("Performing Linear Error Analysis")
    print("The current pose is...")
    robot.printPose()

    print("Driving...")
    robot.moveAsync(LINEAR_DISTANCE, LINEAR_VELOCITY * velocityMultiplier)

    print("The new pose is...")
    robot.printPose()

    print("The error is ...")
    expectedPose = Pose.fromXYA(LINEAR_DISTANCE, 0, 0)
    actualPose = robot.getPose()

    print("mag: {:7.3f} mm".format(actualPose.getTranslationError(expectedPose)))
    print("x: {:9.3f} mm".format(actualPose.getXError(expectedPose)))
    print("y: {:9.3f} mm".format(actualPose.getYError(expectedPose)))
    print("ang: {:7.3f} deg".format(actualPose.getAngleError(expectedPose) * 180))

    Menu([
        Text("Pose (Linear)"),
        Text("x: {:9.3f} mm".format(actualPose.x)),
        Text("y: {:9.3f} mm".format(actualPose.y)),
        Text("ang: {:7.3f} deg".format(180 - (180 - math.degrees(actualPose.angle)) % 360)),
        Button("Ok", lambda: None),
    ]).inputAsync()

    Menu([
        Text("Error (Linear)"),
        Text("mag: {:7.3f} mm".format(actualPose.getTranslationError(expectedPose))),
        Text("x: {:9.3f} mm".format(actualPose.getXError(expectedPose))),
        Text("y: {:9.3f} mm".format(actualPose.getYError(expectedPose))),
        Text("ang: {:7.3f} deg".format(actualPose.getAngleError(expectedPose) * 180)),
        Button("Ok", lambda: None),
    ]).inputAsync()

    return

def angular():
    Menu([
        Text("Performing Angular"),
        Text("Error Analysis")
    ]).draw()
        
    robot = Robot()

    print("Performing Angular Error Analysis")
    print("The current pose is...")
    robot.printPose()

    print("Driving...")
    robot.pivotAsync(ANGULAR_OFFSET, ANGULAR_VELOCITY * velocityMultiplier)

    print("The new pose is...")
    robot.printPose()

    print("The error is ...")
    expectedPose = Pose.fromXYA(0, 0, 0)
    actualPose = robot.getPose()

    print("mag: {:7.3f} mm".format(actualPose.getTranslationError(expectedPose)))
    print("x: {:9.3f} mm".format(actualPose.getXError(expectedPose)))
    print("y: {:9.3f} mm".format(actualPose.getYError(expectedPose)))
    print("ang: {:7.3f} deg".format(actualPose.getAngleError(expectedPose) * 180))

    Menu([
        Text("Pose (Angular)"),
        Text("x: {:9.3f} mm".format(actualPose.x)),
        Text("y: {:9.3f} mm".format(actualPose.y)),
        Text("ang: {:7.3f} deg".format(180 - (180 - math.degrees(actualPose.angle)) % 360)),
        Button("Ok", lambda: None),
    ]).inputAsync()

    Menu([
        Text("Error (Angular)"),
        Text("mag: {:7.3f} mm".format(actualPose.getTranslationError(expectedPose))),
        Text("x: {:9.3f} mm".format(actualPose.getXError(expectedPose))),
        Text("y: {:9.3f} mm".format(actualPose.getYError(expectedPose))),
        Text("ang: {:7.3f} deg".format(actualPose.getAngleError(expectedPose) * 180)),
        Button("Ok", lambda: None),
    ]).inputAsync()

def main():
    running = [True]
    while running[0]:
        Menu([
            Text("Select Speed"),
            Button("33%", lambda: setVelocityMultiplier(1/3)),
            Button("66%", lambda: setVelocityMultiplier(2/3)),
            Button("100%", lambda: setVelocityMultiplier(1)),
            Button("Quit", lambda: running.__setitem__(0, False)),
        ]).inputAsync()
        if (not running[0]): break

        Menu([
            Text("Select Error"),
            Button("Linear", linear),
            Button("Angular", angular),
            Button("Quit", lambda: running.__setitem__(0, False)),
        ]).inputAsync()
        if (not running[0]): break

    Menu("Done", []).draw()

    return

if __name__ == "__main__":
    main()