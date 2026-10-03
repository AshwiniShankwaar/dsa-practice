# 12 — Graphs

## Idea
A graph is nodes (dots) joined by edges (lines). Store it as an adjacency list:
```python
from collections import defaultdict
edges = [(0, 1), (1, 2)]
adj = defaultdict(list)
for u, v in edges:
    adj[u].append(v)
    adj[v].append(u)        # remove this line for a directed graph
```

## BFS: explore in rings (shortest steps, unweighted)
Use a queue. Visit all neighbours of the current node before going further.
Mark a node as seen **when you add it** to the queue.
```python
from collections import deque
def bfs_dist(adj, start, n):
    dist = [-1] * n
    dist[start] = 0
    q = deque([start])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
```

## DFS: go deep first
Use recursion or a stack. Good for "is it connected?" and counting islands.

## Counting components
Loop over all nodes. Each time you find an unvisited one, start a BFS/DFS and add 1 to the count.

## Topological order (tasks with prerequisites)
Start with nodes that have no incoming edges. Remove them and their outgoing edges. Repeat.
If you cannot finish all nodes, there is a cycle.
```python
def topo(n, adj):
    indeg = [0] * n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order            # shorter than n means a cycle
```

## Shortest path with weights (Dijkstra)
Always expand the closest unfinished node next (use a heap). Works only with **non-negative** weights.
```python
import heapq
def dijkstra(adj, src, n):           # adj[u] = [(v, w), ...]
    dist = [float("inf")] * n
    dist[src] = 0
    h = [(0, src)]
    while h:
        d, u = heapq.heappop(h)
        if d > dist[u]:
            continue                 # old entry, skip
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(h, (d + w, v))
    return dist
```

## Which algorithm?
| Situation | Use |
|---|---|
| no weights | BFS |
| weights 0 or 1 | 0-1 BFS (deque) |
| weights ≥ 0 | Dijkstra |
| negative weights | Bellman-Ford |
| all pairs, small n | Floyd-Warshall |
| minimum cost to connect everything | Kruskal or Prim (MST) |

## Classic problems
Number of Islands, Clone Graph, Course Schedule (topo / cycle), Rotting Oranges (multi-source BFS),
Word Ladder (BFS on words), Network Delay Time (Dijkstra), Cheapest Flights Within K Stops,
Min Cost to Connect All Points, Redundant Connection ([13](13_union_find.md)).

## Mistakes
- Forgetting `visited` → infinite loops.
- Using Dijkstra with negative edges.
- Recursive DFS on huge graphs → recursion error. Use a stack.
