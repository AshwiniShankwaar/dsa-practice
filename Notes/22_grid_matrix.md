# 22 — Grids and Matrices

## Idea
A grid is a graph where each cell touches its neighbours (up, down, left, right).

## Neighbours (copy this)
```python
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def neighbours(grid, r, c):
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            yield nr, nc
```

## Flood fill (count islands)
When you find land, sink it (mark it visited) and sink everything connected to it.
```python
def count_islands(grid):
    count = 0
    def sink(r, c):
        if not (0 <= r < len(grid) and 0 <= c < len(grid[0])) or grid[r][c] != "1":
            return
        grid[r][c] = "0"
        for nr, nc in neighbours(grid, r, c):
            sink(nr, nc)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "1":
                count += 1
                sink(r, c)
    return count
```

## Multi-source BFS (things spreading at the same time)
Rotting oranges: put **all** rotten oranges in the queue at the start, then BFS. Each BFS layer is one minute.

## Shortest path in a grid
BFS (each step costs 1). Mark a cell when you add it to the queue.

## Matrix tricks
- **Rotate 90° clockwise**: transpose, then reverse each row. (`[list(r) for r in zip(*m[::-1])]`)
- **Spiral order**: keep top, bottom, left, right edges; walk each side and shrink the edge.
- **Set zeros**: use the first row and column as markers instead of extra space.

## Classic problems
Number of Islands, Max Area of Island, Rotting Oranges, 01 Matrix, Surrounded Regions,
Pacific Atlantic Water Flow, Word Search, Spiral Matrix, Rotate Image, Set Matrix Zeroes, Game of Life.

## Mistakes
- Forgetting the bounds check before using `grid[r][c]`.
- Deep recursion on large grids → use BFS or an explicit stack.
- Mixing up row and column when the problem says `(x, y)`.
