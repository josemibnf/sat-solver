#!/usr/bin/python3

import sys

import solvers.single as single
import solvers.frontier as frontier


import json

import sys
import os
import subprocess
import random

def train():
    

    def read_tmp_rating(ratio ,dic):
        ratio_dic = dic.get(ratio)
        f = open("tmp-rating.txt", "r")
        for i in range(3,0,-1):
            l = f.readline()
            solver = l.split()[0]
            if solver in ratio_dic.keys():
                score = ratio_dic.get(solver) + i
            else:
                score = i
            ratio_dic[solver] = score
        dic[ratio] = ratio_dic
        return dic

    dic = { 1:{},
            2:{},
            3:{},
            4:{},
            5:{},
            6:{},
            7:{},
            8:{},
        }
    
    try:
        os.system("rm -r benchmark-folder/*")
        while 1:
            n_var = random.randrange(1,999)
            ratio = random.randrange(1,8)
            n_clauses = n_var//ratio
            rnd_cnf = "./rnd-cnf-gen-satisfiable.sh "+str(n_var)+" "+str(n_clauses)+" 3"
            if subprocess.call(rnd_cnf, shell=True) == 0:
                subprocess.call("./rate-solvers.sh")
                os.system("rm -r benchmark-folder/*")
                dic = read_tmp_rating(ratio ,dic)
            else:
                print ("NO SE ENCONTRO SATISF")
    except KeyboardInterrupt:
        pass
    os.system("rm -f tmp-rating.txt")
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