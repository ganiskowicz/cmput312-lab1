#!/usr/bin/env python3
# Part 5 - Convert your differential drive vehicle into a Braitenberg vehicle (10)

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.button import Button
from ev3dev2.display import Display

# Set up the motors and sensors

# Initialize the color sensor 
right_sensor = ColorSensor(INPUT_2)
left_sensor = ColorSensor(INPUT_3)

# Initialize the motors
right_motor = LargeMotor(OUTPUT_B)
left_motor = LargeMotor(OUTPUT_C)

# Set the color sensors to measure the ambient light from a flashlight
right_sensor.mode = 'COL-AMBIENT'
left_sensor.mode = 'COL-AMBIENT'

btn = Button()
display = Display()

# ambient_light_intensity is scaled from 0-100

# Calibration ranges, set by calibrate() before any behavior runs
left_range = (0, 100)
right_range = (0, 100)

def show_text(line1, line2=""):
    display.clear()

    display.text_pixels(
        line1,
        clear_screen=False,
        x=5,
        y=20,
        font='luBS18'
    )

    if line2:
        display.text_pixels(
            line2,
            clear_screen=False,
            x=5,
            y=50,
            font='luBS18'
        )

    display.update()

def wait_for_enter():
    # Wait for a fresh press (avoid catching a press held over from the last screen)
    while btn.enter:
        sleep(0.05)
    while not btn.enter:
        sleep(0.05)
    sleep(0.2)  # debounce


def scale(value, low, high):
    if high == low:
        return 0
    pct = (value - low) / (high - low) * 100
    return max(0, min(100, pct))


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
        if btn.backspace:
            left_motor.off()
            right_motor.off()
            return

        left_intensity = left_sensor.ambient_light_intensity
        right_intensity = right_sensor.ambient_light_intensity

        left_speed = scale(left_intensity, *left_range)
        right_speed = scale(right_intensity, *right_range)

        left_motor.on(SpeedPercent(left_speed))
        right_motor.on(SpeedPercent(right_speed))

        # Brighter light on one side makes that same side's motor spin faster, causing the robot to turn away.

        sleep(0.01)


# 5.2 Aggression
# Each sensor drives the motor on the opposite side; brighter light means faster. The robot charges toward the light.
def aggression():
    while True:
        if btn.backspace:
            left_motor.off()
            right_motor.off()
            return

        left_intensity = left_sensor.ambient_light_intensity
        right_intensity = right_sensor.ambient_light_intensity

        left_speed = scale(right_intensity, *right_range)
        right_speed = scale(left_intensity, *left_range)

        left_motor.on(SpeedPercent(left_speed))
        right_motor.on(SpeedPercent(right_speed))

        # Crossed connections mean the brighter side drives the opposite motor faster, causing the robot to charge toward the light.

        sleep(0.01)


# 5.3 Love
# Each sensor drives the motor on its own side; brighter light means slower. The robot approaches the light and stops in front of it.
def love():
    while True:
        if btn.backspace:
            left_motor.off()
            right_motor.off()
            return

        left_intensity = left_sensor.ambient_light_intensity
        right_intensity = right_sensor.ambient_light_intensity

        left_speed = 100 - scale(left_intensity, *left_range)
        right_speed = 100 - scale(right_intensity, *right_range)

        left_motor.on(SpeedPercent(left_speed))
        right_motor.on(SpeedPercent(right_speed))

        # Inverted speeds (100 - intensity) on direct connections mean the sensor closer to the light slows down its motor, turning the robot toward it.

        sleep(0.01)


# 5.4 Curiosity
# Each sensor drives the motor on the opposite side; brighter light means slower. The robot approaches the light, then turns away and continues exploring.
def curiosity():
    while True:
        if btn.backspace:
            left_motor.off()
            right_motor.off()
            return

        left_intensity = left_sensor.ambient_light_intensity
        right_intensity = right_sensor.ambient_light_intensity

        left_speed = 100 - scale(right_intensity, *right_range)
        right_speed = 100 - scale(left_intensity, *left_range)

        left_motor.on(SpeedPercent(left_speed))
        right_motor.on(SpeedPercent(right_speed))

        # Inverted speeds on crossed connections steer the robot toward the light initially, then past it and away.

        sleep(0.01)



behaviors = [
    ("COWARD", cowardice),
    ("AGGRO", aggression),
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
            sleep(0.3)
        elif btn.up:
            idx = (idx - 1) % len(behaviors)
            show_selection(behaviors[idx][0])
            sleep(0.3)
        elif btn.enter:
            show_text("RUNNING:", behaviors[idx][0])
            sleep(0.5)
            return behaviors[idx][1]
        elif btn.backspace:
            return None
        sleep(0.05)


def main():
    show_text("STARTING", "PART 5")
    sleep(3)
    # Calibrate ONLY ONCE
    calibrate()

    # Keep returning to the behavior-selection menu
    while True:
        selected = choose_behavior()

        if selected is None:
            left_motor.off()
            right_motor.off()
            show_text("STOPPED")
            sleep(1)
            return

        selected()
        
        # Wait for button release to avoid detecting the same press in the menu
        while btn.backspace:
            sleep(0.05)
        sleep(0.2)  # debounce

if __name__ == "__main__":
    main()