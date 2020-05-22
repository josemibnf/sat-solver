#!/usr/bin/python

import sys
import os
import copy

# Recorre hasta encontrar True,
# 	o hasta que algun método diga que
# 	todo es False.
# Usa simplify, y check_out.

class Interpretation:
	def __init__(self, n_vars, clauses):
		self.n_vars = n_vars
		self.vars = [None]*(self.n_vars+1)
		self.clauses = clauses

	def simplify(self):
		def has_value(l):
			if l < 0:
				return self.vars[-l]!=None
			else:
				return self.vars[l]!=None
		for c in self.clauses:
			try:
				for l in c:
					if has_value(l):
						if self.chekc_if_literal_is_satisfiable(l) :
							self.clauses.remove(c)
						else :
							c.remove(l)
							if c == []:
								return False #Como nos queda una clausula vacia, ya sabemos que el cnf en insat.
			except ValueError:
				print("Ya no tenemos la clausula.")

	def check_unit(self):
		def has_value(c):
			l = c[0]
			if l < 0:
				return self.vars[-l]!=None
			else:
				return self.vars[l]!=None
		def put_value(c):
			l = c[0]
			if l < 0:
				self.vars[-1*l] = False
			else:
				self.vars[l] = True
		for c in self.clauses:
			if len(c)==1:
				if has_value(c)==False:
					put_value(c)
					self.clauses.remove(c)
				elif self.check_if_clause_is_satisfiable(c):
					self.clauses.remove(c)
				else:
					return False # Si no se cumple esa clausula, ya sabemos que el cnf es insat.

	def next_varT(self):
		nexti = Interpretation(self.n_vars, copy.deepcopy(self.clauses))
		for i in range(1, len(self.vars)):
			if self.vars[i]==None:
				nexti.vars = list(self.vars)
				nexti.vars[i]=True
				return nexti

	def next_varF(self):
		nexti = Interpretation(self.n_vars, copy.deepcopy(self.clauses))
		for i in range(1, len(self.vars)):
			if self.vars[i]==None:
				nexti.vars = list(self.vars)
				nexti.vars[i]=False
				return nexti
	
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
			if self.chekc_if_literal_is_satisfiable(l)==True:
				return True
		return False

	def check_if_satisfiable(self):
		#Si no es completo retornará False
		for c in self.clauses:
			if self.check_if_clause_is_satisfiable(c)==False:
				print("es insatisfactible por la clausula ",c)
				return False
		print("bueno pues ya esta, es satisfactible, si.")
		return True
        
	def show(self):
		print("\n-----")
		print(self)
		print(self.clauses)
		print(self.vars)

class Solver():
	
	def __init__(self, num_vars, clauses):
		self.clauses = clauses
		self.num_vars = num_vars

	def solve(self):
		def rec(interpretation):
			print("\n\n****************************\n")
			interpretation.show()
			print("Simplify .....")
			if interpretation.simplify()==False: return False
			print("Check_unit .....")
			if interpretation.check_unit()==False: return False
			interpretation.show()
			if interpretation.is_complete():
				print("isComplete.")
				return interpretation.check_if_satisfiable()
			else:
				return ( rec(interpretation.next_varT()) or rec(interpretation.next_varF()) )
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
	if solver.solve():
		sys.stdout.write('\ns SATISFIABLE\nv ')
	else:
		sys.stdout.write('\ns UNSATISFIABLE\nv ')
	# Show the best solution found
	#best_sol.show()