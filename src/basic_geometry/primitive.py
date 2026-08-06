# Kreise werden als primitive genutzt da die Überlappungen hier von aabb test unterscheidbar sind, aber nicht so deep zu implementieren. 
# Quadrate wären sinnlos, da aabb tests identisch zu kreistests sind

from dataclasses import dataclass
from .vec2 import Vec2

@dataclass
class Particle():
    id: int
    center:Vec2
    radius:float

    