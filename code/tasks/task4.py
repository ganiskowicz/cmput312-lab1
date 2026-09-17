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
from controller.odometry import Pose
from controller.menu import Menu, Option

# ==================== Constants ==================== #
COMMANDS = [
    [80, 60, 2],
    [60, 60, 1],
    [-50, 80, 2]
]

# ===================== Module ====================== #
def deadReckoning():
    print("Fix me: Finish Implementation")

    robot = Robot()

    print("Driving...")
    robot.executeCommandsAsync(COMMANDS)

    return

def main():
    deadReckoning()

    return

if __name__ == "__main__":
    main()