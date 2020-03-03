#!/usr/bin/python3
import sys
import random
import satlib as sl

if __name__ == "__main__":
    max_tries = 2000
    max_flips = 2000

    formula, num_vars = sl.getFormula(open(sys.argv[1], "r"))
    for i in range(1, max_tries):
        interpretation=sl.getRandomInterpretation(formula, num_vars)
        for j in range(1, max_flips):
            if sl.satisfies(interpretation, formula):
                print("SATISFIABLE")
                exit()
            else:
                interpretation = sl.flipped(interpretation)
    print("UNSATISFIABLE")
