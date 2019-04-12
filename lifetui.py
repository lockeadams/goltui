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
    GAME_LINES = curses.LINES - 1
    GAME_COLS = curses.COLS
    gameoflife.init_board(GAME_LINES, GAME_COLS)
    gameoflife.generate_random()
    manual_mode = False
    debug_mode = False
    loop_time = 0.1
    color = 4

    # Game loop
    while True:

        # Display cells
        for i in range(GAME_LINES):
            for j in range(GAME_COLS):
                if not debug_mode:
                    if gameoflife.cells[i][j] == gameoflife.state['alive']:
                        stdscr.addstr(i, j, '#', curses.A_BOLD | curses.color_pair(color))
                    elif gameoflife.cells[i][j] == gameoflife.state['dead']:
                        stdscr.addstr(i, j, ' ', curses.A_BOLD | curses.color_pair(color))
                else:
                    neighbors = str(gameoflife.get_neighbors(i, j))
                    if gameoflife.cells[i][j] == gameoflife.state['alive']:
                        stdscr.addstr(i, j, neighbors, curses.A_BOLD)
                    elif gameoflife.cells[i][j] == gameoflife.state['dead']:
                        stdscr.addstr(i, j, neighbors, curses.A_DIM)

        # Display metrics
        generation = str(gameoflife.generation)
        population = str(gameoflife.get_population())
        stdscr.addstr(GAME_LINES, 0, 'Generation: ' + generation
                + ' Population: ' + population + ' ', curses.A_BOLD)
        stdscr.refresh()

        # Advance generation
        gameoflife.advance_generation()

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
                gameoflife.generate_random()
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


if __name__ == '__main__':
    curses.wrapper(main)
