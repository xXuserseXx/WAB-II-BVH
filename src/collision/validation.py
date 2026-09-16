from __future__ import annotations
from basic_geometry.primitive import Particle
from basic_geometry.aabb import AABB
from tree_construction.node import Node

# Wenn ein Experiment spätr nicht alle Collisions findet, dann muss es unvalid sein, und wird ignoremaxxed

def brute_force_collisions(particles: list[Particle]):
    collisions = set()
    for i,first in enumerate(particles):
        for second in particles[i + 1:]:
            if first.collision_check(second):
                collisions.add((min(first.id, second.id),max(first.id, second.id),))
    return collisions


def brute_force_aabb_overlaps(particles: list[Particle]):
    overlaps = set()
    for i, first in enumerate(particles):
        for second in particles[i + 1:]:
            if first.aabb().overlaps(second.aabb()):
                overlaps.add((min(first.id, second.id), max(first.id, second.id)))
    return overlaps


def validate_bvh(root: Node, particles: list[Particle]) -> Node:
    particles_by_id = {}
    
    for particle in particles:
        particles_by_id[particle.id] = particle
        
    visited_nodes = set()
    visited_node_ids = set()
    seen_particle_ids = set()
    
    visited_nodes = set()
    visited_node_ids = set()
    seen_particle_ids = set()

    def validate_node(node: Node) -> int:

        object_id = id(node)

        if object_id in visited_nodes:
            raise AssertionError(f"Node {node.node_id} occurs multiple times in the tree.")

        visited_nodes.add(object_id)

        if node.node_id in visited_node_ids:
            raise AssertionError(f"Duplicate node ID: {node.node_id}")

        visited_node_ids.add(node.node_id)

        if node.is_leaf():

            if node.left is not None or node.right is not None:
                raise AssertionError(f"Leaf {node.node_id} has children.")

            if node.leaf_count != 1:
                raise AssertionError(f"Leaf {node.node_id} has leaf_count "f"{node.leaf_count}, expected 1.")

            particle_id = node.particle_id

            if particle_id not in particles_by_id:
                raise AssertionError(
                    f"Leaf {node.node_id} references unknown "f"particle {particle_id}.")

            if particle_id in seen_particle_ids:
                raise AssertionError(f"Particle {particle_id} occurs multiple times.")

            seen_particle_ids.add(particle_id)

            expected_aabb = particles_by_id[particle_id].aabb()

            if node.aabb != expected_aabb:
                raise AssertionError(f"Leaf {node.node_id} has incorrect AABB.")

            return 1

        if node.left is None or node.right is None:
            raise AssertionError(f"Internal node {node.node_id} does not have "f"exactly two children.")

        if node.left.parent is not node:
            raise AssertionError(f"Left child of node {node.node_id} "f"has incorrect parent.")

        if node.right.parent is not node:
            raise AssertionError(f"Right child of node {node.node_id} "f"has incorrect parent.")

        left_count = validate_node(node.left)
        right_count = validate_node(node.right)

        expected_leaf_count = left_count + right_count

        if node.leaf_count != expected_leaf_count:
            raise AssertionError(f"Node {node.node_id} has leaf_count "f"{node.leaf_count}, expected "f"{expected_leaf_count}.")

        expected_aabb = node.left.aabb.merge_aabb(node.right.aabb)

        if node.aabb != expected_aabb:
            raise AssertionError(f"Internal node {node.node_id} "f"has incorrect AABB.")

        return expected_leaf_count

    total_leaf_count = validate_node(root)

    expected_ids = set(particles_by_id)

    if seen_particle_ids != expected_ids:

        missing = expected_ids - seen_particle_ids
        unexpected = seen_particle_ids - expected_ids

        raise AssertionError(f"BVH particle mismatch. "f"Missing={sorted(missing)}, "f"unexpected={sorted(unexpected)}")

    if total_leaf_count != len(particles):
        raise AssertionError(f"BVH contains {total_leaf_count} leaves, "f"expected {len(particles)}.")
    