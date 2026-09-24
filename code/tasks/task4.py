#!/usr/bin/env python3

"""
Group Members: Matvey Okoneshnikov (okoneshn), Graeme Aniskowicz (ganiskow), Dominik Vrbanek (vrbanek)

Date: September 14th 2026
 
Brick Number: ...

Lab Number: 1

Problem Number: 4
 
Brief Program/Problem Description: 

	Executes a predefined sequence of differential-drive motor commands while
    estimating the robot's final pose using dead reckoning. The resulting
    encoder-based position and orientation estimate is then displayed for
    comparison with the robot's measured final pose.


Brief Solution Summary:

	The program creates a Robot object and executes a sequence of left and
    right motor power commands for specified durations using executeCommandsAsync(). 
    During execution, the Robot class continuously updates its Odometry object 
    from the wheel encoder measurements.

    After the command sequence is complete, the estimated pose is retrieved from the odometry system 
    and displayed in both the terminal and on the EV3 screen. The implementation relies 
    on the dead-reckoning model in the Odometry class, where wheel encoder changes are converted into left and
    right wheel motion and integrated using the differential-drive kinematic model to estimate x, y, 
    and orientation over time.


Used Resources/Collaborators:
	...

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
COMMANDS = [
    [80, 60, 2],
    [60, 60, 1],
    [-50, 80, 2]
]

# ===================== Module ====================== #
def deadReckoning():
    Menu([
        Text("Performing Dead Reckoning")
    ]).draw()
        
    robot = Robot()

    print("Performing Dead Reckoning")
    print("The current pose is...")
    robot.printPose()

    print("Driving...")
    robot.executeCommandsAsync(COMMANDS)

    print("The new pose is...")
    robot.printPose()

    print("The error is ...")
    expectedPose = Pose.fromXYA(1000, 0, 0)
    actualPose = robot.getPose()

    print("mag: {:7.3f} mm".format(actualPose.getTranslationError(expectedPose)))
    print("x: {:9.3f} mm".format(actualPose.getXError(expectedPose)))
    print("y: {:9.3f} mm".format(actualPose.getYError(expectedPose)))
    print("ang: {:7.3f} deg".format(actualPose.getAngleError(expectedPose) * 180))

    Menu([
        Text("Pose (Estimate)"),
        Text("x: {:9.3f} mm".format(actualPose.x)),
        Text("y: {:9.3f} mm".format(actualPose.y)),
        Text("ang: {:7.3f} deg".format(math.degrees(actualPose.getWrappedAngle()))),
        Button("Ok", lambda: None),
    ]).inputAsync()

    return

def main():
    running = [True]
    while running[0]:
        Menu([
            Text("Select Program"),
            Button("Dead Reckoning", deadReckoning),
            Button("Quit", lambda: running.__setitem__(0, False)),
        ]).inputAsync()

    Menu("Done", []).draw()

    return

if __name__ == "__main__":
    main()