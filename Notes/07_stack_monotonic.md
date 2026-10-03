# 07 — Stack and Monotonic Stack

## Stack idea
A stack is a pile of plates: you add and remove only from the top. Use it when the **most recent unmatched** item matters.

## Example: matching brackets
Opening bracket → push. Closing bracket → top must match, then pop.
```python
def is_valid(s):
    pair = {')': '(', ']': '[', '}': '{'}
    st = []
    for ch in s:
        if ch in pair:
            if not st or st[-1] != pair[ch]:
                return False
            st.pop()
        else:
            st.append(ch)
    return not st
```

## Monotonic stack idea
Keep the stack sorted (for example, values going down). When a new item breaks the order, pop the old items: the new item is their answer.

## Template: next greater element
```python
def next_greater(a):
    res = [-1] * len(a)
    st = []                        # indexes of items still waiting for an answer
    for i, x in enumerate(a):
        while st and a[st[-1]] < x:
            res[st.pop()] = x      # x is the next greater for that waiting item
        st.append(i)
    return res
```
Each item is pushed once and popped once, so it is O(n).

## Largest rectangle in histogram (the classic hard one)
For each bar, you need the nearest shorter bar on the left and right. A monotonic stack finds both in one pass.
Add a 0 at the end so everything is flushed out.

## Classic problems
Valid Parentheses, Min Stack, Evaluate Reverse Polish Notation, Daily Temperatures,
Next Greater Element, Largest Rectangle in Histogram, Remove K Digits, Basic Calculator, Decode String.

## Mistakes
- Popping from an empty stack: check `st` first.
- Store **indexes** when you need widths or distances; store **values** when you only compare.
