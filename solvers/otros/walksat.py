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

def flipped(interpretation, vars_clause):
    flip_var = random.randrange(0,vars_clause)
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

def broken(interpretation, formula):
    print("interpretation and formula: ",interpretation, formula)
    breakcost = 0
    breakcost_actual = 0
    return_variable = None

    # Get a random variable
    variable = interpretation[random.randrange(0, len(interpretation)+1)]
    switch_variable = -1 * variable

    for clause in formula:
        if switch_variable in clause:
            breakcost_actual += 1

    return -1 * return_variable

if __name__ == "__main__":
    max_tries = 20000
    max_flips = 20000

    global num_vars
	
    formula = getFormula(open(sys.argv[1], "r"))
    for i in range(1, max_tries+1):
        print("\nTrie: ",i)
        interpretation=getRandomInterpretation()
        for j in range(1, max_flips+1):
            print("\nFlip: ",j)
            if satisfies(interpretation, formula):
                print("c walksat")
                print("s SATISFIABLE")
                print("v "+" ".join(map(str, interpretation)))
                exit()
            else:
                switch_variable = broken(interpretation, formula)
                print("Variable to change = ",switch_variable)

                index = interpretation.index(switch_variable)
                interpretation[index] = switch_variable * -1
               

    print("c walksat")
    print("s UNSATISFIABLE")