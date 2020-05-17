#!/usr/bin/python

class Interpretation:
	def __init__(self, n_vars, clauses):
		self.n_vars = n_vars
		self.vars = [None]*(self.n_vars+1)
		self.clauses = clauses
	
	def davis(self):
		def get_var_clauses(v):
			var_clauses=[None]*(len(self.clauses))
			for c in self.clauses:
				for l in c:
					if l==v :
						var_clauses.append[self.clauses.index(c)]
					elif -l==v :
						var_clauses.append[-self.clauses.index(c)]
			return var_clauses
		def fusion( v, i1, i2):
			#Toma dos indices de clausulas y las fusiona quitando el literal v, y lo añade.
			c1 = self.clauses[i1].remove(v)
			c2 = self.clauses[i2].remove(v)
			self.clauses.append(c1+c2)
		for v in range(self.n_vars):
			var_clauses = get_var_clauses(v)
			while len(var_clauses)>1:
				contrario = None
				for c in var_clauses[1:]:
					if c>0 and var_clauses[0]<0 :
						contrario = c
					elif c>0 and var_clauses[0]<0 :
						contrario = c
				if contrario==None:
					break # Son todas del mismo signo, no hay nada que fusionar.
				else:
					fusion( v, var_clauses[0], var_clauses[contrario])
				

	def simplify(self):
		def value(l):
			if l < 0:
				return self.vars[-1*l]
			else:
				return self.vars[l]
		for c in self.clauses:
			for l in c:
				if ( value(l) == False and l <0 ) :
					c.remove(l)
				elif ( value(l) == True and l >0 ) :
					self.clauses.remove(c)

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
					exit()

	def show(self):
		print("-----")
		print(self.clauses)
		print(self.vars)
		print("-------")


if __name__ == "__main__":
	i = Interpretation(5, [[1,-2],[2,3,-4],[5,-5]])
	i.vars=[None, True, None, None, None, False]
	i.show()
	i.davis()
	i.show()
	i.simplify()
	i.show()
	i.check_unit()
	i.show()