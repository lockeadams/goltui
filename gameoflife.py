""" CONWAYS GAME OF LIFE """

import random

class GameOfLife:
    """ Provides necessary operations to play Game of Life. """

    state = {'alive' : True, 'dead' : False}

    def __init__(self, lines, cols):
        """ Creates cell list of given dimensions and initializes them to all dead. """
        self.lines = lines
        self.cols = cols
        self.cells = [[self.state['dead']] * cols for x in range(lines)]
        self.generation = 0

    def generate_random(self, prob_alive=0.5):
        """ Randomly assigns each cell in list to dead or alive. """
        for i in range(self.lines):
            for j in range(self.cols):
                if random.random() < prob_alive:
                    self.cells[i][j] = self.state['alive']

    def get_neighbors(self, line, col):
        """ Returns number of neighbors for a given cell at line, col. """
        neighbors = 0
        for line_mod in [-1, 0, 1]:
            for col_mod in [-1, 0, 1]:
                if line_mod == 0 and col_mod == 0:
                    continue # Do not count given cell
                # % connects left/right and up/down
                i = (line + line_mod) % self.lines
                j = (col + col_mod) % self.cols
                if self.cells[i][j] == self.state['alive']:
                    neighbors += 1
        return neighbors

    def advance_generation(self):
        """ Advances cell list to next generation based on Conway's rules. """
        self.generation += 1
        next_cells = [[self.state['dead']] * self.cols for x in range(self.lines)]
        for i in range(self.lines):
            for j in range(self.cols):
                neighbors = self.get_neighbors(i, j)
                if self.cells[i][j] == self.state['alive']:
                    if neighbors == 2 or neighbors == 3:
                        next_cells[i][j] = self.state['alive']
                elif self.cells[i][j] == self.state['dead']:
                    if neighbors == 3:
                        next_cells[i][j] = self.state['alive']
        self.cells = next_cells

    def get_population(self):
        """ Returns number of alive cells. """
        population = 0
        for i in self.cells:
            population += i.count(self.state['alive'])
        return population
