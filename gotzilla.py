#!/usr/bin/python3

import sys

import solvers.single as single


import json

import sys
import os
import subprocess
import random

def train():
    

    def read_tmp_rating(ratio ,dic):
        new = {}
        ratio_dic = dic.get(ratio)
        f = open("tmp-rating.txt", "r")
        for i in range(3,0,-1):
            l = f.readline()
            solver = l.split()[0]
            print(solver,end="   <<=-=>>   ")
            if solver in ratio_dic.keys():
                score = ratio_dic.get(solver) + i
            else:
                score = i
            new[solver] = score
        return {ratio:new}

    with open("gotzilla-train.json") as j:
        dic = json.load(j)
    
    try:
        os.system("rm -r benchmark-folder/*")
        while 1:
            n_var = random.randrange(1,999)
            ratio = random.randrange(1,9)
            n_clauses = n_var//ratio
            rnd_cnf = "./rnd-cnf-gen-satisfiable.sh "+str(n_var)+" "+str(n_clauses)+" 3"
            if subprocess.call(rnd_cnf, shell=True) == 0:
                subprocess.call("./rate-solvers.sh")
                os.system("rm -r benchmark-folder/*")
                print("\nBenchmark ",n_var," - ",n_clauses, end=" ------=>>>     ")
                dic.update( read_tmp_rating(str(ratio) ,dic) )
            else:
                print ("\nNO SE ENCONTRO SATISF")
    except KeyboardInterrupt:
        pass
    os.system("rm -f tmp-rating.txt && rm -f tmp.txt")
    os.system("rm -r benchmark-folder/*")
    print("\n\n",dic)
    with open("gotzilla-train.json","w") as j:
        json.dump( dic, j)

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
    train()