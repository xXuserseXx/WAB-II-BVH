# Kreise werden als primitive genutzt da die Überlappungen hier von aabb test unterscheidbar sind, aber nicht so deep zu implementieren. 
# Quadrate wären sinnlos, da aabb tests identisch zu kreistests sind
from __future__ import annotations
from dataclasses import dataclass

from .vec2 import Vec2
from .aabb import AABB

@dataclass
class Particle():
    id: int
    center:Vec2
    radius:float

    def aabb(self) -> AABB:
        return AABB(
            Vec2(self.center.x - self.radius,self.center.y - self.radius),
            Vec2(self.center.x + self.radius,self.center.y + self.radius)
        )
    
    def collision_check(self, other: Particle) -> bool:
        squared_distance = Vec2.squared_distance(
            self.center,
            other.center
        )

        return squared_distance <= (self.radius + other.radius) ** 2