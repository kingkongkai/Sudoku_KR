from sudoku_generator import generate_sudoku
from cnf_converter import convert2cnf
from sudoku_solver import solve_sudoku

if __name__ == '__main__':
	sudoku, number_of_cells = generate_sudoku(25)
	clauses = convert2cnf(sudoku)
	solve_sudoku(clauses)
	# Solve
	# Analyze results