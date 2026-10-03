# 03 — Sliding Window

## Idea
Imagine a box sliding over the array. The box has a left edge and a right edge.
- Move the **right** edge to add items.
- Move the **left** edge to remove items when the box breaks the rule.
Each edge only moves forward, so it is O(n).

## Template: longest valid window
```python
def longest_unique(s):
    last = {}                 # char -> where it last appeared
    left = best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1       # jump the left edge past the old copy
        last[ch] = right
        best = max(best, right - left + 1)
    return best
```

## Template: shortest valid window
Shrink while the window is still valid, and record the size each time.
```python
def min_subarray_len(target, nums):     # positive numbers
    left = total = 0
    best = float("inf")
    for right, x in enumerate(nums):
        total += x
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return 0 if best == float("inf") else best
```

## Fixed size k
Add the new item on the right, remove the old one on the left.

## Rule of thumb
- **Longest**: shrink while the window is *invalid*.
- **Shortest**: shrink while the window is *valid*.

## Classic problems
Longest Substring Without Repeating Characters, Minimum Size Subarray Sum,
Longest Repeating Character Replacement, Find All Anagrams, Minimum Window Substring,
Subarrays with K Different Integers (answer = atMost(K) − atMost(K−1)).

## Mistakes
- Negative numbers break "shrink when sum is too big". Use prefix sums ([04](04_prefix_sums.md)).
- Window length is `right - left + 1`, not `right - left`.
