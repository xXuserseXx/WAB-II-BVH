
from dataclasses import dataclass
from basic_geometry.aabb import AABB

@dataclass
class Node():

    node_id: int
    particle_id: int
    aabb: AABB
    left: "Node | None" = None
    right: "Node | None" = None
    parent: "Node | None" = None
    leaf_count: int = 1 #ANzahl der Kreise unter diesem Knoten, mindestens 1 für Blattknoten

    def is_leaf(self) -> bool:
        if self.particle_id is None:
            return False
        else:
            return True
    