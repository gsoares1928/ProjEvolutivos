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
