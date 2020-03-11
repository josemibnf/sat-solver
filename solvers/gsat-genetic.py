#!/usr/bin/python3
import sys
import random

def cost(interpretation):
    global formula
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

def random_population(nk):
    pop=[]
    for i in range(nk):
        pop.append(getRandomInterpretation())
    return pop

def best_individual(pop):
    best=[None, 99999999999]
    for i in pop:
        costi=cost(i)
        if costi == 0:
            print("c gsat")
            print("s SATISFIABLE")
            print("v "+" ".join(map(str, i)))
            exit()
        if costi<best[1]:
            best[0]=i
            best[1]=costi
    return best[0]

def selection(n, pop):
    def bubbleSort(arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1] :
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr    
    bubbleSort(pop)
    return pop[:n]
    
def mutation(k, pop):
    new_pop=[]
    for i in pop:
        new_pop.append(i)
        new_pop.append(flipped(i))
    return new_pop

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

#####
#sort: bubble O(n2)
#flip: random
#####

if __name__ == "__main__":
    global num_vars
    global formula
    n=10
    k=5
    max_flips=2000
    formula = getFormula(open(sys.argv[1], "r"))
    pop = random_population(n + k)
    best = best_individual(pop)
    for i in range (max_flips):
        best_pop = selection(n, pop)
        pop = mutation(k, best_pop)
        best = best_individual(pop)
    