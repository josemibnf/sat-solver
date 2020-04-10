#!/usr/bin/python3

import sys
import random
from multiprocessing import Process, Value
from ctypes import c_bool

################################## COMPARTIDO ##################################

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


#################################### SINGLE ####################################

def get_random_interpretation_single(n_vars):
    return [i if random.random() < 0.5 else -i for i in range(n_vars + 1)]

def compute_broken_single(clause, true_sat_lit, lit_clause, omega=0.4):
    min_daño = sys.maxsize
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
        #Hay una probabilidad omega de que, si no hay un literal perfecto, vayamos a barajar entre todos y no solo los de minimo 'daño'.

    return random.choice(best_literals)


def run_sat_single(clauses, n_vars, lit_clause, max_flips_proportion=4):
    max_flips = n_vars * max_flips_proportion
    while 1:
        interpretation = get_random_interpretation_single(n_vars)
        true_sat_lit = get_true_sat_lit(clauses, interpretation) # lista de positivos en cada clausula
        for _ in range(max_flips):

            unsatisfied_clauses_index = [index for index, true_lit in enumerate(true_sat_lit) if
                                         not true_lit]

            if not unsatisfied_clauses_index:

                print('c single')
                print('s SATISFIABLE')
                print('v ' + ' '.join(map(str, interpretation[1:])) + ' 0')
                exit()



            clause_index = random.choice(unsatisfied_clauses_index) # Seleccionamos random una de las clausulas F.
            unsatisfied_clause = clauses[clause_index] # Obtenemos la clausula.

            lit_to_flip = compute_broken_single(unsatisfied_clause, true_sat_lit, lit_clause) # Literal que modificamos.

            # Actualizamos interpretacion.
            update_tsl(lit_to_flip, true_sat_lit, lit_clause)
            interpretation[abs(lit_to_flip)] *= -1

################################### FRONTIER ###################################

def get_random_interpretation_frontier(n_vars, n_clauses, frontera):
    valor_0_1 = frontera[1] / n_clauses
    omega = valor_0_1**(1/3)
    if random.random() > omega    and len(frontera[0])!=0:
        return random.choice(frontera[0])
    else:
        return [i if random.random() < 0.5 else -i for i in range(n_vars + 1)]

def compute_broken_frontier(clause, true_sat_lit, lit_clause, omega=0.4):
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

def run_sat_frontier(clauses, n_vars, lit_clause, max_flips_proportion=4):
    max_flips = n_vars * max_flips_proportion
    frontera = ([], len(clauses))
    while 1:
        interpretation = get_random_interpretation_frontier(n_vars, len(clauses), frontera)
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

            lit_to_flip, up_frontera = compute_broken_frontier(unsatisfied_clause, true_sat_lit, lit_clause) # Literal que modificamos.
            if up_frontera:
                frontera = ( frontera[0] , len(unsatisfied_clauses_index) )
                frontera = prune(frontera)

            # Actualizamos interpretacion.
            update_tsl(lit_to_flip, true_sat_lit, lit_clause)
            interpretation[abs(lit_to_flip)] *= -1

        if len(unsatisfied_clauses_index) < frontera[1]:
            frontera[0].append(interpretation)

#################################### THREAD ####################################

def get_random_interpretation_thread(n_vars):
    return [i if random.random() < 0.5 else -i for i in range(n_vars + 1)]

def compute_broken_thread(clause, true_sat_lit, lit_clause, omega=0.4):
    min_daño = sys.maxsize
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
        #Hay una probabilidad omega de que, si no hay un literal perfecto, vayamos a barajar entre todos y no solo los de minimo 'daño'.

    return random.choice(best_literals)


def run_sat_thread():
    global eco, clauses, n_vars, lit_clause

    max_flips = n_vars * 4
    while 1:

        interpretation = get_random_interpretation_thread(n_vars)
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

            lit_to_flip = compute_broken_thread(unsatisfied_clause, true_sat_lit, lit_clause)

            update_tsl(lit_to_flip, true_sat_lit, lit_clause)

            interpretation[abs(lit_to_flip)] *= -1

def main_thread():
    global eco, clauses, n_vars, lit_clause  # eco=True ssi encontramos interpretacion valida.

    clauses, n_vars, lit_clause = parse(sys.argv[1])
    n_pop=len(clauses)//n_vars #poblacion en funcion del ratio clausulas/variables.

    p1 = Process(target=run_sat_thread)
    p2 = Process(target=run_sat_thread)
    p3 = Process(target=run_sat_thread)
    p4 = Process(target=run_sat_thread)
    p5 = Process(target=run_sat_thread)
    p6 = Process(target=run_sat_thread)
    p7 = Process(target=run_sat_thread)
    p8 = Process(target=run_sat_thread)
    p9 = Process(target=run_sat_thread)
    p10 = Process(target=run_sat_thread)
    p11 = Process(target=run_sat_thread)
    p12 = Process(target=run_sat_thread)
    p13 = Process(target=run_sat_thread)
    p14 = Process(target=run_sat_thread)
    p15 = Process(target=run_sat_thread)
    p16 = Process(target=run_sat_thread)
    p17 = Process(target=run_sat_thread)
    p18 = Process(target=run_sat_thread)
    p19 = Process(target=run_sat_thread)
    p20 = Process(target=run_sat_thread)

    eco = Value('i', 0)
    pop=[ p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20 ]

    for p in pop[:n_pop]:
        p.start()

    for p in pop[:n_pop]:
        p.join()

################################### GOTZILLA ###################################

def select_solver(hardness):
    solver_hardness = {
        "1": {"frontier": 30, "single": 20, "thread": 10},
        "2": {"single": 48, "frontier": 32, "thread": 16},
        "3": {"frontier": 60, "single": 40, "thread": 20},
        "4": {"frontier": 57, "single": 38, "thread": 19},
        "5": {"frontier": 51, "single": 34, "thread": 17},
        "6": {"frontier": 57, "single": 38, "thread": 19},
        "7": {"frontier": 72, "single": 48, "thread": 24},
        "8": {"frontier": 6, "single": 4, "thread": 2}
    }

    round_hardness = str(round(hardness))
    best_solver = list(solver_hardness[round_hardness])[0]

    return best_solver

if __name__ == '__main__':

    # Obtener datos del cnf pasado como parametro
    clauses, n_vars, lit_clause = parse(sys.argv[1])

    # Calcular su hardness (Ratio of Clauses-to-Variables)
    hardness = len(clauses)/n_vars

    # Seleccionar solver en funcion del hardness
    solver = select_solver(hardness)

    if solver == "single":
        run_sat_single(clauses, n_vars, lit_clause)
    elif solver == "frontier":
        run_sat_frontier(clauses, n_vars, lit_clause)
    elif solver == "thread":
        main_thread()
