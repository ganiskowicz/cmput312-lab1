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

# Written By Matvey Okoneshnikov and Graeme Aniskowicz

# ===================== Modules ===================== #
import sys
import os

sys.path.append(os.path.abspath('../'))
from controller.robot import Robot

# ==================== Constants ==================== #
LINEAR_VELOCITY = 50.0 # mm/s
ANGULAR_VELOCITY = 45.0 # deg/s

STRAIGHT_LINE_DISTANCE = 1000 # mm

CIRCLE_RADIUS = 500 # mm

RECTANGLE_HEIGHT = 500 # mm
RECTANGLE_WIDTH = 1000 # mm

LEMNISCATE_SCALE = 0.5

# ===================== Module ====================== #
def straightLine():
    print("Fix me: Finish Implementation")

    robot = Robot()

    print("Driving...")
    robot.moveAsync(STRAIGHT_LINE_DISTANCE, LINEAR_VELOCITY)

    return

def circle():
    print("Fix me: Finish Implementation")

    robot = Robot()

    print("Driving...")
    robot.arcAsync(360.0, ANGULAR_VELOCITY, CIRCLE_RADIUS)

    return

def rectangle():
    print("Fix me: Finish Implementation")

    robot = Robot()

    print("Driving...")
    for i in range(2):
        robot.moveAsync(RECTANGLE_HEIGHT, LINEAR_VELOCITY)
        robot.pivotAsync(90, ANGULAR_VELOCITY)
        robot.moveAsync(RECTANGLE_WIDTH, LINEAR_VELOCITY)
        robot.pivotAsync(90, ANGULAR_VELOCITY)

    return

def lemniscate():
    print("Fix me: Finish Implementation")

    robot = Robot()

    print("Driving...")
    robot.lemniscateAsync(LEMNISCATE_SCALE, LINEAR_VELOCITY)

    return

def main():
    straightLine()
    # circle()
    # rectangle()
    # lemniscate()

    return

if __name__ == "__main__":
    main()