#!/usr/bin/python3

""" CURSES INTERFACE FOR PLAYING GAME OF LIFE """

import gameoflife
import curses
import time


def main(stdscr):

    # Curses initialization
    stdscr.nodelay(True)
    curses.curs_set(False)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_CYAN)

    # Game initialization
    INIT_LINES = curses.LINES - 1
    INIT_COLS = curses.COLS
    cells = gameoflife.CellList(INIT_LINES, INIT_COLS)
    last_lines, last_cols = INIT_LINES, INIT_COLS
    cells.generate_random()
    manual_mode = False
    debug_mode = False
    loop_time = 0.1
    color = 4

    # Game loop
    while True:

        # Handle changing screen size
        lines, cols = stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1]
        if lines != last_lines or cols != last_cols:
            cells = gameoflife.CellList(lines, cols)
            stdscr.clear()
            cells.generate_random()

        # Display cells
        for i in range(lines):
            for j in range(cols):
                if not debug_mode:
                    if cells[i][j] == cells.cell_state['alive']:
                        stdscr.addstr(i, j, '#', curses.A_BOLD | curses.color_pair(color))
                    elif cells[i][j] == cells.cell_state['dead']:
                        stdscr.addstr(i, j, ' ', curses.A_BOLD | curses.color_pair(color))
                else:
                    neighbors = str(cells.get_neighbors(i, j))
                    if cells[i][j] == cells.cell_state['alive']:
                        stdscr.addstr(i, j, neighbors, curses.A_BOLD)
                    elif cells[i][j] == cells.cell_state['dead']:
                        stdscr.addstr(i, j, neighbors, curses.A_DIM)

        # Display metrics
        generation = str(cells.generation)
        population = str(cells.get_population())
        stdscr.addstr(lines, 0, 'Generation: ' + generation
                + ' Population: ' + population + ' ', curses.A_BOLD)
        stdscr.refresh()

        # Advance generation
        cells.advance_generation()

        # Handle keypresses
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
                color = (color + 1) % 7
            if key == 'r':
                cells.generate_random()
            if key == 'q':
                break
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

        # Save dimensions for next loop
        last_lines, last_cols = lines, cols


if __name__ == '__main__':
    curses.wrapper(main)
