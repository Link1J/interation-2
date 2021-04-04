from typing import List, Tuple
from enum import Enum, unique

from pygame import Surface, Color
from pygame.math import Vector2
from pygame.draw import aaline

from random import randint, uniform
from math import cos, sin, sqrt

import pygame
import pygame.gfxdraw


@unique
class PlayerShape(Enum):
    Diamond = 0
    Arrow = 1


class Drawing:
    prev_qix: List[Tuple[Vector2, float]]
    size: Tuple[int, int]
    scale: int
    offset: Tuple[float, float]
    player_shape: PlayerShape
    surface: Surface

    def __init__(self) -> None:
        self.player_shape = PlayerShape.Diamond
        self.prev_qix = [(Vector2(-100, -100), 0.) for _ in range(10)]

    def set_surface(self, surface: Surface) -> None:
        self.surface = surface

    def setup_frame(self) -> None:
        self.size = self.surface.get_size()
        self.scale = min(self.size[0], self.size[1])
        self.offset = ((self.size[0] / 2) - (self.scale / 2),
                       (self.size[1] / 2) - (self.scale / 2))
        self.surface.fill(Color(0, 0, 0))

    def qix_update(self, pos: Vector2, facing: float) -> None:
        for i in range(len(self.prev_qix) - 1):
            self.prev_qix[i] = self.prev_qix[i + 1]
        self.prev_qix[-1] = (pos, facing)

    def qix(self, pos: Vector2, facing: float, size: float) -> None:
        global screen

        draw_color = (255, 0, 0)
        delta = Vector2(0, size / 2)

        for (pos, facing) in self.prev_qix:
            offset = delta.rotate(facing)
            start = (pos + offset) * self.scale + Vector2(self.offset)
            end = (pos - offset) * self.scale + Vector2(self.offset)
            pygame.draw.aaline(self.surface, draw_color, start, end, 2)

    def Player(self, pos: Vector2, facing: float, size: float) -> None:
        delta = Vector2(0, size / 2)
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

            aaline(self.surface, draw_color, t, r, 2)
            aaline(self.surface, draw_color, r, b, 2)
            aaline(self.surface, draw_color, b, l, 2)
            aaline(self.surface, draw_color, l, t, 2)

    def sparx(self, pos: Vector2, facing: float, size: float) -> None:
        max_delta = int(size / 2 * self.scale)
        pos = pos * self.scale + Vector2(self.offset)
        for _ in range(0, self.scale // 4):
            r = randint(128, 255)
            g = randint(0, 0xA5)
            dr = max_delta * sqrt(uniform(0, 1))
            dt = max_delta * sqrt(uniform(0, 1))
            x = int(pos.x + 1 + dr * cos(dt))
            y = int(pos.y + dr * sin(dt))
            self.surface.set_at((x, y), pygame.Color(r, g, 0))

        pass

    def Borders(self) -> None:
        global screen

        l = int(self.offset[0])
        r = self.size[0] - l - 1
        t = int(self.offset[1])
        b = self.size[1] - t - 1

        pygame.gfxdraw.line(self.surface, l, t, l, b, (255, 255, 255))
        pygame.gfxdraw.line(self.surface, r, t, r, b, (255, 255, 255))
        pygame.gfxdraw.line(self.surface, l, t, r, t, (255, 255, 255))
        pygame.gfxdraw.line(self.surface, l, b, r, b, (255, 255, 255))


drawing = Drawing()
