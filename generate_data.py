import sudoku_generator, numpy as np

gradient = np.ones((9,9))
for i in range(9):
    gradient[i] *= i
gradient /= np.sum(gradient)

print gradient

"""
probabilities = np.ones(81)
probabilities[0:70:5] = 3
print probabilities
probabilities = probabilities/sum(probabilities)
print probabilities
board = construct_puzzle(construct_puzzle_solution(), is_uniform=True, probabilities=probabilities)


pprint(board)
"""
