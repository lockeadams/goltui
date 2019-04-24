""" CONWAYS GAME OF LIFE """

import random
import collections
from collections import UserList

class CellList(UserList):
    """ List object representing cells for Game of Life. """

    cell_state = {'alive' : True, 'dead' : False}

    def __init__(self, lines, cols):
        """ Creates cell list of given dimensions and initializes them to all dead. """
        self.lines = lines
        self.cols = cols
        self.generation = 0
        initial_list = [[self.cell_state['dead']] * cols for x in range(lines)]
        super().__init__(initial_list)

    def generate_random(self, prob_alive=0.3):
        """ Randomly assigns each cell in list to dead or alive. """
        for i in range(self.lines):
            for j in range(self.cols):
                if random.random() < prob_alive:
                    self[i][j] = self.cell_state['alive']

    def get_neighbors(self, line, col):
        """ Returns number of neighbors for a given cell at line, col. """
        neighbors = 0
        for line_shift in [-1, 0, 1]:
            for col_shift in [-1, 0, 1]:
                if line_shift == 0 and col_shift == 0:
                    continue # Do not count given cell
                # % connects left/right and up/down
                i = (line + line_shift) % self.lines
                j = (col + col_shift) % self.cols
                if self[i][j] == self.cell_state['alive']:
                    neighbors += 1
        return neighbors

    def advance_generation(self):
        """ Advances cell list to next generation based on Conway's rules. """
        self.generation += 1
        next_cells = [[self.cell_state['dead']] * self.cols for x in range(self.lines)]
        for i in range(self.lines):
            for j in range(self.cols):
                neighbors = self.get_neighbors(i, j)
                if self[i][j] == self.cell_state['alive']:
                    if neighbors == 2 or neighbors == 3:
                        next_cells[i][j] = self.cell_state['alive']
                elif self[i][j] == self.cell_state['dead']:
                    if neighbors == 3:
                        next_cells[i][j] = self.cell_state['alive']
        super().__init__(next_cells)

    def get_population(self):
        """ Returns number of alive cells. """
        population = 0
        for i in self:
            population += i.count(self.cell_state['alive'])
        return population

