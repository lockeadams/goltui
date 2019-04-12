#!/usr/bin/python3

""" CURSES INTERFACE FOR PLAYING GAME OF LIFE """

import gameoflife
import curses
import time

def main(stdscr):

    # Curses initialization
    curses.curs_set(True)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_CYAN)

    # Game initialization
    GAME_LINES = curses.LINES - 1
    GAME_COLS = curses.COLS
    game = gameoflife.GameOfLife(GAME_LINES, GAME_COLS)
    game.generate_random()

    # Game loop
    while True:

        # Display cells
        for i in range(GAME_LINES):
            for j in range(GAME_COLS):
                if game.cells[i][j] == game.state['alive']:
                    stdscr.addstr(i, j, '#', curses.A_BOLD | curses.color_pair(4))
                elif game.cells[i][j] == game.state['dead']:
                    stdscr.addstr(i, j, ' ', curses.A_BOLD | curses.color_pair(4))

        # Display metrics
        generation = str(game.generation)
        population = str(game.get_population())
        stdscr.addstr(GAME_LINES, 0, 'Generation: ' + generation
                + ' Population: ' + population + ' ', curses.A_BOLD)

        # Refresh screen
        stdscr.refresh()

        # Advance generation
        game.advance_generation()

        # Wait
        time.sleep(0.1)

if __name__ == '__main__':
    curses.wrapper(main)
