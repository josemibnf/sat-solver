#!/usr/bin/python

import sys
import os

class Interpretation:
	def __init__(self, n_vars, clauses):
		self.n_vars = n_vars
		self.vars = [None]*(self.n_vars+1)
		self.clauses = clauses

	def davis_putman(self):
		def get_var_clauses(v):
			print("Obteniendo el var_clauses de la varialbe ",v, "  en ", self.clauses)
			var_clauses = []
			for c in self.clauses:
				print("Vamos a ver la clausula  ", c)
				for l in c:
					print(" El literal ...  ",l )
					if l==v :
						var_clauses.append((self.clauses.index(c),True)) #Is positive
						print("         Añado el indice de la clausula ",c, " ----> ",var_clauses," <------")
					elif -l==v :
						var_clauses.append((self.clauses.index(c),False)) #Is not positive
						print("         Añado el indice de la clausula ",c, " ----> ",var_clauses," <------")
			print("Saco ", var_clauses," de la  variable ",v," de ",self.clauses,"\n")
			return var_clauses
		def fusion( v, i1, i2):
			def s(bool):
				if bool:
					return v
				else:
					return -v
			#Toma dos indices de clausulas y las fusiona quitando el literal v, y lo añade.
			print(" --- Fusion ----")
			print(" Tenemos las clausulas ",self.clauses,"  y la variable es ", v)
			print("Elimina de la clausula ",i1[0]," el elemento ",s(i1[1]))
			self.clauses[i1[0]].remove(s(i1[1]))
			c1 = self.clauses[i1[0]]
			print(" Queda tal que asi ",self.clauses)
			print("Elimina de la clausula ",i2[0]," el elemento ",s(i2[1]))
			self.clauses[i2[0]].remove(s(i2[1]))
			c2 = self.clauses[i2[0]]
			print(" Queda tal que asi ",self.clauses, " he almacenado las clausulas c1: ",c1," y la c2: ",c2)
			try:
				self.clauses.remove(c1)
			except ValueError:
				pass
			try:
				self.clauses.remove(c2)
			except ValueError:
				pass
			print("Nos sacamos las dos clausulas, ", self.clauses)
			if c1 != [] or c2 != []:
				self.clauses.append(c1+c2)
			print("Y al final nos queda .. ",self.clauses)
		for v in range(1,self.n_vars+1):
			var_clauses = get_var_clauses(v)
			while len(var_clauses)>1:
				contrario = None
				for c in var_clauses[1:]:
					if c[1]==True and var_clauses[0][1]==False :
						contrario = c
					elif c[1]==False and var_clauses[0][1]==True :
						contrario = c
				if contrario==None:
					print(" Son todas del mismo signo, no hay nada que fusionar. ")
					break
				else:
					fusion( v, var_clauses[0], contrario)
					var_clauses = get_var_clauses(v)			

	def simplify(self):
		def value(l):
			if l < 0:
				return self.vars[-1*l]
			else:
				return self.vars[l]
		for c in self.clauses:
			try:
				for l in c:
					self.show()
					if ( value(l) == False and l <0 ) :
						self.clauses.remove(c)
					elif ( value(l) == True and l >0 ) :
						self.clauses.remove(c)
					elif ( value(l) == True and l <0 ) :
						c.remove(l)
					elif ( value(l) == False and l >0 ) :
						c.remove(l)
			except ValueError:
				print("Ya no tenemos la clausula.")

	def check_unit(self):
		def get_value(c):
			l = c[0]
			if l < 0:
				return self.vars[-1*l]
			else:
				return self.vars[l]
		def put_value(c):
			l = c[0]
			if l < 0:
				self.vars[-1*l] = False
			else:
				self.vars[l] = True
		for c in self.clauses:
			if len(c)==1:
				if get_value(c) == None:
					put_value(c)
					self.clauses.remove(c)
				else:
					print("ESTA INTERPRETACION NO ME VALE")
					return False

	def cost(self):
		pass

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
		return self.clauses==[[]]

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
				print("AtrtibuteError.")
				maybe_satisfiable = False
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