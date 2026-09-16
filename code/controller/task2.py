import math

import config
from robot import Robot

# params
SPEEDS = [30, 50, 70]
STRAIGHT_DISTANCE = 1.0

# helpers
def wheel_degrees(distance):
    circumference = math.pi * config.WHEEL_DIAMETER
    return distance / circumference * 360


def duration(robot, degrees, speed):
    motor_speed = min(
        robot.left_motor.max_speed,
        robot.right_motor.max_speed
    )

    return abs(degrees) / (motor_speed * speed / 100)


def run_straight(robot, speed):
    robot.odometry.reset()

    degrees = wheel_degrees(STRAIGHT_DISTANCE)
    seconds = duration(robot, degrees, speed)

    robot.executeCommand(speed, speed, seconds)


def run_rotation(robot, speed):
    robot.odometry.reset()

    angle = math.radians(360)

    wheel_distance = (
        config.AXLE_LENGTH / 2
    ) * angle

    degrees = wheel_degrees(wheel_distance)
    seconds = duration(robot, degrees, speed)

    robot.executeCommand(-speed, speed, seconds)


def print_pose(robot):
    x, y, theta = robot.odometry.getPose()

    print("x:", round(x, 3))
    print("y:", round(y, 3))
    print("theta:", round(math.degrees(theta), 2))


# main
def main():
    robot = Robot()

    try:
        for speed in SPEEDS:
            for trial in range(3):

                print()
                print("STRAIGHT")
                print("speed:", speed)
                print("trial:", trial + 1)

                input() # WAIT

                run_straight(robot, speed)
                print_pose(robot)
              
                input() # WAIT

                print()
                print("ROTATION")
                print("speed:", speed)
                print("trial:", trial + 1)

                input() # WAIT

                run_rotation(robot, speed)
                print_pose(robot)

                input() # WAIT

    finally:
        robot.stop()


if __name__ == "__main__":
    main()
