#!/usr/bin/env python3

"""
Group Members: Matvey Okoneshnikov (okoneshn), Graeme Aniskowicz (ganiskow), Dominik Vrbanek (vrbanek)

Date: September 14th 2026
 
Brick Number: ...

Lab Number: 1

Problem Number: 3
 
Brief Program/Problem Description: 
    Drive the differential drive robot along four predefined trajectories:
    a straight line, circle, rectangle, and lemniscate.

Brief Solution Summary:
    Each trajectory is constructed using the movement functions we've implemented
    in Robot. Straight lines use moveAsync(), rotations use pivotAsync(),
    circular motion uses arcAsync(), and the lemniscate uses
    lemniscateAsync() with continuously changing wheel velocities.

Used Resources/Collaborators:
    CMPUT 312 Lab 1 materials.

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
from controller.menu import Menu, Text, Button

# ==================== Constants ==================== #
LINEAR_VELOCITY = 50.0 # mm per s
ANGULAR_VELOCITY = 45.0 # deg per s

STRAIGHT_LINE_DISTANCE = 1000 # mm

CIRCLE_RADIUS = 500 # mm

RECTANGLE_HEIGHT = 500 # mm
RECTANGLE_WIDTH = 1000 # mm

LEMNISCATE_SCALE = 0.5

# ===================== Module ====================== #
def straightLine():
    robot = Robot()

    print("Driving straight line...")
    robot.moveAsync(STRAIGHT_LINE_DISTANCE, LINEAR_VELOCITY)
    robot.printPose()

    return

def circle():
    robot = Robot()

    print("Driving circle...")
    robot.arcAsync(360.0, ANGULAR_VELOCITY, CIRCLE_RADIUS)
    robot.printPose()

    return

def rectangle():
    robot = Robot()

    print("Driving rectangle...")
    for i in range(2):
        robot.moveAsync(RECTANGLE_HEIGHT, LINEAR_VELOCITY)
        robot.pivotAsync(90, ANGULAR_VELOCITY)

        robot.moveAsync(RECTANGLE_WIDTH, LINEAR_VELOCITY)
        robot.pivotAsync(90, ANGULAR_VELOCITY)

    robot.printPose()

    return

def lemniscate():
    robot = Robot()

    print("Driving lemniscate...")
    robot.lemniscateAsync(LEMNISCATE_SCALE, LINEAR_VELOCITY)
    robot.printPose()

    return

def main():
    Menu([
        Text("Select Shape"),
        Button("Straight Line", straightLine),
        Button("Circle", circle),
        Button("Rectangle", rectangle),
        Button("Lemniscate", lemniscate),
    ]).inputAsync()

    return

if __name__ == "__main__":
    main()