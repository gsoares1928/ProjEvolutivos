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
        self.fit_val = None
    
    def fitness(self, maze, exit1, exit2):
        if self.fit_val is None:
            self.fit_val = 0
            x, y = exit1
            vis = np.zeros_like(maze)
            for move in self.seq:
                if abs(exit2[0] - x) + abs(exit2[1] - y) == 0:
                    break
                vis[x, y] = 1
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
                if vis[x, y]:
                    self.fit_val -= 1
                else:
                    self.fit_val += 2
                if _is_corner(maze, x, y):
                    self.fit_val -= 8
            dist = abs(exit2[0] - x) + abs(exit2[1] - y)
            self.fit_val -= dist
            if dist == 0:
                self.fit_val = float('inf')
        return self.fit_val
    
    def combine(self, other):
        k = int(min(len(self.seq), len(other.seq)) * _rng.random())
        self.seq = other.seq[:k] + self.seq[k:]
        #for i in range():
            #if _rng.random() < 0.5:
                #self.seq[i] = other.seq[i]
        self.fit_val = None
        pass
    
    def mutation(self, mutation_factor):
        if len(self.seq) > 0 and _rng.random() < mutation_factor[2]:
            del self.seq[-1]
        if len(self.seq) == 0 or _rng.random() < mutation_factor[0]:
            self.seq.append(_random_move())
        if len(self.seq) > 0 and _rng.random() < mutation_factor[1]:
            self.seq[-1] = _random_move()
        self.fit_val = None

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
    
    def next_gen(self):
        pop_fitness = [ind.fitness(self.maze, self.exit1, self.exit2) for ind in self.pop]
        best = np.argsort(pop_fitness)[::-1]
        top = max(self.num // 10, 1)
        if pop_fitness[best[0]] == float('inf'):
            return
        self.gen_number += 1
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
        for i in best[top:]:
            j = best[_rng.integers(top)]
            self.pop[i].combine(self.pop[j])
            self.pop[i].mutation(self.mutation_factor)
        if self.predate_every is not None and self.gen_number % self.predate_every == 0:
            worst = best[-1]
            self.pop[worst] = Individual()
    
    def plot(self, plt):
        pop_fitness = [ind.fitness(self.maze, self.exit1, self.exit2) for ind in self.pop]
        best = np.argmax(pop_fitness)
        if pop_fitness[best] == float('inf'):
            plt.title(f'Generation: {self.gen_number}')
        else:
            plt.title(f'Generation: {self.gen_number} Best fitness: {pop_fitness[best]:.3f}')
        all_nodes = []
        x, y = self.exit1
        node = plt.plot(y, x, marker='.', color='blue')
        all_nodes.extend(node)
        for move in self.pop[best].seq:
            if abs(self.exit2[0] - x) + abs(self.exit2[1] - y) == 0:
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
                or x >= self.maze.shape[0] 
                or y >= self.maze.shape[1] 
                or self.maze[x, y] == 0
            ):
                x, y = old_x, old_y
            else:
                node = plt.plot(y, x, marker='.', color='blue')
                all_nodes.extend(node)
                pass
        return all_nodes
