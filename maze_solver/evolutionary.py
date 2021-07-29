import numpy as np

_rng = np.random.default_rng()

def _random_move():
    return 'udlr'[_rng.integers(4)]

def _is_corner(maze, x, y):
    if (
        x == 0 
        or y == 0 
        or x == maze.shape[0] - 1 
        or y == maze.shape[1] - 1 
    ):
        return False
    return np.sum(maze[x - 1:x + 2, y - 1:y + 2]) == 2

class Individual:
    def __init__(self, seq = None):
        self.seq = seq if seq is not None else [_random_move()]
        self.path = None
    
    def calc_path(self, maze, exit1, exit2):
        if self.path is not None:
            return
        
        self.path = [exit1]
        for move in self.seq:
            x, y = self.path[-1]
            if exit2[0] == x and exit2[1] == y:
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
                or maze[x, y] == 0
            ):
                x, y = old_x, old_y
            self.path.append((x, y))
    
    def populate_markers(self, markers, i):
        for x, y in self.path:
            markers[x, y, i] = 1
    
    def fitness(self, maze, exit1, exit2, markers):
        fit_val = 0
        vis = np.zeros_like(maze)
        for x, y in self.path:
            fit_val -= markers[x, y] - 1
            fit_val -= _is_corner(maze, x, y) * 8
            vis[x, y] = 1
        fit_val += 3 * np.sum(vis)
        dist = abs(exit2[0] - x) + abs(exit2[1] - y)
        fit_val -= dist
        if dist == 0:
            fit_val = float('inf')
        return fit_val
    
    def combine(self, other):
        k = int(min(len(self.seq), len(other.seq)) * _rng.random())
        self.seq = other.seq[:k] + self.seq[k:]
        pass
    
    def mutation(self, mutation_factor):
        if len(self.seq) > 0 and _rng.random() < mutation_factor[2]:
            del self.seq[-1]
        if len(self.seq) == 0 or _rng.random() < mutation_factor[0]:
            self.seq.append(_random_move())
        if len(self.seq) > 0 and _rng.random() < mutation_factor[1]:
            self.seq[-1] = _random_move()
        self.path = None

class Population:
    def __init__(self, num, mutation_factor, predate_every, patience, maze, exit1, exit2):
        self.num = num
        self.mutation_factor = mutation_factor
        self.predate_every = predate_every
        self.patience = patience
        self.maze = maze
        self.exit1 = exit1
        self.exit2 = exit2
    
    def generate(self):
        self.gen_number = 0
        self.pop = [Individual() for i in range(self.num)]
        self.cur_patience = self.patience
        self.last_fitness = -float('inf')
        self.markers = np.zeros_like(self.maze)
    
    def next_gen(self):
        new_markers = np.zeros(self.maze.shape + (self.num, ))
        for i, ind in enumerate(self.pop):
            ind.calc_path(self.maze, self.exit1, self.exit2)
            ind.populate_markers(new_markers, i)
        new_markers = 2 * np.sum(new_markers, axis=2) / self.num
        self.markers = self.markers * 0.5 + new_markers
        pop_fitness = [ind.fitness(self.maze, self.exit1, self.exit2, self.markers) for ind in self.pop]
        
        best = np.argsort(pop_fitness)[::-1]
        top = max(self.num // 10, 1)
        if pop_fitness[best[0]] == float('inf'):
            return
        self.gen_number += 1
        
        for i in best[top:]:
            j = best[_rng.integers(top)]
            self.pop[i].combine(self.pop[j])
            self.pop[i].mutation(self.mutation_factor)
        
        if pop_fitness[best[0]] == self.last_fitness:
            self.cur_patience -= 1
            if self.cur_patience == 0:
                self.cur_patience = self.patience
                for i in best[:top]:
                    self.pop[i] = Individual()
                return
        else:
            self.cur_patience = self.patience
        self.last_fitness = pop_fitness[best[0]]
        
        if self.predate_every is not None and self.gen_number % self.predate_every == 0:
            for i in best[-top:]:
                self.pop[i] = Individual()
    
    def plot(self, plt):
        for i, ind in enumerate(self.pop):
            ind.calc_path(self.maze, self.exit1, self.exit2)
        pop_fitness = [ind.fitness(self.maze, self.exit1, self.exit2, self.markers) for ind in self.pop]
        
        best = np.argmax(pop_fitness)
        if pop_fitness[best] == float('inf'):
            plt.title(f'Generation: {self.gen_number}')
        else:
            plt.title(f'Generation: {self.gen_number} Best fitness: {pop_fitness[best]:.3f}')
        
        all_nodes = []
        for x, y in self.pop[best].path:
            node = plt.plot(y, x, marker='.', color='blue')
            all_nodes.extend(node)
        x, y = self.exit1
        node = plt.plot(y, x, marker='.', color='blue')
        all_nodes.extend(node)
        return all_nodes
