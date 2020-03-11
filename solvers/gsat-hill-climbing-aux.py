#!/usr/bin/python3
import sys
import random

def cost(interpretation, formula):
    def isTrue(var):
        if ( interpretation[abs(var)-1]>0 and var<0 ) or ( interpretation[abs(var)-1]<0 and var>0 ) :
            return False
        else:
            return True

    cost=len(formula)
    for clausula in formula:
        clausula_bool=False
        for var in clausula:
            if isTrue(var)==True:
                cost=cost-1
                break
    return cost

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
    global aux
    for i in range(0, num_vars):
        if aux[i]<0:
            interpretation[i]*=-1
            aux[i]=abs(aux[i])
            return interpretation
    return -1

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
    max_tries = 20000
    max_flips = 20000
    global num_vars
    global aux

    formula = getFormula(open(sys.argv[1], "r"))
    aux=[]
    for i in range(1, num_vars+1):
        aux.append(-i)
    for i in range(1, max_tries):
        interpretation=getRandomInterpretation()
        cost_interpretation = cost(interpretation, formula)
        if cost_interpretation == 0:
            print("c gsat-hill-climbing")
            print("s SATISFIABLE")
            print("v "+" ".join(map(str, interpretation)))
            exit()
        for j in range(1, max_flips):
            flip_interpretation = flipped(interpretation)
            if flip_interpretation == -1:
                for i in range(0, num_vars):
                    aux[i]=-1*aux[i]
                break
            flip_cost = cost(flip_interpretation, formula)
            if flip_cost < cost_interpretation:
                interpretation = flip_interpretation
                cost_interpretation = flip_cost
                if cost_interpretation == 0:
                    print("c gsat-hill-climbing")
                    print("s SATISFIABLE")
                    print("v "+" ".join(map(str, flip_interpretation)))
                    exit()
    print("c gsat-hill-cimbing")
    print("s UNSATISFIABLE")