# hwk6p2
import itertools # Python toolpack; used in part to easily define variables with multiple subscripts
import numpy as np
import gurobipy as gp
from gurobipy import GRB

def solve(items, a, boxes, b, Q, K):
    # Define your model here
    model = gp.Model("moving_problem")

    # Decision variables
    x = model.addVars(boxes, items, range(K), vtype=GRB.BINARY, name="x")
    y = model.addVars(range(K), vtype=GRB.BINARY, name="y")

    # Objective
    model.setObjective(
        gp.quicksum(y[k] for k in range(K)),
        GRB.MINIMIZE
    )

    model.addConstrs(
		(y[k] >= x[i,j,k] for j in items for i in boxes for k in range(K)),
		name="linking_xy"
	)

    model.addConstrs(
		(gp.quicksum(x[i,j,k] for i in boxes for k in range(K)) == 1  for j in items),
		name="assignment"
	)

    model.addConstrs(
		(gp.quicksum(a[j]* x[i,j,k] for j in items) <= b[i] for i in boxes for k in range(K)),
		name="box_capacity"
	)

    model.addConstrs(
		(gp.quicksum(a[j]* x[i,j,k] for j in items for i in boxes) <= Q for k in range(K)),
		name="truck_capacity"
	)

    # Solve the model
    model.optimize()

    # Output the solve status
    print("***** Gurobi solve status:", model.status)

    if model.status != GRB.Status.OPTIMAL:
        print("***** Problem instance does not have an optimal solution")
    else:
        print(f"\nOptimal numbr of trips: {model.ObjVal:,.0f}")
        print(" ")
        for k in range(K):
            if y[k].X > 0.5:
                print(f"Trip {k+1}")
                for i in boxes:
                    items_in_box = []
                    for j in items:
                        if x[i, j, k].X > 0.5:
                            items_in_box.append(f"{j} ({a[j]})")
                    if items_in_box:
                        print(f"   Box {i}: {', '.join(items_in_box)}")