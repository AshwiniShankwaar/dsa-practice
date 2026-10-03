# 14 — Binary Search

## Idea
Guess the middle. Throw away the half that cannot contain the answer. Repeat.
Works on sorted data, and also on any question with a clear yes/no boundary.

## Template (write it this way every time)
```python
def find_first_true(lo, hi, ok):
    # returns the smallest x in [lo, hi] where ok(x) is True
    # ok must be False ... False True ... True
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid          # mid might be the answer, keep it
        else:
            lo = mid + 1      # mid is too small, drop it
    return lo
```

## Use 1: search in a sorted list
```python
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```
Python shortcut: `bisect.bisect_left(nums, x)` gives the first index where x fits.

## Use 2: search on the answer
Ask: "is speed k fast enough?" If yes for k, it is yes for every bigger k. Find the smallest yes.
Example (Koko bananas): `ok(k) = total hours at speed k ≤ h`. Then `find_first_true(1, max_pile, ok)`.

## Use 3: rotated sorted array
At each step, one half is still sorted. Check if the target is inside that sorted half. If yes, go there; if not, go to the other half.

## Mistakes
- Mixing `lo <= hi` and `lo < hi` styles. Pick the template above and stick to it.
- Forgetting the predicate must flip only once (False then True). Otherwise binary search gives nonsense.
- Infinite loops: each step must shrink the range (`lo = mid + 1` or `hi = mid`).

## Classic problems
Binary Search, Search Insert Position, First and Last Position, Search in Rotated Sorted Array,
Find Minimum in Rotated Sorted Array, Koko Eating Bananas, Capacity To Ship Packages,
Split Array Largest Sum, Median of Two Sorted Arrays (hard).
