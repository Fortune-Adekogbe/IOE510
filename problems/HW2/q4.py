import numpy as np
from itertools import permutations

picks = set(map(lambda a: tuple(sorted(a)), permutations([i for i in range(5)], 2)))
print(picks)
print(len(picks))

A = np.array([
    [1, 0, -5, 0, -1],
    [0, 1, -1, 0, 1],
    [0, 0, -2, 1, 0]
])
b = np.array([5, 4, 2])

def solve_underspecified(free_variables):
    cols = [i for i in range(A.shape[1]) if i not in free_variables]
    B = A[:, cols]
    try:
        x_star = np.linalg.inv(B) @ b
        
    except:
        raise
    return x_star, cols

for pick in picks:
    try:
        x_star, cols = solve_underspecified(pick)
        x = {}
        x[pick[0]+1] = 0
        x[pick[1]+1] = 0
        for i, col in zip(x_star, cols):
            x[col+1] = round(float(i), 2)
        print(f"x{pick[0]+1} = 0, x{pick[1]+1} = 0 ==> (x1, x2, x3, x4, x5) = {(x[1], x[2], x[3], x[4],x[5])}")
    except:
        print(f"x{pick[0]+1} = 0, x{pick[1]+1} = 0 ==> no feasible solution.")