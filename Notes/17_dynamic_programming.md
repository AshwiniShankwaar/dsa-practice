# 17 — Dynamic Programming (DP)

## Idea
Some problems keep solving the same smaller problem again and again.
DP = **solve each small piece once, write the answer down, reuse it.**

Example: climbing stairs. To reach step 5, you came from step 4 or step 3.
`ways[5] = ways[4] + ways[3]`.

## 4 steps to write any DP
1. **State**: what does `dp[i]` mean? (in words, one sentence)
2. **Transition**: how is `dp[i]` built from smaller `dp` values?
3. **Base case**: the smallest values you know directly.
4. **Order**: fill from small to big.

## Example 1: climbing stairs
```python
def climb(n):
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

## Example 2: coin change (fewest coins)
`dp[x]` = fewest coins to make x. Try each coin c: `dp[x] = min(dp[x - c] + 1)`.
```python
def coin_change(coins, amount):
    INF = float("inf")
    dp = [0] + [INF] * amount
    for x in range(1, amount + 1):
        for c in coins:
            if c <= x:
                dp[x] = min(dp[x], dp[x - c] + 1)
    return dp[amount] if dp[amount] != INF else -1
```

## Example 3: 0/1 knapsack (each item once)
Each item: take it or leave it. Loop capacity **backwards** so an item is not used twice.
```python
def knapsack(items, W):           # items = [(weight, value), ...]
    dp = [0] * (W + 1)
    for wt, val in items:
        for w in range(W, wt - 1, -1):
            dp[w] = max(dp[w], dp[w - wt] + val)
    return dp[W]
```

## Example 4: LCS (two strings, common subsequence)
Compare the last letters. Same letter → take it and look at both shorter strings. Different → drop one letter from either side and take the better result.
```python
def lcs(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

## Example 5: longest increasing subsequence (fast version)
Keep `tails[k]` = smallest end of an increasing run of length k+1. Use binary search to place each number.
```python
import bisect
def lis_length(a):
    tails = []
    for x in a:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
```

## Types of DP to recognise
| Type | Clue | Example |
|---|---|---|
| 1D | one index, "best up to i" | climbing stairs, house robber |
| Knapsack | pick items under a limit | subset sum, coin change |
| 2D on two strings | compare two sequences | LCS, edit distance |
| Grid | paths on a grid | unique paths, min path sum |
| Interval | best over a range [l, r] | burst balloons |
| Bitmask | n ≤ 20, visited set | travelling salesman |
| Tree | answer per subtree | house robber III |

## Mistakes
- Wrong loop direction for 0/1 knapsack (forwards lets an item be used twice).
- Base cases missing; `dp[-1]` in Python silently gives the last item.
- Using `inf` as "not reachable" and returning it. Convert to `-1`.

## Practice path
Climbing Stairs → House Robber → Coin Change → Longest Increasing Subsequence → LCS → Edit Distance → 0/1 Knapsack → Unique Paths → Burst Balloons.
