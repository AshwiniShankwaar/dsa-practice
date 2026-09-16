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


def tree_to_list(root):
    """Inverse of build_tree: level-order list with None marking a missing
    child, matching LeetCode's serialization (trailing Nones past the last
    node's children are omitted).
    """
    if root is None:
        return []
    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            result.append(None)
            continue
        result.append(node.val)
        if node.left or node.right:
            queue.append(node.left)
            queue.append(node.right)
    return result
