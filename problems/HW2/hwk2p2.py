#! /usr/bin/python
# Solves problem instances in IOE 510F25 homework 2 problem 2
# With the data provided in the homework
# Uses models for parts (a), (b), and (c) implemented in separate .py files

import hwk2p2aModel
import hwk2p2bModel
import hwk2p2cModel
import numpy as np
import gurobipy as gp
from gurobipy import GRB


sugars, content=gp.multidict({
    'Cane': 52, 'Corn': 56, 'Beet': 59
})

suppliers, cost=gp.multidict({
    'A':10,
    'B':11,
    'C':12,
    'D':13,
    'E':14,
    'F':12,
    'G':15
})

percentage={
    ('Cane','A'):   10,
    ('Corn','A'):   30,
    ('Beet','A'):   60,
    
    ('Cane','B'):   10,
    ('Corn','B'):   40,
    ('Beet','B'):   50,
    
    ('Cane','C'):   20,
    ('Corn','C'):   40,
    ('Beet','C'):   40,
    
    ('Cane','D'):   30,
    ('Corn','D'):   20,
    ('Beet','D'):   50,
    
    ('Cane','E'):   40,
    ('Corn','E'):   60,
    ('Beet','E'):   0,
    
    ('Cane','F'):   20,
    ('Corn','F'):   70,
    ('Beet','F'):   10,
    
    ('Cane','G'):   60,
    ('Corn','G'):   10,
    ('Beet','G'):   30,
    
}

minPurchase=10

l=30
u=37

print('\nPart (a):')
hwk2p2aModel.solve(sugars, content, suppliers, cost, percentage)

print('\nPart (b):')
hwk2p2bModel.solve(sugars, content, suppliers, cost, percentage, minPurchase)

print('\nPart (c):')
hwk2p2cModel.solve(sugars, content, suppliers, cost, percentage, l, u)