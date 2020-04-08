#!/usr/bin/python3

import random
import sys


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


def get_random_interpretation(n_vars, frontera, omega=1):
    rand_interp =  [i if random.random() < 0.5 else -i for i in range(n_vars + 1)]
    if random.random() > omega and len(frontera[0])!=0:
        return frontera, random.choice(frontera[0])
    else:
        return frontera, rand_interp


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
    min_daño = sys.maxsize
    up_frontera = False
    best_literals = []
    for literal in clause:

        daño = 0

        for clause_index in lit_clause[-literal]:
            if true_sat_lit[clause_index] == 1:
                daño += 1

        for clause_index in lit_clause[literal]:
            if true_sat_lit[clause_index] == 0:
                daño -=1

        if daño < min_daño:
            min_daño = daño
            best_literals = [literal]
        elif daño == min_daño:
            best_literals.append(literal)

    if min_daño > 0 and random.random() < omega:
        best_literals = clause
        up_frontera = True
        #Hay una probabilidad omega de que, si no hay un literal perfecto, vayamos a barajar entre todos y no solo los de minimo 'daño'.

    return random.choice(best_literals), up_frontera

def prune(frontera):
    new = []
    for interpretacion in frontera[0]:
        if interpretacion[1] < frontera[1]:
            new.append(interpretacion)
    return ( new, frontera[1])

def run_sat(clauses, n_vars, lit_clause, max_flips_proportion=4):
    max_flips = n_vars * max_flips_proportion
    frontera = ([], len(clauses))
    while 1:
        frontera, interpretation = get_random_interpretation(n_vars, frontera)
        true_sat_lit = get_true_sat_lit(clauses, interpretation) # lista de positivos en cada clausula
        for _ in range(max_flips):

            unsatisfied_clauses_index = [index for index, true_lit in enumerate(true_sat_lit) if
                                         not true_lit]

            if not unsatisfied_clauses_index:
                
                print('c frontier')
                print('s SATISFIABLE')
                print('v ' + ' '.join(map(str, interpretation[1:])) + ' 0')
                exit()


            clause_index = random.choice(unsatisfied_clauses_index) # Seleccionamos random una de las clausulas F.
            unsatisfied_clause = clauses[clause_index] # Obtenemos la clausula.

            lit_to_flip, up_frontera = compute_broken(unsatisfied_clause, true_sat_lit, lit_clause) # Literal que modificamos.
            if up_frontera:
                frontera = ( frontera[0] , len(unsatisfied_clauses_index) )
                frontera = prune(frontera)

            # Actualizamos interpretacion.
            update_tsl(lit_to_flip, true_sat_lit, lit_clause)
            interpretation[abs(lit_to_flip)] *= -1

        if len(unsatisfied_clauses_index) < frontera[1]:
            frontera[0].append(interpretation)

 
if __name__ == '__main__':
    clauses, n_vars, lit_clause = parse(sys.argv[1])
    run_sat(clauses, n_vars, lit_clause)