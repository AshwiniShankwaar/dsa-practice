# 16 — Recursion and Backtracking

## Recursion in one sentence
A function that calls itself on a smaller problem, and stops at a base case.

Checklist:
1. What is the smallest case I can answer directly? (base case)
2. How does a bigger case become a smaller case? (recursive step)

## Backtracking: choose, explore, undo
Like walking a maze: step in, keep going, and if you hit a dead end, step back out and try another path.
```python
def backtrack(path):
    if done(path):
        answer.append(path[:])     # save a COPY
        return
    for choice in options(path):
        path.append(choice)        # choose
        backtrack(path)            # explore
        path.pop()                 # undo
```

## Example: subsets (each item in or out)
```python
def subsets(nums):
    res, path = [], []
    def dfs(i):
        if i == len(nums):
            res.append(path[:])
            return
        path.append(nums[i])       # take it
        dfs(i + 1)
        path.pop()                 # leave it
        dfs(i + 1)                 # skip it
    dfs(0)
    return res
```

## Example: permutations (each item once)
Keep a `used` list. Try each unused item, mark it used, recurse, then unmark.

## Speed-ups
- Sort the input and skip choices that repeat the previous one (for duplicates).
- Stop early when a partial choice already breaks the rule (pruning).

## Classic problems
Subsets, Permutations, Combination Sum, Letter Combinations of a Phone Number, Generate Parentheses,
Palindrome Partitioning, Word Search, N-Queens, Sudoku Solver.

## Mistakes
- `result.append(path)` saves a reference. Always append `path[:]`.
- Forgetting to undo (`pop`) leaves garbage in the path.
- Exponential time: check input size first (see [00](00_problem_solving_framework.md)).
