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

<<<<<<< de1f23c7a1381e5998adff1759d9c81eff2a8cf8
"""
Randomly pluck out cells (numbers) from the solved puzzle grid, ensuring that any
plucked number can still be deduced from the remaining cells.

For deduction to be possible, each other cell in the plucked number's row, column,
or square must not be able to contain that number. """
def pluck(puzzle, n=0):

    """
    Answers the question: can the cell (i,j) in the puzzle "puz" contain the number
    in cell "c"? """


    def canBeA(puz, i, j, c):
        v = puz[c/9][c%9]
        if puz[i][j] == v: return True
        if puz[i][j] in range(1,10): return False

        for m in range(9): # test row, col, square
            # if not the cell itself, and the mth cell of the group contains the value v, then "no"
            if not (m==c/9 and j==c%9) and puz[m][j] == v: return False
            if not (i==c/9 and m==c%9) and puz[i][m] == v: return False
            if not ((i/3)*3 + m/3==c/9 and (j/3)*3 + m%3==c%9) and puz[(i/3)*3 + m/3][(j/3)*3 + m%3] == v:
                return False

        return True

    """
    starts with a set of all 81 cells, and tries to remove one (randomly) at a time
    but not before checking that the cell can still be deduced from the remaining cells. """
    cells     = set(range(81))
    cellsleft = cells.copy()
    while len(cells) > n and len(cellsleft):
        cell = random.choice(list(cellsleft)) # choose a cell from ones we haven't tried
        cellsleft.discard(cell) # record that we are trying this cell


            # this is a pluckable cell!
    	puzzle[cell/9][cell%9] = 0 # 0 denotes a blank cell
       	cells.discard(cell) # remove from the set of visible cells (pluck it)
            # we don't need to reset "cellsleft" because if a cell was not pluckable
            # earlier, then it will still not be pluckable now (with less information
            # on the board).

    # This is the puzzle we found, in all its glory.
    return (puzzle, len(cells))

#use this definition to create a puzzle with n variables inside
def generate_sudoku(n):
   	a_puzzle_solution = construct_puzzle_solution()
	result, number_of_cells = pluck(a_puzzle_solution, n)

	return result, number_of_cells

def construct_puzzle(puzzle_solution, is_uniform=False, probabilities=None, n_clues=40):

    # Check if distribution should be uniform
    while True:
        if is_uniform:
            clues = random.sample(xrange(81), n_clues)
        else:
            elements = np.arange(81)
            clues = np.random.choice(elements, n_clues, True, list(probabilities))


        # Make sudoku puzzles until we have a proper one
        # Create the board with the chosen clues
        puzzle = [[0]*9 for i in range(9)]
        for clue in clues:
            puzzle[clue / 9][clue % 9] = puzzle_solution[clue / 9][clue % 9]
        ret = solver.is_proper(puzzle)
        print ret
        # Check if it's proper and return the board if it is
        if ret:
            return puzzle
