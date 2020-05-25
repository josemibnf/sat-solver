#!/usr/bin/python3

# Libraries

import sys
import os
import random
import signal
import time

# Functions

def unit_propagation(formula):
	unit_clauses = []
	resulting_formula = formula.copy()

	# Get all unit clauses
	for clause in formula:
		if len(clause) == 1:
			unit_clauses += clause

	# Propagate unit clauses
	for clause in formula:
		for literal in unit_clauses:
			# Every clause (other than the unit clause itself) containing l is removed (the clause is satisfied if l is)
			if len(clause) > 1 and literal in clause:
				if clause in resulting_formula:
					# print(clause, " remove because we have ",literal)
					resulting_formula.remove(clause)

			# In every clause that contains -l this literal is deleted (-l can not contribute to it being satisfied)
			flip_literal = literal * -1
			if flip_literal in clause:
				if clause in resulting_formula:
					# print(clause, " change to", [x for x in clause if x != flip_literal], "because we have",literal)
					resulting_formula.remove(clause)
					resulting_formula.append([x for x in clause if x != flip_literal])

	# Keep simplifying the formula as long as new unit clauses exist
	if resulting_formula != formula:
		return unit_propagation(resulting_formula)

	return resulting_formula

def pure_literal_rule(self):
	pass

def dpll(self):
	pass

# Classes

class CNF():
	"""A CNF formula """

	def __init__(self, cnf_file_name):
		"""
		Initialization
		num_vars: Number of variables
		num_clauses: Number of clauses
		clause_length: Length of the clauses
		clauses: List of clauses
		"""
		self.num_vars = None
		self.num_clauses = None
		self.clauses = []
		self.read_cnf_file(cnf_file_name)

	def read_cnf_file(self, cnf_file_name):
		instance = open(cnf_file_name, "r")
		for l in instance:
			if l[0] == "c":
				continue
			if l[0] == "p":
				sl = l.split()
				self.num_vars = int(sl[2])
				self.num_clauses = int(sl[3])
				continue
			if l.strip() == "":
				continue
			sl = list(map(int, l.split()))
			sl.pop() # Remove last 0
			self.clauses.append(sl)

	def show(self):
		"""Prints the formula to the stdout"""

		sys.stdout.write("c Random CNF formula\n")
		sys.stdout.write("p cnf %d %d\n" % (self.num_vars, self.num_clauses))
		for c in self.clauses:
			sys.stdout.write("%s 0\n" % " ".join(map(str, c)))

class Interpretation():
	"""An interpretation is an assignment of the possible values to variables"""

	def __init__(self, num_vars):
		"""
		Initialization
		TODO
		"""
		self.num_vars = num_vars
		self.vars = [None] * (self.num_vars + 1)

	def cost(self):
		cost = 0
		for c in cnf.clauses:
			length = len(c)
			for l in c:
				if self.vars[abs(l)] == None or (l < 0 and self.vars[abs(l)] == 0) or (l > 0 and self.vars[abs(l)] == 1): # Undef or Satisfies clause
					break
				else:
					length -= 1
			if length == 0: # Falsified clause
				cost += 1
		return cost

	def copy(self):
		new = Interpretation(self.num_vars)
		new.vars = list(self.vars)
		return new

	def show(self):
		if self.vars[self.num_vars] == None:
			sys.stdout.write('\ns UNSATISFIABLE\n')
		else:
			sys.stdout.write('\ns SATISFIABLE\nv ')
			for v, s in enumerate(self.vars[1:]):
				if not s:
					sys.stdout.write('-')
				sys.stdout.write('%i ' % (v + 1))
			sys.stdout.write('0\n')

class Solver():
	"""The class Solver implements an algorithm to solve a given problem instance"""

	def __init__(self, cnf):
		"""
		Initialization
		TODO
		"""
		self.cnf = cnf
		self.best_sol = None
		self.best_cost = cnf.num_clauses + 1

	def solve(self):
		"""
		Implements an algorithm to solve the instance of a problem
		"""

		self.cnf.clauses = unit_propagation(self.cnf.clauses)

		curr_sol = Interpretation(self.cnf.num_vars)
		var = 1
		while var > 0:
			if curr_sol.vars[var] == 1: # Backtrack
				curr_sol.vars[var] = None
				var = var - 1
				continue
			if curr_sol.vars[var] == None: # Extend left branch
				curr_sol.vars[var] = 0
			else: # Extend right branch
				curr_sol.vars[var] = 1
			if curr_sol.cost() == 0: # Undet or SAT
				if var == self.cnf.num_vars: # SAT
					return curr_sol
				else: # Undet
					var = var + 1
		return curr_sol


# Main

if __name__ == '__main__' :
	"""
	TODO
	"""

	# Check parameters
	if len(sys.argv) < 1 or len(sys.argv) > 2:
		sys.exit("Use: %s <cnf_instance>" % sys.argv[0])

	if os.path.isfile(sys.argv[1]):
		cnf_file_name = os.path.abspath(sys.argv[1])
	else:
		sys.exit("ERROR: CNF instance not found (%s)." % sys.argv[1])

	# Read cnf instance
	cnf = CNF(cnf_file_name)
	# Create a solver instance with the problem to solve
	solver = Solver(cnf)
	# Solve the problem and get the best solution found
	best_sol = solver.solve()
	# Show the best solution found
	best_sol.show()
