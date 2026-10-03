# 25 — Design Problems

## Idea
You are asked to build a data structure where each operation must be fast.
Pick the right tool for each operation, then combine them.

## Ask first
1. Which operations are needed? (add, remove, get, random, min…)
2. What speed is required? (usually O(1) or O(log n))

## Tools
| Need | Tool |
|---|---|
| find by key in O(1) | dict |
| add or remove at ends in O(1) | deque |
| remove from middle in O(1) | doubly linked list + dict |
| always get min/max | heap |
| get a random item | list (+ dict for positions) |

## Example 1: LRU cache (forget the oldest used item)
- Dict: key → node (for instant lookup).
- Doubly linked list: order of use. Newest at the back, oldest at the front.
- On `get` or `put`, move the node to the back. When full, remove the front.

Easy version in Python:
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, cap):
        self.cap = cap
        self.d = OrderedDict()
    def get(self, k):
        if k not in self.d:
            return -1
        self.d.move_to_end(k)
        return self.d[k]
    def put(self, k, v):
        if k in self.d:
            self.d.move_to_end(k)
        self.d[k] = v
        if len(self.d) > self.cap:
            self.d.popitem(last=False)     # remove oldest
```
(Interviews may ask you to build the linked list version yourself.)

## Example 2: insert, delete, get random in O(1)
- Dict: value → its position in the list.
- List: the values.
- Delete: swap the item with the last item, then pop the last. This avoids a slow shift.

## Example 3: min stack
Store `(value, current_min)` on each push. The min is always the top's second item.

## Example 4: time-based store
Dict: key → list of `(time, value)` in time order. For a query, use `bisect` to find the latest time ≤ the query time.

## Classic problems
LRU Cache, LFU Cache, Min Stack, Implement Queue using Stacks, Insert Delete GetRandom O(1),
Time Based Key-Value Store, Design Twitter, Implement Trie.

## Mistakes
- Forgetting to update the position map after a swap-delete.
- Not handling removing a key that does not exist.
