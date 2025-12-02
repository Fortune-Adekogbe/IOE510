#!/usr/bin/env python3

# Provides the data for bike rebalancing problem

import gurobipy as gp
from gurobipy import GRB
import hwk6p3aModel
import hwk6p3bModel

depots=[1,2,3,4]
s={1: 8, 2: 6, 3: 2,4: 4}
d={1: 7,2: 3,3: 5,4: 5}


# Relocation fee from i to j
# (i,j): c_{ij}
c = {
	(1,1):	0, 
	(1,2):	5, 
	(1,3):	1.5, 
	(1,4):	4, 
	(2,1):	5, 
	(2,2):	0, 
	(2,3):	3, 
	(2,4):	2, 
	(3,1):	1.5, 
	(3,2):	3, 
	(3,3):	0, 
	(3,4):	4.5, 
	(4,1):	4, 
	(4,2):	2, 
	(4,3):	2, 
	(4,4):	0, 
}

B=6

print('\nPart (a):')
hwk6p3aModel.solve(depots,s,d,c)

print('\nPart (b):')
hwk6p3bModel.solve(depots,s,d,c,B)
