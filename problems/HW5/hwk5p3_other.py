# hwk5p3
import itertools # Python toolpack; used in part to easily define variables with multiple subscripts
import numpy as np
import gurobipy as gp
from gurobipy import GRB

# Is the win record vector possible?
# Implementation for n=4 teams and k=3 games between each pair of teams

Supplies={
	# team i: -w_i,
	1: -4,
	2: -5,
	3: -4,
	4: -5,
	# team combo: k,
	12: 3,
	13: 3,
	14: 3,
	23: 3,
	24: 3,
	34: 3
}


ArcCosts={
	(12,1):0,
	(13,1):0,
	(14,1):0,
	(12,2):0,
	(23,2):0,
	(24,2):0,
	(13,3):0,
	(23,3):0,
	(34,3):0,
	(14,4):0,
	(24,4):0,
	(34,4):0
}

Nodes=list(Supplies.keys()) # get node list from supply data 
Arcs=list(ArcCosts.keys()) # get arc list from capacities data

# Define your model here

model = gp.Model("hwk5p3_win_record_mcf")


x= model.addVars(Arcs, name="x", lb=0.0)

model.setObjective(
    gp.quicksum(ArcCosts[i, j] * x[i, j] for i, j in Arcs),
    GRB.MINIMIZE
)

for node in Nodes:
	outgoing = gp.quicksum(x[i,j] for i,j in Arcs if i == node)
	incoming = gp.quicksum(x[i,j] for i,j in Arcs if j == node)

	print(outgoing - incoming)
	
	model.addConstr(
		(outgoing - incoming) == Supplies[node], name=f"flow_balance_{node}"
	)

# Optimize
model.optimize()

# Output the solve status
print("***** Gurobi solve status:", model.status)

if model.status != GRB.Status.OPTIMAL:
	print("***** Problem instance does not have an optimal solution") 
else:
	print(" ") 
	print("***** Flows:")
	for (i,j) in Arcs:
		t1, t2 = str(i)
        # print the number of win by team i in some game against team j
		print(f"Team {j} wins team {t2 if int(t2) != j else t1} {x[i,j].X} times.")