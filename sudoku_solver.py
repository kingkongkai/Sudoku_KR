import pycosat
import pprint
import timeit

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

def sudoku_clauses():
    """
    Create the (11745) Sudoku clauses, and return them as a list.
    Note that these clauses are *independent* of the particular
    Sudoku puzzle at hand.
    """
    res = []
    # for all cells, ensure that the each cell:
    for i in range(1, 10):
        for j in range(1, 10):
            # denotes (at least) one of the 9 digits (1 clause)
            res.append([v(i, j, d) for d in range(1, 10)])
            # does not denote two different digits at once (36 clauses)
            for d in range(1, 10):
                for dp in range(d + 1, 10):
                    res.append([-v(i, j, d), -v(i, j, dp)])

    def valid(cells):
        # Append 324 clauses, corresponding to 9 cells, to the result.
        # The 9 cells are represented by a list tuples.  The new clauses
        # ensure that the cells contain distinct values.
        for i, xi in enumerate(cells):
            for j, xj in enumerate(cells):
                if i < j:
                    for d in range(1, 10):
                        res.append([-v(xi[0], xi[1], d), -v(xj[0], xj[1], d)])

    # ensure rows and columns have distinct values
    for i in range(1, 10):
        valid([(i, j) for j in range(1, 10)])
        valid([(j, i) for j in range(1, 10)])
    # ensure 3x3 sub-grids "regions" have distinct values
    for i in 1, 4, 7:
        for j in 1, 4 ,7:
            valid([(i + k % 3, j + k // 3) for k in range(9)])

    assert len(res) == 81 * (1 + 36) + 27 * 324
    return res

def is_proper(grid):
    """
    solve a Sudoku grid inplace
    """
    clauses = sudoku_clauses()
    for i in range(1, 10):
        for j in range(1, 10):
            d = grid[i - 1][j - 1]
            # For each digit already known, a clause (with one literal).
            # Note:
            #     We could also remove all variables for the known cells
            #     altogether (which would be more efficient).  However, for
            #     the sake of simplicity, we decided not to do that.
            if d:
                clauses.append([v(i, j, d)])

	def py_itersolve(clauses): # don't use this function!
	    while True:            # (it is only here to explain things)
	        sol = pycosat.solve(clauses)
	        if isinstance(sol, list):
	            yield sol
	            clauses.append([-x for x in sol])
	        else: # no more solutions -- stop iteration
	            return

    # solve the SAT problem
    generator = py_itersolve(clauses)
    t = 0
    for solution in generator:
        t += 1
        if t == 2:
            return False
    return True

def measure_hardness(grid):
    """
    solve a Sudoku grid inplace
    """
    clauses = sudoku_clauses()
    for i in range(1, 10):
        for j in range(1, 10):
            d = grid[i - 1][j - 1]
            # For each digit already known, a clause (with one literal).
            # Note:
            #     We could also remove all variables for the known cells
            #     altogether (which would be more efficient).  However, for
            #     the sake of simplicity, we decided not to do that.
            if d:
                clauses.append([v(i, j, d)])

	start = timeit.timeit()
    solution = pycosat.solve(clauses, verbose=1)
    end = timeit.timeit()

    print end-start