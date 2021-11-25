from sudoku import Sudoku
from ac3 import AC3
from utils import fetch_sudokus, print_grid

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


def solve(grid, index, total):
    print("AC3 starting".format(index, total))

    # instanciate Sudoku
    sudoku = Sudoku(grid)

    # launch AC-3 algorithm of it
    AC3_result = AC3(sudoku)

    # Sudoku has no solution
    if not AC3_result:
        print("This sudoku has no solution".format(index, total))

    # check if AC-3 algorithm has solve the Sudoku
    elif sudoku.isFinished():
        print("AC3 was enough to solve this sudoku !".format(index, total))
        print("Result: \n{}".format(sudoku))

    # continue the resolution
    else:
        print("{}/{} : AC3 finished, could not solve it.".format(index, total))


if __name__ == "__main__":
    sudoku_grid_as_string = ''.join([line[0] for line in sudoku])
    # print(sudoku_grid_as_string)
    # exit()

    # fetch sudokus from user input
    sudoku_queue = fetch_sudokus(sudoku_grid_as_string)

    # for each sudoku, solve it !
    for index, sudoku_grid in enumerate(sudoku_queue):
        solve(sudoku_grid, index + 1, len(sudoku_queue))
