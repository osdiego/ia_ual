from utils import validate_input_sudoku
from solver import solve


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

if __name__ == "__main__":
    sudoku_grid_as_string = ''.join([line[0] for line in sudoku])
    # print(sudoku_grid_as_string)
    # exit()

    # fetch Sudoku from user input
    sudoku_queue = validate_input_sudoku(sudoku_grid_as_string)

    # for each sudoku, solve it !
    for index, sudoku_grid in enumerate(sudoku_queue):
        solve(sudoku_grid, index + 1, len(sudoku_queue))
