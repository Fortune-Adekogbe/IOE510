# hwk6p3a
import gurobipy as gp
from gurobipy import GRB

def solve(depots,s,d,c):
    # Define your model here
    model = gp.Model("hwk6p3aModel")
    S = [[i for i in depots if i != j] for j in depots]

    # Decision variables
    x = model.addVars(depots, depots, vtype=GRB.INTEGER, lb=0, name="x")
    
    model.setObjective(
        gp.quicksum(gp.quicksum(c[(i,j)]*x[i,j] for i in S[j-1]) for j in depots),
        GRB.MINIMIZE
    )

    model.addConstrs(
		(gp.quicksum(x[j,i] for i in S[j-1]) - gp.quicksum(x[i,j] for i in S[j-1]) <= (s[j] - d[j])  for j in depots),
		name="flow_balance"
	)

    # Solve the model
    model.optimize()

    # Output the solve status
    print("***** Gurobi solve status:", model.status)

    if model.status != GRB.Status.OPTIMAL:
        print("***** Problem instance does not have an optimal solution")
    else:
        print(" ")
        print(f"Total rebalancing cost is ${model.ObjVal}.")
        for j in depots:
            for i in S[j-1]:
                if x[i,j].X > 0:
                    print(f"{int(x[i,j].X)} ride(s) from depot {i} to depot {j}.")