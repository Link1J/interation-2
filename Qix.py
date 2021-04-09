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
        self.qix_lines = []                 # List containing starting point and end point of all 11 lines of qix
        self.player_lines = []              # List containing starting point and end point of 4 lines of player(Diamond)

    def bound(self, pos: Vector2):
        if pos.x < 0:
            pos.x = 1 - 0
        if pos.x > 1 - 0:
            pos.x = 0
        if pos.y < 0:
            pos.y = 1 - 0
        if pos.y > 1 - 0:
            pos.y = 0

    def angle(self) -> float:
        return math.atan2(self.y_vel, self.x_vel) * (180 / math.pi)

    def draw(self, size: float) -> None:
        """
        Draws the qix
        :param size: Size of the qix
        :return: None
        """
        self.qix_pos = self.qix_pos
        self.bound(self.qix_pos)
        drawing.qix(self.qix_pos, self.angle(), size)
        self.qix_lines = drawing.get_qix_lines()
        self.player_lines = drawing.get_player_lines()

    def collision(self):
        """
        Detects collision between qix and the player(Diamond)
        :return: True if collision happens
        """
        for p_line in self.player_lines:
            p_slope, p_y_int = self.find_mb(p_line)             # y = p_slope(x) + p_y_int
            for q_line in self.qix_lines:
                q_slope, q_y_int = self.find_mb(q_line)         # y = q_slope(x) + q_y_int
                if q_slope == float('inf'):
                    collide = self.vertical_line_collision(q_line[0][0], q_line[0][1], q_line[1][1], p_line)
                else:
                    x_val, y_val = self.find_int((p_slope, p_y_int), (q_slope, q_y_int))
                    collide = self.check_collision(x_val, y_val, p_line, q_line)
                if collide:
                    return collide

    def check_collision(self, x_val, y_val, p_line, q_line):
        collision_p = False
        collision_q = False
        bigpx, smallpx = max(p_line[0][0], p_line[1][0]), min(p_line[0][0], p_line[1][0])
        bigpy, smallpy = max(p_line[0][1], p_line[1][1]), min(p_line[0][1], p_line[1][1])
        bigqx, smallqx = max(q_line[0][0], q_line[1][0]), min(q_line[0][0], q_line[1][0])
        bigqy, smallqy = max(q_line[0][1], q_line[1][1]), min(q_line[0][1], q_line[1][1])
        if smallpx < x_val < bigpx:
            if smallpy < y_val < bigpy:
                collision_p = True
        if smallqx < x_val < bigqx:
            if smallqy < y_val < bigqy:
                collision_q = True

        if collision_p and collision_q:
            return True
        else:
            return False

    def find_int(self, mb1, mb2):
        """
        Method to find intersect between given lines' slope and y-intercept
        Might be confusing, I'll add more comments later
        :param mb1: line1's slope and y_intercept
        :param mb2: line2's slope and y_intercept
        :return: x and y value of the intersecting point.
        """
        if mb1[0] != mb2[0]:
            x_val = ((mb2[1] - mb1[1]) / (mb1[0] - mb2[0]))
        else:
            x_val = -99
        y_val = mb1[0] * x_val + mb1[1]
        return x_val, y_val

    def find_mb(self, line):
        """
        Find slope(m) and y-intercept(b) from the given line.
        Might be confusing, I'll add more comments later
        :return: slope and y_intercept of the given line.
        """
        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[1][0]
        y2 = line[1][1]
        if x2 != x1:
            slope = float((y2 - y1) / (x2 - x1))
        else:
            slope = float('inf')
        y_int = float(line[0][1] - slope * line[0][0])
        return slope, y_int

    def vertical_line_collision(self, x_val, y_start, y_end, line2):
        """
        Checks for collision when the line is vertical and thus cannot calculate slope.
        :param x_val: x_value of the vertical line
        :param y_start: y value of the vertical line's starting point.
        :param y_end: y value of the vertical line's ending point.
        :param line2: non-vertical line
        :return: Whether the intersection between the lines exists.
        """
        slope, y_int = self.find_mb(line2)
        y_val = slope * x_val + y_int
        collisionx = False
        collisiony = False
        bigx = max(line2[0][0], line2[1][0])
        smallx = min(line2[0][0], line2[1][0])
        bigy = max(y_start, y_end)
        smally = min(y_start, y_end)
        if smallx <= x_val <= bigx:
            collisionx = True
        if smally < y_val < bigy:
            collisiony = True
        if collisionx and collisiony:
            return True
        else:
            return False

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
