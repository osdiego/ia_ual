from sudoku import Sudoku
from ac3 import AC3


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
    elif sudoku.is_solved():
        print("AC3 was enough to solve this sudoku !".format(index, total))
        print("Result: \n{}".format(sudoku))

    else:
        print("AC3 finished, could not solve it.".format(index, total))
