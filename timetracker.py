from typing import Callable

class TimeTracker:
    def __init__(self, clock: Callable[[], int]) -> None:
        self.clock = clock
        self.start = clock()
        self.delta = 0
        self.last = [0 for _ in range(10)]
        self.index = 0

    def clear(self) -> None:
        self.delta = 0

    def accumulate(self) -> None:
        stop = self.clock()
        self.delta += stop - self.start
        self.start = stop

    def tick(self) -> None:
        self.clear()
        self.accumulate()
        self.last[self.index % len(self.last)] = self.delta
        self.index += 1

    def after(self, nano: int, action: Callable[[], None]) -> None:
        if self.delta >= nano:
            self.delta -= nano
            action()

    def once_after(self, nano: int, action: Callable[[], None]) -> None:
        if self.delta >= nano:
            self.delta = 0
            action()

    def every(self, nano: int, action: Callable[[], None]) -> None:
        while self.delta >= nano:
            self.delta -= nano
            action()

    def fps(self) -> int:
        total = 0.0
        for i in self.last:
            total += ((1/((i + 1)/1000000000)) - 1/1000000000)
        return int(total / len(self.last))  # 1/((self.delta + 1)/1000000000))