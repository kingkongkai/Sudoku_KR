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

probabilities = [gradient / np.sum(gradient),
                block_diagonal_gradient / np.sum(block_diagonal_gradient),
                block_diagonal_hill / np.sum(block_diagonal_hill)]

for k in range(100):
    flag = False
    puzzle_solution = generator.construct_puzzle_solution()
    sudokus = [generator.generate_sudoku(puzzle_solution, is_uniform=True, n_clues=40)]
    for j in range(3):
        sudokus.append(generator.generate_sudoku(puzzle_solution, probabilities=probabilities[j], n_clues=40))
        if len(sudokus[-1]) == 0:
            flag = True
            break
    if flag:
        print "No proper sudoku found, generating new solution...\n"
        continue

    with open('sudoku_puzzles.txt', 'a') as f:
        f.write('\n')
        sudokus[0].tofile(f, sep=",", format="%s")
        f.write('\n\n')
        sudokus[1].tofile(f, sep=",", format="%s")
        f.write('\n\n')
        sudokus[2].tofile(f, sep=",", format="%s")
        f.write('\n\n')
        sudokus[3].tofile(f, sep=",", format="%s")
        f.write('\n')
