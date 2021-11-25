from utils import fetch_sudokus
from solver import solve


"""
default sudokus' grid
"""

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

if __name__ == "__main__":
    sudoku_grid_as_string = ''.join([line[0] for line in sudoku])
    # print(sudoku_grid_as_string)
    # exit()

    # fetch sudokus from user input
    sudoku_queue = fetch_sudokus(sudoku_grid_as_string)

    # for each sudoku, solve it !
    for index, sudoku_grid in enumerate(sudoku_queue):
        solve(sudoku_grid, index + 1, len(sudoku_queue))
