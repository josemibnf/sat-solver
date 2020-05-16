#!/usr/bin/python

class Interpretation:
	def __init__(self, n_vars, clauses):
		self.n_vars = n_vars
		self.vars = [None]*(self.n_vars+1)
		self.clauses = clauses
	
	def simplify(self):
		def value(l):
			if l < 0:
				return self.vars[-1*l]
			else:
				print(self.vars)
				return self.vars[l]
		for c in self.clauses:
			for l in c:
				if value(l) == None:
					print(l,c)
				elif ( value(l) == True and l >0 ) or ( value(l) == False and l <0 ) :
					print("remove")
					c = c.remove(l)

	def check_unit(self):
		for c in self.clauses:
			pass

	


if __name__ == "__main__":
	i = Interpretation(3, [[1,-2],[2,3]])
	i.vars=[None, True, None, None, None, None]
	print(i.clauses)
	print(i.vars)
	print("-------")
	i.simplify()
	print("-----")
	print(i.clauses)
	print(i.vars)
