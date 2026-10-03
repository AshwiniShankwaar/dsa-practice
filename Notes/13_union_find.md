# 13 — Union-Find (Disjoint Set)

## Idea
Friend groups. Two operations:
- `find(x)`: who is the leader of x's group?
- `union(a, b)`: join two groups.

If `find(a) == find(b)`, they are already in the same group.

## Template
```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))     # everyone starts as their own leader
        self.size = [1] * n
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # shortcut upward
            x = self.parent[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                 # already friends -> this edge makes a cycle
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra             # small group joins big group
        self.size[ra] += self.size[rb]
        return True
```

## Where it helps
- Count connected groups: start with n groups, subtract one per successful union.
- Find the extra edge that makes a cycle: the first `union` that returns False.
- Kruskal's minimum spanning tree: sort edges by cost, union the ones that do not form a cycle.

## Classic problems
Number of Provinces, Redundant Connection, Accounts Merge, Satisfiability of Equality Equations,
Min Cost to Connect All Points, Number of Islands II.

## Mistakes
- Forgetting that after a union, old `find` results may be stale. Call `find` again.
