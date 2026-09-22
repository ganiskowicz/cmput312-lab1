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
import math
import sys
import os

sys.path.append(os.path.abspath('../'))

from controller.robot import Robot
from controller.odometry import Pose
from controller.menu import Menu, Text, Button

# ==================== Constants ==================== #
LINEAR_VELOCITY = 150.0 # mm/s
ANGULAR_VELOCITY = 45.0 # deg/s

STRAIGHT_LINE_DISTANCE = 1000 # mm

CIRCLE_RADIUS = 500 # mm

RECTANGLE_HEIGHT = 500 # mm
RECTANGLE_WIDTH = 1000 # mm

LEMNISCATE_SCALE = 500 # mm

# ===================== Module ====================== #
def straightLine():
    Menu([
        Text("Performing Straight"),
        Text("Line")
    ]).draw()
        
    robot = Robot()

    print("Performing Straight Line")
    print("The current pose is...")
    robot.printPose()

    print("Driving...")
    robot.moveAsync(STRAIGHT_LINE_DISTANCE, LINEAR_VELOCITY)

    print("The new pose is...")
    robot.printPose()

    print("The error is ...")
    expectedPose = Pose.fromXYA(1000, 0, 0)
    actualPose = robot.getPose()

    print("mag: {:7.3f} mm".format(actualPose.getTranslationError(expectedPose)))
    print("x: {:9.3f} mm".format(actualPose.getXError(expectedPose)))
    print("y: {:9.3f} mm".format(actualPose.getYError(expectedPose)))
    print("ang: {:7.3f} deg".format(math.degrees(actualPose.getAngleError(expectedPose))))

    Menu([
        Text("Pose (Line)"),
        Text("x: {:9.3f} mm".format(actualPose.x)),
        Text("y: {:9.3f} mm".format(actualPose.y)),
        Text("ang: {:7.3f} deg".format(math.degrees(actualPose.getWrappedAngle()))),
        Button("Ok", lambda: None),
    ]).inputAsync()

    Menu([
        Text("Error (Line)"),
        Text("mag: {:7.3f} mm".format(actualPose.getTranslationError(expectedPose))),
        Text("x: {:9.3f} mm".format(actualPose.getXError(expectedPose))),
        Text("y: {:9.3f} mm".format(actualPose.getYError(expectedPose))),
        Text("ang: {:7.3f} deg".format(math.degrees(actualPose.getAngleError(expectedPose)))),
        Button("Ok", lambda: None),
    ]).inputAsync()

    return

def circle():
    Menu([
        Text("Performing Circle")
    ]).draw()
        
    robot = Robot()

    print("Performing Circle")
    print("The current pose is...")
    robot.printPose()

    print("Driving...")
    robot.arcAsync(360.0, -ANGULAR_VELOCITY / 5, -CIRCLE_RADIUS)

    print("The new pose is...")
    robot.printPose()

    print("The error is ...")
    expectedPose = Pose.fromXYA(0, 0, 0)
    actualPose = robot.getPose()

    print("mag: {:7.3f} mm".format(actualPose.getTranslationError(expectedPose)))
    print("x: {:9.3f} mm".format(actualPose.getXError(expectedPose)))
    print("y: {:9.3f} mm".format(actualPose.getYError(expectedPose)))
    print("ang: {:7.3f} deg".format(math.degrees(actualPose.getAngleError(expectedPose))))

    Menu([
        Text("Pose (Circle)"),
        Text("x: {:9.3f} mm".format(actualPose.x)),
        Text("y: {:9.3f} mm".format(actualPose.y)),
        Text("ang: {:7.3f} deg".format(math.degrees(actualPose.getWrappedAngle()))),
        Button("Ok", lambda: None),
    ]).inputAsync()

    Menu([
        Text("Error (Circle)"),
        Text("mag: {:7.3f} mm".format(actualPose.getTranslationError(expectedPose))),
        Text("x: {:9.3f} mm".format(actualPose.getXError(expectedPose))),
        Text("y: {:9.3f} mm".format(actualPose.getYError(expectedPose))),
        Text("ang: {:7.3f} deg".format(math.degrees(actualPose.getAngleError(expectedPose)))),
        Button("Ok", lambda: None),
    ]).inputAsync()

    return

def rectangle():
    Menu([
        Text("Performing Rectangle")
    ]).draw()
        
    robot = Robot()

    print("Performing Rectangle")
    print("The current pose is...")
    robot.printPose()

    print("Driving...")
    for i in range(2):
        robot.moveAsync(RECTANGLE_HEIGHT, LINEAR_VELOCITY)
        robot.pivotAsync(90, ANGULAR_VELOCITY)

        robot.moveAsync(RECTANGLE_WIDTH, LINEAR_VELOCITY)
        robot.pivotAsync(90, ANGULAR_VELOCITY)

    print("The new pose is...")
    robot.printPose()

    print("The error is ...")
    expectedPose = Pose.fromXYA(0, 0, 0)
    actualPose = robot.getPose()

    print("mag: {:7.3f} mm".format(actualPose.getTranslationError(expectedPose)))
    print("x: {:9.3f} mm".format(actualPose.getXError(expectedPose)))
    print("y: {:9.3f} mm".format(actualPose.getYError(expectedPose)))
    print("ang: {:7.3f} deg".format(math.degrees(actualPose.getAngleError(expectedPose))))

    Menu([
        Text("Pose (Rectangle)"),
        Text("x: {:9.3f} mm".format(actualPose.x)),
        Text("y: {:9.3f} mm".format(actualPose.y)),
        Text("ang: {:7.3f} deg".format(math.degrees(actualPose.getWrappedAngle()))),
        Button("Ok", lambda: None),
    ]).inputAsync()

    Menu([
        Text("Error (Rectangle)"),
        Text("mag: {:7.3f} mm".format(actualPose.getTranslationError(expectedPose))),
        Text("x: {:9.3f} mm".format(actualPose.getXError(expectedPose))),
        Text("y: {:9.3f} mm".format(actualPose.getYError(expectedPose))),
        Text("ang: {:7.3f} deg".format(math.degrees(actualPose.getAngleError(expectedPose)))),
        Button("Ok", lambda: None),
    ]).inputAsync()

    return

def geronoLemniscateAsync():
    Menu([
        Text("Performing Lemniscate")
    ]).draw()
        
    robot = Robot()

    print("Performing Lemniscate")
    print("The current pose is...")
    robot.printPose()

    print("Driving...")
    robot.geronoLemniscateAsync(LEMNISCATE_SCALE, LINEAR_VELOCITY)

    print("The new pose is...")
    robot.printPose()

    print("The error is ...")
    expectedPose = Pose.fromXYA(0, 0, 0)
    actualPose = robot.getPose()

    print("mag: {:7.3f} mm".format(actualPose.getTranslationError(expectedPose)))
    print("x: {:9.3f} mm".format(actualPose.getXError(expectedPose)))
    print("y: {:9.3f} mm".format(actualPose.getYError(expectedPose)))
    print("ang: {:7.3f} deg".format(math.degrees(actualPose.getAngleError(expectedPose))))

    Menu([
        Text("Pose (Lemniscate)"),
        Text("x: {:9.3f} mm".format(actualPose.x)),
        Text("y: {:9.3f} mm".format(actualPose.y)),
        Text("ang: {:7.3f} deg".format(math.degrees(actualPose.getWrappedAngle()))),
        Button("Ok", lambda: None),
    ]).inputAsync()

    Menu([
        Text("Error (Lemniscate)"),
        Text("mag: {:7.3f} mm".format(actualPose.getTranslationError(expectedPose))),
        Text("x: {:9.3f} mm".format(actualPose.getXError(expectedPose))),
        Text("y: {:9.3f} mm".format(actualPose.getYError(expectedPose))),
        Text("ang: {:7.3f} deg".format(math.degrees(actualPose.getAngleError(expectedPose)))),
        Button("Ok", lambda: None),
    ]).inputAsync()

def bernoulliLemniscateAsync():
    Menu([
        Text("Performing Lemniscate")
    ]).draw()
        
    robot = Robot()

    print("Performing Lemniscate")
    print("The current pose is...")
    robot.printPose()

    print("Driving...")
    robot.bernoulliLemniscateAsync(LEMNISCATE_SCALE, LINEAR_VELOCITY)

    print("The new pose is...")
    robot.printPose()

    print("The error is ...")
    expectedPose = Pose.fromXYA(0, 0, 0)
    actualPose = robot.getPose()

    print("mag: {:7.3f} mm".format(actualPose.getTranslationError(expectedPose)))
    print("x: {:9.3f} mm".format(actualPose.getXError(expectedPose)))
    print("y: {:9.3f} mm".format(actualPose.getYError(expectedPose)))
    print("ang: {:7.3f} deg".format(math.degrees(actualPose.getAngleError(expectedPose))))

    Menu([
        Text("Pose (Lemniscate)"),
        Text("x: {:9.3f} mm".format(actualPose.x)),
        Text("y: {:9.3f} mm".format(actualPose.y)),
        Text("ang: {:7.3f} deg".format(math.degrees(actualPose.getWrappedAngle()))),
        Button("Ok", lambda: None),
    ]).inputAsync()

    Menu([
        Text("Error (Lemniscate)"),
        Text("mag: {:7.3f} mm".format(actualPose.getTranslationError(expectedPose))),
        Text("x: {:9.3f} mm".format(actualPose.getXError(expectedPose))),
        Text("y: {:9.3f} mm".format(actualPose.getYError(expectedPose))),
        Text("ang: {:7.3f} deg".format(math.degrees(actualPose.getAngleError(expectedPose)))),
        Button("Ok", lambda: None),
    ]).inputAsync()

    return

def main():
    running = [True]
    while running[0]:
        Menu([
            Text("Select Shape"),
            Button("Straight Line", straightLine),
            Button("Circle", circle),
            Button("Rectangle", rectangle),
            Button("Lemniscate (Bernoulli)", bernoulliLemniscateAsync),
            Button("Lemniscate (Gerono)", geronoLemniscateAsync),
            Button("Quit", lambda: running.__setitem__(0, False)),
        ]).inputAsync()

    Menu("Done", []).draw()

    return

if __name__ == "__main__":
    main()