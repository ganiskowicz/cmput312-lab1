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

# ==================== Constants ==================== #
LINEAR_DISTANCE = 250.0 # mm
LINEAR_VELOCITY = 50.0 # mm/s
ANGULAR_OFFSET = 360.0 # deg
ANGULAR_VELOCITY = 45.0 # deg/s

# ===================== Module ====================== #
def linear():
    print("Fix me: Finish Implementation")

    robot = Robot()

    print("Performing Straight-Line Error Analysis")
    print("The current pose is...")
    robot.printPose()

    print("Driving...")
    robot.moveAsync(LINEAR_DISTANCE, LINEAR_VELOCITY)

    print("The new pose is...")
    robot.printPose()

    print("The error is ...")
    # Error Calculation Formula

    return

def rotational():
    print("Fix me: Finish Implementation")

    robot = Robot()

    print("Performing Rotational Error Analysis")
    print("The current pose is...")
    robot.printPose()

    print("Driving...")
    robot.pivotAsync(ANGULAR_OFFSET, ANGULAR_VELOCITY)

    print("The new pose is...")
    robot.printPose()

    print("The error is ...")
    # Error Calculation Formula

    return

def main():
    linear()
    # rotational()

    return

if __name__ == "__main__":
    main()