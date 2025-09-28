import gurobipy as gp
from gurobipy import GRB
import numpy as np



P = np.array(
    [[300, 160, 360],
    [220, 130, 280],
    [100, 80, 140]]
)

D = np.array(
    [[4, 8, 3],
    [8, 13, 10],
    [22, 20, 18]]
)

N = 30
num_fare_class=3
num_type_passenger=3

fare_map = {i:j for i,j in zip(range(num_fare_class), ["Y", "M", "B"])}
passenger_map = {i:j for i,j in zip(range(num_type_passenger), ["A-C", "C-B", "A-B"])}

def solve(num_fare_class=3, num_type_passenger=3, N=30):
    m = gp.Model(name="airline")

    x = m.addVars(
        num_fare_class, 
        num_type_passenger, 
        vtype=GRB.INTEGER,
        name="n_tickets"
    )

    m.addConstr(
        gp.quicksum(x[i,j] for i in range(num_fare_class) for j in range(num_type_passenger) if j != 0) <= N,
        name="second_leg"  
    )

    m.addConstr(
        gp.quicksum(x[i,j] for i in range(num_fare_class) for j in range(num_type_passenger) if j != 1) <= N,
        name="first_leg" 
    )

    m.addConstrs(
        (x[i,j] <= D[i,j] for i in range(num_fare_class) for j in range(num_type_passenger)), 
    )


    m.setObjective(
       gp.quicksum(P[i,j] * x[i,j] for i in range(num_fare_class) for j in range(num_type_passenger)), 
        GRB.MAXIMIZE
    )

    def printSolution():
        if m.status == GRB.OPTIMAL:
            print(f"\nRevenue: {m.ObjVal:g}")
            
            for i in range(num_fare_class):
                for j in range(num_type_passenger):
                    if x[i,j].X > 0:
                        print("number of tickets for", (fare_map[i], passenger_map[j]), "is", x[i,j].X)
        else:
            print("no solution...")
    # Solve
    m.optimize()
    printSolution()

solve()

