import itertools
from argparse import Namespace


class Sudoku:
    cols = "123456789"
    rows = "ABCDEFGHI"

    def __init__(self, grid: str, args: Namespace):
        # Generate all the coordinates of the grid
        self.args = args
        self.cells = self.generate_coords()

        # Generate all the possibilities for each one of these coords
        self.possibilities = self.generate_possibilities(grid)

        # Generate all the line / row / square constraints
        rule_constraints = self.generate_rules_constraints()

        # Convertion of these constraints to binary constraints
        self.binary_constraints = self.generate_binary_constraints(
            rule_constraints)

        # Generate all constraint-related cells for each of them
        self.related_cells = self.generate_related_cells()

    def generate_coords(self) -> list[str]:
        all_coords = [row + col for col in self.cols for row in self.rows]

        if self.args.debug:
            print(all_coords)

        return all_coords

    def generate_possibilities(self, grid: str) -> dict:
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

    def generate_rules_constraints(self) -> list[list[str]]:
        """
        generates the constraints based on the rules of the game:
        value different from any in row, column or square
        """

        # get rows constraints
        row_constraints = [[row + col for col in self.cols]
                           for row in self.rows]

        # get columns constraints
        column_constraints = [[row + col for row in self.rows]
                              for col in self.cols]

        # get square constraints
        square_constraints = []
        rows_square_coords = [self.rows[i:i+3]
                              for i in range(0, len(self.rows), 3)]

        cols_square_coords = [self.cols[i:i+3]
                              for i in range(0, len(self.cols), 3)]

        # for each square
        for square_rows in rows_square_coords:
            for square_cols in cols_square_coords:

                # and for each value in this square
                current_square_constraints = [
                    row + col for col in square_cols for row in square_rows]

                square_constraints.append(current_square_constraints)

        all_constraints = row_constraints + column_constraints + square_constraints

        if self.args.debug:
            print('\nrow_constraints:')
            print(row_constraints)

            print('\column_constraints:')
            print(column_constraints)

            print('\square_constraints:')
            print(square_constraints)

            print('\nall_constraints:')
            print(all_constraints)

        # all constraints is the sum of these 3 rules
        return all_constraints

    def generate_binary_constraints(self, rule_constraints: list[list[str]]) -> list[list[str]]:
        """
        Generates the binary constraints based on the rule constraints
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

        if self.args.debug:
            print(
                f'\n {len(generated_binary_constraints)} generated_binary_constraints:')
            print(generated_binary_constraints)

        return generated_binary_constraints

    def generate_related_cells(self) -> dict:
        """
        Generates the the constraint-related cell for each one of them
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

    def is_solved(self) -> bool:
        """
        checks if the Sudoku's solution is finished
        we loop through the possibilities for each cell
        if all of them has only one, then the Sudoku is solved
        """

        return not any([len(p) > 1 for p in self.possibilities.values()])

    def __str__(self) -> str:
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
