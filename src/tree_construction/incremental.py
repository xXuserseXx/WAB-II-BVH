from itertools import count

from basic_geometry.primitive import Particle
from basic_geometry.aabb import AABB
from tree_construction.node import Node

def build_incremental(particles: list[Particle]) -> Node:
  if not particles:
    raise ValueError("List is Empty!")
  
  node_ids = count()
  
  root = create_leaf(particles[0], next(node_ids))
  
  for particle in particles[1:]:
    new_leaf = create_leaf(particle, next(node_ids))
    root = insert_leaf(root, new_leaf, node_ids)
    
  return root  
  
def create_leaf(particle: Particle, node_id: int) -> Node:
  return Node(node_id= node_id , particle_id = particle.id, aabb = particle.aabb(), leaf_count = 1)

def insert_leaf(root: Node, new_leaf: Node, node_ids: int) -> Node:
  path = find_search_path(root, new_leaf.aabb)
  
  insertion_node = min(path,key=lambda node: insertion_cost(node, new_leaf.aabb))
  
  old_parent = insertion_node.parent
  
  new_parent = Node(node_id=next(node_ids),particle_id=None,aabb=insertion_node.aabb.merge_aabb(new_leaf.aabb),left=insertion_node,right=new_leaf,leaf_count=insertion_node.leaf_count + new_leaf.leaf_count)
  
  insertion_node.parent = new_parent
  new_leaf.parent = new_parent
  
  if old_parent is None:
    return new_parent
  
  new_parent.parent = old_parent
  
  if old_parent.left is insertion_node:
    old_parent.left = new_parent
  elif old_parent.right is insertion_node:
    old_parent.right = new_parent
  else:
    raise RuntimeError("Eltern Kind Beziehung broken")
  
  refit(old_parent)
  
  return root
  

def find_search_path(root: Node, new_aabb: AABB) -> list[Node]:
  path = []

  current = root

  while True:
    path.append(current)

    if current.is_leaf():
      break

    left_growth = area_increase(current.left.aabb,new_aabb)

    right_growth = area_increase(current.right.aabb,new_aabb)
        
    if left_growth <= right_growth:
      current = current.left
    else:
      current = current.right

  return path

def area_increase(existing: AABB, new_aabb: AABB) -> float:
  merged = existing.merge_aabb(new_aabb)

  return merged.area() - existing.area()

def insertion_cost(node:Node, new_aabb: AABB) -> float:
  merged = node.aabb.merge_aabb(new_aabb)
  
  cost = merged.area()
  
  ancestor = node.parent
  
  while ancestor is not None:
    expanded = ancestor.aabb.merge_aabb(new_aabb)
    
    cost += expanded.area() - ancestor.aabb.area()
    
    ancestor = ancestor.parent
    
  return cost

def refit(node: Node)-> None:
  current = node
  
  while current is not None:
    current.aabb = current.left.aabb.merge_aabb(current.right.aabb)
    
    current.leaf_count = (current.left.leaf_count + current.right.leaf_count)
    
    current = current.parent