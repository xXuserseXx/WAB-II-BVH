from itertools import count

from basic_geometry.primitive import Particle
from tree_construction.node import Node

def build_bottom(particles: list[Particle]) -> Node:
  if not particles:
    raise ValueError("List is Empty!")
  
  node_ids = count()
  
  active_nodes = []

  for particle in particles:
    active_nodes.append(create_leaf(particle, next(node_ids)))
    
  while(len(active_nodes)) > 1:
    first_index, second_index = find_best_pair(active_nodes)
    
    first = active_nodes[first_index]
    second = active_nodes[second_index]
    
    merged_aabb = first.aabb.merge_aabb(second.aabb)
    
    parent = Node(node_id=next(node_ids), particle_id=None, aabb=merged_aabb, left=first, right=second, leaf_count=first.leaf_count + second.leaf_count)
    
    first.parent = parent
    second.parent = parent
    
    for index in sorted((first_index, second_index), reverse=True):
      del active_nodes[index]
      
    active_nodes.append(parent)
    
  return(active_nodes[0])
  
  
  


def create_leaf(particle: Particle, node_id: int) -> Node:
  return Node(node_id= node_id , particle_id = particle.id, aabb = particle.aabb(), leaf_count = 1)

def find_best_pair(nodes: list[Node]) -> tuple[int, int]:
  best_i = 0
  best_j = 1

  best_area = (
    nodes[0].aabb.merge_aabb(nodes[1].aabb).area())

  for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
      merged = nodes[i].aabb.merge_aabb(nodes[j].aabb)
      area = merged.area()

      if area < best_area:
        best_area = area
        best_i = i
        best_j = j
  
  return best_i, best_j
