#!/usr/bin/python

import sys
import os

class Interpretation:
	def __init__(self, n_vars, clauses):
		self.n_vars = n_vars
		self.vars = [None]*(self.n_vars+1)
		self.clauses = clauses

	def next_varT(self):
		for i, v in enumerate(self.vars[1:]):
			if v==None:
				self.vars[i]=True
				return self

	def next_varF(self):
		for i, v in enumerate(self.vars[1:]):
			if v==None:
				self.vars[i]=False
				return self
	
	def is_complete(self):
		for v in self.vars[1:]:
			if v == None:
				return False
		return True

	def chekc_if_literal_is_satisfiable(self, literal):
		if literal>0:
			return self.vars[literal]==True
		else:
			return self.vars[-literal]==False

	def check_if_clause_is_satisfiable(self, clause):
		for l in clause:
			if chekc_if_literal_is_satisfiable(l)==True:
				return True
		return False

	def check_if_satisfiable(self):
		#Si no es completo retornará False
		for c in self.clauses:
			if check_if_clause_is_satisfiable(c)==False:
				return False
		return True
        

	def show(self):
		print("-----")
		print(self.clauses)
		print(self.vars)
		print("-------")

class Solver():
	
	def __init__(self, num_vars, clauses):
		self.clauses = clauses
		self.num_vars = num_vars

	def solve(self):
	
		def rec(interpretation):
			if interpretation.is_complete():
				return interpretation.check_if_satisfiable()
			else:
				return rec(interpretation.next_varT()) or rec(interpretation.next_varF())
		interpretation = Interpretation(self.num_vars, self.clauses)
		return rec(interpretation)

def parse(file):
    clauses = []
    count = 0
    for line in open(file):
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
    return n_vars, clauses

if __name__ == '__main__' :
	# Check parameters
	if len(sys.argv) < 1 or len(sys.argv) > 2:
		sys.exit("Use: %s <cnf_instance>" % sys.argv[0])

	if os.path.isfile(sys.argv[1]):
		cnf_file_name = os.path.abspath(sys.argv[1])
	else:
		sys.exit("ERROR: CNF instance not found (%s)." % sys.argv[1])

	# Read cnf instance
	num_vars, clauses = parse(cnf_file_name)
	# Create a solver instance with the problem to solve
	solver = Solver(num_vars, clauses)
	# Solve the problem and get the best solution found
	print(solver.solve())
	# Show the best solution found
	#best_sol.show()