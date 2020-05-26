#!/usr/bin/python

import sys
import os
import copy

# SAT  simple, recorre todo el árbol,
# 	aunque encuentre True.


class Interpretation:
	def __init__(self, n_vars, clauses):
		self.n_vars = n_vars
		self.vars = [None]*(self.n_vars+1)
		self.clauses = clauses
		self.best = best  #Puntero para guardar la mejor interpretacion del sover (solo var list).


	def next_varT(self):
		nexti = Interpretation(self.n_vars, copy.deepcopy(self.clauses), self.best)
		for i in range(1, len(self.vars)):
			if self.vars[i]==None:
				nexti.vars = list(self.vars)
				nexti.vars[i]=True
				return nexti

	def next_varF(self):
		nexti = Interpretation(self.n_vars, copy.deepcopy(self.clauses), self.best)
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
		self.best.set_list(self.vars)
		return True
        
	def show(self):
		print("\n-----")
		print(self)
		print(self.clauses)
		print(self.vars)

class Best:
	def __init__(self):
	 super().__init__()
	 self.list = []
	def set_list(self, vars):
		l=['v']
		for i in range(1,len(vars)):
			if vars[i]==True:
				l.append(i)
			else:
				l.append(-i)
		l.append(0)
		self.list = l
	def get_list(self):
		return ' '.join([str(elem) for elem in self.list])
class Solver():
	
	def __init__(self, num_vars, clauses):
		self.clauses = clauses
		self.num_vars = num_vars
		self.best=Best()

	def solve(self):
	
		def rec(interpretation):
			interpretation.show()
			if interpretation.is_complete():
				print("isComplete.")
				return interpretation.check_if_satisfiable()
			else:
				is_T_sat = rec(interpretation.next_varT())
				print(is_T_sat)
				interpretation.show()
				print("Voy ha hacer la rama F")
				is_F_sat = rec(interpretation.next_varF())
				if is_T_sat or is_F_sat:
					return True
				else:
					return False
		interpretation = Interpretation(self.num_vars, self.clauses, self.best)
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
		sys.stdout.write('\n')
		sys.stdout.write('c SAT-URADO\n')
		sys.stdout.write('s SATISFIABLE\n')
		sys.stdout.write(solver.best.get_list())
		sys.stdout.write('\n')

	else:
		sys.stdout.write('\n')
		sys.stdout.write('c SAT-URADO\n')
		sys.stdout.write('s UNSATISFIABLE')
		sys.stdout.write('\n')
