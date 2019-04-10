#!/usr/bin/env python3

""" CONWAYS GAME OF LIFE TERMINAL USER INTERFACE """

import curses
from curses import wrapper
import time
import random

def main(stdscr):

    # Hide cursor
    curses.curs_set(False)

    # Useful constants
    LINES = curses.LINES - 1
    COLS = curses.COLS
    MID_LINE = round(LINES / 2)
    MID_COL = round(COLS / 2)

    # Character to represent alive cell
    LIVE_CHAR = '█'

    # Initialize generation counter
    generation_count = 0

    # Create list to represent cells and randomly create initial state
    # Format is [line][column]. 0 is dead, 1 is alive
    current_cells = [[0] * COLS for x in range(LINES)]
    for i in range(LINES):
        for j in range(COLS):
            if random.random() > 0.9:
                current_cells[i][j] = 1

    # Determine number of neighbors for a cell at line, col
    def count_neighbors(line, col):
        neighbors = 0
        for line_mod in [-1, 0, 1]:
            for col_mod in [-1, 0, 1]:
                if line_mod == 0 and col_mod == 0:
                    pass # Do not count given cell
                else:
                    try:
                        cell_value = current_cells[line + line_mod][col + col_mod]
                    except:
                        cell_value = 0
                    if cell_value == 1:
                        neighbors += 1
        return neighbors

    # Main loop
    while True:

        # Create list for next cells (initialized to all dead)
        next_cells = [[0] * COLS for x in range(LINES)]

        # Iterate through current list. If element is 1, paint character at position.
        # Also perform game logic: alive cell with 2 or 3 neighbors lives, dead cell
        # with 3 neighbors comes to life. Next generation copied to next_cells so as
        # to not mutate current_cells during operation.
        for i in range(LINES):
            for j in range(COLS):
                neighbors = count_neighbors(i, j)
                if current_cells[i][j] == 1:
                    stdscr.addstr(i, j, LIVE_CHAR, curses.A_BOLD)
                    if not(neighbors == 2 or neighbors == 3):
                        next_cells[i][j] = 0
                    else:
                        next_cells[i][j] = 1
                else:
                    stdscr.delch(i, j)
                    if neighbors == 3:
                        next_cells[i][j] = 1

        # Increment generation counter, display it, and refresh screen
        generation_count += 1
        stdscr.addstr(LINES, 0, "Generation: " + str(generation_count))
        stdscr.refresh()

        # Save next cells as current for next loop
        current_cells = next_cells

        # Wait
        time.sleep(0.1)

wrapper(main)
