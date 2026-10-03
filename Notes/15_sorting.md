# 15 — Sorting

## Idea
Once data is sorted, many problems become simple: duplicates sit next to each other, pairs can be found with two pointers, and intervals line up.

## Python
```python
a = [3, 1, 2]
a.sort()                       # in place
b = sorted(a, reverse=True)    # new list, biggest first
pairs = [(1, 9), (2, 3)]
pairs.sort(key=lambda p: p[1]) # sort by second item
words = ["bb", "a", "ccc", "ab"]
words.sort(key=lambda w: (len(w), w))   # by length, then alphabetically
```

## Idea 1: merge sort (split, sort halves, merge)
Split in half, sort each half, then merge two sorted lists. O(n log n).
```python
def merge_sort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left, right = merge_sort(a[:mid]), merge_sort(a[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]
```
Bonus use: while merging, count how many pairs are out of order (inversions).

## Idea 2: quickselect (k-th smallest without full sort)
Pick a pivot, split into smaller / equal / bigger, and only recurse into the side with the answer.

## Idea 3: sort first, then solve
- Intervals: sort by start, then merge overlapping ones.
- Two sum in sorted list: two pointers.
- Duplicates: they become neighbours.

## Classic problems
Sort Colors, Kth Largest Element (quickselect), Merge Intervals, Largest Number (custom comparator: `a+b > b+a`),
Reverse Pairs, Sort List.

## Mistakes
- Sorting strings: `"10" < "9"` is True. Compare numbers as numbers.
- Quickselect with a fixed first pivot is slow on sorted input. Pick a random pivot.
