from sudoku import Sudoku
from ac3 import ac3
from argparse import Namespace


def solve(grid: str, args: Namespace) -> None:
    print('AC3 starting..', end='\n\n')

    # Instanciate Sudoku
    sudoku = Sudoku(grid, args)

    # launch AC-3 algorithm of it
    ac3_result = ac3(sudoku)

    # Sudoku has no solution
    if not ac3_result:
        print('This sudoku has no solution.')

    # check if AC-3 algorithm has solve the Sudoku
    elif sudoku.is_solved():
        print("AC3 was enough to solve this sudoku!", end='\n\n')
        print(f'Result: \n{sudoku}')

    else:
        print('AC3 finished, could not solve it.')
