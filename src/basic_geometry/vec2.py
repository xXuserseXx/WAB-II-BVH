from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Vec2():
    x: float
    y: float

    @staticmethod
    def squared_distance(first:Vec2, second:Vec2):
        dy = first.y - second.y
        dx = first.x - second.x

        return dx ** 2 + dy ** 2

    # Primitive Operationen

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)