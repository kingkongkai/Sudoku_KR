import sudoku_generator

probabilities = np.ones(81)
probabilities[0:70:5] = 3
print probabilities
probabilities = probabilities/sum(probabilities)
print probabilities
board = construct_puzzle(construct_puzzle_solution(), is_uniform=True, probabilities=probabilities)


pprint(board)
