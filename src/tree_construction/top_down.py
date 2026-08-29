from basic_geometry.aabb import AABB
from basic_geometry.primitive import Particle
from tree_construction.node import Node

from itertools import count


def build_top_down(particles: list[Particle]) -> Node:
  if not particles:
    raise ValueError("Cannot build BVH from empty particle list.")

  node_ids = count()

  return build_recursive(particles, node_ids)
    
def build_recursive(particles: list[Particle],node_ids,) -> Node:
  if len(particles) == 1:
    return create_leaf(particles[0], next(node_ids),)

  node_aabb = combined_aabb(particles)

  left_particles, right_particles = split_particles(particles, node_aabb)

  left = build_recursive(left_particles, node_ids)

  right = build_recursive(right_particles, node_ids)

  node = Node(node_id=next(node_ids), particle_id=None, aabb=node_aabb, left=left, right=right, leaf_count=left.leaf_count + right.leaf_count,)

  left.parent = node
  right.parent = node

  return node
  
def create_leaf(particle: Particle, node_id: int) -> Node:
  return Node(node_id= node_id , particle_id = particle.id, aabb = particle.aabb(), leaf_count = 1)
  
def combined_aabb(particles: list[Particle]) -> AABB:
  combined = particles[0].aabb()

  for particle in particles[1:]:
    combined = combined.merge_aabb(particle.aabb())

  return combined
  
def split_particles(particles: list[Particle], aabb: AABB) -> tuple[list[Particle], list[Particle]]:
  width = aabb.vec_max.x - aabb.vec_min.x
  height = aabb.vec_max.y - aabb.vec_min.y 
  
  if width >= height:
    particles = sorted(particles, key=lambda particle: particle.center.x)
  else:
    particles = sorted(particles, key=lambda particle: particle.center.y)
    
  middle = len(particles) // 2
  
  return(particles[:middle], particles[middle:])
        
      