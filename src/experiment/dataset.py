from __future__ import annotations

import hashlib
import math
import random

from basic_geometry.primitive import Particle
from basic_geometry.vec2 import Vec2

def det_seed(base_seed:int, particle_count: int, dataset_id:int) -> int:
    # Suche nur ne ausrede um mal hashs zu benutzen lol, aber ein guter weg um deterministische random seeds für bestimmte experiment config zu kriegen ig
    payload = f"{base_seed}:{particle_count}:{dataset_id}"
    return int.from_bytes((hashlib.sha256(payload).digest())[:8], "big")

def domain_side_for_coverage(particle_count: int, radius: float, coverage: float) -> int:
    # Experimente sollten unabhängig der zahl an Partikeln ungefähr die gleiche coverage machen, sonst kann man die Kollisions nicht ordentlichen vergleichen

    total_particle_area = particle_count * math.pi * radius * radius
    side = math.sqrt(total_particle_area / coverage)
    return side

def generate_particle_set(particle_count: int, radius:float, coverage: float, seed:int) -> tuple[list[Particle], int]:
    side = domain_side_for_coverage(particle_count, radius, coverage)
    rng = random.Random(seed)
    low = radius
    high = side -radius

    particles = []

    for i in range(particle_count):
        particles.append(Particle(i,Vec2(rng.uniform(low, high),rng.uniform(low, high)),radius))

    return (particles, side)


    