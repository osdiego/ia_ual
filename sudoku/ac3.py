from utils import is_different


def ac3(csp, queue=None):
    """
    Constraint Propagation with AC-3
    """

    if queue == None:
        queue = list(csp.binary_constraints)

    while queue:

        (xi, xj) = queue.pop(0)

        if revise(csp, xi, xj):

            # if a cell has 0 possibilities, sudoku has no solution
            if len(csp.possibilities[xi]) == 0:
                return False

            for Xk in csp.related_cells[xi]:
                if Xk != xi:
                    queue.append((Xk, xi))

    return True


def revise(csp, cell_i, cell_j):
    """
    remove_inconsistent_values

    returns true if a value is revised
    """

    revised = False

    # for each possible value remaining for the cell_i cell
    for value in csp.possibilities[cell_i]:

        # if cell_i=value is in conflict with cell_j=poss for each possibility
        if not any([is_different(value, poss) for poss in csp.possibilities[cell_j]]):

            # then remove cell_i=value
            csp.possibilities[cell_i].remove(value)
            revised = True

    # returns true if a value has been revised
    return revised
