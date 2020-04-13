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

def get_random_interpretation_frontier(n_vars, n_clauses, frontera, var_omega):
    valor_0_1 = frontera[1] / n_clauses
    omega = valor_0_1**(1/var_omega)
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

def run_sat_frontier(clauses, n_vars, lit_clause, var_omega, max_flips_proportion=4):
    max_flips = n_vars * max_flips_proportion
    frontera = ([], len(clauses))
    while 1:
        interpretation = get_random_interpretation_frontier(n_vars, len(clauses), frontera, var_omega)
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

##################################### WALL #####################################

def get_random_interpretation_wall(n_vars):
    return [i if random.random() < 0.5 else -i for i in range(n_vars + 1)]

# Igual que Frontier
def compute_broken_wall(clause, true_sat_lit, lit_clause, omega=0.4):
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

def run_sat_wall(clauses, n_vars, lit_clause, var_omega, max_flips_proportion=4):
    max_flips = n_vars * max_flips_proportion
    frontera = len(clauses)
    while 1:
        interpretation = get_random_interpretation_wall(n_vars)
        true_sat_lit = get_true_sat_lit(clauses, interpretation) # lista de positivos en cada clausula
        for _ in range(max_flips):

            unsatisfied_clauses_index = [index for index, true_lit in enumerate(true_sat_lit) if
                                         not true_lit]

            if not unsatisfied_clauses_index:

                print('c frontier')
                print('s SATISFIABLE')
                print('v ' + ' '.join(map(str, interpretation[1:])) + ' 0')
                exit()

            valor_0_1 = frontera / len(clauses)
            omega = valor_0_1**(1/var_omega)
            if len(unsatisfied_clauses_index) > frontera  and  random.random() > omega:
                break

            clause_index = random.choice(unsatisfied_clauses_index) # Seleccionamos random una de las clausulas F.
            unsatisfied_clause = clauses[clause_index] # Obtenemos la clausula.

            lit_to_flip, up_frontera = compute_broken_wall(unsatisfied_clause, true_sat_lit, lit_clause) # Literal que modificamos.
            if up_frontera:
                frontera = len(unsatisfied_clauses_index)

            # Actualizamos interpretacion.
            update_tsl(lit_to_flip, true_sat_lit, lit_clause)
            interpretation[abs(lit_to_flip)] *= -1


################################### GOTZILLA ###################################

def select_solver(hardness):
    omega = 0
    solver_hardness = {"1": {"frontier1": 3, "frontier3": 3, "wall1": 1}, "2": {"single": 3, "frontier1": 2, "frontier2": 1}, "3": {"frontier2": 10, "single": 4, "wall3": 1}, "4": {"frontier2": 8, "wall4": 2, "frontier1": 5}, "5": {"frontier1": 6, "frontier2": 3, "frontier3": 3}, "6": {"frontier1": 10, "frontier2": 4, "single": 5}, "7": {"wall2": 4, "frontier1": 2, "frontier3": 4}, "8": {"frontier3": 3, "single": 2, "wall1": 1}}
    round_hardness = str(round(hardness))
    solvers_available = solver_hardness[round_hardness]
    best_solver = min(solvers_available, key=solvers_available.get)

    if best_solver != "single":
        omega = int(best_solver[len(best_solver)-1])
        best_solver = best_solver[:-1]

    return best_solver, omega

if __name__ == '__main__':

    # Obtener datos del cnf pasado como parametro
    clauses, n_vars, lit_clause = parse(sys.argv[1])

    # Calcular su hardness (Ratio of Clauses-to-Variables)
    hardness = len(clauses)/n_vars

    # Seleccionar solver en funcion del hardness
    solver, omega = select_solver(hardness)

    if solver == "single":
        run_sat_single(clauses, n_vars, lit_clause)
    elif solver == "frontier":
        run_sat_frontier(clauses, n_vars, lit_clause, omega)
    elif solver == "wall":
        run_sat_wall(clauses, n_vars, lit_clause, omega)
    else:
        print("{} is not a valid solver".format(solver))
