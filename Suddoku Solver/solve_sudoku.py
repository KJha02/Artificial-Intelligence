from display import display_sudoku_solution
import random, sys
from SAT import SAT
from time import time

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    # random.seed(1)

    puzzle_name = input("What puzzle would you like to solve: \n")
    sol_filename = puzzle_name + ".sol"

    sat = SAT(puzzle_name + ".cnf")
    start = time()
    result = None
    
    result = sat.walk_sat()
    #result = sat.gsat() # uncomment for testing

    if result:
        sat.write_solution(sol_filename, result)
        print("Solved after visiting {} states".format(sat.statesVisited))
        print("Solved in: {} seconds\n".format(time() - start))
        display_sudoku_solution(sol_filename)

    # Handles failure case display
    else:
        print("No solution found after visiting {} states".format(sat.statesVisited))
        print("Run time: {} seconds".format(time() - start))
        print("Clauses left unsolved: {}".format(sat.unsolvedClauses))