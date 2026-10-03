# 24 — Pattern Cheat-Sheet

Read the problem, find the clue in the left column, use the technique on the right.

| If you see… | Use | Note |
|---|---|---|
| sorted list, find a pair | two pointers | [02](02_arrays_two_pointers.md) |
| longest/shortest contiguous part | sliding window | [03](03_sliding_window.md) |
| subarray sum = k (negatives allowed) | prefix sums + dict | [04](04_prefix_sums.md) |
| "have I seen it?", counts, groups | dict / set / Counter | [05](05_hashing.md) |
| palindrome, anagram, pattern in text | two pointers, counts, KMP | [06](06_strings.md) |
| matching brackets, undo | stack | [07](07_stack_monotonic.md) |
| next greater / smaller | monotonic stack | [07](07_stack_monotonic.md) |
| k-th largest, top K | heap | [08](08_heaps_deques.md) |
| sliding window maximum | monotonic deque | [08](08_heaps_deques.md) |
| reverse / cycle / middle of list | pointers | [09](09_linked_lists.md) |
| depth, path, ancestor, tree shape | recursion on children | [10](10_trees.md) |
| prefix search over many words | trie | [11](11_tries.md) |
| tasks with order / prerequisites | topological sort | [12](12_graphs.md) |
| shortest path, no weights | BFS | [12](12_graphs.md) |
| shortest path, weights | Dijkstra | [12](12_graphs.md) |
| groups merging together | union-find | [13](13_union_find.md) |
| minimum X that works (monotone) | binary search on answer | [14](14_binary_search.md) |
| sorted or rotated array | binary search | [14](14_binary_search.md) |
| all combinations / permutations | backtracking | [16](16_recursion_backtracking.md) |
| max/min/count over choices, repeats | DP | [17](17_dynamic_programming.md) |
| knapsack, coin amount | DP (knapsack) | [17](17_dynamic_programming.md) |
| two strings, common subsequence | 2D DP | [17](17_dynamic_programming.md) |
| schedule, non-overlapping intervals | sort + greedy | [18](18_greedy_intervals.md) |
| odd one out, power of two | bits | [19](19_bit_manipulation.md) |
| n ≤ 20 with all subsets | bitmask | [19](19_bit_manipulation.md) |
| answer mod 10⁹+7, nCr | math / combinatorics | [20](20_math_number_theory.md) |
| primes up to N | sieve | [20](20_math_number_theory.md) |
| many updates + range queries | Fenwick / segment tree | [21](21_segment_tree_fenwick.md) |
| grid, islands, spreading | BFS / DFS on grid | [22](22_grid_matrix.md) |
| design a fast data structure | dict + linked list / heap | [25](25_design_problems.md) |

## Input size → what you can use
| n | Use |
|---|---|
| ≤ 20 | try all subsets |
| ≤ 500 | n³ |
| ≤ 5,000 | n² |
| ≤ 10⁶ | n or n log n |

## Words that give hints
- "minimum / maximum" → DP, greedy, or binary search
- "number of ways" → DP or counting
- "all possible" → backtracking
- "return any" → greedy
