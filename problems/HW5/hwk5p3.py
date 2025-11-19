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

Nodes = list(Supplies.keys()) # get node list from supply data 
Arcs = list(ArcCosts.keys())  # get arc list from cost data

# Define your model here
model = gp.Model("sports_league_win_record")

# Decision variables
x = model.addVars(Arcs, lb=0.0, name="x")

# Objective
model.setObjective(
    gp.quicksum(ArcCosts[a] * x[a] for a in Arcs),
    GRB.MINIMIZE
)

# Flow balance constraints
for i in Nodes:
    outflow = gp.quicksum(x[a] for a in Arcs if a[0] == i)
    inflow  = gp.quicksum(x[a] for a in Arcs if a[1] == i)
    model.addConstr(outflow - inflow == Supplies[i], name=f"flow_{i}")

# Solve the model
model.optimize()

# Output the solve status
print("***** Gurobi solve status:", model.status)

if model.status != GRB.Status.OPTIMAL:
    print("***** Problem instance does not have an optimal solution")
else:
    print(" ")
    print("***** Flows (wins by team against opponent):")
    for (pair_node, team) in Arcs:
        val = x[pair_node, team].X
        if val > 1e-6:
            # get the two teams
            t1 = pair_node // 10
            t2 = pair_node % 10
            opponent = t2 if team == t1 else t1
            print(f"Team {team} wins {int(round(val))} games against team {opponent}")
