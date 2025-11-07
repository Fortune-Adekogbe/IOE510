import gurobipy as gp
from gurobipy import GRB
# import numpy as np

m = gp.Model("hw4q1a")

x1 = m.addVar(name="x1")
x2 = m.addVar(name="x2")
x3 = m.addVar(name="x3")

m.setObjective(200*x1 + 60*x2 + 206*x3, GRB.MAXIMIZE)

cA = m.addConstr(
    3*x1 + x2 + 5*x3 <= 8_000_000, name="cA"
)
cB = m.addConstr(
    5*x1 + x2 + 3*x3 <= 5_000_000, name="cB"
)


m.optimize()

if m.status == GRB.OPTIMAL:
    print("\nOptimal solution:")
    print(f"  x1 = {x1.X:,.0f}")
    print(f"  x2 = {x2.X:,.0f}")
    print(f"  x3 = {x3.X:,.0f}")

    print(f"\nOptimal objective value: ${m.ObjVal:,.0f}")

    print("\nConstraint slacks:")
    print(f"  crude_A slack = {cA.Slack:,.0f}")
    print(f"  crude_B slack = {cB.Slack:,.0f}")

    print("\nDual prices:")
    print(f"  crude_A Pi = {cA.Pi:.2f}")
    print(f"  crude_B Pi = {cB.Pi:.2f}")
else:
    print("Model did not solve to optimality.")