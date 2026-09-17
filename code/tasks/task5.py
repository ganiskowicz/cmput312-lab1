#!/usr/bin/env python3

"""
Group Members: Matvey Okoneshnikov (okoneshn), Graeme Aniskowicz (ganiskow), Dominik Vrbanek (vrbanek)

Date: September 14th 2026
 
Brick Number: ...

Lab Number: 1

Problem Number: 5
 
Brief Program/Problem Description: 

	Convert the differential drive vehicle into a Braitenberg vehicle with
	calibration and a behavior-selection menu.

Brief Solution Summary:

	Use ambient-light measurements from the left and right sensors to map the
	light intensity into motor speeds. Each behavior selects a different
	combination of direct/crossed and direct/inverted drive logic.

Used Resources/Collaborators:
	... 

I/we hereby certify that I/we have produced the following solution 
using only the resources listed above in accordance with the 
CMPUT 312 collaboration policy.
"""

# Written By Dominik Vrbanek

print("Task 5 starting...")
# ===================== Modules ===================== #
import time
import sys
import os

from ev3dev2.button import Button
from ev3dev2.display import Display

sys.path.append(os.path.abspath('../'))
from controller.robot import Robot
from controller import config as Config

# ==================== Constants ==================== #
# Set up the robot, display and buttons

robot = Robot()
btn = Button()
display = Display()

# Set the color sensors to measure ambient light from a flashlight
left_sensor = robot.sensorLeft
right_sensor = robot.sensorRight

# Calibration ranges, set by calibrate() before any behavior runs
left_range = (0, 100)
right_range = (0, 100)

# ===================== Module ====================== #
# Module to show text on the display for the menu
def show_text(line1, line2=""):
    display.clear()
    display.text_pixels(line1, clear_screen=False, x=5, y=20, font='luBS18')
    if line2:
        display.text_pixels(line2, clear_screen=False, x=5, y=50, font='luBS18')
    display.update()

# Wait for a fresh press (avoid catching a press held over from the last screen)
def wait_for_enter():
    while btn.enter:
        time.sleep(0.05)
    while not btn.enter:
        time.sleep(0.05)
    time.sleep(0.2)

# brickrun grabs the Back/backspace button as the system-level stop button and sends your process a termination signal.
# so will just use the left button instead of the backspace button to stop the robot and go back to the menu.
# comment it out when ready
def wait_for_backspace():
    while btn.backspace:
        time.sleep(0.05)
    while not btn.backspace:
        time.sleep(0.05)
    time.sleep(0.2)

# Scale a value from a range to 0-100 - used for the light calibration
def scale(value, low, high):
    if high == low:
        return 0
    pct = (value - low) / (high - low) * 100
    return max(0, min(100, pct))

# Calibrate the light sensors
def calibrate():
    global left_range, right_range

    show_text("CALIBRATION", "1: NO LIGHT")
    wait_for_enter()

    left_low = left_sensor.ambient_light_intensity
    right_low = right_sensor.ambient_light_intensity

    show_text("CALIBRATION", "2: LIGHT")
    wait_for_enter()

    left_high = left_sensor.ambient_light_intensity
    right_high = right_sensor.ambient_light_intensity

    left_range = (left_low, left_high)
    right_range = (right_low, right_high)

    show_text("CALIBRATED", "Press ENTER")
    wait_for_enter()


# 5.1 Cowardice
# Each sensor drives the motor on its own side; brighter light means faster. The robot runs away from the light.
def cowardice():
    while True:
        if btn.left:
            robot.stop()
            return

        left_intensity = left_sensor.ambient_light_intensity
        right_intensity = right_sensor.ambient_light_intensity

        left_speed = scale(left_intensity, *left_range)
        right_speed = scale(right_intensity, *right_range)

        robot.setPower(left_speed, right_speed)
        time.sleep(0.01)


# 5.2 Aggression
# Each sensor drives the motor on the opposite side; brighter light means faster. The robot charges toward the light.
def aggression():
    while True:
        if btn.left:
            robot.stop()
            return

        left_intensity = left_sensor.ambient_light_intensity
        right_intensity = right_sensor.ambient_light_intensity

        left_speed = scale(right_intensity, *right_range)
        right_speed = scale(left_intensity, *left_range)

        robot.setPower(left_speed, right_speed)
        time.sleep(0.01)


# 5.3 Love
# Each sensor drives the motor on its own side; brighter light means slower. The robot approaches the light and stops in front of it.
def love():
    while True:
        if btn.left:
            robot.stop()
            return

        left_intensity = left_sensor.ambient_light_intensity
        right_intensity = right_sensor.ambient_light_intensity

        left_speed = 100 - scale(left_intensity, *left_range)
        right_speed = 100 - scale(right_intensity, *right_range)

        robot.setPower(left_speed, right_speed)
        time.sleep(0.01)


# 5.4 Curiosity
# Each sensor drives the motor on the opposite side; brighter light means slower. The robot approaches the light, then turns away and continues exploring.
def curiosity():
    while True:
        if btn.left:
            robot.stop()
            return

        left_intensity = left_sensor.ambient_light_intensity
        right_intensity = right_sensor.ambient_light_intensity

        left_speed = 100 - scale(right_intensity, *right_range)
        right_speed = 100 - scale(left_intensity, *left_range)

        robot.setPower(left_speed, right_speed)
        time.sleep(0.01)


behaviors = [
    ("COWARDICE", cowardice),
    ("AGGRESSION", aggression),
    ("LOVE", love),
    ("CURIOUS", curiosity),
]


def show_selection(label):
    show_text("SELECT:", label)


def choose_behavior():
    idx = 0
    show_selection(behaviors[idx][0])

    while True:
        if btn.down:
            idx = (idx + 1) % len(behaviors)
            show_selection(behaviors[idx][0])
            time.sleep(0.3)
        elif btn.up:
            idx = (idx - 1) % len(behaviors)
            show_selection(behaviors[idx][0])
            time.sleep(0.3)
        elif btn.enter:
            show_text("RUNNING:", behaviors[idx][0])
            time.sleep(0.5)
            return behaviors[idx][1]
        elif btn.left:
            while btn.left:
                time.sleep(0.05)
            return None
        time.sleep(0.05)


def main():
    show_text("STARTING", "PART 5")
    time.sleep(3)
    calibrate()

    while True:
        selected = choose_behavior()

        if selected is None:
            robot.stop()
            show_text("STOPPED")
            time.sleep(1)
            return

        selected()

        while btn.left:
            time.sleep(0.05)
        time.sleep(0.2)


if __name__ == "__main__":
    main()