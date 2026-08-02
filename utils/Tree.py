from collections import deque
from utils.Node import Node


def build_tree(values):
    """Build a binary tree from a LeetCode-style level-order list
    (None marks a missing child) and return the root Node.
    """
    if not values or values[0] is None:
        return None

    root = Node(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = Node(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = Node(values[i])
            queue.append(node.right)
        i += 1
    return root
