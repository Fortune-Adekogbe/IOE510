import numpy as np

A = np.array(
    [
        [1, 5, 1, -3, 3],
        [3, 1, -1, -1, 1],
        [0, 1, 1, -2, 0],
    ]
)

b = np.array([6, 2, 4])
rhs = np.array([0, 0, 0])

A_with_norm_row = np.array(
    [
        [1, 5, 1, -3, 3],
        [3, 1, -1, -1, 1],
        [0, 1, 1, -2, 0],
        [1, 1, 1, 1, 1]
    ]
)
rhs_with_norm_row = np.array([0, 0, 0, 1])

for free_var in range(A.shape[1]):
    A_star = A_with_norm_row[:, [i for i in range(A.shape[1]) if i is not free_var]]
    print(f"\nSet d{free_var+1} = 0")
    print("A:\n", A_star)
    d_star = np.linalg.inv(A_star) @ rhs_with_norm_row
    d = np.insert(d_star, free_var, 0).round(4)
    print("d:\n", d)