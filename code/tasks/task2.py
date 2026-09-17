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
import sys
import os

sys.path.append(os.path.abspath('../'))
from controller.robot import Robot
from controller.odometry import Pose
from controller.menu import Menu, Option

# ==================== Constants ==================== #
LINEAR_DISTANCE = 250.0 # mm
LINEAR_VELOCITY = 50.0 # mm/s
ANGULAR_OFFSET = 360.0 # deg
ANGULAR_VELOCITY = 45.0 # deg/s

# ===================== Module ====================== #
def linear():
    robot = Robot()

    print("Performing Linear Error Analysis")
    print("The current pose is...")
    robot.printPose()

    print("Driving...")
    robot.moveAsync(LINEAR_DISTANCE, LINEAR_VELOCITY)

    print("The new pose is...")
    robot.printPose()

    print("The error is ...")
    expectedPose = Pose.fromXYA(LINEAR_DISTANCE, 0, 0)
    actualPose = robot.getPose()

    Menu("Straight Line Error", [
        Option("mag: {:7.3f} mm".format(actualPose.getTranslationError(expectedPose)), lambda: None),
        Option("x: {:9.3f} mm".format(actualPose.getXError(expectedPose)), lambda: None),
        Option("y: {:9.3f} mm".format(actualPose.getYError(expectedPose)), lambda: None),
        Option("ang: {:7.3f} deg".format(actualPose.getAngleError(expectedPose) * 180), lambda: None),
    ]).inputAsync()

    return

def angular():
    robot = Robot()

    print("Performing Angular Error Analysis")
    print("The current pose is...")
    robot.printPose()

    print("Driving...")
    robot.pivotAsync(ANGULAR_OFFSET, ANGULAR_VELOCITY)

    print("The new pose is...")
    robot.printPose()

    print("The error is ...")
    expectedPose = Pose.fromXYA(0, 0, 0)
    actualPose = robot.getPose()

    Menu("Rotational Error", [
        Option("mag: {:7.3f} mm".format(actualPose.getTranslationError(expectedPose)), lambda: None),
        Option("x: {:9.3f} mm".format(actualPose.getXError(expectedPose)), lambda: None),
        Option("y: {:9.3f} mm".format(actualPose.getYError(expectedPose)), lambda: None),
        Option("ang: {:7.3f} deg".format(actualPose.getAngleError(expectedPose)), lambda: None),
    ]).inputAsync()

def main():
    running = [True]
    while running[0]:
        Menu("Select Error", [
            Option("Straight Line", linear),
            Option("Rotational", angular),
            Option("Quit", lambda: running.__setitem__(0, False)),
        ]).inputAsync()

    Menu("Done", []).inputAsync()

    return

if __name__ == "__main__":
    main()