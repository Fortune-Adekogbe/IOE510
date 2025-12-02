#! /usr/bin/python
# Provides the data for moving problem

import gurobipy as gp
from gurobipy import GRB
import hwk6p2Model

# ---------------- Instance ----------------
# Items (name -> size)
items, a = gp.multidict({
    'I1': 57, 'I2': 52, 'I3': 49, 'I4': 44, 'I5': 41, 'I6': 38,
    'I7': 35, 'I8': 33, 'I9': 29, 'I10': 27, 'I11': 24, 'I12': 18
})

# Boxes (reusable each trip) (name -> capacity)
boxes, b = gp.multidict({
    'B1': 60, 'B2': 60, 'B3': 50, 'B4': 40, 'B5': 35
})

# Truck capacity
Q = 145

# A safe a priori upper bound on number of trips
K = len(items)   # e.g., move one item per trip (reusing any single box)

print('\n=== Moving instance summary ===')
print(f'Items (n={len(items)}):')
for j in items:
    print(f'  {j}: size {a[j]}')
print(f'\nBoxes (m={len(boxes)}), reusable each trip:')
for i in boxes:
    print(f'  {i}: capacity {b[i]}')
print(f'\nTruck capacity Q = {Q}')
print(f'Upper bound on trips K = {K} (safe)\n')

# ---------------- Solve ----------------
hwk6p2Model.solve(items, a, boxes, b, Q, K)