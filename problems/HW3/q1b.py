import gurobipy as gp
from gurobipy import GRB

def solve():
    m = gp.Model(name="Q1b")

    x1_i = m.addVar()
    x2_i = m.addVar()
    x1_ii = m.addVar()
    x2_ii = m.addVar()

    x3 = m.addVar()
    x4 = m.addVar()

    m.addConstr((x1_i + x2_i) - (x1_ii + x2_ii) - x4 == -1, name="sum_lb")
    m.addConstr((x1_i + x2_i) - (x1_ii + x2_ii) + x3 == 1,  name="sum_ub")

    m.setObjective(
       (x1_i + x2_i) - (x1_ii + x2_ii), 
        GRB.MINIMIZE
    )

    def printSolution():
        if m.status == GRB.OPTIMAL:
            print(f"\nObjective: {m.ObjVal:g}")
            print(f"x1_i = {x1_i.X}\nx2_i = {x2_i.X}")
            print(f"x1_ii = {x1_ii.X}\nx2_ii = {x2_ii.X}")
            print(f"x3 = {x3.X}\nx4 = {x4.X}")
        else:
            print("no solution...")
    # Solve
    m.optimize()
    printSolution()

solve()

