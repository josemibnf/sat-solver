#!/usr/bin/python3
import sys
def satisfies(interpretation, formula):
    pass

def getRandomInterpretation(formula):
    pass

def flipped(interpretation):
    pass

def getFormula(cnf):
    if cnf.readline is not "c Random CNF formula":
        print ("Error: NO ES UN CNF.")
        exit
    second_line = cnf.readline()
    num_clauses = second_line.split()[2] 
    print(num_clauses)
    num_var = second_line.split()[3]
    formula=[]
    for i in range(2, num_clauses):
        line=cnf.readline()
        clause=[]
        for var in line.split():
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
            else:
                flipped(interpretation)
    print("No solution found")
