from sympy import pretty
from math_engine.math_engine import matrix_rref


matrix = [
    [1, 1, 1, 1, 1, 5],
    [0, 2, 1, -2, 1, 1],
    [0, 0, 4, 1, -2, 1],
    [0, 0, 0, 1, -3, 0],
    [0, 0, 0, 0, 2, 2]
]

result, pivots = matrix_rref(matrix)

print("\nRREF:")
print(pretty(result))

print("\nSolutions:")

num_variables = result.cols - 1

for i in range(num_variables):
    print(f"x{i + 1} = {result[i, -1]}")