#!/usr/bin/python

class Interpretation:
	def __init__(self, n_vars, clauses):
		self.n_vars = n_vars
		self.vars = [None]*(self.n_vars+1)
		self.clauses = clauses
	
	def davis(self):
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
			#Toma dos indices de clausulas y las fusiona quitando el literal v, y lo añade.
			c1 = self.clauses[i1].remove(v)
			c2 = self.clauses[i2].remove(v)
			self.clauses.remove(c1)
			self.clauses.remove(c2)
			self.clauses.append(c1+c2)
		for v in range(1,self.n_vars+1):
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
					var_clauses = get_var_clauses(v)
				

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
	"""
	i.simplify()
	i.show()
	i.check_unit()
	i.show()
	"""