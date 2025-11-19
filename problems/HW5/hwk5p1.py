import gurobipy as gp
from gurobipy import GRB

# Create model
m = gp.Model("lp_path")

# Arcs
arcs = ["S1", "S2", "S7",
        "15", "23", "24", "13",
        "45", "46",
        "78",
        "3F", "5F", "6F", "8F"]

# Variables: 0 <= x_ij <= 1
x = m.addVars(arcs, lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS, name="x")

# Objective:
# 5x13 + x23 + x24 + x45 + x46 + 4x78 + 3x3F + 2x5F + x6F + 3x8F
m.setObjective(
    5 * x["13"] +
    1 * x["23"] +
    1 * x["24"] +
    1 * x["45"] +
    1 * x["46"] +
    4 * x["78"] +
    3 * x["3F"] +
    2 * x["5F"] +
    1 * x["6F"] +
    3 * x["8F"],
    GRB.MAXIMIZE
)

# Constraints

# x_S1 + x_S2 + x_S7 = 1
m.addConstr(x["S1"] + x["S2"] + x["S7"] == 1, "start")

# x_15 - x_S1 = 0
m.addConstr(x["15"] - x["S1"] == 0, "node1")

# x_23 + x_24 - x_S2 = 0
m.addConstr(x["23"] + x["24"] - x["S2"] == 0, "node2")

# x_3F + x_13 - x_23 = 0
m.addConstr(x["3F"] - x["13"] - x["23"] == 0, "node3")

# x_45 + x_46 - x_24 = 0
m.addConstr(x["45"] + x["46"] - x["24"] == 0, "node4")

# x_5F - x_45 = 0
m.addConstr(x["5F"] - x["45"] == 0, "node5")

# x_6F - x_46 = 0
m.addConstr(x["6F"] - x["46"] == 0, "node6")

# x_78 - x_S7 = 0
m.addConstr(x["78"] - x["S7"] == 0, "node7")

# x_8F - x_78 = 0
m.addConstr(x["8F"] - x["78"] == 0, "node8")

# -x_3F - x_5F - x_6F - x_8F = -1   (equivalently x_3F + x_5F + x_6F + x_8F = 1)
m.addConstr(x["3F"] + x["5F"] + x["6F"] + x["8F"] == 1, "sinkF")

# Optimize
m.optimize()

# Print solution
if m.status == GRB.OPTIMAL:
    print(f"Optimal objective value: {m.objVal}")
    for a in arcs:
        print(f"x_{a} = {x[a].X}")
