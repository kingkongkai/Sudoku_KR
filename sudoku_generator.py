"""
SUDOKU (NUMBER PLACE) PUZZLE GENERATOR
by Arel Cordero November 12, 2005

This program is released into the public domain.
Revision 3
"""

import random, copy, numpy as np
import sudoku_solver as solver
from pprint import pprint

"""
Randomly arrange numbers in a grid while making all rows, columns and
squares (sub-grids) contain the numbers 1 through 9.
"""

def construct_puzzle_solution():
    # Loop until we're able to fill all 81 cells with numbers, while
    # satisfying the constraints above.
    while True:
        try:
            puzzle  = [[0]*9 for i in range(9)] # start with blank puzzle
            rows    = [set(range(1,10)) for i in range(9)] # set of available
            columns = [set(range(1,10)) for i in range(9)] #   numbers for each
            squares = [set(range(1,10)) for i in range(9)] #   row, column and square
            for i in range(9):
                for j in range(9):
                    # pick a number for cell (i,j) from the set of remaining available numbers
                    choices = rows[i].intersection(columns[j]).intersection(squares[(i/3)*3 + j/3])
                    choice  = random.choice(list(choices))

                    puzzle[i][j] = choice

                    rows[i].discard(choice)
                    columns[j].discard(choice)
                    squares[(i/3)*3 + j/3].discard(choice)

            # success! every cell is filled.
            return puzzle

        except IndexError:
            # if there is an IndexError, we have worked ourselves in a corner (we just start over)
            pass

def generate_sudoku(puzzle_solution, is_uniform=False, probabilities=None, n_clues=40):

    # Check if distribution should be uniform
    while True:
        if is_uniform:
            clues = random.sample(xrange(81), n_clues)
        else:
            elements = np.arange(81)
            clues = np.random.choice(elements, size=n_clues, replace=True, p=probabilities.flatten())


        # Make sudoku puzzles until we have a proper one
        # Create the board with the chosen clues
        puzzle = [[0]*9 for i in range(9)]
        for clue in clues:
            puzzle[clue / 9][clue % 9] = puzzle_solution[clue / 9][clue % 9]
        ret = solver.is_proper(puzzle)
        print ret
        # Check if it's proper and return the board if it is
        if ret:
            return np.array(puzzle)
