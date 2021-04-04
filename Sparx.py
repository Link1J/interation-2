from Line import Line
from pygame import Surface
from CircularLinkedList import CircularLinkedList
from pygame.math import Vector2
from drawing import drawing


class Sparx:

    def __init__(self, x: float, y: float, vel: float, reverse: bool) -> None:
        self.win = None                                 # Window(screen) which the sparx is drawn on.
        self.x, self.y = x, y                           # x and y value of the Sparx.
        self.vel = vel                                  # velocity of the Sparx.
        self.x_vel, self.y_vel = vel, 0                 # x and y velocity of the Sparx.
        self.inner_list = CircularLinkedList()          # List containing inner lines that Sparcs move along.
        self.cur_line = None                            # Current line that Sparx is moving along.
        self.corner = False                             # True if the Sparx has reached the end of the line.
        self.reverse = reverse                          # if self.reverse = True => Sparx moves to the left at the start
        self.setup_lines()                              # Initializing the lines that the sparx move through.

    def setup_lines(self) -> None:
        """
        Sets up the lines for the sparx to move along (made for testing purpose).
        Should be replaced with inner_list created by the player.
        """
        line1 = Line([(0.1, 0.1), (0.9, 0.1)])          # Top line
        line2 = Line([(0.9, 0.1), (0.9, 0.9)])          # Right line
        line3 = Line([(0.9, 0.9), (0.1, 0.9)])          # Bottom line
        line4 = Line([(0.1, 0.9), (0.1, 0.1)])          # Left line
        self.inner_list.insert_end(line1)
        self.inner_list.insert_end(line2)
        self.inner_list.insert_end(line3)
        self.inner_list.insert_end(line4)
        self.cur_line = line1

    def set_surface(self, win: Surface) -> None:
        self.win = win

    def draw(self, facing: float, size: float) -> None:
        """
        Calls drawing.sparx from drawing.py
        This is done so that Sparx object contains the method 'draw'
        :param facing: What is facing param for?
        :param size: Size of the Sparx
        :return: None
        """
        pos = Vector2(self.x, self.y)
        drawing.sparx(pos, facing, size)

    def move(self) -> None:
        """
        Moves the Sparx
        :return: None
        """
        if self.corner:
            if self.reverse:
                self.cur_line = self.cur_line.prev
            else:
                self.cur_line = self.cur_line.next
            self.corner = False

        # Moving Vertically
        if self.cur_line.data[0][0] == self.cur_line.data[1][0]:
            self.x_vel = 0
            if self.cur_line.data[0][1] < self.cur_line.data[1][1]:
                self.y_vel = self.vel
            elif self.cur_line.data[0][1] > self.cur_line.data[1][1]:
                self.y_vel = -1 * self.vel
            self.x += self.x_vel
            self.y += self.y_vel
            if not self.reverse:
                # Moving Down
                if self.y_vel > 0:
                    if self.y > self.cur_line.data[1][1]:
                        self.corner = True
                # Moving up
                else:
                    if self.y < self.cur_line.data[1][1]:
                        self.corner = True
            else:
                # Moving Down (Reverse Sparx)
                if self.y_vel > 0:
                    if self.y > self.cur_line.data[0][1]:
                        self.corner = True
                # Moving Up (Reverse Sparx)
                else:
                    if self.y < self.cur_line.data[0][1]:
                        self.corner = True
        # Moving Horizontally
        else:
            self.y_vel = 0
            if self.cur_line.data[0][0] < self.cur_line.data[1][0]:
                self.x_vel = self.vel
            elif self.cur_line.data[0][0] > self.cur_line.data[1][0]:
                self.x_vel = -1 * self.vel
            self.x += self.x_vel
            self.y += self.y_vel
            if not self.reverse:
                # Moving right
                if self.x_vel > 0:
                    if self.x > self.cur_line.data[1][0]:
                        self.corner = True
                # Moving left
                else:
                    if self.x < self.cur_line.data[1][0]:
                        self.corner = True
            else:
                # Moving right (Reverse Sparx)
                if self.x_vel > 0:
                    if self.x > self.cur_line.data[0][0]:
                        self.corner = True
                # Moving Left (Reverse Sparx)
                else:
                    if self.x < self.cur_line.data[0][0]:
                        self.corner = True

