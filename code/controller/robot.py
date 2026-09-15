import math
import time
import config

from ev3dev2.motor import (
    LargeMotor,
    SpeedPercent
)

from odometry import Odometry

class Robot:
    def __init__(self):
        self.left_motor = LargeMotor(config.LEFT_MOTOR_PORT)
        self.right_motor = LargeMotor(config.RIGHT_MOTOR_PORT)

        self.odometry = Odometry(
            self.left_motor,
            self.right_motor,
            config.WHEEL_DIAMETER,
            config.AXLE_LENGTH,
        )

    def setPower(self, left_power, right_power):
        """
        Set motor powers as percentages (negatives included)
        """

        left_power = max(-100, min(100, left_power))
        right_power = max(-100, min(100, right_power))

        self.left_motor.on(
            SpeedPercent(left_power),
            brake=False,
            block=False
        )

        self.right_motor.on(
            SpeedPercent(right_power),
            brake=False,
            block=False
        )

    def stop(self):
        self.left_motor.off(brake=True)
        self.right_motor.off(brake=True)

    def executeCommand(self, left_power, right_power, duration):
        """
        Execute command while continuously updating odometry.
        """

        self.setPower(left_power, right_power)
        start = time.monotonic()

        while time.monotonic() - start < duration:
            self.odometry.heartbeat()
            time.sleep(HEARTBEAT_PERIOD)

        self.stop()

        # update encoders after stopping
        self.odometry.heartbeat()

    def executeCommands(self, commands):
        """
        Execute commands sequentially
        """

        self.odometry.reset()

        for command in commands:
            left_power, right_power, duration = command

            print(
                "Executing:",
                left_power,
                right_power,
                duration
            )

            self.executeCommand(
                left_power,
                right_power,
                duration
            )

        return self.odometry.getPose()

    def printPose(self):
        x, y, theta = self.odometry.getPose()

        theta_deg = math.degrees(theta)

        print()
        print("Estimated pose:")
        print("x = {:.3f} m".format(x))
        print("y = {:.3f} m".format(y))
        print("theta = {:.2f} deg".format(theta_deg))


def main():
    # testing use only

    commands = [
        [80, 60, 2],
        [60, 60, 1],
        [-50, 80, 2]
    ]

    robot = Robot()

    try:
        robot.executeCommands(commands)
        robot.printPose()

    finally:
        robot.stop()


if __name__ == "__main__":
    main()