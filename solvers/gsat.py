#!/usr/bin/python3
import sys
import random

def satisfies(interpretation, formula):

    def isTrue(var):
        if ( interpretation[abs(var)-1]==0 and var<0 ) or ( interpretation[abs(var)-1]==1 and var>0 ) :
            return False
        else:
            return True

    for clausula in formula:
        clausula_bool=False
        for var in clausula:
            if isTrue(var):
                clausula_bool=True
                break
        if clausula_bool is False:
            return False
    return True

def getRandomInterpretation(formula):
    global num_vars
    interpretation=[]
    for var in range (0, num_vars):
        interpretation.append(random.randrange(0,2))
    print("Su nueva interpretacion es: ", interpretation)
    return interpretation

def flipped(interpretation):
    flip_var = random.randrange(0,len(formula[0])-1)
    if interpretation[flip_var]==0:
        interpretation[flip_var]=1
    else:
        interpretation[flip_var]=0
    print("Ahora es: ", interpretation)
    return interpretation

def getFormula(cnf):
    global num_vars
    formula=[]
    for line in cnf:
        if line.split()[0] is not "c":
            if line.split()[0] is "p":
                num_vars = int(line.split()[2])
            else:
                clause=[]
                for var in line.split():
                    if int(var) != 0:
                        clause.append(int(var))
                formula.append(clause)
    return formula
    

if __name__ == "__main__":
    global num_vars
    max_tries = 20
    max_flips = 20

    formula = getFormula(open(sys.argv[1], "r"))
    print(num_vars)
    print(formula)
    for i in 1, max_tries:
        interpretation=getRandomInterpretation(formula)
        for j in 1, max_flips:
            if satisfies(interpretation, formula):
                print("Satisfactible")
                exit()
            else:
                interpretation = flipped(interpretation)
    print("Insatisfactible")
