""" CONWAYS GAME OF LIFE """

import random

state = {'alive' : True, 'dead' : False}

def init_board(_lines, _cols):
    """ Creates cell list of given dimensions and initializes them to all dead. """
    global lines, cols, cells, generation
    lines = _lines
    cols = _cols
    cells = [[state['dead']] * cols for x in range(lines)]
    generation = 0

def generate_random(prob_alive=0.3):
    """ Randomly assigns each cell in list to dead or alive. """
    global lines, cols, cells, generation
    generation = 0
    for i in range(lines):
        for j in range(cols):
            if random.random() < prob_alive:
                cells[i][j] = state['alive']

def get_neighbors(line, col):
    """ Returns number of neighbors for a given cell at line, col. """
    global lines, cols, cells
    neighbors = 0
    for line_shift in [-1, 0, 1]:
        for col_shift in [-1, 0, 1]:
            if line_shift == 0 and col_shift == 0:
                continue # Do not count given cell
            # % connects left/right and up/down
            i = (line + line_shift) % lines
            j = (col + col_shift) % cols
            if cells[i][j] == state['alive']:
                neighbors += 1
    return neighbors

def advance_generation():
    """ Advances cell list to next generation based on Conway's rules. """
    global lines, cols, cells, generation
    generation += 1
    next_cells = [[state['dead']] * cols for x in range(lines)]
    for i in range(lines):
        for j in range(cols):
            neighbors = get_neighbors(i, j)
            if cells[i][j] == state['alive']:
                if neighbors == 2 or neighbors == 3:
                    next_cells[i][j] = state['alive']
            elif cells[i][j] == state['dead']:
                if neighbors == 3:
                    next_cells[i][j] = state['alive']
    cells = next_cells

def get_population():
    """ Returns number of alive cells. """
    global cells
    population = 0
    for i in cells:
        population += i.count(state['alive'])
    return population
