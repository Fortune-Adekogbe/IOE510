# hwk6p3b
import gurobipy as gp
from gurobipy import GRB

def solve(depots,s,d,c, B):
    # Define your model here
    model = gp.Model("hwk6p3bModel")
    S = [[i for i in depots if i != j] for j in depots]

    # Decision variables
    x = model.addVars(depots, depots, vtype=GRB.INTEGER, lb=0, name="x")
    z = model.addVars(depots, vtype=GRB.INTEGER, lb=0, name="z")
    
    model.setObjective(
        gp.quicksum(z[j] for j in depots),
        GRB.MINIMIZE
    )

    model.addConstrs(
		(gp.quicksum(x[j,i] for i in S[j-1]) - gp.quicksum(x[i,j] for i in S[j-1]) - z[j] <= (s[j] - d[j])  for j in depots),
		name="flow_balance"
	)

    model.addConstr(
        gp.quicksum(gp.quicksum(c[(i,j)]*x[i,j] for i in S[j-1]) for j in depots) <= B,
        name="within_budget"
   )

    # Solve the model
    model.optimize()

    # Output the solve status
    print("***** Gurobi solve status:", model.status)

    if model.status != GRB.Status.OPTIMAL:
        print("***** Problem instance does not have an optimal solution")
    else:
        print(" ")
        print(f"Total unmet demand is {model.ObjVal} bikes.")
        for j in depots:
            for i in S[j-1]:
                if x[i,j].X > 0:
                    print(f"{int(x[i,j].X)} ride(s) from depot {i} to depot {j}.")