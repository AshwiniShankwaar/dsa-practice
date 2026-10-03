# 23 — Contest and Python Tips

## Fast input (for contests)
```python
import sys
data = sys.stdin.buffer.read().split()    # read everything at once
n = int(data[0])
```
Print once at the end: `sys.stdout.write("\n".join(map(str, out)) + "\n")`.

## Deep recursion
Python stops at about 1000 nested calls. Two fixes:
```python
import sys
sys.setrecursionlimit(10**6)
```
Or, better, write the recursion with an explicit stack (a list you push to and pop from).

## Standard library you should know
| Module | Use for |
|---|---|
| `collections` | `deque` (queue), `Counter` (counts), `defaultdict` (groups) |
| `heapq` | smallest item fast |
| `bisect` | binary search in a sorted list |
| `itertools` | `permutations`, `combinations`, `accumulate` |
| `functools` | `lru_cache` (auto-memoise a function) |
| `math` | `gcd`, `isqrt`, `comb` |

## Handy Python
- `for i, x in enumerate(a):` — index and value
- `zip(*matrix)` — transpose
- `a[::-1]` — reverse
- `divmod(7, 2)` → `(3, 1)`
- `float("inf")` — a value bigger than anything
- `first, *rest = items`

## Speed tips
- Use a `set` for "is it there?" checks, not a list.
- Build strings with `"".join(list)`, not `+=` in a loop.
- Create lists at full size: `dp = [0] * (n + 1)`.
- Python does about 10⁷ simple steps per second. For 10⁶ items, keep each loop body small.

## Traps
- `/` gives a float; `//` gives an integer.
- `int(-7 / 2)` is -3, but `-7 // 2` is -4. Pick the one you mean.
- Comparing floats with `==` can fail. Use a small tolerance.

## Contest habit
Read all the problems first. Start with the one that looks easiest. If you have been stuck for 15 minutes, check [24](24_pattern_cheatsheet.md) for another approach.
