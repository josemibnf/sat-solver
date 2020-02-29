#!/usr/bin/python3
import sys
def satisfies(interpretation, formula):
    pass

def getRandomInterpretation(formula):
    pass

def flipped(interpretation):
    pass

def getFormula(cnf):
    formula=[]
    for line in cnf:
        if line.split()[0] is not "c" and line.split()[0] is not "p":
            clause=[]
            for var in line.split():
                if int(var) != 0:
                    clause.append(int(var))
            formula.append(clause)
    return formula
    

if __name__ == "__main__":
    formula = getFormula(open(sys.argv[1], "r"))
    for i in 1, max_tries:
        interpretation=getRandomInterpretation(formula)
        for j in 1, max_flips:
            if satisfies(interpretation, formula):
                print(interpretation)
                break
            else:
                flipped(interpretation)
    print("No solution found")
