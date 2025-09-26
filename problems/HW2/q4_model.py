import gurobipy as gp
from gurobipy import GRB
import numpy as np


A = np.array([
    [1, 0, -5, 0, 1],
    [0, 1, -1, 0, 1],
    [0, 0, -2, 1, 0]
])
b = np.array([5, 4, 2])

c = np.array([0,0,-2,0,3])

m = gp.Model("q4")

x = m.addMVar(5)

m.setObjective(c @ x, GRB.MINIMIZE)

m.addMConstr(
    A, x,'=', b
)

m.optimize()

if m.status == GRB.OPTIMAL:
    print(f"\nCost: {m.ObjVal:g}")
    for i in range(5):
        print(x[i].X)