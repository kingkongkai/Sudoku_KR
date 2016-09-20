import pycosat
from pprint import pprint
import timeit
import numpy as np
import subprocess
import re

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
    clauses = get_clauses(grid)

    filename = 'temp-cnf.txt'
    f = open(filename, 'w')

    for clause in clauses:
        np.array(clause).tofile(f, sep=" ", format="%s")
        f.write(" 0\n")

    f.close()

    p = subprocess.Popen(['minisat', filename, '-verb=2'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.communicate()[0]

    n_restarts = int(re.search("restarts.*: ([0-9])*", output).group(1))
    n_conflicts = int(re.search("conflicts.*: ([0-9])*", output).group(1))
    n_decisions = int(re.search("decisions.*: ([0-9])*", output).group(1))
    n_propagations = int(re.search("propagations.*: ([0-9])*", output).group(1))
    n_conflict_literals = int(re.search("conflict literals.*: ([0-9])*", output).group(1))
    cpu_time = float(re.search("CPU time.*: ([0-9]*\.*[0-9]*)", output).group(1))

    return [n_restarts, n_conflicts, n_decisions,
            n_propagations, n_conflict_literals, cpu_time]

    # start = timeit.timeit()
    # solution = pycosat.solve(clauses, verbose=0)
    # end = timeit.timeit()

    # return end-start

def get_clauses(grid):
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

    return clauses

if __name__ == '__main__':
    f = open('sudoku_puzzles.txt', 'r')

    measured_hardness = []
    n_different_distributions = 7
    n_read_sudokus = 0

    while True:
        read_lines = [f.readline() for i in range(n_different_distributions)]

        if not read_lines[-1]:
            if read_lines[0]:
                print "Line count isn't a multiple of {}.".format(n_different_distributions)
            break

        read_sudokus = [np.fromstring(line, int, 81, ',').reshape((9,9)) for line in read_lines]
        hardness = [measure_hardness(sudoku) for sudoku in read_sudokus]
        # print hardness
        measured_hardness.append(hardness)
        # print measured_hardness


        clauses = get_clauses(read_sudokus[3])

        n_read_sudokus += 1
        if n_read_sudokus > 2:
            break
        if n_read_sudokus % 10 == 0:
            print "Read sudokus: {}".format(n_read_sudokus * n_different_distributions)

    measured_hardness = np.array(measured_hardness)

    # Get mean of column
    mean = np.mean(measured_hardness, 0)
    print mean