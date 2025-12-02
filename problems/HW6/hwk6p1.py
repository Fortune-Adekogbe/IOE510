import numpy as np
import gurobipy as gp
from gurobipy import GRB
from copy import deepcopy
from collections import deque

queue = deque()

env = gp.Env(empty=True)
env.setParam("LogToConsole", 0) # Suppress console output
env.start()

v = [19, 10, 15, 3]
B = 12
w = [5,3,8,7]

lb = -np.inf
ub = np.inf

class Node():
    def __init__(self):
        self.left = None
        self.right = None
        self.lb = None
        self.ub = None
        self.branching_constraints = []
        self.solution = ""
        self.status = ""

    def __str__(self):
        branching_info = ""
        for i,j in self.branching_constraints:
            branching_info += f"x[{i}] == {j}; "
        branching_info = branching_info.rstrip("; ")

        print(branching_info)
        print(f"lb: {self.lb}, ub: {self.ub}")

        print(self.solution)
        print(self.status)
        return ""


root = Node()
root.lb = -np.inf
root.ub = np.inf
global_lb = -np.inf
global_ub = np.inf
solution_node = None
queue.append(root)

while queue:
    curr = queue.popleft()

    model = gp.Model("Knapsack", env=env)

    x = model.addMVar(len(w), vtype=GRB.CONTINUOUS, lb=0, ub=1)

    basket = model.addConstr(
        gp.quicksum(w[i]*x[i] for i in range(len(w))) <= B, 
        name="Basket_Limit"
    )

    model.setObjective(
        gp.quicksum(v[i]*x[i] for i in range(len(v))),
        GRB.MAXIMIZE
    )
    branching_info = ""
    for i,j in curr.branching_constraints:
        model.addConstr(x[i] == j)
        branching_info += f"x[{i}] == {j}; "
    branching_info = branching_info.rstrip("; ")

    model.optimize()

    if model.status != GRB.Status.OPTIMAL:
        curr.status = "fathomed because of infeasibility"
    else:
        solution = f"[{', '.join([str(round(float(x[i].X), 4)) for i in range(len(w))])}]"
        curr.solution = solution

        curr.ub = min(model.objVal, curr.ub)

        if curr.ub < global_lb:
            curr.status = "fathomed because current ub is not as good as current lb"
        else:
            global_ub = min(curr.ub, global_ub)

            if not any(x[i].X % 1 for i in range(len(w))):
                curr.lb = max(model.objVal, curr.lb)
                global_lb = max(curr.lb, global_lb)
                curr.status = "fathomed because solution is integer"
                if global_lb == global_ub:
                    solution_node = curr
                    curr.status = "fathomed because this is the solution."
            else:
                curr.status = "branching"
                for i in range(len(w)):
                    if x[i].X % 1 != 0:
                        node1 = Node()
                        node1.lb = curr.lb
                        node1.ub = curr.ub
                        node1.branching_constraints = curr.branching_constraints + [(i, 0)]
                        curr.left = node1

                        node2 = Node()
                        node2.lb = curr.lb
                        node2.ub = curr.ub
                        node2.branching_constraints = curr.branching_constraints + [(i, 1)]
                        curr.right = node2

                        queue.extend([node1, node2])

def branch_and_bound(branching_constraints=[], verbose=True):
    global lb
    global ub

    if lb == ub:
        return
    
    model = gp.Model("Knapsack", env=env)

    x = model.addMVar(len(w), vtype=GRB.CONTINUOUS, lb=0, ub=1)

    basket = model.addConstr(
        gp.quicksum(w[i]*x[i] for i in range(len(w))) <= B, 
        name="Basket_Limit"
    )

    model.setObjective(
        gp.quicksum(v[i]*x[i] for i in range(len(v))),
        GRB.MAXIMIZE
    )
    branching_info = ""
    for i,j in branching_constraints:
        model.addConstr(x[i] == j)
        branching_info += f"x[{i}] == 0; "
    branching_info = branching_info.rstrip("; ")

    model.optimize()

    if model.status != GRB.Status.OPTIMAL:
        print("fathomed because of infeasibility")
    else:
        print(" ")
        if branching_info:
            print(branching_info)
        else:
            print("Root\n")
        print(f"lb = {lb}; ub = {ub}")
        for i in range(len(w)):
                print(f"Item {i+1}: {x[i].X}")

        if model.ObjVal < lb:
            print("fathomed because solution is not as good as current lb")
        else:
            ub = min(model.objVal, ub)
            
            integer_check = True

            for i in range(len(w)):
                if x[i].X % 1 != 0: # implicit fathom if solution is integer
                    integer_check = False
                    bc_1 = deepcopy(branching_constraints)
                    bc_1.append((i, 0))
                    branch_and_bound(branching_constraints=bc_1, verbose=True)

                    bc_2 = deepcopy(branching_constraints)
                    bc_2.append((i, 1))
                    branch_and_bound(branching_constraints=bc_2, verbose=True)
            if integer_check == True:
                print("fathomed because solution is integer")
                lb = max(model.objVal, lb)
def binary_knapsack():
    model = gp.Model("BKnapsack")

    x = model.addMVar(len(w), vtype=GRB.INTEGER, lb=0, ub=1)

    basket = model.addConstr(
        gp.quicksum(w[i]*x[i] for i in range(len(w))) <= B, 
        name="Basket_Limit"
    )

    model.setObjective(
        gp.quicksum(v[i]*x[i] for i in range(len(v))),
        GRB.MAXIMIZE
    )

    model.optimize()

    if model.status != GRB.Status.OPTIMAL:
        ...
    else:
        print(" ")
        for i in range(len(w)):
            print(f"Item {i+1}: {x[i].X}")
            
print("Solution is:", global_ub)
print(solution_node)

def print_branch_and_bound_tree(root):
    def format_constraints(node):
        if not node.branching_constraints:
            return "-"
        return ", ".join(f"x[{i}] == {j}" for i, j in node.branching_constraints)

    def format_label(node):
        output = (
            f"lb={round(node.lb, 4)}, ub={round(node.ub,4)}, "
            f"constraints={format_constraints(node)}, "
        )
        output += (f"solution={node.solution}, " if node.solution else "")
        output += f"status={node.status}"
        return output

    def _print(node, prefix="", is_last=True, tag="root"):
        connector = "└──" if is_last else "├──"
        print(f"{prefix}{connector} {tag}: {format_label(node)}")

        children = []
        if node.left:
            children.append(("L", node.left))
        if node.right:
            children.append(("R", node.right))

        for idx, (child_tag, child) in enumerate(children):
            last_child = (idx == len(children) - 1)
            child_prefix = prefix + ("    " if is_last else "│   ")
            _print(child, child_prefix, last_child, child_tag)

    if root is not None:
        _print(root)

print_branch_and_bound_tree(root)
