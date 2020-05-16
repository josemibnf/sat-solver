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
				return self.vars[l]
		for c in self.clauses:
			for l in c:
				if ( value(l) == True and l >0 ) or ( value(l) == False and l <0 ) :
					c = c.remove(l)

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
				else:
					print("ESTA INTERPRETACION NO ME VALE")
					exit()

	def show(self):
		print("-----")
		print(self.clauses)
		print(self.vars)
		print("-------")


if __name__ == "__main__":
	i = Interpretation(3, [[1,-2],[2,3]])
	i.vars=[None, True, None, None, None, None]
	i.show()
	i.simplify()
	i.show()
	i.check_unit()
	i.show()