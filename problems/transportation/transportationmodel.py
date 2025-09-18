#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gurobipy as gp
from gurobipy import GRB

def solve(num_plants, num_warehouses, cost, capacity, demand):
    # Name your Model
    m = gp.Model("transportation")
    
    # Transportation decision variables: transport[w,p] captures
    # the optimal quantity to transport from plant p to warehouse w
    transport = m.addVars(num_plants, num_warehouses, name="transportation_amount")

    # Set objective function to minimize the total cost
    m.setObjective(
        gp.quicksum(cost[i][j] * transport[i,j] for i in range(num_plants)
                    for j in range(num_warehouses)),
                    GRB.MINIMIZE
    )
    # Add demand constraints for each warehouse
    m.addConstrs(
        ((gp.quicksum(transport[i,j] for i in range(num_plants)) >= demand[j]) for j in range(num_warehouses)),
        name="demand",
    )
    # Add capacity constraints for each plant
    m.addConstrs(
        ((gp.quicksum(transport[i,j] for j in range(num_warehouses)) <= capacity[i]) for i in range(num_plants)),
        name="supply",
    )
    # Solution print out
    def printSolution():
        if m.status == GRB.OPTIMAL:
            print(f"\nCost: {m.ObjVal:g}")
            for i in range(num_plants):
                for j in range(num_warehouses):
                    if transport[i,j].X > 0:
                        print("non-zero unit on arc", (i,j), "is", transport[i,j].X)
        else:
            print("no solution...")
    # Solve
    m.optimize()
    printSolution()