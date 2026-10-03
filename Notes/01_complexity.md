# 01 — Complexity (How Fast Is It?)

Big-O says how work grows when the input grows. Ignore constants.

## Common speeds
| Big-O | Meaning | Example |
|---|---|---|
| O(1) | Same time always | `x in dict`, `a[5]` |
| O(log n) | Halves each step | binary search |
| O(n) | One pass | loop over list once |
| O(n log n) | Sorting | `sorted(a)` |
| O(n²) | Two nested loops | compare every pair |
| O(2ⁿ) | Every subset | try every yes/no choice |
| O(n!) | Every ordering | all permutations |

## Quick rules
- One loop → O(n). A loop inside a loop → multiply: O(n·m).
- Loop that halves (`i //= 2`) → O(log n).
- `x in list` is O(n). `x in set` is O(1). Use a set when checking membership a lot.
- `s += c` in a loop is slow for strings. Use a list and `"".join(list)`.
- `list.pop(0)` is O(n). Use `deque.popleft()`.

## Amortised = "usually cheap"
A monotonic stack's inner `while` looks slow, but each item is pushed and popped once, so the total is O(n).

## Always say
"Time is O(…) because …. Space is O(…) because …."
