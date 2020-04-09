#!/usr/bin/python3

import sys
import single
import frontier

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
    clauses, n_vars, lit_clause = parse(sys.argv[1])
    ratio = len(clauses)/n_vars

    if ratio > 3.5 and 4.5 > ratio:
        print("Using single for {} ratio\n".format(ratio))
        single.run_sat(clauses, n_vars, lit_clause)
    else:
        print("Using frontier for {} ratio\n".format(ratio))
        frontier.run_sat(clauses, n_vars, lit_clause)
