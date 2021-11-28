from utils import format_sudoku
from solver import solve
import argparse


# Inspired by https://github.com/stressGC/Python-AC3-Backtracking-CSP-Sudoku-Solver

# Default Sudoku's grid
sudoku = [
    ['003020600'],
    ['900305001'],
    ['001806400'],
    ['008102900'],
    ['700000008'],
    ['006708200'],
    ['002609500'],
    ['800203009'],
    ['005010300']
]

# Example of sudoku that the AC-3 algorithm cannot solve
# sudoku = [
#     ['005300000'],
#     ['800000020'],
#     ['070010500'],
#     ['400005300'],
#     ['010070006'],
#     ['003200080'],
#     ['060500009'],
#     ['004000030'],
#     ['000009700']
# ]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Program so solve Sudoku problems.')
    parser.add_argument('--debug', '-d', action='store_true')
    args = parser.parse_args()

    # fetch Sudoku from user input
    sudoku_string = format_sudoku(sudoku)

    # for each sudoku, solve it !
    for index, sudoku_grid in enumerate(sudoku_string):
        solve(sudoku_grid, args)
