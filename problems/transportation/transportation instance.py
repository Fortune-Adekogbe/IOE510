#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import transportationmodel
import gurobipy as gp
from gurobipy import GRB

# number of plants 
num_plants = 8
# number of warehouses
num_warehouses = 6
# costs for each edge
# This is a two-dimensional list with size num_plants * num_warehouse
# For simplicity, we define all the costs as integer values. For your instance, 
# you can define any costs you like. 
cost = [[3, 1, 1, 2, 3, 1],
        [5, 2, 5, 2, 1, 5],
        [2, 2, 5, 3, 4, 2],
        [5, 4, 5, 5, 4, 5],
        [5, 2, 2, 2, 5, 3],
        [4, 5, 5, 5, 2, 1],
        [1, 1, 1, 5, 3, 5],
        [2, 3, 4, 1, 4, 4]]
# Production capacity. It is a vector with size num_plant
capacity = [3, 8, 5, 9, 9, 6, 13, 15]
# Demand. It is a vector with size num_warehouse
demand = [8, 13, 8, 6, 11, 9]

transportationmodel.solve(num_plants, num_warehouses, cost, capacity, demand)