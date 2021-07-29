import numpy as np

rng = np.random.default_rng()

class UnionFind:
    def __init__(self, size):
        self.parent = [-1] * size

    def find(self, x):
        root = x
        while self.parent[root] != -1:
            root = self.parent[root]
        while self.parent[x] != -1:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x != y:
            self.parent[x] = y

def random_move():
    return 'udlr'[rng.integers(4)]

def is_inverse(move1, move2):
    if move1 == 'u' and move2 == 'd':
        return True
    if move1 == 'd' and move2 == 'u':
        return True
    if move1 == 'l' and move2 == 'r':
        return True
    if move1 == 'r' and move2 == 'l':
        return True
    return False

def is_corner(maze, x, y):
    if (
        x == 0 
        or y == 0 
        or x == maze.shape[0] - 1 
        or y == maze.shape[1] - 1 
    ):
        return False
    return int(maze[x - 1, y]) + int(maze[x + 1, y]) + int(maze[x, y - 1]) + int(maze[x, y + 1]) <= 1
