from typing import List, Tuple, Union
from enum import Enum, unique

from pygame import Surface, Color
from pygame.math import Vector2
from pygame.draw import aaline
from pygame.font import Font

from random import randint, uniform
from math import cos, sin, sqrt

import pygame
import pygame.gfxdraw


@unique
class PlayerShape(Enum):
    Diamond = 0
    Arrow = 1


class Drawing:
    prev_qix: List[Tuple[Vector2, float, Color]]
    size: Tuple[int, int]
    scale: int
    offset: Tuple[float, float]
    player_shape: PlayerShape
    surface: Surface
    font: Font

    score: Surface
    filled: Surface
    required: Surface
    filled_text: Surface
    required_text: Surface
    score_text: Surface
    space_size: int

    # Cache values (DO NOT USE)
    score_value: int
    # Cache values (DO NOT USE)
    filled_value: int
    # Cache values (DO NOT USE)
    required_value: int

    def __init__(self) -> None:
        self.player_shape = PlayerShape.Diamond
        self.prev_qix = [(Vector2(-100, -100), 0., Color(0, 255, 0))
                         for _ in range(10)]
        self.surface = None
        self.size = (0, 0)
        self.score_value = 0
        self.filled_value = 0
        self.required_value = 0
        self.player_pos = []
        self.player_lines = []
        self.qix_lines = []

    def set_surface(self, surface: Surface) -> None:
        size = surface.get_size()
        scale = min(size[0], size[1])

        self.surface = surface

        self.font = Font("PressStart2P.ttf", int(scale * 0.03))
        self.required_text = self.font.render(
            "Required", True, (255, 255, 255))
        self.filled_text = self.font.render("Filled", True, (255, 255, 255))
        self.score_text = self.font.render("Score", True, (255, 255, 255))
        self.space_size = self.font.render(
            " ", True, (255, 255, 255)).get_width()

        self.update_required(self.required_value)
        self.update_filled(self.filled_value)
        self.update_score(self.score_value)

    def setup_frame(self) -> None:
        if self.size != self.surface.get_size():
            self.set_surface(self.surface)
        self.size = self.surface.get_size()
        self.full_scale = min(self.size[0], self.size[1])
        self.scale = int(self.full_scale * 0.8)
        self.offset = ((self.size[0] / 2) - (self.scale / 2),
                       (self.size[1] / 2) - (self.scale / 2))
        self.full_offset = ((self.size[0] / 2) - (self.full_scale / 2),
                            (self.size[1] / 2) - (self.full_scale / 2))
        self.surface.fill(Color(0, 0, 0))

    def update_required(self, value: Union[int, float]) -> None:
        """
        Updates the texture for min required filled
        :param value: min required filled
        :return: None
        """
        self.required = self.font.render(
            str(value) + "%", True, (255, 255, 255))
        self.required_value = value

    def update_filled(self, value: Union[int, float]) -> None:
        """
        Updates the texture for filled
        :param value: filled
        :return: None
        """
        self.filled = self.font.render(str(value) + "%", True, (255, 255, 255))
        self.filled_value = value

    def update_score(self, value: int) -> None:
        """
        Updates the texture for score
        :param value: score
        :return: None
        """
        self.score = self.font.render(str(value), True, (255, 255, 255))
        self.score_value = value

    def qix_update(self, pos: Vector2, facing: float) -> None:
        for i in range(len(self.prev_qix) - 1):
            self.prev_qix[i] = self.prev_qix[i + 1]
        self.prev_qix[-1] = (Vector2(pos), facing, Color(255, 0, 0))

    def qix(self, pos: Vector2, facing: float, size: float) -> None:
        """
        Draws the Qix
        :param pos: Current position
        :param facing: Facing direction
        :param size: Size of object
        :return: None
        """
        draw_color = (255, 0, 0)
        delta = Vector2(0, size / 2)

        if pos.distance_to(self.prev_qix[-1][0]) >= 0.01 or facing - self.prev_qix[-1][1] > 0.01 or facing - self.prev_qix[-1][1] < -0.01:
            self.qix_update(pos, facing)

        offset = delta.rotate(facing)
        start = (pos + offset) * self.scale + Vector2(self.offset)
        end = (pos - offset) * self.scale + Vector2(self.offset)
        pygame.draw.aaline(self.surface, draw_color, start, end, 2)
        self.qix_lines = [[start, end]]
        for (pos, facing, draw_color) in self.prev_qix:
            offset = delta.rotate(facing)
            start = (pos + offset) * self.scale + Vector2(self.offset)
            end = (pos - offset) * self.scale + Vector2(self.offset)
            pygame.draw.aaline(self.surface, draw_color, start, end, 2)
            self.qix_lines.append([start, end])

    def get_qix_lines(self):
        return self.qix_lines

    def player(self, pos: Vector2, facing: float, size: float) -> None:
        """
        Draws the Player
        :param pos: Current position
        :param facing: Facing direction
        :param size: Size of object
        :return: None
        """
        self.player_pos = pos
        delta = Vector2(0, size)
        draw_color = (128, 128, 128)

        if self.player_shape == PlayerShape.Arrow:
            tc = (pos - delta.rotate(facing + 0)) * \
                self.scale + Vector2(self.offset)
            bl = (pos - delta.rotate(facing + 120)) * \
                self.scale + Vector2(self.offset)
            br = (pos - delta.rotate(facing + -120)) * \
                self.scale + Vector2(self.offset)
            cc = (pos) * self.scale + Vector2(self.offset)

            aaline(self.surface, draw_color, tc, bl, 2)
            aaline(self.surface, draw_color, tc, br, 2)
            aaline(self.surface, draw_color, bl, cc, 2)
            aaline(self.surface, draw_color, br, cc, 2)

        elif self.player_shape == PlayerShape.Diamond:
            t = (pos - delta.rotate(0)) * self.scale + Vector2(self.offset)
            r = (pos - delta.rotate(90)) * self.scale + Vector2(self.offset)
            b = (pos - delta.rotate(180)) * self.scale + Vector2(self.offset)
            l = (pos - delta.rotate(270)) * self.scale + \
                Vector2(self.offset) + Vector2(1/1017, 0) * self.scale
            self.player_lines = []
            aaline(self.surface, draw_color, t, r, 2)
            aaline(self.surface, draw_color, r, b, 2)
            aaline(self.surface, draw_color, b, l, 2)
            aaline(self.surface, draw_color, l, t, 2)
            self.player_lines.append([t, r])
            self.player_lines.append([r, b])
            self.player_lines.append([b, l])
            self.player_lines.append([l, t])

    def get_player_lines(self):
        return self.player_lines

    def get_player_pos(self):
        return self.player_pos

    def sparx(self, pos: Vector2, facing: float, size: float) -> None:
        """
        Draws the sparx
        :param pos: Current position
        :param facing: Does nothing (Facing direction)
        :param size: Size of object
        :return: None
        """
        max_delta = int(size / 2 * self.scale)
        pos = pos * self.scale + Vector2(self.offset) + Vector2(1, 0)
        for _ in range(0, self.scale // 5):
            r = randint(128, 255)
            g = randint(0, 0xA5)
            dr = max_delta * sqrt(uniform(0, 4))
            dt = max_delta * sqrt(uniform(0, 4))
            x = int(pos.x + dr * cos(dt))
            y = int(pos.y + dr * sin(dt))
            self.surface.set_at((x, y), pygame.Color(r, g, 0))

        pass

    def borders(self) -> None:
        l = int(self.offset[0])
        r = int(self.size[0] - l - 1)
        t = int(self.offset[1])
        b = int(self.size[1] - t - 1)

        pygame.gfxdraw.line(self.surface, l, t, l, b, (255, 255, 255))
        pygame.gfxdraw.line(self.surface, r, t, r, b, (255, 255, 255))
        pygame.gfxdraw.line(self.surface, l, t, r, t, (255, 255, 255))
        pygame.gfxdraw.line(self.surface, l, b, r, b, (255, 255, 255))

    def end(self) -> None:
        rect = self.required_text.get_rect()
        rect.move_ip(self.full_offset[0] + self.full_scale -
                     rect.width - self.space_size, self.full_scale * 0.01)
        self.surface.blit(self.required_text, rect)
        prev_rect = rect

        rect = self.required.get_rect()
        rect.move_ip(prev_rect.x + prev_rect.width/2, prev_rect.bottom)
        rect.move_ip(-(rect.width/2), 0)
        self.surface.blit(self.required, rect)

        rect = self.filled_text.get_rect()
        rect.move_ip(prev_rect.x - self.space_size, prev_rect.top)
        rect.move_ip(-rect.width, 0)
        self.surface.blit(self.filled_text, rect)
        prev_rect = rect

        rect = self.filled.get_rect()
        rect.move_ip(prev_rect.x + prev_rect.width/2, prev_rect.bottom)
        rect.move_ip(-(rect.width/2), 0)
        self.surface.blit(self.filled, rect)

        rect = self.score_text.get_rect()
        rect.move_ip(self.full_offset[0] +
                     self.space_size, self.full_scale * 0.01)
        self.surface.blit(self.score_text, rect)
        prev_rect = rect

        rect = self.score.get_rect()
        rect.move_ip(prev_rect.x, prev_rect.bottom)
        self.surface.blit(self.score, rect)

    def lines(self, polys : List[List[Tuple[int, int]]], lines : List[Tuple[Tuple[int, int], Tuple[int, int]]]):
        # Draw polygons
        for poly in polys:
            temp = poly.copy()

            for i in range(len(temp)):
                temp[i] = (temp[i][0] / 500 * self.scale + self.offset[0], temp[i][1] / 500 * self.scale + self.offset[1])

            pygame.draw.polygon(self.surface, (0, 255, 0), temp)
            for i in range(-1, len(temp) - 1):
                aaline(self.surface, (255, 255, 255), temp[i], temp[i + 1])

        for line in lines:
            startx = line[0][0] / 500 * self.scale + self.offset[0]
            starty = line[0][1] / 500 * self.scale + self.offset[1]
            endx = line[1][0] / 500 * self.scale + self.offset[0]
            endy = line[1][1] / 500 * self.scale + self.offset[1]
            aaline(self.surface, (255, 255, 255),
                   (startx, starty), (endx, endy))


drawing = Drawing()
