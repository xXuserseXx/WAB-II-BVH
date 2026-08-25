from __future__ import annotations
from basic_geometry.primitive import Particle
from basic_geometry.aabb import AABB

# Wenn ein Experiment spätr nicht alle Collisions findet, dann muss es unvalid sein, und wird ignoremaxxed

def brute_force_collisions(particles: List[Particle]):
    collisions = set()
    for i,first in enumerate(particles):
        for second in particles[i + 1:]:
            if first.collision_check(second):
                collisions.add((min(first.id, second.id),max(first.id, second.id),))
    return collisions


def brute_force_aabb_overlaps(particles: List[Particle]):
    overlaps = set()
    for i, first in enumerate(particles):
        for second in particles[i + 1:]:
            if first.aabb().overlaps(second.aabb()):
                overlaps.add((min(first.id, second.id), max(first.id, second.id)))
    return overlaps