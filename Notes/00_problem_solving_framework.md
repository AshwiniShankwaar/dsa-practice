# 00 — How to Solve Any Problem

## The 5 steps
1. **Understand**: What is the input? What is the output? Try a tiny example by hand.
2. **Brute force**: Write the slow, obvious solution first. It makes the idea clear.
3. **Find the waste**: What work is repeated? Can I remember it, sort it, or skip it?
4. **Pick a pattern**: Use [24 — cheat-sheet](24_pattern_cheatsheet.md).
5. **Test edge cases**: empty input, one item, all same, negatives, biggest input.

## Input size tells you the speed you need
| n (input size) | You can afford |
|---|---|
| up to 20 | try all subsets (2ⁿ) |
| up to 500 | n³ (three nested loops) |
| up to 5,000 | n² (two nested loops) |
| up to 10⁶ | n or n log n only |

## Common edge cases
- Empty list / empty string / `None`
- One element
- All numbers equal
- Negative numbers and zero
- Duplicates

## When stuck
- Solve a smaller version (n = 3) by hand.
- Ask: "what do I need to know to answer the last step?"
- Write the brute force, then look at what it recomputes.
