#!/usr/bin/python

import sys
import os
import copy

class Interpretation:
	def __init__(self, n_vars, clauses):
		self.n_vars = n_vars
		self.vars = [None]*(self.n_vars+1)
		self.clauses = clauses

	def davis_putman(self):
		def get_var_clauses(v):
			var_clauses = []
			for c in self.clauses:
				for l in c:
					if l==v :
						var_clauses.append((self.clauses.index(c),True)) #Is positive
					elif -l==v :
						var_clauses.append((self.clauses.index(c),False)) #Is not positive
			return var_clauses
		def fusion( v, i1, i2):
			def s(bool):
				if bool:
					return v
				else:
					return -v
			self.clauses[i1[0]].remove(s(i1[1]))
			c1 = self.clauses[i1[0]]
			self.clauses[i2[0]].remove(s(i2[1]))
			c2 = self.clauses[i2[0]]
			try:
				self.clauses.remove(c1)
			except ValueError:
				pass
			try:
				self.clauses.remove(c2)
			except ValueError:
				pass
			if c1 != [] or c2 != []:
				self.clauses.append(c1+c2)
		for v in range(1,self.n_vars):
			var_clauses = get_var_clauses(v)
			while len(var_clauses)>1:
				contrario = None
				for c in var_clauses[1:]:
					if c[1]==True and var_clauses[0][1]==False :
						contrario = c
					elif c[1]==False and var_clauses[0][1]==True :
						contrario = c
				if contrario==None:
					break
				else:
					fusion( v, var_clauses[0], contrario)
					var_clauses = get_var_clauses(v)			

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
			except ValueError:
				print("Ya no tenemos la clausula.")

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
			interpretation.davis_putman()
			interpretation.simplify()
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
	print(solver.solve())
	# Show the best solution found
	#best_sol.show()