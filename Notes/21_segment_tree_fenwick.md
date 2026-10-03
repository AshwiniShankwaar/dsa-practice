# 21 — Fenwick Tree and Segment Tree

## Problem these solve
You have a list. Many times you do:
- change one value, and
- ask for a sum (or min/max) over a range.

Plain loops cost O(n) per question. These trees cost O(log n).

## Fenwick tree (BIT): sums with point updates
Simple to write. Index starts at 1.
```python
class Fenwick:
    def __init__(self, n):
        self.n = n
        self.t = [0] * (n + 1)
    def add(self, i, delta):           # a[i] += delta
        while i <= self.n:
            self.t[i] += delta
            i += i & -i
    def prefix(self, i):               # sum of a[1..i]
        s = 0
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s
    def range_sum(self, l, r):         # sum of a[l..r]
        return self.prefix(r) - self.prefix(l - 1)
```
Usage: `f.add(3, 5)` then `f.range_sum(1, 4)`.

## Segment tree: range min/max/sum with point updates
Think of a tournament bracket: each parent stores the result of its two children.
A range query combines only a few nodes.
```python
class SegTree:                          # range sum, 0-indexed
    def __init__(self, a):
        self.n = len(a)
        self.t = [0] * (2 * self.n)
        self.t[self.n:] = a
        for i in range(self.n - 1, 0, -1):
            self.t[i] = self.t[2*i] + self.t[2*i + 1]
    def update(self, i, v):
        i += self.n
        self.t[i] = v
        i //= 2
        while i:
            self.t[i] = self.t[2*i] + self.t[2*i + 1]
            i //= 2
    def query(self, l, r):              # sum of a[l..r-1]
        res = 0
        l += self.n; r += self.n
        while l < r:
            if l & 1:
                res += self.t[l]; l += 1
            if r & 1:
                r -= 1; res += self.t[r]
            l //= 2; r //= 2
        return res
```
For min or max, replace `+` with `min` or `max`.

## Which one?
- Only sums with point updates → Fenwick (shorter).
- Min/max, or more complex updates → segment tree.

## Classic problems
Range Sum Query Mutable, Count of Smaller Numbers After Self (Fenwick with compressed values),
Reverse Pairs, Count Inversions, Range Minimum Query.

## Mistakes
- Fenwick is 1-indexed. Index 0 makes `i & -i` zero and loops forever.
- Forgetting to compress big values before using them as indexes.
