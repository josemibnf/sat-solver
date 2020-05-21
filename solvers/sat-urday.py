#!/usr/bin/python

import sys
import os

class Interpretation:
	def __init__(self, n_vars, clauses):
		self.n_vars = n_vars
		self.vars = [None]*(self.n_vars+1)
		self.clauses = clauses

	def next_varT(self):
		for i, v in enumerate(self.vars):
			if v==None:
				self.vars[i]=True
				return self

	def next_varF(self):
		for i, v in enumerate(self.vars):
			if v==None:
				self.vars[i]=False
				return self
	
	def is_complete(self):
		for v in self.vars:
			if v == None:
				return False
		return True

	def check_if_satisfiable(self):
		#Si no es completo retornará False
		print(self.clauses)
		return self.clauses==[]

	def show(self):
		print("-----")
		print(self.clauses)
		print(self.vars)
		print("-------")

class Solver():
	"""The class Solver implements an algorithm to solve a given problem instance"""

	def __init__(self, num_vars, clauses):
		self.clauses = clauses
		self.num_vars = num_vars

	def solve(self):
		"""
		Implements an algorithm to solve the instance of a problem
		"""
		def rec(interpretation):
			maybe_satisfiable = True
			try:
				interpretation.show()
				interpretation.davis_putman()
				interpretation.simplify()
				maybe_satisfiable = interpretation.check_unit()
			except AttributeError:
				print("AtrtibuteError. Ya hemos quitado todas las clausulas que se cumplian.")
			if maybe_satisfiable==False:
				return False
			elif interpretation.is_complete():
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