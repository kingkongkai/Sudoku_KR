import sudoku_generator as generator
from pprint import pprint
import numpy as np

gradient = np.ones((9,9))
for i in range(9):
    gradient[i] *= i

block_diagonal_gradient = np.ones((9,9))
for i in range(3, 9):
    for j in range(3, 9):
        if i > 5 or j > 5:
            block_diagonal_gradient[i][j] = 3
for i in range(3):
    for j in range(3):
        block_diagonal_gradient[i][6 + j] = 2
        block_diagonal_gradient[3 + i][3 + j] = 2
        block_diagonal_gradient[6 + i][j] = 2

block_diagonal_hill = np.ones((9,9))
for i in range(3):
    for j in range(3):
        block_diagonal_hill[i][6 + j] = 3
        block_diagonal_hill[3 + i][3 + j] = 3
        block_diagonal_hill[6 + i][j] = 3

gradient /= np.sum(gradient)
block_diagonal_gradient /= np.sum(block_diagonal_gradient)
block_diagonal_hill /= np.sum(block_diagonal_hill)

for k in range(100):
    puzzle_solution = generator.construct_puzzle_solution()
    sudoku_uniform = generator.generate_sudoku(puzzle_solution, is_uniform=True, n_clues=35)
    sudoku_gradient = generator.generate_sudoku(puzzle_solution, probabilities=gradient, n_clues=35)
    sudoku_block_diag_grad = generator.generate_sudoku(puzzle_solution, probabilities=block_diagonal_gradient, n_clues=35)
    sudoku_block_diag_hill = generator.generate_sudoku(puzzle_solution, probabilities=block_diagonal_hill, n_clues=35)

    with open('sudoku_puzzles.txt', 'w') as f:
        f.write('\n')
        sudoku_uniform.tofile(f, sep=",", format="%s")
        f.write('\n\n')
        sudoku_gradient.tofile(f, sep=",", format="%s")
        f.write('\n\n')
        sudoku_block_diag_grad.tofile(f, sep=",", format="%s")
        f.write('\n\n')
        sudoku_block_diag_hill.tofile(f, sep=",", format="%s")
        f.write('\n')
