#!/usr/bin/env python3

""" CONWAYS GAME OF LIFE TERMINAL USER INTERFACE """

import curses
from curses import wrapper
import time
import random

def main(stdscr):

    # Hide cursor
    curses.curs_set(False)

    # Don't wait for keypresses
    stdscr.nodelay(True)

    # Useful constants
    LINES = curses.LINES - 1
    COLS = curses.COLS
    MID_LINE = round(LINES / 2)
    MID_COL = round(COLS / 2)

    # Character to represent alive cell
    LIVE_CHAR = '#'

    # Initialize vars
    generation_count = 0
    debug_mode = False
    manual_mode = False
    loop_time = 0.1
    color_pair = 4

    # Initialize color pairs
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_CYAN)

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
                    # Mod keeps index from getting out of bounds
                    # Also connects left/right and up/down (I think)
                    current_line = (line + line_mod) % LINES
                    current_col = (col + col_mod) % COLS
                    cell_value = current_cells[current_line][current_col]
                    if cell_value == 1:
                        neighbors += 1
        return neighbors

    # Main loop
    while True:

        # Create list for next cells (initialized to all dead)
        next_cells = [[0] * COLS for x in range(LINES)]

        # Initialize population count
        population_count = 0

        # Iterate through current list
        for i in range(LINES):
            for j in range(COLS):

                # Get neighbor count for each cell
                neighbors = count_neighbors(i, j)

                # Cell is currently alive
                if current_cells[i][j] == 1:

                    # Increment population size
                    population_count += 1

                    # If in debug mode, show neighbor count (bold)
                    # Otherwise, show LIVE_CHAR
                    if debug_mode:
                        stdscr.addstr(i, j, str(neighbors), curses.A_BOLD)
                    else:
                        stdscr.addstr(i, j, LIVE_CHAR, curses.color_pair(color_pair) 
                                | curses.A_BOLD)

                    # If neighbor count is less than 2 or greater than 3,
                    # kill it in next generation
                    if not(neighbors == 2 or neighbors == 3):
                        next_cells[i][j] = 0
                    else:
                        next_cells[i][j] = 1

                # Cell is currently dead
                else:

                    # If in debug mode, show neighbor count (dim)
                    # Otherwise, replace with space (delete)
                    if debug_mode:
                        stdscr.addstr(i, j, str(neighbors), curses.A_DIM)
                    else:
                        stdscr.addstr(i, j, ' ', curses.color_pair(color_pair))

                    # If cell has 3 neighbors, bring it to
                    # life in next generation
                    if neighbors == 3:
                        next_cells[i][j] = 1

        # Increment generation count
        generation_count += 1

        # Display metrics and refresh screen
        stdscr.addstr(LINES, 0, "Generation: " + str(generation_count)
                + " Population: " + str(population_count), curses.A_BOLD)
        stdscr.refresh()

        # Save next cells as current for next loop
        current_cells = next_cells

        # Poll for keypress while loop runs
        # d: toggle debug mode
        # m: toggle manual mode
        # k: speed up loop
        # j: slow down loop
        # c: cycle through colors
        try:
            key = stdscr.getkey()
            if key == 'd':
                debug_mode = not debug_mode
            if key == 'm':
                manual_mode = not manual_mode
            if key == 'k':
                loop_time -= 0.03
            if key == 'j':
                loop_time += 0.03
            if key == 'c':
                color_pair = (color_pair + 1) % 7
        except:
            if loop_time >= 0.01:
                time.sleep(loop_time)
            else:
                loop_time = 0.01

        # If in manual mode, make keypress blocking
        # Causes generation to not advance until key pressed
        if manual_mode:
            stdscr.nodelay(False)
        else:
            stdscr.nodelay(True)

wrapper(main)
