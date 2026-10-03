# 18 — Greedy and Intervals

## Idea
Greedy = at each step, take the choice that looks best right now, and never go back.
It only works if the choice can be proven safe. If you cannot prove it, use DP ([17](17_dynamic_programming.md)).

Quick test: "If I swap in my greedy choice into the best solution, is it still at least as good?" If yes, greedy works.

## Pattern 1: maximum non-overlapping intervals
Sort by **end time**. Take an interval if it starts after the last one you took ends.
```python
def max_non_overlap(iv):
    iv.sort(key=lambda x: x[1])
    end, count = float("-inf"), 0
    for s, e in iv:
        if s >= end:
            count += 1
            end = e
    return count
```

## Pattern 2: merge overlapping intervals
Sort by start. If the next one starts before the current one ends, stretch the current one.
```python
def merge(iv):
    iv.sort()
    out = []
    for s, e in iv:
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
```

## Pattern 3: jump game
Keep track of the farthest index you can reach. If you ever stand past it, you are stuck.
```python
def can_jump(nums):
    far = 0
    for i, x in enumerate(nums):
        if i > far:
            return False
        far = max(far, i + x)
    return True
```

## Pattern 4: counting overlaps (sweep line)
Turn each interval into a "+1 at start" and "−1 at end" event. Sort the events, walk through, and track the running total. The biggest total is the maximum overlap.

## Pattern 5: task scheduler
If the most frequent task has `k` copies, you need at least `(k - 1) * (cooldown + 1) + 1` slots.
The answer is `max(len(tasks), that)`.

## Classic problems
Non-overlapping Intervals, Merge Intervals, Meeting Rooms II, Jump Game I and II, Gas Station,
Task Scheduler, Candy, Partition Labels, Minimum Arrows to Burst Balloons.

## Mistakes
- Sorting by start when you need end (for "maximum count" problems).
- Touching intervals `[1,2]` and `[2,3]`: check the statement — do they overlap?
- Trusting greedy without a test. Compare against brute force on small random inputs.
