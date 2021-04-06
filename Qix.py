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
        self.qix_pos = pos
        self.qix_mov = Vector2(0.01, 0.0)
        self.x = pos[0]
        self.y = pos[1]
        self.win = None
        self.x_vel = 0
        self.y_vel = 0
        self.x_sign = 1
        self.y_sign = 1
        self.vel = 0.1
        self.count = 0

    def set_surface(self, win):
        self.win = win

    def update(self, facing: float):
        pos = Vector2(self.x, self.y)
        drawing.qix_update(pos, facing)

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

    def draw(self, size: float):
        self.qix_pos = self.qix_pos + self.qix_mov
        self.bound(self.qix_pos)
        self.qix_mov.rotate_ip(10)# random.randint(0, 20))
        drawing.qix(self.qix_pos, self.angle(self.qix_mov), size)

    def test_move(self):
        self.qix_pos[0] += 0.001
        print (self.qix_pos[0])

    def move(self):
        self.count += 1
        if (self.count % 50) == 0:
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
            self.x_vel = self.x_sign * (math.cos(math.radians(angle))) * hyp
            self.y_vel = self.y_sign * (math.sin(math.radians(angle))) * hyp

        #if (0 < (self.qix_pos[0] + self.x_vel) < 1) and (0 < (self.qix_pos[1] + self.y_vel) < 1):
        self.qix_pos[0] += self.x_vel
        self.qix_pos[1] += self.y_vel

    def get_pos(self):
        pos = Vector2(self.x, self.y)
        return pos
