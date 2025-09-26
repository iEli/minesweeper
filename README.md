# Eli's Console Minesweeper
Tired of Google's version of Minesweeper? Well, so am I. That's why I decided to make my own Minesweeper that can be played directly from the console, coz why not.

This version of Minesweeper is playable from the console terminal and is written in Python by an elite software engineer named Elias Nemiri. 

## Requirements:
- Python 3.8+ installed
- Download the minesweeper.py file

## How to run the game:
### Windows:
1. Open command prompt or PowerShell
2. Get to wherever you downloaded the file using `cd ~\Downloads\minesweeper`
3. Type `python3 minesweeper.py` or `py minesweeper.py`

### macOS:
1. Open Terminal
2. Get to wherever you downloaded the file using `cd ~/Downloads/minesweeper`
3. Type  `python3 minesweeper.py` or `python3 minesweeper.py <ROWS> <COLUMNS> <MINES>` to choose your own number of rows, columns, and mines
> Optionally, add three integer values at the end of the command to use your own number of rows, columns, and mines, using
> `python3 minesweeper.py <ROWS> <COLUMNS> <MINES>`
>

## How to play:
To reveal a cell, use `r <ROW> <COLUMN>`
>
> NOTE: The first reveal is always safe.
> 

To flag a cell, use `f <ROW> <COLUMN>`\
To quit, use `q`
