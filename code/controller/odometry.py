import math
import time


class Odometry:
    """
    Differential-drive odometry.

    Coordinates breakdown:
        x: forward from the starting pose (m)
        y: left from the starting pose (m)
        theta: counter-clockwise positive (rad)
    """

    def __init__(
        self,
        left_motor,
        right_motor,
        wheel_diameter,
        axle_length,
        # if encoders reversed change
        left_encoder_sign=1,
        right_encoder_sign=1
    ):
        self.left_motor = left_motor
        self.right_motor = right_motor

        self.wheel_radius = wheel_diameter / 2.0
        self.axle_length = axle_length

        self.left_encoder_sign = left_encoder_sign
        self.right_encoder_sign = right_encoder_sign

        self.reset()

    def heartbeat(self):
        """
        Read the motor encoders and update the estimated pose.
        """

        now = time.monotonic()

        left_deg = (
            self.left_encoder_sign * self.left_motor.position
        )
        right_deg = (
            self.right_encoder_sign * self.right_motor.position
        )

        dt = now - self.last_time

        if dt <= 0:
            return

        # Encoder change in radians
        delta_left_angle = math.radians(
            left_deg - self.last_left_deg
        )

        delta_right_angle = math.radians(
            right_deg - self.last_right_deg
        )

        # Distance travelled by each wheel
        delta_left = self.wheel_radius * delta_left_angle
        delta_right = self.wheel_radius * delta_right_angle

        # Measured wheel velocities from encoders
        v_left = delta_left / dt
        v_right = delta_right / dt

        # Differential-drive forward kinematics
        v = (v_right + v_left) / 2.0

        omega = (
            v_right - v_left
        ) / self.axle_length

        delta_theta = omega * dt
        delta_distance = v * dt

        old_theta = self.theta
        new_theta = old_theta + delta_theta

        # Exact integration for an arc
        if abs(delta_theta) < 1e-9:
            # Essentially straight
            self.x += delta_distance * math.cos(old_theta)
            self.y += delta_distance * math.sin(old_theta)

        else:
            radius = delta_distance / delta_theta

            self.x += radius * (
                math.sin(new_theta) -
                math.sin(old_theta)
            )

            self.y += -radius * (
                math.cos(new_theta) -
                math.cos(old_theta)
            )

        self.theta = self._wrap_angle(new_theta)

        # Save values for next heartbeat
        self.last_left_deg = left_deg
        self.last_right_deg = right_deg
        self.last_time = now

    def getPose(self):
        """
        Return (x, y, theta).

        x, y in metres
        theta in radians
        """
        return self.x, self.y, self.theta

    def reset(self):
        """
        Reset estimated pose to (0, 0, 0).
        """

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.last_left_deg = (
            self.left_encoder_sign *
            self.left_motor.position
        )

        self.last_right_deg = (
            self.right_encoder_sign *
            self.right_motor.position
        )

        self.last_time = time.monotonic()

    @staticmethod
    def _wrap_angle(angle):
        """
        Wrap radians to (-pi, pi].
        """
        while angle <= -math.pi:
            angle += 2.0 * math.pi

        while angle > math.pi:
            angle -= 2.0 * math.pi

        return angle