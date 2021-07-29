import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_tools import ToolBase

import settings
from maze import generate_maze
from evolutionary import Population, _is_corner

maze, exit1, exit2 = generate_maze(settings.maze_size, settings.maze_size, settings.seed)
pop = Population(settings.num, settings.mutation_factor, settings.predate_every, maze, exit1, exit2)
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
    
    def __init__(self, *args, **kwargs):
        self.skip_cnt = kwargs.pop('skip_cnt', 1)
        if self.skip_cnt == 1:
            self.description = 'Advance to the next generation'
        else:
            self.description = f'Advance {self.skip_cnt} generations'
        super().__init__(*args, **kwargs)
    
    def trigger(self, *args, **kwargs):
        global clean_up
        if clean_up is not None:
            for obj in clean_up:
                obj.remove()
            for i in range(self.skip_cnt):
                pop.next_gen()
        else:
            pop.generate()
        clean_up = pop.plot(plt)

fig.canvas.manager.toolmanager.add_tool('Next', NextGen, skip_cnt = 1)
fig.canvas.manager.toolbar.add_tool('Next', 'navigation')
fig.canvas.manager.toolmanager.add_tool('Next 10', NextGen, skip_cnt = 10)
fig.canvas.manager.toolbar.add_tool('Next 10', 'navigation')
fig.canvas.manager.toolmanager.add_tool('Reset', Reset)
fig.canvas.manager.toolbar.add_tool('Reset', 'navigation')

plt.imshow(maze)
plt.show(block=True)
