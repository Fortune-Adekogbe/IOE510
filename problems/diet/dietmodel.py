#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gurobipy as gp
from gurobipy import GRB

def solve(categories, minNutrition, maxNutrition, foods, cost, nutritionValues):
    # Name your Model
    m = gp.Model("diet")
    # Create decision variables for the foods to buy
    buy = m.addVars(foods, name="buy")
    
    # The objective is to minimize the costs
    m.setObjective(buy.prod(cost), GRB.MINIMIZE)
    
    # Nutrition constraints
    m.addConstrs(
        (gp.quicksum(nutritionValues[f,c]*buy[f] for f in foods) >= minNutrition[c] for c in categories),
        name="min",
    )

    m.addConstrs(
        (gp.quicksum(nutritionValues[f,c]*buy[f] for f in foods) <= maxNutrition[c]
        for c in categories),
        name="max",
    )
    
    # Solution print out
    def printSolution():
        if m.status == GRB.OPTIMAL:
            print(f"\nCost: {m.ObjVal:g}")
            for f in foods:
                if buy[f].X > 0.001:
                    print(f"{f} {buy[f].X} ")

            
        else:
            print("No solution.")
            
    # Solve
    m.optimize()
    printSolution()