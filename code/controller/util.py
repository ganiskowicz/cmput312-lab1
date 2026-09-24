#!/usr/bin/env python3

"""
Group Members: Graeme Aniskowicz (ganiskow), Matvey Okoneshnikov (okoneshn), Dominik Vrbanek (vrbanek)

Date: September 14th 2026
 
Brick Number: ...

Lab Number: 1

Problem Number: n/a
 
Brief Program/Problem Description: 
	Small module for some convenience functions. Sign and clamp.

Brief Solution Summary:
	n/a

Used Resources/Collaborators:
	n/a

I/we hereby certify that I/we have produced the following solution 
using only the resources listed above in accordance with the 
CMPUT 312 collaboration policy.
"""

# Written By Graeme Aniskowicz

# ==================== Constants ==================== #
MIN = min
MAX = max

# ===================== Module ====================== #
def clamp(n, min, max):
    """
    Clamps a number between min and max
    """
    return MAX(min, MIN(n, max))

def sign(x):
    """
    Returns the sign of a number
    """
    return (x > 0) - (x < 0)