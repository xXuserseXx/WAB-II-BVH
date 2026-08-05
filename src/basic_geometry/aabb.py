from dataclasses import dataclass
from . import Vec2
@dataclass
class AABB():
    vec_min:Vec2
    vec_max:Vec2

    def center(self):
        return (self.vec_max + self.vec_min) * 0,5