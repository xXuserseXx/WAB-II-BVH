import unittest

from basic_geometry.primitive import Particle
from basic_geometry.aabb import AABB

class GeometryTests(unittest.TestCase):
    def test_tangent_particle_count_as_collision(self) -> None:
        first = Particle(0, 0.0, 0.0, 1.0)
        second = Particle(1, 2.0, 0.0, 1.0)
        self.assertTrue(first.collides_with(second))
        self.assertTrue(first.aabb.overlaps(second.aabb))