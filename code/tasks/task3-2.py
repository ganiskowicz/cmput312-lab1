import math
import time

import config
from robot import Robot

# params
SHAPE = "line" # line, circle, lem, rect
DRIVE_SPEED = 0.15
TURN_SPEED = 0.10


def to_power(motor, speed):
    radius = config.WHEEL_DIAMETER / 2
    deg_per_sec = math.degrees(speed / radius)

    return deg_per_sec / motor.max_speed * 100


def drive(robot, left_speed, right_speed, seconds):
    left = to_power(robot.left_motor, left_speed)
    right = to_power(robot.right_motor, right_speed)

    robot.executeCommand(left, right, seconds)


def straight(robot, distance):
    seconds = distance / DRIVE_SPEED

    drive(
        robot,
        DRIVE_SPEED,
        DRIVE_SPEED,
        seconds
    )


def rotate(robot, angle):
    angle = math.radians(angle)

    angular_speed = (
        2 * TURN_SPEED /
        config.AXLE_LENGTH
    )

    seconds = abs(angle) / angular_speed

    if angle > 0:
        drive(
            robot,
            -TURN_SPEED,
            TURN_SPEED,
            seconds
        )
    else:
        drive(
            robot,
            TURN_SPEED,
            -TURN_SPEED,
            seconds
        )


def line(robot):
    print("trying line")
    straight(robot, 1.0)


def circle(robot):
    print("trying circle")

    radius = 0.5

    left = DRIVE_SPEED * (
        radius - config.AXLE_LENGTH / 2
    ) / radius

    right = DRIVE_SPEED * (
        radius + config.AXLE_LENGTH / 2
    ) / radius

    seconds = (
        2 * math.pi * radius /
        DRIVE_SPEED
    )

    drive(robot, left, right, seconds)


def rectangle(robot):
    print("trying rectangle")

    straight(robot, 1.0)
    rotate(robot, 90)

    straight(robot, 0.5)
    rotate(robot, 90)

    straight(robot, 1.0)
    rotate(robot, 90)

    straight(robot, 0.5)
    rotate(robot, 90)


def lemniscate(robot):
    print("trying lemniscate")

    a = 0.5
    speed = 0.12
    u = 0

    dt = config.HEARTBEAT_PERIOD

    while u < 2 * math.pi:

        dx = a * math.cos(u)
        dy = a * math.cos(2 * u)

        ddx = -a * math.sin(u)
        ddy = -2 * a * math.sin(2 * u)

        ds = math.sqrt(
            dx * dx +
            dy * dy
        )

        curvature = (
            dx * ddy -
            dy * ddx
        ) / (ds ** 3)

        left_speed = speed * (
            1 -
            curvature * config.AXLE_LENGTH / 2
        )

        right_speed = speed * (
            1 +
            curvature * config.AXLE_LENGTH / 2
        )

        left = to_power(
            robot.left_motor,
            left_speed
        )

        right = to_power(
            robot.right_motor,
            right_speed
        )

        robot.setPower(left, right)
        robot.odometry.heartbeat()

        u += speed / ds * dt

        time.sleep(dt)

    robot.stop()


def main():
    robot = Robot()

    input() # WAIT

    robot.odometry.reset()

    try:
        if SHAPE == "line":
            line(robot)

        elif SHAPE == "circle":
            circle(robot)

        elif SHAPE == "rect":
            rectangle(robot)

        elif SHAPE == "lem":
            lemniscate(robot)

        else:
            print("womp womp")

        print()
        print("done")
        robot.printPose()

    finally:
        robot.stop()


if __name__ == "__main__":
    main()
