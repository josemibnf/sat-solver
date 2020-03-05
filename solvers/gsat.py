#!/usr/bin/python3
import sys
import random

def satisfies(interpretation, formula):
    def isTrue(var):
        if ( interpretation[abs(var)-1]>0 and var<0 ) or ( interpretation[abs(var)-1]<0 and var>0 ) :
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

def getRandomInterpretation():
    global num_vars 
    interpretation=[]
    for var in range (1, num_vars+1):
        new_var=0
        while new_var == 0:
            new_var=random.randrange(-1,2)*var
        interpretation.append(new_var)
    return interpretation

def flipped(interpretation):
    global num_vars
    flip_var = random.randrange(0, num_vars)
    interpretation[flip_var]*=-1
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
    max_tries = 2000
    max_flips = 2000
    global num_vars

    formula = getFormula(open(sys.argv[1], "r"))
    for i in range(1, max_tries):
        interpretation=getRandomInterpretation()
        for j in range(1, max_flips):
            if satisfies(interpretation, formula):
                print("c gsat")
                print("s SATISFIABLE")
                print("v "+" ".join(map(str, interpretation)))
                exit()
            else:
                interpretation = flipped(interpretation)
    print("c fsat")
    print("s UNSATISFIABLE")
