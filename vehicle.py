import enum
import numpy as np

class VehicleState(enum.Enum):
    CRASH = 0
    PASSED = 1
    TRANSIT = 2
    IDLE = 3

class Vehicle:
    halt_time: int
    size: int
    speed: int
    risk: int

    def __init__(self, halt_time, size):
        self.halt_time = halt_time
        self.size = size
        self.risk = 0
        self.speed = 0

    def brake(self, time):
        if time <= self.halt_time:
            self.risk *= 1.65
        r = np.random.random()
        if r <= self.risk:
            return VehicleState.CRASH
        self.risk = 0
        self.speed = 0
        return VehicleState.IDLE

    def slow(self, time):
        self.speed *= pow(0.92, time)
        self.risk *= pow(0.92, time)
        return VehicleState.TRANSIT

    def accelerate(self, time):
        self.speed = max(1, self.speed)
        self.risk = max(0.05, self.risk)
        for i in range(time):
            self.speed *= 1.05
            self.risk *= 1.08
            self.size -= self.speed
            if self.size <= 0:
                return VehicleState.PASSED, i
        return VehicleState.TRANSIT, time
