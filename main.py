from timetracker import TimeTracker
from drawing import Vector2, drawing
from debug import debug

import time
import math
import random

import pygame
# import antigravity

running = True


def bound(pos: Vector2) -> None:
    if pos.x < 0:
        pos.x = 1 - 0
    if pos.x > 1 - 0:
        pos.x = 0
    if pos.y < 0:
        pos.y = 1 - 0
    if pos.y > 1 - 0:
        pos.y = 0


def angle(mov: Vector2) -> float:
    return math.atan2(mov.y, mov.x) * (180 / math.pi)


def game_update() -> None:
    global qix_pos
    global qix_mov

    global ply_pos
    global ply_mov

    global count

    drawing.setup_frame()

    if count % 4 == 0:
        qix_pos = qix_pos + qix_mov
        bound(qix_pos)

        ply_pos = ply_pos + ply_mov
        bound(ply_pos)

        drawing.Qix_update(qix_pos, angle(qix_mov))
        qix_mov.rotate_ip(random.randint(0, 20))

    drawing.Qix(qix_pos, angle(qix_mov), 0.1)
    drawing.Player(ply_pos, angle(ply_mov), 0.1)
    drawing.Sparx(Vector2(0.5, 0.5), 0, 0.1)

    drawing.Borders()

    debug.draw_tps()

    pygame.display.flip()


def main():
    global running

    global qix_pos
    global qix_mov

    global ply_pos
    global ply_mov

    global count

    pygame.init()
    pygame.display.set_caption("Qix")
    screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE)

    gameUpdate = TimeTracker(time.perf_counter_ns)

    drawing.set_surface(screen)
    debug.set_surface(screen)

    qix_pos = Vector2(0.25, 0.5)
    qix_mov = Vector2(0.01, 0.0)

    ply_pos = Vector2(0.5, 0.5)
    ply_mov = Vector2(random.uniform(0, 0.01), random.uniform(0, 0.01))

    count = 0

    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False

        #  16666667
        #  16000000
        # 100000000
        gameUpdate.once_after(16666667, game_update)
        gameUpdate.accumulate()


if __name__ == "__main__":
    main()
