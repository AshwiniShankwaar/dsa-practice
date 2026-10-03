# 02 — Two Pointers

## Idea
Use two indexes instead of a nested loop. Each index moves forward, so the work is O(n).

## Type A: one from each end (sorted array)
Start at both ends. If the sum is too small, move the left one right. If too big, move the right one left.
```python
def two_sum_sorted(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target:
            return [lo, hi]
        if s < target:
            lo += 1
        else:
            hi -= 1
    return []
```

## Type B: read pointer and write pointer (in place)
`r` reads every item. `w` marks where the next kept item goes.
```python
def remove_duplicates(nums):          # sorted input
    if not nums:
        return 0
    w = 1
    for r in range(1, len(nums)):
        if nums[r] != nums[w - 1]:
            nums[w] = nums[r]
            w += 1
    return w
```

## Type C: three groups (Sort Colors)
Keep 0s at the front, 2s at the back, 1s in the middle.

## Useful tricks
- **Reverse a part** to rotate: reverse all, then reverse the first k, then the rest.
- **Kadane (max subarray)**: keep `cur = max(x, cur + x)`. If the running sum becomes negative, start fresh.
- **Boyer-Moore (majority)**: keep a candidate and a count; same value → +1, different → −1.

## Classic problems
Two Sum II, Remove Duplicates, Remove Element, Sort Colors, 3Sum (sort + two pointers),
Container With Most Water (move the shorter wall), Trapping Rain Water, Maximum Subarray.

## Mistakes
- Forgetting the array must be sorted for Type A.
- Off-by-one: last index is `len - 1`.
- 3Sum duplicates: skip equal values after a match.
