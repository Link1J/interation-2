from pygame import Vector2
from drawing import drawing
import random
import math
from math import cos, sin, radians


class Qix:
    """
    Class representing Qix
    """
    def __init__(self, pos: Vector2):
        self.qix_pos = pos                  # Current Position of qix
        self.qix_mov = Vector2(0.01, 0.0)   # Makes the sticks move in circle
        self.vel = 0                        # Overall velocity of the qix
        self.x_vel, self.y_vel = 0, 0       # x and y velocity of the qix
        self.x_sign, self.y_sign = 1, 1     # 1 for positive sign, -1 for negative sign
        self.count = 0                      # Count so that qix doesnt change direction every time qix.move() is called

    def bound(self, pos: Vector2):
        if pos.x < 0:
            pos.x = 1 - 0
        if pos.x > 1 - 0:
            pos.x = 0
        if pos.y < 0:
            pos.y = 1 - 0
        if pos.y > 1 - 0:
            pos.y = 0

    def angle(self, mov: Vector2) -> float:
        return math.atan2(mov.y, mov.x) * (180 / math.pi)

    def draw(self, size: float) -> None:
        """
        Draws the qix
        :param size: Size of the qix
        :return: None
        """
        self.qix_pos = self.qix_pos + self.qix_mov
        self.bound(self.qix_pos)
        self.qix_mov.rotate_ip(10)  # random.randint(0, 20))
        drawing.qix(self.qix_pos, self.angle(self.qix_mov), size)

    def move(self) -> None:
        """
        Makes qix move in random direction and random speed for certain period of time.
        :return: None
        """
        self.count += 1
        # Changes direction and speed every 50th time move() is called.
        if (self.count % 50) == 0:
            # Speed of the qix can be from 0.003 to 0.006
            self.vel = random.randrange(3, 6)
            self.vel = self.vel/1000
            # Gets a random direction from degree 1 to 360
            angle = random.randrange(1, 360)
            if 0 < angle <= 90:
                self.x_sign = 1
                self.y_sign = -1

            elif (90 < angle) and (angle <= 180):
                angle = 180 - angle
                self.x_sign = -1
                self.y_sign = -1

            elif (180 < angle) and (angle <= 270):
                angle = angle - 180
                self.x_sign = -1
                self.y_sign = 1

            elif (270 < angle) and (angle <= 360):
                angle = 360 - angle
                self.x_sign = 1
                self.y_sign = 1

            hyp = self.vel
            # Calculates x_velocity and y_velocity required in order to move in the selected angle.
            self.x_vel = self.x_sign * (math.cos(math.radians(angle))) * hyp
            self.y_vel = self.y_sign * (math.sin(math.radians(angle))) * hyp

        # if (0 < (self.qix_pos[0] + self.x_vel) < 1) and (0 < (self.qix_pos[1] + self.y_vel) < 1):
        self.qix_pos[0] += self.x_vel
        self.qix_pos[1] += self.y_vel

    def get_pos(self) -> Vector2:
        """
        Returns the current position of the qix
        :return: Current position of qix.
        """
        pos = Vector2(self.x, self.y)
        return pos
