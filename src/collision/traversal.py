from dataclasses import dataclass

from basic_geometry.primitive import Particle
from tree_construction.node import Node

@dataclass
class TraversalResult:
    candidate_pairs: set[tuple[int, int]]
    collision_pairs: set[tuple[int, int]]
    bounding_volume_checks: int
    primitive_checks: int


def detect_all_pairs(root: Node, particles: list[Particle]) -> TraversalResult:

  particles_by_id = {particle.id: particle for particle in particles}

  result = TraversalResult(candidate_pairs=set(), collision_pairs=set(), bounding_volume_checks=0, primitive_checks=0)

  def traverse_pair(first: Node, second: Node) -> None:
    # AABB-Test.
    if not first.is_leaf() or not second.is_leaf():
      result.bounding_volume_checks += 1

    if not first.aabb.overlaps(second.aabb):
      return

    if first.is_leaf() and second.is_leaf():

      first_id = first.particle_id
      second_id = second.particle_id

      pair = (min(first_id, second_id), max(first_id, second_id))

      result.candidate_pairs.add(pair)

      result.primitive_checks += 1

      first_particle = particles_by_id[first_id]
      second_particle = particles_by_id[second_id]

      if first_particle.collision_check(second_particle):
        result.collision_pairs.add(pair)

      return

    if first.is_leaf():
      traverse_pair(first, second.left)
      traverse_pair(first, second.right)
      return
          
    if second.is_leaf():
      traverse_pair(first.left, second)
      traverse_pair(first.right, second)
      return

        # Beide internen Knoten
    traverse_pair(first.left, second.left)
    traverse_pair(first.left, second.right)
    traverse_pair(first.right, second.left)
    traverse_pair(first.right, second.right)

  def self_traverse(node: Node) -> None:

    if node.is_leaf():
      return

    self_traverse(node.left)
    self_traverse(node.right)

    traverse_pair(node.left, node.right)

  self_traverse(root)

  return result