import re
from gurobipy import Model, GRB, quicksum

# Arcs and costs (i, j) : c_ij
arcs = {
    (1, 2): 12,
    (2, 6): 32,
    (2, 3): 18,
    (3, 7): 30,
    (3, 4): 13,
    (4, 10): 38,
    (5, 1): 20,
    (5, 6): 18,
    (6, 2): 32,
    (6, 5): 18,
    (6, 7): 28,
    (6, 9): 25,
    (7, 3): 30,
    (7, 6): 28,
    (7, 9): 21,
    (7, 10): 49,
    (8, 5): 18,
    (8, 9): 36,
    (9, 6): 25,
    (9, 7): 21,
    (9, 8): 36,
    (9, 10): 40,
    (10, 7): 49,
    (10, 8): 28,
    (10, 9): 40,
}

# Create model
m = Model("primal_LP")

# Decision variables x_ij >= 0
x = m.addVars(arcs.keys(), name="x", lb=0.0)

# Objective
m.setObjective(
    quicksum(arcs[i, j] * x[i, j] for i, j in arcs),
    GRB.MINIMIZE
)

# Flow balance constraints

# Node 1: x_12 - x_51 = 1
m.addConstr(x[1, 2] - x[5, 1] == 1, name="node1")

# Node 2: x_26 + x_23 - x_12 - x_62 = 0
m.addConstr(x[2, 6] + x[2, 3] - x[1, 2] - x[6, 2] == 0, name="node2")

# Node 3: x_34 + x_37 - x_23 - x_73 = 0
m.addConstr(x[3, 4] + x[3, 7] - x[2, 3] - x[7, 3] == 0, name="node3")

# Node 4: x_4,10 - x_34 = 0
m.addConstr(x[4, 10] - x[3, 4] == 0, name="node4")

# Node 5: x_51 + x_56 - x_65 - x_85 = 0
m.addConstr(x[5, 1] + x[5, 6] - x[6, 5] - x[8, 5] == 0, name="node5")

# Node 6: x_62 + x_65 + x_67 + x_69 - x_26 - x_56 - x_96 - x_76 = 0
m.addConstr(
    x[6, 2] + x[6, 5] + x[6, 7] + x[6, 9]
    - x[2, 6] - x[5, 6] - x[9, 6] - x[7, 6] == 0,
    name="node6"
)

# Node 7: x_73 + x_76 + x_79 + x_7,10 - x_37 - x_67 - x_97 - x_10,7 = 0
m.addConstr(
    x[7, 3] + x[7, 6] + x[7, 9] + x[7, 10]
    - x[3, 7] - x[6, 7] - x[9, 7] - x[10, 7] == 0,
    name="node7"
)

# Node 8: x_85 + x_89 - x_98 - x_10,8 = 0
m.addConstr(
    x[8, 5] + x[8, 9] - x[9, 8] - x[10, 8] == 0,
    name="node8"
)

# Node 9: x_96 + x_97 + x_98 + x_9,10 - x_69 - x_79 - x_89 - x_10,9 = 0
m.addConstr(
    x[9, 6] + x[9, 7] + x[9, 8] + x[9, 10]
    - x[6, 9] - x[7, 9] - x[8, 9] - x[10, 9] == 0,
    name="node9"
)

# Node 10: x_10,8 + x_10,9 + x_10,7 - x_4,10 - x_7,10 - x_9,10 = -1
m.addConstr(
    x[10, 8] + x[10, 9] + x[10, 7]
    - x[4, 10] - x[7, 10] - x[9, 10] == -1,
    name="node10"
)

# Optimize
m.optimize()

if m.status == GRB.OPTIMAL:
    print(f"\n(a) Optimal primal objective value: {m.ObjVal:,.0f}")

    arcs_on_shortest_path = ([xij.VarName for xij in m.getVars() if xij.X == 1])
    shortest_path = []
    seen = set()
    for arc in arcs_on_shortest_path:
        i, j = re.findall(r'\d+', arc)
        i, j = int(i), int(j)
        if i not in seen:
            shortest_path.append(i)
            seen.add(i)
        if j not in seen:
            shortest_path.append(j)
            seen.add(j)
    shortest_path = sorted(shortest_path)

    print(f"Shortest Path: {shortest_path}")
    print(f"\t\t{' --> '.join(map(str, shortest_path))}")
else:
    print("Model did not solve to optimality.")


# Nodes
N = range(1, 11)

# Model
m2 = Model("dual_LP")

# dual values w_i are unrestricted (free)
w = m2.addVars(N, lb=-GRB.INFINITY, name="w")

# Objective: min w1 - w10
m2.setObjective(w[1] - w[10], GRB.MAXIMIZE)

# Constraints: w_i - w_j <= c_ij for each arc (i,j)
for (i, j), c in arcs.items():
    m2.addConstr(w[i] - w[j] <= c, name=f"arc_{i}_{j}")

m2.optimize()

if m2.status == GRB.OPTIMAL:
    print(f"\n(b) Optimal dual; objective value: {m2.ObjVal:,.0f}")
    for i in N:
        print(f"w_{i}: {w[i].X}")
else:
    print("Model did not solve to optimality.")