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

from ev3dev2.motor import OUTPUT_A, OUTPUT_D
from ev3dev2.sensor import INPUT_4, INPUT_1

# ==================== Constants ==================== #

# ---------- Robot ---------- #
WHEEL_BASE = 165.0 # mm
WHEEL_DIAMETER = 56.0 # mm
WHEEL_CIRCUMFRENCE = math.pi * WHEEL_DIAMETER # mm

LEFT_MOTOR_PORT = OUTPUT_D
RIGHT_MOTOR_PORT = OUTPUT_A

LEFT_SENSOR_PORT = INPUT_4
RIGHT_SENSOR_PORT = INPUT_1

# -------- Alt Robot -------- #
# WHEEL_BASE = 150.0 # mm
# WHEEL_DIAMETER = 43.2 # mm
# WHEEL_CIRCUMFRENCE = math.pi * WHEEL_DIAMETER # mm

# LEFT_MOTOR_PORT = OUTPUT_D
# RIGHT_MOTOR_PORT = OUTPUT_A

# LEFT_SENSOR_PORT = INPUT_4
# RIGHT_SENSOR_PORT = INPUT_1

# -------- Odometry --------- #
HEARTBEAT_PERIOD = 1000.0/120.0 # ms (120 Hz)