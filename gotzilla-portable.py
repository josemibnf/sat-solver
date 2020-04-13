#!/usr/bin/python3

import sys
import random
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

def get_random_interpretation(n_vars, n_clauses=None, frontera=None, var_omega=None):
    if solver == "frontier":
        valor_0_1 = frontera[1] / n_clauses
        omega = valor_0_1**(1/var_omega)
        if random.random() > omega    and len(frontera[0])!=0:
            return random.choice(frontera[0])

    return [i if random.random() < 0.5 else -i for i in range(n_vars + 1)]

def run_sat(clauses, n_vars, lit_clause, var_omega=None, max_flips_proportion=4):
    max_flips = n_vars * max_flips_proportion
    if solver == "frontier":
        frontera = ([], len(clauses))
    else:
        frontera = len(clauses)

    while 1:
        if solver == "frontier":
            interpretation = get_random_interpretation(n_vars, len(clauses), frontera, var_omega)
        else:
            interpretation = get_random_interpretation(n_vars)

        true_sat_lit = get_true_sat_lit(clauses, interpretation) # lista de positivos en cada clausula
        for _ in range(max_flips):

            unsatisfied_clauses_index = [index for index, true_lit in enumerate(true_sat_lit) if
                                         not true_lit]

            if not unsatisfied_clauses_index:

                print('c {}'.format(solver))
                print('s SATISFIABLE')
                print('v ' + ' '.join(map(str, interpretation[1:])) + ' 0')
                exit()

            if solver == "wall":
                valor_0_1 = frontera / len(clauses)
                omega = valor_0_1**(1/var_omega)
                if len(unsatisfied_clauses_index) > frontera  and  random.random() > omega:
                    break

                clause_index = random.choice(unsatisfied_clauses_index) # Seleccionamos random una de las clausulas F.
                unsatisfied_clause = clauses[clause_index] # Obtenemos la clausula.

                lit_to_flip, up_frontera = compute_broken(unsatisfied_clause, true_sat_lit, lit_clause) # Literal que modificamos.
                if up_frontera:
                    frontera = len(unsatisfied_clauses_index)

            elif solver == "single":
                clause_index = random.choice(unsatisfied_clauses_index) # Seleccionamos random una de las clausulas F.
                unsatisfied_clause = clauses[clause_index] # Obtenemos la clausula.

                lit_to_flip, up_frontera = compute_broken(unsatisfied_clause, true_sat_lit, lit_clause) # Literal que modificamos.

            elif solver == "frontier":

                clause_index = random.choice(unsatisfied_clauses_index) # Seleccionamos random una de las clausulas F.
                unsatisfied_clause = clauses[clause_index] # Obtenemos la clausula.

                lit_to_flip, up_frontera = compute_broken(unsatisfied_clause, true_sat_lit, lit_clause) # Literal que modificamos.
                if up_frontera:
                    frontera = ( frontera[0] , len(unsatisfied_clauses_index) )
                    frontera = prune(frontera)

            # Actualizamos interpretacion.
            update_tsl(lit_to_flip, true_sat_lit, lit_clause)
            interpretation[abs(lit_to_flip)] *= -1

        if solver == "frontier":
            if len(unsatisfied_clauses_index) < frontera[1]:
                frontera[0].append(interpretation)

def prune(frontera):
    new = []
    for interpretacion in frontera[0]:
        if interpretacion[1] < frontera[1]:
            new.append(interpretacion)
    return ( new, frontera[1])

################################### GOTZILLA ###################################

def select_solver(hardness):
    omega = 0
    solver_hardness = {"1": {"frontier1": 781, "frontier2": 652, "frontier3": 612, "single": 542, "wall1": 340, "wall2": 418, "wall3": 272, "wall4": 296, "frontier4": 452}, "2": {"frontier1": 926, "frontier2": 828, "frontier4": 555, "single": 671, "wall3": 362, "wall4": 413, "frontier3": 781, "wall1": 444, "wall2": 555}, "3": {"frontier1": 906, "frontier4": 526, "single": 682, "wall4": 465, "frontier2": 751, "frontier3": 779, "wall1": 461, "wall2": 541, "wall3": 334}, "4": {"frontier1": 822, "frontier2": 700, "frontier3": 711, "single": 610, "wall3": 300, "frontier4": 561, "wall1": 405, "wall2": 473, "wall4": 413}, "5": {"frontier2": 748, "frontier4": 561, "single": 596, "wall3": 330, "wall4": 410, "frontier1": 859, "frontier3": 704, "wall1": 441, "wall2": 481}, "6": {"frontier2": 702, "wall3": 323, "wall4": 334, "frontier1": 809, "frontier3": 681, "frontier4": 535, "single": 606, "wall1": 399, "wall2": 471}, "7": {"frontier1": 834, "frontier2": 739, "frontier4": 541, "wall3": 376, "frontier3": 715, "single": 626, "wall1": 442, "wall2": 464, "wall4": 393}, "8": {"frontier2": 806, "single": 697, "wall2": 540, "wall4": 435, "frontier1": 963, "frontier3": 833, "frontier4": 615, "wall1": 468, "wall3": 358}}
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
        run_sat(clauses, n_vars, lit_clause)
    elif solver == "frontier":
        run_sat(clauses, n_vars, lit_clause, omega)
    elif solver == "wall":
        run_sat(clauses, n_vars, lit_clause, omega)
    else:
        print("{} is not a valid solver".format(solver))
