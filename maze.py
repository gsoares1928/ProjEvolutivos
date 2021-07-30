import numpy as np
from random import randint, shuffle, seed

from utils import UnionFind

class MazeNode:
    def __init__(self, x, y = None, m = None):
        assert y is not None or m is not None

        if y is not None:
            self.x = x
            self.y = y
        else:
            self.x = x // m
            self.y = x % m
        self.open_down = self.open_right = False

    def __str__(self):
        return f'({self.x}, {self.y})'

def generate_nodes(n, m):
    nodes = [MazeNode(i, m = m) for i in range(n * m)]
    edges = []
    edges.extend([(i, i + 1, False) for i in range(n * m) if i % m != m - 1])
    edges.extend([(i, i + m, True) for i in range(n * m - m)])
    shuffle(edges)
    uf = UnionFind(n * m)
    for u, v, vert in edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            if vert:
                nodes[u].open_down = True
            else:
                nodes[u].open_right = True
    return nodes

def generate_exit(n, m):
    if randint(0, 1):
        exit_coord = 2 * randint(0, m - 1) + 1
        if randint(0, 1):
            return (0, exit_coord)
        else:
            return (2 * n, exit_coord)
    else:
        exit_coord = 2 * randint(0, n - 1) + 1
        if randint(0, 1):
            return (exit_coord, 0)
        else:
            return (exit_coord, 2 * m)

def generate_maze(n, m, sd = None):
    '''Generate a maze of size (2*n+1)x(2*m+1) using the seed sd.'''
    if sd is None:
        sd = randint(0, 1000000000)
    print('Seed:', sd)
    seed(sd)

    nodes = generate_nodes(n, m)
    maze = np.zeros((2 * n + 1, 2 * m + 1), dtype = bool)
    for node in nodes:
        maze[2 * node.x + 1, 2 * node.y + 1] = True
        if node.open_down:
            maze[2 * node.x + 2, 2 * node.y + 1] = True
        if node.open_right:
            maze[2 * node.x + 1, 2 * node.y + 2] = True

    exit1, exit2 = generate_exit(n, m), generate_exit(n, m)
    while exit1 == exit2:
        exit2 = generate_exit(n, m)
    maze[exit1[0], exit1[1]] = True
    maze[exit2[0], exit2[1]] = True

    return maze, exit1, exit2
