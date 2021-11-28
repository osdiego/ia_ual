import itertools


cols = "123456789"
rows = "ABCDEFGHI"


class Sudoku:
    def __init__(self, grid):
        # generation of all the coords of the grid
        self.cells = [row + col for col in cols for row in rows]
        print(self.cells)

        # generation of all the possibilities for each one of these coords
        self.possibilities = self.generate_possibilities(grid)

        # generation of the line / row / square constraints
        rule_constraints = self.generate_rules_constraints()

        # convertion of these constraints to binary constraints
        self.binary_constraints = self.generate_binary_constraints(
            rule_constraints)

        # generating all constraint-related cells for each of them
        self.related_cells = self.generate_related_cells()

        # prune
        self.pruned = dict()
        self.pruned = {v: list() if grid[i] == '0' else [
            int(grid[i])] for i, v in enumerate(self.cells)}

    def generate_possibilities(self, grid):
        """
        generates all possible value remaining for each cell
        """

        grid_as_list = list(grid)

        possibilities = dict()

        for index, coords in enumerate(self.cells):
            # if value is 0, then the cell can have any value in [1, 9]
            if grid_as_list[index] == "0":
                possibilities[coords] = list(range(1, 10))
            # else value is already defined, possibilities is this value
            else:
                possibilities[coords] = [int(grid_as_list[index])]

        return possibilities

    def generate_rules_constraints(self):
        """
        generates the constraints based on the rules of the game:
        value different from any in row, column or square
        """

        # get rows constraints
        row_constraints = [[row + col for col in cols] for row in rows]

        # get columns constraints
        column_constraints = [[row + col for row in rows] for col in cols]

        # get square constraints
        square_constraints = []
        rows_square_coords = [rows[i:i+3] for i in range(0, len(rows), 3)]
        print(rows_square_coords)

        cols_square_coords = [cols[i:i+3] for i in range(0, len(cols), 3)]
        print(cols_square_coords)

        # for each square
        for square_rows in rows_square_coords:
            for square_cols in cols_square_coords:

                current_square_constraints = []

                # and for each value in this square
                for x in square_rows:
                    for y in square_cols:
                        current_square_constraints.append(x + y)

                square_constraints.append(current_square_constraints)

        # all constraints is the sum of these 3 rules
        print()
        print(row_constraints)
        print()
        print(column_constraints)
        print()
        print(square_constraints)
        print()
        print(row_constraints + column_constraints + square_constraints)
        print()

        return row_constraints + column_constraints + square_constraints

    def generate_binary_constraints(self, rule_constraints):
        """
        generates the binary constraints based on the rule constraints
        """

        generated_binary_constraints = list()

        # for each set of constraints
        for constraint_set in rule_constraints:

            binary_constraints = list()

            # 2 because we want binary constraints

            # for tuple_of_constraint in itertools.combinations(constraint_set, 2):
            for tuple_of_constraint in itertools.permutations(constraint_set, 2):
                binary_constraints.append(list(tuple_of_constraint))

            # for each of these binary constraints
            for constraint in binary_constraints:

                # check if we already have this constraint saved
                if constraint not in generated_binary_constraints:
                    generated_binary_constraints.append(
                        [constraint[0], constraint[1]])

        print(generated_binary_constraints)
        print(len(generated_binary_constraints))
        return generated_binary_constraints

    def generate_related_cells(self):
        """
        generates the the constraint-related cell for each one of them
        """

        related_cells = dict()

        # for each one of the 81 cells
        for cell in self.cells:

            related_cells[cell] = list()

            # related cells are the ones that current cell has constraints with
            for constraint in self.binary_constraints:
                if cell == constraint[0]:
                    related_cells[cell].append(constraint[1])

        return related_cells

    def is_solved(self):
        """
        checks if the Sudoku's solution is finished
        we loop through the possibilities for each cell
        if all of them has only one, then the Sudoku is solved
        """

        return not any([len(p) > 1 for p in self.possibilities.values()])

    def __str__(self):
        """
        returns a human-readable string
        """

        output = ""
        count = 1

        # for each cell, print its value
        for cell in self.cells:

            # trick to get the right print in case of an AC3-finished sudoku
            value = str(self.possibilities[cell])
            if type(self.possibilities[cell]) == list:
                value = str(self.possibilities[cell][0])

            output += "[" + value + "]"

            # if we reach the end of the line,
            # make a new line on display
            if count >= 9:
                count = 0
                output += "\n"

            count += 1

        return output
