# 19 — Bit Manipulation

## Idea
Numbers are stored as bits (0s and 1s). Bit operations are very fast and solve some puzzles in one line.

## The 5 operators you need
| Operator | Meaning | Example |
|---|---|---|
| `&` | both bits are 1 | `6 & 3 = 2` (110 & 011 = 010) |
| `\|` | either bit is 1 | `6 \| 3 = 7` |
| `^` | bits differ (XOR) | `6 ^ 3 = 5` |
| `<<` | shift left (×2) | `1 << 3 = 8` |
| `>>` | shift right (÷2) | `8 >> 2 = 2` |

## Useful tricks
- Is the number odd? `x & 1`
- Is x a power of two? `x > 0 and x & (x - 1) == 0`
- Remove the lowest 1 bit: `x & (x - 1)`
- Check bit i: `(x >> i) & 1`
- Count 1-bits: `bin(x).count("1")`

## XOR trick: find the one that appears once
`x ^ x = 0` and `x ^ 0 = x`. XOR all numbers: pairs cancel, the single one remains.
```python
def single_number(nums):
    ans = 0
    for x in nums:
        ans ^= x
    return ans
```

## Subsets with bitmasks
Each number 0 … 2ⁿ−1 is a yes/no pattern for n items.
```python
items = ["a", "b", "c"]
for mask in range(1 << len(items)):
    subset = [items[i] for i in range(len(items)) if mask >> i & 1]
```

## Mistakes
- Operator precedence in Python: `a & b == c` means `a & (b == c)`. Always write `(a & b) == c`.
- Python integers have no fixed size, so there is no automatic overflow.

## Classic problems
Single Number, Number of 1 Bits, Counting Bits, Power of Two, Missing Number, Reverse Bits, Gray Code, Subsets (bitmask).
