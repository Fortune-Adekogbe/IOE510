#! /usr/bin/python
# Implements the model in IOE 510F25 homework 2 problem 2(b) 

import gurobipy as gp
from gurobipy import GRB
import numpy as np

def solve(sugars, content, suppliers, cost, percentage, minPurchase):
	# Name your Model
	m=gp.Model("510hwk2p2b")
	

	# defining parameters

	c = np.zeros(shape=(len(suppliers),))
	for j, value in cost.items():
		c[suppliers.index(j)] = value

	P = np.zeros(shape=(len(sugars), len(suppliers)))
	for (i, j), p in percentage.items():
		P[sugars.index(i), suppliers.index(j)] = p/100 # fractional probability values

	b = np.zeros(shape=(len(sugars),))
	for i, blend_i in content.items():
		b[sugars.index(i)] = blend_i
	
	t = minPurchase
	
	# Create decision variables: amounts to buy from each supplier
	# nonnegative by default

	x = m.addMVar(len(suppliers))
	
	# Objective: total cost
	# to be minimized by default
	m.setObjective(c @ x, GRB.MINIMIZE)
	
	# Constraints on blend 
	
	m.addMConstr(
		P, x,'=', b
	)

	m.addConstrs(
		(x[j] >= t for j, _ in enumerate(suppliers)),
		name="good_relations"
	)
	
	# Specify how to format the output
	def printSolution():
		if m.status == GRB.OPTIMAL:
			print('\nCost: %g' % m.objVal)
			print('\nbuy:')
			for j, supplier in enumerate(suppliers):
				print(f"\t{x[j].X:.2f} tons of sugar from supplier {supplier}")

		elif m.status == GRB.INFEASIBLE:
			print('Model is infeasible')
		elif m.status == GRB.UNBOUNDED:
			print('Model is unbounded')
		else:
			print('Optimization ended with status %d' % m.status)
			
			
	# Change default values of parameters to differentiate 
	# infeasible from unbounded LPs if no optimal solution found
	# (This is a technicality; leave it in;
	# It can help with debugging, but it's not yet important 
	# for you to understand exactly how it works)	m.Params.DualReductions=0
	m.Params.DualReductions=0
	
	# Solve
	m.optimize()
	# Print out the relevant results
	printSolution()