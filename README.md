# GOLTUI

## gameoflife.py
Module containing the operations necessary to play Conway's Game of Life. Contains CellList class that represents cells as alive (True) or dead (False), and has functions to create, evlove, and gain info about the cell population.

## lifetui.py
Script using the gameoflife module to print the game to a terminal screen using the curses library. Initial generation is random.

Controls:

| Keypress | Description |
| :------: | ----------- |
| d        | Toggles debug mode. Prints cells as their neighbor count, with live cells bold and dead dim. |
| m        | Toggles manual mode. Advances generation after pressing any key instead of automatically. |
| k        | Speeds up loop. |
| j        | Slows down loop. |
| c        | Cycles background color. |
| r        | Restarts game by randomizing generation. |
| q        | Exit game cleanly. |

## installation
To use the script, clone this repo in a directory of your choice and execute `./lifetui.py`. Windows users will additionally need to install `windows-curses`: `python -m pip install windows-curses`
