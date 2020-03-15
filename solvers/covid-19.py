#!/usr/bin/python3

import random
import sys
from multiprocessing import Process, Value
from ctypes import c_bool

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


def get_random_interpretation(n_vars):
    return [i if random.random() < 0.5 else -i for i in range(n_vars + 1)]


def get_true_sat_lit(clauses, interpretation):
    true_sat_lit = [0 for _ in clauses]
    for index, clause in enumerate(clauses):
        for lit in clause:
            if interpretation[abs(lit)] == lit:
                true_sat_lit[index] += 1
    return true_sat_lit


def update_tsl(literal_to_flip, true_sat_lit, lit_clause):
    for clause_index in lit_clause[literal_to_flip]:
        true_sat_lit[clause_index] += 1
    for clause_index in lit_clause[-literal_to_flip]:
        true_sat_lit[clause_index] -= 1


def compute_broken(clause, true_sat_lit, lit_clause, omega=0.4):
    break_min = sys.maxsize
    best_literals = []
    for literal in clause:

        break_score = 0

        for clause_index in lit_clause[-literal]:
            if true_sat_lit[clause_index] == 1:
                break_score += 1
        
        for clause_index in lit_clause[literal]:
            if true_sat_lit[clause_index] == 0:
                break_score -=1

        if break_score < break_min:
            break_min = break_score
            best_literals = [literal]
        elif break_score == break_min:
            best_literals.append(literal)

    #Si el break_min esta en menos de 0 significa que el literal escogido no hace ningun 'daño'.
    if break_min > 0 and random.random() < omega:
        best_literals = clause
        #Hay una probabilidad omega de que, si no hay un literal que nos perfecto, vayamos a barajar entre todos y no solo los de minimo 'daño'.

    return random.choice(best_literals)


def run_sat():
    global eco, clauses, n_vars, lit_clause

    max_flips = n_vars * 4
    for flip in range(max_flips):

        interpretation = get_random_interpretation(n_vars)
        true_sat_lit = get_true_sat_lit(clauses, interpretation)
        for _ in range(max_flips):
            unsatisfied_clauses_index = [index for index, true_lit in enumerate(true_sat_lit) if
                                         not true_lit]

            if bool(eco.value) is True:
                exit()
            elif not unsatisfied_clauses_index:
                eco.value = 1
                print('c covid-19')
                print('s SATISFIABLE')
                print('v ' + ' '.join(map(str, interpretation[1:])) + ' 0')
                exit()

            clause_index = random.choice(unsatisfied_clauses_index)
            unsatisfied_clause = clauses[clause_index]

            lit_to_flip = compute_broken(unsatisfied_clause, true_sat_lit, lit_clause)

            update_tsl(lit_to_flip, true_sat_lit, lit_clause)

            interpretation[abs(lit_to_flip)] *= -1



if __name__ == '__main__':
    global eco, clauses, n_vars, lit_clause

    clauses, n_vars, lit_clause = parse(sys.argv[1])
    n_pop=len(clauses)//n_vars #poblacion en funcion del ratio clausulas/variables.

    p1 = Process(target=run_sat)
    p2 = Process(target=run_sat)
    p3 = Process(target=run_sat)
    p4 = Process(target=run_sat)
    p5 = Process(target=run_sat)
    p6 = Process(target=run_sat)
    p7 = Process(target=run_sat)
    p8 = Process(target=run_sat)
    p9 = Process(target=run_sat)
    p10 = Process(target=run_sat)
    p11 = Process(target=run_sat)
    p12 = Process(target=run_sat)
    p13 = Process(target=run_sat)
    p14 = Process(target=run_sat)
    p15 = Process(target=run_sat)
    p16 = Process(target=run_sat)
    p17 = Process(target=run_sat)
    p18 = Process(target=run_sat)
    p19 = Process(target=run_sat)
    p20 = Process(target=run_sat)

    eco = Value('i', 0)
    pop=[p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20]

    for p in pop[:n_pop]:
        p.start()

    for p in pop[:n_pop]:
        p.join()

    if bool(eco.value) is False:
        print('c covid-19')
        print('s INSATISFIABLE')
        exit()