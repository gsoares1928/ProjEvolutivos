import numpy as np

_rng = np.random.default_rng()

def _random_move():
    return 'udlr'[_rng.integers(4)]
    
def _is_inverse(move1, move2):
    if move1 == 'u' and move2 == 'd':
        return True
    if move1 == 'd' and move2 == 'u':
        return True
    if move1 == 'l' and move2 == 'r':
        return True
    if move1 == 'r' and move2 == 'l':
        return True
    return False

def _is_corner(maze, x, y):
    if (
        x == 0 
        or y == 0 
        or x == maze.shape[0] - 1 
        or y == maze.shape[1] - 1 
    ):
        return False
    return int(maze[x - 1, y]) + int(maze[x + 1, y]) + int(maze[x, y - 1]) + int(maze[x, y + 1]) <= 1
    #return np.sum(maze[x - 1:x + 2, y - 1:y + 2]) == 2

class Individual:
    def __init__(self, seq = None):
        self.seq = seq if seq is not None else [_random_move()]
        self.path = None
    
    def calc_path(self, maze, exit1, exit2, markers = None):
        if self.path is not None:
            return
        
        self.path = [exit1]
        for move in self.seq:
            x, y = self.path[-1]
            if exit2 == (x, y):
                break
            old_x, old_y = x, y
            if move == 'u':
                x -= 1
            elif move == 'd':
                x += 1
            elif move == 'l':
                y -= 1
            elif move == 'r':
                y += 1
            if (
                x < 0 
                or y < 0 
                or x >= maze.shape[0] 
                or y >= maze.shape[1] 
                or not maze[x, y]
            ):
                x, y = old_x, old_y
            self.path.append((x, y))
        self.last_pos = self.path[-1]
        
        if markers is not None and exit1 != (x, y) != exit2 and _is_corner(maze, x, y):
            markers[x, y] = False
    
    def fitness(self, maze, exit1, exit2):
        fit_val = 0
        vis = np.zeros_like(maze)
        for x, y in self.path:
            vis[x, y] = True
        fit_val += np.sum(vis)
        dist = abs(exit2[0] - x) + abs(exit2[1] - y)
        fit_val -= dist
        if dist == 0:
            fit_val = float('inf')
        return fit_val
    
    def combine(self, other):
        k = int(min(len(self.seq), len(other.seq)) * _rng.random())
        self.seq = other.seq[:k] + self.seq[k:]
        pass
    
    def mutation(self, mutation_factor, advance_only = False):
        if len(self.seq) > 0 and _rng.random() < mutation_factor[2] and not advance_only:
            del self.seq[-1]
        if len(self.seq) == 0 or _rng.random() < mutation_factor[0]:
            self.seq.append(_random_move())
        if len(self.seq) > 0 and _rng.random() < mutation_factor[1] and not advance_only:
            self.seq[-1] = _random_move()
        if len(self.seq) > 1 and _is_inverse(self.seq[-2], self.seq[-1]):
            self.seq[-1] = self.seq[-2]
        self.path = None

class Population:
    def __init__(self, num, mutation_factor, predate_every, maze, exit1, exit2):
        self.num = num
        self.mutation_factor = mutation_factor
        self.predate_every = predate_every
        self.maze = maze
        self.exit1 = exit1
        self.exit2 = exit2
    
    def generate(self):
        self.gen_number = 0
        self.pop = [Individual() for i in range(self.num)]
        self.last_fitness = -float('inf')
        self.markers = np.ones_like(self.maze)
        self.pop_fitness = None
    
    def next_gen(self):
        marked_maze = self.maze & self.markers
        new_markers = np.ones_like(self.markers)
        for i, ind in enumerate(self.pop):
            ind.calc_path(marked_maze, self.exit1, self.exit2, new_markers)
        self.markers = self.markers & new_markers
        self.pop_fitness = [ind.fitness(marked_maze, self.exit1, self.exit2) for ind in self.pop]
        
        best = np.argsort(self.pop_fitness)[::-1]
        top = max(self.num // 10, 1)
        if self.pop_fitness[best[0]] == float('inf'):
            return
        self.gen_number += 1
        
        for i in best[top:]:
            j = best[_rng.integers(top)]
            self.pop[i].combine(self.pop[j])
            self.pop[i].mutation(self.mutation_factor)
        
        for i in best[:top]:
            self.pop[i].mutation(self.mutation_factor, advance_only = True)
        
        self.last_fitness = self.pop_fitness[best[0]]
        
        if self.predate_every is not None and self.gen_number % self.predate_every == 0:
            for i in best[-top:]:
                self.pop[i] = Individual()
    
    def plot(self, plt):
        if self.pop_fitness is None:
            return []
        all_nodes = []
        best = np.argmax(self.pop_fitness)
        if self.pop_fitness[best] == float('inf'):
            plt.title(f'Generation: {self.gen_number}')
            for x, y in self.pop[best].path:
                node = plt.plot(y, x, marker='.', color='green')
                all_nodes.extend(node)
        else:
            plt.title(f'Generation: {self.gen_number} Best fitness: {self.pop_fitness[best]:.3f}')
            for x in range(self.markers.shape[0]):
                for y in range(self.markers.shape[1]):
                    if not self.markers[x, y]:
                        node = plt.plot(y, x, marker='x', color='red')
                        all_nodes.extend(node)
            for ind in self.pop:
                x, y = ind.last_pos
                node = plt.plot(y, x, marker='1', color='blue')
                all_nodes.extend(node)
        return all_nodes
