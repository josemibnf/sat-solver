#!/usr/bin/python3
#-*- coding:utf-8 -*-
#######################################################################
# Copyright 2020 Josep Argelich

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################

# Libraries

import sys
import random

# Classes 

class Interpretation():
	"""An interpretation is an assignment of the possible values to variables"""

	def __init__(self, N):
		"""
		Initialization
		N: The problem to solve
		num_vars: Number of variables to encode the problem
		vars: List of variables from 0 to num_vars - 1. The value in position [i]
	          of the list is the value that the variable i takes for the current
	          interpretation
		"""
		self.num_vars = N
		self.vars = list(range(self.num_vars))
		self.get_random_interpretation()

	def get_random_interpretation(self):
		"""Get a random interpretation for all the variables"""
		#First method that can repeat rows
		for i in range(self.num_vars):
			self.vars[i] = random.randint(0, self.num_vars - 1)
		#Second method (faster, but cannot generate all possible permutations for big N)
		#random.shuffle(self.vars)

	def get_neighbors(self):
		"""Get neighbors that differ in one variable"""
		nbs = []
		for i in range(self.num_vars):
			new_nb = self.copy()
			value = random.randint(0, self.num_vars - 2)
			if value >= new_nb.vars[i]:
				value += 1
			new_nb.vars[i] = value
			nbs.append(new_nb)
		return nbs

	def get_neighbor(self):
		"""Get the best neighbors (ties broken by picking first best solution)"""
		nbs = self.get_neighbors()
		best_nb = None
		best_cost = self.num_vars
		for inb, nb in enumerate(nbs):
			if nb.cost() < best_cost:
				best_nb = inb
				best_cost = nb.cost()
		return nbs[best_nb]

	def cost(self):
		"""Compute the cost for the interpretation"""
		total_cost = 0
		for num_queen, row_queen in enumerate(self.vars): # Iterate over all the columns
			for num_queen2 in range(num_queen + 1, self.num_vars): # Iterate over the columns on the right of num_queen
				if row_queen == self.vars[num_queen2] or abs(num_queen - num_queen2) == abs(row_queen - self.vars[num_queen2]): # If they are in the same row (not needed for random.shuffle) or they are in the same diagonal
					total_cost += 1
					break
		return total_cost

	def copy(self):
		"""Copy the values of this instance of the class Interpretation to another instance"""
		c = Interpretation(self.num_vars)
		c.vars = list(self.vars)
		return c

	def show(self):
		"""Show the solution that represents this interpretation"""
		print("Solution for %i queens with cost %i:" % (self.num_vars, self.cost()))
		print(self.vars)
		# First line
		sys.stdout.write("+")
		for c in range(self.num_vars):
			sys.stdout.write("---+")
		sys.stdout.write("\n")
		# Draw board rows
		for r in range(self.num_vars):
			sys.stdout.write("|")
			# Draw column position
			for c in range(self.num_vars):
				if r == self.vars[c]: # If the row == to the value of the variable
					sys.stdout.write(" X |")
				else:
					sys.stdout.write("   |")
			sys.stdout.write("\n")
			# Middle lines
			sys.stdout.write("+")
			for c in range(self.num_vars):
				sys.stdout.write("---+")
			sys.stdout.write("\n")

class Solver():
	"""The class Solver implements an algorithm to solve a given problem instance"""

	def __init__(self, problem):
		"""
		Initialization
		problem: An instance of a problem
		best_sol: Best solution found so far
		best_cost: Cost of the best solution
		"""
		self.problem = problem
		self.best_sol = None
		self.best_cost = problem

	def solve(self, max_tries = 1000):
		"""
		Implements an algorithm to solve the instance of a problem
		max_tries: Maximum number of tries to solve the problem
		"""
		curr_sol = Interpretation(self.problem) # Random initial interpretation
		for i in range(max_tries): # Try to find a solution max_tries times
			curr_sol = curr_sol.get_neighbor() # Get a new interpretation
			if curr_sol.cost() < self.best_cost: # If it improves the best solution found so far
				self.best_sol = curr_sol.copy() # Save it as best solution
				self.best_cost = curr_sol.cost() # and its cost
				if self.best_cost == 0: # If the best solution cannot be improved
					break # Finish
		return self.best_sol


# Main

if __name__ == '__main__' :
	"""
	A basic neighborhood search algorithm to solve the N queens problem
	Techniques: Steepest ascent Hill Climbing + Mildest descent
	"""

	# Check parameters
	if len(sys.argv) < 2 or len(sys.argv) > 3:
		sys.exit("Use: %s <N> [<random_seed>]" % sys.argv[0])
	
	try:
		N = int(sys.argv[1])
	except:
		sys.exit("ERROR: Number of queens not an integer (%s)." % sys.argv[1])
	if (N < 4):
		sys.exit("ERROR: Number of queens must be >= 4 (%d)." % N)

	if len(sys.argv) > 2:
		try:
			seed = int(sys.argv[2])
		except:
			sys.exit("ERROR: Seed number not an integer (%s)." % sys.argv[2])
	else:
		seed = None

	# Initialize random seed (current time)
	random.seed(seed)
	# Create a solver instance with the problem to solve
	solver = Solver(N)
	# Solve the problem and get the best solution found
	best_sol = solver.solve()
	# Show the best solution found
	best_sol.show()
