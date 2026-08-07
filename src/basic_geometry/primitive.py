# Kreise werden als primitive genutzt da die Überlappungen hier von aabb test unterscheidbar sind, aber nicht so deep zu implementieren. 
# Quadrate wären sinnlos, da aabb tests identisch zu kreistests sind

from dataclasses import dataclass
from math import sqrt
from .vec2 import Vec2
from .aabb import AABB

@dataclass
class Particle():
    id: int
    center:Vec2
    radius:float

    def aabb(self) -> AABB:
        return AABB(
            (self.center.x - self.radius,
            self.center.y - self.radius),
            (self.center.x + self.radius,
            self.center.y + self.radius)
        )
    
    def collision_check(self, other):
        dm = sqrt((self.center.x - other.center.x)**2 + (self.center.y - other.center.y)**2)