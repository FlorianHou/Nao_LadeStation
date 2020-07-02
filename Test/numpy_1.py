import numpy as np

a = np.array([
    [2, 0, 0, 0],
    [4, 5, 0, 0],
    [-2, 6.6, 1.2, 0],
    [0, 0, 0, 2]
])
print(a)
print(a.T)

print(a@a.T)