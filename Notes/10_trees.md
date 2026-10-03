# 10 — Trees

## Idea
A tree is a root with children. Most tree problems use one trick:
**solve the left subtree, solve the right subtree, then combine the two answers at the root.**
Repo helpers: `utils/Tree.py` (`build_tree`, `tree_to_list`), `utils/Node.py`.

## Base case first
Every recursive tree function starts with: `if not root: return ...`

## Three walks (traversals)
- **Inorder** (left, root, right): on a BST this gives sorted order.
- **Preorder** (root, left, right): good for copying a tree.
- **Postorder** (left, right, root): good when the answer needs children first (heights).
- **Level order**: go level by level with a queue (BFS).

```python
from collections import deque
def level_order(root):
    if not root:
        return []
    q, out = deque([root]), []
    while q:
        level = []
        for _ in range(len(q)):          # exactly one level
            node = q.popleft()
            level.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        out.append(level)
    return out
```

## Template: height
```python
def height(root):
    if not root:
        return 0
    return 1 + max(height(root.left), height(root.right))
```

## Template: valid BST (pass limits down)
Every node must sit between a lower and an upper limit set by its ancestors.
```python
def is_valid_bst(root, lo=float("-inf"), hi=float("inf")):
    if not root:
        return True
    if not (lo < root.val < hi):
        return False
    return is_valid_bst(root.left, lo, root.val) and is_valid_bst(root.right, root.val, hi)
```

## Lowest common ancestor
If p and q are on different sides of the current node, the current node is the answer.

## Classic problems
Max Depth, Same Tree, Symmetric Tree, Level Order, Right Side View, Validate BST,
Lowest Common Ancestor, Diameter of Binary Tree (height + track the best sum),
Max Path Sum, Kth Smallest in BST (inorder), Build Tree from Preorder + Inorder.

## Mistakes
- Forgetting `if not root`.
- Checking only parent vs child for BST; you must check against all ancestors.
- Deep skewed trees can overflow recursion; see [23](23_contest_python_tricks.md).
