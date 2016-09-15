import pycosat
import pprint

def v(i, j, d):
	"""
	Return the number of the variable of cell i, j and digit d,
	which is an integer in the range of 1 to 729 (including).
	"""
	return 81 * (i - 1) + 9 * (j - 1) + d

def solve_sudoku(clauses):
	grid = [[0]*9 for i in range(9)]

	solutions = pycosat.itersolve(clauses)
	n_solutions = 0

	def read_cell(i, j):
		# return the digit of cell i, j according to the solution
		for d in range(1, 10):
			if v(i, j, d) in sol:
				return d

	for sol in solutions:
		n_solutions += 1
		sol = set(sol)

		if n_solutions is 1:
			for i in range(1, 10):
				for j in range(1, 10):
					grid[i - 1][j - 1] = read_cell(i, j)

	return grid, n_solutions