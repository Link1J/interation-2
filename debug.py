from pygame.font import SysFont, Font
from pygame import Surface

from time import perf_counter_ns

from timetracker import TimeTracker

class Debug:
    surface: Surface
    tps: TimeTracker
    font: Font

    def __init__(self) -> None:
        self.tps = TimeTracker(perf_counter_ns)
        pass
    
    def set_surface(self, surface: Surface) -> None:
        self.font = SysFont(None, 25)
        self.surface = surface

    def draw_tps(self) -> None:
        image = self.font.render("TPS: " + str(self.tps.fps()), True, (255, 255, 255))
        self.surface.blit(image, image.get_rect())
        self.tps.tick()

debug = Debug()