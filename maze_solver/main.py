import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_tools import ToolBase

import settings
from maze import generate_maze
from evolutionary import Population, _is_corner

maze, exit1, exit2 = generate_maze(settings.maze_size, settings.maze_size, settings.seed)
pop = Population(settings.num, settings.mutation_factor, settings.predate_every, settings.patience, maze, exit1, exit2)
plt.rcParams['toolbar'] = 'toolmanager'
plt.ion()

fig, ax = plt.subplots()

clean_up = None

class Reset(ToolBase):
    description = 'Reset the population'
    
    def trigger(self, *args, **kwargs):
        global clean_up
        if clean_up is not None:
            for obj in clean_up:
                obj.remove()
        pop.generate()
        clean_up = pop.plot(plt)

class NextGen(ToolBase):
    description = 'Advance to the next generation'
    
    def trigger(self, *args, **kwargs):
        global clean_up
        if clean_up is not None:
            for obj in clean_up:
                obj.remove()
            for i in range(10):
                pop.next_gen()
        else:
            pop.generate()
        clean_up = pop.plot(plt)

fig.canvas.manager.toolmanager.add_tool('NextGen', NextGen)
fig.canvas.manager.toolbar.add_tool('NextGen', 'navigation')
fig.canvas.manager.toolmanager.add_tool('Reset', Reset)
fig.canvas.manager.toolbar.add_tool('Reset', 'navigation')

for i in range(2 * settings.maze_size + 1):
    for j in range(2 * settings.maze_size + 1):
        if _is_corner(maze, i, j):
            plt.plot(j, i, marker='.', color='green')

plt.imshow(maze)
plt.show(block=True)
