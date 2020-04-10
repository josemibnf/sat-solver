#!/usr/bin/python3

import sys

import solvers.single as single
import solvers.frontier as frontier


import pandas as pd 
import numpy as np 

import sys
import os
import subprocess
import random

def train():
    
    # Generate CNFs
    os.system("rm -r benchmark-folder/*")
    try:
        while 1:
            if random.random() < 0.5:    # Mas variables que clausulas
                n_var = random.randrange(1,999)
                ratio = random.randrange(1,8)
                n_clauses = n_var//ratio
            else:                       # Mas clausulas que variables
                n_clauses = random.randrange(1,999)
                ratio = random.randrange(1,8)
                n_var = n_clauses//ratio
            rnd_cnf = "./rnd-cnf-gen-satisfiable.sh "+str(n_var)+" "+str(n_clauses)+" 3"
            subprocess.call(rnd_cnf, shell=True)
    except KeyboardInterrupt:
        pass
    
    # Rate CNFs
    
    

def parse(filename):
    clauses = []
    count = 0
    for line in open(filename):

        if line[0] == 'c':
            continue
        if line[0] == 'p':
            n_vars = int(line.split()[2])
            lit_clause = [[] for _ in range(n_vars * 2 + 1)]
            continue

        clause = []
        for literal in line[:-2].split():
            literal = int(literal)
            clause.append(literal)
            lit_clause[literal].append(count)
        clauses.append(clause)
        count += 1
    return clauses, n_vars, lit_clause


if __name__ == '__main__':
    """
    clauses, n_vars, lit_clause = parse(sys.argv[1])
    ratio = len(clauses)/n_vars

    if (ratio >= 2 and 3 > ratio) or (ratio >= 6 and 7 > ratio):
        print("Using frontier for {} ratio\n".format(ratio))
        frontier.run_sat(clauses, n_vars, lit_clause)
    else:
        print("Using single for {} ratio\n".format(ratio))
        single.run_sat(clauses, n_vars, lit_clause)
    """
    train()