from tree_construction.node import Node


def tree_height(root: Node) -> int:
    max_depth = 0
    stack = [(root, 0)]

    while stack:
        node, depth = stack.pop()
        max_depth = max(max_depth, depth)

        if node.is_leaf():
            continue

        if node.left is None or node.right is None:
            raise ValueError(f"Internal node {node.node_id} does not have two children.")

        stack.append((node.left, depth + 1))
        stack.append((node.right, depth + 1))

    return max_depth

def total_internal_aabb_area(root: Node) -> float:
    total_area = 0.0
    stack = [root]

    while stack:
        node = stack.pop()

        if node.is_leaf():
            continue

        if node.left is None or node.right is None:
            raise ValueError(f"Internal node {node.node_id} does not have two children.")

        total_area += node.aabb.area()

        stack.append(node.left)
        stack.append(node.right)

    return total_area