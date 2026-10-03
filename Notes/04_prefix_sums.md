# 04 — Prefix Sums

## Idea
Make a running total once. Then any range sum is one subtraction.

```python
a = [3, 1, 4, 1, 5]
P = [0]
for x in a:
    P.append(P[-1] + x)      # P = [0, 3, 4, 8, 9, 14]

def range_sum(l, r):         # sum of a[l..r], inclusive
    return P[r + 1] - P[l]

range_sum(1, 3)              # 1 + 4 + 1 = 6  -> P[4] - P[1] = 9 - 3 = 6
```

## Subarray sum = k (works with negatives)
Two prefix sums `P[j]` and `P[i]` give subarray `i..j-1` with sum `P[j] - P[i]`.
So for each prefix, count how many earlier prefixes equal `current - k`.
```python
def subarray_sum_eq_k(nums, k):
    seen = {0: 1}            # the empty prefix
    prefix = count = 0
    for x in nums:
        prefix += x
        count += seen.get(prefix - k, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return count
```

## Difference array (many range adds)
To add `v` to `a[l..r]`: `d[l] += v` and `d[r+1] -= v`. Then take prefix sums of `d` once.

## 2D prefix sums
Same idea on a grid: a rectangle sum is 4 lookups. Useful for "sum of submatrix" questions.

## Classic problems
Range Sum Query Immutable, Subarray Sum Equals K, Continuous Subarray Sum (store `prefix % k`),
Product of Array Except Self (prefix and suffix products), Corporate Flight Bookings (difference array).

## Mistakes
- Forgetting `{0: 1}` — you miss subarrays that start at index 0.
- `P` has length n + 1, not n.
