# 05 — Hashing (dict and set)

## Idea
A dict or set answers "is it here?" and "what is its value?" in about O(1).
Trade a little memory for speed: a nested loop of O(n²) becomes one loop of O(n).

## Tools
- `set()` — membership and removing duplicates
- `dict` — key → value (for example, value → index)
- `Counter` — count items: `Counter("hello")` → `{'l': 2, ...}`
- `defaultdict(list)` — group items without checking if the key exists

## Template 1: find a pair (Two Sum)
For each number, ask: "have I already seen the number I need?"
```python
def two_sum(nums, target):
    seen = {}                       # value -> index
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []
```

## Template 2: group things
```python
from collections import defaultdict
def group_anagrams(words):
    groups = defaultdict(list)
    for w in words:
        groups["".join(sorted(w))].append(w)   # same sorted letters = same key
    return list(groups.values())
```

## Template 3: longest consecutive run
Put everything in a set. Only start counting at a number whose `x - 1` is not in the set. Each run is counted once.

## Classic problems
Contains Duplicate, Valid Anagram, Two Sum, Group Anagrams, Top K Frequent Elements,
Longest Consecutive Sequence, Subarray Sum Equals K (see [04](04_prefix_sums.md)).

## Mistakes
- Lists cannot be dict keys. Convert to `tuple`.
- `d[key]` on a `defaultdict` creates the key. Use `d.get(key, 0)` to only read.
