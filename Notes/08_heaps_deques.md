# 08 — Heaps and Deques

## Heap idea
A heap always gives you the smallest item quickly (O(log n) to add or remove). Python's `heapq` is a **min-heap**.

```python
import heapq
h = []
heapq.heappush(h, 5)
heapq.heappush(h, 1)
heapq.heappop(h)        # 1 (smallest)
```
**Max-heap trick**: push the negative of each number, then negate when you read it.

## Template: k-th largest
Keep a heap of size k. When it gets too big, remove the smallest. The top is the k-th largest.
```python
def kth_largest(nums, k):
    h = []
    for x in nums:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)
    return h[0]
```

## Template: merge k sorted lists
Put the first item of each list in the heap. Pop the smallest, then push the next item from that same list.

## Two heaps (running median)
- A max-heap for the smaller half (store negatives).
- A min-heap for the bigger half.
- The median sits at the top of one or both.

## Deque idea
A deque is a list you can add to or remove from **both ends** in O(1). Use `collections.deque`.

## Template: sliding window maximum
Keep a deque of indexes whose values go down. The front is always the current maximum.
Remove from the front when it leaves the window; remove from the back when a bigger value arrives.

## Classic problems
Kth Largest Element, Top K Frequent Elements, Find Median from Data Stream, Merge K Sorted Lists,
Sliding Window Maximum, Meeting Rooms II, Task Scheduler, Dijkstra ([12](12_graphs.md)).

## Mistakes
- Heap items that are lists or dicts cannot be compared. Use `(priority, index, item)` tuples.
- Forgetting to negate for a max-heap.
