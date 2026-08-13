from __future__ import annotations

from dataclasses import dataclass
from .vec2 import Vec2

@dataclass
class AABB():
    vec_min:Vec2
    vec_max:Vec2

    def center(self):
        return (self.vec_max + self.vec_min) * 0.5

    # Randberührungen sind Kollisionen
    def overlaps(self, other):
        return not (
            self.vec_max.x < other.vec_min.x
            or self.vec_min.x > other.vec_max.x
            or self.vec_max.y < other.vec_min.y
            or self.vec_min.y > other.vec_max.y
        )

    def merge_aabb(self, other: AABB) -> AABB:
        return AABB(
            Vec2(min(self.vec_min.x, other.vec_min.x),min(self.vec_min.y, other.vec_min.y)),
            Vec2(max(self.vec_max.x, other.vec_max.x),max(self.vec_max.y, other.vec_max.y))
        )
    #def longest_axis():

