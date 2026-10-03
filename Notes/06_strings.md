# 06 — Strings

## Basics
- Strings cannot change: `s[0] = "x"` fails. Build a list and join it.
- `s[::-1]` reverses. `ord("a")` gives 97. `ord(c) - ord("a")` gives 0–25.
- `s.split()` splits on any spaces and drops empty parts.

## Palindrome check (two pointers)
A palindrome reads the same both ways. Compare the ends, move inward.
```python
def is_palindrome(s):
    l, r = 0, len(s) - 1
    while l < r:
        while l < r and not s[l].isalnum(): l += 1
        while l < r and not s[r].isalnum(): r -= 1
        if s[l].lower() != s[r].lower():
            return False
        l += 1
        r -= 1
    return True
```

## Longest palindrome substring (expand from the middle)
Every palindrome has a center. Try each center and grow outward.
Two kinds of center: one letter (`aba`) or between two letters (`abba`).

## Pattern matching
- **Simple**: `pattern in text` (fine for most contest work).
- **KMP**: avoids re-checking letters. Know the idea: when a match breaks, use the pattern's own prefix info to jump ahead.
- **Anagram check**: compare letter counts (`Counter(a) == Counter(b)`).

## Classic problems
Valid Palindrome, Longest Palindromic Substring, Valid Anagram, Longest Common Prefix (sort the list; compare first and last),
Implement strStr, Repeated Substring Pattern, Decode String (use a stack, see [07](07_stack_monotonic.md)).

## Mistakes
- Building strings with `+=` in a long loop. Use join.
- `isalnum()` counts digits as alphanumeric; `isalpha()` does not.
