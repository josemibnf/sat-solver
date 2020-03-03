#!/usr/bin/python3
import sys
import random

#  1->True  0->False

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

def getRandomInterpretation(formula, num_vars): 
    interpretation=[]
    for var in range (0, num_vars):
        interpretation.append(random.randrange(0,2))
    return interpretation

def flipped(interpretation):
    flip_var = random.randrange(0,len(formula[0])-1)
    if interpretation[flip_var]==0:
        interpretation[flip_var]=1
    else:
        interpretation[flip_var]=0
    return interpretation

def getFormula(cnf):
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
    return formula, num_vars