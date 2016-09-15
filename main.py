from pprint import pprint

from sudoku_generator import generate_sudoku
from cnf_converter import convert2cnf
from sudoku_solver import solve_sudoku

if __name__ == '__main__':
	sudoku = generate_sudoku(True)
	# clauses = convert2cnf(sudoku)
	# solved, number_of_solutions = solve_sudoku(clauses)

	# pprint(sudoku)
	# pprint(solved)
	# print "Found {} solutions".format(number_of_solutions)
	# Solve
	# Analyze results