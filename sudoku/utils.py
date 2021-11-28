from defined_errors import InputError


def is_different(cell_i, cell_j):
    """
    is_different
    checks if two cells are the same
    """

    result = cell_i != cell_j
    return result


def validate_input_sudoku(input):
    """
    fetches Sudoku based on user's input
    """

    DEFAULT_SIZE = 81

    # if the input does not have the DEFAULT_SIZE
    if len(input) != DEFAULT_SIZE:
        raise InputError(
            f'The inserted Sudoku need to have {DEFAULT_SIZE} characters.')

    formatted_input = input.replace(
        "X", "0").replace("#", "0").replace("@", "0")

    if not formatted_input.isdigit():

        raise ValueError(
            "Only the following characters are allowed: [1,9], 'X', '#' and '@'.")

    else:
        return [formatted_input[0:DEFAULT_SIZE]]
